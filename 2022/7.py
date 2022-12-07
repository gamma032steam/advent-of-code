import math 
import functools
import re
import random
import collections
from helpers import *
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    graph = collections.defaultdict(list)
    parent = {}
    curr = ''

    for line in inp.splitlines():
        if line.startswith('$'):
            cmd = line.split()
            if cmd[1] == 'cd' and cmd[2] == '..':
                curr = parent[curr]
            elif cmd[1] == 'cd':
                graph[curr].append(curr + cmd[2])
                new_path = curr + cmd[2]
                parent[new_path] = curr
                curr = new_path
        else:
            size, _ = line.split()
            if size != 'dir': graph[curr].append(int(size))

    max_size = 100000
    tot = 0

    def get_size(root):
        size = 0
        stack = [root]
        while stack:
            c = stack.pop()
            for file in graph[c]:
                if isinstance(file, int):
                    size += file
                else:
                    stack.append(file)
        return size

    for u in graph:
        size = get_size(u)
        if size <= max_size: 
            tot += size

    print(tot)

    needed = 30000000 - (70000000 - get_size('/'))
    best = float('inf')
    for u in graph:
        size = get_size(u)
        if size >= needed and size < best:
            best = size
    print(best)

try:
    fname = './7-input.txt' 
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
if True: solve(f.read().strip())

sample="""$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
