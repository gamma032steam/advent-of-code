import math 
import functools
import re
import random
import collections

from collections import deque
from collections import defaultdict

def num_objectives(grid):
    count = 0
    x, y = None, None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].isnumeric():
                count += 1
            if grid[i][j] == "0":
                x = i
                y = j
    return count - 1, x, y

def is_valid_pos(grid, i, j):
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])

if __name__ == "__main__":
    with open('./input/24.txt') as f:
        data = f.read().splitlines()

        goal, start_i, start_j = num_objectives(data)

        queue = deque()
        init = (0, tuple([0] * goal), start_i, start_j)
        queue.append(init)
        seen = dict()
        seen[(start_i, start_j, tuple([0] * goal))] = 0

        x = len(data)
        y = len(data[0])
        size = x * y
        max_size = 0
        found = False
        while len(queue) > 0:
            max_size = max(max_size, len(queue))
            dist, objs, i, j = queue.popleft()
            cnt = objs.count(1)
            if not found and cnt == goal:
                print(dist)
                found = True

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for di, dj in directions:
                ni = i + di
                nj = j + dj

                if not is_valid_pos(data, ni, nj): continue
                if data[ni][nj] == "#":
                    continue
                new_objs = list(objs)
                if data[ni][nj].isnumeric():
                    val = int(data[ni][nj])
                    val -= 1
                    if val == -1 and cnt == goal:
                        print(dist + 1)
                        print(max_size)
                        exit()
                    if val == -1: continue 
                    if objs[val] == 0:
                        new_objs[val] = 1
                new_objs = tuple(new_objs)

                new = (dist + 1, new_objs, ni, nj)
                state = (ni, nj, new_objs)
                
                if state in seen and seen[state]:
                    continue
                else:
                    seen[state] = dist + 1

                queue.append(new)
