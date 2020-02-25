from inverted_index import create_inverted_index, doc1, doc2, doc3, find, find_sequential, InvertedIndex

if __name__ == "__main__":
    # With Functions
    # inv_indexes = create_inverted_index(docs=[doc1, doc2, doc3])
    # print(find(inv_indexes, ["un", "atto"]))
    # print(find(inv_indexes, ["un", "animale"]))
    # print(find_sequential(inv_indexes, ["animale", "un"]))

    # With Classes
    inv_indexes = InvertedIndex(docs=[doc1, doc2, doc3])
    print(inv_indexes.find(["un", "atto"]))
    print(inv_indexes.find(["un", "animale"]))
    print(inv_indexes.find_sequential(["animale", "un"]))
