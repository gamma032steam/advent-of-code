from itertools import combinations
from queue import PriorityQueue

# non-matching generators kills microchips

SAMPLE_FLOORS = (
    (("H", "M"), ("L", "M")),
    (("H", "G"),),
    (("L", "G"),),
    ()
)

# The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.
# The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
# The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
# The fourth floor contains nothing relevant.
Q1_FLOORS = (
    (("T", "G"), ("T", "M"), ("PL", "G"), ("S", "G")),
    (("PL", "M"), ("S", "M")),
    (("PR", "G"), ("PR", "M"), ("R", "G"), ("R", "M")),
    ()
)

# On the first floor
# An elerium generator.
# An elerium-compatible microchip.
# A dilithium generator.
# A dilithium-compatible microchip
Q2_FLOORS = (
    (("T", "G"), ("T", "M"), ("PL", "G"), ("S", "G"), ("E", "G"), ("E", "M"), ("D", "G"), ("D", "M")),
    (("PL", "M"), ("S", "M")),
    (("PR", "G"), ("PR", "M"), ("R", "G"), ("R", "M")),
    ()
)

def is_finished(floors):
    return all([len(floor) == 0 for floor in floors[:-1]])

def is_state_valid(floors):
    for floor in floors:
        f = set(floor)
        # any unnatached microships?
        unattached_microchip = False
        # any generators?
        generator = False
        for element, type in f:
            if type == "M":
                if (element, "G") not in f:
                    unattached_microchip = True
            else:
                generator = True
        if unattached_microchip and generator: return False
    return True


# big search
seen = set([(Q2_FLOORS, 0)])
queue = PriorityQueue() # prioritize max number of things on final floor -> min number of steps
queue.put((0, 0, Q2_FLOORS, 0))
while True:
    _, steps, floors, elevator_floor = queue.get()
    #if steps % 5 == 0: print(steps, queue.qsize())
    if is_finished(floors):
        print(f'Finished in {steps} moves.')
        break

    # we can pick up either 1 or 2 things and move them up or down a floor
    for elevator in list(combinations(floors[elevator_floor], 2)) + list(combinations(floors[elevator_floor], 1)):
        for direction in [-1, 1]:
            new_elevator_floor = elevator_floor + direction
            if not (0 <= new_elevator_floor < len(floors)): continue
            # 2 PRUNING THINGS
            # 1. never take two things down
            if direction == -1 and len(elevator) == 2: continue
            # 2. if going down, only take generators
            if direction == -1 and len(elevator) == 1 and elevator[0][1] != "G": continue

            new_floors = list(floors)
            new_floors = [list(f) for f in new_floors]
            for item in elevator:
                new_floors[elevator_floor].remove(item)
                new_floors[new_elevator_floor].append(item)

            new_floors = [tuple(f) for f in new_floors]
            new_floors = tuple(new_floors)
            # remove duplicate states
            if is_state_valid(new_floors) and (new_floors, new_elevator_floor) not in seen:
                queue.put((-len(new_floors[-1]), steps + 1, new_floors, new_elevator_floor))
                seen.add((new_floors, new_elevator_floor))
