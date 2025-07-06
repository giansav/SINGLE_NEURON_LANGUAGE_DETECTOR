"""
*** SINGLE NEURON LANGUAGE DETECTOR - vers. 3 ***


IL PROGRAMMA STABILISCE L'APPARTENENZA DI UN TESTO ALLA LINGUA ITALIANA MEDIANTE UN SINGOLO NEURONE CON 5 INPUT E 1 OUTPUT 
IL SUO SCOPO E' FORNIRE UN ESEMPIO MINIMALE DI INTELLIGENZA ARTIFICIALE DA UTILIZZARE IN UN CONTESTO DIDATTICO



** DESCRIZIONE **

Il codice è diviso in 3 parti:

1) INPUT: acquisizione della stringa di testo da valutare

2) SENSORE: un blocco di 5 funzioni che generano i 5 input neurali mediante la valutazione di 5 caratteristiche del testo:
    a) quante parole finiscono per vocale
    b) quante parole corrispondono ad articoli determinativi o indeterminativi dell'italiano 
    c) quanti digrammi o trigrammi o qadrigrammi peculiari dell'italiano sono presenti nella stringa
    d) qual è la lunghezza media delle parole inserite (l'italiano ha in genere parole più lunghe dell'inglese, ad esempio)
    e) quante parole sono accentate sull'ultima sillaba

3) NEURONE: una funzione che associa gli input neurali e genera un output compreso tra 0 e 1

    In base al valore dell'output il programma scrive la sua conclusione sull'appartenenza del testo alla lingua italiana.
    A differenza della vers.2, in questa versione il peso dei vari input sull'output non è stato scelto in base a osservazioni empiriche ma in base a un processo di fine tuning svolto dal programma WeightsOptimizer.
    Il fine tuning del vettore dei pesi abbatte molto il numero dei falsi negativi generati dal modello e ne migliora la performance.

    ANche in qeusta versione un bias viene aggiunto per spingere in alto solo i casi borderline già promettenti ma solo sopra una certa soglia (output >= 0.6) per evitare di alzare troppo i valori deboli.


            
** CONFRONTO CON LE VERSIONI PRECEDENTI **

La vers.3 performa meglio della vers.1 e della vers.2 nei test effettuati. 
Il miglioramento riguarda la diminuzione dei falsi negativi e dei casi di indecisione ed è dovuto al fine tuning del vettore dei pesi effettuato dal programma WeightsOptimizer.



** POSSIBILI MIGLIORAMENTI **

Il programma può facilemnte essere esteso: 
- si possono usare features diverse per la valutazione dell'italianità del testo (dopo aver verificato una loro eventuale migliore performance)
- si può trasformare il singolo neurone in una rete neurale e addestrarla tramite algoritmi di backpropagation
- si può aggiungere una GUI.

"""


while True:

    # (1) INPUT
    
    print()
    text = str(input("Inserisci un testo (sarebbe meglio che fosse almeno di 10 parole):  "))



    # (2) SENSORE

    # Funzione 0: quante parole ci sono nel testo inserito e quali sono?
    def count_words(text):
        words = text.lower().split()
        return len(words), words

    
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


    # funzione 4: qual è la lunghezza media delle parole inserite?
    def avg_word_length(word_list):
        total_len = sum(len(word) for word in word_list)
        avg = total_len / len(word_list)
        if avg < 4.5:
            value = 0.3
        elif avg > 6.5:
            value = 0.9
        else:
            value = 0.7
        return avg, value


    # funzione 5: quante parole accentate sull'ultima sillaba ci sono?
    def check_accents(word_list):
        accents = "àèéìòù"
        count = sum(1 for word in word_list if any(char in accents for char in word))
        if count == 0:
            value = 0.2
        elif count >= 2:
            value = 0.9
        else:
            value = 0.6
        return count, value

    
    # eseguiamo le funzioni per il calcolo degli input neurali
    num, word_list = count_words(text)
    vowels_count, value1 = check_vowels_before_spaces(text, num)
    articles_found, value2 = check_articles(text)
    strings_found, value3 = check_strings(text)
    avg_len, value4 = avg_word_length(word_list)
    accented_found, value5 = check_accents(word_list)
    


    # (3) NEURONE SINGOLO

    # funzione neurone singolo
    def compute_neuron_output(values, weights, bias):
        output = sum(v * w for v, w in zip(values, weights))
        
        # il modello tende a generare falsi negativi, per cui, se il testo è breve ma ha indicatori forti, aumentiamo leggermente l'output
        if num < 10 and (value2 >= 0.7 or value3 >= 0.7):
            output += 0.05  

        # l'aggiunta del bias serve semrep a compensare la tendenza verso i falsi negativi
        if output >= 0.6:
            output += bias
        return output


    # calcolo dell'output neurale
    weights = [0.356, 0.338, 0.257, 0.032, 0.017]
    bias = 0.05
    values = [value1, value2, value3, value4, value5]

    output = compute_neuron_output(values, weights, bias)

    
    # comunicazione della conclusione raggiunta dal neurone
    print(f"\nIl testo inserito è composto di  {num} parole.")
    print(f"\nOsservo che in esso ci sono: \n(1) {vowels_count} parole che finiscono con una vocale;\n(2) {articles_found} articoli tipici dell'italiano;\n(3) {strings_found} digrammi/trigrammi/quadrigrammi tipici dell'italiano;\n(4) parole con una lunghezza media di {avg_len} caratteri;\n(5) {accented_found} parole accentate sull'ultima sillaba.")
    print(f"\nIn base a queste osservazioni calcolo un valore dell'output neurale pari a {output:.3f}. E per questo...")

    
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