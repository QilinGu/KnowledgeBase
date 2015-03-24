class Relation:
    def __init__(self, name, seed_pairs):
        self.name = name
        self.pair_list = seed_pairs
        self.occurence_list = []
        self.pattern_list = []

class WikiRelationExtractor:

    def __init__(self, filename, prefix_length, middle_length, suffix_length, relation_list):
        self.filename = filename
        self.prefix_length = prefix_length
        self.middle_length = middle_length
        self.suffix_length = suffix_length
        self.relation_list = relation_list

    def to_string(self, occurence):
        if occurence[2] == 0:
            string = occurence[3]           #prefix
            string += '|' + occurence[0]    #sub
            string += '|' + occurence[4]    #middle
            string += '|' + occurence[1]    #obj
            string += '|' + occurence[5]    #suffix
        else:
            string = occurence[3]           #prefix
            string += '|' + occurence[1]    #obj
            string += '|' + occurence[4]    #middle
            string += '|' + occurence[0]    #sub
            string += '|' + occurence[5]    #suffix
        return string

    def occurence_phase(self):
        for sent in  open(self.filename):
            for relation in self.relation_list:
                relation.occurence = []
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
                        occurence = (sub, obj, order, prefix, middle, suffix)
                        print(self.to_string((occurence)))
                        relation.occurence_list.append(occurence)
        for relation in self.relation_list:
            print(relation.name + " : " + str(len(relation.occurence_list)))

    def pattern_phase(self):
        pass

    def pair_phase(self):
        pass

    def extract(sentences):
        pass

if __name__ == "__main__":
    relation_list = []
    relation_list.append(Relation("创作者", [
        ("曹雪芹", "《紅樓夢》"),
        ("丹·布朗", "《达芬奇密码》"),
        ("鲁迅", "《狂人日记》"),
        ("達·芬奇", "《蒙娜丽莎》"),
    ]))
    relation_list.append(Relation("出生时间", [
        ("毛泽东", "1893年12月26日"),
        ("李彦宏", "1968年11月17日"),
        ("曹雪芹", "约1715年"),
        ("孔丘", "前551年"),
        ("達·芬奇", "1452年4月15日"),
    ]))
    relation_list.append(Relation("首都", [
        ("中国", "北京"),
        ("美国", "华盛顿"),
        ("西汉", "长安"),
        ("苏联", "莫斯科"),
        ("东罗马帝国", "君士坦丁堡"),
    ]))
    filename = "/home/ezio/filespace/data/sents.txt"
    # filename = "/home/ezio/filespace/data/sentences.txt"
    ex = WikiRelationExtractor(filename, 5, 5, 5, relation_list)
    ex.occurence_phase()

