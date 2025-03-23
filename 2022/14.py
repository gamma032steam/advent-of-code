import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    rocks = set()
    for line in inp.splitlines():
        coord = [(int(coord.split(',')[0]), int(coord.split(',')[1])) for coord in line.split(' -> ')]
        for i in range(len(coord) - 1):
            u = coord[i]
            v = coord[i+1]
            if u[0] == v[0]:
                start = min(u[1], v[1])
                end = max(u[1], v[1])
                for k in range(start, end+1):
                    rocks.add((u[0], k))
            else:
                start = min(u[0], v[0])
                end = max(u[0], v[0])
                for k in range(start, end+1):
                    rocks.add((k, u[1]))
                    
    sand = set()
    
    lowest_rock = max([x[1] for x in rocks])
    
    def in_bounds(x, y):
        return y <= lowest_rock + 3
        
    def taken(x, y):
        return (x, y) in rocks or (x, y) in sand or y == lowest_rock + 2
    #print(rocks)
    #print(lowest_rock)
    #return
    not_done = True
    while True:
        sx, sy = 500, 0
        if not not_done: break
        while True:
            l = (sx -1, sy + 1)
            r = (sx + 1, sy + 1)
            d = (sx, sy + 1)
            
            if not in_bounds(sx, sy):
                not_done = False
                break
            
            if not taken(*d):
                sx, sy = d
            elif not taken(*l):
                sx, sy = l
            elif not taken(*r):
                sx, sy = r
            else:
                sand.add((sx, sy))
                if (sx, sy) == (500, 0):
                    not_done = False
                break
    
    print(len(sand))

fname = './14-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample=""""""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
