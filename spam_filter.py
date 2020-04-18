import random

from nltk import word_tokenize
from nltk.corpus import CategorizedPlaintextCorpusReader
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


def evaluate_classifier(clf, xTrain, yTrain):
    pipeline = Pipeline([
        ('vect', TfidfVectorizer(strip_accents='unicode',
                                 tokenizer=word_tokenize,
                                 stop_words='english',
                                 decode_error='ignore',
                                 analyzer='word',
                                 norm='l2',
                                 ngram_range=(1, 2)
                                 )),
        ('clf', clf)
    ])
    pipeline.fit(xTrain, yTrain)
    predicted = pipeline.predict(xTest)
    print(accuracy_score(yTest, predicted))
    print(precision_recall_fscore_support(yTest, predicted))
    print(classification_report(yTest, predicted))
    return pipeline


if __name__ == '__main__':
    spam_corpus = CategorizedPlaintextCorpusReader(
        './corpus/',
        r'.*\.txt',
        cat_pattern=r'(\w+)/*',
        encoding="latin-1"
    )

    documents = [(spam_corpus.raw(fileid), category)
                 for category in spam_corpus.categories()
                 for fileid in spam_corpus.fileids(category)]
    random.shuffle(documents)
    documents = documents[:1000]
    xData = [doc[0] for doc in documents]
    yData = [doc[1] for doc in documents]
    xTrain, xTest, yTrain, yTest = train_test_split(
        xData, yData,
        test_size=0.33,
        random_state=42
    )
    svm_clf = SVC(probability=True,
                  C=10,
                  shrinking=True,
                  kernel='linear')
    random_forest_clf = RandomForestClassifier(n_jobs=2,
                                               random_state=0)
    svm_clf = evaluate_classifier(svm_clf, xTrain, yTrain)
    random_forest_clf = evaluate_classifier(random_forest_clf, xTrain, yTrain)

    parameters = {
        'vect__max_df': [0.75, 1.0],
        'vect__max_features': [1000, 2000],
        'vect__ngram_range': [[1, 2]],
        'clf__kernel': ['linear', 'rbf'],
        'clf__C': [1, 10],
        'clf__probability': [True]
    }
    grid_search = GridSearchCV(estimator=svm_clf,
                               param_grid=parameters)
    print("Performing grid search...")
    print("pipeline:", [name for name, _ in svm_clf.steps])
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
