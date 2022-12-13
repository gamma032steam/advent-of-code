import math 
import functools
import re
import random
import collections
import helpers
import sys
import ast
import copy
sys.setrecursionlimit(100000)

def solve(inp):
    pairs = []
    lines = []
    for p in inp.split('\n\n'):
        line1, line2 = [ast.literal_eval(x) for x in p.splitlines()]
        pairs.append((line1, line2))
        lines.extend([line1, line2])
    
    def correct_order(e1, e2):
        if isinstance(e1, list) and isinstance(e2, int):
            e2 = [e2]
        if isinstance(e2, list) and isinstance(e1, int):
            e1 = [e1]

        if isinstance(e1, list):
            # compare 2 lists
            while e1 and e2:
                e1, e2 = copy.deepcopy(e1), copy.deepcopy(e2)
                x1, x2 = e1.pop(0), e2.pop(0)
                correct = correct_order(x1, x2)
                if correct is not None: return correct

            if len(e1) == 0 and len(e2) == 0: return None
            return not e1
             
        else:
            # compare 2 ints
            if e1 == e2: return None
            return e1 < e2

    def order_sort(e1, e2):
        correct = correct_order(e1, e2)
        match correct:
            case None:
                return 0
            case True:
                return -1
            case False:
                return 1


    tot = 0
    for i, pair in enumerate(pairs):
        result = correct_order(pair[0], pair[1])
        assert(result != None)
        if result: tot += i + 1

    print(tot)
    lines.append([[2]])
    lines.append([[6]])
    lines = sorted(lines, key=functools.cmp_to_key(order_sort))
    k1 = lines.index([[2]]) + 1
    k2 = lines.index([[6]]) + 1
    print(k1 * k2)

fname = './13-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
