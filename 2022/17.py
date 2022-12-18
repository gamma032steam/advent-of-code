import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

shapes = [
    [
        '####'
    ],
    [
        '.#.',
        '###',
        '.#.'
    ],
    [
        '..#',
        '..#',
        '###'
    ],
    [
        '#',
        '#',
        '#',
        '#'
    ],
    [
        '##',
        '##'
    ]
]

def print_grid(highest, taken_cells, shape_points):
    for y in range(highest + 7, -1, -1):
        line = ''
        for x in range(7):
            if (x, y) in taken_cells:
                line += '#'
            elif [x, y] in shape_points:
                line += '@'
            else:
                line += '.'
        print(line)
    print('\n')

def solve(jet): 
    n_shapes = 0
    taken_cells = set()
    highest = -1
    time = -1
    floor = -1
    while n_shapes < 2022:
        shape = shapes[n_shapes % 5]
        n_shapes += 1
        # place the shape
        shape_points = []
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == '.': continue
                shape_points.append([2 + j, highest + 3 + len(shape) - i])
        #print_grid(highest, taken_cells, shape_points)
        while True:
            time += 1
            if time >= len(jet): time = 0
            # apply gas
            new_points = [(x + (1 if jet[time] == '>' else -1), y) for x, y in shape_points]
            if not any([(x, y) in taken_cells or x < 0 or x > 6 for x, y in new_points]):
                shape_points = new_points
            # fall
            new_points = [(x, y - 1) for x, y in shape_points]
            if any([(x, y) in taken_cells or y <= floor for x, y in new_points]):
                # stop falling
                for x, y in shape_points:
                    highest = max(highest, y)
                    taken_cells.add((x, y))
                break
            shape_points = new_points
    print(highest + 1)
fname = './input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample=""">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
