import math 
import functools
import re
import random
import collections
from helpers.helpers import *

if __name__ == "__main__":
    with open('./input/2.txt') as f:
        data = f.read().splitlines()
        for l in data:
            l = whitespace_split(l)
            print(l)
        