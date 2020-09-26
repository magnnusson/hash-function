#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 15:35:11 2020

@author: alanhandukic, daviddarling
"""

import math
from collections import deque
import random

prime_list = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,
              139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,
              281,283,293,307,311] # a list of the first 64 prime numbers

# Constant number of bits that we want
NUM_BITS = 16

def process_primes(prime_list):
  cube_roots = [] #this will hold our cube roots
  constants = []
  for index, prime in enumerate(prime_list):
    prime = prime**(1/3)
    cube_roots.append(prime) # calculate and hold all cube roots in another list

  for index, cubes in enumerate(cube_roots):
    cubes = math.modf(cubes) # use modf to get the fractional part of the cube root
    fraction = cubes[0]
    fraction = fraction * (2**16) # multiply the fractional part by 2^16, truncate, and then convert to binary
    fraction = int(fraction)
    fraction = bin(fraction)[2:]
    constants.append(fraction) # we have our list of constants

  return constants

def parse_user_input():
  new_string = [] # we will hold the final values here and return the list
  user_string = input("Enter a string: ")
  user_string = [letter for letter in user_string] # split the user's input into separate characters in a list

  for index, letter in enumerate(user_string):
    ascii_val = ord(letter)
    ascii_val = bin(ascii_val)[2:]
    new_string.append(ascii_val)

  return new_string

def pad_message(user_string):
  user_string = str(user_string) # first concatenate a 1 to the message
  user_string += '1'

  while len(user_string) <= 447: # add 0s to the message until we have a length of 448
    user_string += '0'

  padded_string = int(user_string) # return the padded string
  return padded_string

def split_block(msg_block):
    divided_list = []
    curr_string = ''
    for i, num in enumerate(str(msg_block)):
        if i < 16:
            curr_string += (str(num))
        elif i % 16 == 0:
            divided_list.append(curr_string)
            curr_string = ''
            curr_string += (str(num))
        else:
            curr_string += (str(num))
    return divided_list

def right_rotate(num, rot, num_bit):
    return (num >> rot)|(num << (num_bit - rot)) & 0xFFFF

def create_message_schedule(divided_string):
  while len(divided_string) <= 63: # stop once we reach 64 words
    length_of_string = len(divided_string) # updating the value of the length
    val1 = sigma1(divided_string[length_of_string-2]) # first we perform an upper-case sigma 1 rotation to this element
    val2 = divided_string[length_of_string-7] # we just retrieve this element
    val3 = sigma0(divided_string[length_of_string-31]) # we perform a lower-case sigma 0 rotation to this element
    val4 = divided_string[length_of_string-32] # we just retrieve this element

    sum = int(val1, 2) + int(val2, 2) + int(val3, 2) + int(val4, 2) # add the binary numbers together
    bin_sum = bin(sum)[2:]
    if len(bin_sum) > NUM_BITS:
      bin_sum = bin_sum[len(bin_sum) - NUM_BITS:] # truncate to 16 bits if needed


    divided_string.append(bin_sum) # append the binary sum to the end of the list

  return divided_string

def intialize_state_registers():
    state_registers = []
    square_roots = []
    for index, prime in enumerate(prime_list):
        if index <= 7:  # we only want the first 8 primes
            prime = math.sqrt(prime)
            square_roots.append(prime)

    for index, square in enumerate(square_roots):
        fraction = math.modf(square)  # use modf to get the irrational part of the number
        fraction = fraction[0]
        fraction = fraction * (2 ** 16)  # multiply the fractional part by 2^16, truncate, and then convert to binary
        fraction = int(fraction)
        fraction = bin(fraction)[2:]
        if len(fraction) > NUM_BITS:
          fraction = fraction[len(fraction) - NUM_BITS:]  # truncate to 16 bits if needed
        elif len(fraction) < NUM_BITS:
          new_sum = '0' * (NUM_BITS - len(fraction))  # add more bits to equal 16 if needed
          new_sum += fraction
          fraction = new_sum
        state_registers.append(fraction)  # we have our 8 state registers with initial hash values

    return state_registers

def choice(e, f, g):
    temp_list = []
    temp_str = ''
    which_index = 0
    
    for index in range(0, len(e)):
        temp_list.append(e[index])
        temp_list.append(f[index])
        temp_list.append(g[index])
        which_index = random.randrange(0,3) # Generate a random number between 0-2
        temp_str += temp_list[which_index]
        temp_list.clear()
    return temp_str

def majority(a, b, c):
    temp_list = []
    temp_str = ''
    
    for index in range(0, len(a)):
        temp_list.append(a[index])
        temp_list.append(b[index])
        temp_list.append(c[index])
        temp_str += max(set(temp_list), key = temp_list.count)
        temp_list.clear()
    return temp_str

def sigma0(curr_word):
    word_val = int(curr_word, 2) # This will conver binary string into number
    temp1 = right_rotate(word_val, 7, NUM_BITS)
    temp2 = right_rotate(word_val, 11, NUM_BITS) # Should be 18 however we are using 16 bit words
    temp3 = word_val >> 3   # Shift word_val to the right 3 
    temp1 = temp1 ^ temp2 # XOR temp1 with temp2
    temp1 = temp1 ^ temp3 # XOR new temp1 with temp3
    
    bin_num = bin(temp1)[2:]
    
    if len(bin_num) < NUM_BITS:
        temp_str = '0' * (NUM_BITS - len(bin_num))
        temp_str += bin_num
        return temp_str
    else:
        return bin_num

def sigma1(curr_word):
    word_val = int(curr_word, 2)
    temp1 = right_rotate(word_val, 10, NUM_BITS) # Should be 17 however we are using 16 bit words
    temp2 = right_rotate(word_val, 12, NUM_BITS) # Should be 19 however we are using 16 bit words
    temp3 = word_val >> 10   # Shift word_val to the right 3 
    temp1 = temp1 ^ temp2 # XOR temp1 with temp2
    temp1 = temp1 ^ temp3 # XOR new temp1 with temp3
    
    bin_num = bin(temp1)[2:]
    if len(bin_num) < NUM_BITS:
        temp_str = '0' * (NUM_BITS - len(bin_num))
        temp_str += bin_num
        return temp_str
    else:
        return bin_num

def upper_sigma0(curr_word):
    word_val = int(curr_word, 2)
    temp1 = right_rotate(word_val, 2, NUM_BITS) 
    temp2 = right_rotate(word_val, 13, NUM_BITS) 
    temp3 = right_rotate(word_val, 14, NUM_BITS) # Should be 22 however we are using 16 bit words
    temp1 = temp1 ^ temp2 # XOR temp1 with temp2
    temp1 = temp1 ^ temp3 # XOR new temp1 with temp3
    
    bin_num = bin(temp1)[2:]
    if len(bin_num) < NUM_BITS:
        temp_str = '0' * (NUM_BITS - len(bin_num))
        temp_str += bin_num
        return temp_str
    else:
        return bin_num

def upper_sigma1(curr_word):
    word_val = int(curr_word, 2)
    temp1 = right_rotate(word_val, 6, NUM_BITS) 
    temp2 = right_rotate(word_val, 11, NUM_BITS) 
    temp3 = right_rotate(word_val, 15, NUM_BITS) # Should be 25 however we are using 16 bit words 
    temp1 = temp1 ^ temp2 # XOR temp1 with temp2
    temp1 = temp1 ^ temp3 # XOR new temp1 with temp3
    
    bin_num = bin(temp1)[2:]
    if len(bin_num) < NUM_BITS:
        temp_str = '0' * (NUM_BITS - len(bin_num))
        temp_str += bin_num
        return temp_str
    else:
        return bin_num

def compression(message_schedule, constants_list, state_registers):
    original_state_registers = state_registers # perserve original values of hashes
    for word, constant in zip(message_schedule, constants_list):  # parallel iteration of the schedule and constants
      val1 = upper_sigma1(state_registers[4])  # take the uppercase sigma 1 rotation of register 'e', index 4
      val2 = choice(state_registers[4], state_registers[5], state_registers[6])  # choosing 1 or 0 from either of these registers to create the value
      val3 = state_registers[7]  # the 'h' register value
      val4 = constant  # the current constant value
      val5 = word  # the current word value from the schedule

      sum1 = int(val1, 2) + int(val2, 2) + int(val3, 2) + int(val4, 2) + int(val5, 2) # add the binary numbers together
      temp_word_1 = bin(sum1)[2:]
      if len(temp_word_1) > NUM_BITS:
        temp_word_1 = temp_word_1[len(temp_word_1) - NUM_BITS:]  # truncate to 16 bits if needed
      elif len(temp_word_1) < NUM_BITS:
        new_sum = '0' * (NUM_BITS - len(temp_word_1))  # add more bits to equal 16 if needed
        new_sum += temp_word_1
        temp_word_1 = new_sum

      val6 = upper_sigma0(state_registers[0])  # take the uppercase sigma 0 rotation of register 'a', index 0
      val7 = majority(state_registers[0], state_registers[1], state_registers[2])  # find max value between registers a, b, c

      sum2 = int(val6, 2) + int(val7, 2)  # add the binary numbers together
      temp_word_2 = bin(sum2)[2:]
      if len(temp_word_2) > NUM_BITS:
        temp_word_2 = temp_word_2[len(temp_word_2) - NUM_BITS:]  # truncate to 16 bits if needed
      elif len(temp_word_2) < NUM_BITS:
        new_sum = '0' * (NUM_BITS - len(temp_word_2))  # add more bits to equal 16 if needed
        new_sum += temp_word_2
        temp_word_2 = new_sum

      temp_word_sum = int(temp_word_1, 2) + int(temp_word_2, 2) # add the temp words together
      temp_word_sum = bin(temp_word_sum)[2:]
      if len(temp_word_sum) > NUM_BITS:
        temp_word_sum = temp_word_sum[len(temp_word_sum) - NUM_BITS:]  # truncate to 16 bits if needed
      elif len(temp_word_sum) < NUM_BITS:
        new_sum = '0' * (NUM_BITS - len(temp_word_sum))  # add more bits to equal 16 if needed
        new_sum += temp_word_sum
        temp_word_sum = new_sum

      state_registers = deque(state_registers)
      state_registers.rotate(1) # we now shift the registers down once
      state_registers[0] = temp_word_sum # register 'a' becomes our temp_word_sum
      state_registers[4] = int(state_registers[4], 2) + int(temp_word_1, 2) # add temp_word_1 to register 'e'
      state_registers[4] = bin(state_registers[4])[2:]
      if len(state_registers[4]) > NUM_BITS:
        state_registers[4] = state_registers[4][len(state_registers[4]) - NUM_BITS:]  # truncate to 16 bits if needed
      elif len(state_registers[4]) < NUM_BITS:
        new_sum = '0' * (NUM_BITS - len(state_registers[4]))  # add more bits to equal 16 if needed
        new_sum += state_registers[4]
        state_registers[4] = new_sum
                             # we repeat this process until all 64 words and constants have been iterated and compressed

    for index, value in enumerate(state_registers): # finally, add the final hash values to the original hash values
      new_val = int(value, 2) + int(original_state_registers[index], 2)
      new_val = bin(new_val)[2:]
      if len(new_val) > NUM_BITS:
        new_val = new_val[len(new_val) - NUM_BITS:]  # truncate to 16 bits if needed
      elif len(new_val) < NUM_BITS:
        new_sum = '0' * (NUM_BITS - len(new_val))  # add more bits to equal 16 if needed
        new_sum += new_val
        new_val = new_sum
      state_registers[index] = new_val
    state_registers = list(state_registers)

    return state_registers

def main():
    # This list will hold our constants that we calculate at the beginning
    constants_list = []
    # This list will hold the user string
    user_string = []
    # This list will hold registers a-h for the scheduling portion 
    #   of the algorithm
    schedule = []
    # This list will hold the newly calculated a-h that we will add 
    #   add to the old schedule
    schedule_new = []
    # Temp 1 variable to hold the result of the temp 1 calculation
    t1 = 0
    # Temp 2 variable
    t2 = 0
    # List to hold the output from our encryption algorithm
    encrypt_result = []
    
    constants_list = process_primes(prime_list) # This list will hold our constants that we calculate at the beginning
    
    user_string = parse_user_input() # This list will hold the user string's characters, in ASCII, in binary

    len_message_in_binary = len(str(user_string))
    user_string[0] = " ".join(user_string)
    user_string[0] = user_string[0].replace(" ", "")
    user_string = user_string[0]
    padded_string = pad_message(user_string)
    
    divided_string = split_block(padded_string)
    message_schedule = create_message_schedule(divided_string)
    print(message_schedule)
    state_registers = intialize_state_registers() # we'll now need the state registers intialized using the prime numbers
    
    tmp_str = majority(divided_string[0], divided_string[1], divided_string[2])
    
    compression(message_schedule, constants_list, state_registers) # compress the words of the schedule into the registers
    
    # divided_list = split_block(padded_string)
    
    # upper_sigma0(divided_list[0])
    
    # msg_block = []
    
    # for i in range(513):
    #     if i % 2 == 0:
    #         msg_block.append('1')
    #     else:
    #         msg_block.append('0')
    
    # msg_block[0] = "".join(msg_block)
    
    print("hi")
        
if __name__ == "__main__":
    main()