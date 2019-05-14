# infix2postfix as COM Server
# js 2.9.2004

from ex.ex4 import infix2postfix, split, operators

class Infix2postfixServer:
    _public_methods_ = ['infix2postfix']
    _reg_progid_     = 'PythonDemos.Infix2postfix'
    _reg_clsid_      = '{B8137A12-E43A-11D5-AE1E-000374890932}'

    def infix2postfix(self, formula):
        return infix2postfix(str(formula), operators)

class PythonUtilities:
    _public_methods_ = [ 'Split' ]
    _reg_progid_     = 'PythonDemos.Utilities'
    _reg_clsid_      = '{D7E21D10-E442-11D5-AE1E-000374890932}'

    def Split(self, val, item = None):
        import string
        if item != None:
            item = str(item)
        return string.split(str(val), item)
    

if __name__ == '__main__':
    print "Registering COM Server ..."
    import win32com.server.register
    win32com.server.register.UseCommandLine(Infix2postfixServer)
    win32com.server.register.UseCommandLine(PythonUtilities)
    

if __name__ == '__main__':
    print infix2postfix('( a + b ) - c * d', operators)
