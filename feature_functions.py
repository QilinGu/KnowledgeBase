import re
import pickle

'''
pos_sent = '其_r 基本_a 概念_n 的_u 精煉_n 早_a 在_p 古_a 埃及_ns 、_wp 美索不达米亚_ns 及_c 印度_ns 历史內_n 的_u 古代_nt 數學_n 文本_n 便_d 可_v 觀見_v 。_wp'
ner_sent = '其 基本 概念 的 精煉 早 在 古 [埃及]Ns 、 [美索不达米亚]Ns 及 印度 历史內 的 古代 數學 文本 便 可 觀見 。'
dpt_sent = '其_0 概念_2 ATT###基本_1 概念_2 ATT###概念_2 精煉_4 ATT###的_3 概念_2 RAD###精煉_4 觀見_20 SBV###早_5 觀見_20 ADV###在_6 觀見_20 ADV###古_7 埃及_8 ATT###埃及_8 历史內_13 ATT###、_9 美索不达米亚_10 WP###美索不达米亚_10 埃及_8 COO###及_11 印度_12 LAD###印度_12 埃及_8 COO###历史內_13 在_6 POB###的_14 在_6 RAD###古代_15 數學_16 ATT###數學_16 文本_17 ATT###文本_17 觀見_20 FOB###便_18 觀見_20 ADV###可_19 觀見_20 ADV###觀見_20 -1 HED###。_21 觀見_20 WP'
'''

pos_sent = '許多_nh 數_nh 學_nh 家_n 認為_v 稱_v 他們_r 的_u 工作_v 是_v 一_m 種_q 科學_n ，_wp 是_v 低估_v 了_u 其_r 美學_n 方面_n 的_u 重要性_n ，_wp 以及_c 其_r 做為_v 七大_j 博雅_a 教育_v 之一_r 的_u 歷史_n ；_wp###另外_c 亦_d 有_v 人_n 認為_n 若_c 忽略_v 其_r 與科學_n 之_u 間_n 的_u 關聯_n ，_wp 是_v 假_a 裝沒_n 看到_v 數學_n 和_c 其_r 在_p 科學_n 與_v 工程学_n 之_u 間_n 的_u 交界_v 導致_v 了_u 許多_nh 在_p 數學_n 上_nd 的_u 發展_v 此_r 一_m 事實_n 。_wp'
ner_sent = '許多 數 [學]Nh 家 認為 稱 他們 的 工作 是 一 種 科學 ， 是 低估 了 其 美學 方面 的 重要性 ， 以及 其 做為 七大 博雅 教育 之一 的 歷史 ；###另外 亦 有 人 認為 若 忽略 其 與科學 之 間 的 關聯 ， 是 假 裝沒 看到 數學 和 其 在 科學 與 工程学 之 間 的 交界 導致 了 [許多]Nh 在 數學 上 的 發展 此 一 事實 。'
dpt_sent = '許多_0 家_3 ATT###數_1 許多_0 COO###學_2 家_3 ATT###家_3 工作_8 SBV###認為_4 工作_8 ADV###稱_5 認為_4 COO###他們_6 工作_8 ATT###的_7 他們_6 RAD###工作_8 是_9 SBV###是_9 -1 HED###一_10 種_11 ATT###種_11 科學_12 ATT###科學_12 是_9 VOB###，_13 是_9 WP###是_14 是_9 COO###低估_15 是_14 VOB###了_16 低估_15 RAD###其_17 重要性_21 ATT###美學_18 方面_19 ATT###方面_19 重要性_21 ATT###的_20 方面_19 RAD###重要性_21 低估_15 VOB###，_22 是_9 WP###以及_23 做為_25 LAD###其_24 做為_25 SBV###做為_25 是_9 COO###七大_26 教育_28 SBV###博雅_27 教育_28 ATT###教育_28 之一_29 ATT###之一_29 歷史_31 ATT###的_30 之一_29 RAD###歷史_31 做為_25 VOB###；_32 是_9 WP######另外_0 有_2 ADV###亦_1 有_2 ADV###有_2 -1 HED###人_3 認為_4 ATT###認為_4 有_2 VOB###若_5 忽略_6 ADV###忽略_6 有_2 COO###其_7 與科學_8 ATT###與科學_8 間_10 ATT###之_9 與科學_8 RAD###間_10 關聯_12 ATT###的_11 間_10 RAD###關聯_12 忽略_6 VOB###，_13 有_2 WP###是_14 看到_17 ADV###假_15 是_14 VOB###裝沒_16 看到_17 SBV###看到_17 有_2 COO###數學_18 間_26 ATT###和_19 工程学_24 LAD###其_20 工程学_24 ATT###在_21 與_23 ADV###科學_22 在_21 POB###與_23 工程学_24 ATT###工程学_24 數學_18 COO###之_25 數學_18 RAD###間_26 交界_28 ATT###的_27 間_26 RAD###交界_28 看到_17 VOB###導致_29 交界_28 COO###了_30 交界_28 RAD###許多_31 發展_36 SBV###在_32 發展_36 ADV###數學_33 上_34 ATT###上_34 在_32 POB###的_35 在_32 RAD###發展_36 事實_39 ATT###此_37 一_38 ATT###一_38 事實_39 ATT###事實_39 交界_28 VOB###。_40 有_2 WP'

