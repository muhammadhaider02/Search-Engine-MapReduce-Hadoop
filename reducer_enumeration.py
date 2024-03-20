#!/usr/bin/env python3
import sys

current_word= None
word_id= 0 
# Input comes from standard input (stdin)
for line in sys.stdin:
    # Parse the input we got from mapper.py
    line= line.strip()
    # Split the line into word
    try:
        word,= line.split(' ')
    except ValueError:
        continue
    # Check if this word is different from the last one processed
    if word != current_word:
        # Output the word along with its unique ID
        print(f'{word}\t{word_id}')
        word_id+= 1  # Increment word_id for the next unique word
        current_word= word  # Update current_word to the new word
# if block to cater last word
if current_word == word:
    print(f'{current_word}\t{word_id}')


