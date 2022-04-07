import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/5.txt') as f:
        data = f.read().splitlines()
        data = list(map(int, data))

        pos = 0
        steps = 0
        while pos >= 0 and pos < len(data):
            dist = data[pos]
            oldpos = pos
            pos += dist
            if data[oldpos] >= 3:
                data[oldpos] -= 1
            else:
                data[oldpos] += 1
            steps += 1
        
        print(steps)
        