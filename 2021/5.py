import math 
import functools
import re
import random
import collections

def generate_straight_lines(c1, c2):
    axis = 0
    if c1[0] == c2[0]: axis = 0
    elif c1[1] == c2[1]: axis = 1
    else: return []
    coords = []
    if axis == 0:
        start, end = (c1[1], c2[1]) if c1[1] < c2[1] else (c2[1], c1[1])
        for i in range(start, end+1):
            coords.append((c1[0], i))
    if axis == 1:
        start, end = (c1[0], c2[0]) if c1[0] < c2[0] else (c2[0], c1[0])
        for i in range(start, end+1):
            coords.append((i, c1[1]))
    return coords

def generate_all_lines(c1, c2):
    if c1[0] == c2[0] or c1[1] == c2[1]: return generate_straight_lines(c1, c2)
    coords = []
    x_start, x_end, y_coord = (c1[0], c2[0], c1[1]) if c1[0] < c2[0] else (c2[0], c1[0], c2[1])
    y_dir = 1 if y_coord < c1[1] or y_coord < c2[1] else -1
    for x in range(x_start, x_end+1):
        coords.append((x, y_coord))
        y_coord += y_dir
    return coords


if __name__ == "__main__":
    with open('./input/5.txt') as f:
        data = f.read().splitlines()
        lines = list(map(lambda x: list(map(lambda y: [int(y.split(",")[0]), int(y.split(',')[1])], x.split(" -> "))), data))
        # part 1
        points_with_lines = [item for sublist in list(map(lambda x: generate_straight_lines(x[0], x[1]), lines)) for item in sublist]
        print(len([x for x, count in collections.Counter(points_with_lines).items() if count > 1]))
        # part 2
        points_with_lines = [item for sublist in list(map(lambda x: generate_all_lines(x[0], x[1]), lines)) for item in sublist]
        print(len([x for x, count in collections.Counter(points_with_lines).items() if count > 1]))
