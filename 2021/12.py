import math 
import functools
import re
import random
import collections

# Finished in 477th place

if __name__ == "__main__":
    with open('./input/12.txt') as f:
        data = f.read().splitlines()

        paths = collections.defaultdict(list)

        for line in data:
            start, end = line.split('-')
            paths[start].append(end)
            paths[end].append(start)
        num_paths = 0
        stack = [('start', set(['start']))]

        while stack:
            node, seen = stack.pop()
            for end in paths[node]:
                if end == 'end':
                    num_paths += 1
                    continue
                if end not in seen:
                    new_set = seen.copy()
                    if end.lower() == end:
                        new_set.add(end)
                    stack.append((end, new_set))
        print(num_paths)
        
        num_paths = 0
        stack = [('start', set(['start']), False)]



        while stack:
            node, seen, used = stack.pop()
            for end in paths[node]:
                if end == 'end':
                    num_paths += 1
                    continue
                if end not in seen:
                    new_set = seen.copy()
                    if end.lower() == end:
                        new_set.add(end)
                    stack.append((end, new_set, used))
                elif not used and end != 'start' and end != 'end':
                    new_set = seen.copy()
                    if end.lower() == end:
                        new_set.add(end)
                    stack.append((end, new_set, True))
        print(num_paths) 


