import random
import re
import string

from nltk import PorterStemmer, WordNetLemmatizer, word_tokenize
from nltk.corpus import movie_reviews
from nltk.corpus import wordnet as wn, stopwords
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import warnings

DOMAIN_STOP_WORDS = """
trunk build commit branch patch
release bug regression close fix
"""


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


def decision_tree_example(criterion='entropy'):
    iris = datasets.load_iris()
    x = iris.data[:, [2, 3]]
    y = iris.target
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=0)
    tree = DecisionTreeClassifier(criterion=criterion, max_depth=3, random_state=0)

    tree.fit(x_train, y_train)

    X_combined = np.vstack((x_train, x_test))
    y_combined = np.hstack((y_train, y_test))
    plot_decision_regions(X_combined, y_combined,
                          classifier=tree, test_idx=range(105, 150))

    plt.xlabel('petal length [cm]')
    plt.ylabel('petal width [cm]')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()


def domain_stop_words():
    return re.split("\n| |\t", DOMAIN_STOP_WORDS)


class LemmaTokenizer(object):
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def lemmatize(self, w):
        return self.lemmatizer.lemmatize(w)

    def __call__(self, doc):
        stop = stopwords.words('english')
        return [self.lemmatize(t) for t in word_tokenize(doc) if
                t not in string.punctuation and
                self.lemmatize(t) not in domain_stop_words() and
                t not in stop and
                wn.synsets(t)]


def random_forest_example():
    classifier = Pipeline([
        ('vect', TfidfVectorizer(strip_accents='unicode',
                                 tokenizer=word_tokenize,
                                 stop_words='english',
                                 decode_error='ignore',
                                 analyzer='word',
                                 norm='l2',
                                 ngram_range=(1, 2)
                                 )),
        ('clf', RandomForestClassifier(n_jobs=2, random_state=0))
    ])
    documents = [(movie_reviews.raw(fileid), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    documents = documents[:100]
    x_data = [doc[0] for doc in documents]
    y_data = [doc[1] for doc in documents]
    x_train, x_test, y_train, y_test = train_test_split(
        x_data, y_data,
        test_size=0.33,
        random_state=42
    )
    classifier.fit(x_train, y_train)
    predicted = classifier.predict(x_test)
    print(accuracy_score(y_test, predicted))
    print(precision_recall_fscore_support(y_test, predicted))
    print(classification_report(y_test, predicted))


if __name__ == '__main__':
    decision_tree_example('entropy')
    decision_tree_example('gini')
    random_forest_example()
