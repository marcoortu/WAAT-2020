# WAAT-2020


## Esercizio 1

Utilizzare il dataset pubblico [Enron-spam](http://www2.aueb.gr/users/ion/data/enron-spam/) per
creare un filtro anti-spam ([why spam?](https://www.youtube.com/watch?v=9OVKXIfrGJE&t=27s)). 
Utilizzare la versione _pre-processed_ del dataset e scaricare il primo link (Enron1).

1. Il dataset è organizzato nel seguente modo:

    ```
    enron1
        ├── ham
        ├── spam
    ```

3. Selezionando 1000 documenti (misti tra spam e ham) e creare una pipeline per classificare le email.
    1. Utilizzare un *TfidfVectorizer* configurato per eliminare le stop words e punteggiatura.
    2. Utilizzare un classificatore *SVC* per la classificazione
    3. valutare le performance _accuracy_, _precision_, _recall_ e _F1_
    
4. Ripetere il passo 3 utilizzando un classificatore *RandomForest* e confrontare le performance.

5. Segliere il classificatore migliore individudato nei punti precendenti e utilizzare una *grid search* per 
ottenere i parametri ottimali tra:
    1. max idf : [0.25, 0.5, 0.75, 1.0],
    2. max features: [None, 500, 1000, 2000],
    3. numero n-grams: [1, 2]

## Esercizio 2

Utilizzare il dataset della [Stanford University dataset](https://ai.stanford.edu/~amaas/data/sentiment/) basato sul 
popolare sito di reviews di film [IMDb](https://www.imdb.com/) per effettuare una __sentiment analysis__ implementando 
un classificatore di recensioni positive/negative utilizzando la seguente pipeline :

    1. TfidfVectorizer
    2. SVC
    3. GridSearchCV

Ottimizzare i parametri del vectorizer e del SVC e misurare le seguenti performance:
   - precision
   - recall
   - F1
   - Confusion matrix

Il dataset contiene 50.000 (25.000 per il testing, 25.000 per il training) recensioni _raw_ che 
vanno opportunamente ripulite e successivamente analizzate.



## Esercizio 3

Utilizziare il [20-Newsgroups](https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json) dataset
che contiene ~18K post da 20 diversi newsgroups. Il dataset è in formato [JSON](https://it.wikipedia.org/wiki/JavaScript_Object_Notation)
e per semplicità possiamo utilizzare pandas per ottenere il dataset.

```python
import pandas as pd
from pprint import pprint
url = 'https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json'
df = pd.read_json(url)
print(df.target_names.unique()) 
pprint(df.head(15))
```
Per accedere ai valori di righe e colonne contenute in un DataFrame in pandas fare riferimento
alla [documentazione ufficiale](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html).
Limitare il numero di documenti a 500 e il numero di feature a 1000.

1. Fare il clustering dei documenti utilizzando KMeans e 10, 15, 20 come numero di clusters.
2. Utilizzare la LDA per ottenere i topics ottimizzando con la Grid Search i parametri :
    1. _n_components_: 10, 15, 20
    2. _learning_decay_: .5, .7, .9
3. Calcolare la distribuzione di documenti per topic.
4. Calcolare le top 10 parole per topic
5. Per ogni topic ottenuto, confrontare le top 10 keywords e le categorie dei documenti associati ad
ogni topic





## Scikit-Learn

Scikit-Learn esempi e tutorial da [scikit-learn.org](http://scikit-learn.org/stable/tutorial/index.html) e [altri](https://www.machinelearningplus.com/nlp/topic-modeling-python-sklearn-examples/).

### BOW

#### CountVectorizer

```python

from sklearn.feature_extraction.text import CountVectorizer
text = ["The quick brown fox jumped over the lazy dog."]
vectorizer = CountVectorizer()
vectorizer.fit(text)
print(vectorizer.vocabulary_)
vector = vectorizer.transform(text)
print(vector.shape)
print(type(vector))
print(vector.toarray())

```

#### TfidfVectorizer

```python
from sklearn.feature_extraction.text import TfidfVectorizer
text = ["The quick brown fox jumped over the lazy dog.",
        "The dog.",
        "The fox"
]
vectorizer = TfidfVectorizer()
vectorizer.fit(text)
print(vectorizer.vocabulary_)
print(vectorizer.idf_)
vector = vectorizer.transform([text[0]])
print(vector.shape)
print(vector.toarray())

```


#### HashingVectorizer

```python
from sklearn.feature_extraction.text import HashingVectorizer
text = ["The quick brown fox jumped over the lazy dog."]
vectorizer = HashingVectorizer(n_features=20)
vector = vectorizer.transform(text)
print(vector.shape)
print(vector.toarray())



```

### Classificazione

#### Support Vector Machine

```python

from sklearn import svm
X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
clf.fit(X, y)
print clf.predict([[2., 2.]])

```

#### Random Forest

```python

from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target
rf = RandomForestClassifier(n_estimators=10)
rf.fit(X, y)
rf.predict([[5.4, 1.5], [3.6, 5.1]])

```

### Grid Search

```python

import numpy as np
from sklearn import datasets
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
dataset = datasets.load_diabetes()
cParams = np.array([1,2,3,4,5])
# create and fit a ridge regression model, testing each alpha
model = SVC()
grid = GridSearchCV(estimator=model, param_grid=dict(C=cParams))
grid.fit(dataset.data, dataset.target)
print(grid)
# summarize the results of the grid search
print(grid.best_score_)
print(grid.best_estimator_.C)
```

