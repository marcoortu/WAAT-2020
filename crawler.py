import requests
import networkx as nx
import pylab as plt

from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup


class Page:

    def __init__(self, address):
        self.url = urlparse(address)
        self.address = address
        self.page_rank = 0
        self.links = {}
        self.text = ''
        try:
            page = requests.get(self.url.geturl()).text
            soup = BeautifulSoup(page, "html.parser")
            self.links = {a['href'] for a in soup.find_all('a', href=True)}
            self.text = soup.text
            self._parse_urls()
        except Exception:
            raise ConnectionError()

    def __str__(self):
        return "{}: {:.3f}".format(self.address, self.page_rank)

    def __eq__(self, other):
        return self.address == other.address

    def __hash__(self):
        return hash(self.address)

    def _parse_urls(self):
        external_links = []
        for link in self.links:
            external_url = urlparse(link)
            if not external_url.netloc:
                external_links.append(urlparse(urljoin(self.url.geturl(), external_url.path)))
            else:
                external_links.append(external_url)
        self.links = {link.geturl() for link in external_links}


class Crawler:

    def __init__(self, start_page, max_depth=1):
        self.start_page, self.max_depth = start_page, max_depth
        self.web = {start_page}

    def crawl_page(self, page, depth):
        if depth >= self.max_depth:
            return
        print("{} : {}".format(depth, page.address))
        for link in page.links:
            if not self.visited(link):
                try:
                    new_page = Page(link)
                    self.crawl_page(new_page, depth + 1)
                    self.web.add(new_page)
                except ConnectionError:
                    return

    def visited(self, link):
        return link in [p.address for p in self.web]

    def crawl(self):
        self.crawl_page(self.start_page, 0)
