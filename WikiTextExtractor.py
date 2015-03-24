import xml.etree.ElementTree as etree
from WikiPageExtractor import page_extract

class WikiTextExtractor:

    def extract(self, page):
        page_node = etree.fromstring(page)
        text_node = list(page_node.iter('text'))[0]
        text = text_node.text
        return text

def text_extract():
    text_extractor = WikiTextExtractor()
    i = 0
    for page in page_extract():
        print('page' + str(i))
        i += 1
        yield text_extractor.extract(page)

if __name__ == "__main__":
    for text in text_extract():
        print(text)
        print("=========================================================")
