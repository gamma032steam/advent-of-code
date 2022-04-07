import math 
import functools
import re
import random
import collections


def clean_edges(line):
    edges = line.strip()
    edges = edges.split()
    edges = list(map(int, edges))
    return edges

if __name__ == "__main__":
    with open('./input/3.txt') as f:
        data = f.read().splitlines()

        valid = 0
        for t in data:
            edges = clean_edges(t)
            if edges[0] + edges[1] <= edges[2]:
                continue
            if edges[0] + edges[2] <= edges[1]:
                continue
            if edges[1] + edges[2] <= edges[0]:
                continue
            valid += 1

        print(valid)
        valid = 0
        for i in range(0, len(data), 3):
            t1e1, t2e1, t3e1 = clean_edges(data[i])
            t1e2, t2e2, t3e2 = clean_edges(data[i+1])
            t1e3, t2e3, t3e3 = clean_edges(data[i+2])

            #print(t1e1,t1e2,t1e3)
           # print(t3e1, t3e2, t3e3)
            if ((t1e2 + t1e3 > t1e1) and (t1e1 + t1e3 > t1e2) and (t1e1 + t1e2 > t1e3)):
                valid += 1
            
            if ((t2e2 + t2e3 > t2e1) and (t2e1 + t2e3 > t2e2) and (t2e1 + t2e2 > t2e3)):
                valid += 1

            if ((t3e2 + t3e3 > t3e1) and (t3e1 + t3e3 > t3e2) and (t3e1 + t3e2 > t3e3)):
                valid += 1

        print(valid)
