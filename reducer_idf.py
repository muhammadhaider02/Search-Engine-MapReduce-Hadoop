#!/usr/bin/env python3
import sys

current_term= None
current_docs= set()
# Input comes from standard input (stdin)
for line in sys.stdin:
    # Parse the input we got from mapper.py
    line= line.strip()
    # Split the line into term and document id
    try:
        term, document_id= line.split('\t', 1)
    except ValueError:
        continue
    # If it's a same term, add the document_id to the set
    if term == current_term:
        current_docs.add(document_id)
    else:
        # If this is a new term, and not an existing term
        if current_term is not None:
            # Print the term along with the count of unique document IDs
            print(f'{current_term}\t{len(current_docs)}')
        # Reset the document ID set with the new term's document ID
        current_term= term  
        current_docs= {document_id}  
if current_term is not None:
    print(f'{current_term}\t{len(current_docs)}')
