if __name__ == "__main__":
    with open('./input/2.txt') as f:
        data = f.read().splitlines()
        total = 0
        total2 = 0
        for line in data:
            l, w, h = [int(x) for x in line.split("x")]
            sides = [2*l*w, 2*w*h, 2*h*l]
            cost = 0
            cost += sum(sides)
            cost += min(sides) / 2
            total += cost

            sides = [l, w, h]
            sides.sort()
            total2 += sides[0] * 2
            total2 += sides[1] * 2
            total2 += l * w * h

        print(total)
        print(total2)            