import random
import re
import string

from nltk import PorterStemmer, WordNetLemmatizer, word_tokenize
from nltk.corpus import movie_reviews
from nltk.corpus import wordnet as wn, stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support, f1_score, \
    make_scorer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import SVC

DOMAIN_STOP_WORDS = """
trunk build commit branch patch
release bug regression close fix
"""


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
                wn.synsets(t)]


if __name__ == '__main__':
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
    parameters = {
        'vect__max_df': [0.75, 1.0],
        'vect__max_features': [1000, 2000],
        'vect__ngram_range': [[1, 2]],  # unigrams or bigrams
        'clf__kernel': ['linear', 'rbf'],
        'clf__C': [1, 10],
        'clf__probability': [True]
    }
    classifier = Pipeline([
        ('vect', TfidfVectorizer(strip_accents='unicode',
                                 tokenizer=word_tokenize,
                                 stop_words='english',
                                 decode_error='ignore',
                                 analyzer='word',
                                 norm='l2'
                                 )),
        ('clf', SVC())
    ])
    grid_search = GridSearchCV(classifier, parameters, verbose=1, scoring='f1_micro')
    print("Performing grid search...")
    print("pipeline:", [name for name, _ in classifier.steps])
    print("parameters:")
    print(parameters)
    grid_search.fit(xTrain, yTrain)
    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
    predicted = grid_search.predict(xTest)
    print(accuracy_score(yTest, predicted))
    print(precision_recall_fscore_support(yTest, predicted))
    print(classification_report(yTest, predicted))
