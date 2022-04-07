import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/1.txt') as f:
        data = f.read().splitlines()

        print(data[0].count('(') - data[0].count(')')) 

        pos = 0
        for i, char in enumerate(data[0]):
            if char == '(':
                pos += 1
            else:
                pos -= 1
            if pos == -1:
                print(i)
                break