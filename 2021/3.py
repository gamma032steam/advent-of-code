import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/3.txt') as f:
        data = f.read().splitlines()
        print(int(''.join([str(int([x[i] for x in data].count('1') > [x[i] for x in data].count('0'))) for i in range(12)]), 2) * (int(''.join([str(int([x[i] for x in data].count('1') > [x[i] for x in data].count('0'))) for i in range(12)]), 2) ^ int('111111111111', 2)))
        criteria = lambda strs, pos, sort, default: ('1' if sort == 'most' else '0') if [x[pos] for x in strs].count('1') > [x[pos] for x in strs].count('0') else default if [x[pos] for x in strs].count('1') == [x[pos] for x in strs].count('0') else ('0' if sort == 'most' else '1')
        i, j, ox, co2 = (0, 0, data[:], data[:])
        while len(ox) > 1 or len(co2) > 1: 
            if len(ox) > 1: ox = [x for x in ox if x[i] == criteria(ox, i, 'most', '1')]
            if len(co2) > 1: co2 = [x for x in co2 if x[i] == criteria(co2, i, 'least', '0')]
            i, j = i + 1, j + 1
        print(int(ox[0], 2) * int(co2[0], 2))