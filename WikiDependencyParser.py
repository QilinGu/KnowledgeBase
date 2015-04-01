import requests
import traceback

class WikiDependencyParser:

    def __init__(self):
        self.base_url = "http://ltpapi.voicecloud.cn/analysis/?"
        self.api_key = "A3Q1y6d97QjSAzKAIaFLlN5LXItLoP2MpzAZLH6z"
        self.pattern = "dp"
        self.result_format = "plain"

    def parse(self, sent):
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
    input_file_path = "/home/ezio/filespace/data/backup/plain_sentences.txt"
    output_file_path = "/home/ezio/filespace/data/dp_sentences.txt"
    input_file = open(input_file_path, 'r')
    output_file = open(output_file_path, 'w', 1000)
    parser = WikiDependencyParser()

    total_count = 0
    fail_count = 0
    for line in input_file:
        sent = line.strip()
        dp_sent = parser.parse(sent)
        dp_sent = "".join(dp_sent.split('\n'))
        if dp_sent == "### can't get url!!!":
            fail_count += 1
        total_count += 1
        print(total_count, end = ' ')
        print(fail_count, end = ' ')
        print(dp_sent[0: min(len(dp_sent), 20)])
        output_file.write(dp_sent + '\n')
