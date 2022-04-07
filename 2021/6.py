import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/6.txt') as f:
        data = f.read().splitlines()
        # make a count of each the number of fish at each age
        days_until_reproduction = collections.defaultdict(int)
        for fish in data[0].split(","):
            days_until_reproduction[int(fish)] += 1

        # part 1: set to 80, part 2: set to 256
        for day in range(256):
            day_0_fish = days_until_reproduction[0]
            # age all fish by one day
            for i in range(8):
                days_until_reproduction[i] = days_until_reproduction[i+1]
            # spawn new fish
            days_until_reproduction[6] += day_0_fish
            days_until_reproduction[8] = day_0_fish
        print(sum(days_until_reproduction.values()))
