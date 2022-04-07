import hashlib

input = "yzbqklnj"
#input = "abcdef609043"

i = 1
while True:
    word = input + str(i)
    #word = input
    hash = hashlib.md5(word.encode()).hexdigest()
    if hash[:6] == "000000":
        print(i)
        break

    i+=1