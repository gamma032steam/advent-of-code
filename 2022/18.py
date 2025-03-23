import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    cubes = set()
    for line in inp.splitlines():
        cubes.add(tuple(helpers.ints(line)))

    # part 1
    faces = 0
    air_faces = []
    for cube in cubes:
        for i in range(3):
            for delta in [-1, 1]:
                moved_cube = list(cube)
                moved_cube[i] += delta
                if tuple(moved_cube) not in cubes:
                    air_faces.append(tuple(moved_cube))
                    faces += 1

    print(faces)
    minx, miny, minz = [min([c[i] for c in cubes]) for i in range(3)]
    maxx, maxy, maxz = [max([c[i] for c in cubes]) for i in range(3)]
    
    # dfs for air pockets
    seen = set()
    air_pockets = []
    def dfs(root, pockets):
        stack = [root]
        seen_in_search = [root]
        found_edge = False # check if we hit outside the cube
        while stack:
            coord = stack.pop()
            for i in range(3):
                for delta in [-1, 1]:
                    nei = list(coord)
                    nei[i] += delta
                    nx, ny, nz = nei
                    nei = tuple(nei)
                    if not (minx <= nx <= maxx and miny <= ny <= maxy and minz <= nz <= maxz):
                        found_edge = True
                        continue
                    if nei in cubes:
                        continue
                    if nei in seen: continue
                    stack.append(nei)
                    seen_in_search.append(nei)
                    seen.add(nei)


        if not found_edge: pockets += seen_in_search

    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            for z in range(minz, maxz + 1):
                if (x, y, z) not in seen and (x, y, z) not in cubes:
                    dfs((x, y, z), air_pockets)
    
    for coord in air_pockets:
        air_faces = [x for x in air_faces if x != coord]
    print(len(air_faces))

fname = './18-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
