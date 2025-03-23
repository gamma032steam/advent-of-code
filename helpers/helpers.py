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
    return [int(x) for x in re.findall(r'[+-]?\d+', s)]

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
    can be of any dimension. Returns starting from the deepest nested index.'''
    seen = []
    find_all_nd_rec(grid, target, [], seen)
    return seen

def find_all_nd_rec(grid, target, path=[], seen=[]):
    for i, element in enumerate(grid):
        if element != target and (isinstance(element, (list, tuple)) or (isinstance(element, str) and len(element) > 1)):
            path.insert(0, i)
            find_all_nd_rec(element, target, path, seen)
            path.pop(0)
        elif element == target: seen.append((i, *path))

assert(find_all_nd([[0, 1], [2,3]], 2) == [(0, 1)])
assert(find_all_nd([[[0, 1], [2, 3]], [[4, 7],[6,7]]], 7) == [(1, 0, 1), (1, 1, 1)])
assert(find_all_nd([[[0, 1], [2, 3]], [[4, 7],[6,7]]], 1) == [(1, 0, 0)])

def manhattan(x, y):
    return sum(abs(x - y) for x, y in zip(x, y))

assert(manhattan((-2, 5), (8, 9)) == (10 + 4))

def floyd_warshall(graph, edges=None):
    '''Finds the distange from one node to every other node. If no edge weights
    are provided, assumes a cost of 1.'''
    distance = collections.defaultdict(lambda: float('inf'))

    # add all the known distances
    for u, vs in graph.items():
        distance[(u, u)] = 0
        for v in vs:
            edge_weight = 1 if edges is None else edges[(u, v)]
            distance[(u, v)] = edge_weight

    # k is the 'stepping stone'
    for k in graph:
        for i in graph:
            for j in graph:
                if distance[(i, j)] > distance[(i, k)] + distance[(k, j)]:
                    distance[(i, j)] = distance[(i, k)] + distance[(k, j)]

    return distance

def min_max_bounds(it):
    minx, maxx, miny, maxy = float('inf'), float('-inf'), float('inf'), float('-inf')
    for x, y in it:
        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)
    return minx, maxx, miny, maxy     
