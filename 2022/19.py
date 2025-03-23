import math 
import functools
import re
import random
import collections
import helpers
import sys
sys.setrecursionlimit(100000)

def solve(inp):
    # read input
    bps = []
    for line in inp.splitlines():
        bps.append(helpers.ints(line))

    bps = bps[0:3]
    duration = 33 # duration should be + 1 over the target
    tot_quality = 0
    geodes = []

    for i, bp in enumerate(bps):
        _, ore_ore, clay_ore, ob_ore, ob_clay, g_ore, g_ob = bp
        stack = [(1, 1, 0, 0, 0, 0, 0, 0, 0, False, False, False, False)]
        seen = set()
        best = 0

        # optimisation 1: basic caching
        def add_st(state):
            if state not in seen:
                stack.append(state)
            seen.add(state)
        
        while stack:
            time, orob, crob, obrob, grob, o, c, ob, g, buildo, buildc, buildob, buildg = stack.pop()

            # finished
            if time == duration:
                best = max(best, g)
                continue

            # buy
            # optimisation 2: if we could have build a robot last turn but didn't,
            # you can't build it the next turn
            if o >= g_ore and ob >= g_ob and not buildg:
                add_st((time + 1, orob, crob, obrob, grob + 1, o + orob - g_ore, c + crob, ob + obrob - g_ob, g + grob, False, False, False, False))
                buildg = True
                # optimisation 3: if we can build a g robot, don't even consider other choices
                continue
            if o >= ore_ore and not buildo:
                add_st((time + 1, orob + 1, crob, obrob, grob, o + orob - ore_ore, c + crob, ob + obrob, g + grob, False, False, False, False))
                buildo = True
            if o >= clay_ore and not buildc:
                add_st((time + 1, orob, crob + 1, obrob, grob, o + orob - clay_ore, c + crob, ob + obrob, g + grob, False, False, False, False))          
                buildc = True
            if o >= ob_ore and c >= ob_clay and not buildob:
                add_st((time + 1, orob, crob, obrob + 1, grob, o + orob - ob_ore, c + crob - ob_clay, ob + obrob, g + grob, False, False, False, False))
                buildob = True
    
            # optimisation 4: don't build robots that producemore that we can 
            # consume in a turn
            if orob > max([ore_ore, clay_ore, ob_ore, g_ore]):
                continue
            if crob > ob_clay:
                continue
            if obrob > g_ob:
                continue

            # optimisation 5: if we assume we add a new geode robot every turn
            # from here and still we can't beat the current best, stop here
            if g + sum([grob + t for t in range(1, duration + 1 - time)]) < best:
                continue

            # don't buy anything
            add_st((time + 1, orob, crob, obrob, grob, o + orob, c + crob, ob + obrob, g + grob, buildo, buildc, buildob, buildg))
        
        tot_quality += best * (i + 1)
        geodes.append(best)
        print(best)
    print('quality', tot_quality)
    print(geodes)
    if len(geodes) == 3: print(geodes[0] * geodes[1] * geodes[2])
fname = './19-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    #solve(sample)
    print('------------')
