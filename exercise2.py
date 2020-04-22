import string

import nltk
import pyprind
import pandas as pd
import os
import numpy as np
import wget
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords, brown

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from nltk.stem.snowball import SnowballStemmer

import tarfile
import matplotlib.pyplot as plt

stemmer = SnowballStemmer("english")
stop_words = stopwords.words('english')


def load_imdb_data(basepath='corpus_imdb'):
    print("Loading dataset...")
    if not os.path.exists(basepath):
        os.mkdir(basepath)
        file_name = 'aclImdb_v1.tar.gz'
        url = 'https://ai.stanford.edu/~amaas/data/sentiment/{}'.format(file_name)
        # download Stanford University dataset
        print("downloading archive....")
        wget.download(url, out=basepath)
        # extract .tar.gz file to basepath directory
    if not os.path.exists(os.path.join(basepath, 'aclImdb', 'train')):
        file_name = 'aclImdb_v1.tar.gz'
        with tarfile.open(os.path.join(basepath, file_name), 'r') as archive:
            print("extracting archive....")
            archive.extractall(path=basepath)
    csv_dataset_file = os.path.join(basepath, 'movie_data.csv')
    if not os.path.exists(csv_dataset_file):
        print("creating dataframe....")
        labels = {'pos': 1, 'neg': 0}
        pbar = pyprind.ProgBar(50000)
        df = pd.DataFrame()
        for s in ('test', 'train'):
            for l in ('pos', 'neg'):
                path = os.path.join(basepath, 'aclImdb', s, l)
                for file in os.listdir(path):
                    with open(os.path.join(path, file), 'r', encoding='utf-8') as infile:
                        txt = infile.read()
                    df = df.append([[txt, labels[l]]], ignore_index=True)
                    pbar.update()
        df.columns = ['review', 'sentiment']
        # shuffle
        np.random.seed(0)
        df = df.reindex(np.random.permutation(df.index))
        df.to_csv(csv_dataset_file, index=False)
    else:
        df = pd.read_csv(csv_dataset_file)
    return df


class Stemmer(object):
    def __init__(self):
        self.stemmer = SnowballStemmer("english")

    def __call__(self, text):
        tokens = word_tokenize(text)
        tokens = [t for t in tokens
                  if t not in string.punctuation
                  and t not in stop_words]
        return [self.stemmer.stem(t) for t in tokens]


class Lemmatizer(object):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def lemmatize(self, w):
        return self.lemmatizer.lemmatize(w)

    def __call__(self, text):
        tokens = word_tokenize(text)
        return [self.lemmatize(t) for t in tokens
                if t not in string.punctuation
                and t not in stop_words]


class StemmerLemmatizerPOS(object):
    def __init__(self):
        self.stemmer = SnowballStemmer("english")
        self.lemmatizer = WordNetLemmatizer()
        brown_tagged_sents = brown.tagged_sents(categories='news')
        self.unigramTagger = nltk.UnigramTagger(brown_tagged_sents)
        self.allowedPostags = ['NN', 'JJ', 'VBZ', 'RB']

    def lemmatize(self, w):
        return self.lemmatizer.lemmatize(w)

    def tag_tokens(self, tokens):
        return self.unigramTagger.tag(tokens)

    def __call__(self, text):
        tokens = word_tokenize(text)
        tokens = [t[0] for t in self.tag_tokens(tokens) if t[1] in self.allowedPostags]
        tokens = [self.lemmatize(t) for t in tokens
                  if t not in string.punctuation
                  and t not in stop_words]
        tokens = [self.stemmer.stem(t) for t in tokens]
        return tokens


if __name__ == '__main__':
    df = load_imdb_data()
    pipeline_clf = Pipeline([
        ('vect', TfidfVectorizer(
            strip_accents='unicode',
            decode_error='ignore',
            stop_words='english'
        )),
        ('clf', SVC())
    ])

    n_train_docs = 25000
    n_test_docs = 25000
    x_train = df.loc[:n_train_docs, 'review'].values
    y_train = df.loc[:n_train_docs, 'sentiment'].values
    x_test = df.loc[n_test_docs:, 'review'].values
    y_test = df.loc[n_test_docs:, 'sentiment'].values

    # Optimization
    parameters = {
        'vect__max_df': [0.75, 1.0],
        'vect__norm': ['l1', 'l2'],
        'vect__max_features': [1000, 2000, 5000],
        'vect__tokenizer': [Stemmer(), Lemmatizer(), StemmerLemmatizerPOS(), word_tokenize],
        'vect__ngram_range': [[1, 1], [1, 2]],  # unigrams or bigrams
        'clf__kernel': ['linear', 'rbf'],
        'clf__C': [0.1, 1, 10],
        'clf__probability': [True]
    }

    grid_search = GridSearchCV(
        pipeline_clf,
        parameters,
        verbose=1,
        scoring='f1_micro',
        n_jobs=4
    )
    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline_clf.steps])
    print("parameters:")
    print(parameters)
    grid_search.fit(x_train, y_train)
    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
    y_pred = grid_search.predict(x_test)
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
