import math 
import functools
import re
import random
from collections import defaultdict
from copy import deepcopy

def part1(vectors):
    # part 1, answer the second one but that's a guess really
    total_acc = []
    for i, vec in enumerate(vectors):
        a = vec[2]
        a = list(map(abs, a))
        p = list(map(abs, vec[0]))
        total_acc.append((sum(a), sum(p), i))
    total_acc.sort()
    print(total_acc)

def part2(vectors):
    # run a simulation, find conflicts in a set
    # dict of position, index of nodes in that position
    for t in range(1000):
        same_poses = set()
        next_vectors = deepcopy(vectors)
        conflicts = defaultdict(set)
        for i, vec in enumerate(vectors):
            if vec == "": continue
            p, v, a = vec
            p = tuple(p)

            # find the conflicts
            if len(conflicts[p]) > 0:
                same_poses.add(p)
            conflicts[tuple(p)].add(i)

            # remove conflicts
            for same in same_poses:
                for conflicting_node in conflicts[same]:
                    next_vectors[conflicting_node] = ""

        # step all the points for things not removed
        for i, vec in enumerate(next_vectors):
            # was removed
            if vec == "": continue
            p, v, a = vec
            v[0] += a[0]
            v[1] += a[1]
            v[2] += a[2]

            p[0] += v[0]
            p[1] += v[1]
            p[2] += v[2]
            next_vectors[i] = [p, v, a]
        vectors = next_vectors
    print(vectors)
    print(len([x for x in vectors if x != ""]))

if __name__ == "__main__":
    with open('./input/20.txt') as f:
        data = f.read().splitlines()

        vectors = []
        for line in data:
            spl = re.split("(, [a-z]=|[a-z]=)", line)
            p = spl[2]
            v = spl[4]
            a = spl[6]
            info = [p, v, a]
            out = []
            for element in info:
                element = element[1:-1]
                elements = element.split(",")
                elements = list(map(int, elements))
                out.append(elements)
            vectors.append(out)

        #part1(vectors)

        part2(vectors)
        
