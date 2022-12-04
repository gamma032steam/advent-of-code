import re

def whitespace_split(str):
    '''Splits on all whitespace, not just spaces.'''
    return re.split('\s+', str)

assert(whitespace_split('a b    c d e') == ['a', 'b', 'c', 'd', 'e'])

class MutableSet:
    """Like a set, but accepts arrays by converting them to tuples first."""
    pass
