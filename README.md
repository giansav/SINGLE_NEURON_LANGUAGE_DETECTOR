# SINGLE NEURON LANGUAGE DETECTOR

IL PROGRAMMA STABILISCE L'APPARTENENZA DI UN TESTO ALLA LINGUA ITALIANA MEDIANTE UN SINGOLO NEURONE CON 3 INPUT E 1 OUTPUT. 
IL SUO SCOPO E' FORNIRE UN ESEMPIO MINIMALE DI INTELLIGENZA ARTIFICIALE DA UTILIZZARE IN UN CONTESTO DIDATTICO.


** DESCRIZIONE **

Il codice è diviso in 3 parti:

1) INPUT: acquisizione della stringa di testo da valutare

2) SENSORE: un blocco di 3 funzioni che generano i 3 input neurali mediante la valutazione di 3 caratteristiche del testo:
    a) quante parole finiscono per vocale
    b) quante parole corrispondono ad articoli determinativi o indeterminativi dell'italiano (escluse quelle particelle che sono comuni anche in altre lingue)
    c) quanti digrammi o trigrammi o qadrigrammi peculiari dell'italiano sono presenti nella stringa

    L'input b) è il più "pesante" di tutti perché la presenza di articoli o preposizioni titpiche dell'italiano è un ottimo indicatore di appartenenza del testo all'italiano.

3) NEURONE: una funzione che associa gli input neurali e genera un output compreso tra 0 e 1

    In base al valore dell'output il programma scrive la sua conclusione sull'appartenenza del testo alla lingua italiana.

    
** LIMITI **

- Bilanciamento dei valori
Le variabili value1, value2 e value3 potrebbero essere normalizzate per evitare che l’indicatore più frequente domini.

- Bias adattivo
Il bias è aggiunto quando l'output raggiunge una soglia fissa di 0.75 ma si potrebbe implementare una sigmoide o un’altra funzione d’attivazione per un output più fluido. 

- Valori di soglia flessibili
Invece che soglie rigide si potrebbero definire soglie parametriche o calcolate dinamicamente (es. in base alla deviazione standard di un dataset di prova).


** POSSIBILI MIGLIORAMENTI **

Il programma può facilemnte essere esteso: 
- si possono aggiungere altre features per la valutazione dell'italianità del testo
- si può trasformare il singolo neurone in una rete neurale e addestrarla tramite algoritmi di backpropagation
- si può aggiungere una GUI.



à Ogni commento o suggerimento è benvenuto.
