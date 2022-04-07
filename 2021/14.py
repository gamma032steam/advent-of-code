import math
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open("./input/14.txt") as f:
        data = f.read()

        template, rules = data.split("\n\n")
        rules = rules.split("\n")

        result_of_pair = dict()
        for rule in rules:
            input, output = rule.split(" -> ")
            input = (input[0], input[1])
            result_of_pair[input] = output

        # part 1
        amount_of_each_pair = collections.defaultdict(int)
        for i in range(len(template) - 1):
            amount_of_each_pair[(template[i], template[i + 1])] += 1

        # 10 for part 1, 40 for part 2
        for i in range(40):
            next_template = collections.defaultdict(int)
            for pair, count in amount_of_each_pair.items():
                result = result_of_pair[pair]
                next_template[(pair[0], result)] += count
                next_template[(result, pair[1])] += count
            amount_of_each_pair = next_template

        letter_count = collections.defaultdict(int)
        for pair, count in amount_of_each_pair.items():
            letter_count[pair[0]] += count
        letter_count[template[-1]] += 1
        print(max(letter_count.values()) - min(letter_count.values()))
