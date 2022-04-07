import math 
import functools
import re
import random
import collections
from itertools import combinations

hp = 109
dmg = 8
armour = 2

if __name__ == "__main__":
    with open('./input/21.txt') as f:
        data = f.read().split('\n\n')
        data = [d.splitlines() for d in data]

        swords = [x.split() for x in data[0]]
        armour = [y.split() for y in data[1]]
        rings = [z.split() for z in data[2]]

        armour.append(["", "0", "0", "0"])

        options = []
        for s in swords:
            c, d, a = int(s[1]), int(s[2]), 0
            
            for p in armour:
                x, y, z = c, d, a
                x += int(p[1])
                z += int(p[3])
                options.append((x, y, z))

                for r in rings:
                    i, j, k = x, y, z
                    i += int(r[2])
                    j += int(r[3])
                    k += int(r[4])
                    options.append([i, j, k])

                for pair in combinations(rings, 2):
                    i, j, k = x, y, z
                    i += int(pair[0][2])
                    j += int(pair[0][3])
                    k += int(pair[0][4])
                    i += int(pair[1][2])
                    j += int(pair[1][3])
                    k += int(pair[1][4])
                    options.append([i, j, k])
        print(len(options))
        lc = float('inf')
        hc = float('-inf')
        for cost, dmg, ar in options:
            my_hp = 100
            b_hp = 109
            b_dmg = 8
            b_ar = 2

            turn = True
            while my_hp > 0 and b_hp > 0:
                if turn:
                    b_hp -= max(1, dmg - b_ar)
                else:
                    my_hp -= max(1, b_dmg - ar)
                turn = not turn

            if b_hp <= 0:
                #print(cost, dmg, ar)
                lc = min(lc, cost)
            else:
                hc = max(hc, cost)
        print(lc)
        print(hc)


