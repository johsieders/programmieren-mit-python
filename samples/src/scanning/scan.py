
## Scanning nach Let Over Lambda
## js 10.08.2011
## Tuntenhausen

## Problem: a text is delivered in blocks. How often does
## the string trigger occur (all blocks concatenated)?
## 
## Solution: scanner returns the function aux that keeps the trigger
## and the number idx of matched characters. Each call of aux leaves
## behind the match count idx for the next call.

## The nonlocal variable idx is shared by all calls of aux,
## but invisible outside.


def scanner(trigger):
    idx = 0                 ## that many characters have matched so far
    def aux(block):
        nonlocal idx
        hits = 0            ## number of hits in current block
        for c in block:
            if c == trigger[idx]:
                idx += 1    ## one more character match
            else: 
                idx = 0     ## no match, start over
            if idx == len(trigger):                
                hits += 1
                idx = 0     ## match completed, start over
        return hits
    return aux


if __name__ == '__main__':
    s = scanner('abc')
    print(s('xyab'))       ## 0
    print(s('cxyab'))      ## 1
    print(s('cxyabc'))     ## 2
    print(s('cxyabcabca')) ## 2
    print(s('b'))          ## 0
    print(s('c'))          ## 1

