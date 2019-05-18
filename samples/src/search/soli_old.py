# das Solitaer-Spiel
# Simon Siedersleben
# 29.12.02

from operator import add

Board = map(list, 7 * [7 * [None]])


def b(x, y):
    if x in (0, 1, 5, 6) and y in (0, 1, 5, 6):
        return 9
    elif (x, y) == (3, 3):
        return 0
    else:
        return 1


def ypsilon(x):
    if x in (0, 1, 5, 6):
        return (2, 3, 4)
    elif x in (2, 3, 4):
        return range(7)
    else:
        assert 0


def resetBoard():
    global Board
    for x in range(7):
        for y in range(7):
            Board[x][y] = b(x, y)


## Jetzt gilt       
##    Board == [[9, 9, 1, 1, 1, 9, 9], \
##              [9, 9, 1, 1, 1, 9, 9], \
##              [1, 1, 1, 1, 1, 1, 1], \
##              [1, 1, 1, 0, 1, 1, 1], \
##              [1, 1, 1, 1, 1, 1, 1], \
##              [9, 9, 1, 1, 1, 9, 9], \
##              [9, 9, 1, 1, 1, 9, 9]]

resetBoard()


def count():
    """ liefert die Anzahl der besetzten Felder """
    return reduce(add, [u.count(1) for u in Board])


def isValid(x, y):
    """ prueft, ob (x,y) auf dem Feld liegt """
    return 0 <= x < 7 and \
           0 <= y < 7 and \
           Board[x][y] in (0, 1)


def printBoard():
    for u in Board:
        print
        u


def mayMoveUp(x, y):
    return isValid(x, y) and \
           isValid(x - 2, y) and \
           Board[x][y] is 1 and \
           Board[x - 1][y] is 1 and \
           Board[x - 2][y] is 0


def mayMoveDown(x, y):
    return isValid(x, y) and \
           isValid(x + 2, y) and \
           Board[x][y] is 1 and \
           Board[x + 1][y] is 1 and \
           Board[x + 2][y] is 0


def mayMoveLeft(x, y):
    return isValid(x, y) and \
           isValid(x, y - 2) and \
           Board[x][y] is 1 and \
           Board[x][y - 1] is 1 and \
           Board[x][y - 2] is 0


def mayMoveRight(x, y):
    return isValid(x, y) and \
           isValid(x, y + 2) and \
           Board[x][y] is 1 and \
           Board[x][y + 1] is 1 and \
           Board[x][y + 2] is 0


def mayMove(x, y):
    return mayMoveUp(x, y) or \
           mayMoveDown(x, y) or \
           mayMoveLeft(x, y) or \
           mayMoveRight(x, y)


def getEnds(x, y):
    """ liefert die Punkte, zu denen man von (x,y) aus springen kann """
    result = []
    if mayMoveUp(x, y):
        result.append((x - 2, y))
    if mayMoveDown(x, y):
        result.append((x + 2, y))
    if mayMoveLeft(x, y):
        result.append((x, y - 2))
    if mayMoveRight(x, y):
        result.append((x, y + 2))
    return result


def moveUp(x, y):
    """ (x, y) Start, (x-2, y) Ziel """
    if mayMoveUp(x, y):
        Board[x][y] = 0
        Board[x - 1][y] = 0
        Board[x - 2][y] = 1
        return 1
    else:
        return 0


def moveDown(x, y):
    """ (x, y) Start, (x+2, y) Ziel """
    if mayMoveDown(x, y):
        Board[x][y] = 0
        Board[x + 1][y] = 0
        Board[x + 2][y] = 1
        return 1
    else:
        return 0


def moveLeft(x, y):
    """ (x, y) Start, (x, y-2) Ziel """
    if mayMoveLeft(x, y):
        Board[x][y] = 0
        Board[x][y - 1] = 0
        Board[x][y - 2] = 1
        return 1
    else:
        return 0


def moveRight(x, y):
    """ (x, y) Start, (x, y+2) Ziel """
    if mayMoveRight(x, y):
        Board[x][y] = 0
        Board[x][y + 1] = 0
        Board[x][y + 2] = 1
        return 1
    else:
        return 0


def move(start, target):
    x = start[0]
    y = start[1]
    dx = target[0] - x
    dy = target[1] - y
    if dx == 2:
        moveDown(x, y)
    elif dx == -2:
        moveUp(x, y)
    elif dy == 2:
        moveRight(x, y)
    elif dy == -2:
        moveLeft(x, y)
    elif dx == 0 and dy == 0:
        return
    else:
        assert 0
