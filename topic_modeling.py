import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))


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


def topic_modeling_examples(no_top_words=10):
    dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
    documents = dataset.data
    no_features = 1000
    # NMF is able to use tf-idf
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(documents)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(documents)
    tf_feature_names = tf_vectorizer.get_feature_names()
    no_topics = 10
    # Run NMF
    nmf = NMF(
        n_components=no_topics,
        random_state=1,
        alpha=.1,
        l1_ratio=.5,
        init='nndsvd'
    ).fit(tfidf)
    # Run LDA
    lda = LatentDirichletAllocation(
        n_components=no_topics,
        max_iter=5,
        learning_method='online',
        learning_offset=50.,
        random_state=0
    ).fit(tf)

    display_topics(nmf, tfidf_feature_names, no_top_words)

    display_topics(lda, tf_feature_names, no_top_words)


if __name__ == '__main__':
    # topic_modeling_examples()
    hierarchical_clustering()
