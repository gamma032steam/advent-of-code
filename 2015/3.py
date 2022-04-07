if __name__ == "__main__":
    with open('./input/3.txt') as f:
        data = f.read()

        i, j = 0, 0
        x, y = 0, 0
        seen = set([(0, 0)])
        turn = 0
        for c in data:
            if turn == 0:
                if c == '^': 
                    j += 1
                if c == 'v':
                    j -= 1
                if c == "<":
                    i -= 1
                if c == ">": 
                    i += 1
                seen.add((i, j))
            else:
                if c == '^': 
                    y += 1
                if c == 'v':
                    y -= 1
                if c == "<":
                    x -= 1
                if c == ">": 
                    x += 1
                seen.add((x, y))
            turn = (turn + 1) % 2 
        print(len(seen))