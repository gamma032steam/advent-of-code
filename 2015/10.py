input = "1321131112"
#input = "111221"

if __name__ == "__main__":
    current_number = input
    for _ in range(50):
        new_number = ""
        curr, length = current_number[0], 1
        for i, c in enumerate(current_number):
            if i == 0: continue
            if c == curr:
                length += 1
            else:
                new_number += str(length)
                new_number += str(curr)
                curr = c
                length = 1

        new_number += str(length)
        new_number += str(curr)  
        current_number = new_number

    print(current_number)
    print(len(current_number))