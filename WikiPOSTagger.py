# import sys
import jieba
import jieba.posseg as pseg
# from WikiSentExtractor import sent_extract

class POSTagger:

    def tag(self, sent):
        tagged_sent = list(pseg.cut(sent))
        return tagged_sent

if __name__ == "__main__":
    jieba.enable_parallel(4)
    input_file_path = "/home/ezio/filespace/data/plain_sentences.txt"
    output_file_path = "/home/ezio/filespace/data/tagged_sentences.txt"
    input_file = open(input_file_path, 'r')
    output_file = open(output_file_path, 'a', 1000)
    tagger = POSTagger()
    i = 0
    for line in input_file:
        i += 1
        print(i)
        if i <= 561213: continue
        sent = line.strip()
        tagged_sent = tagger.tag(sent)
        for token in tagged_sent:
            output_file.write(str(token))
            output_file.write(' ')
        output_file.write('\n')
        # print(tagged_sent)

"""
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
"""
