from collections import defaultdict
from itertools import permutations

from numpy import short

if __name__ == "__main__":
    with open('./input/9.txt') as f:
        data = f.read().splitlines()

        distances = defaultdict(dict)
        nodes = set()
        for line in data:
            words = line.split()
            origin, destination, distance = words[0], words[2], int(words[4])
            distances[origin][destination] = distance
            distances[destination][origin] = distance
            nodes.add(origin)
            nodes.add(destination)

        shortest = float('inf')
        longest = float('-inf')
        for path in permutations(nodes):
            cost = 0
            for i in range(len(path) - 1):
                if path[i+1] not in distances[path[i]]: break
                cost += distances[path[i]][path[i+1]]

            if cost != 0: 
                shortest = min(shortest, cost)
                longest = max(longest, cost)

        print(shortest)
        print(longest)
