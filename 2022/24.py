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
    storms = []
    for y, line in enumerate(inp.splitlines()):
        grid.append(list(line))
        for x, c in enumerate(line):
            if c in ['v', '^', '>', '<']:
                storms.append((x, y, c))

    maps = [storms]
    def next_storm():
        new_storm = []
        for a, b, c in maps[-1]:
            new_x, new_y = a, b
            match c:
                case 'v':
                    new_y += 1
                case '^':
                    new_y -= 1
                case '>':
                    new_x += 1
                case '<':
                    new_x -= 1
                case _:
                    assert(False)
            if new_x == 0: new_x = len(grid[0]) - 2
            if new_x == len(grid[0]) - 1: new_x = 1

            if new_y == 0: new_y = len(grid) - 2
            if new_y == len(grid) - 1: new_y = 1
            new_storm.append((new_x, new_y, c))
        maps.append(new_storm)

    q = [(0, 1, 0, False, False)]
    seen = set([(0, 1, 0, False, False)])
    h = False
    i = False
    while q:
        dist, x, y, been_end, been_start = q.pop(0)
        if h and not been_end: continue
        if i and not been_start: continue

        if y == len(grid) - 1 and x == len(grid[0]) - 2:
            been_end = True
            h = True

        if (x, y) == (1, 0) and been_end:
            been_start = True
            i = True

        if y == len(grid) - 1 and x == len(grid[0]) - 2 and been_start and been_end:
            print(dist - 1)
            return

        if len(maps) < dist + 1:
            next_storm()
        storm = maps[dist]

        for new_x, new_y in [*helpers.adjacent(x, y), (x, y)]:
            if not(1 <= new_x < (len(grid[0]) -1) and 1 <= new_y < (len(grid) - 1)) and not ((new_x, new_y) == (1, 0)) and not (new_y == len(grid) - 1 and new_x == len(grid[0]) - 2): continue
            if (dist + 1, new_x, new_y, been_end, been_start) in seen: continue
            ok = True
            
            for a, b, k in storm:
                if new_x == a and new_y == b:
                    ok = False
                    break

            if not ok: continue
            
            seen.add((dist + 1, new_x, new_y, been_end, been_start))
            q.append((dist + 1, new_x, new_y, been_end, been_start)) 

    assert(False)

fname = './24-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
