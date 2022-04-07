import math
import functools
import re
import random
import operator

def nTrees(trees):
    xPos = yPos = 0
    rStep, dStep = 3, 1
    treeCount = 0
    while yPos < len(trees):
        if trees[yPos][xPos] == '#':
            treeCount += 1
        xPos = (xPos + rStep) % len(trees[0])
        yPos += dStep
    print(treeCount)

def nTreesSimple(trees, xStep, yStep):
    return len([x for i, x in enumerate(range(0, len(trees), yStep)) if trees[x][i*xStep % len(trees[0])] == '#'])

def allSlopes(trees):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    print(reduce(operator.mul, [nTreesSimple(trees, xStep, yStep) for xStep, yStep in slopes], 1))

if __name__ == "__main__":
    with open('./input/3-input.txt') as f:
        data = f.read().splitlines()
        nTreesSimple(data, 3, 1)
        allSlopes(data)