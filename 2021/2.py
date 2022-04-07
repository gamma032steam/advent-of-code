import math 
import functools
import re
import random
import collections

def solve1(data):
    depth = forward = 0
    for direction, amount in data:
        amount = int(amount)
        if direction == 'forward': forward += amount
        if direction == 'down': depth += amount
        if direction == 'up': depth -= amount
    print(depth * forward)

def solve2(data):
    aim = forward = depth = 0
    for direction, amount in data:
        amount = int(amount)
        if direction == 'forward': 
            forward += amount
            depth += aim * amount
        if direction == 'down': aim += amount
        if direction == 'up': aim -= amount
    print(depth * forward)


if __name__ == "__main__":
    with open('./input/2.txt') as f:
        data = [i.split(" ") for i in f.read().splitlines()]
        solve1(data)
        solve2(data)