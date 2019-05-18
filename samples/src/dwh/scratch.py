## Test von super
## js 4/10/2005

from numarray import *

from dwh import *
from testdim import *

s = DWHSimpleDimension(produkt)
t = DWHTimeDimension((2004, 1, 1), (2004, 1, 4))
d = DWH(lambda: arange(len(s) * len(t)), s, t)
