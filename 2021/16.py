import math 
import functools
import re
import random
import collections

total_version_numbers = 0

def form_binary_string(hex_string):
    return ''.join([bin(int(char, 16))[2:].zfill(4) for char in hex_string])

def read_packet(packet, current_packet=0, current_bits=0, max_bits=None, max_subpackets=None, acc=None):
    if acc == None: acc = []
    if (not packet or 
      (max_subpackets != None and current_packet >= max_subpackets) or 
      (max_bits != None and current_bits >= max_bits)): return acc, current_bits
   
    version = int(packet[0:3], 2)
    id = int(packet[3:6], 2)
    remaining_packet = packet[6:]
    global total_version_numbers
    total_version_numbers += version

    if id == 4: 
        num, pos = read_literal(remaining_packet)
    else:
        num, pos = read_operator(remaining_packet, id)
    acc.append(num)
    return read_packet(remaining_packet[pos:], current_packet + 1, current_bits + pos + 6, max_bits, max_subpackets, acc)

def read_literal(packet):
    current_number = ""
    i = 0
    while i < len(packet):
        current_number += packet[i+1:i+5]
        if packet[i] == '0':
            return str(int(current_number, 2)), i + 5
        i += 5

def read_operator(packet, id):
    length_type_id = packet[0]
    if length_type_id == '0':
        packet_size_bits = int(packet[1:16], 2)
        nums, length = read_packet(packet[16:], max_bits=packet_size_bits)
        return perform_calculation(nums, id), 16 + length
    elif length_type_id == '1':
        num_sub_packets = int(packet[1:12], 2)
        nums, length = read_packet(packet[12:], max_subpackets=num_sub_packets)
        return perform_calculation(nums, id), 12 + length

def perform_calculation(nums, id):
    nums = [int(num) for num in nums]
    if id == 0:
        return sum(nums)
    elif id == 1:
        return functools.reduce(lambda x, y: x * y, nums)
    elif id == 2:
        return min(nums)
    elif id == 3:
        return max(nums)
    elif id == 5:
        return 1 if nums[0] > nums[1] else 0
    elif id == 6:
        return 1 if nums[1] > nums[0] else 0
    elif id == 7:
        return 1 if nums[0] == nums[1] else 0

if __name__ == "__main__":
    with open('./input/16.txt') as f:
        data = f.read()
        bin_string = form_binary_string(data)
        result, _ = read_packet(bin_string, max_subpackets=1)
        print(total_version_numbers)
        print(result[0])
