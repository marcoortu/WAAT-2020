from invertedIndex import createInvertedIndex, find, findSequential, doc1, doc2, doc3, InvertedIndex

if __name__ == "__main__":
    # With Functions
    invertedIndex = createInvertedIndex(docs=[doc1, doc2, doc3])
    print(find(invertedIndex, ["un", "atto"]))
    print(find(invertedIndex, ["un", "animale"]))
    print(findSequential(invertedIndex, ["animale", "un"]))

    # With Classes
    invertedIndex = InvertedIndex(docs=[doc1, doc2, doc3])
    print(invertedIndex.find(["un", "atto"]))
    print(invertedIndex.find(["un", "animale"]))
    print(invertedIndex.findSequential(["animale", "un"]))
