from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup


class Page:

    def __init__(self, address):
        self.url = urlparse(address)
        page = requests.get(self.url.geturl())
        soup = BeautifulSoup(page.text, "html.parser")
        self.address = address
        self.links = [a['href'] for a in soup.find_all('a')]
        self.text = page.text
        self.page_rank = 0
        self._parse_urls()

    def __str__(self):
        return "{}: {:.3f}".format(self.address, self.page_rank)

    def _parse_urls(self):
        external_links = []
        for link in self.links:
            external_url = urlparse(link)
            if not external_url.netloc:
                external_links.append(urlparse(urljoin(self.url.geturl(), external_url.path)))
            else:
                external_links.append(external_url)
        self.links = [l.geturl() for l in external_links]


class Crawler:

    def __init__(self, start_page, max_depth=2):
        self.start_page, self.max_depth = start_page, max_depth

    def crawl_page(self, page, depth):
        print("{} : {}".format(depth, page.address))
        if depth > self.max_depth:
            return
        for link in page.links:
            page = Page(link)
            self.crawl_page(page, depth + 1)

    def crawl(self):
        self.crawl_page(self.start_page, 1)


if __name__ == '__main__':
    stat_page = Page('http://info.cern.ch/hypertext/WWW/TheProject.html')
    crawler = Crawler(stat_page)
    crawler.crawl()
