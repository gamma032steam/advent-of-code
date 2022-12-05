import math 
import functools
import re
import random
import collections
import sys
import os

from helpers import whitespace_split

if __name__ == "__main__":
    with open('./input/2.txt') as f:
        data = f.read().splitlines()
        for l in data:
            l = whitespace_split(l)
            print(l)
        