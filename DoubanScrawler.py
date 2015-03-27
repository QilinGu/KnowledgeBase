import sqlite3
import requests
from lxml import html

def parse_page(page):
    etree = html.fromstring(page)
    next_node = etree.find('.//span[@class="next"]/a')
    if next_node == None:
        next_url = ''
    else:
        next_url = next_node.get('href')
    subject_list = []
    for a_node in etree.iterfind('./body/div[3]/div[1]/div/div[1]/div[2]/table//tr/td[2]/div/a'):
        subject_id = a_node.get('href').split('/')[-2]
        subject_name = a_node.text.split()[0]
        subject_list.append((subject_id, subject_name))
    return subject_list, next_url

def get_all_subject(tag_file, db_file):
    all_subject = set()
    for line in open(tag_file):
        tag = line.strip()
        next_url = 'http://movie.douban.com/tag/' + tag
        print("=============== " + tag + " ===================")
        print("len(all_subject): " + str(len(all_subject)))

        while next_url != '':
            req = requests.get(next_url)
            subject_list, next_url = parse_page(req.text)
            print(next_url)
            for subject in subject_list:
                print(subject)
                all_subject.add(subject)

    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute("""select * from sqlite_master where name = 'subject' and type = 'table'""")
    if len(cursor.fetchall()) > 0:
        cursor.execute("""drop table subject""")
    cursor.execute("""create table subject(id int primary key, name text)""")
    for (subject_id, subject_name) in all_subject:
        cursor.execute("""insert into subject(id, name), values(?, ?)""", (subject_id, subject_name))

    return all_subject

tag_file = '/home/ezio/filespace/data/douban_tags.txt'
db_file = '/home/ezio/filespace/data/douban.db'
all_subject = get_all_subject(tag_file, db_file)
