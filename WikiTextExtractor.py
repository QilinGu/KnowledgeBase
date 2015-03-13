import xml.etree.ElementTree as etree
from WikiPageExtractor import WikiPageExtractor

class WikiTextExtractor:

    def extract(self, page):
        page_node = etree.fromstring(page)
        text_node = list(page_node.iter('text'))[0]
        text = text_node.text
        return text

if __name__ == "__main__":
    base_path = "/home/ezio/filespace/data/"
    # xml_path = base_path + "zhwiki-20140508-pages-articles-multistream.xml"
    xml_path = base_path + "sample.xml"

    extractor = WikiPageExtractor()
    page_extractor = WikiPageExtractor()
    text_extractor = WikiTextExtractor()
    for page in page_extractor.extract(xml_path):
        print(text_extractor.extract(page))
        break
