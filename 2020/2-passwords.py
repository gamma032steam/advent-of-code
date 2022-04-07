import math 
import functools
import re
import random

def solve(data):
    cnt = 0
    for line in data:
        spl = line.split(':')
        rule = spl[0].split(' ')
        minn = rule[0].split('-')[0]
        maxn = rule[0].split('-')[1]
        letter = rule[1]
        password = spl[1].strip()
        if password.count(letter) >= int(minn) and password.count(letter) <= int(maxn):
            cnt += 1
    print(cnt)

def solve2(data):
    cnt = 0
    for line in data:
        spl = line.split(':')
        rule = spl[0].split(' ')
        minn = rule[0].split('-')[0]
        maxn = rule[0].split('-')[1]
        letter = rule[1]
        password = spl[1].strip()
        if (password[int(minn)-1] == letter) != (password[int(maxn)-1] == letter):
            cnt += 1
    print(cnt)


if __name__ == "__main__":
    with open('./input/2-input.txt') as f:
        data = f.read().splitlines()
        solve2(data)