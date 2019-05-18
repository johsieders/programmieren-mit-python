from unittest import makeSuite, TestCase, TestSuite, TextTestRunner

from scanning.scan import scanner


class TestScan(TestCase):
    def testScan(self):
        s = scanner('abc')
        b = s('qqqq')
        print(b)
        b = s('abc')
        print(b)
        b = s('xxabcyy')
        print(b)
        b = s('abcxxx')
        print(b)
        b = s('yyyabc')
        print(b)


def suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestScan))
    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
