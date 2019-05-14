## time three versions of reverse

from timeit import *

t0 = Timer('xs.reverse()',  'xs = 1000*[1]')
t1 = Timer('reverse1(xs)', 'from ex1 import reverse1; xs = 1000*[1]')
t2 = Timer('reverse2(xs)', 'from ex1 import reverse2; xs = 1000*[1]')

print ('v0: ', t0.repeat(2, 10000))
print ('v1: ', t1.repeat(2, 10000))
print ('v2: ', t2.repeat(2, 10000))


t0 = Timer('xs.reverse()',  'xs = range(1000)*3')
t1 = Timer('reverse1(xs)', 'from ex1 import reverse1; xs = range(1000)*3')
t2 = Timer('reverse2(xs)', 'from ex1 import reverse2; xs = range(1000)*3')


print ('v0: ', t0.repeat(2, 10000))
print ('v1: ', t1.repeat(2, 10000))
print ('v2: ', t2.repeat(2, 10000))