class BinaryFeatureFunction:
    def __init__(self, candidate_list):
        self.candidate_list = sorted(candidate_list)
        self.length = len(candidate_list)
    def linear_search(self, target, index):
        while index < self.length:
            if target in list(self.candidate_list[index]):
                return index
        return -1
    def __call__(self, target_list):
        if type(target_list) != list: target_list = [target_list]
        feature = [0] * self.length
        start_index = 0
        for target in sorted(target_list):
            start_index = self.linear_search(target, start_index)
            if start_index == -1: break
            else: feature[start_index] = 1
        return feature
ne_type_list    = ['Nh', 'Ni', 'Ns']
pos_tag_list    = pickle.load(open('/home/ezio/filespace/data/pos_tag_list.data', 'rb'))
word_list       = []
dependency_list = ['WP', 'SBV', 'VOB', 'IOB', 'FOB', 'DBL', 'ATT', 'ADV', 'CMP', 'COO', 'POB', 'LAD', 'RAD', 'IS ', 'HED',]
ne_type_feature    = BinaryFeatureFunction(ne_type_list)
pos_feature        = BinaryFeatureFunction(pos_tag_list)
word_feature       = BinaryFeatureFunction(word_list)
dependency_feature = BinaryFeatureFunction(dependency_list)

def get_feature(pos_sent, ner_sent, dpt_sent, reverse):
    #print(pos_sent)
    #print(ner_sent)
    #print(dpt_sent)
    fea_vec = [1 if reverse else 0]

    #------------------拆分三个句子------------------
    pos_sent = ' '.join(pos_sent.split('###'))
    pos_list = [token.split('_') for token in pos_sent.split(' ')]
    ner_sent = ' '.join(ner_sent.split('###'))
    ner_list = ner_sent.split(' ')
    dpt_list = [dp.split(' ') for dp in dpt_sent.split('###') if dp != '']
    for dp in dpt_list:
        try: assert len(dp) == 3
        except: return []
        dp[0] = dp[0].split('_')
        if dp[1] == '-1': dp[1] = ['', '-1']
        else: dp[1] = dp[1].split('_')
        try: assert len(dp[0]) == len(dp[1]) == 2
        except: return []
        dp[0][1] = int(dp[0][1])
        dp[1][1] = int(dp[1][1])
    try:
        assert len(pos_list) == len(ner_list)
        assert len(pos_list ) == max([dp[0][1] for dp in dpt_list]) + 1
        for token in pos_list:
            assert len(token) == 2
        for dp in dpt_list:
            assert len(dp) == 3
            assert len(dp[0]) == 2
            assert len(dp[1]) == 2
            assert type(dp[2]) == str
    except:
        return []

    #------------------定位两个实体------------------#
    ne1 = ne2 = ""
    ne1_type = ne2_type = ""
    ne1_index = ne2_index = -1
    for i, item in enumerate(ner_list):
        match = re.search(r'\[(.+?)\](N[ihs])', item)
        if match != None:
            if ne1 == "":
                ne1 = match.group(1)
                ne1_type = match.group(2)
                ne1_index = i
            elif ne2 == "":
                ne2 = match.group(1)
                ne2_type = match.group(2)
                ne2_index = i
            else:
                raise Exception() # 找到不止两个实体那就大有问题

    #------------------实体类型作为特征------------------#
    fea_vec.extend(ne_type_feature(ne1_type))
    fea_vec.extend(ne_type_feature(ne2_type))

    #------------------前中后缀长度作为特征------------------#
    fea_vec.append(ne1_index) # 前缀长度
    fea_vec.append(ne2_index - ne1_index)  # 中缀长度
    fea_vec.append(len(ner_list) - 1 - ne2_index) # 后缀长度

    #------------------前中后缀词和词性作为特征------------------#
    #fea_vec.extend(word_feature([token[0] for token in pos_list[0:ne1_index]]))
    #fea_vec.extend(word_feature([token[0] for token in pos_list[ne1_index + 1: ne2_index]]))
    #fea_vec.extend(word_feature([token[0] for token in pos_list[ne2_index + 1:]]))
    fea_vec.extend(pos_feature([token[1] for token in pos_list[0:ne1_index]]))
    fea_vec.extend(pos_feature([token[1] for token in pos_list[ne1_index + 1: ne2_index]]))
    fea_vec.extend(pos_feature([token[1] for token in pos_list[ne2_index + 1:]]))

    #------------------实体前后临接词和词性作为特征------------------#
    token_before_ne1 = pos_list[ne1_index - 1] if ne1_index > 0 else ['', '']
    token_after_ne1  = pos_list[ne1_index + 1]
    token_before_ne2 = pos_list[ne2_index - 1]
    token_after_ne2  = pos_list[ne2_index + 1] if ne2_index < len(ner_list) - 1 else ['', '']
    #fea_vec.extend(word_feature(token_before_ne1[0]))
    #fea_vec.extend(word_feature(token_after_ne1[0]))
    #fea_vec.extend(word_feature(token_before_ne2[0]))
    #fea_vec.extend(word_feature(token_after_ne2[0]))
    fea_vec.extend(pos_feature(token_before_ne1[1]))
    fea_vec.extend(pos_feature(token_after_ne1[1]))
    fea_vec.extend(pos_feature(token_before_ne2[1]))
    fea_vec.extend(pos_feature(token_after_ne2[1]))

    #------------------句法依存对象作为特征------------------#
    ne1_dp_feature_dict = {}
    ne2_dp_feature_dict = {}
    for dependency in dependency_list:
        ne1_dp_feature_dict[dependency] = pos_feature([])
        ne1_dp_feature_dict[dependency].extend(word_feature([]))
        ne2_dp_feature_dict[dependency] = pos_feature([])
        ne2_dp_feature_dict[dependency].extend(word_feature([]))
    for dp in dpt_list:
        dependency = dp[2]
        if dp[1][0] == ne1 and dp[1][1] == ne1_index:
            [dp_word, dp_pos] = pos_list[dp[0][1]]
            ne1_dp_feature_dict[dependency] = pos_feature(dp_pos)
            #ne1_dp_feature_dict[dependency].extend(word_feature(dp_word))
        if dp[1][0] == ne2 and dp[1][1] == ne2_index:
            [dp_word, dp_pos] = pos_list[dp[0][1]]
            ne2_dp_feature_dict[dependency] = pos_feature(dp_pos)
            #ne2_dp_feature_dict[dependency].extend(word_feature(dp_word))
    for dependency in dependency_list:
        fea_vec.extend(ne1_dp_feature_dict[dependency])
        fea_vec.extend(ne2_dp_feature_dict[dependency])

    #------------------返回------------------#
    return fea_vec

fea_vec = get_feature(pos_sent, ner_sent, dpt_sent, True)
