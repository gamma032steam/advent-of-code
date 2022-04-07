if __name__ == "__main__":
    #with open('./input/25.txt') as f:
    grid = [[None for _ in range(8000)] for _ in range(8000)]

    grid[1][1] = 20151125
    last_num = grid[1][1]
    for i in range(2, 9000):
        if i >= len(grid): break
        for col in range(1, i+1):
            new_num = last_num * 252533
            new_num %= 33554393
            
            row = i + 1 - col
            grid[row][col] = new_num
            last_num = new_num
    #for row in grid:
    #    print(row)

    print(grid[3010][3019])