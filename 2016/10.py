import math 
import functools
import re
import random
import collections

from collections import defaultdict

if __name__ == "__main__":
    with open('./input/10.txt') as f:
        data = f.read().splitlines()

        initial = defaultdict(list)
        starter = None
        for line in data:
            words = line.split(" ")
            if len(words) != 6: continue
            val, bot = int(words[1]), int(words[5])
            initial[bot].append(val)
            if len(initial[bot]) == 2: starter = bot

        ins = dict()
        for line in data:
            words = line.split(" ")
            if len(words) == 6: continue
            ins[int(words[1])] = (words[5], int(words[6]), words[10], int(words[11]))

        output = dict()
        while True:
            curr = None
            for key, val in initial.items():
                if len(val) == 2:
                    curr = key
                    break

            if curr == None: break

            #print(curr)
            low_type, low_number, high_type, high_number = ins[curr]
            lo, hi = sorted(initial[curr])
            if lo == 17 and hi == 61:
                print(curr)

            if low_type == "output":
                output[low_number] = lo
            else:
                initial[low_number].append(lo)

            if high_type == "output":
                output[high_number] = hi
            else:
                initial[high_number].append(hi)

            initial[curr] = []
    print(output[0] * output[1] * output[2])
