import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    grid = []
    for line in inp.splitlines():
        grid.append([ord(x) - ord('a') for x in list(line)])

    sx, sy = helpers.find_nd(grid, ord('S') - ord('a'))
    a_locs = helpers.find_all_nd(grid, 0)
    a_locs.append((sx, sy))

    queue = [(x, y, 0) for x, y in a_locs]
    seen = set(a_locs)

    ex, ey = helpers.find_nd(grid, ord('E') - ord('a'))

    grid[sy][sx] = 0
    grid[ey][ex] = 25

    while queue:
        x, y, dist = queue.pop(0)
        for nx, ny in helpers.adjacent(x, y, grid):
            grad = grid[ny][nx] - grid[y][x]
            if grad > 1: continue
            if (nx, ny) in seen: continue
            seen.add((nx, ny))
            queue.append((nx, ny, dist + 1))
            if nx == ex and ny == ey:
                print(dist + 1)
                return

fname = './12-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
