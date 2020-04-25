import regex as re
import requests
from bs4 import BeautifulSoup


class NewsProvider:
    def __init__(self, searchItem, number):
        self.searchItem = searchItem
        self.number = number

    def getGoogleLinks(self):
        g_clean = []
        url = 'https://news.google.com/rss/search?q={}'.format(self.searchItem)
        try:
            html = requests.get(url)
            if html.status_code == 200:
                soup = BeautifulSoup(html.text, 'lxml')
                links = soup.find_all('body')
                body = links[0].text
                soup = BeautifulSoup(body, 'lxml')
                a = soup.find_all('a')
                for i in a:
                    k = i.get('href')
                    g_clean.append(k)
        except Exception as ex:
            print(str(ex))
        finally:
            return g_clean

    def getNews(self):
        links = self.getGoogleLinks()
        news = {}
        for item in range(self.number):
            # Get the text of article
            link = links[item]
            article = requests.get(link)
            soup = BeautifulSoup(article.text, "html.parser")
            for script in soup(["script", "style", "meta", "noscript"]):
                script.extract()  # rip it out
            text = soup.get_text()
            text = text.replace("\n", "")
            # Get the source
            source_1 = re.search('\.\\s*([^.]*)', link).group(1)
            source_2 = re.search('//\\s*([^.]*)', link).group(1)
            if "/" in source_1:
                source = source_2
            else:
                source = source_1
            news[source] = text
        return news
