# test iterator utilities
# js, 8.6.04

from unittest import makeSuite, TestCase, TestSuite, TextTestRunner


class TestUtil(TestCase):
    def testgcd(self):
        pass


def suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestUtil))
    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
