import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./3-input.txt') as f:
        data = f.read().splitlines()
        tot = 0
        for l in data:
            s1 = l[:len(l) // 2]
            s2 = set(l[len(l)//2:])
            print(l, s1,s2)
            s1 = set(s1)
            for i in s2:
                if i in s1:
                    if i.isupper():
                        tot += ord(i) - ord('A') + 27
                        print(i, tot)
                    else:
                        tot += ord(i) - ord('a') + 1
                        print(i, tot)
        print(tot)
                    
        tot = 0
        for i in range(0, len(data), 3):
            a = set(data[i])
            b=  set(data[i+1])
            c = set(data[i+2])
            k = a.intersection(b).intersection(c)
            d = k.pop()
            if d.isupper():
                tot += ord(d) - ord('A') + 27
            else:
                tot += ord(d) - ord('a') + 1
        print(tot)
