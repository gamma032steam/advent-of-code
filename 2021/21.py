import math 
import functools
import re
import random
import collections
import functools

# the number of dfferent rolls in a turn, and the number of ways you can roll it
possibilities = dict({
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
})
assert(sum(possibilities.values()) == (3*3*3))

def part_2(p1_start, p2_start):
    print(solve(0, 0, p1_start, p2_start, 1))

@functools.cache
def solve(p1_score, p2_score, p1_position, p2_position, turn):
    # base case: there is a winner
    if p1_score > 20:
        return 1
    elif p2_score > 20:
        return 0

    # recursive case
    ways_to_win = 0
    for score, paths in possibilities.items():
        if turn == 1:
            new_pos = (p1_position + score) % 10
            new_pos = 10 if new_pos == 0 else new_pos
            new_score = p1_score + new_pos
            ways_to_win += paths * solve(new_score, p2_score, new_pos, p2_position, 2)
        else:
            new_pos = (p2_position + score) % 10
            new_pos = 10 if new_pos == 0 else new_pos
            new_score = p2_score + new_pos
            ways_to_win += paths * solve(p1_score, new_score, p1_position, new_pos, 1)
    return ways_to_win

if __name__ == "__main__":
    with open('./input/21.txt') as f:
        data = f.read().splitlines()
        p1_start = int(data[0][-1])
        p2_start = int(data[1][-1])

        # part 1
        p1_pos, p2_pos = p1_start, p2_start
        p1_score, p2_score = 0, 0
        turn = 1
        die = 1
        times_rolled = 0
        while p1_score < 1000 and p2_score < 1000:
            die_sum = 0
            for _ in range(3):
                die_sum += die
                die += 1
                if die == 101: die = 1
            times_rolled += 3

            if turn == 1:
                new_pos = (p1_pos + die_sum) % 10
                p1_pos = 10 if new_pos == 0 else new_pos
                p1_score += p1_pos
            else:
                new_pos = (p2_pos + die_sum) % 10
                p2_pos = 10 if new_pos == 0 else new_pos
                p2_score += p2_pos
            turn = 2 if turn == 1 else 1

        print(p2_score * times_rolled)

        # part 2
        part_2(p1_start, p2_start)
