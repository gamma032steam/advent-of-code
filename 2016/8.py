import math 
import functools
import re
import random
import collections

x = 50
y = 6

def vis(grid):
    for line in grid:
        new = []
        for item in line:
            if item == "1":
                new.append('X')
            else:
                new.append(' ')
        text = ''.join(new)
        print(text)

if __name__ == "__main__":
    with open('./input/8.txt') as f:
        data = f.read().splitlines()

        grid = [['0'] * x] * y

        for ins in data:
            rect = re.match("rect (\d+)x(\d+)", ins)
            if rect:
                width, height = rect.groups()
                for i in range(int(height)):
                    for j in range(int(width)):
                        grid[i][j] = '1'
                continue

            row = re.match("rotate row y=(\d+) by (\d+)", ins)
            if row:
                n_row, dist = row.groups()
                n_row, dist = int(n_row), int(dist)
                new_row = [None] * x
                for i, item in enumerate(grid[n_row]):
                    new_i = (i + dist) % x
                    new_row[new_i] = item
                grid[n_row] = new_row

            col= re.match("rotate column x=(\d+) by (\d+)", ins)
            if col:
                n_col, dist = col.groups()
                n_col, dist = int(n_col), int(dist)
                new_col = [None] * y
                for i, item in enumerate([grid[i][n_col] for i in range(y)]):
                    new_i = (i + dist) % y
                    new_col[new_i] = item
                
                for i in range(y):
                    grid[i][n_col] = new_col[i]

        vis(grid)
        print(sum([x.count('1') for x in grid]))