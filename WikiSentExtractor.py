import xml.etree.ElementTree as etree
import re
from WikiPageExtractor import WikiPageExtractor

class WikiSentExtractor:

    def extract_text(self, page):
        page_node = etree.fromstring(page)
        text_node = list(page_node.iter('text'))[0]
        text = text_node.text
        return text

    def sent_tokenize(self, text):
        pattern1 = re.compile("<ref.*?\/.*?>", re.S)
        pattern2 = re.compile("\[\[File:.*\]\]")
        pattern3 = re.compile("==.*==")
        pattern4 = re.compile("[^。\n]*。")
        text = pattern1.sub("", text)
        text = pattern2.sub("", text)
        text = pattern3.sub("", text)
        sentences = pattern4.findall(text)
        sentences = [sent for sent in sentences if "http" not in sent]
        return sentences

    def extract(self, page):
        text = self.extract_text(page)
        sentences = self.sent_tokenize(text)
        return sentences


if __name__ == "__main__":
    base_path = "/home/ezio/filespace/data/"
    # xml_path = base_path + "zhwiki-20140508-pages-articles-multistream.xml"
    xml_path = base_path + "sample.xml"

    page_extractor = WikiPageExtractor()
    sent_extractor = WikiSentExtractor()
    for page in page_extractor.extract(xml_path):
        sentences = sent_extractor.extract(page)
        for sent in sentences:
            print(sent)
            print("=========================================================")
