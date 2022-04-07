if __name__ == "__main__":
    with open('./input/16.txt') as f:
        data = f.read().splitlines()

        my_sue = {
            "children": 3,
            "cats": 7,
            "samoyeds": 2,
            "pomeranians": 3,
            "akitas": 0,
            "vizslas": 0,
            "goldfish": 5,
            "trees": 3,
            "cars": 2,
            "perfumes": 1
        }

        def valid(data, thing, count):
            if thing in ["cats", "trees"]:
                return count > data[thing]
            if thing in ["pomeranians", "goldfish"]:
                return count < data[thing]
            return count == data[thing]

        for line in data:
            words = line.split(" ")
            sue = words[1]
            thing1 = words[2][:-1]
            count1 = int(words[3][:-1])

            thing2 = words[4][:-1]
            count2 = int(words[5][:-1])

            thing3 = words[6][:-1]
            count3 = int(words[7])
        
            #if my_sue[thing1] == count1:
            #    continue
            #     and my_sue[thing2] == count2 and my_sue[thing3] == count3:
            #    print(sue)

            if valid(my_sue, thing1, count1) and valid(my_sue, thing2, count2) and valid(my_sue, thing3, count3):
                print(sue)
