## js 10.3.2004

## Convert to and from Roman numerals
##
## This program is part of "Dive Into Python", a free Python book for
## experienced programmers.  Visit http://diveintopython.org/ for the
## latest version.
## comments by js 29.8.02


## define exceptions
class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass
class NotIntegerError(RomanError): pass
class InvalidRomanNumeralError(RomanError): pass

#Roman numerals must be less than 5000
MAX_ROMAN_NUMERAL = 4999

#Define digit mapping
romanNumeralMap = (('M',  1000),
                   ('CM', 900),
                   ('D',  500),
                   ('CD', 400),
                   ('C',  100),
                   ('XC', 90),
                   ('L',  50),
                   ('XL', 40),
                   ('X',  10),
                   ('IX', 9),
                   ('V',  5),
                   ('IV', 4),
                   ('I',  1))

# Create tables for fast conversion of roman numerals.
# toRomanTable[0] = None
# toRomanTable[1] = 'I'       fromRomanTable['I'] = 1
# toRomanTable[2] = 'II'      fromRomanTable['II'] = 2
# ..
# toRomanTable[10] = 'X'      fromRomanTable['X'] = 10
# ..
# toRomanTable[105] = 'CV'    fromRomanTable['CV'] = 105
# usw.

toRomanTable = [ None ]  # Skip an index since Roman numerals have no zero
fromRomanTable = {}

def toRoman(n):
    """convert integer to Roman numeral"""
    if not 0 < n <= MAX_ROMAN_NUMERAL:
        raise OutOfRangeError("number out of range (must be 1..4999)")
    if int(n) != n:
        raise NotIntegerError("decimals can not be converted")
    return toRomanTable[n]

def fromRoman(s):
    """convert Roman numeral to integer"""
    if not s:
        raise InvalidRomanNumeralError('Input cannot be blank')
    if s not in fromRomanTable:
        raise InvalidRomanNumeralError('Invalid Roman numeral: %s' % s)
    return fromRomanTable[s]

def toRomanDynamic(n):
    """convert integer to Roman numeral using dynamic programming
    Der Aufruf toRomanDynamic(n) funktioniert nur, wenn alle roemischen Zahlen k
    mit k < n schon in toRomanTable stehen.
    """
    assert 0 < n <= MAX_ROMAN_NUMERAL
    assert int(n) == n
    result = ""
    for num, i in romanNumeralMap:
        if n >= i:
            result = num
            n -= i
            break  
    if n > 0:
        result += toRomanTable[n]
        
    return result

def fillLookupTables():
    """compute all the possible roman numerals"""
    #Save the values in two global tables to convert to and from integers.
    for integer in range(1, MAX_ROMAN_NUMERAL + 1):
        romanNumber = toRomanDynamic(integer)
        toRomanTable.append(romanNumber)
        fromRomanTable[romanNumber] = integer
    
fillLookupTables()
