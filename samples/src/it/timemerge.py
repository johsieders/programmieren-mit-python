## Python time iterators
## js, 15.8.04

from timeit import *

if __name__ == '__main__':
    print
    print
    
    t = Timer('take(200, imerge((igeo(2), iari(10))))', 'from iterators_rec import iari, igeo, imerge, take')
    result = t.repeat(3, 100)
    print '100 * take(200, imerge((igeo(2), iari(10)))) : ', result

    t = Timer('take(200, imerge_((igeo(2), iari(10))))', 'from iterators_rec import iari, igeo, imerge_, take')
    result = t.repeat(3, 100)
    print '100 * take(200, imerge_((igeo(2), iari(10)))) : ', result

    t = Timer('take(200, imerge__((igeo(2), iari(10))))', 'from iterators_rec import iari, igeo, imerge__, take')
    result = t.repeat(3, 100)
    print '100 * take(200, imerge__((igeo(2), iari(10)))) : ', result


    print    

    t = Timer('take(100, hamming(2,3,5))', 'from iterators_rec import hamming, take')
    result = t.repeat(2, 10)
    print '10 * take(100, hamming(2,3,5)) : ', result

    t = Timer('take(100, hamming_(2,3,5))', 'from iterators_rec import hamming_, take')
    result = t.repeat(2, 10)
    print '10 * take(100, hamming_(2,3,5)) : ', result

    t = Timer('take(100, hamming__(2,3,5))', 'from iterators_rec import hamming__, take')
    result = t.repeat(2, 10)
    print '10 * take(100, hamming__(2,3,5)) : ', result       