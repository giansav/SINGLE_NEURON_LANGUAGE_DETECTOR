# SINGLE NEURON LANGUAGE DETECTOR

IL PROGRAMMA STABILISCE L'APPARTENENZA DI UN TESTO ALLA LINGUA ITALIANA MEDIANTE UN SINGOLO NEURONE.  
IL SUO SCOPO E' FORNIRE UN ESEMPIO MINIMALE DI INTELLIGENZA ARTIFICIALE DA UTILIZZARE IN UN CONTESTO DIDATTICO.
VARIE VERSIONI VENGONO SVILUPPATE ALLO SCOPO DI MOSTRARE LE MODIFICHE CHE PORTANO A UN MIGLIORAMENTO DELLA PERFORMANCE.


# Caratteristiche generali di tutte le versioni del programma

I codici non si avvalgono mai di importazioni di librerie o di dipendenze e sono sempre divisi in 3 parti:

1) INPUT: acquisizione della stringa di testo da valutare

2) SENSORE: un blocco di funzioni che generano gli input neurali mediante la valutazione di alcune caratteristiche del testo.

3) NEURONE: una funzione che associa gli input neurali, genera un output compreso tra 0 e 1 e, in base a tale valore, scrive la sua conclusione sull'appartenenza del testo alla lingua italiana.

All'interno dei codici c'è una descrizione delle loro caratteristiche specifiche, una valutazione dei miglioramenti conseguiti rispetto alle versioni precedenti e una presentazione dei loro limiti.  


# Versioni ed evoluzione del programma

- La versione 1 usa un neurone con 3 input e 1 output e assegna alle features dei pesi calcolati in maniera empirica.
- La versione 2 usa un neurone con 5 input e 1 output e assegna alle features dei pesi calcolati in maniera empirica.
- Il programma WeightsOptimizer genera casualmente 1000 vettori (minimo 50 se non viene passato alcun valore) di 5 pesi, li testa su un dataset di 40 frasi (25 in italiano e 15 in altre lingue) e restituisce il vettore con la performance (percentuale di successo) migliore. Si nota che il vettore scelto da WeightsOptimizer conserva in genere le stesse proporzioni di peso tra le features che erano state stabilite nelle versioni 1 e 2 sulla base di ragionamenti empirici.
- La versione 3 è identica alla versione 2 ma, anzichè assegnare in maniera empirica il peso alle features, usa un vettore scelto da WeightsOptimizer.
  
- Dalle prove fatte risulta che la versione 3 è quella con la migliore performance. Risulta anche che usare un dataset molto più grande per la generazione del vettore dei pesi non implica un miglioramento significativo della performance.

- Il file SingleNeuronLangDetector.html non è altro che la versione 3 del programma in forma di webapp eseguibile in un qualsiasi browser. Le funzioni sono state ovviamente "tradotte" in JavaScript; la GUI è molto semplice.


# Ogni commento o suggerimento è benvenuto.
