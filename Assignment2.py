#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 15:35:11 2020

@author: alanhandukic, daviddarling
"""
def main():
  """ This is the main function to run our program."""
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
  
