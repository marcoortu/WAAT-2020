import string

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

    def __init__(self, docs):
        self.invertedIndexes = {}
        for doc in docs:
            index = self.getIndexOccurence(doc)
            self.update(index, doc[0])

    def update(self, indexes, docName):
        for index in indexes:
            if index[0] in self.invertedIndexes.keys():
                self.invertedIndexes[index[0]].append((docName, index[1]))
            else:
                self.invertedIndexes[index[0]] = [(docName, index[1])]

    def __str__(self):
        return str(self.invertedIndexes)

    def __iter__(self):
        return iter(self.invertedIndexes.items())

    def getIndexOccurence(self, doc):
        words = doc[1].split()
        words = [word.translate(translator) for word in words]
        index = []
        for i, word in enumerate(words):
            index.append((word, i + 1))
        return index


def getIndexOccurence(doc):
    words = doc[1].split()
    words = [word.translate(translator) for word in words]
    return [(word, i + 1) for i, word in enumerate(words)]


def createInvertedIndex(docs=[]):
    invertedIndex = {}
    for doc in docs:
        for index in getIndexOccurence(doc):
            if index[0] in invertedIndex.keys():
                invertedIndex[index[0]].append((doc[0], index[1]))
            else:
                invertedIndex[index[0]] = [(doc[0], index[1])]
    return invertedIndex


def find(invertedIndex={}, query=[]):
    docs = []
    for term in query:
        if term in invertedIndex.keys():
            docs.append(set([t[0] for t in invertedIndex[term]]))
    return list(set.intersection(*docs))


def findSequential(invertedIndex={}, query=[]):
    docs = find(invertedIndex, query)
    docDict = {}
    retrievedDocs = []
    for term in query:
        if term in invertedIndex.keys():
            for t in [t for t in invertedIndex[term] if t[0] in docs]:
                if t[0] in docDict.keys():
                    docDict[t[0]].append(t[1])
                else:
                    docDict[t[0]] = [t[1]]
    for key in docDict.keys():
        docDict[key] = sorted(docDict[key])
        docDict[key] = [abs(docDict[key][i] - docDict[key][i + 1])
                        for i in range(0, len(docDict[key]) - 1)]
        if 1 in docDict[key]:
            retrievedDocs.append(key)
    return retrievedDocs
