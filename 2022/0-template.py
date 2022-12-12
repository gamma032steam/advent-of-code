import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    pass

fname = './input.txt' 
try:
    f = open(fname)
    solve(f.read().strip())
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")

sample="""
"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
