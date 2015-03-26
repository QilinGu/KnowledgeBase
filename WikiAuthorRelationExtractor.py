import re
import sqlite3
from WikiTextExtractor import text_extract

class WikiAuthorRelationExtractor:

    def extract_works(self, text):
        match = re.search('== 作品 ==(.*?)== .*? ==', text, re.S)
        if match != None:
            works_text = match.group(0)
        else:
            return []
        works_list = re.findall('《.*?》', works_text)
        return works_list

    def extract(self):
        for text, author in text_extract():
            works_list = self.extract_works(text)
            yield author, works_list

if __name__ == "__main__":
    db_path = "/home/ezio/filespace/data/relation.db"
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM sqlite_master WHERE name = 'author' and type = 'table'""")
    if len(cursor.fetchall()) > 0:
        cursor.execute("""DROP TABLE author""")
    cursor.execute("""CREATE TABLE author(subject TEXT, object TEXT)""")

    i= 0
    extractor = WikiAuthorRelationExtractor()
    for author, works_list in extractor.extract():
        for works in works_list:
            cursor.execute("""INSERT INTO author(subject, object) VALUES(?, ?)""", (author, works))
            i += 1
            if i % 100 == 0:
                print(i)
            if i % 10000 == 0:
                db.commit()
    db.commit()
