from math import isclose

import numpy as np


def simple(origin, forward):
    """
    :param origin: [p(a), p(xa)]
    :param forward: [[p(b|a), p(xb|a)],
                     [p(b|xa), p(xb|xa)]]
    :return: evidence = [p[b], p[xb]],
             backward = [[p(a|b), p(xa|b)],
                         [p(a|xb), p(xa|xb)]]
    simple(*simple(origin, forward)) = origin, forward
    """
    org = np.array(origin).reshape(2, 1)  # make it a column
    if not isclose(org.sum(), 1.0, abs_tol=1e-5):
        raise Exception

    fwd = np.array(forward).reshape(2, 2)
    if any([not isclose(p, 1.0, abs_tol=1e-5) for p in fwd.sum(axis=1)]):  # sum over rows
        raise Exception

    joint = fwd * org  # p(a, b) = p(b|a) * p(a)
    evidence = joint.sum(axis=0)  # p(b) = p(a, b) + p(xa, b)
    backward = (joint / evidence).T  # p(a, b) / p(b)
    return evidence, backward


def fork(origin, forward1, forward2):
    """
    :param origin: [p(a), p(xa)]
           forward1 = [[p(b1|a), p(xb1|a)],
                      [p(b1|xa), p(xb1|xa)]
           forward2 = [p(b2|a), p(xb2|a)],
                      [p(b2|xa), p(xb2|xa)]
    :return: evidence1 = [p(b1), p(xb2)]
             evidence2 =  [p(b2), p(xb2)]
             Backward = [[p(a|b1, b2), p(xa|b1, b2)],
                         p(a|b1, xb2), p(xa|b1, xb2)]
                         p(a|xb1, b2), p(xa|xb1, b2)]
                         p(a|xb1, xb2), p(xa|xb1, xb2)]]
           """
    org = np.array(origin).reshape(2, 1)  # make it a column
    if not isclose(org.sum(), 1.0, abs_tol=1e-5):  # sum over row
        raise Exception

    fwd1 = np.array(forward1).reshape(2, 2)
    if any([not isclose(p, 1.0, abs_tol=1e-5) for p in fwd1.sum(axis=1)]):  # sums over rows
        raise Exception

    fwd2 = np.array(forward2).reshape(2, 2)
    if any([not isclose(p, 1.0, abs_tol=1e-5) for p in fwd1.sum(axis=1)]):  # sums over rows
        raise Exception

    joint = fwd1 * fwd2 * org  # p(a, b) = p(b|a) * p(a)
    evidence = joint.sum(axis=0)  # p(b) = p(a, b) + p(xa, b)
    backward = (joint / evidence).T  # p(a, b) / p(b)   backward.shape = (2, 4)
    return evidence, backward


def collider(origin1, origin2, Forward):
    """
       :param origin1: [p(a1), p(xa1)]
              origin2: [p(a2), p(xa2)]
       :param forward: [[p(b|a1, a2), p(xb|a1, a2)],
                         p(b|a1, xa2), p(xb|a1, xa2)]
                         p(b|xa1, a2), p(xb|xa1, a2)]
                         p(b|xa1, xa2), p(xb|xa1, xa2)]]
       :return: evidence = [p[b], p[xb]]
                backward = [[p(a1,a2|b), p(a1, xa2|b), p(xa1, a2|b), p(xa1, xa2|b)]
                            [p(a1,a2|xb), p(a1, xa2|xb), p(xa1, a2|xb), p(xa1, xa2|xb)]]
       """
    tmp = np.array(origin1).reshape(2, 2)  # make it two columns
    if any([not isclose(p, 1.0, abs_tol=1e-5) for p in tmp.sum(axis=1)]):  # sums over rows
        raise Exception
    org = np.outer(tmp[0], tmp[1]).reshape(4, 1)

    fwd = np.array(Forward).reshape(4, 2)
    if any([not isclose(p, 1.0, abs_tol=1e-5) for p in fwd.sum(axis=1)]):  # sums over rows
        raise Exception

    joint = fwd * org  # p(a, b) = p(b|a) * p(a)
    evidence = joint.sum(axis=0)  # p(b) = p(a, b) + p(xa, b)
    backward = (joint / evidence).T  # p(a, b) / p(b)
    return evidence, backward


def chain(origin, forward1, forward2):
    """
       :param origin: [p(a), p(xa)]
       :param forward1: [[p(h|a), p(xh|a)],
                        [p(h|xa), p(xh|xa)]]         ]
       :param forward2: [[p(b|h), p(xb|h)],
                        [p(b|xh), p(xb|xh)]]
       :return: evidence = [p[b], p[xb]],
                backward = [[p(a|b), p(xa|b)],
                            [p(a|xb), p(xa|xb)]]
       """
    org = np.array(origin).reshape(2, 1)  # make it a column
    if not isclose(org.sum(), 1.0, abs_tol=1e-5):
        raise Exception

    fwd = np.array(forward1).reshape(4, 2)
    if any([not isclose(p, 1.0, abs_tol=1e-5) for p in fwd.sum(axis=1)]):  # sum over rows
        raise Exception

    joint = fwd * org  # p(a, b) = p(b|a) * p(a)
    evidence = joint.sum(axis=0)  # p(b) = p(a, b) + p(xa, b)
    backward = (joint / evidence).T  # p(a, b) / p(b)
    return evidence, backward


def test_fork():
    triv = 2 * [0.5], 8 * [0.25]
    tc1 = [0.7, 0.3], [0.7, 0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3]

    for tc in [triv, tc1]:
        print(fork(*tc))
