# first steps with keras
# Learning to classify movie reviews
# js 20.5.2019
# from Chollet, p.27 ff

# from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras


def movies():

    # get the training dataset (25.000 texts, 25.000 labels) and the test dataset
    imdb = keras.datasets.imdb
    (train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

    # A dictionary mapping words to an integer index
    word_index = imdb.get_word_index()

    # The first indices are reserved
    word_index = {k: (v + 3) for k, v in word_index.items()}
    word_index["<PAD>"] = 0
    word_index["<START>"] = 1
    word_index["<UNK>"] = 2  # unknown
    word_index["<UNUSED>"] = 3

    # padding all texts to the same length
    train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                            value=word_index["<PAD>"],
                                                            padding='post',
                                                            maxlen=256)

    test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                           value=word_index["<PAD>"],
                                                           padding='post',
                                                           maxlen=256)

    # input shape is the vocabulary count used for the movie reviews (10,000 words)
    vocab_size = 10000

    # define the model
    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    model.summary()

    # compile it
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['acc'])

    # separating test data in two parts
    x_val = train_data[:10000]
    partial_x_train = train_data[10000:]

    y_val = train_labels[:10000]
    partial_y_train = train_labels[10000:]

    # train it on second part of training data
    history = model.fit(partial_x_train,
                        partial_y_train,
                        epochs=40,
                        batch_size=512,
                        validation_data=(x_val, y_val),
                        verbose=1)

    results = model.evaluate(test_data, test_labels)

    return imdb, history, results


if __name__ == '__main__':
    imdb = keras.datasets.imdb
    (train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

    # db, his, res = movies()
    #
    # # get a dictionary mapping words to an integer index
    # word_index = db.get_word_index()
    #
    # # The first indices are reserved
    # word_index = {k: (v + 3) for k, v in word_index.items()}
    # word_index["<PAD>"] = 0
    # word_index["<START>"] = 1
    # word_index["<UNK>"] = 2  # unknown
    # word_index["<UNUSED>"] = 3
    #
    # reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
    #
    # def decode_review(text):
    #     return ' '.join([reverse_word_index.get(i, '?') for i in text])
    #
    #
    # # decode_review(train_data[0])
    #
    # print(res)
    #
    # history_dict = his.history
    # history_dict.keys()
    #
    # acc = history_dict['acc']
    # val_acc = history_dict['val_acc']
    # loss = history_dict['loss']
    # val_loss = history_dict['val_loss']
    #
    # epochs = range(1, len(acc) + 1)
    #
    # # "bo" is for "blue dot"
    # plt.plot(epochs, loss, 'bo', label='Training loss')
    # # b is for "solid blue line"
    # plt.plot(epochs, val_loss, 'b', label='Validation loss')
    # plt.title('Training and validation loss')
    # plt.xlabel('Epochs')
    # plt.ylabel('Loss')
    # plt.legend()
    #
    # plt.show()
    #
    # plt.clf()  # clear figure
    #
    # plt.plot(epochs, acc, 'bo', label='Training acc')
    # plt.plot(epochs, val_acc, 'b', label='Validation acc')
    # plt.title('Training and validation accuracy')
    # plt.xlabel('Epochs')
    # plt.ylabel('Accuracy')
    # plt.legend()
    #
    # plt.show()
