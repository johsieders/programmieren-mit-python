## time four versions of histogram

from timeit import *

t0 = Timer('histogram(xs)',  'from ex1 import histogram;  xs = 100*[1]')
t1 = Timer('histogram1(xs)', 'from ex1 import histogram1; xs = 100*[1]')
t2 = Timer('histogram2(xs)', 'from ex1 import histogram2; xs = 100*[1]')
t3 = Timer('histogram3(xs)', 'from ex1 import histogram3; xs = 100*[1]')

print
print
print 'v0: ', t0.repeat(2, 1000)
print 'v1: ', t1.repeat(2, 1000)
print 'v2: ', t2.repeat(2, 1000)
print 'v3: ', t3.repeat(2, 1000)

t0 = Timer('histogram(xs)',  'from ex1 import histogram;  xs = range(100)*3')
t1 = Timer('histogram1(xs)', 'from ex1 import histogram1; xs = range(100)*3')
t2 = Timer('histogram2(xs)', 'from ex1 import histogram2; xs = range(100)*3')
t3 = Timer('histogram3(xs)', 'from ex1 import histogram3; xs = range(100)*3')

print
print 'v0: ', t0.repeat(2, 1000)
print 'v1: ', t1.repeat(2, 1000)
print 'v2: ', t2.repeat(2, 1000)
print 'v3: ', t3.repeat(2, 1000)