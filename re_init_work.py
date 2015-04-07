import re
import random
import pickle
#import numpy
import functools
import collections
from feature_functions import fea_funcs

def random_select_seed():
    sent_list = pickle.load(open('/home/ezio/filespace/data/re_sent_list.data', 'rb'))
    with open('/home/ezio/filespace/data/training_seeds.txt', 'w') as f:
        for i, sent_dict in enumerate(sent_list):
            if random.randint(0, 100) == 1:
                if 'Ns' not in sent_dict['ner'] and random.randint(0, 1) != 0: continue
                f.write(str(i))
                f.write(' ' + sent_dict['ner'] + '\n')

def dump_sent_list():
    pos_file  = open('/home/ezio/filespace/data/pos_sentences.txt' , 'r', 1000)
    ner_file  = open('/home/ezio/filespace/data/ner_sentences.txt' , 'r', 1000)
    dpt_file  = open('/home/ezio/filespace/data/dpt_sentences.txt' , 'r', 1000)
    dump_file = open('/home/ezio/filespace/data/re_sent_list.data', 'wb')

    sent_list = []
    while True:
        pos_sent = pos_file.readline().strip()
        ner_sent = ner_file.readline().strip()
        dpt_sent = dpt_file.readline().strip()
        if pos_sent == '' or ner_sent == '' or dpt_sent == '': break
        if pos_sent == "### can't get url!!!" or ner_sent == "### can't get url!!!" or dpt_sent == "### can't get url!!!": continue
        if re.search(r'\[.*\]N[ihs] .* \[.*\]N[ihs]', ner_sent) == None: continue
        sent_list.append({'pos': pos_sent, 'ner': ner_sent, 'dpt': dpt_sent})
    pickle.dump(sent_list, dump_file)
    dump_file.close()
    return sent_list

def pairwise_ner(ner_sent):
    pattern = '\[.*?\]N[ihs]'
    nes = re.findall(pattern, ner_sent)
    nes = [''.join(ne.split()) for ne in nes]
    sps = re.split(pattern, ner_sent)
    nes_stripped = [ne.split(']')[0].split('[')[1] for ne in nes]
    ne_count = len(nes)
    pairwise_ner_sents = []
    ne_pairs = []
    for i in range(ne_count):
        for j in range(i + 1, ne_count):
            sent = ""
            for k in range(ne_count):
                sent += sps[k]
                if k == i or k == j:
                    sent += nes[k]
                else:
                    sent += nes_stripped[k]
            sent += sps[ne_count]
            pairwise_ner_sents.append(sent)
            ne_pair = (nes_stripped[i], nes_stripped[j])
            ne_pairs.append(ne_pair)
    return pairwise_ner_sents, ne_pairs

def sent_triple_features(pos_sent, ner_sent, dpt_sent, reverse):
    fea_vec_list = [func(pos_sent, ner_sent, dpt_sent, reverse) for func in fea_funcs]
    return functools.reduce(lambda x, y: x + y, fea_vec_list)

def sent_dict_features(sent_dict, lino):
    pos_sent = sent_dict['pos']
    dpt_sent = sent_dict['dpt']
    pairwise_ner_sents, ne_pairs = pairwise_ner(sent_dict['ner'])
    fea_vecs = []
    for ner_sent, pair in zip(pairwise_ner_sents, ne_pairs):
        raw_fea_vec = sent_triple_features(pos_sent, ner_sent, dpt_sent, reverse = False)
        fea_vec = [lino, pair[0], pair[1]] + raw_fea_vec
        fea_vecs.append(fea_vec)
        raw_fea_vec = sent_triple_features(pos_sent, ner_sent, dpt_sent, reverse = True)
        fea_vec = [lino, pair[1], pair[0]] + raw_fea_vec
        fea_vecs.append(fea_vec)
    return fea_vecs

def sent_list_features(sent_list):
    all_fea_vecs = []
    for lino, sent_dict in enumerate(sent_list):
        print(lino, ' sent_dict')
        #if lino > 10000: break
        fea_vecs = sent_dict_features(sent_dict, lino)
        all_fea_vecs.extend(fea_vecs)
    return all_fea_vecs

def boostrap_init_data():
    sent_list = pickle.load(open('/home/ezio/filespace/data/re_sent_list.data', 'rb'))
    all_fea_vecs = sent_list_features(sent_list)

    print('get all_fea_vecs!')

    training_dict = {}
    for line in open('/home/ezio/filespace/data/training_seeds.txt'):
        splited_line = line.strip().split('#')
        if len(splited_line) == 2:
            lino = int(splited_line[1].split()[0])
            pair_list = [(pair.split('@')[0], pair.split('@')[1]) for pair in splited_line[0].split()]
            pair_set = set(pair_list)
        else:
            lino = int(splited_line[0].split()[0])
            pair_set = set()
        training_dict[lino] = pair_set

    print('get training_dict!')

    training_list = []
    testing_list = []
    for fea_vec in all_fea_vecs:
        lino = fea_vec[0]
        pair = (fea_vec[1], fea_vec[2])
        if lino in training_dict:
            if pair in training_dict[lino]:
                training_list.append(fea_vec + [1])
            else:
                training_list.append(fea_vec + [0])
        else:
            testing_list.append(fea_vec + [-1])

    print('get training_list testing_list!')

    pickle.dump(training_list, open('/home/ezio/filespace/data/training_list.data', 'wb'))
    pickle.dump(testing_list, open('/home/ezio/filespace/data/testing_list.data', 'wb'))
    return training_list, testing_list

training_list, testing_list = boostrap_init_data()

def get_words():
    word_dict = collections.defaultdict(lambda: 1)
    for i, line in enumerate(open('/home/ezio/filespace/data/ner_sentences.txt')):
        print(i, len(word_dict))
        if re.search(r'\[.*\]Ns .* \[.*\]Ns', line) == None: continue
        tokens = line.strip().split()
        for token in tokens:
            if len(token) > 2:
                suffix = token[-2:]
                if suffix == 'Ns' or suffix == 'Ni' or suffix == 'Nh': continue
            word_dict[token.split('/')[0]] += 1
    word_list = sorted(word_dict.items(), key = lambda x: x[1], reverse = True)
    with open('/home/ezio/filespace/data/words.data', 'wb') as f:
        pickle.dump([word[0] for word in word_list[:5000]], f)
