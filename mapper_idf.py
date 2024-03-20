#!/usr/bin/env python3
import sys
import re

# Define the set of stopwords
stopwords= set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"])
# Input comes from standard input (stdin)
for line in sys.stdin:
    columns= line.strip().split(',')
    article_id= columns[0]  # Extract the ARTICLE_ID
    section_text= columns[3] if len(columns) > 3 else ""
    # Remove punctuation, considering only alphabetic characters
    words= re.findall(r'\b[a-zA-Z]+\b', section_text)
    # Iterate over words
    for word in words:
        # Convert to lower case
        word= word.lower()
        # Skip stopwords
        if word not in stopwords:
            print(f'{word}\t{article_id}')
