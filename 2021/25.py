import math 
import functools
import re
import random
import collections

def visualise(board):
    for line in board:
        print(''.join(line))

def step(board):
    # step east facing
    moved_east = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '>' and (i, j) not in moved_east:
                new_pos = (j + 1) % len(board[0])
                if board[i][new_pos] == '.' and (i, new_pos) not in moved_east:
                    board[i][new_pos] = '>'
                    board[i][j] = '.'
                    moved_east.add((i, new_pos))
                    moved_east.add((i, j))

    # step south facing
    moved_south = set()
    for j in range(len(board[0])):
        for i in range(len(board)):
            if board[i][j] == 'v' and (i, j) not in moved_south:
                new_pos = (i + 1) % len(board)
                if board[new_pos][j] == '.' and (new_pos, j) not in moved_south:
                    board[new_pos][j] = 'v'
                    board[i][j] = '.'
                    moved_south.add((new_pos, j))
                    moved_south.add((i, j))

    return board, moved_south.union(moved_east)

if __name__ == "__main__":
    with open('./input/25.txt') as f:
        data = [list(x) for x in f.read().split('\n')]
        steps = 0
        while True:
            steps += 1
            data, moved = step(data)
            if len(moved) == 0:
                print(steps)
                break
        visualise(data)