import math 
import functools
import re
import random
import collections
import sys
import numpy as np
sys.setrecursionlimit(100000)

def solve(inp):
    cycle = 1
    register = 1
    tot = 0
    for operation in inp.splitlines():
        if (cycle - 20) % 40 == 0 and cycle <= 240:
            tot += register * cycle
        cycle += 1
        if operation.startswith('addx'):
            if (cycle - 20) % 40 == 0 and cycle <= 240:
                tot += register * cycle 
            cycle += 1
            register += int(operation.split()[1])

    print(tot)

    grid = [[None for _ in range(40)] for _ in range(6)]
    cycle = 1
    register = 1
    def draw():
        if abs(register - ((cycle-1) % 40)) <= 1:
            grid[(cycle - 1) // 40][(cycle - 1) % 40] = '#'
        else:
            pass
            grid[(cycle - 1) // 40][(cycle - 1) % 40] = '.'

    for operation in inp.splitlines():
        draw()
        cycle += 1
        if operation.startswith('addx'):
            draw()
            cycle += 1
            register += int(operation.split()[1])

    for line in grid:
        print(''.join(line))

fname = './input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
