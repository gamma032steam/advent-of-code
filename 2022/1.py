import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input.txt') as f:
        d = f.read()
        # part 1
        print(max([sum([int(y) for y in x.split('\n')]) for x in d.split('\n\n')]))
        # part 2
        print(sum(sorted([sum([int(y) for y in x.split('\n')]) for x in d.split('\n\n')])[-3:]))
