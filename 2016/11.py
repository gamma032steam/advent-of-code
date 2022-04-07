import math 
import functools
import re
import random
import collections

// microchips (M) and generators (RTG) --
        //
        // chips can only be powered by corresponding RTG

        //In other words, if a chip is ever left in the same area as another RTG,
        // and it's not connected to its own RTG, the chip will be fried.

        //it can carry at most yourself and two RTGs or microchips in any combination
        //the elevator will only function if it contains at least one RTG or microchip

        //The elevator always stops on each floor to recharge, and this takes long enough that the items
        // within it and the items on that floor can irradiate each other.
        // (You can prevent this if a Microchip and its Generator end up on the same floor in this way,
        // as they can be connected while the elevator is recharging

if __name__ == "__main__":
    with open('./input/11.txt') as f:
        data = f.read().splitlines()

        