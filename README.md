# WAAT-2020

Weka branch.

## Esercizio 1

Utilizzare il file *data/language.arff* con almeno 3 algoritmi di classificazione e identificare quello 
con le performance migliori per l’identificazione della lingua di un testo.



## Esercizio 2

Utilizzare i *converters* forniti da Weka per creare un file _arff_ *data/reviews_sentiment.arff*. Utilizzare il dataset creato per
creare un classificatore in grado di predire il sentiment di una review con WEKA.

1. Creare il dataset utilizzando i conversers di Weka

    ```bash
    java weka.core.converters.TextDirectoryLoader -dir text_example > text_example.arff
    ```
2. Importare il file su Weka utilizzando l’explorer e analizzare la struttura
3. Creare un *FilteredClassifier* composto da:
    1. *StringToWordVector* utilizzando le trasformazioni TF e IDF
    2. *SMO* (Sequential Minimum Optimization, implementazione del SVM) classifier
4. Creare un esperimento con la cross validation utilizzando 10 folds e valutare le performance del classificatore.
