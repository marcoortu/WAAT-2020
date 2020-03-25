import re
import numpy as np

doc1 = (
    "doc1",
    """Era un oggetto troppo grande per chiamarlo spada. Troppo spesso, troppo pesante e grezzo. 
    Non era altro che un enorme blocco di ferro.
    """
)

doc2 = (
    "doc2",
    """Fu allora che vidi il Pendolo. La sfera, mobile all'estremità di un lungo filo fissato alla volta del coro, descriveva 
    le sue  ampie oscillazioni con isocrona maestà. 
    """
)

doc3 = (
    "doc3",
    """Era una bella mattina di fine novembre. Nella notte aveva nevicato un poco,
    ma il terreno era coperto di un velo fresco non più alto di tre dita. Al buio, subito
    dopo laudi, avevamo ascoltato la messa in un villaggio a valle. Poi ci eravamo messi
    in viaggio verso le montagne, allo spuntar del sole.
    Come ci inerpicavamo per il sentiero scosceso che si snodava intorno al monte,
    vidi l'abbazia
    """
)

docs = (doc1, doc2, doc3)


def rank(query, corpus=docs, use_tfidf=False):
    ranking = [(doc[0], cosine_similarity(('query', query), doc, use_tfidf)) for doc in corpus]
    ranking = sorted(ranking, key=lambda rank: rank[1], reverse=True)
    return ranking


def cosine_similarity(document1, document2, useTfIdf=False):
    vector1 = vectorize(document1, use_tfidf=useTfIdf)
    vector2 = vectorize(document2, use_tfidf=useTfIdf)
    norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    return vector1.dot(vector2) / norm_product if norm_product else 0


def vectorize(document, corpus=docs, use_tfidf=False):
    terms = set([term for doc in corpus for term in tokenize(doc)])
    terms = sorted(terms)
    weight_function = tfidf_weight if use_tfidf else binary_weight
    return np.array([weight_function(term, document) for term in terms])


def tokenize(doc):
    return [w.lower() for w in re.split('\W+', doc[1]) if w]


def binary_weight(term, document):
    document_terms = set([word for word in tokenize(document)])
    return 1 if term in document_terms else 0


def tfidf_weight(term, document, corpus=docs):
    document_terms = tokenize(document)
    corpus_list = [doc[0] for doc in corpus if term in tokenize(doc)]
    max_term_freq = max([tokenize(doc).count(term) for doc in corpus])
    idf = np.log(len(corpus) / len(corpus_list)) if len(corpus_list) else 0
    tf = document_terms.count(term) / max_term_freq
    return tf * idf


class Document(object):

    def __init__(self, name, text):
        self.name, self.text = name, text
        self.tokens = self.tokenize()
        self.max_freq = max([self.tokens.count(t) for t in self.tokens])

    def tokenize(self):
        return [w.lower() for w in re.split(r'\W+', self.text) if w]

    def tf(self, token):
        return self.tokens.count(token) / self.max_freq

    def binary(self, term):
        return 1 if term in self.tokens else 0


corpus = [Document(doc1[0], doc1[1]),
          Document(doc2[0], doc2[1]),
          Document(doc3[0], doc3[1])]


class Corpus:
    corpus = corpus

    def __init__(self):
        self.terms = {term for doc in self.corpus for term in doc.tokenize()}
        self.use_tf_idf = True

    def vectorize(self, doc):
        return np.array([self.weight(term, doc) for term in self.terms])

    def cosine_similarity(self, doc1, doc2):
        vector1 = self.vectorize(doc1)
        vector2 = self.vectorize(doc2)
        norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        return vector1.dot(vector2) / norm_product if norm_product else 0

    def idf(self, term):
        corpus_term_docs = len([doc.name for doc in self.corpus if term in doc.tokenize()])
        return np.log(len(self.corpus) / corpus_term_docs) if corpus_term_docs else 0

    def weight(self, term, doc):
        if self.use_tf_idf:
            return doc.tf(term) * self.idf(term)
        return doc.binary(term)

    def rank(self, query):
        doc_query = Document('', query)
        ranking = [(doc.name, self.cosine_similarity(doc_query, doc)) for doc in self.corpus]
        ranking = sorted(ranking, key=lambda r: r[1], reverse=True)
        return ranking
