import re
import xml.etree.ElementTree as etree

class WikiPageExtractor:

    def extract(self, filename):
        page = ""
        with open(filename) as file:
            for line in file:
                if line == "  <page>\n":
                    page = ""
                page += line
                if line == "  </page>\n":
                    yield page

if __name__ == "__main__":
    base_path = "/home/ezio/filespace/data/"
    xml_path = base_path + "sample.xml"
    extractor = WikiPageExtractor()
    for page in extractor.extract(xml_path):
        print(page)
        print("\n\n\n\n\n\n\n\n\n\n\n\n")
