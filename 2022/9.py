import math 
import functools
import re
import random
import collections
from helpers import *
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    x, y = 0, 0
    a, b = 0, 0
    seen = set()
    for line in inp.splitlines():
        direction, dist = line.split()
        dist = int(dist)
        #print(direction, dist)
        for _ in range(dist):
            if direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            elif direction == 'L':
                x -= 1
            else:
                x += 1

            if x != a and y != b and (abs(x - a) > 1 or abs(y-b) > 1):
                if x > a:
                    a += 1
                else:
                    a -= 1
                if y > b:
                    b += 1
                else:
                    b -= 1
            elif abs(x - a) > 1:
                if x > a:
                    a += 1
                else:
                    a -= 1
            elif abs(y - b) > 1:
                if y > b:
                    b += 1
                else:
                    b -= 1
                
            seen.add((a, b))
            #print(a,b, x, y)
    print(len(seen))

    seen = set()
    rope = [[0, 0] for _ in range(10)]
    for line in inp.splitlines():
        direction, dist = line.split()
        dist = int(dist)

        for _ in range(dist):
            # move the head
            if direction == 'U':
                rope[0][1] += 1
            elif direction == 'D':
                rope[0][1] -= 1
            elif direction == 'L':
                rope[0][0] -= 1
            else:
                rope[0][0] += 1

            # everything else follow's what's in front
            for i in range(1, len(rope)):
                x,y = rope[i-1]
                a,b = rope[i]
                if x != a and y != b and (abs(x - a) > 1 or abs(y-b) > 1):
                    if x > a:
                        a += 1
                    else:
                        a -= 1
                    if y > b:
                        b += 1
                    else:
                        b -= 1
                elif abs(x - a) > 1:
                    if x > a:
                        a += 1
                    else:
                        a -= 1
                elif abs(y - b) > 1:
                    if y > b:
                        b += 1
                    else:
                        b -= 1
                rope[i] = [a,b]
                if i == 9: seen.add((a,b))
    print(len(seen))
fname = './9-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
