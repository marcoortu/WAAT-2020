from vectorModel import rank

if __name__ == "__main__":
    useTfIdf = True
    print rank(query="spada oggetto", useTfIdf=useTfIdf)
    print rank(query="un che", useTfIdf=useTfIdf)
    print rank(query="mattina sole", useTfIdf=useTfIdf)
