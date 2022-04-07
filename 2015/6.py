if __name__ == "__main__":
    with open('./input/6.txt') as f:
        data = f.read().splitlines()

        # grid = [['.' for _ in range(1000)] for _ in range(1000)]
        # for line in data:
        #     words = line.split()
        #     ins = words[0] if words[0] == "toggle" else words[0] + " " + words[1]
        #     startx, starty = list(map(int, words[-3].split(",")))
        #     endx, endy = list(map(int, words[-1].split(",")))
        #     for i in range(startx, endx + 1):
        #         for j in range(starty, endy + 1):
        #             if ins == "toggle":
        #                 grid[i][j] = "#" if grid[i][j] == "." else "."
        #             elif ins == "turn on":
        #                 grid[i][j] = "#"
        #             else:
        #                 grid[i][j] = "."
        # print(sum([l.count("#") for l in grid]))

        # part 2
        grid = [[0 for _ in range(1000)] for _ in range(1000)]
        for line in data:
            words = line.split()
            ins = words[0] if words[0] == "toggle" else words[0] + " " + words[1]
            startx, starty = list(map(int, words[-3].split(",")))
            endx, endy = list(map(int, words[-1].split(",")))
            for i in range(startx, endx + 1):
                for j in range(starty, endy + 1):
                    if ins == "toggle":
                        grid[i][j] += 2
                    elif ins == "turn on":
                        grid[i][j] += 1
                    else:
                        grid[i][j] = max(0, grid[i][j] - 1)
        print(sum([sum(l) for l in grid]))