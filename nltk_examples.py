from __future__ import division

import codecs

import matplotlib
import networkx as nx
import nltk
from nltk.corpus import brown
from nltk.corpus import names


def male_female_name_final_letter_freq():
    """
    Plots the count of male and female names per finale letter
    :return: None
    """
    cfd = nltk.ConditionalFreqDist(
        (fileid, name[-1])
        for fileid in names.fileids()
        for name in names.words(fileid))
    cfd.plot()


def ruzzle_puzzle(letters='egivrvonl'):
    """
    Return all words with length >= 4 with the given letters
    :param letters: a string containing all the letters constraint
    :type letters:str
    :return: the list of words
    :rtype list
    """
    puzzle_letters = nltk.FreqDist(letters)
    obligatory = 'r'
    wordlist = nltk.corpus.words.words()
    return [w for w in wordlist if len(w) >= 4
            and obligatory in w
            and nltk.FreqDist(w) <= puzzle_letters]


def differences_in_language_word_length():
    """Creates a plot of cumulative occurrences of words given a specific word length for different languages.

    The text used in this example is the Universal Declaration Of Human Rights corpus
    that contains the UDHR in more than 300 languages
    :return: None
    """
    from nltk.corpus import udhr
    languages = ['Chickasaw', 'English', 'German_Deutsch',
                 'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Italian_Italiano']
    cfd = nltk.ConditionalFreqDist(
        (lang, len(word))
        for lang in languages
        for word in udhr.words(lang + '-Latin1'))
    cfd.plot(cumulative=True)


def modal_verb_usage():
    """
    Prints the modal verbs usage in the brown corpus
    :return: None
    """
    cfd = nltk.ConditionalFreqDist(
        (genre, word)
        for genre in brown.categories()
        for word in brown.words(categories=genre))
    genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
    modals = ['can', 'could', 'may', 'might', 'must', 'will']
    cfd.tabulate(conditions=genres, samples=modals)


def create_text(filePath, encoding='utf-8'):
    """
    Create a NLTK Text object
    :param filePath: filepath of txt file
    :param encoding: default utf-8
    :return: Text instance
    """
    return nltk.Text(tokenize(get_text(filePath, encoding)))


def get_text(file_path, encoding='utf-8'):
    """
    Reads a file and return its content as a string
    :param encoding:
    :param file_path: the file path of the file to be opened
    :type file_path:str
    :return: a string containing the file raw text
    :rtype:str
    """
    with codecs.open(file_path, encoding=encoding) as txtfile:
        return txtfile.read()


def tokenize(text, pattern='[A-z]\w+'):
    """
    Return a list of tokens using a regualar expression
    :param pattern: default [A-z]\w+
    :param text: the text to be tokenized
    :return: a list of tokens
    """
    return nltk.RegexpTokenizer(pattern).tokenize(text)


def traverse(graph, start, node):
    """
    This function initialize a graph with the node hyponyms
    :param graph: The graph to be initialized
    :param start: The initial node
    :param node: The current node
    :return: None
    """
    graph.depth[node.name] = node.shortest_path_distance(start)
    for child in node.hyponyms():
        graph.add_edge(node.name, child.name)
        # This is a recursive call, it is needed since we want to visit all the graph children
        traverse(graph, start, child)


def hyponym_graph(start):
    """
    Given a starting Synset node this function creates the Graph object
    :param start: The initial Node
    :return: The Graph object
    :rtype Graph
    """
    G = nx.Graph()
    G.depth = {}
    traverse(G, start, start)
    return G


def graph_draw(graph):
    """
    Draw the graph with color and labels settings
    :param graph: The Graph object to be drawn
    :type graph:Graph
    :return: None
    """
    nx.draw_networkx(graph,
                     node_size=[16 * graph.degree(n) for n in graph],
                     node_color=[graph.depth[n] for n in graph],
                     with_labels=False)
    matplotlib.pyplot.show()
