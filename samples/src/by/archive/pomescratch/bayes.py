# This program creates trivial a Bayesian Network with two nodes
# They represent famous examples such as morse, alarm, blue cabs, mammography, lung cancer

from pomegranate import *


def simple_input(origin, forward):
    org = {}
    for i in range(2):
        org[i] = origin[i]
    dist = DiscreteDistribution(org)  # nodes labeled 0 and 1
    fwd = []
    for i in range(2):
        for j in range(2):
            fwd.append([i, j, forward[i][j]])
    return dist, ConditionalProbabilityTable(fwd, [dist])


def fork_input(origin, forward1, forward2):
    org = {}
    for i in range(2):
        org[i] = origin[i]
    dist = DiscreteDistribution(org)  # nodes labeled 0 and 1
    fwd1 = []
    for i in range(2):
        for j in range(2):
            fwd1.append([i, j, forward1[i][j]])
    fwd2 = []
    for i in range(2):
        for j in range(2):
            fwd2.append([i, j, forward2[i][j]])
    return dist, ConditionalProbabilityTable(fwd1, [dist]), ConditionalProbabilityTable(fwd2, [dist])


def collider_input(origin1, origin2, forward):
    org1 = {}
    for i in range(2):
        org1[i] = origin1[i]
    dist1 = DiscreteDistribution(org1)  # nodes labeled 0 and 1
    org2 = {}
    for i in range(2):
        org2[i] = origin2[i]
    dist2 = DiscreteDistribution(org2)  # nodes labeled 0 and 1
    fwd = []
    for i in range(2):
        for j in range(2):
            fwd.append([i, j, forward[i][j]])

    return dist1, dist2, ConditionalProbabilityTable(fwd, [dist2])


def evidence(network):
    return [network.marginal()[1].probability(i) for i in range(2)]


def backward(network):
    q = [network.predict_proba([None, i])[0] for i in range(2)]
    return [[q[j].probability(k) for k in range(2)] for j in range(2)]


def backward_long(network):
    q = [[network.predict_proba([None, i, j])[0] for i in range(2)] for j in range(2)]
    return [[[q[i][j].probability(k) for k in range(2)] for i in range(2)] for j in range(2)]


def simple(origin, forward):
    dist, cpt = simple_input(origin, forward)
    network = BayesianNetwork('network')
    org = Node(dist)
    evd = Node(cpt)
    network.add_nodes(org, evd)
    network.add_edge(org, evd)
    network.bake()
    return evidence(network), backward(network)


def fork(origin, forward1, forward2):
    """
    :param origin: [p(a), p(xa)]
           forward1 = [[p(b1|a), p(xb1|a)],
                      [p(b1|xa), p(xb1|xa)]
           forward2 = [p(b2|a), p(xb2|a)],
                      [p(b2|xa), p(xb2|xa)]
    :return: evidence1 = [p(b1), p(xb2)]
             evidence2 = [p(b2), p(xb2)]
             Backward = [[p(a|b1, b2), p(xa|b1, b2)],
                         p(a|b1, xb2), p(xa|b1, xb2)]
                         p(a|xb1, b2), p(xa|xb1, b2)]
                         p(a|xb1, xb2), p(xa|xb1, xb2)]]
    """
    dist, cpt1, cpt2 = fork_input(origin, forward1, forward2)
    network = BayesianNetwork('network')
    org = Node(dist)
    evd1 = Node(cpt1)
    evd2 = Node(cpt2)
    network.add_nodes(org, evd1, evd2)
    network.add_edge(org, evd1)
    network.add_edge(org, evd2)
    network.bake()
    return evidence(network), backward_long(network)


def collider(origin1, origin2, forward):
    dist1, dist2, cpt = collider_input(origin1, origin2, forward)
    network = BayesianNetwork('network')
    org1 = Node(dist1)
    org2 = Node(dist2)
    evd = Node(cpt)
    network.add_nodes(org1, org2, evd)
    network.add_edge(org1, evd)
    network.add_edge(org2, evd)
    network.bake()
    return evidence(network), backward(network)


def show(network):
    m = network.marginal()
    p = network.probability([[0, 0], [0, 1], [1, 0], [1, 1]])
    p0 = network.predict_proba([0, None])
    p1 = network.predict_proba([1, None])
    q0 = network.predict_proba([None, 0])
    q1 = network.predict_proba([None, 1])
    pass
