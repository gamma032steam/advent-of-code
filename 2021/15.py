import math 
import functools
import re
import random
import collections
from queue import PriorityQueue

if __name__ == "__main__":
    with open('./input/15.txt') as f:
        data = f.read().splitlines()
        data = [[int(j) for j in i] for i in data]
        
        # part 1
        # dijikstra's
        cost_map = {(i, j): float('inf') for i in range(len(data)) for j in range(len(data[0]))}
        costs = PriorityQueue()

        seen = set()
        costs.put((0, (0, 0)))
        cost_map[(0, 0)] = 0

        for i in range(len(data)):
            for j in range(len(data[0])):
                costs.put((float('inf'), (i, j)))

        while True:
            cost, current = costs.get()
            seen.add(current)
            if current[0] == len(data) - 1 and current[1] == len(data[0]) - 1:
                print(cost)
                break

            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for direction in dirs:
                new_pos = (current[0] + direction[0], current[1] + direction[1])
                if not (0 <= new_pos[0] < len(data) and 0 <= new_pos[1] < len(data[0])):
                    continue

                if new_pos in seen:
                    continue

                old_cost = cost_map[new_pos]
                new_cost = data[new_pos[0]][new_pos[1]] + cost
                if new_cost < old_cost:
                    cost_map[new_pos] = new_cost
                    costs.put((new_cost, new_pos))

        # part 2
        cost_map = {(i, j): float('inf') for i in range(len(data) * 5) for j in range(len(data[0] * 5))}
        costs = PriorityQueue()

        seen = set()
        costs.put((0, (0, 0)))
        cost_map[(0, 0)] = 0

        for i in range(len(data)*5):
            for j in range(len(data[0]*5)):
                costs.put((float('inf'), (i, j)))

        while True:
            cost, current = costs.get()
            seen.add(current)
            if current[0] == len(data) * 5- 1 and current[1] == len(data[0] * 5) - 1:
                print(cost)
                break

            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for direction in dirs:
                new_pos = (current[0] + direction[0], current[1] + direction[1])
                if not (0 <= new_pos[0] < len(data) * 5 and 0 <= new_pos[1] < len(data[0]) * 5):
                    continue

                if new_pos in seen:
                    continue

                old_cost = cost_map[new_pos]
                tile_cost = (data[new_pos[0] % len(data)][new_pos[1] % len(data)] + (new_pos[0] // len(data) + new_pos[1] // len(data)))
                tile_cost = tile_cost if tile_cost <= 9 else tile_cost % 9
                new_cost = tile_cost + cost

                if new_cost < old_cost:
                    cost_map[new_pos] = new_cost
                    costs.put((new_cost, new_pos))