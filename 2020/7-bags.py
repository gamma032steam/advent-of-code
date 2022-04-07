import math 
import functools
import re
import random
import collections

def solve1(data):
    graph = form_graph(data)
    cnt = 0
    for bag, children in graph.items():
        # run a DFS
        curr = list(map(lambda x: x[1], children))

        while len(curr) > 0:
            b = curr.pop()

            # see golden bag
            if b == "shiny gold":
                cnt += 1
                break

            # add new bags
            for _, new_bag in graph[b]:
                curr.append(new_bag)

    print(cnt)

def solve2(data):
    graph = form_graph(data)
    total_bags = 0
    curr = graph['shiny gold']
    
    while len(curr) > 0:
        b = curr.pop()
        # add bag amount
        total_bags += int(b[0])

        # add new bags
        for quantity, name in graph[b[1]]:
            curr.append((int(quantity) * int(b[0]), name))            

    print(total_bags)

# Convert input into an adjacency list graph
def form_graph(data):
    graph = {}
    for line in data:
        match = re.match('^(.*) bags contain (.*)$', line)
        # Name of this bag
        name = match.group(1)
        # Search the list for bags, extract (quantity, colour) tuples
        children = re.findall('(\d+) (\D*) bags?[.,]', match.group(2))
        graph[name] = children
    return graph

if __name__ == "__main__":
    with open('./input/7-input.txt') as f:
        data = f.read().splitlines()
        solve1(data)
        solve2(data)