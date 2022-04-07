import math
import functools
import re
import random
import collections


def convert(val):
    if isinstance(val, int) or val.isnumeric() or val[0] == "-":
        return int(val)
    elif len(val) == 1:
        return ord(val.lower()) - 97
    assert False


def part_2():
    with open("./input/18.txt") as f:
        data = f.read().splitlines()
        data = list(map(lambda x: x.split(" "), data))

        context = 0
        prog_0_ins = 0
        prog_1_ins = 0
        prog_0_queue = []
        prog_1_queue = []
        prog_0_registers = [0] * 26
        prog_1_registers = [0] * 26
        prog_0_registers[convert('p')] = 0
        prog_1_registers[convert('p')] = 1

        values_sent_by_1 = 0

        while True:
            idx, queue, registers = (
                (prog_0_ins, prog_0_queue, prog_0_registers)
                if context == 0
                else (prog_1_ins, prog_1_queue, prog_1_registers)
            )
            other_queue = prog_1_queue if context == 0 else prog_0_queue
            ins = data[idx]

            x = convert(ins[1])
            if ins[1].isalpha():
                z = registers[x]
            else:
                z = x
            if len(ins) == 3:
                y = convert(ins[2])
                if ins[2].isalpha():
                    y = registers[y]

            if ins[0] == "set":
                registers[x] = y
            elif ins[0] == "add":
                registers[x] += y
            elif ins[0] == "mul":
                registers[x] *= y
            elif ins[0] == "snd":
                other_queue.insert(0, registers[x])
                if context == 1:
                    values_sent_by_1 += 1
            elif ins[0] == "mod":
                registers[x] %= y
            elif ins[0] == "rcv":
                registers[x] = queue.pop()
            elif ins[0] == "jgz":
                if z > 0:
                    idx += y - 1

            idx += 1
            if context == 0:
                prog_0_ins = idx
            else:
                prog_1_ins = idx

            # determine which program goes next
            next_0_ins = data[prog_0_ins][0]
            next_1_ins = data[prog_1_ins][0]
            in_bounds_0 = 0 <= prog_0_ins <= len(data)
            in_bounds_1 = 0 <= prog_1_ins <= len(data)
            if (
                next_0_ins == "rcv"
                and next_1_ins == "rcv"
                and len(prog_0_queue) == 0
                and len(prog_1_queue) == 0
            ) or (not in_bounds_0 and not in_bounds_1):
                break
            elif (next_0_ins == "rcv" and len(prog_0_queue) == 0) or not in_bounds_0:
                context = 1
            else:
                context = 0

    print(values_sent_by_1)


def part_1():
    with open("./input/18.txt") as f:
        data = f.read().splitlines()
        data = list(map(lambda x: x.split(" "), data))

        print(data)

        instruction_idx = 0
        last_played_sound = None
        registers = [0] * 26
        i = 0
        while True and 0 <= instruction_idx < len(data):

            i += 1
            ins = data[instruction_idx]

            x = convert(ins[1])
            if ins[1].isalpha():
                z = registers[x]
            else:
                z = x
            if len(ins) == 3:
                y = convert(ins[2])
                if ins[2].isalpha():
                    y = registers[y]
            print(x, y, ins)

            if ins[0] == "set":
                registers[x] = y
            elif ins[0] == "add":
                registers[x] += y
            elif ins[0] == "mul":
                registers[x] *= y
            elif ins[0] == "snd":
                last_played_sound = registers[x]
            elif ins[0] == "mod":
                registers[x] %= y
            elif ins[0] == "rcv":
                if registers[x] > 0:
                    registers[x] = last_played_sound
                    print(last_played_sound)
                    break
            elif ins[0] == "jgz":
                if z > 0:
                    instruction_idx += y - 1

            print(registers, instruction_idx)
            instruction_idx += 1


if __name__ == "__main__":
    # part_1()
    part_2()
