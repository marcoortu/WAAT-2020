# WAAT-2020


## Esercitazione 1


### Esercizio 1

```python
#Utilizzare le tuple per rappresentare i documenti
doc1 = (
    "doc1",
    """una mattina, svegliandosi da sogni irrequieti Gregor Samsa
    si trovo nel suo letto trasformato in un insetto mostruoso
    """
)

doc2 = (
    "doc2",
    """Voi che trovate quando tornate a casa il cibo caldo e visi amici 
    Considerate se questo è un uomo
    """
)

doc3 = (
    "doc3",
    """Vidi un magnifico disegno rappresentava un serpente boa 
    nell atto di inghiottire un animale
    """
)
```

Scrivere il codice per eseguire le seguenti query utilizzando gli inverted index:

1. Documenti contenenti "un" e "atto"
    - Risposta : "doc3" 
2. Documenti contenenti "un atto"
    - Risposta : nessuno 
3. Documenti contenenti "un animale"
    - Risposta : "doc3" 
