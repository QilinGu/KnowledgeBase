from collections import defaultdict
import re

entity_dict = defaultdict(lambda: 0)
entity_re = re.compile(r'\[(.+?)\](N[ihs])')
for line in open('/Users/warbean/filespace/data/ner_sentences.txt'):
    entity_list = entity_re.findall(line.strip())
    for entity in entity_list:
        entity_dict[entity] += 1
entity_list = [[key[0], key[1], value] for key, value in entity_dict.items()]
entity_list.sort(key = lambda x: x[2], reverse = True)
entity_type_dict = defaultdict(lambda: 0)
for entity in entity_list:
    entity_type_dict[entity[1]] += 1
