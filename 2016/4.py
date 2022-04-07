import math 
import functools
import re
import random
import collections

from collections import Counter
from tabnanny import check

if __name__ == "__main__":
    with open('./input/4.txt') as f:
        data = f.read().splitlines()

        sum_of_ids = 0
        for room in data:
            parts = room.split("-")
            ids, checksum = parts[-1].split("[")
            checksum = checksum[:-1]

            # get all the words
            name = ""
            for word in parts:
                if not word[0].isalpha(): break
                name += word

            counts = Counter(name)

            arr = []
            for i, count in counts.items():
                arr.append((-count, i))
            arr.sort()

            valid = True
            for letter in checksum:
                #print(letter)
                if len(arr) == 0:
                    valid = False
                    break
                freq, letter2 = arr.pop(0)
                if letter != letter2: 
                    valid = False
                    break
            
            if (valid):
                sum_of_ids += int(ids)
            else:
                continue

            # part 2: do the shift
            new_name = ""
            for key in name:
                integer = ord(key) - 97
                integer += int(ids)
                integer %= 26
                integer += 97
                new_key = chr(integer)
                new_name += new_key
            #print(new_name, ids)
            if ("north" in new_name): print(new_name, ids)
        print(sum_of_ids)
        