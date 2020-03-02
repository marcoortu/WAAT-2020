import string
from collections import defaultdict

translator = str.maketrans('', '', string.punctuation)

doc1 = (
    "doc1",
    """una mattina, svegliandosi da sogni irrequieti Gregor Samsa
    si trovo nel suo letto trasformato in un insetto mostruoso
    """
)

doc2 = (
    "doc2",
    """Voi che trovate quando tornate a casa il cibo caldo e visi amici 
    Considerate se questo è un uomo
    """
)

doc3 = (
    "doc3",
    """Vidi un magnifico disegno rappresentava un serpente boa 
    nell atto di inghiottire un animale
    """
)

doc4 = (
    "doc4",
    """animale Vidi un magnifico disegno rappresentava un serpente boa 
    nell atto di inghiottire un 
    """
)


class InvertedIndex(object):

    def __init__(self, docs: list):
        self.inverted_indexes = defaultdict(list)
        for doc in docs:
            index = self.get_index_occurrence(doc)
            self.update(index, doc[0])

    def update(self, indexes, doc_name):
        for index in indexes:
            self.inverted_indexes[index[0]].append((doc_name, index[1]))

    def __str__(self):
        return str(self.inverted_indexes)

    def __iter__(self):
        return iter(self.inverted_indexes.items())

    def get_index_occurrence(self, doc):
        words = map(lambda w: w.translate(translator), doc[1].split())
        return map(lambda t: (t[1], t[0] + 1), enumerate(words))

    def find(self, query=[]):
        if any(map(lambda t: t not in self.inverted_indexes.keys(), query)):
            return []
        docs = map(lambda term: set([t[0] for t in self.inverted_indexes[term]]),
                   query)
        return list(set.intersection(*docs))

    def find_sequential(self, query=[]):
        doc_dict = defaultdict(list)
        retrieved_docs = []
        for term in filter(lambda t: t in self.inverted_indexes.keys(), query):
            for t in filter(lambda t: t[0] in self.find(query), self.inverted_indexes[term]):
                doc_dict[t[0]].append(t[1])
        for key in doc_dict.keys():
            doc_dict[key] = sorted(doc_dict[key])
            doc_dict[key] = [abs(doc_dict[key][i] - doc_dict[key][i + 1])
                             for i in range(0, len(doc_dict[key]) - 1)]
            if 1 in doc_dict[key]:
                retrieved_docs.append(key)
        return retrieved_docs


def index_occurrence(doc):
    words = doc[1].split()
    words = [word.translate(translator) for word in words]
    return [(word, i + 1) for i, word in enumerate(words)]


def create_inverted_index(docs=[]):
    inverted_index = {}
    for doc in docs:
        for index in index_occurrence(doc):
            if index[0] in inverted_index.keys():
                inverted_index[index[0]].append((doc[0], index[1]))
            else:
                inverted_index[index[0]] = [(doc[0], index[1])]
    return inverted_index


def find(inverted_index={}, query=[]):
    docs = []
    if any(map(lambda t: t not in inverted_index.keys(), query)):
        return []
    for term in query:
        if term in inverted_index.keys():
            docs.append(set([t[0] for t in inverted_index[term]]))
    return list(set.intersection(*docs))


def find_sequential(inverted_index={}, query=[]):
    docs = find(inverted_index, query)
    doc_dict = {}
    retrieved_docs = []
    for term in query:
        if term in inverted_index.keys():
            for t in [t for t in inverted_index[term] if t[0] in docs]:
                if t[0] in doc_dict.keys():
                    doc_dict[t[0]].append(t[1])
                else:
                    doc_dict[t[0]] = [t[1]]
    for key in doc_dict.keys():
        doc_dict[key] = sorted(doc_dict[key])
        doc_dict[key] = [abs(doc_dict[key][i] - doc_dict[key][i + 1])
                         for i in range(0, len(doc_dict[key]) - 1)]
        if 1 in doc_dict[key]:
            retrieved_docs.append(key)
    return retrieved_docs
