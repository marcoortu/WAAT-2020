import string

import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from nltk.corpus import brown


def get_html_text(url):
    """
    Retrieve the html at url and parses it to remove scripts
    and styles
    :param url:
    :return:
    """
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    return soup.get_text()


def tokenizer(text):
    """
    Returns the tokens from text
    :param text:
    :return:
    """
    return [w.lower() for w in nltk.word_tokenize(text)]


def remove_stop_words(tokens):
    """
    Removes stop words and punctuation from tokens list
    :param tokens:
    :return:
    """
    return [w for w in tokens
            if w not in nltk.corpus.stopwords.words('english')
            and w not in string.punctuation]


def remove_non_english_words(tokens):
    """
    Removes all tokens without synsets
    :param tokens:
    :return:
    """
    return [w for w in tokens if wn.synsets(w)]


def tag_tokens(tokens):
    """
    Tags all tokens using UnigramTagger trained with
    news from brown corpus
    :param tokens:
    :return:
    """
    brown_tagged_sents = brown.tagged_sents(categories='news')
    unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
    return unigram_tagger.tag(tokens)


def get_adjectives(url):
    """
    Returns a list of adjectives from the page provide by url
    :param url:
    :return:
    """
    text = get_html_text(url)
    tokens = tokenizer(text)
    tokens = remove_stop_words(tokens)
    tokens = remove_non_english_words(tokens)
    tokens = list(set(tokens))
    return [t[0] for t in tag_tokens(tokens) if t[1] == 'JJ']
