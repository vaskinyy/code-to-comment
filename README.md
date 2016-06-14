# comment-generation
Set of (Tensorflow) implementations which generate comments from code. Thesis for the B.sc. AI. 

# How to execute:
## Seq2seq: 
- Enter tf: source ~/tensorflow/bin/activate
- Execute code: python translate.py --size=256 --num_layers=3 --steps_per_checkpoint=50 --bleu
- Or interactive mode (only works when the model has been trained): python translate.py --size=350 --num_layers=3 --step_per_checkpoint=50 --decode

### Options
- add --evaluate to see the score with a trained model on the development file (default False)
- add --size=XX to change size of LSTM layer to XX (default 256)
- add --num_layers=XX to change number of LSTM layers to XX (default 2)
- add --steps_per_checkpoint=XX to change amount of steps per evaluation output to XX(default 200)
- add --code_vocab_size=XX to change the code vocabulary size to XX (default 3000)
- add --en_vocab_size=XX to change the English vocabulary size to XX (default 3000)
- add --lstm=XX to change the LSTM type to normal or attention (default attention)
- uncomment the 'embedding_rnn_seq2seq' part in seq2seq_model.py to enable the embedded_seq2seq lstm without attention


# Results:

## Data info
### Distribution among buckets:
English buckets:
- Bucket 10 has 6251 items
- Bucket 15 has 3049 items
- Bucket 25 has 3791 items
- Bucket 50 has 1790 items
- Bucket 100 has 146 items (not implemented)
- Bucket 2000 has 17 items (not implemented) 


Code buckets:
- Bucket 5 has 3582 items  
- Bucket 10 has 6211 items
- Bucket 20 has 4109 items
- Bucket 40 has 946 items
- Bucket 100 has 178 items (not implemented)
- Bucket 2000 has 18 items (not implemented)



## Seq2seq 

### Python / Django dataset

#### Default: vocab=3000, layers=2 and size=256, lstm=attention
- global step 10400 learning rate 0.5000 step-time 0.23 perplexity 1.09
-  eval: bucket 0 perplexity 2.31
-  eval: bucket 1 perplexity 2.22
-  eval: bucket 2 perplexity 8.32
-  eval: bucket 3 perplexity 24.29
- BLEU = 14.19(BP=1.000, ratio=1.071, hyp_len=41721, ref_len=38963)
-  1-gram: 39.1
-  2-gram: 20.1
-  3-gram:11.3
-  4-gram: 4.6

#### Different layers / size

##### layers=2,  size = 512
- global step 6600 learning rate 0.4950 step-time 0.21 perplexity 1.28
-  eval: bucket 0 perplexity 1.30
-  eval: bucket 1 perplexity 3.13
-  eval: bucket 2 perplexity 5.72
-  eval: bucket 3 perplexity 15.49
- BLEU = 13.94 (Bravity Penalty=1.000, Length ratio=1.042, Translated length=40586, Reference length=38963)
-  1-gram: 39.0
-  2-gram: 20.1
-  3-gram:11.1
-  4-gram: 4.3

  
##### layers=2, size=1000
- global step 4400 learning rate 0.5000 step-time 0.34 perplexity 1.33
-  eval: bucket 0 perplexity 1.34
-  eval: bucket 1 perplexity 2.65
-  eval: bucket 2 perplexity 5.15
-  eval: bucket 3 perplexity 14.88
- BLEU = 13.39 (Bravity Penalty=1.000, Length ratio=1.029, Translated length=40074, Reference length=38963)
-  1-gram: 39.4
-  2-gram: 19.6
-  3-gram:10.6
-  4-gram: 3.9
- Accuracy is: 0.1393246477

With more steps:
- global step 7400 learning rate 0.5000 step-time 0.35 perplexity 1.11
-  eval: bucket 0 perplexity 1.78
-  eval: bucket 1 perplexity 2.65
-  eval: bucket 2 perplexity 6.00
-  eval: bucket 3 perplexity 34.64
- BLEU = 14.18 (Bravity Penalty=1.000, Length ratio=1.065, Translated length=41500, Reference length=38963)
-  1-gram: 39.9
-  2-gram: 20.3
-  3-gram:11.2
-  4-gram: 4.5
- Accuracy is: 0.149162456793

  
##### layers=3, size=256
- global step 9000 learning rate 0.4901 step-time 0.21 perplexity 1.23
-  eval: bucket 0 perplexity 3.04
-  eval: bucket 1 perplexity 3.20
-  eval: bucket 2 perplexity 7.34
-  eval: bucket 3 perplexity 18.86
- BLEU = 12.20 (Bravity Penalty=1.000, Length ratio=1.044, Translated length=40659, Reference length=38963)
-  1-gram: 36.8
-  2-gram: 17.7
-  3-gram:9.5
-  4-gram: 3.6
- Accuracy is: 0.137995214039


