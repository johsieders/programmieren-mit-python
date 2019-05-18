## unit one
## js 10.3.2004

#################
#### basics #####
#################

def fibo(n):
    """ return n th fibonacci number """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for i in range(n - 1):
            a, b = b, a + b
        return b


def fibo1(n):
    """ return fibonacci series up to n """
    if n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    else:
        result = fibo1(n - 1)
        result.append(result[-2] + result[-1])
        return result


def faculty(n):
    """ return n! """
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def gcd(a, b):
    """ return gcd of a and b """
    while b != 0:
        a, b = b, a % b
    return a


##################
#### reverse #####
##################

## compare this with reverse!!

def reverse1(xs):
    """ return seq in reversed order """
    return xs[::-1]


def reverse2(xs):
    """ reverse order of seq; return None """
    for i in range(len(xs) // 2):
        xs[i], xs[-i - 1] = xs[-i - 1], xs[i]
    return None


####################
#### histogram #####
####################

def histogram(xs):
    result = {}
    for x in xs:
        if x in result.keys():
            result[x] += 1
        else:
            result[x] = 1
    return result


def histogram1(xs):
    result = {}
    for x in xs:
        if x not in result.keys():
            result[x] = xs.count(x)
    return result


def histogram2(xs):
    return dict([(x, xs.count(x)) for x in xs])


def histogram3(xs):
    return dict([(x, xs.count(x)) for x in set(xs)])


######################
#### split money #####
######################

EUROS = (20000, 10000, 5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1)


def split(value):
    result = [0] * len(EUROS)
    for i, euro in enumerate(EUROS):
        result[i], value = divmod(value, euro)
        if value <= 0:
            return result


#####################
#### palindrome #####
#####################

def normstring(s):
    import string
    result = ''
    for c in s:
        if c in string.ascii_letters:
            result += str.lower(c)
    return result


def isPalindrome(s, norm=True):
    if norm:
        s = normstring(s)
    if len(s) < 2:
        return True
    else:
        return s[0] == s[-1] and isPalindrome(s[1:-1], False)


#########################
#### merge and sort #####
#########################

def merge(xs, ys):
    if not xs:
        return ys
    if not ys:
        return xs
    elif xs[0] <= ys[0]:
        return xs[:1] + merge(xs[1:], ys)
    else:
        return ys[:1] + merge(xs, ys[1:])


def msort(xs):
    if len(xs) <= 1:
        return xs[:]
    else:
        m = len(xs) // 2
        return merge(msort(xs[:m]), msort(xs[m:]))


def qsort(xs):
    if len(xs) <= 1:
        return xs[:]
    else:
        return qsort(list(filter(lambda x: x < xs[0], xs))) + \
               list(filter(lambda x: x == xs[0], xs)) + \
               qsort(list(filter(lambda x: x > xs[0], xs)))


#################
#### grades #####
#################

def zeugnisnote(proben, kurzproben, stegreifaufgaben):
    return (3 * sum(proben) + 2 * sum(kurzproben) + sum(stegreifaufgaben)) / \
           (3 * len(proben) + 2 * len(kurzproben) + len(stegreifaufgaben))
