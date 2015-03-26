import xml.etree.ElementTree as etree
from WikiPageExtractor import page_extract

class WikiTextExtractor:

    def extract(self, page):
        page_node = etree.fromstring(page)
        text_node = list(page_node.iter('text'))[0]
        text = text_node.text
        return text

def text_extract():
    i = 0
    text_extractor = WikiTextExtractor()
    for page, title in page_extract():
        i += 1
        # print(i)
        text = text_extractor.extract(page)
        if type(text) == str:
            yield text, title

if __name__ == "__main__":
    for text, title in text_extract():
        print(text)
        print("=========================================================")
