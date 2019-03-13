# coding=utf-8
from __future__ import division

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

docs = [doc1, doc2, doc3]


def rank(query, corpus=docs, useTfIdf=False):
    ranking = [(doc[0], cosineSimilarity(('query', query), doc, useTfIdf)) for doc in corpus]
    ranking = sorted(ranking, key=lambda rank: rank[1], reverse=True)
    return ranking


def cosineSimilarity(document1, document2, useTfIdf=False):
    vector1 = vectorize(document1, useTfIdf=useTfIdf)
    vector2 = vectorize(document2, useTfIdf=useTfIdf)
    normProduct = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    return vector1.dot(vector2) / normProduct if normProduct else 0


def vectorize(document, corpus=docs, useTfIdf=False):
    terms = set([term for doc in corpus for term in tokenize(doc)])
    terms = sorted(terms)
    weightFunction = tfIdfWeight if useTfIdf else binaryWeight
    return np.array([weightFunction(term, document) for term in terms])


def tokenize(doc):
    return [w.lower() for w in re.split('\W+', doc[1]) if w]


def binaryWeight(term, document):
    documentTerms = set([word for word in tokenize(document)])
    return 1 if term in documentTerms else 0


def tfIdfWeight(term, document, corpus=docs):
    documentTerms = tokenize(document)
    corpusList = [doc[0] for doc in corpus if term in tokenize(doc)]
    maxTermFreq = max([tokenize(doc).count(term) for doc in corpus])
    idf = np.log(len(corpus) / len(corpusList)) if len(corpusList) else 0
    tf = documentTerms.count(term) / maxTermFreq
    return tf * idf


class Document(object):

    def __init__(self, name, text):
        self.name, self.text = name, text


corpus = [Document(doc1[0], doc1[1]),
          Document(doc2[0], doc2[1]),
          Document(doc3[0], doc3[1])]


class Corpus(object):

    def __init__(self, corpus=corpus):
        self.corpus = corpus
        self.terms = set([term for doc in self.corpus for term in self.tokenize(doc)])
        self.useTfIdf = True

    def vectorize(self, doc):
        weightFunction = self.tfIdfWeight if self.useTfIdf else self.binaryWeight
        return np.array([weightFunction(term, doc) for term in self.terms])

    def tokenize(self, doc):
        return [w.lower() for w in re.split('\W+', doc.text) if w]

    def cosineSimilarity(self, doc1, doc2):
        vector1 = self.vectorize(doc1)
        vector2 = self.vectorize(doc2)
        normProduct = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        return vector1.dot(vector2) / normProduct if normProduct else 0

    def binaryWeight(self, term, doc):
        documentTerms = set([word for word in self.tokenize(doc)])
        return 1 if term in documentTerms else 0

    def tfIdfWeight(self, term, document):
        documentTerms = self.tokenize(document)
        corpusTermList = [doc.name for doc in self.corpus if term in self.tokenize(doc)]
        maxTermFreq = max([self.tokenize(doc).count(term) for doc in self.corpus])
        idf = np.log(len(self.corpus) / len(corpusTermList)) if len(corpusTermList) else 0
        tf = documentTerms.count(term) / maxTermFreq
        return tf * idf

    def rank(self, query):
        docQuery = Document('', query)
        ranking = [(doc.name, self.cosineSimilarity(docQuery, doc)) for doc in self.corpus]
        ranking = sorted(ranking, key=lambda rank: rank[1], reverse=True)
        return ranking
