import math 
import functools
import re
import random
import collections

import pandas as pd
import collections

if __name__ == "__main__":
    with open('./input/6.txt') as f:
        data = f.read().splitlines()

    # part 1
    for i in range(len(data)):
        data[i] = list(data[i])

    df = pd.DataFrame(data)
    most_common = ""
    for i in range(8):
        # part 1
        #most_common += df[df.columns[i]].mode()
        
        # part 2
        most_common += collections.Counter(df[i].to_list()).most_common()[-1][0]
    print(most_common)

    
