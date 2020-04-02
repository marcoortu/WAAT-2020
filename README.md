# WAAT-2020
Repository del Corso WAAT AA-2019-20

## Setup NLTK


1. Aprire la console di Python e digitare i seguenti comandi:
    
    ```python
    
        import nltk
        print(nltk.__version__) # per verificare la versione
        nltk.download() # o nltk.download_gui() in caso di errore
    ```

2. Scaricare la collection _book_ dalla GUI, in caso non si riesca a visualizzare la GUI scaricare direttamente 
la collection con il seguente comando:

```python
    import nltk
    nltk.download('book') 
 ```

## Esercizi

Utilizzando la classe __CategorizedPlaintextCorpusReader__ è possibile
creare un corpus di documenti a partire da una directory di base. Tutte
le cartelle contenute nella directory di base rappresentano categorie identificate 
dal nome della directory. 
```python
    from nltk.corpus import CategorizedPlaintextCorpusReader
    root_dir = './corpora'
    italian_authors_corpus = CategorizedPlaintextCorpusReader(
        './%s/' % root_dir, # root directory
        r'.*\.txt', # specifies a file patter using a regular expression -> read only .txt files
        cat_pattern=r'(\w+)/*',  # specifies the category name using a regular expression -> the category is the name of parent directory
        encoding='latin-1' # specifies the text encoding
    )
 ```
Nell'esempio di codice riportato, partendo dalla cartella __corpora__ presente nel in questo branch, 
viene creato un corpus di documenti contenente i due autori italiani.
### Esercizio 1

Utilizzare i testi di Grazia Deledda e Luigi Pirandello per confrontare la _concordance_ e la _similarity_
della parola *donna*. I testi si trovano nella cartella _corpora_.

### Esercizio 2

Utilizzare i testi di Grazia Deledda e Luigi Pirandello per confrontare le 30 parole, di lunghezza maggiore a 4, più comunemente 
utilizzate dai due autori. Le stopwords vanno filtrate prima di effettuare il calcolo.

### Esercizio 3

Ottenete una distribuzione di frequenza condizionale (per autore) per esaminare le differenze nelle lunghezze 
delle parole utilizzare dai due autori italiani.
