import jieba
import jieba.posseg as pseg
import requests

jieba.enable_parallel(4)
class JiebaPOSTagger:

    def tag(self, sent):
        pos_sent = list(pseg.cut(sent))
        return pos_sent

class LtpPOSTagger():

    def __init__(self):
        self.base_url = "http://ltpapi.voicecloud.cn/analysis/?"
        self.api_key = "A3Q1y6d97QjSAzKAIaFLlN5LXItLoP2MpzAZLH6z"
        self.pattern = "pos"
        self.result_format = "plain"

    def tag(self, sent):
        url = "%sapi_key=%s&text=%s&format=%s&pattern=%s" % (self.base_url, self.api_key, sent, self.result_format, self.pattern)
        try_count = 3
        while try_count > 0:
            try_count -= 1
            try:
                result = requests.get(url)
            except:
                continue
            if result.status_code !=  200:
                continue
            else:
                return "###".join(result.text.split('\n'))
        if try_count == 0:
            return "### can't get url!!!"

if __name__ == "__main__":
    input_file_path = "/home/ezio/filespace/data/plain_sentences.txt"
    output_file_path = "/home/ezio/filespace/data/pos_sentences.txt"
    input_file = open(input_file_path, 'r')
    output_file = open(output_file_path, 'a', 1000)
    tagger = LtpPOSTagger()
    i = 0
    for line in input_file:
        i += 1
        print(i)
        if i <= 1427: continue
        sent = line.strip()
        pos_sent = tagger.tag(sent)
        output_file.write(pos_sent)
        output_file.write('\n')
        # print(pos_sent)

