import os
import queue
import time
import threading
import requests
import pickle
import random
import traceback
import urllib
from lxml import html

url_queue_dump = '/home/ezio/filespace/data/url_queue.data'
page_queue_dump = '/home/ezio/filespace/data/page_queue.data'
subject_set_dump = '/home/ezio/filespace/data/subject_set.data'
tag_file = '/home/ezio/filespace/data/douban_tags.txt'
ip_file = '/home/ezio/filespace/data/good_ip.txt'
db_file = '/home/ezio/filespace/data/douban.db'

# 第一车间
def scrawl_url(control_dict, data_dict):
    thread_id = control_dict['id']
    stop_event = control_dict['stop']
    except_event = control_dict['except']
    url_queue = data_dict['url']
    page_queue = data_dict['page']
    proxies = data_dict['proxies']
    try:
        proxies_count = len(proxies)
        try_again = False
        while not stop_event.is_set():
            if try_again == False:
                time.sleep(0.1) # 控制访问频率
                print('url_queue size: ' + str(url_queue.qsize()))
                url = url_queue.get()
            proxy = proxies[random.randint(0, proxies_count - 1)]
            try:
                req = requests.get(url, proxies = {'http': proxy, 'https': proxy})
            except:
                try_again = True
                continue
            if req.status_code != 200:
                try_again = True
            else:
                try_again = False
                page_queue.put(req.text)
        print('scrawl_url ' + str(thread_id) + ' stopped by master')
    except:
        print('scrawl_url ' + str(thread_id) + ' raise an exception!!!')
        traceback.print_exc()
        except_event.set()

# 第二车间
def parse_page(control_dict, data_dict):
    stop_event = control_dict['stop']
    except_event = control_dict['except']
    url_queue = data_dict['url']
    page_queue = data_dict['page']
    subject_list_queue = data_dict['subject_list']
    try:
        while not stop_event.is_set():
            if page_queue.empty():
                time.sleep(0.1)
                continue
            page = page_queue.get()
            etree = html.fromstring(page)
            next_node = etree.find('.//span[@class="next"]/a')
            if next_node != None:
                next_url = next_node.get('href')
                url_queue.put(next_url)
                print('parse_page yield next url: ' + urllib.parse.unquote(next_url))
            subject_list = []
            for a_node in etree.iterfind('./body/div[3]/div[1]/div/div[1]/div[2]/table//tr/td[2]/div/a'):
                subject_id = a_node.get('href').split('/')[-2]
                subject_name = a_node.text.split()[0]
                subject_list.append((subject_id, subject_name))
            subject_list_queue.put(subject_list)
        print('parse_page stopped by master')
    except:
        print('parse_page raise an exception!!!')
        traceback.print_exc()
        except_event.set()

# 第三车间
def merge_subject(control_dict, data_dict):
    stop_event = control_dict['stop']
    subject_list_queue = data_dict['subject_list']
    subject_set = data_dict['subject']
    # 在主线程发停止信号后，仍然会坚守岗位直到最后一批subject归入集合
    while (not stop_event.is_set()) or (not subject_list_queue.empty()):
        if subject_list_queue.empty():
            time.sleep(0.1)
            continue
        subject_list = subject_list_queue.get()
        for subject in subject_list:
            subject_set.add(subject)
    print('merge_subject stopped by master')

def list_to_queue(l):
    q = queue.Queue()
    for item in l:
        q.put(l)
    return q

def queue_to_list(q):
    l = []
    while not q.empty():
        l.append(q.get())
    return l

def load_from_disk():
    print('load_from_disk')
    if os.path.isfile(url_queue_dump) and os.path.isfile(page_queue_dump) and os.path.isfile(subject_set_dump):
        with open(url_queue_dump, 'rb') as f: url_list = pickle.load(f)
        with open(page_queue_dump, 'rb') as f: page_list = pickle.load(f)
        with open(subject_set_dump, 'rb') as f: subject_set = pickle.load(f)
        url_queue = list_to_queue(url_list)
        page_queue = list_to_queue(page_list)
    else:
        url_queue = queue.Queue()
        base_url = 'http://movie.douban.com/tag/'
        for line in open(tag_file):
            url_queue.put(base_url + line.strip())
        page_queue = queue.Queue()
        subject_set = set()
    subject_list_queue = queue.Queue()
    proxies = []
    for line in open(ip_file):
        proxies.append(line.strip())

    return {'url': url_queue, 'page': page_queue, 'subject': subject_set, 'subject_list': subject_list_queue, 'proxies': proxies}

def dump_to_disk(data_dict):
    print('dump_to_disk')
    try:
        if os.path.isfile(url_queue_dump):   os.remove(url_queue_dump)
        if os.path.isfile(page_queue_dump):  os.remove(page_queue_dump)
        if os.path.isfile(subject_set_dump): os.remove(subject_set_dump)
        url_list = queue_to_list(data_dict['url'])
        page_list = queue_to_list(data_dict['page'])
        subject_set = data_dict['subject']
        with open(url_queue_dump,   'wb') as f: pickle.dump(url_list,    f); print(str(len(url_list))    + ' url dumped!')
        with open(page_queue_dump,  'wb') as f: pickle.dump(page_list,   f); print(str(len(page_list))   + ' page dumped!')
        with open(subject_set_dump, 'wb') as f: pickle.dump(subject_set, f); print(str(len(subject_set)) + ' subject dumped!')
    except:
        print("要完要完！dump不下去！")

# def master(scrawl_thread_count):
scrawl_thread_count = 2
try:
    data_dict = load_from_disk()

    # 先准备好各种Event
    scrawl_stop_events = []
    scrawl_except_events = []
    for i in range(scrawl_thread_count):
        scrawl_stop_events.append(threading.Event())
        scrawl_except_events.append(threading.Event())
    parse_stop_event = threading.Event()
    parse_except_event = threading.Event()
    merge_stop_event = threading.Event()

    # 创建并启动各个线程
    scrawl_threads = []
    for i in range(scrawl_thread_count):
        control_dict = {'id': i, 'stop': scrawl_stop_events[i], 'except': scrawl_except_events[i]}
        scrawl_thread = threading.Thread(target = scrawl_url, args = (control_dict, data_dict))
        scrawl_thread.start()
        scrawl_threads.append(scrawl_thread)
    control_dict = {'stop': parse_stop_event, 'except': parse_except_event}
    parse_thread = threading.Thread(target = parse_page, args = (control_dict, data_dict))
    parse_thread.start()
    control_dict = {'stop': merge_stop_event}
    merge_thread = threading.Thread(target = merge_subject, args = (control_dict, data_dict))
    merge_thread.start()

    stop_all = False
    while not stop_all:
        time.sleep(2)
        except_count = 0
        for except_event in scrawl_except_events:
            if except_event.is_set():
                except_count += 1
        if except_count == scrawl_thread_count:
            stop_all = True
        if parse_except_event.is_set():
            stop_all = True
# 无论如何一定会执行的善后处理
except:
    print('master raise an exception!!!')
    traceback.print_exc()
finally:
    print("处理善后")
    if 'scrawl_except_events' in locals():
        for stop_event in scrawl_stop_events:
            stop_event.set()
    if 'parse_stop_event' in locals():
        parse_stop_event.set()
    if 'merge_stop_event' in locals():
        merge_stop_event.set()
    if 'scrawl_threads' in locals():
        for scrawl_thread in scrawl_threads:
            scrawl_thread.join()
    if 'parse_thread' in locals():
        parse_thread.join()
    if 'merge_thread' in locals():
        merge_thread.join()
    if 'data_dict' in locals():
        dump_to_disk(data_dict)

# master(1)
