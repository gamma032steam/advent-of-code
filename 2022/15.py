import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

test_y = 2000000

def solve(inp):

    def manhattan(x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    data = []
    dists = []
    for line in inp.splitlines():
        a, b, c, d = helpers.ints(line)
        data.append([(a,b), (c, d)])
        dists.append(manhattan(*data[-1]))
    
    cnt = 0
    max_x = max([x[0][0] for x in data]) + max(dists)
    min_x = min([x[0][0] for x in data]) - max(dists)
    for x in range(min_x, max_x+1):
        for i, d in enumerate(data):
            c1, c2 = d
            a, b = c1
            r = dists[i]
            if manhattan((a, b), (x, test_y)) <= r:
                cnt += 1
                break

    bs = [x[1] for x in data if x[1][1] == test_y]
    bs = len(set(bs))
    cnt -= bs
    print(cnt)

    all_bs = [x[1] for x in data]
    dx = 0
    while dx < 4000000:
        dy = 0
        # progress bar because its slow
        if dx % 10000 == 0: print((dx / 4000000) * 100)
        while dy < 4000000:
            found = False
            for i, d in enumerate(data):
                c1, _ = d
                a, b = c1
                r = dists[i]
                gap = r - manhattan((a, b), (dx, dy))
                if gap >= 0:
                    found = True
                    dy += gap
                    break
            if not found and ((dx, dy) not in all_bs):
                print((dx * 4000000) + dy)
                return
            dy += 1
        dx += 1
fname = './15-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
