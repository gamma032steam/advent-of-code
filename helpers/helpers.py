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
    '''Finds adjacent coordinates. Verifies they're inside the grid, if provided.'''
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


assert(adjacent(0, 0) == [(1, 0), (-1, 0), (0, 1), (0, -1)])

def find_nd(grid, target):
    '''Finds the coordinate location of the target inside the grid, where grid
    can be of any dimension.'''
    for i, element in enumerate(grid):
        if element != target and (isinstance(element, list) or isinstance(element, tuple)):
            search = find_nd(element, target)
            if search is not None:
                return (*search, i)
        else:
            if element == target: return (i,)

    return None


assert(find_nd([[0, 1], [2,3]], 2) == (0, 1))
assert(find_nd([[0, 1], [2,3]], 5) == None)
assert(find_nd([[[0, 1], [2, 3]], [[4, 5],[6,7]]], 7) == (1, 1, 1))


def find_all_nd(grid, target):
    '''Finds the coordinate locations of the targets inside the grid, where grid
    can be of any dimension.'''
    seen = []
    find_all_nd_rec(grid, target, [], seen)
    return seen

def find_all_nd_rec(grid, target, path=[], seen=[]):
    for i, element in enumerate(grid):
        if element != target and (isinstance(element, list) or isinstance(element, tuple)):
            path.insert(0, i)
            search = find_all_nd_rec(element, target, path, seen)
            path.pop(0)
        else:
            if element == target: seen.append((i, *path))

    return None

assert(find_all_nd([[0, 1], [2,3]], 2) == [(0, 1)])
assert(find_all_nd([[[0, 1], [2, 3]], [[4, 7],[6,7]]], 7) == [(1, 0, 1), (1, 1, 1)])

