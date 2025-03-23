import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

sides = {
    "A": { # shape
        "U": ("F", "D", False), # (face, edge, reversed)
        "D": ("C", "R", False),
        "L": ("B", "R", False),
        "R": ("D", "R", True)
    },
    "B": {
        "U": ("F", "L", False),
        "D": ("C", "U", False),
        "L": ("E", "L", True),
        "R": ("A", "L", False)
    },
    "C": {
        "U": ("B", "D", False),
        "D": ("D", "U", False),
        "L": ("E", "U", False),
        "R": ("A", "D", False)
    },
    "D": {
        "U": ("C", "D", False),
        "D": ("F", "R", False),
        "L": ("E", "R", False),
        "R": ("A", "R", True)
    },
    "E": {
        "U": ("C", "L", False),
        "D": ("F", "U", False),
        "L": ("B", "L", True),
        "R": ("D", "L", False)
    },
    "F": {
        "U": ("E", "D", False),
        "D": ("A", "U", False),
        "L": ("B", "U", False),
        "R": ("D", "D", False)
    }
}

# validation
for start_side, value in sides.items():
    for start_dir in ["U", "D", "L", "R"]:
        end_side, end_dir, reverse = value[start_dir]
        # cross reference it
        expected_side, expected_dir, expected_reverse = sides[end_side][end_dir]
        assert(start_dir == expected_dir)
        assert(start_side == expected_side)
        assert(reverse == expected_reverse)

def solve(inp):
    grid = []
    ls = []
    x, y = inp.split('\n\n')
    for line in x.splitlines():
        ls.append(line)
    width = max([len(row) for row in ls])

    # make every line the same width
    for i, l in enumerate(ls):
        if len(l) < width:
            l += " " * (width - len(l))
        grid.append(l)

    # read the directions
    ins = re.findall(r'(\d+)([LR])', y)
    ins = [(int(a), b) for a, b in ins]
    last = int(re.findall(r'(\d+)$', y)[0])
    ins.append((last, 'N'))

    # map each coordinate to a face    
    letter_grid = []
    with open('./22-letters.txt') as f:
        for line in f.read().splitlines():
            letter_grid.append(line)

    # get the minx, maxx, miny and maxy for each block
    extremes = {}
    for face in sides.keys():
        minx, maxx, miny, maxy = float('inf'), float('-inf'), float('inf'), float('-inf')
        for y in range(len(letter_grid)):
            curr_row = letter_grid[y]
            for x in range(len(curr_row)):
                if letter_grid[y][x] != face: continue
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
        extremes[face] = (minx, maxx, miny, maxy) 

    assert(all([len(x) == len(grid[0]) for x in grid]))

    row = 0
    col = grid[0].find('.')
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    dirMap = {
        0: 'R',
        1: 'D',
        2: 'L',
        3: 'U'
    }
    curr_dir = 0
    
    for amt, direction in ins:
        while amt > 0:
            dx, dy = dirs[curr_dir]
            new_x, new_y = col + dx, row + dy
            
            # part 2 logic: move to a different face on the cube
            if not (0 <= new_y < len(letter_grid) and 0 <= new_x < len(letter_grid[new_y])) or (letter_grid[row][col] != letter_grid[new_y][new_x]):
                previous_face = letter_grid[row][col]
                minx, _, miny, _ = extremes[previous_face]

                # the 'offset' is how for right or down we are in the current block
                if curr_dir in [1, 3]: # U or D
                    offset = col - minx
                else: # L or R
                    offset = row - miny
                
                new_face, new_side, reverse = sides[previous_face][dirMap[curr_dir]]
                minx, maxx, miny, maxy = extremes[new_face]

                # some edges are upside-down relative to each other
                grid_size = 49
                if reverse: offset = grid_size - offset
                
                assert(0 <= offset <= grid_size)

                # update coordinate
                prev_dir = curr_dir
                match new_side:
                    case "U":
                        new_x, new_y = minx + offset, miny
                        curr_dir = 1
                    case "D":
                        new_x, new_y = minx + offset, maxy
                        curr_dir = 3
                    case "L":
                        new_x, new_y = minx, miny + offset
                        curr_dir = 0
                    case "R":
                        new_x, new_y = maxx, miny + offset
                        curr_dir = 2
                if grid[new_y][new_x] == '#': curr_dir = prev_dir

            # part 1 logic
            # if (not (0 <= new_y < len(grid) and 0 <= new_x < len(grid[0]))) or grid[new_y][new_x] == ' ':
            #     # wrap around
            #     new_x %= len(grid[0])
            #     new_y %= len(grid)
            #     while grid[new_y][new_x] == ' ':
            #         new_x, new_y = new_x + dx, new_y + dy
            #         new_x %= len(grid[0])
            #         new_y %= len(grid) 

            if grid[new_y][new_x] == '#': break
            
            amt -= 1
            col, row = new_x, new_y

            r = list(grid[row])
            r[col] = 'x'
            grid[row] = ''.join(r)

        # change direction
        if direction == 'L':
            curr_dir -= 1
        elif direction == 'R':
            curr_dir += 1
        curr_dir %= 4

    print((1000 * (row + 1)) + (4 * (col + 1)) + curr_dir)

fname = './22-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read())

