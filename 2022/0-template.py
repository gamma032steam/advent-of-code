import math 
import functools
import re
import random
import collections
from helpers import *
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    pass

try:
    fname = './input.txt' 
    f = open(fname)
    solve(f.read().strip())
except:
    print(f"ERROR: Could not open {fname}.")

sample=""""""
if len(sample) > 0: solve(sample)
