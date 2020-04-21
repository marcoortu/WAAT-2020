import nltk
import numpy as np
import pandas as pd
from nltk import PorterStemmer, WordNetLemmatizer, word_tokenize
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
import string
from nltk.corpus import wordnet as wn, brown
from nltk.corpus import stopwords

from clustering import plot_cluster_graph


class LemmaTokenizer(object):
    def __init__(self, stemming=True):
        self.stemmer = PorterStemmer() if stemming else False
        self.lemmatizer = WordNetLemmatizer()
        brown_tagged_sents = brown.tagged_sents(categories='news')
        self.unigramTagger = nltk.UnigramTagger(brown_tagged_sents)
        self.allowedPostags = ['NN', 'JJ', 'VBZ', 'RB']

    def lemmatize(self, w):
        return self.lemmatizer.lemmatize(w)

    def tag_tokens(self, tokens):
        return self.unigramTagger.tag(tokens)

    def __call__(self, text):
        stop = stopwords.words('english')
        tokens = word_tokenize(text)
        tokens = [t[0] for t in self.tag_tokens(tokens) if t[1] in self.allowedPostags]
        tokens = [self.lemmatize(t) for t in tokens
                  if t not in string.punctuation
                  and t not in stop and wn.synsets(t)]
        if self.stemmer:
            tokens = [self.stemmer.stem(t) for t in tokens]
        return tokens


def lda_example():
    dataset = fetch_20newsgroups(shuffle=True,
                                 random_state=1,
                                 remove=('headers', 'footers', 'quotes'))
    documents = dataset.data[:100]
    no_features = 100
    # LDA is based on a probabilistic model and needs frequency counts
    tf_vectorizer = CountVectorizer(max_df=0.95,
                                    min_df=2,
                                    max_features=no_features,
                                    stop_words='english')
    data_vectorized = tf_vectorizer.fit_transform(documents)
    tf_feature_names = tf_vectorizer.get_feature_names()
    no_topics = 10
    lda = LatentDirichletAllocation(n_components=no_topics,
                                    max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0).fit(data_vectorized)

    print("Model Perplexity: ", lda.perplexity(data_vectorized))
    print("Model Log Likelihood: ", lda.score(data_vectorized))
    print(len(lda.components_))  # the number of topics' components equal to # topics
    print(lda.components_[0])  # the first topic weights
    print(lda.components_[0].argsort())  # argsort returns the sorted indexes of a numpy array
    # we need last 10 indexes which are the words with highest weights for the first topic
    top_n_topic_word_indexes = lda.components_[0].argsort()[:-11:-1]
    print(top_n_topic_word_indexes)
    # given the top 10 words indexes, the words name are contained in the feature names list
    print(" ".join([tf_feature_names[wordIndex] for wordIndex in top_n_topic_word_indexes]))
    # transform method return the topic vector for the first document doc0
    doc0_topics = lda.transform(data_vectorized[0])[0]
    print(doc0_topics)
    # the dominant topic is the one with the highest value, argmax return the index of max in a numpy array
    doc0_dominant_topic = np.array(doc0_topics).argmax()
    print(doc0_dominant_topic)
    # again top 10 words for the dominant topic of doc0
    top10_topic_word_indexes_of_doc0 = lda.components_[doc0_dominant_topic].argsort()[:-11:-1]
    print(" ".join([tf_feature_names[wordIndex] for wordIndex in top10_topic_word_indexes_of_doc0]))


def lda_with_grid_search_example():
    noFeatures = 100
    dataset = fetch_20newsgroups(shuffle=True,
                                 random_state=1,
                                 remove=('headers', 'footers', 'quotes'))
    documents = dataset.data[:100]
    tfVectorizer = CountVectorizer(max_df=0.95,
                                   min_df=2,
                                   max_features=noFeatures,
                                   stop_words='english')
    dataVectorized = tfVectorizer.fit_transform(documents)
    no_topics = 10
    lda = LatentDirichletAllocation()
    search_params = {'n_components': [10, 15, 20, 25, 30], 'learning_decay': [.5, .7, .9]}
    model = GridSearchCV(lda, param_grid=search_params)
    model.fit(dataVectorized)
    print(model.best_params_)
    lda_output = model.transform(dataVectorized)
    topicnames = ["Topic" + str(i) for i in range(no_topics)]
    docnames = ["Doc" + str(i) for i in range(len(documents))]
    df_document_topic = pd.DataFrame(np.round(lda_output, 2),
                                     columns=topicnames,
                                     index=docnames)
    print(df_document_topic.to_string())


