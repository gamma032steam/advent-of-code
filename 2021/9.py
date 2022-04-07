import math 
import functools
import re
import random
import collections

def is_low_point(row, col, grid):
    if ((row + 1 >= len(grid) or grid[row+1][col] > grid[row][col]) and
        (row - 1 < 0 or grid[row+-1][col] > grid[row][col]) and 
        (col + 1 >= len(grid[0]) or grid[row][col+1] > grid[row][col]) and
        (col - 1 < 0 or grid[row][col-1] > grid[row][col])):
        return True
    return False

def find_basin(row, col, grid):
    stack = [(row, col)]
    seen = set(stack)
    while len(stack) > 0:
        current = stack.pop()
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for direction in dirs:
            new_pos = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= new_pos[0] < len(grid)) and (0 <= new_pos[1] < len(grid[0])):
                if grid[new_pos[0]][new_pos[1]] != '9' and new_pos not in seen:
                    seen.add(new_pos)
                    stack.append(new_pos)
    return seen

if __name__ == "__main__":
    with open('./input/9.txt') as f:
        data = f.read().splitlines()

        # part 1
        low_points = [(i, j) for i in range(len(data)) for j in range(len(data[0])) if is_low_point(i, j, data)]
        risk_level = sum([int(data[i][j]) + 1 for i, j in low_points])
        print(risk_level)
        
        # part 2
        all_seen = set()
        basin_sizes = []
        for low_point_i, low_point_j in low_points:
            if (low_point_i, low_point_j) in all_seen: continue
            basin = find_basin(low_point_i, low_point_j, data)
            all_seen = all_seen.union(basin)
            basin_sizes.append(len(basin))
        basin_sizes.sort()
        basin_sizes = basin_sizes[-3:]
        print(functools.reduce(lambda x, y: x * y, basin_sizes))
