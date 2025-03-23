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
    for y in range(highest + 7, highest - 10, -1):
        line = ''
        for x in range(7):
            if (x, y) in taken_cells:
                line += '#'
            elif (x, y) in shape_points:
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
    cache = dict()
    last = None

    #target = 2022
    target = 1000000000000
    prints = list(range(0, target, target // 5000))
    done = False
    while n_shapes < target:
        shape = shapes[n_shapes % 5]
        n_shapes += 1
        # place the shape
        shape_points = []
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == '.': continue
                shape_points.append([2 + j, highest + 3 + len(shape) - i])
        if done: print(n_shapes)

        # drop
        while True:
            time += 1
            time %= len(jet)

            # apply gas
            new_points = [(x + (1 if jet[time] == '>' else -1), y) for x, y in shape_points]
            if not any([(x, y) in taken_cells or x < 0 or x > 6 for x, y in new_points]):
                shape_points = new_points
            
            # fall
            new_points = [(x, y - 1) for x, y in shape_points]
            if any([(x, y) in taken_cells or y <= floor for x, y in new_points]):
                #print_grid(highest, taken_cells, shape_points)
                # stop falling
                for x, y in shape_points:
                    highest = max(highest, y)
                    taken_cells.add((x, y))
                # if we see a full row of points, delete everything under it
                for _, y in shape_points:
                    if all([(tx, y) in taken_cells for tx in range(7)]):
                        # set a new minimum
                        floor = y

                        # delete the points
                        to_remove = [(rx, ry) for rx, ry in taken_cells if ry <= floor]   
                        for taken_x, taken_y in to_remove:
                            taken_cells.remove((taken_x, taken_y))

                        # search the cache
                        while len(taken_cells) == 1:
                            # progress bar
                            if prints and n_shapes > prints[0]:
                                prints.pop(0) 
                                print((n_shapes / target) * 100, (len(cache) / (6 * len(jet) * 5) * 100)) 

                            # update cache
                            if last is not None:
                                old_x, old_time, old_shape, old_highest, old_shapes = last
                                cache[(old_x, old_time, old_shape)] = (list(taken_cells)[0][0], highest - old_highest, n_shapes - old_shapes, time)
                            
                            # record the position for the next clearout
                            last = (list(taken_cells)[0][0], time, n_shapes % 5, highest, n_shapes)
                            
                            # test cache
                            if (list(taken_cells)[0][0], time, n_shapes % 5) in cache:
                                if done: print('cache hit', list(taken_cells), n_shapes)
                                new_x, height, new_shapes, new_time = cache[(list(taken_cells)[0][0], time, n_shapes % 5)]
                                if n_shapes + new_shapes >= target: 
                                    done = True
                                    break
                                time = new_time
                                highest += height
                                n_shapes += new_shapes
                                floor = highest - 1
                                taken_cells = set([(new_x, highest)])
                            else:
                                break
                        break
                break
            shape_points = new_points
    print(highest + 1)
fname = './17-input.txt' 
try:
    f = open(fname)
except Exception as e:
    pass
    #print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample=""">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    #solve(sample)
    print('------------')
