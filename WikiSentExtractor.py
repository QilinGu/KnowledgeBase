import sys
import re
from WikiTextExtractor import text_extract

class WikiSentExtractor:

    def __init__(self):
        self.strip_pattern1 = re.compile(r'\[\[([^\|]*?)\]\]')
        self.strip_pattern2 = re.compile(r'\[\[([^\|]*?)\|[^\|]*?\]\]')
        self.strip_pattern3 = re.compile(r"'''(.*?)'''")

    def extract(self, text):
        pattern1 = re.compile("<ref.*?\/.*?>", re.S)
        pattern2 = re.compile("\[\[File:.*\]\]")
        pattern3 = re.compile("==.*==")
        pattern4 = re.compile("[^。\n]*。")
        text = pattern1.sub("", text)
        text = pattern2.sub("", text)
        text = pattern3.sub("", text)
        sentences = pattern4.findall(text)
        sentences = [sent for sent in sentences if "http" not in sent]
        for sent in sentences:
            yield self.strip_sent(sent)
            #yield sent

    def strip_sent(self, sent):
        sent = self.strip_pattern1.sub(r'\1', sent)
        sent = self.strip_pattern2.sub(r'\1', sent)
        sent = self.strip_pattern3.sub(r'\1', sent)
        return sent

def sent_extract():
    sent_extractor = WikiSentExtractor()
    for text in text_extract():
        for sent in sent_extractor.extract(text):
            if type(sent) == str:
                yield sent

if __name__ == "__main__":
    file_path = "/home/ezio/filespace/data/sentences.txt"
    f = open(file_path, 'w')
    for sent in sent_extract():
        f.write(sent + '\n')
        #print(sent)
        #print("=========================================================")
