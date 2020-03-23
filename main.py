from vector_model import rank, Corpus

if __name__ == "__main__":
    print("Using Functions")
    use_tfidf = True
    print(rank(query="spada oggetto", use_tfidf=use_tfidf))
    print(rank(query="un che", use_tfidf=use_tfidf))
    print(rank(query="mattina sole", use_tfidf=use_tfidf))
    print("Using Objects")
    corpus = Corpus()
    print(corpus.rank(query="spada oggetto"))
    print(corpus.rank(query="un che"))
    print(corpus.rank(query="mattina sole"))
