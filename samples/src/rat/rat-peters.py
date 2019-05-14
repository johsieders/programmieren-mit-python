# Rational Numbers #
# Supplies function `rat' for creating rational-number objects (RNO).
# RNOs support mixed-mode arithmetic (+-*/, pow, unary -), comparisons
# (==, <=, etc), coercion (to float, int, long), and hashing (so an RNO
# can be used as a dictionary key). In Boolean contexts, an RNO is true
# if & only if it's non-zero. # # In mixed-mode arithmetic, ints and longs are converted to rationals,
# while rationals are converted to floats. Function `rat' can be used
# explicitly to convert a float to an exact rational equivalent. #
# Given an RNO r, r is the rational number r.num/r.den. r.den > 0
# always, and r.num and r.den have no non-unit common factor. Along with
# the convention that 0 is represented as 0/1, this implies each
# mathematical rational has a unique representation as an RNO. .num and
# .den are intended to be read-only attributes, so that the module can
# maintain these properties. #
# RNOs come in two flavors: short rats and long rats. The difference is
# solely whether .num and .den are Python integers or long integers.
# Short rats will in general run substantially faster, but this is of
# limited utility since the size of numerators & denominators tends to
# blow up quickly during a chain of rational operations. In addition,
# except for comparisons, an operation on short rats may raise an
# overflow exception during an intermediate calculation, even if the
# final result would be representable as a short rat. The author
# recommends not using short rats at all unless you know exactly what
# you're doing. #
# Function rat accepts these arguments:
# rat(long a) returns long rat equal to a
# rat(int a) returns short rat equal to a #
# rat(long a,long b) returns long rat equal to a/b
# rat(long a, int b) returns long rat equal to a/b
# rat( int a,long b) returns long rat equal to a/b
# rat( int a, int b) returns short rat equal to a/b #
# rat(float x) returns long rat a/b exactly equal to x;
# if x is bizarre (e.g., NaN or infinity on an IEEE # machine), the result is undefined
# # # SOME INTERNAL DETAILS #
# The algorithms are obvious, or adapted from Knuth Volume 2. The
# slowest part of a rational implementation is gcd calculations, so the
# operations are coded "cleverly" to avoid gcd whenever possible, and--
# when gcd can't be avoided --to minimize the size of the operands passed
# to gcd. #
# Speeding gcd itself is difficult. The speed of gcd depends mostly on
# the speed of division. 5 gcd functions are defined here, gcd1 through
# gcd5, that vary in their zeal to avoid divisions. No single function
# is fastest; instead their speed depends on the size of the operands.
# From fastest to slowest, they are: #
# for short arguments for larger arguments (up for huge arguments
# (Python int) to several thousand bits) (many thousand bits)
# ------------------- --------------------------- --------------------
# gcd1 gcd5 gcd4 # gcd2 gcd2 gcd3
# gcd5 gcd1 gcd5 # gcd3 gcd3 gcd2
# gcd4 gcd4 gcd1 #
# There is some sense to this <wink>: gcd1 does the most divisions,
# but it's also the simplest code. For short arguments, saving the
# cost of a short division is overwhelmed by the overhead of executing
# more interpreted statements. Contrarily, gcd4 does the fewest
# divisions but is the most complex code. Pure binary methods aren't
# included here because they were never faster than the division
# methods (& I expect this is an artifact of using an interpreter;
# also that there's no really efficient way to test the last bit of
# a Python long ("x & 1" appears to create a long of x's length, then
# cut it back, making a conceptual O(1) operation an O(log x) operation;
# maybe "odd(x)" could be a builtin?)). #
# gcd is set to gcd2 below, because that's the best compromise for
# the size of rationals the author usually works with (usually a few
# hundred to a couple thousand bits). Bind gcd to one of the other
# routines if your usage is different.

import math

def rat(*args):
    if len(args) == 2:
        return Rat().init( args[0], args[1] )
    elif len(args) == 1:
        arg = args[0]
    t = type(arg)

    if t in (type(1), type(1L)):
        return apply( _rat, coerce(arg,1) )
    elif t is not type(1.0):
        raise TypeError, 'need integer or float argument'

# convert float to rational; the method here is exact provided
# that math.frexp and math.ldexp are exact (which they should be,
# on binary machines)
# take care of negative and 0

    if arg == 0.0:
        return _rat(0L,1L)
    top = bot = 1L if arg < 0.0: top, arg = -top, -arg

# now arg > 0, and arg * top / bot == original arg;
# maintain that equality as an invariant while scaling # so that 0.5 <= arg < 1

    arg, shift = math.frexp( arg ) if shift < 0: bot = bot << (-shift) elif shift > 0: top = top << shift
    answer = _rat( top, bot )

