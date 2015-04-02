import sys
import requests
import traceback

class WikiEntityRecognizer:

    def __init__(self):
        self.base_url = "http://ltpapi.voicecloud.cn/analysis/?"
        self.api_key = "A3Q1y6d97QjSAzKAIaFLlN5LXItLoP2MpzAZLH6z"
        self.pattern = "ner"
        self.result_format = "plain"

    def recognize(self, sent):
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
                return result.text
        if try_count == 0:
            return "### can't get url!!!"

if __name__ == "__main__":
    input_file_path = "/home/ezio/filespace/data/plain_sentences.txt"
    output_file_path = "/home/ezio/filespace/data/ner_sentences.txt"
    input_file = open(input_file_path, 'r')
    output_file = open(output_file_path, 'a', 1000)
    recognizer = WikiEntityRecognizer()

    total_count = 0
    fail_count = 0
    for line in input_file:
        total_count += 1
        print(total_count, end = ' ')
        sys.stdout.flush()
        if total_count <= 304262: continue

        sent = line.strip()
        ner_sent = recognizer.recognize(sent)
        ner_sent = "".join(ner_sent.split('\n'))

        if ner_sent == "### can't get url!!!":
            fail_count += 1
        print(fail_count, end = ' ')

        print(ner_sent[0: min(len(ner_sent), 20)])
        output_file.write(ner_sent + '\n')
