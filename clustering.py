import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import brown
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import scale

from lda_example import get_20newsgroups_categories


def plot_cluster_graph(clusters=5, data=None, features=0):
    kmeans = KMeans(init='k-means++', n_clusters=clusters)
    reduced_data = PCA(n_components=2).fit_transform(data)
    kmeans.fit(reduced_data)
    print(kmeans.cluster_centers_)
    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .02  # point in the mesh [x_min, x_max]x[y_min, y_max].
    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z,
               interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto',
               origin='lower')
    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    plt.title('K-means clustering from Brown with %d categories and %d features' % (clusters, features))
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()


class BrownDataset(object):

    def __init__(self, categories=3, maxFeatures=100):
        documents = [(brown.raw(fileid), category)
                     for category in brown.categories()[:categories]
                     for fileid in brown.fileids(category)]

        random.shuffle(documents)

        documents = documents[:1000]

        self.vectorizer = TfidfVectorizer(max_features=maxFeatures,
                                          strip_accents='unicode',
                                          token_pattern=r'[A-z]\w+',
                                          stop_words='english',
                                          decode_error='ignore',
                                          analyzer='word',
                                          norm='l2')
        self.vectorizer.fit([d[0] for d in documents])
        self.data = self.vectorizer.transform([d[0] for d in documents]).toarray()
        self.target = [d[1] for d in documents]
        self.target_names = list(set(self.target))


def hierarchical_clustering(data=None):
    variables = ['X', 'Y', 'Z']
    labels = ['ID_0', 'ID_1', 'ID_2', 'ID_3', 'ID_4']
    if not data:
        data = np.random.random_sample([5, 3]) * 10
    df = pd.DataFrame(data, columns=variables, index=labels)
    row_dist = pd.DataFrame(
        squareform(pdist(df, metric='euclidean')),
        columns=labels,
        index=labels
    )
    row_clusters = linkage(row_dist, method='complete', metric='euclidean')
    pd.DataFrame(row_clusters,
                 columns=['row label 1', 'row label 2',
                          'distance', 'no. of items in clust.'],
                 index=['cluster %d' % (i + 1)
                        for i in range(row_clusters.shape[0])])
    row_clusters = linkage(pdist(df, metric='euclidean'), method='complete')
    pd.DataFrame(row_clusters,
                 columns=['row label 1', 'row label 2',
                          'distance', 'no. of items in clust.'],
                 index=['cluster %d' % (i + 1)
                        for i in range(row_clusters.shape[0])])

    row_clusters = linkage(df.values, method='complete', metric='euclidean')
    pd.DataFrame(row_clusters,
                 columns=['row label 1', 'row label 2',
                          'distance', 'no. of items in clust.'],
                 index=['cluster %d' % (i + 1)
                        for i in range(row_clusters.shape[0])])
    row_dendr = dendrogram(row_clusters,
                           labels=labels,
                           # make dendrogram black (part 2/2)
                           # color_threshold=np.inf
                           )
    plt.tight_layout()
    plt.ylabel('Euclidean distance')
    # plt.savefig('./figures/dendrogram.png', dpi=300,
    #            bbox_inches='tight')
    plt.show()
    fig = plt.figure(figsize=(8, 8), facecolor='white')
    axd = fig.add_axes([0.09, 0.1, 0.2, 0.6])

    # note: for matplotlib < v1.5.1, please use orientation='right'
    row_dendr = dendrogram(row_clusters, orientation='left')

    # reorder data with respect to clustering
    df_rowclust = df.iloc[row_dendr['leaves'][::-1]]

    axd.set_xticks([])
    axd.set_yticks([])

    # remove axes spines from dendrogram
    for i in axd.spines.values():
        i.set_visible(False)

    # plot heatmap
    axm = fig.add_axes([0.23, 0.1, 0.6, 0.6])  # x-pos, y-pos, width, height
    cax = axm.matshow(df_rowclust, interpolation='nearest', cmap='hot_r')
    fig.colorbar(cax)
    axm.set_xticklabels([''] + list(df_rowclust.columns))
    axm.set_yticklabels([''] + list(df_rowclust.index))

    # plt.savefig('./figures/heatmap.png', dpi=300)
    plt.show()


def kmeans_clustering_example(n_docs=1000, n_features=100):
    dataset = fetch_20newsgroups(shuffle=True,
                                 random_state=1,
                                 remove=('headers', 'footers', 'quotes'),
                                 categories=get_20newsgroups_categories(n_topics=5))
    documents = dataset.data
    tfidf_vectorizer = TfidfVectorizer(max_features=n_features,
                                       stop_words='english',
                                       use_idf=True,
                                       tokenizer=word_tokenize,
                                       ngram_range=(1, 2))

    tfidf_matrix = tfidf_vectorizer.fit_transform(documents[:n_docs])

    max_clusters = 10
    sum_of_squared_distances = []
    K = range(1, max_clusters)
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(tfidf_matrix)
        # inertia_: Sum of squared distances of samples to their closest cluster center.
        sum_of_squared_distances.append(km.inertia_)
    print(sum_of_squared_distances)
    plt.plot(K, sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum of Squared Distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()


if __name__ == '__main__':
    brownDataset = BrownDataset(categories=5, maxFeatures=1000)
    data = scale(brownDataset.data)
    samples, features = data.shape
    clusters = len(brownDataset.target_names)
    labels = brownDataset.target
    print(brownDataset.vectorizer.vocabulary_)
    plot_cluster_graph(clusters, data)
    kmeans_clustering_example(n_docs=1000, n_features=1000)
    hierarchical_clustering()
