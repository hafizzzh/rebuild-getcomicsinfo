import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

def convert_keyword(a):
    a1 = ""
    for i in range(len(a)):
        if a[i] == ' ':
            a1 = a1 + '+'
        else:
            a1 = a1 + a[i]
    return a1

search_item = input('Input comics keyword: ')
page_number = ''
search_item = convert_keyword(search_item)
url = 'https://getcomics.info/{}?s={}'.format(page_number, search_item)
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')
comic = soup.find_all('div', 'post-info')

def url_maker():
    url = 'https://getcomics.info/page/{}/?s={}'.format(page_number, search_item)
    return url

def check_pagination():
    page = soup.find('ul', 'page-numbers')
    if page is not None:
        pages = []
        for li in page.find_all("li"):
            pages.append(li.text)
        return pages.pop()
    else:
        return 0

total_page = int(check_pagination())
f = 0
if total_page == 0:
    for c in comic:
        title = c.find('a', attrs={"class": None}).text
        link_comic = c.find('a', attrs={"class": None}).get('href')
        f += 1
        print(f, ' ', title, ' ', link_comic)
else:
    for c in comic:
        title = c.find('a', attrs={"class": None}).text
        link_comic = c.find('a', attrs={"class": None}).get('href')
        f += 1
        print(f, ' ', title, ' ', link_comic)
    page_number = 2
    while page_number <= total_page:
        url = url_maker()
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        comic = soup.find_all('div', 'post-info')
        for c in comic:
            title = c.find('a', attrs={"class": None}).text
            link_comic = c.find('a', attrs={"class": None}).get('href')
            f += 1
            print(f, ' ', title, ' ', link_comic)
        page_number += 1

print(req)