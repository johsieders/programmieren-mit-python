## numarrays schreiben und lesen

def testWrite(f, n, s):      	## f: Datei, n = Anzahl, s = zu schreibender Text
    for i in xrange(n):
        f.write(s)     
    f.close()


def testRead(f):		## f: Datei
    xs = []
    for x in f:
        xs.append(x)        
    f.close()
    return xs


def testArrays(n):
    fname = 'zzz'
    a = array(n*[27], Int8)
    a.tofile(fname)
    b = fromfile(fname, Int8)
    print len(b)
    

if __name__ == '__main__':
    f = file('test.txt', 'w')
    testWrite(f, 10, "otto\n")
    f.close()

    f = file('test.txt', 'r')
    xs = testRead(f)
    f.close()
    print len(xs)

    ## testArrays(100000000)  laeuft gerade noch

    
