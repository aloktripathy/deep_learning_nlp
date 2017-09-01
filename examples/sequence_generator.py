import os
from six import moves
import ssl
import urllib

# scp -i ~/ssh-keys/deep-learning-key-pair-vishal.pem ubuntu@34.253.207.245:/home/ubuntu/models/us-cities/m-19440.index .

import tflearn
from tflearn.data_utils import *

path = "../data/indian-male-names.txt"
maxlen = 20

string_utf8 = open(path, "r").read()
X, Y, char_idx = string_to_semi_redundant_sequences(string_utf8, seq_maxlen=maxlen, redun_step=3)

g = tflearn.input_data(shape=[None, maxlen, len(char_idx)])
g = tflearn.lstm(g, 512, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 512)
g = tflearn.dropout(g, 0.5)
g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
g = tflearn.regression(g, optimizer='rmsprop', loss='categorical_crossentropy', learning_rate=0.001)

m = tflearn.SequenceGenerator(g, dictionary=char_idx,
                              seq_maxlen=maxlen,
                              clip_gradients=5.0,
                              max_checkpoints=0,
                              checkpoint_path='x')

def train(epochs):
    for i in range(epochs):
        seed = random_sequence_from_string(string_utf8, maxlen)
        m.fit(X, Y, validation_set=0.1, batch_size=128,
              n_epoch=1, run_id='us_cities')
        print("-- TESTING...")
        print("-- Test with temperature of 1.2 --")
        print(m.generate(30, temperature=1.2, seq_seed=seed))
        print("-- Test with temperature of 1.0 --")
        print(m.generate(30, temperature=1.0, seq_seed=seed))
        print("-- Test with temperature of 0.5 --")
        print(m.generate(30, temperature=0.5, seq_seed=seed))