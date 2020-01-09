# Bayesian networks with pomegranate

import numpy as np
from pomegranate import *


def montyhall():
    # The doors are named A, B and C
    # The door selected by the guest and the door hiding the prize are random
    # There are three nodes, each having as value one of the doors A, B or C
    # guest = n1: the guest's choice
    # prize = n2: the door hiding the prize
    # monty = n3: the door Monty picks depending on guest and prize
    # There are two edges: [n1, n3] and {n2, n3]

    guest = DiscreteDistribution({'A': 1 / 3, 'B': 1 / 3, 'C': 1 / 3})
    prize = DiscreteDistribution({'A': 1 / 3, 'B': 1 / 3, 'C': 1 / 3})
    monty = ConditionalProbabilityTable(
        [['A', 'A', 'A', 0.0],  # P(monty = A | guest = A, prize = A)
         ['A', 'A', 'B', 0.5],  # P(monty = B | guest = A, prize = A)
         ['A', 'A', 'C', 0.5],  # P(monty = C | guest = A, prize = A)
         ['A', 'B', 'A', 0.0],  # P(monty = A | guest = A, prize = B)
         ['A', 'B', 'B', 0.0],
         ['A', 'B', 'C', 1.0],
         ['A', 'C', 'A', 0.0],
         ['A', 'C', 'B', 1.0],
         ['A', 'C', 'C', 0.0],
         ['B', 'A', 'A', 0.0],
         ['B', 'A', 'B', 0.0],
         ['B', 'A', 'C', 1.0],
         ['B', 'B', 'A', 0.5],
         ['B', 'B', 'B', 0.0],
         ['B', 'B', 'C', 0.5],
         ['B', 'C', 'A', 1.0],
         ['B', 'C', 'B', 0.0],
         ['B', 'C', 'C', 0.0],
         ['C', 'A', 'A', 0.0],
         ['C', 'A', 'B', 1.0],
         ['C', 'A', 'C', 0.0],
         ['C', 'B', 'A', 1.0],
         ['C', 'B', 'B', 0.0],
         ['C', 'B', 'C', 0.0],
         ['C', 'C', 'A', 0.5],
         ['C', 'C', 'B', 0.5],
         ['C', 'C', 'C', 0.0]], [guest, prize])

    n1 = Node(guest, name="guest")
    n2 = Node(prize, name="prize")
    n3 = Node(monty, name="monty")

    network = BayesianNetwork("Monty Hall Problem")
    network.add_nodes(n1, n2, n3)
    network.add_edge(n1, n3)
    network.add_edge(n2, n3)

    network.bake()

    # print(network.dense_transition_matrix())

    print(network.probability([['A', 'A', 'A'],
                               ['A', 'A', 'B'],
                               ['C', 'C', 'B'],
                               ['A', 'B', 'C']]))

    print(network.predict_proba([None, None, None]))
    print(network.predict_proba(['A', None, None]))
    print(network.predict_proba({'guest': 'A', 'monty': 'C'}))


def morse():
    # dots and dashes are being sent and received

    sender = DiscreteDistribution({"dot": 0.7, "dash": 0.3})
    receiver = ConditionalProbabilityTable(
        [["dot", "dot", 0.99],
         ["dot", "dash", 0.01],
         ["dash", "dot", 0.02],
         ["dash", "dash", 0.98]], [sender])

    n1 = Node(sender, name="sender")
    n2 = Node(receiver, name="receiver")

    network = BayesianNetwork("Morse")
    network.add_nodes(n1, n2)
    network.add_edge(n1, n2)

    network.bake()

    # print(network.probability([['dot', 'dot'],                  # P(dot, dot): dot sent, dot received
    #                             ['dot', 'dash'],                # P(dash, dot): dash sent, dot received
    #                             ['dash', 'dot'],                # P(dot, dash): dash sent, dot received
    #                             ['dash', 'dash']]))             # P(dash, dash): dash sent, dash received

    # print(network.predict_proba([None, None]))                  # returns marginal distribution of dot, dash
    # print(network.marginal())                                     # returns marginal distribution of dot, dash
    #
    # print(network.predict_proba(['dot', None]))                 # forward probabilities given sender = dot
    print(network.predict_proba({'sender': 'dot'}))  # forward probabilities given sender = dot
    # print(network.predict_proba([None, 'dot']))                 # backward probabilities given receiver = dot
    # print(network.predict_proba({'receiver': 'dot'}))           # backward probabilities given receiver = dot
    # print(network.predict_proba(['dot', 'dot']))                # returns just ['dot', 'dot']


def samples():
    numpy.random.seed(111)

    X = numpy.random.randint(2, size=(15, 15))
    X[:, 5] = X[:, 4] = X[:, 3]
    X[:, 11] = X[:, 12] = X[:, 13]

    network = BayesianNetwork.from_samples(X)


def fitting():
    samples1 = np.array([['x', 'x'], ['x', 'x'], ['x', 'y'], ['x', 'y'], ['y', 'y']])
    samples2 = np.array([['x', 'x'], ['x', 'y']])

    samples3 = np.array([['x', 'x'], ['x', 'x'], ['x', 'y'], ['x', 'y'],
                         ['y', 'x'], ['y', 'x'], ['y', 'y'], ['y', 'y']])

    a = DiscreteDistribution({'x': 0.5, 'y': 0.5})
    b = ConditionalProbabilityTable(
        [['x', 'x', 0.5],
         ['x', 'y', 0.5],
         ['y', 'x', 0.5],
         ['y', 'y', 0.5]], [a])

    n1 = Node(a, name="a")
    n2 = Node(b, name="b")

    network = BayesianNetwork('Test')
    network.add_nodes(n1, n2)
    network.add_edge(n1, n2)

    network.bake()
    network.summarize(samples1)
    # network.from_summaries()
    print(network.probability([['x', 'x'],
                               ['x', 'y'],
                               ['y', 'x'],
                               ['y', 'y']]))

    network.summarize(samples2)
    network.from_summaries()
    print(network.probability([['x', 'x'],
                               ['x', 'y'],
                               ['y', 'x'],
                               ['y', 'y']]))
    # network.summarize(samples3)
    # print(network.probability([['x', 'x'],
    #                            ['x', 'y'],
    #                            ['y', 'x'],
    #                            ['y', 'y']]))


def fitting1():
    samples1 = np.array([[0, 0], [0, 0], [0, 1], [0, 1], [1, 1]])
    samples2 = np.array([[0, 0], [1, 1]])

    # samples3 = np.array([[0, 0], [0, 0], [0, 1], [0, 1],
    #                      [1, 0], [1, 0], [1, 1], [1, 1]])
    #
    # a = DiscreteDistribution({0: 0.9, 1: 0.1})
    # # b = DiscreteDistribution({0: 0.5, 1: 0.5})
    #
    # b = ConditionalProbabilityTable(
    #     [[0, 0, 0.5],
    #      [0, 1, 0.5],
    #      [1, 0, 0.5],
    #      [1, 1, 0.5]], [a])
    #
    # n1 = Node(a, name="a")
    # n2 = Node(b, name="b")

    network = BayesianNetwork.from_structure(structure=((), (0,)))
    # network.add_nodes(n1, n2)
    # network.add_edge(n1, n2)

    # network.bake()
    network.fit(samples2)

    print(network.probability([[0, 0],
                               [0, 1],
                               [1, 0],
                               [1, 1]]))

    print(network.marginal())


if __name__ == '__main__':
    # montyhall()
    # morse()
    # mini()
    # fitting1()
    # from_sample_struct()
    from_sample()
