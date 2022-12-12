import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

Monkey = collections.namedtuple("Monkey", "items op test true_throw false_throw")

def solve(inp):
    inp = [x.splitlines() for x in inp.split('\n\n')]
    monkeys = []
    for m in inp:
        items = helpers.ints(m[1])
        op = m[2].split()[-2:]
        if op[1].isnumeric(): op[1] = int(op[1])
        test = helpers.ints(m[3])[0]
        true_throw = helpers.ints(m[4])[0]
        false_throw = helpers.ints(m[5])[0]
        monkeys.append(Monkey(items, op, test, true_throw, false_throw))

    tally = [0] * len(monkeys)
    lcm = math.lcm(*[m.test for m in monkeys])
    for _ in range(10000):
        for i, m in enumerate(monkeys):
            while m.items:
                worry = m.items.pop(0)
                worry = helpers.ops[m.op[0]](worry, worry if m.op[1] == 'old' else m.op[1])
                #worry //= 3
                new_monkey = m.true_throw if worry % m.test == 0 else m.false_throw
                worry %= lcm
                monkeys[new_monkey].items.append(worry)
                tally[i] += 1

    top_monkeys = sorted(tally)[-2:]
    print(top_monkeys[0] * top_monkeys[1])

fname = './11-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