def color_green(val):
    color = 'green' if val > .1 else 'black'
    return 'color: {col}'.format(col=color)


def make_bold(val):
    weight = 700 if val > .1 else 400
    return 'font-weight: {weight}'.format(weight=weight)


def dominant_topic_report(topics, ldaTransformedDate, numberOfDocuments):
    # column names
    topicnames = ["Topic" + str(i) for i in range(topics)]
    # index names
    docnames = ["Doc" + str(i) for i in range(numberOfDocuments)]
    # Make the pandas dataframe
    df_document_topic = pd.DataFrame(np.round(ldaTransformedDate, 2),
                                     columns=topicnames,
                                     index=docnames)
    # Get dominant topic for each document
    dominantTopic = np.argmax(df_document_topic.values,
                              axis=1)
    df_document_topic['dominant_topic'] = dominantTopic
    # Apply Style
    df_document_topics = df_document_topic.head(15).style.applymap(color_green).applymap(make_bold)
    with open('./report/ldaReport.html', 'w') as fileWriter:
        fileWriter.write(df_document_topics.render())
    return df_document_topic


def topic_distribution(df_document_topic_frame):
    df_topic_distribution = df_document_topic_frame['dominant_topic'].value_counts().reset_index(name="Num Documents")
    df_topic_distribution.columns = ['Topic Num', 'Num Documents']
    print(df_topic_distribution.to_string())


def report_topic_key_words(topics, featureNames, ldaData, targetNames, topWords=10):
    keywords = np.array(featureNames)
    topic_keywords = []
    for topicWeights in topics:
        topKeywordDocs = topicWeights.argsort()[:-1 - topWords:-1]
        topic_keywords.append(keywords.take(topKeywordDocs))
    df_topic_keywords = pd.DataFrame(topic_keywords)
    df_topic_keywords.columns = ['Word %d' % i for i in range(df_topic_keywords.shape[1])]
    df_topic_keywords.index = ['Topic %d' % i for i in range(df_topic_keywords.shape[0])]
    df_topic_keywords['Targets'] = get_topic_documents_targets(ldaData, targetNames, len(topics))
    return df_topic_keywords


def get_topic_documents_targets(ldaTransformedData, targetNames, topics):
    topic_targets = [set() for l in range(topics)]
    for i, doc in enumerate(ldaTransformedData):
        dominant_topic = np.array(doc).argmax()
        topic_targets[dominant_topic].add(targetNames[i])
    return [" ".join(list(targets)) for targets in topic_targets]


if __name__ == '__main__':
    documents_number = 100
    features = 1000
    url = 'https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json'
    df = pd.read_json(url)
    documents = df.content.values.tolist()[:documents_number]
    targetNames = df.target_names.values.tolist()[:documents_number]
    tf_vectorizer = CountVectorizer(max_features=features,
                                    tokenizer=LemmaTokenizer(),
                                    lowercase=True,
                                    stop_words='english')
    data_vectorized = tf_vectorizer.fit_transform(documents)

    for clusterNumber in [10, 15, 20]:
        plot_cluster_graph(clusters=clusterNumber,
                           data=data_vectorized.toarray(),
                           features=features)
    lda = LatentDirichletAllocation(learning_method='online')
    search_params = {'n_components': [10, 15, 20], 'learning_decay': [.5, .7, .9]}
    grid_lda = GridSearchCV(lda, param_grid=search_params, cv=5, iid=False)
    # Best Model
    grid_lda.fit(data_vectorized)
    ldaBestModel = grid_lda.best_estimator_
    ldaData = ldaBestModel.transform(data_vectorized)
    topics = len(ldaBestModel.components_)
    # Model Parameters
    print("Best Model's Params: %s" % grid_lda.best_params_)
    # Log Likelihood Score
    print("Best Log Likelihood Score: %.3f" % grid_lda.best_score_)
    # Perplexity
    print("Model Perplexity: %.3f" % ldaBestModel.perplexity(data_vectorized))
    df_document_topics = dominant_topic_report(topics,
                                               ldaData,
                                               len(documents))
    topic_distribution(df_document_topics)
    df_topic_keywords = report_topic_key_words(ldaBestModel.components_,
                                               tf_vectorizer.get_feature_names(),
                                               ldaData,
                                               targetNames)
    print(df_topic_keywords.to_string())
