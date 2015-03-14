import re
from WikiTextExtractor import text_extract

class WikiSentExtractor:

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
            yield sent

def sent_extract():
    sent_extractor = WikiSentExtractor()
    for text in text_extract():
        for sent in sent_extractor.extract(text):
            yield sent

if __name__ == "__main__":
    for sent in sent_extract():
        print(sent)
        print("=========================================================")
