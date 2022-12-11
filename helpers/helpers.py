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

class MutableSet:
    """Like a set, but accepts arrays by converting them to tuples first."""
    pass
