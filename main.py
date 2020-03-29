from exercise1 import get_adjectives

from exercise2 import AuthorSentimentAnalyzer

if __name__ == '__main__':
    # Exercise 1
    print(get_adjectives('https://www.ft.com/'))
    print(get_adjectives('https://www.economist.com/'))

    # Exercise 2
    clf = AuthorSentimentAnalyzer()
    print(clf.get_sentiment('deledda'))
    print(clf.get_sentiment('pirandello'))
