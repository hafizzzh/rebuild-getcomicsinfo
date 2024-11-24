from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def convert_keyword(a):
    a1 = ""
    for i in range(len(a)):
        if a[i] == ' ':
            a1 = a1 + '+'
        else:
            a1 = a1 + a[i]
    return a1

def url_maker(page_number, search_item):
    url = 'https://getcomics.info/page/{}/?s={}'.format(page_number, search_item)
    return url

def check_pagination(soup):
    page = soup.find('ul', 'page-numbers')
    if page is not None:
        pages = []
        for li in page.find_all("li"):
            pages.append(li.text)
        return int(pages[-2])  # Get the second last item which is the last page number
    else:
        return 1

def get_comic_info(comic):
    comics = []
    for c in comic:
        title = c.find('a', attrs={"class": None}).text
        link_comic = c.find('a', attrs={"class": None}).get('href')
        comics.append({'title': title, 'link': link_comic})
    return comics

def fetch_comics_from_page(url, headers):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup.find_all('div', 'post-info'), soup

@app.route('/', methods=['GET', 'POST'])
def index():
    search_url = None
    results = None
    if request.method == 'POST':
        search_item = request.form['keyword']
        search_item = convert_keyword(search_item)
        search_url = 'https://getcomics.info/?s={}'.format(search_item)
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        
        # Fetch comics from the first page
        comic, soup = fetch_comics_from_page(search_url, headers)
        results = get_comic_info(comic)
        
        # Check for pagination and fetch comics from remaining pages
        total_page = check_pagination(soup)
        if total_page > 1:
            for page_number in range(2, total_page + 1):
                url = url_maker(page_number, search_item)
                comic, _ = fetch_comics_from_page(url, headers)
                results.extend(get_comic_info(comic))
        
        # Sort results by title
        results.sort(key=lambda x: x['title'])
    
    return render_template('index.html', search_url=search_url, results=results)

if __name__ == '__main__':
    app.run(debug=True)