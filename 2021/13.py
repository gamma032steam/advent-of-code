import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/13.txt') as f:
        data = f.read()
        coords, folds = data.split("\n\n")

        visible = set()
        for coord in coords.split("\n"):
            x, y = coord.split(",")
            visible.add((int(x), int(y)))

        fold_data = []
        for fold in folds.split("\n"):
            direction, pos = fold.split("=") 
            fold_data.append((direction[-1], int(pos)))

        # part 1
        for i, (direction, pos) in enumerate(fold_data):
            if (i == 1): print(len(visible))
            new_set = set(visible)

            for x, y in visible:
                if direction == 'y' and y > pos:
                    new_set.add((x, pos - (y - pos)))
                    new_set.remove((x, y))
                elif direction == 'x' and x > pos:
                    new_set.add((pos - (x - pos), y))
                    new_set.remove((x, y))
            visible = new_set

        # part 2
        size_x, size_y = max([x for x, _ in visible]), max([y for _, y in visible])
        for i in range(size_y + 1):
            line = ""
            for j in range(size_x + 1):
                line += "#" if (j, i) in visible else ' '
            print(line)
