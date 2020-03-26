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
    pageRanks = [(page.address, pageRanks[hash(page.address)]) for page in web]
    pageRanks = sorted(pageRanks, key=lambda p: p[1], reverse=True)
    for pageRank in pageRanks:
        print(pageRank)
    print(web[0].text)
