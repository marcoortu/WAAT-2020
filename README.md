# WAAT-2019


## Esercitazione 3

dati i seguenti documenti:

```python
#Utilizzare le tuple per rappresentare i documenti
doc1 = (
    "doc1",
    """Era un oggetto troppo grande per chiamarlo spada. Troppo spesso, troppo pesante e grezzo. 
    Non era altro che un enorme blocco di ferro.
    """
)

doc2 = (
    "doc2",
    """Fu allora che vidi il Pendolo. La sfera, mobile all'estremità di un lungo filo fissato alla volta del coro, descriveva 
    le sue  ampie oscillazioni con isocrona maestà. 
    """
)

doc3 = (
    "doc3",
    """Era una bella mattina di fine novembre. Nella notte aveva nevicato un poco,
    ma il terreno era coperto di un velo fresco non più alto di tre dita. Al buio, subito
    dopo laudi, avevamo ascoltato la messa in un villaggio a valle. Poi ci eravamo messi
    in viaggio verso le montagne, allo spuntar del sole.
    Come ci inerpicavamo per il sentiero scosceso che si snodava intorno al monte,
    vidi l'abbazia
    """
)
```

### Esercizio 1

Scrivere il codice per eseguire le seguenti query utilizzando il modello vettoriale e la similarità coseno:

1. Documenti contenenti "spada oggetto"
    - Risposta : "doc1" 
2. Documenti contenenti "un che"
    - Risposta : nessuno 
3. Documenti contenenti "mattina sole"
    - Risposta : "doc3" 
    
Per pesare i termini di un documento utilizzare:
1. Presenza del termine
2. TF-IDF
