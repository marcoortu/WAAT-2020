import csv
import operator
import random

import matplotlib.pyplot as plt
import pandas as pd

from nltk import word_tokenize
from prettytable import PrettyTable
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_similarity


def random_color():
    return '#%02X%02X%02X' % (random.randint(0, 255),
                              random.randint(0, 255),
                              random.randint(0, 255))


def plotConnectionGraph(tfidf_matrix, clusters, positions):
    cluster_colors = {}
    cluster_names = {}
    for i in range(0, len(clusters)):
        cluster_colors[i] = random_color()
        cluster_names[i] = str(i)
    mds = MDS(n_components=2,
              dissimilarity="precomputed",
              random_state=1)

    dist = 1 - cosine_similarity(tfidf_matrix)
    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
    xs, ys = pos[:, 0], pos[:, 1]
    df = pd.DataFrame(dict(x=xs,
                           y=ys,
                           label=clusters,
                           title=positions))
    groups = df.groupby('label')
    fig, ax = plt.subplots(figsize=(17, 9))  # set size
    ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling
    # iterate through groups to layer the plot
    for name, group in groups:
        ax.plot(group.x, group.y,
                marker='o',
                linestyle='',
                ms=12,
                label=cluster_names[name],
                color=cluster_colors[name],
                mec='none')
        ax.set_aspect('auto')
        ax.tick_params(axis='x',
                       which='both',
                       bottom='off',
                       top='off',
                       labelbottom='off')
        ax.tick_params(axis='y',
                       which='both',
                       left='off',
                       top='off',
                       labelleft='off')

    ax.legend(numpoints=1)

    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)

    plt.show()


def cluster_distribution(clusters):
    cluster_dict = {}
    for i, c in enumerate(clusters):
        if c in cluster_dict.keys():
            cluster_dict[c] += 1
        else:
            cluster_dict[c] = 1
    pretty_table = PrettyTable(field_names=['Cluster', 'Count'])
    sorted_clusters = sorted(cluster_dict.items(),
                             key=operator.itemgetter(1),
                             reverse=True)
    for t in sorted_clusters:
        pretty_table.add_row(t)
    print(pretty_table)


def get_best_k_for_k_means(tfidf_matrix, max_clusters=15):
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
    num_clusters = 15
    with open('./data/connections.csv', 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        positions = [row['Position'].decode('utf8') for row in reader]
        tfidf_vectorizer = TfidfVectorizer(max_features=100,
                                           stop_words='english',
                                           use_idf=True,
                                           tokenizer=word_tokenize,
                                           ngram_range=(1, 2))
        tfidf_matrix = tfidf_vectorizer.fit_transform(positions)
        get_best_k_for_k_means(tfidf_matrix)
        km = KMeans(n_clusters=num_clusters)
        km.fit(tfidf_matrix)
        clusters = km.labels_.tolist()
        print(km.predict(tfidf_vectorizer.transform(['Post Doc'])))
        cluster_distribution(clusters)
        plotConnectionGraph(tfidf_matrix, clusters, positions)
