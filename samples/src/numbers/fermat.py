# Zahlentheorie
# Riesel, p. 94
# js 25.1.2018

def powm(a, d, m):  # returns a power d modulo m
    result = 1
    a = a % m
    while d > 0:
        if d%2:
            result = (result * a) % m
        a = (a * a) % m
        d = d >> 1
    return result


            
            



