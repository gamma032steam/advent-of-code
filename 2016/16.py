import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    def run_step(inp):
        b = inp[:]
        b = b[::-1]
        c = ""
        for ch in b:
            if ch == "0":
                c += "1"
            else:
                c += "0"
        return inp + "0" + c

    size = 35651584
    inp = "01111010110010011"
    while len(inp) < size:
        inp = run_step(inp)

    cs = inp[:size]
    while len(cs) % 2 == 0:
        new = ""
        for i in range(0, len(cs), 2):
            if cs[i] == cs[i+1]:
                new += "1"
            else:
                new += "0"
        cs = new

    print(cs)
