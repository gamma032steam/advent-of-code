import math 
import functools
import re
import random
import collections

import hashlib

if __name__ == "__main__":
    with open('./input/5.txt') as f:
        data = f.read()
        print(data)
        password = [None] * 8
        i = 1 
        while True:
            hash_to_test = bytes(data + str(i), 'utf-8')
            hash = hashlib.md5(hash_to_test).hexdigest()
            if i == 3231929: print(hash)
            starts_with_0 = all([hash[i] == "0" for i in range(5)])
            if starts_with_0:
                if hash[5].isnumeric():
                    position = int(hash[5])
                    if (0 <= position <= 7) and password[position] == None:
                            print(position, hash[6])
                            password[position] = hash[6]
                
            if all(password): break
            i += 1
        print(''.join(password))