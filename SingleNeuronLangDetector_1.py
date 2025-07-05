"""
*** SINGLE NEURON LANGUAGE DETECTOR - vers.1 ***


IL PROGRAMMA STABILISCE L'APPARTENENZA DI UN TESTO ALLA LINGUA MEDIANTE UN SINGOLO NEURONE CON 3 INPUT E 1 OUTPUT. 
IL SUO SCOPO E' FORNIRE UN ESEMPIO MINIMALE DI INTELLIGENZA ARTIFICIALE DA UTILIZZARE IN UN CONTESTO DIDATTICO.



** DESCRIZIONE **

Il codice è diviso in 3 parti:

1) INPUT: acquisizione della stringa di testo da valutare

2) SENSORE: un blocco di 3 funzioni che generano i 3 input neurali mediante la valutazione di 3 caratteristiche del testo:
    a) quante parole finiscono per vocale
    b) quante parole corrispondono ad articoli determinativi o indeterminativi dell'italiano 
    c) quanti digrammi o trigrammi o qadrigrammi peculiari dell'italiano sono presenti nella stringa

3) NEURONE: una funzione che associa gli input neurali e genera un output compreso tra 0 e 1

    In base al valore dell'output il programma scrive la sua conclusione sull'appartenenza del testo alla lingua italiana.
    L'input b) è il più "pesante" di tutti perché la presenza di articoli o preposizioni titpiche dell'italiano 
    è un ottimo indicatore di appartenenza del testo all'italiano.


        
** LIMITI **

- Bilanciamento dei valori
Le variabili value1, value2 e value3 potrebbero essere normalizzate per evitare che l’indicatore più frequente domini.

- Bias adattivo
Il bias è aggiunto quando l'output raggiunge una soglia fissa di 0.75
ma si potrebbe implementare una sigmoide o un’altra funzione d’attivazione per un output più fluido. 

- Valori di soglia flessibili
Invece che soglie rigide si potrebbero definire soglie parametriche o calcolate dinamicamente
(es. in base alla deviazione standard di un dataset di prova).



** POSSIBILI MIGLIORAMENTI **

Il programma può facilemnte essere esteso: 
- si possono aggiungere altre features per la valutazione dell'italianità del testo
- si può trasformare il singolo neurone in una rete neurale e addestrarla tramite algoritmi di backpropagation
- si può aggiungere una GUI.

"""


while True:

    # (1) INPUT
    
    print()
    text = str(input("Inserisci un testo (sarebbe meglio che fosse almeno di 10 parole):  "))



    # (2) SENSORE

    # funzione 0: quante parole ci sono nel testo inserito?
    def count_words(text):
        words = text.lower().split()  # tutto minuscolo, poi dividi in parole
        words_num = len(words)
        return words_num

    num = count_words(text)
    print(f"\nIl testo inserito è composto di {num} parole.")


    # funzione 1: quante parole (in percentuale) del testo inserito finiscono per vocale?
    def check_vowels_before_spaces(text, words_num):
        vowels = "aeiouAEIOUàèéìòù"
        count1 = 0
        for i in range(1, len(text)):
            if text[i] == ' ' and text[i - 1] in vowels:
                count1 += 1
        # controlla anche se l'ultima parola finisce con una vocale
        if len(text) > 0 and text[-1] in vowels:
            count1 += 1
        if (count1/words_num) <= 0.4:
            value = 0.3
        elif (count1/words_num) > 0.65:
            value = 0.9
        else:
            value = 0.7   
        return count1, value


    vowels_count, value1 = check_vowels_before_spaces(text, num)
    print(f"\nNel testo inserito ci sono {vowels_count} parole che finiscono con una vocale. Pertanto il valore del primo input neurale è {value1}")


    # funzione 2: quanti articoli o preposizioni ci sono nel testo inserito?
    def check_articles(text):
        articles = {"il", "lo", "la", "gli", "le", "uno", "una", "di", "da", "in", "con", "su", "per", "tra", "fra", "del", "dal", 
                    "nel", "sul", "dello", "dallo", "nello", "sullo", "della", "dalla", "nella", "sulla", "delle", "nelle", "dalle", "sulle"}
        words = text.lower().split()  
        count2 = 0
        for word in words:
            if word in articles:
                count2 += 1
        if count2 == 0:
            value = 0.1
        elif count2 >= 3:
            value = 0.9
        else:
            value = 0.7
        return count2, value

    articles_found, value2 = check_articles(text)
    print(f"\nNel testo inserito ci sono {articles_found} articoli tipici dell'italiano. Pertanto il valore del secondo input neurale è {value2}")


    # funzione 3: quanti digrammi/trigrammi/quadrigrammi tipici dell'italiano ci sono?
    def check_strings(text):
        strings = ["che", "chi", "cia", "cie", "cio", "ciu", "ghe", "ghi", "gia", "già", "gio", "giò", "giu", "giù", 
                    "gna", "gne", "gni", "gno", "gnu", "gli", "glia", "glie", "glio", "gliu", "iù"]
        text = text.lower()  
        count3 = 0
        for string in strings:
            count3 += text.count(string)
        if count3 == 0:
            value = 0.3
        elif count3 >= 3:
            value = 0.9
        else:
            value = 0.7
        return count3, value

    strings_found, value3 = check_strings(text)
    print(f"\nNel testo inserito ci sono {strings_found} digrammi/trigrammi/quadrigrammi tipici dell'italiano. Pertanto il valore del terzo input neurale è {value3}")



    # (3) NEURONE SINGOLO

    # funzione neurone singolo
    def compute_neuron_output(values, weights, bias):
        output = sum(v * w for v, w in zip(values, weights))
        if output >= 0.6:
            output += bias
        return output

    # calcolo output
    weights = [0.30, 0.42, 0.28]
    bias = 0.05
    values = [value1, value2, value3]

    output = compute_neuron_output(values, weights, bias)
    print(f"\nIl valore dell'output neurale è {output:.3f}. Pertanto...")

    # comunicazione della conclusione raggiunta dal neurone
    if output >= 0.65:
        print("...sono piuttosto sicuro che il testo inserito sia scritto in italiano.\n")
    elif output <= 0.45:
        print("...penso che il testo inserito non sia scritto in italiano.\n")
    else:
        print("...non sono sicuro che il testo inserito sia scritto in italiano.\n")


    # === FINE PROGRAMMA ===
    scelta = input("Vuoi inserire un altro testo? (s/n): ").lower()
    if scelta != "s":
        print("Programma terminato.\n")
        break