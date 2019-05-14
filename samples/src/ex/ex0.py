## unit one
## js 10.3.2004

#################
#### basics #####
#################

import pandas as pd
import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense
TARGET_VARIABLE = "user_action"
TRAIN_TEST_SPLIT = 0.5
HIDDEN_LAYER_SIZE = 30

ffnn = Sequential()


def fibo(n):
    """ return n th fibonacci number """    
    if   n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for i in range(n-1):
            a, b = b, a+b
        return b


def fibo1(n):
    """ return fibonacci series up to n """
    if n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    else:
        result = fibo1(n-1)
        result.append(result[-2]+result[-1])
        return result


def faculty(n):
    """ return n! """
    result = 1
    for i in range(1, n+1):
        result *= i
    return result


def gcd(a, b):
    """ return gcd of a and b """
    while b != 0:
        a, b = b, a%b
    return a


if __name__ == '__main__':
    print(4, 6, gcd(4, 6))
    print(98, 100, gcd(98, 100))
    print(0, 1, gcd(0, 1))
    print(1, 0, gcd(1, 0))
    print(-1, 0, gcd(-1, 0))
    print(0, -1, gcd(0, -1))


    
