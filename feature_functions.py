import re
import pickle

'''
pos_sent = '其_r 基本_a 概念_n 的_u 精煉_n 早_a 在_p 古_a 埃及_ns 、_wp 美索不达米亚_ns 及_c 印度_ns 历史內_n 的_u 古代_nt 數學_n 文本_n 便_d 可_v 觀見_v 。_wp'
ner_sent = '其 基本 概念 的 精煉 早 在 古 [埃及]Ns 、 [美索不达米亚]Ns 及 印度 历史內 的 古代 數學 文本 便 可 觀見 。'
dpt_sent = '其_0 概念_2 ATT###基本_1 概念_2 ATT###概念_2 精煉_4 ATT###的_3 概念_2 RAD###精煉_4 觀見_20 SBV###早_5 觀見_20 ADV###在_6 觀見_20 ADV###古_7 埃及_8 ATT###埃及_8 历史內_13 ATT###、_9 美索不达米亚_10 WP###美索不达米亚_10 埃及_8 COO###及_11 印度_12 LAD###印度_12 埃及_8 COO###历史內_13 在_6 POB###的_14 在_6 RAD###古代_15 數學_16 ATT###數學_16 文本_17 ATT###文本_17 觀見_20 FOB###便_18 觀見_20 ADV###可_19 觀見_20 ADV###觀見_20 -1 HED###。_21 觀見_20 WP'
'''

pos_sent = '艾萨克·牛顿_nh 和_c 戈特弗里德·威廉·莱布尼茨_nh 是_v 微积分学_n 的_u 發明者_n ，_wp 費曼_nh 發明_v 了_u 路_n 徑積_v 分_v 表述_v ，_wp 來_v 用_p 於_n 推理_v 及_c 物理_n 的_u 洞察_v ，_wp 而_c 今日_nt 的_u 弦理論_n 亦_d 生成為_v 新_a 的_u 數學_n 。_wp'
ner_sent = '[艾萨克·牛顿]Nh 和 [戈特弗里德·威廉·莱布尼茨]Nh 是 微积分学 的 發明者 ， [費曼]Nh 發明 了 路 徑積 分 表述 ， 來 用 於 推理 及 物理 的 洞察 ， 而 今日 的 弦理論 亦 生成為 新 的 數學 。'
dpt_sent = '艾萨克·牛顿_0 是_3 SBV###和_1 戈特弗里德·威廉·莱布尼茨_2 LAD###戈特弗里德·威廉·莱布尼茨_2 艾萨克·牛顿_0 COO###是_3 -1 HED###微积分学_4 發明者_6 ATT###的_5 微积分学_4 RAD###發明者_6 是_3 VOB###，_7 是_3 WP###費曼_8 發明_9 SBV###發明_9 是_3 COO###了_10 發明_9 RAD###路_11 發明_9 VOB###徑積_12 發明_9 COO###分_13 發明_9 COO###表述_14 分_13 VOB###，_15 發明_9 WP###來_16 發明_9 COO###用_17 推理_19 ADV###於_18 用_17 POB###推理_19 洞察_23 ADV###及_20 物理_21 LAD###物理_21 推理_19 COO###的_22 推理_19 RAD###洞察_23 來_16 VOB###，_24 發明_9 WP###而_25 生成為_30 ADV###今日_26 弦理論_28 ATT###的_27 今日_26 RAD###弦理論_28 生成為_30 SBV###亦_29 生成為_30 ADV###生成為_30 發明_9 COO###新_31 數學_33 ATT###的_32 新_31 RAD###數學_33 生成為_30 VOB###。_34 是_3 WP'

class BinaryFeatureFunction:
    def __init__(self, candidate_list):
        self.candidate_list = sorted(candidate_list)
        self.length = len(candidate_list)
    def __call__(self, target_list):
        if type(target_list) != list: target_list = [target_list]
        feature = [0] * self.length
        start_index = 0
        for target in sorted(target_list):
            try: start_index = self.candidate_list.index(target, start_index)
            except: break
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
    print(pos_sent)
    print(ner_sent)
    print(dpt_sent)
    fea_vec = [1 if reverse else 0]

    #------------------拆分三个句子------------------
    pos_list = [token.split('_') for token in pos_sent.split(' ')]
    ner_list = ner_sent.split(' ')
    dpt_list = [dp.split(' ') for dp in dpt_sent.split('###')]
    for dp in dpt_list:
        dp[0] = dp[0].split('_')
        if dp[1] == '-1': dp[1] = ['', '-1']
        else: dp[1] = dp[1].split('_')
        dp[0][1] = int(dp[0][1])
        dp[1][1] = int(dp[1][1])
    assert len(pos_list) == len(ner_list) == len(dpt_list)
    for token in pos_list:
        assert len(token) == 2
    for dp in dpt_list:
        assert len(dp) == 3
        assert len(dp[0]) == 2
        assert len(dp[1]) == 2
        assert type(dp[2]) == str

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
