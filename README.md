# WAAT-2020


## Esercitazione 4

Sfruttare la libreria BeautifulSoup e NetworkX per implementare una versione semplificata di un crawler e del PageRank


### Esercizio 1

La prima pagina web mai pubblicata si trova all'indirizzo *http://info.cern.ch/hypertext/WWW/TheProject.html*.
Utilizzare Beautifulsoup per fare il crawling del web _primordiale_, utilizzando una ricerca di tipo Breadth-First con una profondità
massima pari a 2. Ottenere un elenco di pagine a cui sono associate le pagine collegate.

```python
import requests
from bs4 import BeautifulSoup

page = requests.get('http://info.cern.ch/hypertext/WWW/TheProject.html').text
soup = BeautifulSoup(page, "html.parser")

```

### Esercizio 2

Partendo dalla pagina iniziale *http://info.cern.ch/hypertext/WWW/TheProject.html* recuperare la _rete_ ottenuta nell'esercizio precedente per calcolare il PageRank delle pagine. 

Per calcolare il PageRank utlizzare la libreria *networkx*. Ad esempio calcolando il PageRank della seguente rete:
![alt text](imgs/web-graph2.gif "Esempio page rank")

si ottiene
- 'A': 0.155
- 'B': 0.316
- 'C': 0.276
- 'D': 0.281

Esempio:
```python
    import networkx as nx
    import matplotlib.pyplot as plt
    web = nx.DiGraph()
    web.add_edges_from([
        ('A', 'B'),
        ('B', 'D'),
        ('D', 'C'),
        ('C', 'B'),
        ('C', 'A'),
    ])
    pos = nx.circular_layout(web)
    nx.draw(web, with_labels=True, pos=pos)
    plt.show()
    print(nx.pagerank(web))
```


