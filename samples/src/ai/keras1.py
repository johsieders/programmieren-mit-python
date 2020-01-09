# first steps with keras
# Learning fashion_mnist
# js 20.5.2019
# from Chollet, p.27 ff

# from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
from tensorflow import keras

# Helper libraries
# import numpy as np
# import matplotlib.pyplot as plt

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


def fashion():
    # get train_images, train labels; test_images, test_labels
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    # define a neuronal network with two layers
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),  # formatting only
        keras.layers.Dense(512, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    # compile it
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    # train it
    model.fit(train_images, train_labels, epochs=6)

    # evaluate it
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    predictions = model.predict(test_images)

    return test_acc, test_loss


if __name__ == '__main__':
    acc, loss = fashion()
    print('Test accuracy:', acc)
    print('Test loss:', loss)
