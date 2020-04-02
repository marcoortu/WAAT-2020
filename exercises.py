import nltk
from nltk.corpus import CategorizedPlaintextCorpusReader, stopwords

root_dir = 'corpora'

italian_authors_corpus = CategorizedPlaintextCorpusReader(
    './%s/' % root_dir,
    r'.*\.txt',
    cat_pattern=r'(\w+)/*',
    encoding='latin-1'
)


def exercise1():
    """
    Utilizzare i testi di Grazia Deledda e Luigi Pirandello per confrontare la concordance e la similarity
    della parola donna. I testi si trovano nella cartella corpora.
    """
    grazia_deledda_tokens = italian_authors_corpus.words(categories='deledda')
    pirandello_tokens = italian_authors_corpus.words(categories='pirandello')
    grazia_deledda = nltk.Text(grazia_deledda_tokens)
    pirandello = nltk.Text(pirandello_tokens)
    print("Grazia Deledda")
    grazia_deledda.similar('donna')
    grazia_deledda.concordance('donna')
    print("Luigi Pirandello")
    pirandello.similar('donna')
    pirandello.concordance('donna')


def exercise2():
    """
    Utilizzare i testi di Grazia Deledda e Luigi Pirandello per confrontare le 30 parole, di lunghezza maggiore a 4, più
    comunemente  utilizzate dai due autori. Le stopwords vanno filtrate prima di effettuare il calcolo.
    """
    grazia_deledda_tokens = italian_authors_corpus.words(categories='deledda')
    pirandello_tokens = italian_authors_corpus.words(categories='pirandello')
    grazia_deledda = nltk.Text(grazia_deledda_tokens)
    pirandello = nltk.Text(pirandello_tokens)
    italian_stopwords = stopwords.words('italian')
    fdist1 = nltk.FreqDist([w for w in grazia_deledda if len(w) >= 4 and w not in italian_stopwords])
    fdist2 = nltk.FreqDist([w for w in pirandello if len(w) >= 4 and w not in italian_stopwords])
    print('Deledda')
    print(fdist1.most_common(30))
    print('Pirandello')
    print(fdist2.most_common(30))


def exercise3():
    """
    Ottenete una distribuzione di frequenza condizionale (per autore) per esaminare le differenze nelle lunghezze
    delle parole utilizzare dai due autori italiani.
    """
    print(italian_authors_corpus.fileids())
    print(italian_authors_corpus.categories())
    cfd = nltk.ConditionalFreqDist(
        (author, len(word))
        for author in ['deledda', 'pirandello']
        for word in italian_authors_corpus.words(categories=author))
    cfd.plot(cumulative=True)


if __name__ == '__main__':
    exercise1()
    exercise2()
    exercise3()
