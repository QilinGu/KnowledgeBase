import sys
import jieba
import jieba.posseg as pseg
from WikiSentExtractor import sent_extract

class POSTagger:

    def __init__(self):
        jieba.enable_parallel(2)

    def tag(self, sent):
        tagged_sent = list(pseg.cut(sent))
        return tagged_sent

def pos_tag():
    pos_tagger = POSTagger()
    for raw_sent in sent_extract():
        tagged_sent = pos_tagger.tag(raw_sent)
        yield raw_sent, tagged_sent

if __name__ == "__main__":
    file_path = "/home/ezio/filespace/data/sentences.txt"
    f = open(file_path, 'w')
    i = 0
    for raw_sent, tagged_sent in pos_tag():
        print(i, end = ' ')
        sys.stdout.flush()
        i += 1
        f.write(raw_sent + '\n')
        # print(raw_sent)
        for token in tagged_sent:
            f.write(token.word + '/' + token.flag + ' ')
            # print(token, end = ' ')
        f.write('\n')
        # print("\n======================================")
