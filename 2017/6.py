import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/6.txt') as f:
        data = f.read().split("\t")
        data = list(map(int, data))

        seen = set()
        state = data[:]
        cycles = 0

        while tuple(state) not in seen or cycles <= 12841:
            if cycles == 12841: seen = set()
            seen.add(tuple(state))
            # find min
            max_idx, max_num = -1, -1
            for i, num in enumerate(state):
                if num > max_num:
                    max_idx = i
                    max_num = num

            # distribute
            state[max_idx] = 0
            curr_idx = max_idx + 1
            while max_num > 0:
                curr_idx %= len(data)
                state[curr_idx] += 1
                curr_idx += 1
                max_num -= 1
            cycles += 1

        print(max_idx, max_num)

        print(cycles)
        print(cycles - 12841)