import requests

class LtpSentParser:

    def __init__(self):
        self.base_url = "http://ltpapi.voicecloud.cn/analysis/?"
        self.api_key = "A3Q1y6d97QjSAzKAIaFLlN5LXItLoP2MpzAZLH6z"
        self.patterns = ["pos", 'ner', 'dpt']
        self.result_format = "plain"

    def parse(self, sent, pattern):
        url = "%sapi_key=%s&text=%s&format=%s&pattern=%s" % (self.base_url, self.api_key, sent, self.result_format, pattern)
        result = "### can't get url!!!"
        try_count = 2
        while try_count > 0:
            try_count -= 1
            try:
                response = requests.get(url)
            except:
                print('try fail')
                continue
            if response.status_code !=  200:
                print('response', response.status_code)
                continue
            else:
                result = "###".join(response.text.split('\n'))
        return result

    def pos(self, sent): return self.parse(sent, 'pos')
    def ner(self, sent): return self.parse(sent, 'ner')
    def dpt(self, sent): return self.parse(sent, 'dp')

if __name__ == "__main__":
    input_file = open("/Users/warbean/filespace/data/plain_sentences.txt", 'r')
    pos_file   = open("/Users/warbean/filespace/data/pos_sentences.txt"  , 'a', 1)
    ner_file   = open("/Users/warbean/filespace/data/ner_sentences.txt"  , 'a', 1)
    dpt_file   = open("/Users/warbean/filespace/data/dpt_sentences.txt"  , 'a', 1)
    parser = LtpSentParser()
    i = 0
    for line in input_file:
        i += 1
        print('-----------------', i)
        if i <= 54620: continue
        sent = line.strip()

        pos_sent = parser.pos(sent)
        assert '\n' not in pos_sent
        pos_file.write(pos_sent + '\n')

        ner_sent = parser.ner(sent)
        assert '\n' not in ner_sent
        ner_file.write(ner_sent + '\n')

        dpt_sent = parser.dpt(sent)
        assert '\n' not in dpt_sent
        dpt_file.write(dpt_sent + '\n')

        print("  ###  ".join([pos_sent[:10], ner_sent[:10], dpt_sent[:10]]))
