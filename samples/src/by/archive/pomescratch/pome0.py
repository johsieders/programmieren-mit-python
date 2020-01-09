# This program shows three different methods to build a Bayesian Network
# from_dist_struct: from the distribution and the structure
# from_sample_struct: from the samples and the structure, the distribution being derived form the samples
# from_sample: from samples only, distribution and structure being derived from the samples

# The example is a trivial network with two nodes and one edge from node 0 to node 1.

import numpy as np
from pomegranate import *


def from_dist_struct():
    network = BayesianNetwork("trivial")
    dist = DiscreteDistribution({0: 1 / 3, 1: 2 / 3})  # nodes labeled 0 and 1
    cpt = ConditionalProbabilityTable(
        [[0, 0, 1],
         [0, 1, 0],
         [1, 0, 0],
         [1, 1, 1]], [dist])
    n0 = Node(dist)
    n1 = Node(cpt)
    network.add_nodes(n0, n1)
    network.add_edge(n0, n1)
    network.bake()
    return network


def from_sample_struct():
    structure = ((), (0,))
    sample = np.array([[0, 0], [1, 1], [1, 1]])
    return BayesianNetwork.from_structure(sample, structure)


def from_sample():
    sample = np.array([[0, 0], [1, 1], [1, 1]])
    return BayesianNetwork.from_samples(sample, algorithm='exact')


def show(network):
    m = network.marginal()
    p = network.probability([[0, 0], [0, 1], [1, 0], [1, 1]])
    p.any()
    p0 = network.predict_proba([0, None])
    p1 = network.predict_proba([1, None])
    print(p0, p1)


if __name__ == '__main__':
    networks = [from_dist_struct(), from_sample_struct(), from_sample()]
    nw = networks[0]
    show(nw)
