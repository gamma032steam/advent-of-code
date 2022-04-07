

if __name__ == "__main__":
    with open('./input/18.txt') as f:
        data = f.read().splitlines()
        current_board = data
        for step in range(100):
            new_board = [[' ' for _ in range(100)] for _ in range(100)] 
            for i, line in enumerate(data):
                for j, cell in enumerate(line):
                    neis = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1)]
                    assert(len(neis) == 8)
                    cnt = 0
                    for di, dj in neis:
                        new_i, new_j = i + di, j + dj
                        if not 0 <= new_i <= 99: continue
                        if not 0 <= new_j <= 99: continue
                        if current_board[new_i][new_j] == "#":
                            cnt += 1
                    if current_board[i][j] == "#":
                        if cnt == 2 or cnt == 3:
                            new_board[i][j] = "#"
                        else:
                            new_board[i][j] = "."
                    else:
                        if cnt == 3:
                            new_board[i][j] = "#"
                        else:
                            new_board[i][j] = "."
            current_board = new_board
            current_board[0][0] = "#"
            current_board[0][-1] = "#"
            current_board[-1][0] = "#"
            current_board[-1][-1] = "#"

        on = sum([line.count("#") for line in current_board])
        print(on)
