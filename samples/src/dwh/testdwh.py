## test unit one
## js 29.8.02

from unittest import makeSuite
from unittest import TestCase
from unittest import TextTestRunner

from dwhdim import *

class TestOne(TestCase):
    pass

class TestTwo(TestCase):
    pass

class TestThree(TestCase):
    pass
    

def suite(): 
    return makeSuite(TestOne)


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
        


