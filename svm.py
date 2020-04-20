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
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

from sklearn.metrics import roc_curve, auc
from scipy import interp

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


def plot_ROC(pipe_clf, x_train, y_train):
    X_train = np.array(x_train)
    Y_train = np.array(y_train)

    cv = list(StratifiedKFold(n_splits=3,
                              random_state=1).split(X_train, Y_train))

    fig = plt.figure(figsize=(7, 5))

    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)
    all_tpr = []

    for i, (train, test) in enumerate(cv):
        probas = pipe_clf.fit(X_train[train],
                              Y_train[train]).predict_proba(Y_train[test])

        fpr, tpr, thresholds = roc_curve(Y_train[test],
                                         probas[:, 1],
                                         pos_label=['pos'])
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr,
                 tpr,
                 lw=1,
                 label='ROC fold %d (area = %0.2f)'
                       % (i + 1, roc_auc))

    plt.plot([0, 1],
             [0, 1],
             linestyle='--',
             color=(0.6, 0.6, 0.6),
             label='random guessing')

    mean_tpr /= len(cv)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, 'k--',
             label='mean ROC (area = %0.2f)' % mean_auc, lw=2)
    plt.plot([0, 0, 1],
             [0, 1, 1],
             lw=2,
             linestyle=':',
             color='black',
             label='perfect performance')

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('false positive rate')
    plt.ylabel('true positive rate')
    plt.title('Receiver Operator Characteristic')
    plt.legend(loc="lower right")

    plt.tight_layout()
    # plt.savefig('./figures/roc.png', dpi=300)
    plt.show()


def pipe_example():
    pipeline_clf = Pipeline([
        ('feature_vect', TfidfVectorizer(strip_accents='unicode',
                                         tokenizer=word_tokenize,
                                         stop_words='english',
                                         decode_error='ignore',
                                         analyzer='word',
                                         norm='l2',
                                         ngram_range=(1, 2)
                                         )),
        ('clf', SVC(probability=True,
                    C=1,
                    shrinking=True,
                    kernel='rbf'))
    ])
    documents = [(movie_reviews.raw(fileid), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    documents = documents[:500]
    x_data = [doc[0] for doc in documents]
    y_data = [doc[1] for doc in documents]
    x_train, x_test, y_train, y_test = train_test_split(
        x_data, y_data,
        test_size=0.1,
        # random_state=42
    )
    pipeline_clf.fit(x_train, y_train)
    y_pred = pipeline_clf.predict(x_test)
    print(accuracy_score(y_test, y_pred))
    print(precision_recall_fscore_support(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    conf_matrix = confusion_matrix(y_true=y_test, y_pred=y_pred)
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    ax.matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax.text(x=j, y=i, s=conf_matrix[i, j], va='center', ha='center')
    print(conf_matrix)
    plt.xlabel('y_pred label')
    plt.ylabel('true label')

    plt.tight_layout()
    # plt.savefig('./figures/confusion_matrix.png', dpi=300)
    plt.show()
    plot_ROC(pipeline_clf, x_data, y_data)


if __name__ == '__main__':
    non_linear_classes()
    pipe_example()
