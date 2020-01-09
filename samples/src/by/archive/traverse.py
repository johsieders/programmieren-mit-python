def traverse(pred, process):
    k = len(pred)
    process(k)
    for p in pred[k]:
        traverse(pred[:-1], process)


def successors(pred):
    result = []
    for i in range(len(pred)):
        result.append([])

    def process(p):
        k = len(p) - 1
        if k < 0:
            return
        else:
            for i in p[k]:
                result[i].append(k)  # k is successor of i
            process(p[:-1])

    process(pred)
    return (tuple(s) for s in result)


test = ((), (0,), (0, 1), (1, 2), (1, 2, 3), (3, 4))

if __name__ == '__main__':
    succ = successors(test)
