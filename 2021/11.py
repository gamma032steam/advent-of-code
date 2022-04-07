import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/11.txt') as f:
        data = [[int(energy) for energy in line] for line in f.read().splitlines()]

        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        size = len(data) * len(data[0])
        # part 1 and 2
        num_flashed = 0
        steps = 0
        while True:
            num_flashed_this_cycle = 0
            # increment everything by 1
            data = [[energy + 1 for energy in line] for line in data]
            # calculate flashes
            octopuses_to_flash = [(i, j) for i in range(len(data)) for j in range(len(data[0])) if data[i][j] > 9]
            octopuses_flashed = []
            while octopuses_to_flash:
                octo_i, octo_j = octopuses_to_flash.pop()
                octopuses_flashed.append((octo_i, octo_j))
                num_flashed_this_cycle += 1

                # add 1 to the energy level of everything adjacent
                for delta_i, delta_j in dirs:
                    new_i, new_j = octo_i + delta_i, octo_j + delta_j
                    if not ((0 <= new_i < len(data)) and (0 <= new_j < len(data[0]))):
                        continue
                    data[new_i][new_j] += 1
                    if data[new_i][new_j] == 10:
                        octopuses_to_flash.append((new_i, new_j))
            # set everything that flashed to 0
            for i, j in octopuses_flashed:
                data[i][j] = 0
            steps += 1
            num_flashed += num_flashed_this_cycle
            if (num_flashed_this_cycle == size):
                print(steps)
                break
            if (steps == 100): print(num_flashed)
        print(num_flashed)
