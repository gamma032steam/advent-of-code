import math 
import functools
import re
import random
import collections

@functools.lru_cache()
def movement_cost(distance):
    return sum([y for y in range(1, distance+1)])

if __name__ == "__main__":
    with open('./input/7.txt') as f:
        data = f.read().splitlines()
        positions = list(map(int, data[0].split(",")))

        # part 1
        min_fuel = float('inf')
        for i in range(min(positions), max(positions)+1):
            min_fuel = min(min_fuel, sum([abs(i - x) for x in positions]))
        print(min_fuel)
        
        # part 2
        min_fuel = float('inf')
        for i in range(min(positions), max(positions)+1):
            min_fuel = min(min_fuel, sum([movement_cost(abs(x - i)) for x in positions]))
        print(min_fuel)
