from vectorModel import rank, Corpus

if __name__ == "__main__":
    print "Using Functions"
    useTfIdf = True
    print rank(query="spada oggetto", useTfIdf=useTfIdf)
    print rank(query="un che", useTfIdf=useTfIdf)
    print rank(query="mattina sole", useTfIdf=useTfIdf)
    print "Using Objects"
    corpus = Corpus()
    corpus.useTfIdf = True
    print corpus.rank(query="spada oggetto")
    print corpus.rank(query="un che")
    print corpus.rank(query="mattina sole")
