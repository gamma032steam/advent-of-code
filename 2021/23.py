import math 
import functools
import re
import random
import collections
from queue import PriorityQueue

CORRECT_BOARD = [['.'] * 11, ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D'], None]
BIG_CORRECT_BOARD = [['.'] * 11, ['A'] * 4 + ['B'] * 4 + ['C'] * 4 + ['D'] * 4, None]

MOVEMENT_COST = dict({
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
})

POD_ROOMS = dict({
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3
})

INVALID_HALLWAY_POSITIONS = set([2, 4, 6, 8])


def solve(initial_board):
    # run a modified dijikstra's
    seen_positions = dict()
    queue = PriorityQueue()
    queue.put((initial_board[2], initial_board))
    best = float('inf')

    while not queue.empty():
        _, curr = queue.get()
        if best != float('inf'):
            if curr[2] > best:
                continue

        if is_board_complete(curr):
            best = min(best, curr[2])
        for board in find_next_moves(curr):
            hashable_board = (tuple(board[0]), tuple(board[1]))
            if hashable_board not in seen_positions:
                seen_positions[hashable_board] = board[2]
                queue.put((board[2], board))
            if board[2] < seen_positions[hashable_board]:
                queue.put((board[2], board))
    return best

def read_initial_board(raw_lines, big=False):
    # hallway is initially empty, rooms are full. But this can read any input.
    hallways = list(raw_lines[1][1:-1])
    assert(len(hallways) == 11)

    rows_of_rooms = []
    for i in range(2, 4 if big == False else 6):
        rows_of_rooms.append([pod for pod in raw_lines[i] if pod not in ['#', ' ']])

    rooms = []
    for i in range(4):
        for room in rows_of_rooms:
            rooms.append(room[i])
    
    assert(len(find_pods([hallways, rooms, 0])) == (8 if big == False else 16))
    return [hallways, rooms, 0]

def visualise_board(board, big=True):
    print("#############")
    print("#" + ''.join(['.' if x == "." else x for x in board[0]]) + "#")
    size = 2 if big == False else 4
    print("###" + ''.join(['.#' if x == "." else x + "#" for i, x in enumerate(board[1]) if i % size == 0]) + "##")
    for j in range(1, size):
        print("  #" + ''.join(['.#' if x == "." else x + "#" for i, x in enumerate(board[1]) if i % size == j]))
    print("  #########  ")

def find_pods(board):
    pod_positions = []
    for i, hallway_pos in enumerate(board[0]):
        if hallway_pos.isalpha(): pod_positions.append((i, None))
    
    for i, room_pos in enumerate(board[1]):
        if room_pos.isalpha(): pod_positions.append((None, i))

    return pod_positions

def find_valid_hallway_positions(board, i):
    # convert room position into x-coordinate
    room_no = get_room_no(i, board)
    x_pos = get_xpos_of_room(room_no)
    assert(x_pos in INVALID_HALLWAY_POSITIONS)

    # search for hallway positions we can reach
    valid_positions = []
    for i in range(x_pos, -1, -1):
        if i in INVALID_HALLWAY_POSITIONS: continue
        # ran into a pod
        if board[0][i].isalpha(): break
        distance = abs(i - x_pos)
        valid_positions.append((i, distance))

    for i in range(x_pos, len(board[0])):
        if i in INVALID_HALLWAY_POSITIONS: continue
        # ran into a pod
        if board[0][i].isalpha(): break
        distance = abs(i - x_pos)
        valid_positions.append((i, distance))

    return valid_positions

def find_next_moves(board):
    possible_moves = []
    for pod in find_pods(board):
        if pod[0] != None:
            # pod in the hallway. The only moves are to go into a room.

            pod_type = board[0][pod[0]]
            assert(pod_type.isalpha())
            room_no = POD_ROOMS[pod_type]
            assert(0 <= room_no <= 3)
            room_distance = get_room_distance(board, room_no, pod[0])
            
            # path blocked
            if room_distance == -1: continue

            if not is_room_ok(room_no, board): continue

            # prefer the bottom position in the room
            goal_position = lowest_hallway_position(board, room_no)
            assert(goal_position != -1)

            size = 2 if len(board[1]) == 8 else 4
            new_board = copy_board(board)
            new_board[1][room_no * size + goal_position] = pod_type
            new_board[0][pod[0]] = '.'
            room_distance += goal_position + 1
            new_board[2] += MOVEMENT_COST[pod_type] * room_distance
            possible_moves.append(new_board)
        else:
            # pod in a room. The only move is to go into the hallway.
            # TODO: extend a bit
            # pod in stuck in the room
            if is_pod_stuck(pod[1], board): continue

            # in correct spot (and doesn't need to move out of the way), don't move
            room_no = get_room_no(pod[1], board)
            if is_room_ok(room_no, board): continue

            # search to see what hallway positions are valid
            for hallway_pos, distance in find_valid_hallway_positions(board, pod[1]):
                # create the new board
                new_board = copy_board(board)

                pod_type = board[1][pod[1]]
                new_board[0][hallway_pos] = pod_type
                new_board[1][pod[1]] = "."
                
                # calculate the cost
                size = 2 if len(board[1]) == 8 else 4
                distance += pod[1] % size + 1
                new_board[2] += MOVEMENT_COST[pod_type] * distance

                possible_moves.append(new_board)

    return possible_moves

def get_room_distance(board, room_no, hallway_pos):
    room_pos = 2 + (room_no * 2)
    dist = 0
    for i in range(min(room_pos, hallway_pos), max(room_pos, hallway_pos)):
        # path blocked
        if dist != 0 and board[0][i].isalpha(): return -1
        dist += 1
    return dist

def lowest_hallway_position(board, room_no):
    size = 2 if len(board[1]) == 8 else 4
    for i in range(size):
        if board[1][(size * room_no) + i].isalpha(): return i - 1

    return size - 1

assert(lowest_hallway_position(BIG_CORRECT_BOARD, 0) == -1)

def get_room_no(room_pos, board):
    # get the room number independent of board size
    if len(board[1]) == 8:
        return room_pos // 2
    else:
        return room_pos // 4

def get_pod_type(room_no):
    for key, value in POD_ROOMS.items():
        if value == room_no: return key
    assert(False)

def is_room_ok(room_no, board):
    size = 2 if len(board[1]) == 8 else 4
    pod_type = get_pod_type(room_no)

    # look down the room
    for i in range(size):
        tile = board[1][(size * room_no) + i]
        if not (tile == pod_type or tile == '.'): return False

    return True

assert(is_room_ok(0, BIG_CORRECT_BOARD) == True)

def is_pod_stuck(room_pos, board):
    room_no = get_room_no(room_pos, board)
    size = 2 if len(board[1]) == 8 else 4

    # look down the room for pods
    for i in range(room_pos % size):
        if board[1][(size * room_no) + i].isalpha(): return True
    
    return False
    
assert(is_pod_stuck(1, CORRECT_BOARD) == True)

def get_xpos_of_room(room_no):
    return 2 + (room_no * 2)

def copy_board(board):
    return [board[0][:], board[1][:], board[2]]

def is_board_complete(board):
    if len(board[1]) == 8:
        return board[0] == CORRECT_BOARD[0] and board[1] == CORRECT_BOARD[1]
    else:
        return board[0] == BIG_CORRECT_BOARD[0] and board[1] == BIG_CORRECT_BOARD[1]

assert(is_board_complete(CORRECT_BOARD) == True)

if __name__ == "__main__":
    with open('./input/23.txt') as f:
        data = f.read().splitlines()
        initial_board = read_initial_board(data, big=True)
        visualise_board(initial_board, big=True)

        print(solve(initial_board))