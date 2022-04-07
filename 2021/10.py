import math 
import functools
import re
import random
import collections

if __name__ == "__main__":
    with open('./input/10.txt') as f:
        data = f.read().splitlines()

        # part 1
        syntax_error_score = dict({
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
        })

        incomplete_lines = []
        syntax_score = 0
        for line in data:
            stack =  []
            for char in line:
                if char in ['(', '[', '{', '<']:
                    stack.append(char)
                else:
                    matches = [('(', ')'), ('[', ']'), ('{', '}'),  ('<', '>')]
                    if len(stack) > 0 and (stack[-1], char) in matches:
                        stack.pop()
                    else:
                        syntax_score += syntax_error_score[char]
                        stack = []
                        break
            if len(stack) > 0:
                incomplete_lines.append(stack)
                        
        print(syntax_score)

        # part 2
        autocomplete_scores = []
        autocomplete_score = dict({
            '(': 1,
            '[': 2,
            '{': 3,
            '<': 4
        })
        for stack in incomplete_lines:
            score = 0
            for char in stack[::-1]:
                score *= 5
                score += autocomplete_score[char]
            autocomplete_scores.append(score)

        autocomplete_scores.sort()
        print(autocomplete_scores[len(autocomplete_scores) // 2])
