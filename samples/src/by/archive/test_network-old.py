import unittest

import by.impl.abstract_x as mb

bst_simple = ((), (0,))

epsilon = 1e-8
bst1 = ((), (0,))  # backward star of a digraph with two nodes and one edge
fpt1 = ((0.7,), (0.2, 0.4))  # forward probability table. fpt[i] = table of node i; contains 2^k entries

bst2 = ((), (0,), (0, 1), (1, 2), (1, 2, 3), (3, 4))
fpt2 = ([0.7], [0.2, 0.4], [0.1, 0.3, 0.5, 0.8], [0.3, 0.4, 0.9, 0.1],
        [0.3, 0.4, 0.9, 0.1, 0.3, 0.4, 0.9, 0.1], [0.3, 0.4, 0.9, 0.1])

bst_fork = ((), (0,), (0,))
fpt_fork = []
bst_collider = ((), (), (0, 1))
bst_chain = ((), (0,), (1,))
fpt_chain = ([0.7], [0.8, 0.1], [0.6, 0.4])

a_implies_b = [[1], [1, 0]]
a_implies_xb = [[1], [0, 1]]

triv = [[0.5], [0.5, 0.5]]
morse = [[0.7], [0.99, 0.02]]

alarm1 = [[0.999], [0.9999, 0.0001]]
alarm2 = [[0.999], [0.999], 0.001]
alarm3 = [[0.999], [0.995, 0.005]]

cabs = [0.85], [[0.8], [0.2]]
cabsrev = [[0.71], [0.9577, 0.5862]]

cancer = [[0.9986], [0.88, 0.27]]
smoker = [[0.95], [0.8, 0.01]]


class TestNetwork(unittest.TestCase):

    def test_simple(self):
        for tc in [triv, morse, alarm1, alarm2, alarm3, cabs, cabsrev, cancer, smoker]:
            pass

    def test_joint_probability(self):
        for i in range(2):
            for j in range(2):
                print(i, j, mb.joint_probability(i, j))

    def test_joint_evidence(self):
        for i in range(2):
            for j in range(2):
                print(i, j, mb.evidence(i, j))

        print(0, 'X', mb.evidence(0, None))
        print(1, 'X', mb.evidence(1, None))
        print('X', 0, mb.evidence(None, 0))
        print('X', 0, mb.evidence(None, 1))
        print('X', 'X', mb.evidence(None, None))

    def test_forward_star(self):
        print(list(mb.forward_star(bst1)))
        print(list(mb.forward_star(bst2)))

    def test_conditional_probability(self):
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    print(i, j, k, mb.conditional_probability(i, (j, k)))

    def test_binary_cube(self):
        pattern = [0, None, 1, None]
        c1 = mb.binary_cube(*pattern)
        print(list(c1))

    def test_chain(self):
        pass
