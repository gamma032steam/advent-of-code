import math 
import functools
import re
import random

from collections import defaultdict

def dfs(graph, node):
    # dfs from 0
    seen = set()
    stack = [node]
    while stack:
        curr = stack.pop()
        seen.add(curr)
        for n in graph[curr]:
            if n in seen: continue
            stack.append(n)
    return seen

if __name__ == "__main__":
    with open('./input/12.txt') as f:
        data = f.read().splitlines()

        graph = defaultdict(list)
        for line in data:
            node, nei = line.split(" <-> ")
            neis = nei.split(", ")
            for n in neis:
                graph[node].append(n)
                graph[n].append(node)

        seen = set()
        groups = 0
        for node in graph:
            if node not in seen:
                seen = seen.union(dfs(graph, node))
                groups += 1
        print(groups)