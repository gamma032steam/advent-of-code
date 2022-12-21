import math 
import functools
import re
import random
import collections
import helpers
import sys
import copy
sys.setrecursionlimit(100000)

def solve(inp):
    data = []
    for line in inp.splitlines():
        data.append(line.split())
        ns = {}
    while len(ns) < (len(data)):
        #print(len(ns), len(data))
        for m in data:
            if m[0] == 'root:':
                name, v1, op, v2 = m
                if v1 in ns and v2 in ns:
                    ns[name[:-1]] = f'({ns[v1]}={ns[v2]})' 
            elif m[0] == 'humn:':
                name, _ = m
                ns[name[:-1]] = 'x'
            elif len(m) == 2:
                name, num = m
                ns[name[:-1]] = num
            else:
                name, v1, op, v2 = m
                if v1 in ns and v2 in ns:
                    ns[name[:-1]] = f'({ns[v1]}{op}{ns[v2]})'

    #print(ns)
    print(ns['root'])

fname = './21-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    #solve(sample)
    print('------------')
