# Python time iterators
# js, 8.6.04

from timeit import *


if __name__ == '__main__':
    print
    print
    
    t = Timer('take(50, hamming__(2,3,5))', 'from iterators import hamming__, take')
    result = t.repeat(2, 20)
    print '20*take(50, hamming-new(2,3,5)) : ', result

##    t = Timer('take(50, hamming(2,3,5))', 'from iterators_new import hamming, take')
##    result = t.repeat(2, 20)
##    print '20*take(50, hamming-newnew(2,3,5)) : ', result

    t = Timer('take(50, hamming(2,3,5))', 'from iterators_classic import hamming, take')
    result = t.repeat(2, 20)
    print '20*take(50, hamming-classic(2,3,5)) : ', result


    print    

    t = Timer('take(100, product(isin(), icos()))', 'from iterators import product, isin, icos, take')
    result = t.repeat(2, 20)
    print '20*take(100, product-new(isin(), icos())) : ', result
    
##    t = Timer('take(50, product(isin(), icos()))', 'from iterators_new import product, isin, icos, take')
##    result = t.repeat(2, 20)
##    print '20*take(50, product-newnew(isin(), icos())) : ', result

    t = Timer('take(100, product(isin(), icos()))', 'from iterators_classic import product, isin, icos, take')
    result = t.repeat(2, 20)
    print '20*take(100, product-classic(isin(), icos())) : ', result


    print    

##    t = Timer('take(100, inverse(iexp()))', 'from iterators import inverse, iexp, take')
##    result = t.repeat(2, 20)
##    print '20*take(100, inverse-new(iexp())) : ', result

##    t = Timer('take(100, inverse(iexp()))', 'from iterators_new import inverse, iexp, take')
##    result = t.repeat(2, 20)
##    print '20*take(100, inverse-newnew(iexp())) : ', result    

    t = Timer('take(100, inverse(iexp()))', 'from iterators_classic import inverse, iexp, take')
    result = t.repeat(2, 20)
    print '20*take(100, inverse-classic(iexp())) : ', result