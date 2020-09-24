import math

prime_list = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,
              139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,
              281,283,293,307,311] # a list of the first 64 prime numbers

NUM_BITS = 16 # Constant number of bits that we want

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
  new_string = [] # we will hold the final values here
  user_string = input("Enter a string: ")
  user_string = [letter for letter in user_string] # split the user's input into separate characters in a list

  for index, letter in enumerate(user_string):
    ascii_val = ord(letter)
    ascii_val = bin(ascii_val)[2:]
    new_string.append(ascii_val)
    binary_val = ''.join(new_string)

  return binary_val

def pad_message(user_string):
  user_string = str(user_string) # first concatenate a 1 to the message
  user_string += '1'

  while len(user_string) <= 512: # add 448 0s to the message until we have a length of 512
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
  
def sigma0(curr_word):
    word_val = int(curr_word, 2) # This will conver binary string into number
    temp1 = right_rotate(word_val, 7, NUM_BITS)
    temp2 = right_rotate(word_val, 14, NUM_BITS) # Should be 18 however we are using 16 bit words
    temp3 = word_val >> 3   # Shift word_val to the right 3 
    temp1 = temp1 ^ temp2 # XOR temp1 with temp2
    temp1 = temp1 ^ temp3 # XOR new temp1 with temp3
    
    bin_num = bin(temp1)[2:]
    
    if len(bin_num) < NUM_BITS:
        temp_str = '0' * (NUM_BITS - len(bin_num))
        temp_str += bin_num
            
    return temp_str

def sigma1(curr_word):
    word_val = int(curr_word, 2)
    temp1 = right_rotate(word_val, 13, NUM_BITS) # Should be 17 however we are using 16 bit words
    temp2 = right_rotate(word_val, 15, NUM_BITS) # Should be 19 however we are using 16 bit words
    temp3 = word_val >> 10   # Shift word_val to the right 3 
    temp1 = temp1 ^ temp2 # XOR temp1 with temp2
    temp1 = temp1 ^ temp3 # XOR new temp1 with temp3
    
    bin_num = bin(temp1)[2:]
    if len(bin_num) < NUM_BITS:
        temp_str = '0' * (NUM_BITS - len(bin_num))
        temp_str += bin_num
            
    return temp_str

def main():
  """This is the main function to run our program."""
  constants_list = process_primes(prime_list) # This list will hold our constants that we calculate at the beginning

  user_string = parse_user_input() # This list will hold the user string's characters, in ASCII, in binary
  len_message_in_binary = len(str(user_string))
  padded_string = pad_message(user_string)
  divided_string = split_block(padded_string)
  #print(len(divided_string)) # the list should have 32 elements each 16 bits long

    # This list will hold registers a-h for the scheduling portion
    #   of the algorithm
   # schedule = []
    # This list will hold the newly calculated a-h that we will add
    #   add to the old schedule
   # schedule_new = []
    # Temp 1 variable to hold the result of the temp 1 calculation
   # t1 = 0
    # Temp 2 variable
   # t2 = 0
    # List to hold the output from our encryption algorithm
   # encrypt_result = []

if __name__ == "__main__":
  main()
