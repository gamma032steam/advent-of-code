import math 
import functools
import re
import random
import collections

a = {
    "X": ['C', 'A', 'B'],
    "Y": ['A', 'B', 'C'],
    "Z": ['B', 'C', 'A']
}

b = {
    "A": ['Z', 'X', 'Y'],
    "B": ['X', 'Y', 'Z'],
    "C": ['Y', 'Z', 'X']
}

if __name__ == "__main__":
    with open('./2-input.txt') as f:
        data = f.read().splitlines()
        s = 0
        for l in data:
            x, y = l.split(" ")
            n = a[y].index(x)
            if n == 0:
                s += 6
            if n == 1:
                s += 3
            if y == "X":
                s += 1
            if y == "Y":
                s += 2
            if y == "Z":
                s += 3
        print(s)

        s = 0
        for l in data:
            x, y = l.split(" ")
            if y == "X":
                g = 0
            if y == "Y":
                g = 1
                s += 3
            if y == "Z":
                g = 2
                s += 6
            y = b[x][g]
            if y == "X":
                s += 1
            if y == "Y":
                s += 2
            if y == "Z":
                s += 3
        print(s)
