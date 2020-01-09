def bayes(p, q1, q2):
    # p  = probability of exception = P(A2)
    # q1 = probability of alarm if no exception (false alarm) = P(B2|A1)
    # q2 = probability of alarm if exception (alarm) = P(B2|A2)

    r = q1 * (1 - p) + q2 * p  # probability of alarm = P(B2)
    s1 = p * (1 - q2) / (1 - r)  # s1 = probability of exception if no alarm (silent exception) = P(A2|B1)
    s2 = p * q2 / r  # s2 = probability of exception if alarm (true alarm) = P(A2|B2)

    return r, s1, s2


def bag(p, n):
    def aux(t):
        return p * (n - t) / (n - p * t)

    return aux


if __name__ == '__main__':
    # mammographie
    mam = [1 / 700, ]
    p = 0.9
    result0 = [[p, 0.0, 1.0], [p, 0.5, 0.5], [p, 0.1, 0.9], [p, 0.2, 0.7], [p, 0.2, 0.9], [p, 1.0, 0.]]
    result1 = [bayes(*bayes(*arg)) for arg in result0]

    for i in range(len(result0)):
        print([x - y for x, y in zip(result0[i], result1[i])])

    ## print([[x - y for x, y in zip(r0, r1)] for r0, r1 in zip(result0, result1)])
