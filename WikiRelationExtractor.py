from collections import defaultdict

class Relation:
    def __init__(self, name, seed_pairs):
        self.name = name
        self.pair_list = seed_pairs
        self.occurence_dict = defaultdict(lambda: list())
        self.pattern_list = []

class WikiRelationExtractor:

    # filename: 存放句子的文件名
    # relation_list: 初始界定要处理哪些关系
    # prefix_length: 限制前缀长度
    # middle_length: 限制中缀长度，主体和客体隔太远认为不可靠，丢弃
    # suffix_length: 限制后缀长度
    # occurence_count: 如果支持一个pattern的occurence太少，认为不可靠，丢弃
    def __init__(self, filename, relation_list, prefix_length, middle_length, suffix_length, occurence_count):
        self.filename = filename
        self.relation_list = relation_list
        self.prefix_length = prefix_length
        self.middle_length = middle_length
        self.suffix_length = suffix_length
        self.occurence_count = occurence_count

    def occurence_phase(self):
        for sent in  open(self.filename):
            for relation in self.relation_list:
                relation.occurence = [] # 清空上次迭代的occurence
                for pair in relation.pair_list:
                    sub = pair[0]
                    obj = pair[1]
                    if sub in sent and obj in sent:
                        s_begin = sent.find(sub)
                        s_end = s_begin + len(sub)
                        o_begin = sent.find(obj)
                        o_end = o_begin + len(obj)
                        if (s_begin < o_begin):
                            if (o_begin - s_end > self.middle_length):
                                continue
                            order = 0
                            prefix_begin = max(0, s_begin - self.prefix_length)
                            prefix_end = s_begin
                            middle_begin = s_end
                            middle_end = o_begin
                            suffix_begin = o_end
                            suffix_end = min(len(sent), o_end + self.suffix_length)
                        else:
                            if (s_begin - o_end > self.middle_length):
                                continue
                            order = 1
                            prefix_begin = max(0, o_begin - self.prefix_length)
                            prefix_end = o_begin
                            middle_begin = o_end
                            middle_end = s_begin
                            suffix_begin = s_end
                            suffix_end = min(len(sent), s_end + self.suffix_length)
                        prefix = sent[prefix_begin : prefix_end]
                        middle = sent[middle_begin : middle_end]
                        suffix = sent[suffix_begin : suffix_end]
                        if order == 0:
                            print('|'.join([prefix, sub, middle, obj, suffix]))
                        else:
                            print('|'.join([prefix, obj, middle, sub, suffix]))
                        relation.occurence_dict[(order, middle)].append([prefix, suffix])
        for relation in self.relation_list:
            print(relation.name + " : " + str(len(relation.occurence_dict)))

    # 得到的pattern必须保证prefix, middle, suffix不为空字符串
    def pattern_phase(self):
        def max_common_fix(string_list, type):
            def slice(string, length, type):
                if type == 'suffix':
                    return string[len(string) - length:]
                else:
                    return string[0:length]
            assert type == 'prefix' or type == 'suffix'
            length = 0
            go_on = True
            while go_on:
                length += 1
                for i, string in enumerate(string_list):
                    if length > len(string):
                        go_on = False
                        break
                    if i == 0:
                        standard = slice(string, length, type)
                    suffix = slice(string, length, type)
                    if suffix != standard:
                        go_on = False
                        break
            length -= 1
            return slice(string_list[0], length, type)

        for relation in self.relation_list:
            relation.pattern_list = [] # 清空上次迭代的pattern
            for key, value in relation.occurence_dict.items():
                if len(value) < self.occurence_count: continue
                if key[1] == '': continue # middle不能为空字符串
                # 注意最大公共前缀实际上是所有前缀的最大公共后缀！
                prefix = max_common_fix([item[0] for item in value], 'suffix')
                suffix = max_common_fix([item[1] for item in value], 'prefix')
                pattern = {'order':key[0], 'prefix':prefix, 'middle':key[1], 'suffix':suffix}
                relation.pattern_list.append(pattern)

    def pair_phase(self):
        for sent in  open(self.filename):
            for relation in self.relation_list:
                relation.pair_list = [] # 清空上次迭代的pair
                for pattern in relation.pattern_list:
                    prefix_begin = sent.find(pattern['prefix'], 0)
                    while prefix_begin != -1:
                        middle_begin = sent.find(pattern['middle'], prefix_begin + 1)
                        if middle_begin == -1: continue
                        suffix_begin = sent.find(pattern['suffix'], middle_begin + 1)
                        if suffix_begin == -1: continue
                        prefix_end = prefix_begin + len(pattern['prefix'])
                        middle_end = middle_begin + len(pattern['middle'])
                        sub    = sent[prefix_end : middle_begin]
                        obj    = sent[middle_end : suffix_begin]
                        if order == 1: sub, obj = obj, sub
                        relation.pair_list.append((sub, obj))
                        prefix_begin = sent.find(pattern['prefix'], prefix_begin + 1)

    def check_phase(self):
        pass

    def extract(sentences):
        pass

if __name__ == "__main__":
    relation_list = []
    # relation_list.append(Relation("首都", [
    #     ("中国", "北京"),
    #     ("美国", "华盛顿"),
    #     ("西汉", "长安"),
    #     ("苏联", "莫斯科"),
    #     ("东罗马帝国", "君士坦丁堡"),
    # ]))
    #relation_list.append(Relation("出生时间", [
    #    ("毛泽东", "1893年12月26日"),
    #    ("李彦宏", "1968年11月17日"),
    #    ("曹雪芹", "约1715年"),
    #    ("孔丘", "前551年"),
    #    ("達·芬奇", "1452年4月15日"),
    #]))
    relation_list.append(Relation("创作者", [
        ("曹雪芹", "《紅樓夢》"),
        ("丹·布朗", "《达芬奇密码》"),
        ("鲁迅", "《狂人日记》"),
        ("達·芬奇", "《蒙娜丽莎》"),
    ]))
    filename = "/home/ezio/filespace/data/sents.txt"
    # filename = "/home/ezio/filespace/data/sentences.txt"
    # 传参：filename, relation_list, prefix_length, middle_length, suffix_length, occurence_count:
    ex = WikiRelationExtractor(filename, relation_list, 5, 5, 5, 3)
    ex.occurence_phase()
    ex.pattern_phase()
