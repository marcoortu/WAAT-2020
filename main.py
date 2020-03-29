from exercise1 import get_adjectives

from exercise2 import AuthorSentimentAnalyzer

if __name__ == '__main__':
    print(get_adjectives('https://www.ft.com/'))
    print(get_adjectives('https://www.economist.com/'))

    clf = AuthorSentimentAnalyzer()
    print(clf.get_sentiment('deledda'))
    print(clf.get_sentiment('pirandello'))
