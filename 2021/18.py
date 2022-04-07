import math 
import functools
import re
import random
import collections
import ast
import copy

class Pair:
    def __init__(self, parent):
        self.parent = parent

    def __str__(self):
        return "[" + str(self.l) + "," + str(self.r) + "]"

def parse_line(line):
    # convert string to lists and integers
    lst = ast.literal_eval(line)

    # parse the nested array and build a tree
    return build_tree(lst)

def build_tree(node, parent=None):
    # base case: regular number
    if isinstance(node, int):
        return node
    new_node = Pair(parent)
    new_node.l = build_tree(node[0], new_node)
    new_node.r = build_tree(node[1], new_node)
    return new_node

def snail_add(left, right):
    new_node = Pair(None)
    new_node.l, new_node.r = left, right
    new_node.l.parent, new_node.r.parent = new_node, new_node
    return new_node

def snail_explode(root):
    # repeatedly explode
    changed = False
    next_to_explode = find_explode(root)
    if next_to_explode != None:
        # perform the explode: find the left and right nodes
        left, side = find_left_adjacent(next_to_explode)
        if left:
            if side == 'l':
                left.l += next_to_explode.l
            else:
                left.r += next_to_explode.l
        right, side = find_right_adjacent(next_to_explode)
        if right:
            if side == 'l':
                right.l += next_to_explode.r
            else:
                right.r += next_to_explode.r

        # replace with 0
        if next_to_explode.parent.r is next_to_explode:
            next_to_explode.parent.r = 0
        else:
            next_to_explode.parent.l = 0
        next_to_explode = find_explode(root)
        changed = True
    return root, changed
        
def find_explode(root):
    # preorder traversal
    stack = [(root, 0)]
    while stack:
        current, depth = stack.pop()
        if isinstance(current, Pair):
            if depth >= 4:
                return current

            stack.append((current.r, depth + 1))
            stack.append((current.l, depth + 1))

    return None

def find_left_adjacent(node):
    # find the lowest parent where the node is on the right
    curr = node.parent
    prev = node
    while curr:
        if curr.l is prev:
            prev = curr
            curr = curr.parent
        else:
            break

    if curr == None: return None, ''

    # sibling is leftmost
    if curr.r is node:
        if isinstance(curr.l, int):
            return curr, 'l'
        curr = curr.l
    else:
        if isinstance(curr.l, int): return curr, 'l'
        curr = curr.l

    # find the rightmost child
    while isinstance(curr.r, Pair):
        curr = curr.r 

    return curr, 'r'

def find_right_adjacent(node):
    # find the lowest parent where the node is on the left
    curr = node.parent
    prev = node
    while curr:
        if curr.r is prev:
            prev = curr
            curr = curr.parent
        else:
            break

    if curr == None: return None, ''

    # sibling is rightmost
    if curr.l is node:
        if isinstance(curr.r, int):    
            return curr, 'r'
        curr = curr.r
    else:
        if isinstance(curr.r, int): return curr, 'r'
        curr = curr.r

    # find the leftmost child
    while isinstance(curr.l, Pair):
        curr = curr.l

    return curr, 'l'

def snail_split(root):
    changed = False
    next_to_split, side = find_split(root)
    if next_to_split:
        if side == 'l':
            new_pair = Pair(next_to_split)
            new_pair.l = math.floor(next_to_split.l / 2)
            new_pair.r = math.ceil(next_to_split.l / 2)
            next_to_split.l = new_pair
        else:
            new_pair = Pair(next_to_split)
            new_pair.l = math.floor(next_to_split.r / 2)
            new_pair.r = math.ceil(next_to_split.r / 2)
            next_to_split.r = new_pair
        next_to_split, side = find_split(root)
        changed = True
    return root, changed

def find_split(root):
    # preorder traversal
    stack = [(root, None)]
    while stack:
        current, parent = stack.pop()
        if isinstance(current, Pair):
            stack.append((current.r, current))
            stack.append((current.l, current))
        else:
            if current >= 10:
                return (parent, 'l') if parent.l == current else (parent, 'r')
    return None, ''

def find_magnitude(root):
    if isinstance(root, int):
        return root
    return 3 * find_magnitude(root.l) + 2 * find_magnitude(root.r)

def reduce(current_sum):
    changed = True
    while changed:
        current_sum, exploded = snail_explode(current_sum)
        while exploded:
            current_sum, exploded = snail_explode(current_sum)
        current_sum, split = snail_split(current_sum)
        changed = exploded or split
    return current_sum

if __name__ == "__main__":
    with open('./input/18.txt') as f:
        # build a graph
        data = f.read().splitlines()
        terms = [parse_line(l) for l in data]

        # part 1
        current_sum = terms[0]
        for i in range(1, len(terms)):
            current_sum = snail_add(current_sum, terms[i])
            current_sum = reduce(current_sum)
        print(find_magnitude(current_sum))

        # part 2
        terms = [parse_line(l) for l in data]
        highest_sum = -1
        for i in range(len(terms)-1):
            x = copy.deepcopy(terms[i])
            for j in range(i + 1, len(terms)):
                # kinda slow, better than coding a copy function
                terms = [parse_line(l) for l in data]
                x, y = terms[i], terms[j]

                x_y_sum = reduce(snail_add(x, y))
                x_y_mag = find_magnitude(x_y_sum)
                terms = [parse_line(l) for l in data]
                x, y = terms[i], terms[j]
                y_x_sum = reduce(snail_add(y, x))
                y_x_mag = find_magnitude(y_x_sum)

                highest_sum = max(highest_sum, max(x_y_mag, y_x_mag))
                terms = [parse_line(l) for l in data]
        print(highest_sum)
