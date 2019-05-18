## depth-first search
## js 27.06.04

def abstract():
    raise NotImplementedError


## Java-like interface
class SearchProblem(object):
    def __init__(self):
        abstract()

    def done(self):
        abstract()

    def getState(self):
        abstract()

    def __iter__(self):
        abstract()

    def do(self, step):
        abstract()

    def undo(self, step):
        abstract()


## search by Java-like class
class SearchByClass(object):
    def __init__(self, problem):
        if not isinstance(problem, SearchProblem):
            raise TypeError
        self.__problem = problem
        self.__solutions = []

    def search(self):
        if self.__problem.done():
            self.__solutions.append(self.__problem.getState())
            return list(self.__solutions)

        for step in self.__problem:
            self.__problem.do(step)
            self.search()
            self.__problem.undo(step)


## search by function
def searchByFunction(problem):
    if problem.done():
        return [problem.getState()]

    result = []
    for option in problem:
        problem.do(option)
        result += searchByFunction(problem)
        problem.undo(option)
    return result


## search by generator
def searchByGenerator(problem):
    if problem.done():
        yield problem.getState()

    for option in problem:
        problem.do(option)
        for x in searchByGenerator(problem):
            yield x
        problem.undo(option)


## permutations as a hello-world search problem
class PermutationProblem(SearchProblem):
    def __init__(self, xs):
        self.__xs = set(xs)
        self.__state = []

    def getState(self):
        return list(self.__state)

    def __iter__(self):
        return iter(self.__xs - set(self.__state))

    def do(self, step):
        self.__state.append(step)

    def undo(self, step):
        self.__state.pop()

    def done(self):
        return len(self.__state) == len(self.__xs)


pp = PermutationProblem
