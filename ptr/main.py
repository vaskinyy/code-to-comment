"""Implementation of Pointer networks: http://arxiv.org/pdf/1506.03134v1.pdf.
"""


from __future__ import absolute_import, division, print_function

import random

import numpy as np
import tensorflow as tf
from tensorflow.models.rnn import rnn, rnn_cell, seq2seq
from dataset import DataGenerator
from pointer import pointer_decoder

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_integer('batch_size', 32, 'Batch size.  ')
flags.DEFINE_integer('max_steps', 10, 'Number of numbers to sort.  ')
flags.DEFINE_integer('rnn_size', 32, 'RNN size.  ')


class PointerNetwork(object):

    def __init__(self, max_len, input_size, size, num_layers, max_gradient_norm,
                 batch_size, learning_rate, learning_rate_decay_factor):
        """Create the network. A simplified network that handles only sorting.

        Args:
            max_len: maximum length of the model.
            input_size: size of the inputs data.
            size: number of units in each layer of the model.
            num_layers: number of layers in the model.
            max_gradient_norm: gradients will be clipped to maximally this norm.
            batch_size: the size of the batches used during training;
                the model construction is independent of batch_size, so it can be
                changed after initialization if this is convenient, e.g., for decoding.
            learning_rate: learning rate to start with.
            learning_rate_decay_factor: decay learning rate by this much when needed.
        """
        self.batch_size = batch_size
        self.learning_rate = tf.Variable(float(learning_rate), trainable=False)
        self.learning_rate_decay_op = self.learning_rate.assign(
            self.learning_rate * learning_rate_decay_factor)
        self.global_step = tf.Variable(0, trainable=False)

        cell = rnn_cell.GRUCell(size)
        if num_layers > 1:
            cell = rnn_cell.MultiRNNCell([single_cell] * num_layers)

        self.encoder_inputs = []
        self.decoder_inputs = []
        self.decoder_targets = []
        self.target_weights = []
        for i in range(max_len):
            self.encoder_inputs.append(tf.placeholder(
                tf.float32, [batch_size, input_size], name="EncoderInput%d" % i))

        for i in range(max_len + 1):
            self.decoder_inputs.append(tf.placeholder(
                tf.float32, [batch_size, input_size], name="DecoderInput%d" % i))
            self.decoder_targets.append(tf.placeholder(
                tf.float32, [batch_size, max_len + 1], name="DecoderTarget%d" % i))  # one hot
            self.target_weights.append(tf.placeholder(
                tf.float32, [batch_size, 1], name="TargetWeight%d" % i))

        # Encoder

        # Need for attention
        encoder_outputs, final_state = rnn.rnn(cell, self.encoder_inputs, dtype=tf.float32)

        # Need a dummy output to point on it. End of decoding.
        encoder_outputs = [tf.zeros([FLAGS.batch_size, FLAGS.rnn_size])] + encoder_outputs

        # First calculate a concatenation of encoder outputs to put attention on.
        top_states = [tf.reshape(e, [-1, 1, cell.output_size])
                      for e in encoder_outputs]
        attention_states = tf.concat(1, top_states)

        with tf.variable_scope("decoder"):
            outputs, states, _ = pointer_decoder(
                self.decoder_inputs, final_state, attention_states, cell)

        with tf.variable_scope("decoder", reuse=True):
            predictions, _, inps = pointer_decoder(
                self.decoder_inputs, final_state, attention_states, cell, feed_prev=True)

        self.predictions = predictions

        self.outputs = outputs
        self.inps = inps
        # move code below to a separate function as in TF examples

    def create_feed_dict(self, encoder_input_data, decoder_input_data, decoder_target_data):
        feed_dict = {}
        for placeholder, data in zip(self.encoder_inputs, encoder_input_data):
            feed_dict[placeholder] = data

        for placeholder, data in zip(self.decoder_inputs, decoder_input_data):
            feed_dict[placeholder] = data

        for placeholder, data in zip(self.decoder_targets, decoder_target_data):
            feed_dict[placeholder] = data

        for placeholder in self.target_weights:
            feed_dict[placeholder] = np.ones([self.batch_size, 1])

        return feed_dict

    def step(self):

        loss = 0.0
        for output, target, weight in zip(self.outputs, self.decoder_targets, self.target_weights):
            loss += tf.nn.softmax_cross_entropy_with_logits(output, target) * weight

        loss = tf.reduce_mean(loss)

        test_loss = 0.0
        for output, target, weight in zip(self.predictions, self.decoder_targets, self.target_weights):
            test_loss += tf.nn.softmax_cross_entropy_with_logits(output, target) * weight

        test_loss = tf.reduce_mean(test_loss)

        optimizer = tf.train.AdamOptimizer()
        train_op = optimizer.minimize(loss)
        
        train_loss_value = 0.0
        test_loss_value = 0.0
        
        correct_order = 0
        all_order = 0

        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.3)
        with tf.Session(config = tf.ConfigProto(gpu_options = gpu_options)) as sess:
            merged = tf.merge_all_summaries()
            writer = tf.train.SummaryWriter("/tmp/pointer_logs", sess.graph)
            init = tf.initialize_all_variables()
            sess.run(init)
            for i in range(10000):
                encoder_input_data, decoder_input_data, targets_data = dataset.next_batch(
                    FLAGS.batch_size, FLAGS.max_steps)

                # Train
                feed_dict = self.create_feed_dict(
                    encoder_input_data, decoder_input_data, targets_data)
                d_x, l = sess.run([loss, train_op], feed_dict=feed_dict)
                train_loss_value = 0.9 * train_loss_value + 0.1 * d_x
                                
                if i % 100 == 0:
                    print("Train: ", train_loss_value)

                encoder_input_data, decoder_input_data, targets_data = dataset.next_batch(
                    FLAGS.batch_size, FLAGS.max_steps, train_mode=False)
                # Test
                feed_dict = self.create_feed_dict(
                    encoder_input_data, decoder_input_data, targets_data)
                inps_ = sess.run(self.inps, feed_dict=feed_dict)

                predictions = sess.run(self.predictions, feed_dict=feed_dict)
                
                test_loss_value = 0.9 * test_loss_value + 0.1 * sess.run(test_loss, feed_dict=feed_dict)

                if i % 100 == 0:
                    print("Test: ", test_loss_value)

                predictions_order = np.concatenate([np.expand_dims(prediction , 0) for prediction in predictions])
                predictions_order = np.argmax(predictions_order, 2).transpose(1, 0)[:,0:FLAGS.max_steps]
                    
                input_order = np.concatenate([np.expand_dims(encoder_input_data_ , 0) for encoder_input_data_ in encoder_input_data])
                input_order = np.argsort(input_order, 0).squeeze().transpose(1, 0)+1
                
                correct_order += np.sum(np.all(predictions_order == input_order,
                                    axis=1))
                all_order += FLAGS.batch_size

                if i % 100 == 0:
                    print(correct_order / all_order)
                    correct_order = 0
                    all_order = 0
                    
                    #print(encoder_input_data, decoder_input_data, targets_data)
                    #print(inps_)

if __name__ == "__main__":
    # TODO: replace other with params
    pointer_network = PointerNetwork(FLAGS.max_steps, 1, FLAGS.rnn_size,
                                     1, 5, FLAGS.batch_size, 1e-2, 0.95)
    dataset = DataGenerator()
    pointer_network.step()
