## taxes
## js 12-30-2010
    
from collections import OrderedDict

class TaxDict(OrderedDict):
    def __init__(self):
        super().__init__(self)
        self.gradient = None
        self.bottom = 16010         ## erster Wert der Steuertabelle
        self.top    = 630046        ## letzter Wert der Steuertabelle
        self.dist   = 1000          ## Genauigkeit des Gradienten
        
    def getGradient(self):
        if self.gradient is None:
            self.gradient = (super().__getitem__(self.top) -       \
                             super().__getitem__(self.top  -       \
                                                 self.dist)) / self.dist
        return self.gradient
        
    def __getitem__(self, n):
        n = round(n)
        if n < 0:
            raise ValueError
        
        if n < self.bottom:
            return 0
            
        if n > self.top:
            return self[self.top] + round((n - self.top) * self.getGradient())
        
        for k in range(n, n+4):
            if k in self:
                return round(super().__getitem__(k))
            
        raise KeyError        ## never get here
        

def taxDict(taxfile):
    result = TaxDict()
    lines = open(taxfile)
    n = 0
    
    for line in lines:
        s = line.split()
        if len(s) != 1:
            continue
        
        y = s[0].replace('.', '')
        y = y.replace(',', '')
        try:
            z = int(y)
        except ValueError:
            continue
      



	  
        if n == 0:       ## new entry
            ek = z
            n = 1
        elif n == 1:
            tax = z      ## get tax
            ## print('tax', tax)
            n = 2
        elif n == 2:     ## get soli
            soli = z/100
            result[ek] = tax + soli
            n = 0
            
    return result


def futureValue_(auszahlungen, zinssaetze, entnahmen, einkommen, \
                 steuertabelle):
    n = len(auszahlungen)
    assert(n > 0)
    assert(len(zinssaetze) == n)
    assert(len(entnahmen)  == n)
    
    a = auszahlungen
    e = entnahmen
    k = einkommen
    t = steuertabelle
    
    z = n * [None]        ## z[i] = Zinsfaktor in Periode i
    z[0] = 1
    for i in range(1, n):
        z[i] = (1+zinssaetze[i])*z[i-1]
        
    w = n * [None]        ## w[i] = zusaetzliche Steuern bei Einkommen k 
                          ## und Auszahlung a
    for i in range(0, n):
        w[i] = t[a[i] + k[i]] - t[k[i]]
    
    return round(sum([(a[i] - w[i]) * z[n-i-1] for i in range(0, n)]))


def futureValue(gesamt, n, k, zinssatz, einkommen, steuertabelle):
    ## Auszahlung in k Teilen ( 1 <= k <= n)
    ## Laufzeit n Jahre
    auszahlungen = k * [gesamt/k] + (n-k) * [0]
    zinssaetze   = n * [zinssatz]
    entnahmen    = n * [0]
    einkommen    = n * [einkommen]
    return futureValue_(auszahlungen, zinssaetze, entnahmen, einkommen, \
                        steuertabelle)               


						
						
						
						
						
						
						
						
						


taxfile = 'splitt_ohne_kist.txt'
t = taxDict(taxfile)
fv = futureValue

result55 = 5 * [None]
result55[0] = [fv(575721, 5, i, 0.00, 20000, t) for i in range(1, 6)]
result55[1] = [fv(575721, 5, i, 0.01, 20000, t) for i in range(1, 6)]
result55[2] = [fv(575721, 5, i, 0.02, 20000, t) for i in range(1, 6)]
result55[3] = [fv(575721, 5, i, 0.03, 20000, t) for i in range(1, 6)]
result55[4] = [fv(575721, 5, i, 0.04, 20000, t) for i in range(1, 6)]

result510 = 5 * [None]
result510[0] = [fv(575721, 5, i, 0.00, 100000, t) for i in range(1, 6)]
result510[1] = [fv(575721, 5, i, 0.01, 100000, t) for i in range(1, 6)]
result510[2] = [fv(575721, 5, i, 0.02, 100000, t) for i in range(1, 6)]
result510[3] = [fv(575721, 5, i, 0.03, 100000, t) for i in range(1, 6)]
result510[4] = [fv(575721, 5, i, 0.04, 100000, t) for i in range(1, 6)]

result105 = 5 * [None]
result105[0] = [fv(575721, 10, i, 0.00, 50000, t) for i in range(1, 11)]
result105[1] = [fv(575721, 10, i, 0.01, 50000, t) for i in range(1, 11)]
result105[2] = [fv(575721, 10, i, 0.02, 50000, t) for i in range(1, 11)]
result105[3] = [fv(575721, 10, i, 0.03, 50000, t) for i in range(1, 11)]
result105[4] = [fv(575721, 10, i, 0.04, 50000, t) for i in range(1, 11)]

result1010 = 5 * [None]
result1010[0] = [fv(575721, 10, i, 0.00, 100000, t) for i in range(1, 11)]
result1010[1] = [fv(575721, 10, i, 0.01, 100000, t) for i in range(1, 11)]
result1010[2] = [fv(575721, 10, i, 0.02, 100000, t) for i in range(1, 11)]
result1010[3] = [fv(575721, 10, i, 0.03, 100000, t) for i in range(1, 11)]
result1010[4] = [fv(575721, 10, i, 0.04, 100000, t) for i in range(1, 11)]
