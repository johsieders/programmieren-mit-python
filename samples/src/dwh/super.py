class A(object):
    def __init__(self, name):
        self.name = name
        print
        'ich bin A ' + self.name


class B(A):
    def __init__(self, n):
        self.n = n
        super(B, self).__init__('bbb')
        print
        'ich bin B '

##class B(A):
##    def __init__(self, n, k):
##        self.n = n
##        self.k = k
##        A.__init__(self, 'bbb')
##        print 'ich bin B ' + str(n) + str(k)
