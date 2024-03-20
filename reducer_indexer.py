#!/usr/bin/env python3
import sys
import math
# this function loads vocabulary
def load_vocabulary(vocabulary_path):
    vocabulary= {}
    with open(vocabulary_path, 'r') as file:
        for line in file:
            parts= line.strip().split('\t')
            if len(parts) == 2:  
                unique_id, document_count= parts
                vocabulary[unique_id]= {'DocumentCount': document_count}
    return vocabulary
vocabulary= load_vocabulary('vocab_out.txt')
# this function parses mapper output
def read_mapper_output(file, separator= '\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator= '\t'):
    term_frequencies= {}
    # Process each line output by the mapper
    data= read_mapper_output(sys.stdin, separator=separator)
    for term_article, tf in data:
        term_id, article_id= term_article.split(',')
        tf= float(tf)
        # if term_id is not in dict
        if term_id not in term_frequencies:
            term_frequencies[term_id]= {}
        if article_id not in term_frequencies[term_id]:
            # compute tf if article_id is in dict
            term_frequencies[term_id][article_id]= 0
        term_frequencies[term_id][article_id]+= tf
    total_documents= sum(vocabulary.values())
    # Calculate TF-IDF using the document count from vocabulary
    for term_id, articles in term_frequencies.items():
        df= vocabulary.get(term_id, 0)
        idf= math.log((total_documents / (1 + df)) + 1)
        for article_id, tf in articles.items():
            tf_idf= tf * idf
            print(f'{article_id}{separator}{tf_idf}')
if __name__ == "__main__":
    main()
