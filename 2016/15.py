import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/15.txt') as f:
        data = f.read().splitlines()

        disc_size = [13,5,17,3,7,19]
        #disc_size = [5,2]

        time = 1
        disc_position = [11, 0, 11, 0, 2, 17]
        #disc_position = [4,1]
        while True:
            #if time >= 10: exit()
            disc_position = [(d + 1) for d in disc_position]

            valid = True
            for i, disc in enumerate(disc_position):
                print(i, disc, disc_position, time)
                if disc % disc_size[i] != i:
                    valid = False
                    break

            if valid:
                print(time-1)
                exit()

            time += 1