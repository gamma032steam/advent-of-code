import math 
import functools
import re
import random
import collections

def find_lit_squares(input):
    lit = set()
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == '#':
                lit.add((j, i))
    return lit

def enhance(x, y, enhancement_string, lit, previous_bounds, default):
    min_x, max_x, min_y, max_y = previous_bounds
    dirs = [[-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
    bin_num = ""
    for direction in dirs:
        adj_pos = (x + direction[0], y + direction[1])
        if adj_pos in lit: bin_num += "1"
        elif min_x <= adj_pos[0] <= max_x and min_y <= adj_pos[1] <= max_y: bin_num += "0"
        else: bin_num += default
    bin_num = int(bin_num, 2)
    return enhancement_string[bin_num]

def update(enhancement_string, lit, current_bounds, previous_bounds, default):
    newly_lit = set()
    min_x, max_x, min_y, max_y = current_bounds

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            new_tile = enhance(x, y, enhancement_string, lit, previous_bounds, default)
            if new_tile == '#': newly_lit.add((x, y))

    return newly_lit

def get_bounds(lit):
    min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')
    for x, y in lit:
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)
    return min_x - 1, max_x + 1, min_y - 1, max_y + 1

def visualise(lit, default):
    min_x, max_x, min_y, max_y = get_bounds(lit)
    for y in range(min_y, max_y+1):
        line = ""
        for x in range(min_x, max_x+1):
            if (y, x) in lit: line += '#'
            elif x == min_x or x == max_x or y == min_y or y == max_y: line += default
            else: line += '.'
        print(line)

if __name__ == "__main__":
    with open('./input/20.txt') as f:
        enhancement_string, input_img = data = f.read().split('\n\n')
        input_img = input_img.split('\n')

        # part 1
        # first enhancement
        initially_lit = find_lit_squares(input_img)
        visualise(initially_lit, ".")

        initial_bounds = get_bounds(initially_lit)
        newly_lit = update(enhancement_string, initially_lit, initial_bounds, get_bounds(set()), "0")
        visualise(newly_lit, "#")

        # second enhancement
        finally_lit = update(enhancement_string, newly_lit, get_bounds(newly_lit), initial_bounds, "0")
        visualise(finally_lit, ".")

        print(len(finally_lit))

        # part 2
        print("Part 2: ")
        currently_lit = initially_lit
        current_bounds = get_bounds(initially_lit)
        previous_bound = get_bounds(set())
        visualise(currently_lit, ".")
        for i in range(50):
            default = "0" if i % 2 == 0 else "1"
            currently_lit = update(enhancement_string, currently_lit, current_bounds, previous_bound, default)
            previous_bound = current_bounds
            current_bounds = get_bounds(currently_lit)
            visualise(currently_lit, "#" if i % 2 == 0 else ".")

        print(len(currently_lit))
