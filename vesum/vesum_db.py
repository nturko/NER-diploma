from pymongo import MongoClient 
# from string import whitespace

client= MongoClient('localhost:27017')
db = client["NER-uk"]
collection = db["vesum"]

# text = open("dict_corp_vis.txt", 'r').readlines()
# norm_form = ''
# for line in text:
#     line = line.replace('\n', '')
#     if line[0] not in whitespace:
#         word_entity_arr = line.split(' ')
#         norm_form = word_entity_arr[0]
#     else:
#         line = line.strip()
#         word_entity_arr = line.split(' ')

#     word_entity = {
#         'word': word_entity_arr[0],
#         'normForm': norm_form,
#         'tags': word_entity_arr[1].split(':')
#         }
#     collection.insert_one(word_entity)

def find_by_word(word):
    return collection.find({'word': word})