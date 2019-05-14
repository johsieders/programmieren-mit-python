## sudoku
## js 5.11.2006

from sets import Set
from numarray import *
from search import *
from types import *
from string import *


## Sudoku as a search problem
## state is a 9x9 numarray, values ranging from 0 to 9 included
## 0 indicates an empty field
## position is an index in range 0..8, 0..8
## the dictionary used contains the used values for each position

def int0(c):
    if c in digits:
        return int(c)
    else:
        return 0
    

class SudokuProblem(SearchProblem):
    def __init__(self, input):
                                    ## contains used digits for each entry (i, j)
        self.__used  = [[[] for i in range(9)] for j in range(9)]
        
        ## The constructor accepts
        ## a) a list of 81 characters: - or an integer between 1 and 9 or
        ## b) a string representing 81 integers (separators being blank and newline)
        if type(input) is NumArray:
            self.__state = array(input)
        elif type(input) is StringType:
            tmp = [int0(c) for c in split(input)]
            self.__state = array(tmp)
        self.__state.shape = 9, 9            

    def row(self, i):           ## 0 <= i <= 2
        return self.__state[i, :]

    def col(self, j):           ## 0 <= j <= 2
        return self.__state[:, j]

    def box(self, i, j):        ## 0 <= i, j <= 2
        return self.__state[i*3: (i + 1)*3, j*3: (j + 1)*3]

    def ok(self):
        for n in range(1, 10):
            for i in range(9):     ## check columns and rows
                if list(self.col(i)).count(n) > 1:
                    return False
                if list(self.row(i)).count(n) > 1:
                    return False
            for i in range(3):     ## check boxes
                for j in range(3):
                    a = array(self.box(i, j))
                    a.ravel()
                    if list(a).count(n) > 1:
                        return False
        return True


    def gotSolution(self):
        for n in range(1, 10):
            for i in range(9):     ## check columns and rows
                if list(self.col(i)).count(n) != 1:
                    return False
                if list(self.row(i)).count(n) != 1:
                    return False
            for i in range(3):     ## check boxes
                for j in range(3):
                    a = array(self.box(i, j))
                    a.ravel()
                    if list(a).count(n) != 1:
                        return False
        return True


    def candidates(self, i, j):
        ## returns all candidate values at position i, j
        ## if that position is empty, else return the empty set.
        ## candidate values = {1, ..10} - row - column - box
        if self.__state[i, j] == 0:
            a = array(self.box(i/3, j/3))
            a.ravel()
            return set(range(1, 10))    \
                 - set(self.row(i))     \
                 - set(self.col(j))     \
                 - set(list(a))         \
                 - set(self.__used[i][j])
        else:
            return set()

        
    def next(self):
        ## next returns a step
        ## a step ist a tuple (i, j, value)
        ## the position is the one with the smallest number of candidates
        ## the value is an arbitrary admissible value for that position
        
        m0 = 10             
        for i in range(9):          
            for j in range(9):
                if self.__state[i, j] != 0:  ## consider only empty fields
                    continue
                c = self.candidates(i, j)
                if len(c) == 0:
                    raise StopIteration     ## dead end
                if len(c) < m0:
                    c0, i0, j0, m0 = c, i, j, len(c)
                    
        if 0 < m0 < 10:             ## candidate found
            return i0, j0, c0.pop()
        else:
            raise StopIteration     ## no candidate left
                
    def __iter__(self):
        return self
    
    def getState(self):
        return array(self.__state)

    def doStep(self, step):
        i, j, val = step
        self.__state[i][j] = val
        if self.__used[i][j]:
            self.__used[i][j].pop()

    def undoStep(self, step):
        i, j, val = step
        self.__state[i][j] = 0
        self.__used[i][j].append(val)

    def __str__(self):
        s = ""
        for i in range(9):
            if i%3 == 0 and i > 0:
                s += "\n"
            for j in range(9):
                if j%3 == 0 and j > 0:
                    s += "  "
                c = str(self.__state[i, j])
                if c == '0':
                    c = '-'
                s = s + c + ' '

            s += "\n"
        return s    
        

    
