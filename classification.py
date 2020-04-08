import random

import nltk
from nltk.corpus import movie_reviews


def gender_features(word):
    """
    return the last character of the given word
    :param word:
    :type word: str
    :return: word[-1]
    :rtype dict
    """
    return {'last_letter': word[-1]}


def gender_features2(name):
    """
    :param name: the input name to extract the features
    :type name: str
    :return: a dict containing all the features
    """
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features


def gender_features3(word):
    """
    return the last and the second last character of the given word
    :param word:
    :type word: str
    :return: word[-1], word[-2]
    :rtype dict
    """
    return {'suffix1': word[-1:],
            'suffix2': word[-2:]}


def movie_review_features(document, word_features):
    """
    return a feature vector containing the occurrence of the top 2000 words
    :param word_features: top words features, default top 2000
    :param document: the document to be classified
    :return: a features vector with the occurrences of top words
    """
    document_words = set(document)
    features = {}
    for word in word_features:
        features[word] = word in document_words
    return features


def movie_review_classification():
    """
    Classify movie reviews in movie_reviews based on occurrence of top 2000 words
    :return: None
    """
    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    word_features = list(all_words)[:2000]
    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    feature_sets = [(movie_review_features(d, word_features), c) for (d, c) in documents]
    train_set, test_set = feature_sets[1000:], feature_sets[:500]
    print(train_set[0])
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))
    classifier.show_most_informative_features(5)
