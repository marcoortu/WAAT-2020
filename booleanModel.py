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


class BooleanModel(object):

    def __init__(self, queryString, docs=docs):
        self.tokens = {}
        self.query = queryString
        self.docs = docs
        for doc in self.docs:
            self.tokens[doc[0]] = tokenize(doc[1])
        self.result = set([k for k in self.tokens.keys() if self.query in self.tokens[k]])

    def __and__(self, other):
        self.result = set.intersection(*[self.result, other.result])
        return self

    def __or__(self, other):
        self.result = set.union(*[self.result, other.result])
        return self

    def __invert__(self):
        self.result = set([k for k in self.tokens.keys() if self.query not in self.tokens[k]])
        return self

    def __str__(self):
        return " ".join(list(self.result))


def tokenize(doc):
    words = doc.split()
    return [word.translate(None, string.punctuation).lower() for word in words]


def match(query, negation=False, docs=docs):
    tokens = {}
    for doc in docs:
        tokens[doc[0]] = tokenize(doc[1])
    if negation:
        return set([k for k in tokens.keys() if query.lower() not in tokens[k]])
    return set([k for k in tokens.keys() if query.lower() in tokens[k]])






if __name__ == "__main__":
    print "Using Fufunctions:"
    print match("recupero") & match("web")
    print match("recupero") | match("web")
    print match("recupero") & match("relitto", negation=True)
    print (match("web") | match("uso")) & match("strumenti")
    print (match("uso") | match("web")) & match("strumenti", negation=True)
    print match("informazioni") & match("relitto") & match("studente")
    print match("informazioni") | match("relitto") | match("studente")
    print match("bologna") | match("padova", negation=True)
    print "Using Objects:"
    print BooleanModel("recupero") & BooleanModel("web")
    print BooleanModel("recupero") | BooleanModel("web")
    print BooleanModel("recupero") & ~BooleanModel("relitto")
    print (BooleanModel("web") | BooleanModel("uso")) & BooleanModel("strumenti")
    print (BooleanModel("uso") | BooleanModel("web")) & ~BooleanModel("strumenti")
    print BooleanModel("informazioni") & BooleanModel("relitto") & BooleanModel("studente")
    print BooleanModel("informazioni") | BooleanModel("relitto") | BooleanModel("studente")
    print BooleanModel("bologna") | ~BooleanModel("padova")
