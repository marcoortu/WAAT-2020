import pandas as pd

from nltk.corpus import wordnet as wn

from classification import movie_review_classification
from nltk_examples import hyponym_graph, graph_draw

if __name__ == '__main__':
    # Semantic Graph Visualization
    dog = wn.synset('dog.n.01')
    graph = hyponym_graph(dog)
    graph_draw(graph)
    # Pandas example: extraction of text data from csv files
    rows = pd.read_csv("./corpora/post_comments.csv").to_dict('records')
    print(rows[0])
    print(rows[0]['comment_id'])
    print(rows[0]['comment_text'])
    # Classification example with NLTK
    movie_review_classification()
