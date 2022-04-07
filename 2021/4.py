import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/4.txt') as f:
        data = f.read().splitlines()
        # both part 1 and 2
        called_nums, boards, marked = data[0].split(','), [list(map(lambda x: x.split(), data[board_start:board_start+5])) for board_start in range(2, len(data), 6)], [[] for _ in range((len(data)-1)//6)]
        is_board_solved = lambda marked: any([list(map(lambda x: x[0], marked)).count(i) == 5 or list(map(lambda x: x[1], marked)).count(i) == 5 for i in range(5)])
        sum_unseen = lambda marked, board: sum([int(board[a][b]) for a, b in [(i, j) for i in range(5) for j in range(5)] if (a, b) not in marked])
        solved = set()
        for num in called_nums:
            for i, board in [(f, x) for f, x in enumerate(boards) if f not in solved]:
                marked[i] = marked[i] + [(i, j) for i in range(5) for j in range(5) if board[i][j] == num]
                if any([list(map(lambda x: x[0], marked[i])).count(j) == 5 or list(map(lambda x: x[1], marked[i])).count(j) == 5 for j in range(5)]): 
                    solved.add(i)
                    if (len(solved) == 1): print(sum_unseen(marked[i], board) * int(num))
                    if (len(solved) == len(boards)): print(sum_unseen(marked[i], board) * int(num))
