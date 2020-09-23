import math

prime_list = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,
              139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,
              281,283,293,307,311] # a list of the first 64 prime numbers

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

def right_rotate(num, rot, num_bit):
    return (num >> rot)|(num << (num_bit - rot)) & 0xFFFF

def main():
  """This is the main function to run our program."""
  # Constant number of bits that we want
  NUM_BITS = 16
  constants_list = process_primes(prime_list) # This list will hold our constants that we calculate at the beginning
  
  user_string = parse_user_input() # This list will hold the user string's characters, in ASCII, in binary
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

if __name__ == "__main__":
  main()


