import math 
import functools
import re
import random
import collections

MIN_CUBE = -50
MAX_CUBE = 50

def switch(on_cubes, area, on_or_off):
    # reorder the ranges from low to high so we can easily iterate them
    for a in area: a.sort()
    # set the area within bounds
    for i in range(len(area)):
        area[i] = [max(MIN_CUBE, area[i][0]), min(MAX_CUBE, area[i][1])]
    for x in range(area[0][0], area[0][1] + 1):
        for y in range(area[1][0], area[1][1] + 1):
            for z in range(area[2][0], area[2][1] + 1):
                if on_or_off == "on":
                    on_cubes.add((x, y, z))
                else:
                    on_cubes.discard((x, y, z))  
    return on_cubes 

def create_cube(area):
    for a in area: a.sort()

    return tuple([value for coord in area for value in coord])

def does_cube_contain(big_cube, small_cube):
    x1, x2, y1, y2, z1, z2 = big_cube
    a1, a2, b1, b2, c1, c2 = small_cube
    return (
        x1 <= a1 <= a2 <= x2 and
        y1 <= b1 <= b2 <= y2 and
        z1 <= c1 <= c2 <= z2
    )

assert(does_cube_contain(
    [10, 12, 10, 12, 10, 12],
    [10, 12, 10, 11, 11, 12]
) == True)

assert(does_cube_contain(
    [0, 10, 0, 10, 0, 10],
    [0, 10, 0, 10, 0, 11]
) == False)

def get_cube_intersection(cube_1, cube_2):
    both_cubes = zip(cube_1, cube_2)

    cube_intersection = []
    for i, pair in enumerate(both_cubes):
        cube_intersection += [max(pair)] if i % 2 == 0 else [min(pair)]
        if i % 2 == 1 and cube_intersection[i] < cube_intersection[i-1]: 
            return None
    return cube_intersection

assert(get_cube_intersection(
    [10, 12, 10, 12, 10, 12],
    [10, 12, 10, 11, 11, 12]
) == [10, 12, 10, 11, 11, 12])

assert(get_cube_intersection(
    [0, 10, 0, 10, 0, 10],
    [0, 10, 0, 10, 0, 11]
) == [0, 10, 0, 10, 0, 10])

assert(get_cube_intersection(
    [0, 10, 0, 10, 0, 10],
    [0, 10, 0, 10, 11, 11]
) == None)

def substract_cube(cube, cube_to_remove):
    intersection = get_cube_intersection(cube[0], cube_to_remove[0])
    # base case: don't need to remove anything
    if intersection == None: return cube

    cube, children = cube
    for i, child in enumerate(children):
        child_intersection = get_cube_intersection(child[0], cube_to_remove[0])
        if child_intersection == None: continue
        children[i] = substract_cube(child, [child_intersection, []])

    children.append([intersection, []])
    return [cube, children]

def cube_size(cube):
    if cube == None: return 0

    x1, x2, y1, y2, z1, z2 = cube[0]
    removed = cube[1]

    size = (x2-x1+1)*(y2-y1+1)*(z2-z1+1)
    removed_sum = sum([cube_size(r) for r in removed])
    return size - removed_sum

if __name__ == "__main__":
    with open('./input/22.txt') as f:
        data = f.read().splitlines()
        ranges = [[v[2:].split("..") for v in l.split()[1].split(',')] for l in data]
        ranges = [[[int(x), int(y)] for x, y in l] for l in ranges]
        on_or_off = [v.split()[0] for v in data]
        
        # part 1
        on_cubes = set()
        for i, instruction in enumerate(on_or_off):
            # comment out for part 2, because it modifies the data in-place
            pass
            #on_cubes = switch(on_cubes, ranges[i], instruction)
        print(len(on_cubes))

        # part 2
        # list of two-tuples containing a list of cubes, and a list of areas
        # to deduct from that cube. Those deducted cubes can have deducted
        # areas themselves, and onwards recursively
        cubes = []
        for i, instruction in enumerate(on_or_off):
            if instruction == 'on':
                cube_to_add = [create_cube(ranges[i]), []]
                if cube_to_add[0] == None: continue 
                for i, cube in enumerate(cubes):
                    # deduct anything in common with other cubes
                    cubes[i] = substract_cube(cube, cube_to_add)
                cubes.append(cube_to_add)
            if instruction == 'off':
                cube_to_remove = [create_cube(ranges[i]), []]
                for i, cube in enumerate(cubes):
                    cubes[i] = substract_cube(cube, cube_to_remove)

        cubes_on = 0
        for cube in cubes:
            cubes_on += cube_size(cube)
        print(cubes_on)
