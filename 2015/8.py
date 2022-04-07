import re
if __name__ == "__main__":
    with open('./input/8.txt') as f:
        data = f.read().splitlines()
        total = 0
        for i, line2 in enumerate(data):
            line = line2[1:-1]
            esc1 = len(re.findall(r"\\\\", line))
            esc2 = len(re.findall(r"\\\"", line))
            esc3 = len(re.findall(r"\\x[\da-fA-F][\da-fA-F]", line))
            size = len(line2) - (len(line2) - 2 - esc1 - esc2 - (3 * esc3))
            print(size)
            print(esc1, esc2, esc3)
            total += size

        print(total)


        # total = 0
        # for i, line in enumerate(data):
        #     esc1 = len(re.findall(r"\"", line))
        #     esc2 = len(re.findall(r"\\", line))
        #     size = esc1 + esc2 + 2
        #     print(size)
        #     #print(esc1, esc2, esc3)
        #     total += size

        print(total)
