def load_reducer_output(file_path):
    out_data= {}
    with open(file_path, 'r') as out_file:
        for line in out_file:
            parts= line.strip().split('\t')
            if len(parts) == 2:
                out_data[parts[0]]= parts[1]
    return out_data
word_enumeration= load_reducer_output('en_out.txt')
document_count= load_reducer_output('idf_out.txt')
# merging into a single structure
vocabulary= {}
for word, unique_id in word_enumeration.items():
    document_count_value= document_count.get(word, 0)  
    vocabulary[word]= {'ID': unique_id, 'DocumentCount': document_count_value}
# this output gets saved in local directory
for word, info in list(vocabulary.items()): 
    print(f'ID: {info["ID"]}, Document Count: {info["DocumentCount"]}')
