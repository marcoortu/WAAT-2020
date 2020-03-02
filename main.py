from inverted_index import create_inverted_index, doc1, doc2, doc3, find, find_sequential, InvertedIndex

if __name__ == "__main__":
    # With Functions
    inv_index = create_inverted_index(docs=[doc1, doc2, doc3])
    print(find(inv_index, ["un", "atto"]))
    print(find_sequential(inv_index, ["un", "atto"]))
    print(find(inv_index, ["un", "animale"]))

    # With Classes
    inv_index = InvertedIndex(docs=[doc1, doc2, doc3])
    print(inv_index.find(["un", "atto"]))
    print(inv_index.find_sequential(["un", "atto"]))
    print(inv_index.find(["un", "animale"]))
