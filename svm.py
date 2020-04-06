import random
import re
import string

from nltk import PorterStemmer, WordNetLemmatizer, word_tokenize
from nltk.corpus import movie_reviews
from nltk.corpus import wordnet as wn, stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

DOMAIN_STOP_WORDS = """
trunk build commit branch patch
release bug regression close fix
"""


def domain_stop_words():
    return re.split(r'\n| |\t', DOMAIN_STOP_WORDS)


class LemmaTokenizer(object):
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def lemmatize(self, w):
        return self.lemmatizer.lemmatize(w)

    def __call__(self, doc):
        return [self.lemmatize(t) for t in word_tokenize(doc) if
                t not in string.punctuation and
                self.lemmatize(t) not in domain_stop_words() and
                t not in stopwords.words('english') and
                wn.synsets(t)]


if __name__ == '__main__':
    classifier = Pipeline([
        ('feature_vect', TfidfVectorizer(strip_accents='unicode',
                                         tokenizer=word_tokenize,
                                         stop_words='english',
                                         decode_error='ignore',
                                         analyzer='word',
                                         norm='l2',
                                         ngram_range=(1, 2)
                                         )),
        ('clf', SVC(probability=True,
                    C=10,
                    shrinking=True,
                    kernel='linear'))
    ])
    documents = [(movie_reviews.raw(fileid), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    documents = documents[:100]
    xData = [doc[0] for doc in documents]
    yData = [doc[1] for doc in documents]
    xTrain, xTest, yTrain, yTest = train_test_split(
        xData, yData,
        test_size=0.33,
        random_state=42
    )
    classifier.fit(xTrain, yTrain)
    predicted = classifier.predict(xTest)
    print(accuracy_score(yTest, predicted))
    print(precision_recall_fscore_support(yTest, predicted))
    print(classification_report(yTest, predicted))
