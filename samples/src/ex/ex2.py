## unit two
## js 10.3.2004

#######################
## index version one ##
#######################

def index1(book):
    """ book[i]      = list of indexable words on page i
        result[word] = list of pages containing word """
    result = {}
    for i, page in enumerate(book):
        for word in page:
            if word not in result.keys():
                result[word] = []
            result[word].append(i)
    return result


#######################
## index version two ##
#######################

def index2(book, keywords):
    """ book[i]  = set of all words on page i
        keywords = set of all indexable words
        result[word] = list of pages containing word """
    result = {}
    for i, page in enumerate(book):
        for word in page & keywords:
            if word not in result.keys():
                result[word] = []
            result[word].append(i)
    return result


###############
### anagram ###
###############


def anagram_sorted(xs):
    return sorted(xs, key=lambda x: sorted(x))


#######################
### boolean formula ###
#######################

from fp.util import unaryAnd, unaryOr, negate


def translate(formula, namespace):
    """ translate a postfix-formula into an executable predicate
    operators are AND, OR, NOT
    namespace contains predicates """

    stack = []
    for token in formula.split():
        if token == "AND":
            p = stack.pop()
            q = stack.pop()
            stack.append(unaryAnd(q, p))
        elif token == "OR":
            p = stack.pop()
            q = stack.pop()
            stack.append(unaryOr(q, p))
        elif token == "NOT":
            p = stack.pop()
            stack.append(negate(p))
        else:
            stack.append(namespace[token])
    assert len(stack) == 1, 'bad formula'
    return stack.pop()
