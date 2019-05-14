## test von deskriptoren

class MyProp(object):
    def __init__(self, get, set):
        self.get = get
        self.set = set

    def __get__(self, x, type = None):
        return self.get(x)

    def __set__(self, x, value):
        self.set(x, value)

    def __del__(self, x):
        pass


def mystaticmethod(f):
    return lambda s, *xs: f(*xs)        ## ignore self


class MyClass(object):
    def __init__(self, a):
        self.a = a

    def get_a(self):
        return self.a

    def set_a(self, a):
        if a < 0:
            raise ValueError
        else:
            self.a = a

    b = property(get_a, set_a)
    c = MyProp(get_a, set_a)

    @staticmethod
    def bar(a, b):
        return a + b

    @classmethod
    def make(cls, x):
        return cls(x)
        