##### layers=3, size=1000
- global step 6400 learning rate 0.4950 step-time 0.45 perplexity 1.18
-  eval: bucket 0 perplexity 1.52
-  eval: bucket 1 perplexity 3.62
-  eval: bucket 2 perplexity 6.13
-  eval: bucket 3 perplexity 26.06
- BLEU = 13.99 (Bravity Penalty=1.000, Length ratio=1.065, Translated length=41487, Reference length=38963)
-  1-gram: 39.4
-  2-gram: 20.2
-  3-gram:11.1
-  4-gram: 4.3
  
  
##### layers=4, size=1000




#### Batch size
##### Different train batch size:  vocab=3000, 2 layers, size=256, train batch_size = 1, lstm=attention
- global step 11200 learning rate 0.4568 step-time 0.19 perplexity 6.50
-  eval: bucket 0 perplexity 1.59
-  eval: bucket 1 perplexity 5.09
-  eval: bucket 2 perplexity 2.32
-  eval: bucket 3 perplexity 21.60
- BLEU = 7.54 (Bravity Penalty=0.931, Length ratio=0.933, Translated length=36362, Reference length=38963)
-  1-gram: 33.4
-  2-gram: 13.6
-  3-gram:6.4
-  4-gram: 1.5
  
##### Different test batch size
Doesn't work, translated sentences are looked up one by one. Can't look up multiple sentences at once. 
 
 
#### Different vocab size
##### Vocab size = 40.000
- global step 8400 learning rate 0.4950 step-time 0.19 perplexity 1.26
-  eval: bucket 0 perplexity 5.05
-  eval: bucket 1 perplexity 16.93
-  eval: bucket 2 perplexity 17.70
-  eval: bucket 3 perplexity 38.03
- BLEU = 12.65 (Bravity Penalty=1.000, Length ratio=1.035, Translated length=40310, Reference length=38963)
-  1-gram: 36.9
-  2-gram: 18.1
-  3-gram:9.9
-  4-gram: 3.9
- Accuracy is: 0.142249401755


##### Vocab size = 40.000, size=1000
- global step 7400 learning rate 0.4950 step-time 0.53 perplexity 1.11
-  eval: bucket 0 perplexity 3.67
-  eval: bucket 1 perplexity 8.05
-  eval: bucket 2 perplexity 24.71
-  eval: bucket 3 perplexity 29.66
- BLEU = 15.30 (Bravity Penalty=1.000, Length ratio=1.033, Translated length=40249, Reference length=38963)
-  1-gram: 41.5
-  2-gram: 21.6
-  3-gram:12.2
-  4-gram: 5.0
- Accuracy is: 0.149428343526 


##### Vocab size = 40.000, size=1000, layers=3
after 9800 steps BLEU ~13.30. Accuracy 14.xx



#### More data: 17000 train 1805 test
##### Default
- global step 5600 learning rate 0.4950 step-time 0.23 perplexity 1.58
-  eval: bucket 0 perplexity 1.55
-  eval: bucket 1 perplexity 3.02
-  eval: bucket 2 perplexity 6.59
-  eval: bucket 3 perplexity 13.44
- BLEU = 12.56 (Bravity Penalty=1.000, Length ratio=1.149, Translated length=20306, Reference length=17680)
-  1-gram: 38.6
-  2-gram: 18.1
-  3-gram:9.3
-  4-gram: 3.8
- Accuracy is: 0.17783933518


##### vocab: 4000, size=512
- global step 4800 learning rate 0.4950 step-time 0.22 perplexity 1.39
-  eval: bucket 0 perplexity 1.92
-  eval: bucket 1 perplexity 4.41
-  eval: bucket 2 perplexity 8.97
-  eval: bucket 3 perplexity 18.79
- BLEU = 12.32 (Bravity Penalty=1.000, Length ratio=1.167, Translated length=20635, Reference length=17680)
-  1-gram: 38.8
-  2-gram: 17.7
-  3-gram:9.0
-  4-gram: 3.7
- Accuracy is: 0.192243767313

##### vocab: 4000, size=512 More steps
- global step 13000 learning rate 0.4901 step-time 0.26 perplexity 1.05
-  eval: bucket 0 perplexity 2.01
-  eval: bucket 1 perplexity 6.82
-  eval: bucket 2 perplexity 13.18
-  eval: bucket 3 perplexity 88.26
- BLEU = 12.31 (Bravity Penalty=1.000, Length ratio=1.169, Translated length=20669, Reference length=17680)
-  1-gram: 37.9
-  2-gram: 17.3
-  3-gram:8.9
-  4-gram: 3.9
- Accuracy is: 0.198337950139


