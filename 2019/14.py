# 2022 attempt
from re import split

from functools import lru_cache

# if __name__ == "__main__":
#     with open('./2019/input/14.txt') as f:
#         data = f.read().splitlines()
#         print(data)
#         reactions = []
#         chems = set()

#         for line in data:
#             ins, out = line.split( "=> ")
#             out_q, out_v = out.split(" ")
#             out_q = int(out_q)
#             ins = split(', ', ins)
#             ins = [x.strip().split(' ') for x in ins]
#             ins = [(int(x), y) for x, y in ins]
#             for x, y in ins: chems.add(y)
#             reactions.append((ins, (out_q, out_v)))
#             chems.add(out_v)

#         chems = list(chems)
#         chem_lookup = {v: i for i, v in enumerate(chems)}

        
#         ore_amt = 500
#         while True:
#             if ore_amt % 25 == 0: print(ore_amt)
#             start = [0] * len(chems)
#             start[chem_lookup['ORE']] = ore_amt
#             start = tuple(start) 

#             stack = [start]
#             seen = set([start])
#             while stack:
#                 state = stack.pop()
#                 if state[chem_lookup['FUEL']] > 0:
#                     print("done", ore_amt)
#                     exit()
                
#                 for ins, outs in reactions:
#                     times = 1
#                     while True:
#                         good = True
#                         # see if we have enough of the ins
#                         for q, v in ins:
#                             if q * times <= state[chem_lookup[v]]: continue
#                             else:
#                                 good = False
#                                 break

#                         if not good: break
#                         # apply the reaction
#                         new_state = list(state)
#                         for q, v in ins:
#                             new_state[chem_lookup[v]] -= q * times
#                         new_state[chem_lookup[outs[1]]] += outs[0]
#                         tup = tuple(new_state)
#                         if tup in seen:
#                             times += 1
#                             continue
#                         seen.add(tup)
#                         stack.append(tup)
#                         times += 1


#             ore_amt += 1

if __name__ == "__main__":
    with open('./input/14.txt') as f:
        data = f.read().splitlines()
        print(data)
        graph = dict()
        chems = set()

        for line in data:
            ins, out = line.split( "=> ")
            out_q, out_v = out.split(" ")
            out_q = int(out_q)
            ins = split(', ', ins)
            ins = [x.strip().split(' ') for x in ins]
            ins = [(int(x), y) for x, y in ins]
            for x, y in ins: chems.add(y)
            graph[out_v] = (out_q, ins)
            chems.add(out_v)

        chems = list(chems)
        chem_lookup = {v: i for i, v in enumerate(chems)}

        l, r = 0, pow(10, 10)
        while l <= r:
            mid = (r + l) // 2
            start = [0] * len(chems)
            start[chem_lookup['FUEL']] = mid
            start = tuple(start)

            min_ore = float('inf')
            print(chems)
            stack = [start]
            seen = set([start])
            
            while stack:
                state = stack.pop()
                #print(state)
                #if len(stack) % 100 == 0: print(len(stack))
                #print(stack)
                # check if we have nothing but ORE
                found = False
                for i, qty in enumerate(state):
                    if i == chem_lookup['ORE']: continue
                    if qty > 0:
                        found = True
                        break
                if not found:
                    min_ore = min(min_ore, state[chem_lookup['ORE']])
                    print(min_ore)
                    break

                # for everything we have a nonzero amount of, run a chem reaction
                for i, qty in enumerate(state):
                    if qty <= 0: continue
                    if i == chem_lookup['ORE']: continue
                    amount, reqs = graph[chems[i]]
                    j, rem = divmod(qty, amount)
                    if rem > 0: j += 1
                    state_copy = list(state)
                    for q, v in reqs:
                        state_copy[chem_lookup[v]] += q * j
                    state_copy[chem_lookup[chems[i]]] -= amount * j
                    tup = tuple(state_copy)
                    if tup in seen: 
                        continue
                    stack.append(tuple(state_copy))
                    seen.add(tup)
            
            if min_ore > 1000000000000:
                 r = mid - 1
            else:
                l = mid
            print(mid)

        print(l, r)
        print("mf", min_ore)
        print(chems)