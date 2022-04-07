input = "vzbxkghb"
#input = "abcdffaa"
#input = "abcdefgh"

def valid(password):
    # 3 increasing
    cnt = 0
    good = False
    for i in range(1, len(password)):
        c = password[i]
        if password[i-1] == (c - 1):
            cnt += 1
            if cnt == 2: 
                good = True
                break
        else:
            cnt = 0

    if not good: return False

    # bad letters
    if 'i' in password or 'o' in password or 'l' in password: return False

    # pairs
    pairs = 0
    i = 1
    while i < len(password):
        c = password[i]
        if c == password[i-1]:
            pairs += 1
            i += 1

        i += 1
    return pairs >= 2 

if __name__ == "__main__":
    with open('./input/11.txt') as f:
        data = f.read().splitlines()
        
        chars = [ord(c) - 97 for c in input]
        print(chars)

        while True:
            # check if valid
            if valid(chars):
                print(''.join([chr(c + 97) for c in chars]))
                

            # incerement
            chars[-1] += 1
            i = -1
            while chars[i] == 26:
                chars[i] = 0
                i -= 1
                chars[i] += 1

