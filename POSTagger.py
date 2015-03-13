import jieba.posseg as pseg
from WikiSentExtractor import sent_extract

class POSTagger:

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
    for token in pos_tag():
        print(token)
    print("\n======================================")
