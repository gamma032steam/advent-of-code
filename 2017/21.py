import math
import functools
import re
import random
import collections

import numpy


def rotate(m):
    return numpy.rot90(m)


def flipy(m):
    return numpy.flip(m, axis=0)


def flipx(m):
    return numpy.flip(m, axis=1)


if __name__ == "__main__":
    with open("./input/17.txt") as f:
        data = f.read().splitlines()

        init = [".#.", "..#", "###"]

        init = [list(x) for x in init]

        data = [[list(map(list, y.split("/"))) for y in x.split(" => ")] for x in data]

        # print(data)

        for i in range(2):

            if len(init) % 3 == 0:
                # divisible byf 3

                # split into submatrices
                subms = []
                for a in range(0, len(init), 3):
                    for b in range(0, len(init), 3):
                        new_m = [x[b : b + 3] for x in init[a : a + 3]]
                        subms.append(new_m)

                new_subms = []
                for m in subms:
                    # try every rule
                    for input, output in data:
                        if numpy.array_equal(input, m):
                            new_subms.append(output)
                            break

                        # try rotations to match
                        for i in range(3):
                            rot = rotate(m)
                            if numpy.array_equal(input, rot):
                                new_subms.append(output)
                                break

                        # try flips to match
                        xflip = flipx(m)
                        if numpy.array_equal(input, xflip):
                            new_subms.append(output)
                            break
                        yflip = flipy(m)
                        if numpy.array_equal(input, yflip):
                            new_subms.append(output)
                            break
                # print(new_subms)

                combined_matrix = None

                for a in range(0, len(new_subms), 3):
                    row = new_subms[a]
                    for b in range(1, len(new_subms), 3):
                        numpy.concatenate((row, new_subms[a + b]), axis=1)

                    if a == 0:
                        combined_matrix = row
                    else:
                        numpy.concatenate((combined_matrix, row), axis=0)
                print(combined_matrix)

                init = combined_matrix
            else:
                # divisible by 2
                # split into submatrices
                subms = []
                for a in range(0, len(init), 2):
                    for b in range(0, len(init), 2):
                        new_m = [x[b : b + 2] for x in init[a : a + 2]]
                        subms.append(new_m)

                new_subms = []
                for m in subms:
                    # try every rule
                    for input, output in data:
                        if numpy.array_equal(input, m):
                            new_subms.append(output)
                            break

                        # try rotations to match
                        for i in range(3):
                            rot = rotate(m)
                            if numpy.array_equal(input, rot):
                                new_subms.append(output)
                                break

                        # try flips to match
                        xflip = flipx(m)
                        if numpy.array_equal(input, xflip):
                            new_subms.append(output)
                            break
                        yflip = flipy(m)
                        if numpy.array_equal(input, yflip):
                            new_subms.append(output)
                            break

                combined_matrix = None
                for a in range(0, len(init), 2):
                    row = new_subms[a]
                    for b in range(0, len(init), 2):
                        numpy.concatenate((row, new_subms[a + b]), axis=1)
                    print(row)
                    if a == 0:
                        combined_matrix = row
                    else:
                        numpy.concatenate((combined_matrix, row), axis=0)

                print(combined_matrix)
