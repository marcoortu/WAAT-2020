# WAAT-2020


## Esercitazione 2
    
### Esercizio 1

```python
#Utilizzare le tuple per rappresentare i documenti
doc1 = (
    "doc1",
    """L'enorme quantità di informazioni presentinelle pagine Web rende necessario l'uso di strumenti automatici per il recupero di informazioni"""
)

doc2 = (
    "doc2",
    """I presenti hanno descritto le fasi del recupero dell’enorme relitto ma le informazioni non concordano su tipo e quantità di strumenti in uso"""
)

doc3 = (
    "doc3",
    """E' stato presentato nel Web un documento che informa sulle enormi difficoltà che incontra chi usa uno strumento informativo automatico"""
)
```

Scrivere il codice per eseguire le seguenti query utilizzando il modello booleano:

1. "recupero" AND "Web"
    - Risposta : ("D1") 
2. "recupero" OR "Web"
    - Risposta : ("D1, D2, D3") 
3. "recupero" AND NOT "relitto"
    - Risposta : ("D1") 
4. ("Web" OR "uso") AND "strumenti"
    - Risposta : ("D1", "D2") 
5. ("Web" OR "uso") AND NOT "strumenti"
    - Risposta : ("D3") 
6. "informazioni" AND "studenti" AND "relitto"
    - Risposta: ()
7. "informazioni" OR "relitto" OR "Internet"
    - Risposta: ("D1","D2")
8. "bologna" OR NOT "padova"
    - Risposta: ("D1, D2, D3") 
