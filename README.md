# WAAT-2020

Scikit-Learn esempi e tutorial da [scikit-learn.org](http://scikit-learn.org/stable/tutorial/index.html).

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

### Advanced LDA

Per visualizzare gli esempi di Topic Modeling avanzata con LDA 
eseguire Pycharm come amministratore (Windows only) e da terminale
eseguire il seguente comando solo una volta prima di eseguire lo script
 __lda_example.py__.

```bash

python -m spacy download en

```
