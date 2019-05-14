
## Building a data warehouse
## js 27.3.05


## a dimension descriptor
orte = ['orte',
        'Ort   Kreis   Land',
        'Tu     RO      BY',
        'Bi',
        'Go     UFF',
        'He',
        'Bu     SHA     BW',
        'Ma',
        'Fu     VS',
        'Tr']

## another dimension descriptor
produkte = ['produkte',
        'Produkt    Gruppe  Sparte',
        'Apfel      Obst    Food',
        'Birne',
        'Kohl       Gemuese',
        'Lauch',
        'Hammer     Werkzeug Non-Food',
        'Bohrer']

## yet another dimension descriptor        
tage = ['days',                             ## name of dimension
        'day        month   year',          ## levels of dimension
        '01-04-04   Jan04   2004',          ## fields are unique within
        '01-05-04',                         ## each column
        '03-15-04   Mar04',
        '04-20-04   Apr04',
        '04-21-04',
        '01-03-05   Jan05   2005',
        '06-10-05   Jun05',
        '12-24-05   Dec05',
        '09-11-06   Dec06   2006']


## a minimal dimension descriptor        
dummy = ['dummy',                           ## name of dimension
         'XXX',                             ## just one level
         'xxx']                             ## just one field