## Tiefe-Zuerst-Suche fuer Solitaer
## js 2.1.2003

from __future__ import generators

BOARD = ((0, 2), (0, 3), (0, 4), \
         (1, 2), (1, 3), (1, 4), \
         (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), \
         (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), \
         (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), \
         (5, 2), (5, 3), (5, 4), \
         (6, 2), (6, 3), (6, 4))


def initBoard():
    on = {}
    for s in BOARD:
        on[s] = 1
    on[(3, 3)] = 0
    return on


def printBoard(on):
    for x in range(7):
        print[on.get((x, y), 9)
        for y in range(7)]


def up(s):
    return s, (s[0] - 1, s[1]), (s[0] - 2, s[1])


def down(s):
    return s, (s[0] + 1, s[1]), (s[0] + 2, s[1])


def left(s):
    return s, (s[0], s[1] - 1), (s[0], s[1] - 2)


def right(s):
    return s, (s[0], s[1] + 1), (s[0], s[1] + 2)


def move(s, d, on):
    s0, s1, s2 = d(s)
    if s2 in BOARD and \
            on[s0] and on[s1] and not on[s2]:
        on[s0], on[s1], on[s2] = 0, 0, 1
        return 1
    else:
        return 0


def undo(s, d, on):
    s0, s1, s2 = d(s)
    on[s0], on[s1], on[s2] = 1, 1, 0


cnt = 0
maxmoves = 0


def search(on, moves=[], result=[]):
    global cnt, maxmoves
    if cnt % 10000 == 0:
        print
        "still alive ", cnt, maxmoves
    cnt += 1

    if len(moves) >= 30:
        yield moves

    for s in BOARD:
        for d in (up, left, down, right):
            if move(s, d, on):
                moves.append((s, d))
                maxmoves = max(maxmoves, len(moves))
                search(on, moves, result)
                moves.pop()
                undo(s, d, on)


if __name__ == "__main__":
    on = initBoard()
    for r in search(on):
        print
        r
