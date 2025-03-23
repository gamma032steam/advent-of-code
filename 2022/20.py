import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    n = []
    w = 0
    key = 811589153

    inps = len(inp.splitlines())
    for line in inp.splitlines():
        v = int(line) * key
        n.append((v, w))
        w += 1

    for _ in range(10):
        goal = 0
        while goal < len(n):
            i = -1
            for j, x in enumerate(n):
                if x[1] == goal:
                    i = j
                    break
            assert(i != -1)

            k, done = n[i]

            n.pop(i)
            new_i = (i + k) % len(n)
            n.insert(new_i, (k, goal))

            goal += 1
    vals = [v[0] for v in n]
    s = 0
    print(vals)
    zero_idx = vals.index(0)
    for i in [1000, 2000, 3000]:
        print(vals[i % len(vals)])
        s += vals[(i + zero_idx) % len(vals)]
    print(s)


fname = './20-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""1
2
-3
3
-2
0
4
"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
