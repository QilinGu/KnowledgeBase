import re
import random
import pickle
from feature_functions import get_feature

# 依赖于ner_sentences，不过一般不用重新生成
'''
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
    with open('/home/ezio/filespace/data/word_list.data', 'wb') as f:
        pickle.dump([word[0] for word in word_list[:500]], f)
    return word_list
'''

# 依赖于pos_sentences，不过一般不用重新生成
def get_pos():
    pos_set = set()
    temp_i = 0
    temp_count = 0
    for i, line in enumerate(open('/home/ezio/filespace/data/pos_sentences.txt', 'r')):
        print(i, len(pos_set))
        if len(pos_set) > temp_count:
            temp_i = i
            temp_count = len(pos_set)
        if len(pos_set) == temp_count and i - temp_i > 50000:
            break
        for token in line.strip().split():
            pos_set.add(token.split('/')[1])
    pos_set.remove('')
    pos_tag_list = list(pos_set)
    pickle.dump(pos_tag_list, open('/home/ezio/filespace/data/pos_tag_list.data', 'wb'))
    return pos_tag_list

# 被sent_dict_features调用
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

# 被dump_sent_list_fea调用
def sent_dict_features(sent_dict, lino):
    pos_sent = sent_dict['pos']
    dpt_sent = sent_dict['dpt']
    pairwise_ner_sents, ne_pairs = pairwise_ner(sent_dict['ner'])
    fea_vecs = []
    for ner_sent, pair in zip(pairwise_ner_sents, ne_pairs):
        raw_fea_vec = get_feature(pos_sent, ner_sent, dpt_sent, reverse = False)
        if raw_fea_vec == []: return []
        fea_vec = [lino, pair[0], pair[1]] + raw_fea_vec
        fea_vecs.append(fea_vec)
        raw_fea_vec = get_feature(pos_sent, ner_sent, dpt_sent, reverse = True)
        if raw_fea_vec == []: return []
        fea_vec = [lino, pair[1], pair[0]] + raw_fea_vec
        fea_vecs.append(fea_vec)
    return fea_vecs

# 依赖于pos/ner/dpt_sentences.txt需要重新生成，句序号与plain_sentences.txt同步，从0开始
def dump_sent_list_fea():
    pos_file  = open('/home/ezio/filespace/data/pos_sentences.txt' , 'r', 1000)
    ner_file  = open('/home/ezio/filespace/data/ner_sentences.txt' , 'r', 1000)
    dpt_file  = open('/home/ezio/filespace/data/dpt_sentences.txt' , 'r', 1000)

    # sent_list
    sent_list = []
    lino = -1
    while True:
        lino += 1
        pos_sent = pos_file.readline().strip()
        ner_sent = ner_file.readline().strip()
        dpt_sent = dpt_file.readline().strip()
        if pos_sent == '' or ner_sent == '' or dpt_sent == '': break
        if pos_sent == "### can't get url!!!" or ner_sent == "### can't get url!!!" or dpt_sent == "### can't get url!!!": continue
        if re.search(r'\[.+?\]N[ihs].+\[.+?\]N[ihs]', ner_sent) == None: continue
        sent_list.append({'lino': lino, 'pos': pos_sent, 'ner': ner_sent, 'dpt': dpt_sent})
        print(len(sent_list))
    pickle.dump(sent_list, open('/home/ezio/filespace/data/re_sent_list.data', 'wb'))

    # all_fea_vecs
    all_fea_vecs = []
    for sent_dict in sent_list:
        lino = sent_dict['lino']
        print(lino, ' sent_dict')
        #if lino > 10000: break
        fea_vecs = sent_dict_features(sent_dict, lino)
        all_fea_vecs.extend(fea_vecs)
    pickle.dump(all_fea_vecs, open('/home/ezio/filespace/data/all_fea_vecs.data', 'wb'))

    return sent_list, all_fea_vecs

# 依赖于dump_sent_list需要重新生成，句序号与plain_sentences.txt同步，从0开始
def random_select_seed():
    sent_list = pickle.load(open('/home/ezio/filespace/data/re_sent_list.data', 'rb'))
    all_fea_vecs = pickle.load(open('/home/ezio/filespace/data/all_fea_vecs.data', 'rb'))
    exist_lino = [sample[0] for sample in all_fea_vecs]
    del all_fea_vecs
    with open('/home/ezio/filespace/data/training_seeds.txt', 'w') as f:
        for sent_dict in sent_list:
            if sent_dict['lino'] not in exist_lino: continue
            if random.randint(0, 25) == 1:
                if 'Ns' not in sent_dict['ner'] and random.randint(0, 1) != 0: continue
                f.write(str(sent_dict['lino']))
                f.write(' ' + sent_dict['ner'] + '\n')

# 依赖于re_sent_list.data需要重新生成
def boostrap_train_test_data():
    training_dict = {}
    for line in open('/home/ezio/filespace/data/training_seeds.txt'):
        splited_line = line.strip().split(' ##### ')
        assert len(splited_line) == 1 or len(splited_line) == 2
        if len(splited_line) == 2:
            lino = int(splited_line[1].split()[0])
            pair_list = [tuple(pair.split('@')) for pair in splited_line[0].split()]
            pair_set = set(pair_list)
        else:
            lino = int(splited_line[0].split()[0])
            pair_set = set()
        for pair in pair_set: assert len(pair) == 2
        training_dict[lino] = pair_set
    print('get training_dict!')

    all_fea_vecs = pickle.load(open('/home/ezio/filespace/data/all_fea_vecs.data', 'rb'))
    print('get all_fea_vecs!')

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
    return all_fea_vecs, training_dict, training_list, testing_list

if __name__ == "__main__":
    #sent_list, all_fea_vecs = dump_sent_list_fea()
    #random_select_seed()
    all_fea_vecs, training_dict, training_list, testing_list = boostrap_train_test_data()
    #pos_tag_list = get_pos()
    pass
