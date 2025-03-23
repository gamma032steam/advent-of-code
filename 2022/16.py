import math 
import functools
import re
import random
import collections
import helpers
import sys
import queue
import itertools
sys.setrecursionlimit(100000)

def solve(inp):
    flow = {} # flow rate for each room
    graph = {} # adjacency list
    rooms = {} # assign each room an int
    for line in inp.splitlines():
        source, room_flow, out = re.search(r'Valve (..) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.+)', line).groups()
        room_flow = int(room_flow)
        out = out.split(', ')
        graph[source] = out
        flow[source] = room_flow
        rooms[source] = len(rooms)
    
    # find the distance between each room and every other room
    distances = helpers.floyd_warshall(graph)
    print(distances)

    # we only really care about rooms that have a flow rate > 0
    targets = [k for k, v in flow.items() if v > 0]

    def get_pressure(room, turns):
        return flow[room] * (26 - turns)

    # state is as follows:
    # pos 1 & 2: the rooms we are in
    # goal 1 & 2: if not '', the target rooms we are trying to reach
    # dist 1 & 2: steps remaining towards the goal
    # steps: minutes passed
    # pressure: total pressure confirmed so far
    # valves: the valves that have been opened 
    start = (0, 'AA', 'AA', '', '', -1, -1, 1, [False] * len(rooms))
    stack = [start] # stack for dfs
    best = float('-inf')
    seen = dict()
    while stack: 
        pressure, pos1, pos2, goal1, goal2, dist1, dist2, steps, valves = stack.pop()

        # we're done at minute 26, or if all valves are turned, as 
        # no actions can release more pressure
        if steps == 26 or all([valves[rooms[i]] for i in targets]):
            if pressure > best: 
                print(pressure)
            best = max(pressure, best)
            continue

        # BAD CODE: skip some of the states that waste time
        if steps == 13 and pressure < 1700: continue 

        # figure out what moves are possible for you and the elephant
        options = [[], []]
        for i, pos in enumerate([pos1, pos2]):
            if (i == 0 and goal1 != '') or (i == 1 and goal2 != ''):
                # continue moving towards a target
                options[i].append(('step', ''))
            elif not valves[rooms[pos]] and flow[pos] != 0:
                # turn a valve
                options[i].append(('valve', pos))
            else:
                # move to a new target
                for target in targets:
                    if valves[rooms[target]]: continue # skip if we've already turned the valve
                    if target == pos: continue # already there
                    options[i].append((('move', target)))

        # enumerate every pair of possible moves
        for you, elephant in itertools.product(options[0], options[1]):
            new_pressure = pressure
            new_valves = list(valves)
            new_pos = [pos1, pos2]
            new_goal = [goal1, goal2]
            new_dist = [dist1, dist2]
            for i, action in enumerate([you, elephant]):
                move, value = action
                match move:
                    case 'valve':
                        # elephant tries to turn a valve we are also turning
                        if new_valves[rooms[value]]: continue

                        new_pressure += get_pressure(value, steps)
                        new_valves[rooms[value]] = True
                    case 'move':
                        new_goal[i] = value
                        new_dist[i] = distances[(new_pos[i], value)] - 1
                        new_pos[i] = ''
                    case 'step':
                        new_dist[i] -= 1

                # completed the journey to a target node
                # note that, if the target was 1 step away, we do this all in one move
                if new_dist[i] == 0:
                    new_pos[i] = new_goal[i]
                    new_goal[i] = ''
                    new_dist[i] = -1

            seen_state = (*new_pos, *new_goal, *new_dist, steps+1, tuple(new_valves))
            if seen_state in seen and seen[seen_state] > new_pressure:
                continue
            else:
                seen[(*new_pos, *new_goal, *new_dist, steps+1, tuple(new_valves))] = new_pressure  

            state = (new_pressure, *new_pos, *new_goal, *new_dist, steps + 1, tuple(new_valves))
            stack.append(state)

    print(best)

fname = './16-input.txt' 
try:
    f = open(fname)
except Exception as e:
    print(f"ERROR: Could not open {fname}: {e}.")
solve(f.read().strip())

sample="""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
if len(sample) > 0:
    print('\n---SAMPLE---')
    solve(sample)
    print('------------')
