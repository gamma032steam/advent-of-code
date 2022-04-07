import math 
import functools
import re
import random
import string

def solve1(data):
    # Get each group
    groups = data.split('\n\n')
    # Concat strings
    groups = [''.join(x.split('\n')) for x in groups]
    cnt = 0
    for g in groups:
        # check if a-z is in string
        cnt += len([x for x in string.ascii_lowercase if x in g])
    print(cnt)

def solve2(data):
    # Get each group
    groups = data.split('\n\n')
    groups = [x.split('\n') for x in groups]

    # Concat strings
    cnt = 0
    for g in groups:
        # check if a-z is in all people's declaration
        cnt += len([x for x in string.ascii_lowercase if all([x in d for d in g])])
    print(cnt)

if __name__ == "__main__":
    with open('./input/6-input.txt') as f:
        data = f.read()
        solve2(data)