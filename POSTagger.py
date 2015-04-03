# import sys
import jieba
import jieba.posseg as pseg

class POSTagger:

    def tag(self, sent):
        pos_sent = list(pseg.cut(sent))
        return pos_sent

if __name__ == "__main__":
    jieba.enable_parallel(4)
    input_file_path = "/home/ezio/filespace/data/plain_sentences.txt"
    output_file_path = "/home/ezio/filespace/data/pos_sentences.txt"
    input_file = open(input_file_path, 'r')
    output_file = open(output_file_path, 'a', 1000)
    tagger = POSTagger()
    i = 0
    for line in input_file:
        i += 1
        print(i)
        if i <= 561213: continue
        sent = line.strip()
        pos_sent = tagger.tag(sent)
        for token in pos_sent:
            output_file.write(str(token))
            output_file.write(' ')
        output_file.write('\n')
        # print(pos_sent)
