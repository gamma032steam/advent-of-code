import math 
import functools
import re
import random
import collections
from helpers import *
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    grid = [list(x) for x in inp.splitlines()]

    num_visible = 0
    best_scenic = -1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            visible_sides = 4
            scenic_score = 1
            for dir in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                curr_i, curr_j = i, j
                height = grid[i][j]
                distance = 0
                while True:
                    curr_i += dir[0]
                    curr_j += dir[1]
                    if not (0 <= curr_i < len(grid) and 0 <= curr_j < len(grid[0])): break
                    if grid[curr_i][curr_j] >= height:
                        visible_sides -= 1
                        distance += 1
                        break
                    distance += 1
                scenic_score *= distance
            
            if visible_sides > 0:
                num_visible += 1
            best_scenic = max(best_scenic, scenic_score)
    print(num_visible)
    print(best_scenic)

fname = './8-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""30373
25512
65332
33549
35390
"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
