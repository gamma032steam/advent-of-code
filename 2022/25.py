import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

cmap = {
    '-': -1,
    '=': -2
}

def solve(inp):
    ns = []
    for line in inp.splitlines():
        ns.append([int(x) if x.isnumeric() else cmap[x] for x in list(line)])
    
    def snafu_to_dec(n):
        t = 0
        c = 1
        for i in range(len(n) - 1, -1, -1):
            t += c * n[i]
            c *= 5
        return t

    dec_sum = sum([snafu_to_dec(x) for x in ns])

    def dec_to_snafu(n):
        # starting from the most significant digit, add digits as so:
        # -2.5x <= n <= -1.5x -> -2
        # -0.5 <= n <= -1.5x -> -1
        # -0.5x <= n <= 0.5x -> 0
        # 0.5 <= n <= 1.5x -> 1
        # 1.5x <= n <= 2.5x -> 2
        c = 1
        res = []

        # find most significant digit
        while (2.5 * c) < n:
            c *= 5

        # add digits
        while c >= 1:
            if (-2.5 * c) <= n <= (-1.5 * c):
                res.append('=')
                n += 2 * c
            elif (-1.5 * c) <= n <= (-0.5 * c):
                res.append('-')
                n += c
            elif (-0.5 * c) <= n <= (0.5 * c):
                res.append('0')
            elif (0.5 * c) <= n <= (1.5 * c):
                res.append('1')
                n -= c
            elif (1.5 * c) <= n <= (2.5 * c):
                res.append('2')
                n -= 2 * c
            c //= 5
        
        return ''.join(res)

    print(dec_to_snafu(dec_sum))

fname = './25-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
