import math 
import functools
import re
import random
import collections

from queue import PriorityQueue
from copy import deepcopy

def is_in_bounds(x, y):
    return (0 <= x <= x_size) and (0 <= y <= y_size) 

def viable_swaps(nodes):
    suggestions = [] 

    for stuff in nodes:
        x, y = stuff[0]
        used, avail = stuff[1:]
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for dx, dy in dirs:
            new_x, new_y = x + dx, y + dy
            if not is_in_bounds(new_x, new_y): continue
            to_used, to_avail = nodes[(new_x, new_y)]
            if used <= to_avail:
                suggestions.append(((x, y), (new_x, new_y)))

    return suggestions

x_size = 0
y_size = 0

if __name__ == "__main__":
    with open('./input/22.txt') as f:
        data = f.read().splitlines()

        nodes = [None] * (30 * 33)
        for line in data:
            match = re.match("/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T", line)
            if not match or len(match.groups()) != 5: continue
            x, y, size, used, avail = match.groups()
            x = int(x)
            y = int(y)
            x_size = max(x_size, x)
            y_size = max(y_size, y)
            
            nodes[30*y+x] = (int(used), int(avail))

        print(nodes[-35:])
        # find the 0
        #for used, avail:
        #    if used == 0