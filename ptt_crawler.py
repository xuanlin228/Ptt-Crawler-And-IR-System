import string
import requests
import bs4
import time
import json
import re
import concurrent.futures
import threading
from fake_useragent import UserAgent

ua = UserAgent()

lock = threading.Lock()


def get_catalogue(URL):
    # 設定Header與Cookie
    #my_headers = {'User-Agent': ua.random}

    # 發送get 請求 到 ptt
    response = requests.get(URL)

    # 2-1 把網頁程式碼(HTML) 丟入 bs4模組分析
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    catalogue_2016 = soup.find_all("a",
                                         string=re.compile('^◆ (2016)'))

    return catalogue_2016


def get_one_page(title, catalogue_title):

    article_detail = {}
    article_detail['catalogueTitle'] = catalogue_title

    if title.find('a') != None:
        article_detail['title'] = title.text.strip()
        url = title.find('a')['href']
        article_detail = get_article_detail(url, article_detail)
        write_json(article_detail)

    time.sleep(1)


def get_article_detail(URL, crawlerDict):

    #my_headers = {'User-Agent': ua.random}
    #組成內容的 link
    content_link = "https://www.ptt.cc/" + URL
    response = requests.get(content_link)
    # 2-1 把網頁程式碼(HTML) 丟入 bs4模組分析
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    header = soup.find_all('span', 'article-meta-value')
    if len(header) > 3:
        # 作者
        author = header[0].text
        # 看版
        board = header[1].text
        # 標題
        title = header[2].text
        # 日期
        date = header[3].text

        crawlerDict['author'] = author
        crawlerDict['board'] = board
        crawlerDict['date'] = date

    else:
        crawlerDict['author'] = "None"
        crawlerDict['board'] = "C_Chat"
        crawlerDict['date'] = "None"

    if soup.find(id='main-content') != None:
        main_content = soup.find(id='main-content')
        main_content_text = main_content.text
        # 把整個內容切割透過 "-- " 切割成2個陣列
        pre_text = main_content_text.split('--')[:-1]
        text = "--".join(pre_text)
        # 把每段文字 根據 '\n' 切開
        texts = text.split('\n')
        articles = texts[1:]
        # 內容
        article = '\n'.join(articles)
    #print(content)
    else:
        article = "None"

    crawlerDict['article'] = article
    time.sleep(5)

    return crawlerDict


def write_json(data):
    lock.acquire()
    json_file = json.dumps(data, ensure_ascii=False)
    with open('data.json', 'a', encoding='utf-8') as f:
        f.write(json_file)
        f.write('\n')
    lock.release()


link = "https://www.ptt.cc/man/C_Chat/DE98/DFF5/index.html"

# 執行爬蟲2016-2017 -> 第一層目錄 ex: 20160101-20160130...
catalogue_2016 = get_catalogue(link)
for i in range(0, 3):
    catalogue = catalogue_2016[i]
    catalogue_title = catalogue.text
    url = "https://www.ptt.cc" + catalogue['href']
    catalogue_response = requests.get(url)
    catalogue_soup = bs4.BeautifulSoup(catalogue_response.text, "html.parser")
    title_list = catalogue_soup.find_all('div', 'title')
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for t in title_list:
            get_one_page(t, catalogue_title)
        
