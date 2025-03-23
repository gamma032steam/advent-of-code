# general solution for part 2

import math
import re
import helpers

sample = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

*grid, instructions = sample.splitlines()
#*grid, instructions = open('22-input.txt').read().splitlines()
grid.pop()

FACES = 6

def cube_map(grid):
    '''Compresses the grid so that each face is one #. This is needed for the cube
    folding magic.'''
    tiles = sum([len(re.findall(r'[.#]', l)) for l in grid])
    resolution = int(math.sqrt(tiles // FACES))
    res = []
    for i in range(0, len(grid), resolution):
        res.append([])
        for j in range(0, len(grid[i]), resolution):
            res[i // resolution].append('#' if grid[i][j] in '.#' else ' ')
    assert(len(helpers.find_all_nd(res, '#')) == FACES)
    return res

print(cube_map(grid))

x, y = grid[0].find('.'), 0
dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
dir = 0

def step(x, y, dir):
    dx, dy = dirs[dir]
    new_x, new_y = x + dx, y + dy
    if not 0 <= new_x < len(grid[new_y]) or not 0 <= new_y < len(grid) or grid[new_y][new_x] == ' ':
        dir = (dir - 1) % 4 # L
        new_x, new_y, dir = step(new_x, new_y, dir)
        dir = (dir + 1) % 4 # R
        new_x, new_y, dir = step(new_x, new_y, dir)
        dir = (dir - 1) % 4 # L
    
    if grid[new_y][new_x] == '#': return x, y, dir
    print(new_y, new_x)
    return new_x, new_y, dir

# for move in re.findall(r'\d+|[LR]', instructions):
#     match move:
#         case 'L':
#             dir = (dir - 1) % 4
#         case 'R':
#             dir = (dir + 1) % 4
#         case _:
#             x, y, dir = step(x, y, dir)

print(x, y)
