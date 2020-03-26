from urllib.parse import urlparse

import networkx as nx
import pylab as plt

from crawler import Crawler

if __name__ == '__main__':
    url = urlparse('http://info.cern.ch/hypertext/WWW/TheProject.html')
    web = Crawler(url, max_depth=2).crawl_page(url)  # or web = crawler(url) if using functions
    web_graph = nx.DiGraph()
    edges = []
    for page in web:
        for link in page.links:
            edges.append((hash(page.address), hash(link)))
    web_graph.add_edges_from(edges)
    nx.draw(web_graph)
    plt.show()
    pageRanks = nx.pagerank(web_graph)
    pages = [page.set_page_rank(pageRanks[hash(page.address)]) for page in web]
    pages = sorted(pages, key=lambda p: p.page_rank, reverse=True)
    for page in pages:
        print(page)
    print(pages[0].text)
