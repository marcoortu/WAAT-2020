from urllib.parse import urlparse

import networkx as nx
import pylab as plt

from crawler import Crawler, Page

if __name__ == '__main__':
    stat_page = Page('http://info.cern.ch/hypertext/WWW/TheProject.html')
    crawler = Crawler(stat_page, max_depth=2)
    crawler.crawl()
    web_graph = nx.DiGraph()
    edges = []
    for page in crawler.web:
        for link in page.links:
            edges.append((hash(page.address), hash(link)))
    web_graph.add_edges_from(edges)
    nx.draw(web_graph)
    plt.show()
    pageRanks = nx.pagerank(web_graph)
    for page in crawler.web:
        page.page_rank = pageRanks[hash(page.address)]
    pages = sorted(crawler.web, key=lambda p: p.page_rank, reverse=True)
    for page in pages:
        print(page)
    print(pages[0].text)
    print(pages[0].links)
    print(pages[0].text)