#### Use spaced file for BLEU calc, 2x512, vocab=4000, testfile = 1805 lines
##### 2x512, vocab 4000, 
- global step 6400 learning rate 0.4950 step-time 0.22 perplexity 1.24
-  eval: bucket 0 perplexity 1.59
-  eval: bucket 1 perplexity 5.98
-  eval: bucket 2 perplexity 8.13
-  eval: bucket 3 perplexity 22.40
- BLEU = 26.93 (Bravity Penalty=0.862, Length ratio=0.871, Translated length=20435, Reference length=23462)
-  1-gram: 68.2
-  2-gram: 38.0
-  3-gram:24.2
-  4-gram: 15.2
- Accuracy is: 0.186149584488

##### Same with more steps
- global step 9200 learning rate 0.4950 step-time 0.23 perplexity 1.13
-  eval: bucket 0 perplexity 2.18
-  eval: bucket 1 perplexity 4.04
-  eval: bucket 2 perplexity 18.51
-  eval: bucket 3 perplexity 45.24
- BLEU = 26.89 (Bravity Penalty=0.871, Length ratio=0.879, Translated length=20625, Reference length=23462)
-  1-gram: 67.6
-  2-gram: 37.5
-  3-gram:23.9
-  4-gram: 15.0
- Accuracy is: 0.183379501385


#### Use spaced file for BLEU calc, 2x512, vocab=5000, testfile = 1805 lines
- global step 5000 learning rate 0.5000 step-time 0.22 perplexity 1.31
-  eval: bucket 0 perplexity 1.83
-  eval: bucket 1 perplexity 3.46
-  eval: bucket 2 perplexity 9.56
-  eval: bucket 3 perplexity 35.55
- BLEU = 27.45 (Bravity Penalty=0.883, Length ratio=0.889, Translated length=20868, Reference length=23462)
-  1-gram: 66.6
-  2-gram: 37.7
-  3-gram:24.4
-  4-gram: 15.2
- Accuracy is: 0.198337950139


#### Spaced file for BLEU, 2x512, vocab=5000, testfile=1805, enters fixed in python code
- global step 6000 learning rate 0.5000 step-time 0.22 perplexity 1.24
-  eval: bucket 0 perplexity 1.86
-  eval: bucket 1 perplexity 4.10
-  eval: bucket 2 perplexity 11.12
-  eval: bucket 3 perplexity 19.37
- BLEU = 27.50 (Bravity Penalty=0.896, Length ratio=0.901, Translated length=21134, Reference length=23459)
-  1-gram: 67.2
-  2-gram: 37.5
-  3-gram:23.9
-  4-gram: 14.7
- Accuracy is: 0.195013850416



#### Spaced file for BLEU, 2x512, vocab=5000, testfile=1805, enters fixed in python code, random train/test set
- global step 6200 learning rate 0.5000 step-time 0.23 perplexity 1.25
-  eval: bucket 0 perplexity 1.49
-  eval: bucket 1 perplexity 2.22
-  eval: bucket 2 perplexity 2.53
-  eval: bucket 3 perplexity 5.61
- BLEU = 39.16 (Bravity Penalty=0.862, Length ratio=0.871, Translated length=20978, Reference length=24092)
-  1-gram: 74.7
-  2-gram: 51.7
-  3-gram:38.6
-  4-gram: 28.5
- Accuracy is: 0.248199445983

##### even more steps
- global step 8000 learning rate 0.5000 step-time 0.23 perplexity 1.15
-  eval: bucket 0 perplexity 1.49
-  eval: bucket 1 perplexity 1.84
-  eval: bucket 2 perplexity 3.29
-  eval: bucket 3 perplexity 7.08
- BLEU = 40.66 (Bravity Penalty=0.885, Length ratio=0.892, Translated length=21479, Reference length=24092)
-  1-gram: 74.5
-  2-gram: 52.1
-  3-gram:39.3
-  4-gram: 29.2
- Accuracy is: 0.256509695291

##### even more steps
- global step 9000 learning rate 0.5000 step-time 0.22 perplexity 1.10
-  eval: bucket 0 perplexity 1.57
-  eval: bucket 1 perplexity 2.37
-  eval: bucket 2 perplexity 2.84
-  eval: bucket 3 perplexity 7.02
- BLEU = 41.64 (Bravity Penalty=0.899, Length ratio=0.903, Translated length=21766, Reference length=24092)
-  1-gram: 74.4
-  2-gram: 52.3
-  3-gram:39.6
-  4-gram: 30.0
- Accuracy is: 0.268144044321


