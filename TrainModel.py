'''
Josh Barrios 1/17/2020

Training an LSTM model for text synthesis using the writings
of Charles Darwin. Testing multiple hyperparameters for science.

Adapted from "LSTM for text generation" on the Keras blog.
'''

from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import random
import sys
import io
import os
import pickle

# read in text, all lowercase to avoid having to learn capitalization space
with io.open('Darwin', encoding='utf-8') as f:
    text = f.read().lower()
print('corpus length:', len(text))

chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

# Vectorize the text. x is the series of sequences of maxlen, y is the next character after those sequences
print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# build the model: 2x LSTM, each with 20% dropout
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars)), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128, input_shape=(maxlen, len(chars)), return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(len(chars), activation='softmax'))

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def on_epoch_end(epoch, _):
    # Function invoked at end of each epoch. Prints generated text.

    print()
    print('----- Generating text after Epoch: %d' % epoch)

    start_index = random.randint(0, len(text) - maxlen - 1)
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print('----- diversity:', diversity)

        generated = ''
        sentence = text[start_index: start_index + maxlen]
        generated += sentence
        print('----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)

        for i in range(400):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

# Define learning rates on which to train models
learning_rates = [0.001, 0.002, 0.005, 0.1]

for lr in learning_rates:
    optimizer = Adam(learning_rate=lr)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    record = model.fit(x, y,
              batch_size=512,
              epochs= 40,
              callbacks=[print_callback])

    try:
        os.mkdir('DarwinModelLR' + str(lr))
    except:
        print('directory already exists')

    # Save the model and the training history of the model
    model.save('DarwinModelLR' + str(lr) + '/model.h5')
    with open('DarwinModelLR' + str(lr) + '/testing_pickle', 'wb') as file_pi:
        pickle.dump(record.history, file_pi)

    # Plot
    fig = plt.figure(figsize=(16, 4))
    ax = fig.add_subplot(121)
    ax.plot(record.history["loss"])
    ax.set_title("validation loss" + 'learning rate = ' + str(lr))
    ax.set_xlabel("epochs")

    plt.show()

# %% Generate some text from a given seed

def print_test_text(seed):
    # Function invoked at end of each epoch. Prints generated text.

    for diversity in [0.5, 1.0]:
        print('----- diversity:', diversity)

        generated = ''
        sentence = seed
        generated += sentence
        print('----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)

        for i in range(400):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()

print_test_text('the male of the species exhibits curious')



