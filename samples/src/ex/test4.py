# test unit four
# js 29.8.02

from unittest import makeSuite, TestCase, TestSuite, TextTestRunner

from ex4 import *

class TestInfix(TestCase):
    def testInfix(self):
        self.failUnlessEqual('x', i2p('x'))
        self.failUnlessEqual('x', i2p('((x))'))           
        self.failUnlessEqual('x~', i2p('~x'))
        self.failUnlessEqual('x~ y*', i2p('~x*y'))        
        self.failUnlessEqual('x~ y* z+', i2p('~x*y +z'))
        self.failUnlessEqual('x~ y a b+**', i2p('~x*y * (a+b)'))               
        self.failUnlessEqual('x~ y a b+**', i2p('~x*y * ((((a)+b)))'))
        
def suite():
    suite = TestSuite()    
    suite.addTest(makeSuite(TestInfix))
    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())



