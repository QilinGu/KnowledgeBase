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

if __name__ == "__main__":
    base_path = "/home/ezio/filespace/data/"
    xml_path = base_path + "zhwiki-20140508-pages-articles-multistream.xml"
    # xml_path = base_path + "sample.xml"
    extractor = WikiPageExtractor()
    i = 0
    for page in extractor.extract(xml_path):
        i += 1
        if i % 10000 == 0:
            print(i)
        # print("\n\n\n\n\n\n\n\n\n\n\n\n")
