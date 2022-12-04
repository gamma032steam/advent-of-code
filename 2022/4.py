import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./4-input.txt') as f:
        data = f.read().splitlines()
        t = 0
        t2 = 0
        x = []
        for l in data:
            x, y = l.split(',')
            a,b = x.split('-')
            c,d = y.split('-')
            a = int(a)
            b = int(b)
            c = int(c)
            d = int(d)
            if a <= c <= d <= b or c <= a <= b <= d:
                t +=1
                print(a,b,c,d)
            for k in range(a, b+1):
                if k in range(c,d+1):
                    t2 += 1
                    break

        print(t)
        print(t2)