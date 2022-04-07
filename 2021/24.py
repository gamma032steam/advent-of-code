import math 
import functools
import re
import random
import collections

VARIABLE_MAP = dict({
    'w': 0,
    'x': 1,
    'y': 2,
    'z': 3
})

# this function is for testing, and isn't part of the solution
def brute_force(data):
    data = data.splitlines()
    variables = [0, 0, 0, 0]
    curr_num = "99999999999999"
    for w in range(1, 9):
        curr_num = str(w)
        for z in range(10000, 10300):
            print(w, z)
            variables = [0, 0, 0, z]
            for instruction in data:
                print(variables, instruction)
                input_num = curr_num[:]
                instruction = instruction.split()
                var = VARIABLE_MAP[instruction[1]]

                if instruction[0] == "inp":
                    variables[var] = int(input_num[0])
                    input_num = input_num[1:]
                    continue

                value = variables[VARIABLE_MAP[instruction[2]]] if instruction[2].isalpha() else int(instruction[2])             
                if instruction[0] == "add":
                    variables[var] += value
                elif instruction[0] == "mul":
                    variables[var] *= value
                elif instruction[0] == "div":
                    if instruction[2] == '0': break
                    assert(instruction[2] != '0')
                    variables[var] //= value
                elif instruction[0] == "mod":
                    if variables[var] < 0 or value <= 0:
                        break
                    assert(variables[var] >= 0)
                    assert(int(instruction[2]) > 0)
                    variables[var] %= value
                elif instruction[0] == "eql":
                    variables[var] = 1 if variables[var] == value else 0
            if variables[3] == 267086:
                print(w, z)
                print("valid")
                quit()

def get_blocks(data):
    # there are only three unique values: where we divide by 1 andthe two numbers added
    blocks = []
    for block in data.split("inp w"):
        if len(block) == 0: continue
        block = block.splitlines()
        blocks.append([int(block[4].split()[2]), int(block[5].split()[2]), int(block[15].split()[2])])
    blocks.reverse()
    return blocks

# analytical/numerical solution to find what zin values produce a zout
def get_required_vals(block, zout):
    # finds the possible zin, w pairs
    pairs = []
    if block[0] == 26:
        # zout = 26*zin + f, F = w - a
        for w in range(1, 10):
            # let f be z % 26
            for f in range(0, 26):
                if (w - block[1]) == f:
                    pairs.append(((26 * zout) + f, w))
    else:
        for w in range(1, 10):
            num_to_divide = zout - (w + block[2])
            if num_to_divide % 26 != 0: continue
            pairs.append((num_to_divide / 26, w))

    return pairs

# solve bottom-up, expecting zout = 0 at the end and zin = 0 at the start
def solve(blocks, target, solutions, current):
    if len(blocks) == 0:
        if target == 0: solutions.append(current)
        return solutions
    for zin, w in get_required_vals(blocks[0], target):
        solve(blocks[1:], zin, solutions, str(w) + current)
    return solutions

if __name__ == "__main__":
    with open('./input/24.txt') as f:
        data = f.read()
        # brute_force(data)
        blocks = get_blocks(data)
        #print(get_required_vals(blocks[0], 267086))
        #brute_force(data)
        solutions = solve(blocks, 0, [], "")
        print(max(solutions))
        print(min(solutions))
