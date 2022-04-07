import math 
import functools
import re
import random

def find1(nums):
    for i in range(0, len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == 2020:
                print(nums[i] * nums[j])

def find2(nums):
    for i in range(0, len(nums)):
        for j in range(i+1, len(nums)):
            for k in range(j+1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 2020:
                    print(nums[i] * nums[j] * nums[k])

if __name__ == "__main__":
    with open('./input/1-input.txt') as f:
        data = f.read().splitlines()
        data = list(map(int, data))
        find1(data)