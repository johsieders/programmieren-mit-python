## scratch
## js 12.11.2006

def take(n, it):
    for i in range(n):
        yield it.next()


def first(n, it):
    return [x for x in take(n, it)]