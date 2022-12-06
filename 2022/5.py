import math 
import functools
import re
import random
import collections
from helpers import *
import sys
sys.setrecursionlimit(100000)

start = {
    1: ['Z', 'T', 'F', 'R', 'W', 'J', 'G'],
    2: ['G', 'W', 'M'],
    3: ['J', 'N', 'H', 'G'],
    4: ['J', 'R', 'C', 'N', 'W'],
    5: ['W', 'F', 'S', 'B', 'G', 'Q','V', 'M'],
    6: ['S', 'R', 'T', 'D', 'V', 'W', 'C'],
    7: ['H,', 'B', 'N', 'C', 'D', 'Z', 'G', 'V'],
    8: ['S', 'J', 'N', 'M', 'G', 'C'],
    9: ['G', 'P', 'N', 'W', 'C', 'J', 'D', 'L']
}

# start = {
#     1: ['Z', 'N'],
#     2: ['M', 'C', 'D'],
#     3: ['P']
# }

with open('./input.txt') as f:
    data = f.read().strip()
    _, y = data.split('\n\n')
    #print(x)
    ins = []
    for l in y.split('\n'):
        n, f, t = [int(x) for x in re.search(r'move (\d+) from (\d+) to (\d+)', l).groups()]
        ins.append((n, f, t))
    for n, f, t in ins:
        #if n == 6: break
        # for _ in range(n):
        #     next = start[f].pop()
        #     start[t].append(next)
        next = start[f][-n:]
        start[f] = start[f][:-n]
        print(start[f], start[f][-n:], n, start[t])

        start[t].extend(next)
        print(start[t])
        print(start)

    c = ""
    for i in range(1, 10):
        c += start[i][-1]
    #print(start)
    print(c)