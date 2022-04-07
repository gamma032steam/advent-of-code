import math 
import functools
import re
import random
import collections

from collections import deque

def isWall(x, y, magic):
    formula = x*x + 3*x + 2*x*y + y + y*y
    formula += magic
    bits = list(bin(formula))[2:]
    n_ones = bits.count("1")
    if n_ones % 2 == 0:
        return False
    else:
        return True

if __name__ == "__main__":
    with open('./input/13.txt') as f:
        data = f.read().splitlines()

        seen = set([(1, 1)])
        queue = deque()
        queue.append((1, 1, 0))

        while len(queue) > 0:
            x, y, cost = queue.popleft()
            #if x == 31 and y == 39:
            #    print(cost)
            #    quit()

            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in dirs:
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) in seen: continue
                if new_x < 0 or new_y < 0: continue
                if isWall(new_x, new_y, 1362): continue
                if cost + 1 > 50: continue
                queue.append((new_x, new_y, cost + 1))
                seen.add((new_x, new_y))

        print(len(seen))