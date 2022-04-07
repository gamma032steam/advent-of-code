
from collections import defaultdict

if __name__ == "__main__":
    with open('./input/7.txt') as f:
        data = f.read().splitlines()
        ops = dict()
        values = dict()
        inbound = defaultdict()
        deps = defaultdict(set)
    
        zeros = []
        for line in data:
            operation, dest_wire = line.split(' -> ')
            op_words = operation.split(" ")
            ops[dest_wire] = op_words
            if len(op_words) == 1:
                if op_words[0].isnumeric():
                    zeros.append(dest_wire)
                    inbound[dest_wire] = 0
                else:
                    inbound[dest_wire] = 1
                    deps[op_words[0]].add(dest_wire)
            elif len(op_words) == 2:
                inbound[dest_wire] = 1
                deps[op_words[1]].add(dest_wire)
            else:
                if op_words[1] == "OR" or op_words[1] == "AND":
                    inbound[dest_wire] = 2
                    deps[op_words[0]].add(dest_wire)
                    deps[op_words[2]].add(dest_wire)
                else:
                    inbound[dest_wire] = 1
                    deps[op_words[0]].add(dest_wire)

        while zeros:
            curr = zeros.pop()
            # calculate value
            op_words = ops[curr]
            if len(op_words) == 1:
                if op_words[0].isnumeric():
                    values[curr] = int(op_words[0])
                else:
                    values[curr] = values[op_words[0]]
            elif len(op_words) == 2:
                val_1 = values[op_words[1]]
                binary = bin(val_1)[2:].zfill(16)
                flipped = ''.join(['1' if c == '0' else '0' for c in binary])
                new = int(flipped, 2)
                values[curr] = new
            else:
                op = op_words[1]
                if op == "AND" or op == "OR":
                    val_1 = values[op_words[0]]
                    val_2 = values[op_words[2]]
                    if op == "AND":
                        new = val_1 & val_2
                    elif op == "OR":
                        new = val_1 | val_2
                else:
                    val_1 = values[op_words[0]]
                    val_2 = int(op_words[2])
                    if op == "LSHIFT":
                        new = val_1 << val_2
                    elif op == "RSHIFT":
                        new = val_1 >> val_2
                values[curr] = new

            # remove deps
            for dep in deps[curr]:
                inbound[dep] -= 1
                if inbound[dep] == 0:
                    zeros.append(dep)

        print(values)
        #print(values['a'])
        print(inbound)

