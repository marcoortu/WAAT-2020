import string

import nltk
import pandas as pd
from nltk.corpus import CategorizedPlaintextCorpusReader

translator = str.maketrans('', '', string.punctuation)


class AuthorSentimentAnalyzer(object):

    def __init__(self):
        self.lexicon = pd.read_csv("sentiment/sentix.csv",
                                   sep="\t",
                                   encoding='latin1')
        self.max_feature = 500
        self.corpus = CategorizedPlaintextCorpusReader(
            './corpora/',
            r'.*\.txt',
            cat_pattern=r'(\w+)/*',
            encoding='latin-1'
        )
        self.freq_dists = {}
        self.stopwords = nltk.corpus.stopwords.words('italian')
        for author in self.get_authors():
            self.freq_dists[author] = nltk.FreqDist(self.filter_stop_words(author))

    def filter_stop_words(self, author):
        words = map(lambda w: w.translate(translator).lower(), self.corpus.words(categories=author))
        return [w for w in words if w and w not in self.stopwords]

    def get_authors(self):
        return self.corpus.categories()

    def get_most_common_words(self, author):
        return [t[0] for t in self.freq_dists[author].most_common(self.max_feature)]

    def get_sentiment(self, author):
        sentiment = 0
        for token in self.get_most_common_words(author):
            sentiment += self.calculate_sentiment(token)
        return sentiment / self.max_feature * 100

    def calculate_sentiment(self, token):
        lemma_sentiment = 0
        for row in self.lexicon[self.lexicon['lemma'] == token].values:
            lemma_sentiment += float(row[4]) - float(row[3])
        return lemma_sentiment


if __name__ == "__main__":
    clf = AuthorSentimentAnalyzer()
    print(clf.get_sentiment('deledda'))
    print(clf.get_sentiment('pirandello'))
