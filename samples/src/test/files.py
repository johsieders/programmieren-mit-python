## testing writing to and reading from files
## js 03/07/05

from timeit import Timer

##def cartesian(xs, ys):
##    zs = []
##    for x in xs:
##        for y in ys:
##            zs.append((x, y))
##    return zs
            
def cartesian(xs, ys):
    return ((x, y) for x in xs for y in ys)

def s(k):
    return k * '01234567890123456789'


def testWrite(f, s, n):
    for i in xrange(n):
        f.write(s)     
    f.close()

        
def testRead(f):
    xs = []
    for x in f:
        xs.append(x)        
    f.close()


if __name__ == "__main__":
    pass
##    f = file('test.txt', 'w')
##    testWrite(f)
##
##    f = file('test.txt', 'r')
##    testRead(f)
##
##    print "files done"
    
##    f = file('test.txt', 'w')
##    f.truncate(0)
##    f.close()
##    
##    w = Timer("testWrite(f)", "from files import testWrite; f = file('test.txt', 'w')")
##    r = Timer("testRead(f)", "from files import testRead; f = file('test.txt', 'r')")
##    
##    print
##    print N
##    print w.timeit(1)
##    print r.timeit(1)

    result = {}
    for n in [1000, 10000, 100000]:
        for t in [s(k) for k in [1, 5, 10]]:
            wTimer = Timer("testWrite(f, t, n)", "from __main__ import t, n, testWrite; f = file('test.txt', 'w')")
            rTimer = Timer("testRead(f)", "from __main__ import testRead; f = file('test.txt', 'r')")
            size = n*len(t)/1e6                          ## size in MB
            result[n, len(t)] = wTimer.timeit(1)/size, rTimer.timeit(1)/size

    print
    keys = result.keys()
    keys.sort()
    for k in keys:
        print (k[0]*k[1]/10e6, k, result[k])

    