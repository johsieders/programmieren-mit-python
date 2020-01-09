# This program implements bayesian networks given by
# backward star (bst): a tuple of tuples containing each node's predecessors
# forward probability table (fpt): a list of conditional probability tables, one for each node


import functools as ft

from search.conjoin import simple_conjoin

epsilon = 1e-8
bst1 = ((), (0,))  # backward star of a digraph with two nodes and one edge
fpt1 = [[0.7], [0.2, 0.4]]  # forward probability table. fpt[i] = table of node i; contains 2^k entries

bst2 = ((), (0,), (0, 1), (1, 2), (1, 2, 3), (3, 4))
fpt2 = [[0.7], [0.2, 0.4], [0.1, 0.3, 0.5, 0.8], [0.3, 0.4, 0.9, 0.1],
        [0.3, 0.4, 0.9, 0.1, 0.3, 0.4, 0.9, 0.1], [0.3, 0.4, 0.9, 0.1]]

bst_fork = ((), (0,), (0,))
fpt_fork = []
bst_collider = ((), (), (0, 1))
bst_chain = ((), (0,), (1,))


def forward_star(bst):
    result = []
    for i in range(len(bst)):
        result.append([])

    def process(p):
        k = len(p) - 1
        if k < 0:
            return
        else:
            for i in p[k]:
                result[i].append(k)  # k is successor of i
            process(p[:-1])

    process(bst)
    return (tuple(s) for s in result)


def joint_probability(*values):
    """
    :param values: binary values of X0, X1, ..., Xk; k < n = number of nodes
    :return: p(X0=x0, ..., Xk=xk)
    """

    n = len(values)
    p = 1
    for k in range(n):
        vs = (values[i] for i in bst1[k])  # values of predecessors of k
        i = ft.reduce(lambda r, d: d + (r << 1), vs, 0)  # index of matching predecessor probabilities
        p *= fpt1[k][i] if values[k] == 0 else 1 - fpt1[k][i]
        if p < epsilon:
            return 0
    return p


def evidence(*pattern):
    """
    :param pattern: fixed variables are 0 or 1; free variables are None
    :return: probability of given pattern of fixed variables
    """
    return sum(joint_probability(*values) for values in binary_cube(*pattern))


def conditional_probability(k, pattern):
    """
    :param k: index of variable
    :param pattern:
    :return: p(Xk= xk | pattern)
    """
    nominator = evidence(*pattern)
    q = list(pattern)
    q[k] = 1 - q[k]
    denominator = nominator + evidence(*q)
    return nominator / denominator


def binary_cube(pattern):
    """
    :param: pattern
    :return: projection of binary cube of dimension = n
    """

    gs = [None] * len(pattern)
    for i, p in enumerate(pattern):
        if p is 0:
            gs[i] = lambda: (0,)
        elif p is 1:
            gs[i] = lambda: (1,)
        else:
            gs[i] = lambda: (0, 1)

    return simple_conjoin(gs)


def backward_probability_table(bst, fpt):
    result = []
    return result


class BayesianNetwork(object):
    def __init__(self, bst, fpt, name='BayesianNetwork'):
        self.__bst = bst
        self.__fst = forward_star(bst)
        self.__fpt = fpt
        self.__bpt = None
        self.__name = name

    def name(self):
        return self.__name

    def __len__(self):
        return len(self.__bst)

    def forward_star(self):
        return self.__fst

    def backward_star(self):
        return self.__bst

    def forward_probability_table(self):
        return self.__fpt

    def backward_probability_table(self):
        if self.__bpt is None:
            self.__bpt = self.__compute_bpt()
        return self.__bst

    def joint_probability(self, values):
        """
        :param values: binary values of X0, X1, ..., Xn; n = number of nodes
        :return: p(X0=x0, ..., Xn=xn)
        """
        n = len(values)
        p = 1
        for k in range(n):
            vs = (values[i] for i in self.__bst[k])  # values of predecessors of k
            i = ft.reduce(lambda r, d: d + (r << 1), vs, 0)  # index of matching predecessor probabilities
            p *= self.__fpt[k][i] if values[k] == 0 else 1 - self.__fpt[k][i]
            if p < epsilon:
                return 0
        return p

    def evidence(self, pattern):
        """
        :param pattern: fixed variables are 0 or 1; free variables are None
        :return: probability of given pattern of fixed variables
        """
        return sum(self.joint_probability(values) for values in binary_cube(pattern))

    def conditional_probability(self, pattern, conditioned):
        """
        :param pattern: fixed and conditioned variables are 0 or 1; free variables are None
        :param conditioned: list of conditioned variables, eg (2, 3)
        :return: p(Xi=xi (i fixed) | Xj = xj (j conditioned)
        """
        pattern_copy = list(pattern)
        numerator = self.evidence(pattern_copy)
        free = [i for i in range(len(pattern)) if i not in conditioned]
        for k in free:
            pattern_copy[k] = None
        denominator = self.evidence(pattern_copy)
        return numerator / denominator

    def __compute_bpt(self):
        n = len(self)
        result = [[] for i in range(n)]  # the future bpt
        for i in range(n):
            pattern = [None] * n  # pattern for cond probability
            pattern[i] = 0
            aux = [None] * len(self.__fst[i])
            for vs in binary_cube(aux):  # enumerate values of successors of i
                k = 0
                for j in self.__fst[i]:  # copy these values to pattern
                    pattern[j] = vs[k]
                    k += 1
                result[i].append(self.conditional_probability(self, pattern, self.__fst[i]))
        return result


if __name__ == '__main__':
    for i in range(2):
        for j in range(2):
            print(i, j, joint_probability(i, j))

    print()

    for i in range(2):
        for j in range(2):
            print(i, j, evidence(i, j))

    print()

    print(0, 'X', evidence(0, None))
    print(1, 'X', evidence(1, None))
    print('X', 0, evidence(None, 0))
    print('X', 0, evidence(None, 1))
    print('X', 'X', evidence(None, None))

    print()

    print(list(forward_star(bst1)))
    print(list(forward_star(bst2)))

    print()

    for i in range(2):
        for j in range(2):
            for k in range(2):
                print(i, j, k, conditional_probability(i, (j, k)))

    print()

    pattern = []
    c1 = binary_cube(*pattern)
    for c in c1:
        print(c)
