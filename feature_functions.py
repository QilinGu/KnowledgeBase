import re
import pickle
import functools

def ne_type(pos_sent, ner_sent, dpt_sent, reverse):
    ne_types = re.findall(r'\[.+?\](N[ihs])', ner_sent)
    if len(ne_types) != 2: print(ner_sent)
    assert len(ne_types) == 2
    if reverse == False: i = 0; j = 1
    else: i = 1; j = 0
    fea_vec = []
    if ne_types[i] == 'Nh': fea_vec.append(0)
    if ne_types[i] == 'Ni': fea_vec.append(1)
    if ne_types[i] == 'Ns': fea_vec.append(2)
    if ne_types[j] == 'Nh': fea_vec.append(0)
    if ne_types[j] == 'Ni': fea_vec.append(1)
    if ne_types[j] == 'Ns': fea_vec.append(2)
    return fea_vec

def has_word(pos_sent, ner_sent, dpt_sent, reverse):
    if not hasattr(has_word, 'words'):
        has_word.words = pickle.load(open('/home/ezio/filespace/data/words.data', 'rb'))
    fea_vec = []

    # 切分
    fix_list = re.split(r'\[.+?\]N[ihs]', ner)
    assert len(fix_list) == 3
    prefix = fix_list[0]
    infix = fix_list[1]
    suffix = fix_list[2]

    fea_vec.append(len(prefix)) # 前缀长度
    fea_vec.append(len(infix))  # 中缀长度
    fea_vec.append(len(suffix)) # 后缀长度
    for word in has_word.words:
        if word in prefix: fea_vec.append(1)
        else: fea_vec.append(0)
        if word in infix: fea_vec.append(1)
        else: fea_vec.append(0)
        if word in suffix: fea_vec.append(1)
        else: fea_vec.append(0)

    return fea_vec

def pos_feature(pos_sent, ner_sent, dpt_sent, reverse):
    fix_list = re.split(r'\[.+?\]N[ihs]', ner)
    ner_prefix = "".join(fix_list[0].split())
    pre_token = ""
    for token in pos_sent.split():
        if

fea_funcs = [ne_type, has_word,]

pos = '其/r 基本概念/l 的/uj 精煉/v 早在/t 古埃及/ns 、/x 美索不达米亚/ns 及/c 印度/ns 历史/n 內/f 的/uj 古代/t 數學/n 文本/n 便/d 可/v 觀見/v 。/x '
ner = '其 基本 概念 的 精煉 早 在 古 [埃及]Ns 、 [美索不达米亚]Ns 及 印度 历史內 的 古代 數學 文本 便 可 觀見 。'
dpt = '其_0 概念_2 ATT基本_1 概念_2 ATT概念_2 精煉_4 ATT的_3 概念_2 RAD精煉_4 觀見_20 SBV早_5 觀見_20 ADV在_6 觀見_20 ADV古_7 埃及_8 ATT埃及_8 历史內_13 ATT、_9 美索不达米亚_10 WP美索不达米亚_10 埃及_8 COO及_11 印度_12 LAD印度_12 埃及_8 COO历史內_13 在_6 POB的_14 在_6 RAD古代_15 數學_16 ATT數學_16 文本_17 ATT文本_17 觀見_20 FOB便_18 觀見_20 ADV可_19 觀見_20 ADV觀見_20 -1 HED。_21 觀見_20 WP'

fea_vec1 = functools.reduce(lambda x, y: x + y, [f(pos, ner, dpt, False) for f in fea_funcs])
fea_vec2 = functools.reduce(lambda x, y: x + y, [f(pos, ner, dpt, True) for f in fea_funcs])
