import re
import xml.etree.ElementTree as etree

class WikiPageExtractor:

    def extract(self, filename):
        page = ""
        drop = False
        with open(filename) as file:
            for line in file:
                if line == "  <page>\n":
                    drop = False
                    page = ""
                if line[:21] == "    <title>Wikipedia:" or line[:16] == "    <title>Help:":
                    drop= True
                if drop == False:
                    page += line
                if line == "  </page>\n" and drop == False:
                    yield page

def page_extract():
    base_path = "/home/ezio/filespace/data/"
    xml_path = base_path + "zhwiki-20140508-pages-articles-multistream.xml"
    # xml_path = base_path + "sample.xml"
    extractor = WikiPageExtractor()
    for page in extractor.extract(xml_path):
        yield page

if __name__ == "__main__":
    for page in page_extract():
        print(page)
        print("\n\n\n\n\n\n\n\n\n\n\n\n")
