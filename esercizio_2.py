import math
import string

doc1 = (
    "doc1",
    """L'enorme quantità di informazioni presentinelle pagine Web rende necessario l'uso di strumenti automatici per il recupero di informazioni"""
)

doc2 = (
    "doc2",
    """I presenti hanno descritto le fasi del recupero dell’enorme relitto ma le informazioni non concordano su tipo e quantità di strumenti in uso"""
)

doc3 = (
    "doc3",
    """E' stato presentato nel Web un documento che informa sulle enormi difficoltà che incontra chi usa uno strumento informativo automatico"""
)


class Point2D:

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


class Point3D(Point2D):

    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

    def __str__(self):
        return "({},{},{})".format(self.x, self.y, self.z)


translator = str.maketrans('', '', string.punctuation)


class BooleanModel:

    def __init__(self, query, docs=[doc1, doc2, doc3]):
        self.query = query
        self.docs = docs
        self.tokens = {doc[0]: self.__tokenize(doc[1]) for doc in self.docs}
        self.result = set([doc[0] for doc in self.docs if query.lower() in self.tokens[doc[0]]])

    def __str__(self):
        return str(self.result)

    def __and__(self, other):
        self.result = set.intersection(self.result, other.result)
        return self

    def __or__(self, other):
        self.result = set.union(self.result, other.result)
        return self

    def __invert__(self):
        self.result = {doc for doc in self.tokens if self.query not in self.tokens[doc]}
        self.result = set([doc for doc in self.tokens if self.query not in self.tokens[doc]])
        return self

    def __tokenize(self, doc):
        return [word.translate(translator).lower() for word in doc.split()]


if __name__ == '__main__':
    print(BooleanModel("recupero"))
    print(BooleanModel("recupero"))
    print(BooleanModel("recupero") & BooleanModel("Web"))
    print(BooleanModel("recupero") | BooleanModel("Web"))
    print(~BooleanModel("recupero"))
