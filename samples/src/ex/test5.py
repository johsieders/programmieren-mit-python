## test unit five
## js 29.8.04

from unittest import makeSuite, TestCase, TestSuite, TextTestRunner

from ex5 import *

class TestXtuple(TestCase):
    
    def testXtuple(self):
        x = xtuple(7)
        r = range(7)
        self.failUnlessEqual(r[0], x[0])
        self.failUnlessEqual(r[6], x[6])
        self.failUnlessEqual(list(r), list(x))
        self.failUnlessEqual(r[2:4], list(x[2:4]))
        self.failUnlessEqual(r[2:], list(x[2:]))
        self.failUnlessEqual(r[:3], list(x[:3]))
        self.failUnlessEqual(r[-1::-1], list(x[-1::-1])) 
                
        x = xtuple(r)
        self.failUnlessEqual(r[0], x[0])
        self.failUnlessEqual(r[6], x[6])
        self.failUnlessEqual(list(r), list(x))
        self.failUnlessEqual(r[2:4], list(x[2:4]))
        self.failUnlessEqual(r[2:], list(x[2:]))
        self.failUnlessEqual(r[:3], list(x[:3]))
        self.failUnlessEqual(r[-1::-1], list(x[-1::-1])) 

    def testAdd(self):
        x = xtuple(7) + range(7, 15)
        self.failUnlessEqual(range(15), list(x)) 
        x = range(7) + xtuple(range(7, 15))
        self.failUnlessEqual(range(15), list(x))
        x = xtuple(7) + xtuple(range(7, 15))
        self.failUnlessEqual(range(15), list(x))

    def testMul(self):
        x = xtuple(7) * 3
        self.failUnlessEqual(3*range(7), list(x))
        x = 3 * xtuple(7)
        self.failUnlessEqual(3*range(7), list(x))

    def testMap(self):
        x = xtuple(7)
        y = x.map(lambda n : 2*n)
        self.failUnlessEqual([2*n for n in range(7)], list(y))
        
        
class TestLazyTuple(TestCase):
    def testLazyTuple(self):
        x = LazyTuple(70)
        r = range(70)
        self.failUnlessEqual(r[0], x[0])
        self.failUnlessEqual(r[6], x[6])
        self.failUnlessEqual(list(r), list(x))
        self.failUnlessEqual(r[2:4], list(x[2:4]))
        self.failUnlessEqual(r[2:], list(x[2:]))
        self.failUnlessEqual(r[:3], list(x[:3]))
        self.failUnlessEqual(r[-1::-1], list(x[-1::-1])) 



    def testAdd(self):
        x = LazyTuple(7) + range(7, 15)
        self.failUnlessEqual(range(15), list(x)) 

    def testMul(self):
        x = LazyTuple(7) * 3
        self.failUnlessEqual(3*range(7), list(x))
        x = 3 * LazyTuple(7)
        self.failUnlessEqual(3*range(7), list(x))

    def testMap(self):
        x = LazyTuple(7)
        y = x.map(lambda n : 2*n)
        self.failUnlessEqual([2*n for n in range(7)], list(y))
        

class TestLazyDictionary(TestCase):
    def testLazyDictionary(self):
        d = LazyDictionary(range(7))
        self.failUnlessEqual(0, d[0])
        self.failUnlessEqual(None, d.get(7))
        self.failUnlessEqual(range(7), list(d.keys()))
        self.failUnlessEqual(range(7), list(d.values()))
        e = d.copy()
        self.failUnlessEqual(range(7), list(e.keys()))
        self.failUnlessEqual(range(7), list(e.values()))

class TestYdict(TestCase):
    def testYdict(self):
        d = {0: 0}
        t = ydict(d)
        self.failUnlessEqual(0, t[0])
        self.failUnlessEqual(None, t.get(1))
        self.failUnlessEqual(3, t.get(1, 3))

        t[0] = 5    ## t aendern
        t[1] = 6
        self.failUnlessEqual(5, t[0])
        self.failUnlessEqual(6, t.get(1))
        self.failUnlessEqual(7, t.get(2, 7))

        t.rollback()    ## t zuruecksetzen
        self.failUnlessEqual(0, t[0])
        self.failUnlessEqual(None, t.get(1))
        self.failUnlessEqual(3, t.get(1, 3))

        t[0] = 5    ## t nochmal aendern
        t[1] = 6
        self.failUnlessEqual(5, t[0])
        self.failUnlessEqual(6, t.get(1))
        self.failUnlessEqual(7, t.get(2, 7))
        
        t.commit()  ## t bestaetigen
        self.failUnlessEqual(5, t[0])
        self.failUnlessEqual(6, t.get(1))
        self.failUnlessEqual(7, t.get(2, 7))

        t.rollback()  ## hat keine Wirkung      
        self.failUnlessEqual(5, t[0])
        self.failUnlessEqual(6, t.get(1))
        self.failUnlessEqual(7, t.get(2, 7))


def suite():
    suite = TestSuite()    
    suite.addTest(makeSuite(TestXtuple))
    suite.addTest(makeSuite(TestLazyTuple))
    suite.addTest(makeSuite(TestLazyDictionary))
    suite.addTest(makeSuite(TestYdict))
    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
