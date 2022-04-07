import math 
import functools
import re
import random
import collections

from collections import defaultdict

from functools import lru_cache

if __name__ == "__main__":
    with open('./input/13.txt') as f:
        data = f.read().splitlines()

        nodes = set()
        edges = defaultdict(int)
        for line in data:
            words = line.split()
            words[10] = words[10][:-1]
            if words[2] == "gain":
                edges[frozenset([words[0], words[10]])] += int(words[3])
            else:
                edges[frozenset([words[0], words[10]])] -= int(words[3])

            nodes.add(words[0])
            nodes.add(words[10])

        #add yourself
        for guest in nodes:
            edges[frozenset([guest, "me"])] = 0
        nodes.add("me")

        # dfs
        seen = dict()
        stack = []
        for person in nodes:
            copy = set(nodes)
            copy.remove(person)
            stack.append((person, person, 0, frozenset([person]), frozenset(copy)))

        best = float('-inf')
        while stack:
            first, p, dist, used, remaining = stack.pop()

            if len(remaining) == 0:
                dist += edges[frozenset([p, first])]
                best = max(dist, best)
                continue

            for nei in remaining:
                new_cost = dist + edges[frozenset([nei, p])]
                new_used = set(used)
                new_used.add(nei)
                new_used = frozenset(new_used)

                new_rem = set(remaining)
                new_rem.remove(nei)
                new_rem = frozenset(new_rem)

                state = (first, nei, new_cost, new_used, new_rem)
                if state in seen and seen[state] <= new_cost: continue
                stack.append(state)

        print(best)


