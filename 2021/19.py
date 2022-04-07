import math 
import functools
import re
import random
import collections
import numpy

# these the the transformation matrices for a 3d object, not including reflections
# see https://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
rotations = [
    [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ],
    [
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ],
    [
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1],
    ],
    [
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0],
    ],
    [
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ],
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0]
    ],
    [
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, -1]
    ],
    [
        [0, 0, -1],
        [1, 0, 0],
        [0, -1, 0]
    ],
    [
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ],
    [
        [-1, 0, 0],
        [0, 0, -1],
        [0, -1, 0]
    ],
    [
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, -1]
    ],
    [
        [-1, 0, 0],
        [0, 0, 1],
        [0, 1, 0]
    ],
    [
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 1]
    ],
    [
        [0, 0, 1],
        [-1, 0, 0],
        [0, -1, 0]
    ],
    [
        [0, -1, 0],
        [-1, 0, 0],
        [0, 0, -1]
    ],
    [
        [0, 0, -1],
        [-1, 0, 0],
        [0, 1, 0]
    ],
    [
        [0, 0, -1],
        [0, 1, 0],
        [1, 0, 0]
    ],
    [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]
    ],
    [
        [0, 0, 1],
        [0, -1, 0],
        [1, 0, 0]
    ],
    [
        [0, -1, 0],
        [0, 0, -1],
        [1, 0, 0]
    ],
    [
        [0, 0, -1],
        [0, -1, 0],
        [-1, 0, 0]
    ],
    [
        [0, -1, 0],
        [0, 0, 1],
        [-1, 0, 0]
    ],
    [
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
    ],
    [
        [0, 1, 0],
        [0, 0, -1],
        [-1, 0, 0]
    ]
]

assert(len(rotations) == 24)

MIN_COMMON_BEACONS = 12

# from a list of scanners, figure out their positions, orientations, and rotated coordinates
def find_scanners(scanners):
    # keep track of the scanner numbers we have seen and haven't seen
    known_scanners = set([(0, 0)])
    unknown_scanners = list(range(1, len(scanners)))
    positions = [-1] * len(scanners)
    positions[0] = [0, 0, 0]
    orientations = [-1] * len(scanners)
    orientations[0] = 0

    # generate all 24 rotations for every scanner
    all_rotations = get_all_rotations(scanners)
    deltas = get_all_deltas(all_rotations)

    while len(unknown_scanners) > 0:
        # log to see status
        print(len(unknown_scanners))

        # try to match an unknown scanner with something we've seen
        unknown_scanner = unknown_scanners.pop()
        found = False
        for rotation_i, known_scanner in known_scanners:
            common = common_beacons(deltas[known_scanner][rotation_i], deltas[unknown_scanner])

            # no match
            if common == None: continue

            # find the relative position by using a single common beacon
            rotation_j, index_i, index_j = common[0]
            beacon_from_i_perspective = all_rotations[known_scanner][rotation_i][index_i]
            beacon_from_j_perspective = all_rotations[unknown_scanner][rotation_j][index_j]

            relative_position = [beacon_from_i_perspective[x] - beacon_from_j_perspective[x] for x in range(3)]

            # calculate the true position and save it
            positions[unknown_scanner] = [positions[known_scanner][x] + relative_position[x] for x in range(3)]
            orientations[unknown_scanner] = rotation_j
            
            found = True
            known_scanners.add((rotation_j, unknown_scanner))
            break
        # if we didn't find it, add it to the end and try the next unknown one. maybe next time :)
        if not found: unknown_scanners.insert(0, unknown_scanner)

    return positions, orientations, all_rotations

# figure out if scanner_2 can be rotated to match scanner_1, which is in a fixed orientation,
# already rotated to match 0. Return some info about the match.
def common_beacons(scanner_1_delta, scanner_2_deltas):
    # for every orientation pairing
    for y, scanner_2_delta in enumerate(scanner_2_deltas):
        # can we find a network of 12 common beacons?
        common_beacons = []
        for i, scanner_1_beacon in enumerate(scanner_1_delta):
            # a beacon is common if it shares a beacon with 12 common deltas
            # in the other scanner
            for j, scanner_2_beacon in enumerate(scanner_2_delta):
                common_deltas = set(scanner_1_beacon).intersection(set(scanner_2_beacon))
                if len(common_deltas) >= MIN_COMMON_BEACONS:
                    common_beacons.append((y, i, j))
        if len(common_beacons) >= MIN_COMMON_BEACONS:
            return common_beacons

    # didn't find anything
    return None

def identify_unique_beacons(positions, orientations, coords):
    beacons = set()
    for i, scanner_pos in enumerate(positions):
        # get the true positions of the beacons it sees
        for beacon in coords[i][orientations[i]]:
            beacon_pos = [beacon[x] + scanner_pos[x] for x in range(3)]
            beacons.add(tuple(beacon_pos))
    return beacons

# get the distance from one coordinate to every other coordinate
def get_deltas(coordinates):
    deltas = []
    # for every coordinate...
    for i in range(len(coordinates)):
        delta_to_i = []
        # calculate it's delta with every other coordinate (incl. itself)
        for j in range(len(coordinates)):
            delta_x = coordinates[j][0] - coordinates[i][0]
            delta_y = coordinates[i][1] - coordinates[j][1]
            delta_z = coordinates[i][2] - coordinates[j][2]
            delta_to_i.append((delta_x, delta_y, delta_z))
        deltas.append(delta_to_i)
    return deltas

def largest_manhattan_distance(beacons):
    max_dist = 0

    for beacon_1 in beacons:
        for beacon_2 in beacons:
            max_dist = max(max_dist, manhattan_distance(beacon_1, beacon_2))

    return max_dist

def get_all_deltas(all_rotations):
    return [[get_deltas(rotated_coordinates) for rotated_coordinates in scanner] for scanner in all_rotations]

def get_all_rotations(scanners):
    return [[rotate_coordinates(scanner, rotation) for rotation in rotations] for scanner in scanners] 

def rotate_coordinates(coordinates, rotation_matrix):
    return [numpy.dot(rotation_matrix, numpy.array(coord).transpose()) for coord in coordinates]

def manhattan_distance(point_1, point_2):
    return sum([abs(point_1[i] - point_2[i]) for i in range(3)])

if __name__ == "__main__":
    with open('./input/19.txt') as f:
        # read in data, convert into integer coordinates
        data = f.read().split('\n\n')
        scanners = [scanner.split('\n')[1:] for scanner in data]
        get_coordinates = lambda x: [list(map(int, v.split(','))) for v in x]
        scanners = list(map(get_coordinates, scanners))
        
        # part 1
        positions, orientations, rotated_coords = find_scanners(scanners)
        beacons = identify_unique_beacons(positions, orientations, rotated_coords)
        print(len(beacons))

        # part 2
        print(largest_manhattan_distance(positions))
