import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

# x, y deltas
directions = [ 
    [(-1, -1), (0, -1), (1, -1)], # N
    [(-1, 1), (0, 1), (1, 1)],    # S
    [(-1, 1), (-1, 0), (-1, -1)], # W
    [(1, 1), (1, 0), (1, -1)]     # E
]

strict_directions = [
    (0, -1),  # N
    (0, 1), # S
    (-1, 0), # W
    (1, 0)   # E
]

def solve(inp):
    elves = set()
    for y, line in enumerate(inp.splitlines()):
        for x, c in enumerate(line):
            if c == '#': elves.add((x, y))

    order = [0, 1, 2, 3] 
    turn = 1
    while True:
        # propose moving
        proposals = []
        for elf in elves:
            x, y = elf

            # don't move if there's anything around
            any_around = False
            for new_x, new_y in helpers.adjacent(x, y, diags=True):
                if (new_x, new_y) in elves:
                    any_around = True
                    break
            if not any_around: continue

            for direction in order:
                # check if there's anything in that direction
                any_in_dir = False
                for dx, dy in directions[direction]:
                    new_x, new_y = x + dx, y + dy
                    if (new_x, new_y) in elves:
                        any_in_dir = True
                        break

                # propose
                if not any_in_dir:
                    dx, dy = strict_directions[direction]
                    new_x, new_y = x + dx, y + dy
                    proposals.append(((x, y), (new_x, new_y)))
                    break
    
        # part 2: check if nothing wants to move
        if not proposals:
            print(turn, proposals)
            return

        # move
        for i, proposal in enumerate(proposals):
            before, after = proposal
            # check that noone else wants to move there
            ok = True
            for j, p in enumerate(proposals):
                _, a = p
                if i != j and a == after:
                    ok = False
                    break

            # move!
            if ok:
                elves.remove(before)
                elves.add(after)

        # next direction
        x = order.pop(0)
        order.append(x)
        minx, maxx, miny, maxy = helpers.min_max_bounds(elves)

        turn += 1

        # debug code: print the grid
        # print(turn)
        # for y in range(miny, maxy + 1):
        #     s = ''
        #     for x in range(minx, maxx + 1):
        #         s += '#' if (x, y) in elves else '.'
        #     print(s)
        # print('\n')


    # count the empty squares
    minx, maxx, miny, maxy = helpers.min_max_bounds(elves)
    size = (maxx - minx + 1) * (maxy - miny + 1)
    size -= len(elves)
    print(size)


        
fname = './23-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

# sample=""".....
# ..##.
# ..#..
# .....
# ..##.
# ....."""
sample="""..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