#### Spaced file for BLEU, 2x512, vocab=6000, testfile=1805, enters fixed in python code, random train/test set
- global step 7400 learning rate 0.4901 step-time 0.22 perplexity 1.16
-  eval: bucket 0 perplexity 1.78
-  eval: bucket 1 perplexity 1.97
-  eval: bucket 2 perplexity 4.59
-  eval: bucket 3 perplexity 5.34
- BLEU = 38.81 (Bravity Penalty=0.883, Length ratio=0.889, Translated length=21419, Reference length=24092)
-  1-gram: 73.0
-  2-gram: 50.1
-  3-gram:37.3
-  4-gram: 27.4
- Accuracy is: 0.263711911357


#### Spaced file for BLEU, 2x512, vocab=5500, testfile=1805, enters fixed in python code, random train/test set
- global step 7800 learning rate 0.4901 step-time 0.29 perplexity 1.16
-  eval: bucket 0 perplexity 1.45
-  eval: bucket 1 perplexity 2.18
-  eval: bucket 2 perplexity 2.93
-  eval: bucket 3 perplexity 8.34
- BLEU = 41.40 (Bravity Penalty=0.902, Length ratio=0.906, Translated length=21830, Reference length=24092)
-  1-gram: 74.1
-  2-gram: 51.8
-  3-gram:39.1
-  4-gram: 29.6
- Accuracy is: 0.272576177285


#### Spaced file for BLEU, 2x512, vocab=5000, testfile=1805, enters fixed in python code, random train/test set, seq2seq cell without attention
- global step 8200 learning rate 0.4950 step-time 0.22 perplexity 1.30
-  eval: bucket 0 perplexity 1.44
-  eval: bucket 1 perplexity 1.93
-  eval: bucket 2 perplexity 3.50
-  eval: bucket 3 perplexity 5.99
- BLEU = 39.32 (Bravity Penalty=0.891, Length ratio=0.897, Translated length=21600, Reference length=24092)
-  1-gram: 73.7
-  2-gram: 50.4
-  3-gram:37.3
-  4-gram: 27.4
- Accuracy is: 0.261495844875

##### more steps
- global step 10600 learning rate 0.4950 step-time 0.21 perplexity 1.18
-  eval: bucket 0 perplexity 1.64
-  eval: bucket 1 perplexity 2.05
-  eval: bucket 2 perplexity 3.15
-  eval: bucket 3 perplexity 6.05
- BLEU = 40.15 (Bravity Penalty=0.881, Length ratio=0.888, Translated length=21386, Reference length=24092)
-  1-gram: 74.7
-  2-gram: 51.7
-  3-gram:38.7
-  4-gram: 28.9
- Accuracy is: 0.267590027701

##### even more steps
- global step 12200 learning rate 0.4901 step-time 0.23 perplexity 1.14
-  eval: bucket 0 perplexity 1.66
-  eval: bucket 1 perplexity 2.59
-  eval: bucket 2 perplexity 3.29
-  eval: bucket 3 perplexity 8.40
- BLEU = 40.94 (Bravity Penalty=0.890, Length ratio=0.896, Translated length=21581, Reference length=24092)
-  1-gram: 74.8
-  2-gram: 52.0
-  3-gram:39.2
-  4-gram: 29.4
- Accuracy is: 0.273684210526


#### Spaced file for BLEU, 2x512, vocab=5000, testfile=1805, enters fixed in python code, vocab=5000, beam search=7 (torch implementation)
35 epochs, 296 steps each = 10360 steps
BLEU = 51.80, 79.1/63.1/53.1/44.4 (BP=0.884, ratio=0.890, hyp_len=21452, ref_len=24092)

#### Spaced file for BLEU, 2x512, vocab=5000, testfile=1805, enters fixed in python code, vocab=5000, beam search=7, repl unk with source attention words (torch implementation)
32 epochs, 296 steps each = 9400 steps
BLEU = 52.58, 79.7/63.9/54.0/45.5 (BP=0.884, ratio=0.890, hyp_len=21452, ref_len=24092)
Accuracy is: 0.413850415512


#### spaced, python tokenizer, 2x512, vocab=5000, no beamsearch, structure alternate 
global step 6200 learning rate 0.5000 step-time 0.30 perplexity 1.15
  eval: bucket 0 perplexity 1.53
  eval: bucket 1 perplexity 5.15
  eval: bucket 2 perplexity 9.95
  eval: bucket 3 perplexity 27.91
BLEU = 58.12 (Bravity Penalty=0.885, Length ratio=0.891, Translated length=21476, Reference length=24092)
  1-gram: 85.3
  2-gram: 70.6
  3-gram:60.3
  4-gram: 51.2
Accuracy is: 0.472576177285


  
  ## Possible things to tweak:
  - steps
  - Add buckets
  - size
  - layers
  - batch size
  - tweak bleu method to ignore unnecessary spaces (e.g. " variable " becomes "variable")
  - reverse/ normal sentence
  - different tokenizer
  - vocab size
  - different dataset
  - Meteor measure
  - Train/test ratio
