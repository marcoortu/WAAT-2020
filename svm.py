import random
import re
import string
import warnings

from matplotlib.colors import ListedColormap
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
import matplotlib.pyplot as plt
import numpy as np


def versiontuple(v):
    return tuple(map(int, (v.split("."))))


def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0],
                    y=X[y == cl, 1],
                    alpha=0.6,
                    c=cmap(idx),
                    edgecolor='black',
                    marker=markers[idx],
                    label=cl)

    # highlight test samples
    if test_idx:
        # plot all samples
        if not versiontuple(np.__version__) >= versiontuple('1.9.0'):
            X_test, y_test = X[list(test_idx), :], y[list(test_idx)]
            warnings.warn('Please update to NumPy 1.9.0 or newer')
        else:
            X_test, y_test = X[test_idx, :], y[test_idx]

        plt.scatter(X_test[:, 0],
                    X_test[:, 1],
                    c='',
                    alpha=1.0,
                    edgecolor='black',
                    linewidths=1,
                    marker='o',
                    s=55, label='test set')


def non_linear_classes():
    np.random.seed(0)
    X_xor = np.random.randn(200, 2)
    y_xor = np.logical_xor(X_xor[:, 0] > 0,
                           X_xor[:, 1] > 0)
    y_xor = np.where(y_xor, 1, -1)

    plt.scatter(X_xor[y_xor == 1, 0],
                X_xor[y_xor == 1, 1],
                c='b', marker='x',
                label='1')
    plt.scatter(X_xor[y_xor == -1, 0],
                X_xor[y_xor == -1, 1],
                c='r',
                marker='s',
                label='-1')

    plt.xlim([-3, 3])
    plt.ylim([-3, 3])
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()
    # Using a non linear kernel
    svm = SVC(kernel='rbf', random_state=0, gamma=0.10, C=10.0)
    svm.fit(X_xor, y_xor)
    plot_decision_regions(X_xor, y_xor,
                          classifier=svm)

    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()


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


def pipe_example():
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


if __name__ == '__main__':
    non_linear_classes()
