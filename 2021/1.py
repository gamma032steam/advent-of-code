import math 
from functools import reduce
import re
import random
import collections

if __name__ == "__main__":  
    with open('./input/1.txt') as f:
        data = list(map(int, f.read().splitlines()))
        print(sum(map(lambda x, y: int(y > x), data, data[1:])))
        print(reduce((lambda w, next: (w[0] + int(next > w[1]), w[2], w[3], next)), data[3:], (0, data[0], data[1], data[2]))[0])