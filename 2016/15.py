import re

with open('./input/15.txt') as f:
    discs = []
    data = f.readlines()
    for line in data: 
        match = re.match('Disc #\d+ has (\d+) positions; at time=0, it is at position (\d+).', line)
        discs.append([int(x) for x in match.groups()])

    print(discs)

    # https://brilliant.org/wiki/chinese-remainder-theorem/
    # https://www.youtube.com/watch?v=ru7mWZJlRQg
    # we want to solve the system of congruences where
    # x = curr disc pos (mod # positions)