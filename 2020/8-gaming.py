import math 
import functools
import re
import random
import collections

class Instruction:
    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

def solve1(code):
    line = 0
    acc = 0
    seen = set()

    while True:
        if line in seen or line >= len(code):
            print(acc)
            break
        seen.add(line)    
        inst = code[line]

        if inst.op == "acc":
            acc += inst.arg
            line += 1
        elif inst.op == "jmp":
            line += inst.arg
        elif inst.op == "nop":
            line += 1

def solve2(code):
    # Try every line, and swap nops for jmp
    for i in range(len(code)):
        if code[i].op == "nop" or code[i].op == "jmp":
            # Swap the op
            code[i].op = "nop" if code[i].op == "jmp" else "jmp"

            # Run the program!
            line = 0
            acc = 0
            seen = set()

            while True:
                if line in seen:
                    break
                if line == len(code):
                    print(acc)
                    return

                seen.add(line)    
                inst = code[line]

                if inst.op == "acc":
                    acc += inst.arg
                    line += 1
                elif inst.op == "jmp":
                    line += inst.arg
                elif inst.op == "nop":
                    line += 1

            # Switch back
            code[i].op = "nop" if code[i].op == "jmp" else "jmp"


if __name__ == "__main__":
    with open('./input/8-input.txt') as f:
        data = f.read().splitlines()
        code = list(map(lambda x: Instruction(x.split()[0], int(x.split()[1])), data))
        solve1(code)
        solve2(code)