# WAAT-2019
Repository del Corso WAAT AA-2018-19

## Installazione


1. da _Pycharm_ aprire il menù *VCS*->*Checkout From Version Control*->*GitHub*
2. selezionare _Auth Type_->*password* e inserire le credenziali del vostro account su GitHub 
3. inserire *https://github.com/marcoortu/WAAT-2019*  nel campo *Git Reposistory Url*

oppure da terminale (per utenti esperti):

```git

    git clone https://github.com/marcoortu/WAAT-2019
    
```

Scaricato il repository, assicurarsi di avere creato il *VirtualEnv* per il progetto.
File -> Settings -> Project Interpreter.
- Premere sull'ingranaggio a destra del campo per selezionare il _Python Interpreter_.
- Selezionare _Add Local_.
- *NB* Assicurarsi in inserire la cartella corretta nel campo _Location_ e premere invio.


oppure da terminale (per utenti esperti):
- Aprire il terminale di _PyCharm_ ed eseguire il seguente comando.

```bash
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
```
Il file requirements.txt contiene la lista di tutte le librerie che serviranno durante le
esercitazioni come ad esempio *nltk*, *numpy* etc.


## Esercitazioni

Le esercitazioni verranno inserite durante il corso come nuovi *branch* in questo repository.
Utilizzando il *checkout* ci si può spostare nel *branch* di una particolare esercitazione.
Per effettuare il *checkout* di un *branch* su _PyCharm_ click sul menù _Git_ in basso a destra e selezionare il branch tra quelli disponibili. I _Local Branches_ sono la lista dei branch locali di cui si è già fatto il checkout mentre i _Remote Branches_ sono tutti i _branch_ presenti nel repository remoto.

- Per i _Local Branches_ selezionare l'opzione _Checkout_
- Per i _Remote Brances_ selezionare l'opzione _Checkout as new branch_

oppure da terminale (per utenti esperti):
- Dal terminale di _Pycharm_ digitare il seguente comando per spostarsi nel *branch* della prima esercitazione.

```git
    git checkout 01-esercitazione
```
