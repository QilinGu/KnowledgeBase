import jieba
import jieba.posseg as pseg
from WikiSentExtractor import sent_extract

class POSTagger:

    def __init__(self):
        jieba.enable_parallel(2)

    def tag(self, sent):
        token_list = list(pseg.cut(sent))
        return token_list

def pos_tag():
    pos_tagger = POSTagger()
    for sentences in sent_extract():
        for sent in sentences:
            token_list = pos_tagger.tag(sent)
            yield token_list

if __name__ == "__main__":
    for token_list in pos_tag():
        for token in token_list:
            print(token)
        print("\n======================================")
