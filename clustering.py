import random

import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import brown
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import scale


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


if __name__ == '__main__':
    brownDataset = BrownDataset(categories=5, maxFeatures=1000)
    data = scale(brownDataset.data)
    samples, features = data.shape
    clusters = len(brownDataset.target_names)
    labels = brownDataset.target
    print(brownDataset.vectorizer.vocabulary_)
    plot_cluster_graph(clusters, data)
