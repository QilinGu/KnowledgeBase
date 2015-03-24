class Relation:
    def __init__(self, name, seed_pairs):
        self.name = name
        self.pair_list = seed_pairs
        self.tuple_list = []
        self.pattern_list = []

class WikiRelationExtractor:

    def __init__(self, filename):
        self.filename = filename
        self.relation_list = []
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

    def iter_sent(self):
        raw_flag = True
        raw_sent = ""
        for line in open(self.filename):
            line = line.strip()
            if (raw_flag):
                raw_sent = line
                raw_flag = False
            else:
                tagged_sent = line
                yield raw_sent, tagged_sent
                raw_flag = True

    def tuple_phase(self):
        for raw_sent, tagged_sent in self.iter_sent():

    def pattern_phase(self):
        pass

    def pair_phase(self):
        pass

    def extract(sentences):
        pass

if __name__ == "__main__":
    filename = "/home/ezio/filespace/data/sents.txt"
    ex = WikiRelationExtractor()
    for raw_sent, tagged_sent in ex.iter_sent(filename):
        print(raw_sent)
        print(tagged_sent)

