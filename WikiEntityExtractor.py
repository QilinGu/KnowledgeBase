import sqlite3
import xml.etree.ElementTree as etree
from WikiPageExtractor import page_extract

class WikiEntityExtractor:

    def get_entity(self, page):
        page_node = etree.fromstring(page)
        title_node = list(page_node.iter('title'))[0]
        entity = title_node.text
        return entity

    def extract(self, page, cursor):
        entity = self.get_entity(page)
        cursor.execute('''INSERT INTO entity(name, std_name) VALUES(?, ?)''', (entity, entity))

if __name__ == "__main__":
    db_path = "/home/ezio/filespace/data/entity.db"
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM sqlite_master WHERE name = 'entity' and type = 'table'""")
    if len(cursor.fetchall()) > 0:
        cursor.execute("""DROP TABLE entity""")
    cursor.execute("""CREATE TABLE entity(name TEXT PRIMARY KEY, std_name TEXT)""")

    entity_extractor = WikiEntityExtractor()
    i = 0
    for page in page_extract():
        entity_extractor.extract(page, cursor)
        i += 1
        if i % 10000 == 0:
            print(i)
            db.commit()
        # print(entity_extractor.get_entity(page))
        # print("==========", i)
