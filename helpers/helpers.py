import collections
import re
import operator

ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,  # use operator.div for Python 2
    '%' : operator.mod,
    '^' : operator.xor,
}

def whitespace_split(str):
    '''Splits on all whitespace, not just spaces.'''
    return re.split('\s+', str)

assert(whitespace_split('a b    c d e') == ['a', 'b', 'c', 'd', 'e'])

def ints(s):
    return [int(x) for x in re.findall(r'\d+', s)]

assert(ints('go from 32 to 42') == [32, 42])

def chars(s):
    return [x for x in s.split() if x.isalpha() and len(x) == 1]

assert(chars('go from x to y') == ['x', 'y'])

def adjacent(x, y, grid=None, diags=False):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diags: directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
    new_positions = []
    for delta_x, delta_y in directions:
        new_x, new_y = x + delta_x, y + delta_y
        # validate positions
        if grid is not None:
            if not (0 <= new_y < len(grid) and 0 <= new_x < len(grid[0])): 
                continue
        new_positions.append((new_x, new_y))
    return new_positions

