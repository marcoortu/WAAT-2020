# coding=utf-8
import string

docs = [(
    "doc1",
    """L'enorme quantità di informazioni presentinelle pagine Web rende necessario
     l'uso di strumenti automatici per il recupero di informazioni"""
), (
    "doc2",
    """I presenti hanno descritto le fasi del recupero dell’enorme relitto ma le 
    informazioni non concordano su tipo e quantità di strumenti in uso"""
), (
    "doc3",
    """E' stato presentato nel Web un documento che informa sulle enormi difficoltà 
    che incontra chi usa uno strumento informativo automatico"""
)]

translator = str.maketrans('', '', string.punctuation)


def tokenize(doc):
    words = doc.split()
    return [word.translate(translator).lower() for word in words]


def match(query, negation=False, docs=docs):
    tokens = {doc[0]: tokenize(doc[1]) for doc in docs}
    if negation:
        return {doc for doc in tokens if query.lower() not in tokens[doc]}
    return {doc for doc in tokens if query.lower() in tokens[doc]}


class BooleanModel(object):

    def __init__(self, query, docs=docs):
        self.tokens = {}
        self.query = query
        self.docs = docs
        self.tokens = {doc[0]: tokenize(doc[1]) for doc in self.docs}
        self.result = {doc for doc in self.tokens if self.query in self.tokens[doc]}

    def __and__(self, other):
        self.result = set.intersection(*[self.result, other.result])
        return self

    def __or__(self, other):
        self.result = set.union(*[self.result, other.result])
        return self

    def __invert__(self):
        self.result = {doc for doc in self.tokens if self.query not in self.tokens[doc]}
        return self

    def __str__(self):
        return " ".join(list(self.result))
