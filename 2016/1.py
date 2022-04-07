import math 
import functools
import re
import random
import collections
from tkinter import Y

if __name__ == "__main__":
    with open('./input/1.txt') as f:
        data = f.read()
        data = data.split(", ")

        dx, dy = 0, 1
        x, y = 0, 0

        seen = set((0, 0))

        while True:
            
            for ins in data:
                dir = ins[0]
                dist = int(ins[1:])
            
                if dir == "R":
                    dx, dy = dy, -dx
                else:
                    dx, dy = -dy, dx 

                for i in range(dist):
                    x += dx
                    y += dy
                
                    if (x, y) in seen:
                        print(x, y)
                        print(x + y)
                        quit()

                    seen.add((x, y))

    print(x + y)