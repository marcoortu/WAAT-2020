from invertedIndex import createInvertedIndex, find, findSequential, doc1, doc2, doc3

if __name__ == "__main__":
    invertedIndex = createInvertedIndex(docs=[doc1, doc2, doc3])
    print find(invertedIndex, ["un", "atto"])
    print find(invertedIndex, ["un", "animale"])
    print findSequential(invertedIndex, ["animale", "un"])
