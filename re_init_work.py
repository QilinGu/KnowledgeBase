import sys
import random
import pickle

def random_select_seed():
    for i, line in enumerate(open('/home/ezio/filespace/data/ner_sentences.txt')):
        if random.randint(0, 1000) == 1:
            print(i + 1, end = ' ')
            print(line, end = '')
            sys.stdout.flush()

def dump_sent_list():
    pos_file  = open('/home/ezio/filespace/data/pos_sentences.txt' , 'r', 1000)
    ner_file  = open('/home/ezio/filespace/data/ner_sentences.txt' , 'r', 1000)
    dpt_file  = open('/home/ezio/filespace/data/dpt_sentences.txt' , 'r', 1000)
    dump_file = open('/home/ezio/filespace/data/re_sent_list.data', 'wb')

    sent_list = [None]
    while True:
        pos_sent = pos_file.readline()
        ner_sent = ner_file.readline()
        dpt_sent = dpt_file.readline()
        if pos_sent == '' or ner_sent == '' or dpt_sent == '': break
        sent_list.append({'pos': pos_sent, 'ner': ner_sent, 'dpt': dpt_sent})
    pickle.dump(sent_list, dump_file)
    dump_file.close()

def get_features(pos_sent, ner_sent, dpt_sent):
    no_feature = False
    if ner_sent == "### can't get url!!!": no_feature = True
    if dpt_sent == "### can't get url!!!": no_feature = True
    if re.search(r'\[.*\].*\[.*\]', ner_sent) == None: no_feature = True

