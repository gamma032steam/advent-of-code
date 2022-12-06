import math 
import functools
import re
import random
import collections
from helpers import *
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    k = 14
    # k = 4
    for i in range(len(inp)-k+1):
        if len(set(inp[i:i+k])) == k:
            print(i + k)
            break

try:
    fname = './6-input.txt' 
    f = open(fname)
    solve(f.read().strip())
except:
    print(f"ERROR: Could not open {fname}.")

sample="""mjqjpqmgbljsphdztnvjfqwrcgsmlb"""
if len(sample) > 0: solve(sample)
