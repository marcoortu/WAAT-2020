from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup


class Page(object):

    def __init__(self, address, links, text=''):
        self.address, self.links, self.text = address, links, text


class Crawler(object):

    def __init__(self, start_url, max_depth=2):
        self.start_url, self.max_depth = start_url, max_depth
        self.web = []

    def crawl_pages(self, url, depth=0):
        if depth >= self.max_depth:
            return self.web
        try:
            page = requests.get(url.geturl()).text
        except Exception:
            return self.web
        soup = BeautifulSoup(page, "html.parser")
        links = []
        for anchor in soup.findAll('a', href=True):
            link = urlparse(anchor['href'])
            if not link.netloc:
                link = urlparse(urljoin(url.geturl(), link.path))
            links += [link.geturl()]
        visited = set([page.address for page in self.web])
        links = list(filter(lambda l: l not in visited, set(links)))
        self.web += [Page(url.geturl(), links, soup.text)]
        for link in links:
            self.crawl_pages(urlparse(link), depth + 1)
        return self.web


def crawler(url, depth=0, max_depth=2, web=[]):
    depth, url.geturl()
    if depth >= max_depth:
        return web
    try:
        page = requests.get(url.geturl()).text
    except Exception:
        return web
    soup = BeautifulSoup(page, "html.parser")
    links = []
    for anchor in soup.findAll('a', href=True):
        link = urlparse(anchor['href'])
        if not link.netloc:
            link = urlparse(urljoin(url.geturl(), link.path))
        links += [link.geturl()]
    visited = set([page.address for page in web])
    links = list(set(links))
    links = list(filter(lambda l: l not in visited, links))
    web += [Page(url.geturl(), links, soup.text)]
    for link in links:
        crawler(urlparse(link), depth + 1, max_depth, web)
    return web
