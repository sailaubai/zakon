import requests
from bs4 import BeautifulSoup as BS
import sys
from datetime import datetime

HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}


def get_content(url):
    res = requests.get(url, headers=HEADERS)
    if res.status_code == requests.codes.ok:
        dt = datetime.strptime(res.headers.get('Date'), '%a, %d %b %Y %H:%M:%S GMT')  # дата тут по гринвичу, так и оставлю
        news_id = url.split('/')[-1].split('-')[0]  # ID в числовом виде где то в html есть, но дешевле так брать
        html = BS(res.text, "html.parser")
        title = html.title.string
        container = html.find("div", {"id": "initial_news_story"}).find_all("p")
        content = " ".join(p.get_text() for p in container[:-1])
        '''
        или 
        content = html.find("div", {"id": "initial_news_story"}).get_text()
        '''
        result = {
            'url': url,
            'news_id': news_id,
            'date': dt.strftime("%s"),
            'title': title,
            'text': content
        }
        return result
    return None


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(get_content(sys.argv[1]))
    else:
        print('Wrong command line args')
