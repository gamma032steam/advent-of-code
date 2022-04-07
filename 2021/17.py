import math
import functools
import re
import random
import collections


def find_highest_point(y):
    curr_pos = 0
    vel = y
    while vel > 0:
        curr_pos += vel
        vel -= 1
    return curr_pos


if __name__ == "__main__":
    with open("./input/17.txt") as f:
        data = f.read().split(" ")
        lo_x, hi_x = [int(x) for x in data[2][2:-1].split("..")]
        lo_y, hi_y = [int(y) for y in data[3][2:].split("..")]

        # part 1
        y_range_lo = 0 if lo_y > 0 else lo_y
        y_range_hi = abs(lo_y) if hi_y < 0 else hi_y

        valid_y = collections.defaultdict(list)
        for y in range(y_range_lo, y_range_hi + 1):
            current_position = 0
            n = 0
            while current_position >= lo_y:
                if lo_y <= current_position <= hi_y:
                    valid_y[n].append(y)
                current_position += y - n
                n += 1

        max_steps = max(valid_y.keys())

        x_range_lo = 0 if lo_x > 0 else lo_x
        x_range_hi = 0 if hi_x < 0 else hi_x

        valid_x = collections.defaultdict(list)
        for x in range(x_range_lo, x_range_hi + 1):
            current_position = 0
            for n in range(0, max_steps + 2):
                if lo_x <= current_position <= hi_x:
                    valid_x[n].append(x)
                current_position += max(x - n, 0)

        solutions = []
        for n, x_list in valid_x.items():
            for x in x_list:
                for y in valid_y[n]:
                    solutions.append((x, y))

        coolest_shot = max(solutions, key=lambda x: x[1])
        print(find_highest_point(coolest_shot[1]))
        print(len(set(solutions)))
