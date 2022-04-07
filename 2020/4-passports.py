import math 
import functools
import re
import random
import copy

def solve1clean(data):
    # Clean into a list of dicts
    passports = data.split('\n\n')
    passport_pairs = []
    for passport in passports:
        passport_pairs.append(dict())
        for row in re.split('[\n ]', passport):
            k, v = row.split(":")
            passport_pairs[-1][k] = v

    # Count number of passports with the correct fields
    cnt = 0
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

    for passport in passport_pairs:
        if all(field in passport.keys() for field in fields):
            cnt += 1
    print(cnt)

def solve2clean(data):
    # Clean into a list of dicts
    passports = data.split('\n\n')
    passport_pairs = []
    for passport in passports:
        passport_pairs.append(dict())
        for row in re.split('[\n ]', passport):
            k, v = row.split(":")
            passport_pairs[-1][k] = v

    # Count number of passports with the correct fields
    cnt = 0
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

    for passport in passport_pairs:
        if all(field in passport.keys() for field in fields) and all([validate(x,y) for x, y in passport.items()]):
            cnt += 1
    print(cnt)

def validate(key, value):
    if key == "byr" and re.match('^[0-9]{4}$', value) and int(value) >= 1920 and int(value) <= 2002:
        return True
    elif key == "iyr" and re.match('^[0-9]{4}$', value) and int(value) >= 2010 and int(value) <= 2020:
        return True
    elif key == "eyr" and re.match('^[0-9]{4}$', value) and int(value) >= 2020 and int(value) <= 2030:
        return True
    elif key == "hgt":
        match = re.match('^([0-9]{2,3})(cm|in)$', value)
        if not match:
            return False

        if match.group(2) == "cm" and int(match.group(1)) >= 150 and int(match.group(1)) <= 193:
            return True
        if match.group(2) == "in" and int(match.group(1)) >= 59 and int(match.group(1)) <= 76:
            return True
    elif key == "hcl" and re.match('^#(\w{6})$', value):
        return True
    elif key == "ecl" and re.match('^(amb|blu|brn|gry|grn|hzl|oth)$', value):
        return True
    elif key == "pid" and re.match('^[0-9]{9}$', value):
        return True
    elif key == "cid":
        return True
    else:
        return False

if __name__ == "__main__":
    with open('./input/4-input.txt') as f:
        #data = f.read().splitlines()
        #solve1(data)
        solve2clean(f.read())