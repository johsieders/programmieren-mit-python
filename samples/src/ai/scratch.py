# first steps with keras
# Learning to classify movie reviews
# js 20.5.2019
# from Chollet, p.27 ff

# from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

if __name__ == '__main__':

    imdb = keras.datasets.imdb
    (train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)