import requests

# 妈蛋这里一定要回来用正则重写！！！
class WikiEntityRecognizer:

    def __init__(self):
        self.base_url = "http://ltpapi.voicecloud.cn/analysis/?"
        self.api_key = "A3Q1y6d97QjSAzKAIaFLlN5LXItLoP2MpzAZLH6z"
        self.pattern = "ner"
        self.result_format = "plain"

    def recognize(self, sent):
        url = "%sapi_key=%s&text=%s&format=%s&pattern=%s" % (self.base_url, self.api_key, sent, self.result_format, self.pattern)
        result = requests.get(url)
        if result.status_code ==  200:
            return result.text
        else:
            print("错误响应" + result.status_code + "！！！")
            return ""

if __name__ == "__main__":
    input_file_path = "/home/ezio/filespace/data/plain_sentences.txt"
    output_file_path = "/home/ezio/filespace/data/ner_sentences.txt"
    input_file = open(input_file_path, 'r')
    output_file = open(output_file_path, 'w', 1000)
    recognizer = WikiEntityRecognizer()

    i = 0
    for line in input_file:
        sent = line.strip()
        ner_sent = recognizer.recognize(sent)
        output_file.write(ner_sent + '\n')
        # print(ner_sent)
        i += 1
        print(i)
