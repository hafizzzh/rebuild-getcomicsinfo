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
for c in comic:
    title = c.find('a', attrs={"class": None}).text
    print(title)

def check_pagination():
    page = soup.find('ul', 'page-numbers')
    if page is not None:
        pages = []
        for li in page.find_all("li"):
            pages.append(li.text)
        return pages.pop()

total_page = check_pagination()
print(total_page)
print(req)
print(convert_keyword(url))