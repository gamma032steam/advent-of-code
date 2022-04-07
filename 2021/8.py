import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/8.txt') as f:
        data = f.read().splitlines()

        # part 1
        print(sum([len([z for z in y if len(z) in [2, 4, 3, 7]]) for y in [x.split('|')[1].strip().split(' ') for x in data]]))

        # part 2
        numbers = dict({
            frozenset('abcefg'): '0',
            frozenset('cf'): '1',
            frozenset('acdeg'): '2',
            frozenset('acdfg'): '3',
            frozenset('bcdf'): '4',
            frozenset('abdfg'): '5',
            frozenset('abdefg'): '6',
            frozenset('acf'): '7',
            frozenset('abcdefg'): '8',
            frozenset('abcdfg'): '9'
        })

        sum = 0
        for line in data:
            puzzle = line.split('|')[0].strip().split(' ')
            
            # find 1 and 7
            one = set([x for x in puzzle if len(x) == 2][0])
            seven = set([x for x in puzzle if len(x) == 3][0])

            # a must be the letter 7 has that 1 doesn't
            a = list(seven - one)[0]

            # find 0, 6 and 9
            six_line_nums = [set(x) for x in puzzle if len(x) == 6]

            # one of these numbers (6) has everything but one of the edges from 1
            six = set([x for x in six_line_nums if list(set('abcdefg') - x)[0] in one][0])

            # that missing edge is c, and the one that's not missing is f
            c = list(one - six)[0]
            f = list(set(one.intersection(six)))[0]

            # the difference between 4 and 2 are b and d
            four = set([x for x in puzzle if len(x) == 4][0])
            b_and_d = four - one

            # d is missing from 0
            zero = set([x for x in six_line_nums if list(set('abcdefg') - x)[0] in b_and_d][0])
            d = list(set('abcdefg') - zero)[0]

            # and the one that's not missing is b
            b = list(b_and_d - set(d))[0]

            # e and g are just whatever's left
            e_and_g = set('abcdefg') - set([a, b, c, d, f])

            # and e doesn't appear in 9
            nine = set([x for x in six_line_nums if list(set('abcdefg') - x)[0] in e_and_g][0])
            e = list(set('abcdefg') - nine)[0]

            # and so the final letter is g
            g = list(e_and_g - set(e))[0]     

            solution = [a, b, c, d, e, f, g]

            # now map the output digits
            output_digits = line.split('|')[1].strip().split(' ')
            translated_digits = [list(map(lambda y: chr(solution.index(y)+97), x)) for x in output_digits]
            num = int(''.join(list(map(lambda x: numbers[frozenset(x)], translated_digits))))
            sum += num
        print(sum)