# now arg in [0.5,1.0), and arg*answer == original arg;
# remains to convert arg and multiply by answer;
# suck up 28 bits at a time: small enough to fit in an int,
# and big enough so that any IEEE double will be done in no
# more than 2 iterations

    top, bot = 0L, 1L

        while arg:
            arg28 = math.ldexp(arg, 28) # arg * 2^28
            ip = math.floor(arg28) # next 28 bits top, bot = top << 28, bot << 28
            top, arg = top + int(ip), arg28 - ip
        return rat(top,bot) * answer
    else:
        raise TypeError, 'need 1 or 2 arguments'

# _rat packs top/bot into a rational; it trusts they have no common # factor, that 0 is passed as (0,1), that bot != 0, and that they're both # ints or long ints; this avoids the expensive gcd in Rat.init def _rat( top, bot ): if bot < 0: top, bot = -top, -bot

answer = Rat()

answer.num, answer.den = top, bot

return answer

# -------------------- GCD routines -------------------- # as simple as they get

def gcd1(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

# since the quotient is 1 some 41% of the time, this one tries
# to save the division in that common case; gcd5 carries the
# idea one more step
def gcd2(a, b):
    a, b = abs(a), abs(b)
    if a < b:
        a, b = b, a
    while b:
        rem = a - b
        if rem < b:
            a, b = b, rem
        else:
            a, b = b, rem % b
        return a

# a mix of division & binary methods. a & b are forced odd. Then # if r = a % b is odd, b-r is even. So one of {r,b-r} is even. # Factors of 2 are shifted out of that until it's odd again, and # we do it again with the new odd pair. gcd4 is an extension of # this idea. def gcd3(a, b):

a, b, ashift, bshift = abs(a), abs(b), 0, 0

if b == 0: return a

if a == 0: return b while a & 1 == 0: a, ashift = a>>1, ashift+1 while b & 1 == 0: b, bshift = b>>1, bshift+1

r = a % b if r & 1: r = b - r

a, b = b, r

while b: b = b >> 1 while b & 1 == 0: b = b >> 1

r = a % b if r & 1: r = b - r

a, b = b, r return a << min( ashift, bshift )

# like gcd3, but takes min(r,b-r) after removing factors of 2. This # guarantees that, after the first iteration, a/b >= 3, so we get # some real benefit out of the division. Alas, the interpreter # overhead is high enough that it doesn't actually pay off until the # arguments are over (about, on one particular machine) 10,000 bits long. def gcd4(a, b):

a, b = abs(a), abs(b)

if a == 0 or b == 0: return max(a,b)

ash = bsh = 0

mask = 1L while (a & mask) == 0: mask, ash = mask<<1, ash+1

mask = 1L while (b & mask) == 0: mask, bsh = mask<<1, bsh+1 a, b = a>>ash, b>>bsh if a < b: a, b = b, a

r = a % b

while r:

r2 = b - r

mask, rsh = 2L, 1 if r & 1: while (r2 & mask) == 0: mask, rsh = mask<<1, rsh+1 r2 = r2 >> rsh

else: while (r & mask) == 0: mask, rsh = mask<<1, rsh+1 r = r >> rsh

a, b = b, min(r,r2)

r = a % b return b << min(ash,bsh)

# carrying gcd2 one more step, to avoid division when the quotient is # 1 (about 41% of the time) or 2 (about 17% of the time) def gcd5(a, b):

a, b = abs(a), abs(b) if a < b: a, b = b, a

while b:

rem = a - b if rem < b:

a, b = b, rem

else:

rem = rem - b if rem < b:

a, b = b, rem

else:

a, b = b, rem % b

return a

gcd = gcd2 # see comments at the start

# return (l, ma, mb) where # l is the least common multiple of a and b # ma * a = l # mb * b = l def lcm(a, b):

g = gcd( a, b )

ma, mb = b/g, a/g

return ma * a, ma, mb

# -------------------- class Rat -------------------- class Rat:

def init(self, num, den):

num, den = coerce( num, den )

if type(num) not in (type(0), type(0L)):

raise TypeError, 'rational must have integer components' if den < 0:

num, den = -num, -den

elif den == 0:

raise ZeroDivisionError, 'rat(x, 0)'

g = gcd(num, den)

self.num = num/g

self.den = den/g

return self

def __repr__(self):

if self.den != 1:

return 'rat' + `self.num, self.den`

return 'rat(' + `self.num` + ')'

def __cmp__(a, b):

# relies on denominators being non-negative

try:

return cmp( a.num*b.den, a.den*b.num )

except OverflowError:

return cmp( long(a.num)*b.den, long(a.den)*b.num )

def __hash__(self):

return hash(self.num) ^ hash(self.den)

def __float__(self):

return float(self.num) / float(self.den)

def __long__(self):

return long(self.num) / long(self.den)

def __int__(self):

return int(self.num / self.den)

def __coerce__(a, b):

t = type(b)

if t is type(a) and b.__class__ is Rat:

return a, b

if t is type(0):

return a, rat(b, 1)

if t is type(0L):

return a, rat(b, 1L)

if t is type(0.0):

return a.__float__(), b

return None

def __nonzero__(self):

return self.num != 0

# Automatic coercion may not take place for + and *, so we check the

# type of b and force coercion if it's not Rat. Note that after

# coercion, there's still no guarantee that the type of b is Rat (or

# the type of a!), since type(coerce(Rat,float)) is float. We worm

# around that by reissuing the operation, letting Python figure out

# how to do it.

def __add__(a, b):

if type(b) is type(a) and b.__class__ is Rat:

g = gcd( a.den, b.den )

if g == 1:

return _rat( a.num*b.den + b.num*a.den, a.den*b.den )

adenoverg = a.den/g

top = a.num*(b.den/g) + b.num*adenoverg

g2 = gcd( top, g )

return _rat( top/g2, adenoverg * (b.den/g2) )

a, b = coerce( a, b )

return a + b

def __mul__(a, b):

if type(b) is type(a) and b.__class__ is Rat:

g1, g2 = gcd(a.num,b.den), gcd(a.den,b.num)

return _rat( (a.num/g1)*(b.num/g2),

(a.den/g2)*(b.den/g1) )

a, b = coerce( a, b )

return a * b

def __sub__(a, b):

return a.__add__( -b )

def __div__(a, b):

if b.num:

return a.__mul__( _rat( b.den, b.num ) )

raise ZeroDivisionError, 'rational division by 0'

def __neg__(self):

a = Rat()

a.num, a.den = -self.num, self.den

return a

def __pow__(a, n):

if n.den == 1:

n = n.num if n < 0: a, n = 1/a, -n

return _rat( pow(a.num,n), pow(a.den,n) )

raise ValueError, 'rational raised to non-integer power'

# -------------------- tests -------------------- RatTestError = 'RatTestError'

def test():

for args, rep in ( ((0,),'0'), ((0L,),'0L'),

((12L,),'12L'), ((12,),'12'), ((-12L,),'-12L'), ((-12,),'-12'),

((144L,12L),'12L'),

((6,9),'2, 3'), ((-6,9),'-2, 3'), ((6,-9),'-2, 3'),

((-6,-9),'2, 3') ):

got = `apply(rat, args)`

want = 'rat(' + rep + ')'

if got != want:

raise RatTestError, ('__repr__', got, want)

a = rat(37,8)

got = `int(a), long(a), float(a), rat(-float(a))`

want = '(4, 4L, 4.625, rat(-37L, 8L))'

if got != want:

raise RatTestError, ('coercion', got, want)

a = rat(1, 10)

b = rat(2, 5)

l = [a+b, a-b, a*b, a/b, pow(-b, 1/a)]

want = [rat(1,2), rat(-3,10), rat(1,25), rat(1,4),

rat(1024,pow(5,10)) ]

if l != want:

raise RatTestError, ('arithmetic', l, want)

l.sort()

want = [rat(-3,10), rat(1024,pow(5,10)), rat(1,25), rat(1,4), rat(1,2)]

if l != want:

raise RatTestError, ('sort', l, want)

if not a or not b or (a+b)*(a-b)-(pow(a,2)-b*b):

raise RatTestError, 'boolean context'

d = { rat(2): 'two', rat(-12L,16L): rat(4L,8L) }

if d[ pow( d[rat(16,7)*rat(21,-64)], -1 ) ] != 'two':

raise RatTestError, 'dictionary'

for e in 'rat(1,0)', '5/(rat(4,2)-1/rat(3,6))', 'pow(rat(0),-3)':

try:

exec( 'print ' + e )

raise RatTestError, ('wanted ZeroDivisionError', e)

except ZeroDivisionError:

pass

for args in ( (), (1,1.0), ({},1), ([],), ('ouch',), (1,2,3) ):

try:

e = apply( rat, args )

raise RatTestError, ('wanted TypeError', args)

except TypeError:

pass

a = rat( 1<<30 ) a = (a < 1/a) # should not overflow

a = rat( 1L, 1<<30 )

if 3+a == a+3 == -(-a-3) == 3-(3-a)+3 == 3-(3+(-a))+3 == \

a*2-a+3 == 3*a-2*a-(-3) == \

((a/45L + a)*(45L/a + a)-46)/a*rat(45,46) + 3:

pass

else:

raise RatTestError, 'probably implicit conversion'

x = 3.0

if x+a == a+x == -(-a-x) == x-(x-a)+x == x-(x+(-a))+x == a-x+2*x:

pass

else:

raise RatTestError, 'probably implicit float conversion'

sum = rat(-2L,3)

for i in range(1,30):

sum = sum + pow(-1,i)*rat(i,i+1)

want = rat(-446993812891L, 332727080400L)

if sum != want:

raise RatTestError, ('sum', want, sum)

for i in range(1,30):

sum = sum - pow(-1,i)*rat(i,i+1)

if sum*3 != -2:

raise RatTestError, ('sum not -2/3', sum)

# test() 