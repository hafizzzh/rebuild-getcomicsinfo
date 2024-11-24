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

def url_maker(page_number):
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

def get_comic_info(comic):
    comics = []
    for c in comic:
        title = c.find('a', attrs={"class": None}).text
        link_comic = c.find('a', attrs={"class": None}).get('href')
        comics.append((title, link_comic))
    return comics

def print_comics(comics):
    comics.sort(key=lambda x: x[0])  # Sort comics by title
    for index, (title, link_comic) in enumerate(comics, start=1):
        print(index, ' ', title, ' ', link_comic)

def fetch_comics_from_page(url):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup.find_all('div', 'post-info')

def main():
    total_page = int(check_pagination())
    all_comics = []
    
    # Print total_page info
    print('Total pages: ', total_page)
    
    # Fetch comics from the first page
    comics = get_comic_info(comic)
    all_comics.extend(comics)
    

    # Fetch comics from the remaining pages
    if total_page > 1:
        for page_number in range(2, total_page + 1):
            url = url_maker(page_number)
            comics = get_comic_info(fetch_comics_from_page(url))
            all_comics.extend(comics)
    
    # Print total comics info
    print('Total comics: ', len(all_comics))

    # Print all comics sorted globally
    print_comics(all_comics)

if __name__ == "__main__":
    main()