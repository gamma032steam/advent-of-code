input = [
".....",
"...#.",
".#..#",
".#.#.",
"...##",
]

# input = [
# "....#",
# "#..#.",
# "#.?##",
# "..#..",
# "#...."
# ]

def trans(grid):
    ng = []
    for r in grid:
        rw = []
        for c in r:
            if c == ".": rw.append(0)
            else: rw.append(1)
        ng.append(tuple(rw))
    return tuple(ng)

def bio(grid):
    sum = 0
    x = 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1: sum += x
            x *= 2
    return sum

def life(grid):
    ng = []
    for i in range(len(grid)):
        rw = []
        for j in range(len(grid[0])):
            cnt = 0
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni = i + di
                nj = j + dj
                if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                    if grid[ni][nj] == 1: cnt += 1
            if grid[i][j] == 1:
                if cnt == 1: rw.append(1)
                else: rw.append(0)
            else:
                if cnt in [1, 2]: rw.append(1)
                else: rw.append(0)
        ng.append(tuple(rw))
    
    return tuple(ng)

# if __name__ == "__main__":
#     grid = trans(input)
#     seen = set([grid])
#     while True:
#         grid = life(grid)
#         s = bio(grid)

#         if grid in seen:
#             print(s)
#             exit()

#         seen.add(grid)

# part 2

def adj(l, i, j):
    res = []
    if i == 0:
        res.append((l+1, 1, 2))
    if i == 4:
        res.append((l+1, 3, 2))
    if j == 0:
        res.append((l+1, 2, 1))
    if j == 4:
        res.append((l+1, 2, 3))

    if i == 2 and j == 1:
        for i2 in range(5):
            res.append((l-1, i2, 0))
    if i == 2 and j == 3:
        for i2 in range(5):
            res.append((l-1, i2, 4))
    if i == 1 and j == 2:
        for j2 in range(5):
            res.append((l-1, 0, j2))
    if i == 3 and j == 2:
        for j2 in range(5):
            res.append((l-1, 4, j2))

    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni = i + di
        nj = j + dj
        if not (0 <= ni < 5 and 0 <= nj < 5): continue
        if ni == 2 and nj == 2: continue
        res.append((l, ni, nj))
    return res

if __name__ == "__main__":
    on = set()
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == '#': on.add((0, i, j))


    for _ in range(200):
        new_on = set()

        def compute(level, i, j):
            cnt = 0
            for l2, i2, j2 in adj(level, i, j):
                if (l2, i2, j2) in on:
                    cnt += 1
            alive = False
            if (level, i, j) in on and cnt == 1: alive = True
            if (level, i, j) not in on and cnt in [1, 2]: alive = True
            if alive: new_on.add((level, i, j))

        for l, i, j in on:
            compute(l, i, j)
            for l2, i2, j2 in adj(l, i, j):
                compute(l2, i2, j2)
        on = new_on
    
    print(len(on))
