"""
*** SINGLE NEURON LANGUAGE DETECTOR - WEIGHTS OPTIMIZER ***


IL PROGRAMMA FA IL FINE TUNING DEL VETTORE DEI PESI UTILIZZATO PER LA GENERAZIONE DEGLI INPUT NEURALI NELLA vers.2 DEL SINGLE NEURON LANGUAGE DETECTOR



** DESCRIZIONE **

Il codice genera 1000 vettori (minimo 50 se non viene passato alcun valore) di 5 pesi e li testa su un dataset di 40 frasi (25 in italiano e 15 in altre lingue).
Confrontando la percentuale di successo dei vari vettori, restituisce il vettore con la performance migliore.
La differenza tra il numero di frasi in italiano e quello delle frasi in altre lingue serve a compensare la tendenza del modello (verificata empiricamente) a generare falsi negativi.


** POSSIBILI MIGLIORAMENTI **

Il programma segue un approccio euristico per l'individuazione del vettore ottimale, perché valuta un insieme di 50 vettori geenrato casualmente. Diversi run del programma produrranno ovviamente diversi vettori ottimali. 
Si potrebbe perciò pensare a un fine tuning di secondo livello che selezioni tra i vettori restituiti da una certa batteria di run quello con la perfomrance migliore.

L'osservazione empirica suggerisce però che i vettori generati dall'ottimizzatore sono sufficienti a garantire una funzionalità soddisfacente del SINGLE NEURON LANGUAGE DETECTOR e che, inoltre, a dataset di frasi molto più grandi non corrisponono risultati significativamente migliori nella funzionalità del programma: il guadagno marginale della crescita dei dataset sembra calare molto rapidamente.

"""



# importazione necessaria per la generazione di valori casuali
import random



# dataset: 25 frasi in italiano e 15 in altre lingue (il modello tende a dare falsi negativi)

dataset = [
    ("Oggi ho comprato del pane fresco al mercato vicino casa mia.", 1),
    ("Je suis allé au marché pour acheter du pain.", 0),
    ("I usually drink a cup of coffee before checking my emails in the morning.", 0),
    ("Il gatto dorme sulla sedia.", 1),
    ("Ho mangiato una pizza deliziosa ieri sera.", 1),
    ("La macchina è parcheggiata sotto casa.", 1),
    ("La voiture est garée devant la maison.", 0),
    ("Der Lehrer hat die Lektion gut erklärt.", 0),
    ("Elle aime écouter de la musique classique quand elle lit des romans historiques.", 0),
    ("Stanno giocando a calcio nel cortile.", 1),
    ("L’autunno è la mia stagione preferita per i suoi colori caldi e l’atmosfera malinconica.", 1),
    ("I bambini giocavano in giardino finché il cielo non si è coperto di nuvole minacciose.", 1),
    ("J’ai acheté du pain frais ce matin en passant devant la boulangerie du quartier.", 0),
    ("Abbiamo camminato ore nel bosco cercando funghi, ma siamo tornati a casa a mani vuote.", 1),
    ("La ragazza indossa un vestito blu.", 1),
    ("Abbiamo visitato Roma la settimana scorsa.", 1),
    ("Los estudiantes estudian con atención.", 0),
    ("Každý víkend jezdíme na chalupu a trávíme tam čas s rodinou.", 0),
    ("L'aria è fresca in montagna al mattino.", 1),
    ("Ho comprato il pane e il latte.", 1),
    ("The children were playing football in the park while their parents talked nearby.", 0),
    ("Andiamo al cinema stasera?", 1),
    ("A shallow depth of field produces flames in a dimmed distance, harlequin patterned jit or juke, footwork. Each muscle in the face follows a separate choreographic text.", 0),
    ("Sucede que entro en las sastrerías y en los cines marchito, impenetrable, como un cisne de fieltro navegando en un agua de origen y ceniza.", 0),
    ("Il sole tramontava lentamente dietro le colline mentre il vento accarezzava gli alberi silenziosi.", 1),
    ("Ho letto un libro molto interessante sulla storia delle esplorazioni polari durante l’Ottocento.", 1),
    ("Les enfants jouent dans le parc.", 0),
    ("Quando arrivi a casa, ricordati di annaffiare le piante e spegnere tutte le luci.", 1),
    ("Los niños jugaban en la playa mientras los adultos preparaban la comida.", 0),
    ("Ogni volta che torno al mio paese d’origine, mi emoziono rivedendo quei luoghi familiari.", 1),
    ("La vispa Teresa avea fra l’erbetta al volo sorpresa gentil farfalletta.", 1),
    ("Fuimos al mercado esta mañana y compramos frutas frescas, verduras y un poco de pan.", 0),
    ("Nel mazzo del cammin di nostra vita mi ritrovai per una selva oscura.", 1),
    ("Né più mai toccherò le sacre sponde ove il mio corpo fanciullesco e nudo giacque un tempo, e la mia vita era un tesoro di sogni e d'illusioni.", 1),
    ("He perdido las llaves del coche.", 0),
]



# funzioni del SENSORE per la valutazione delle features

def count_words(text):
    words = text.lower().split()
    return len(words), words

def check_vowels_before_spaces(text, words_num):
    vowels = "aeiouAEIOUàèéìòù"
    count1 = sum(1 for i in range(1, len(text)) if text[i] == ' ' and text[i - 1] in vowels)
    if len(text) > 0 and text[-1] in vowels:
        count1 += 1
    ratio = count1 / words_num
    value = 0.3 if ratio <= 0.4 else 0.9 if ratio > 0.65 else 0.7
    return count1, value

def check_articles(text):
    articles = {"il","lo","la","gli","le","uno","una","di","da","in","con","su","per","tra","fra","del","dal",
                "nel","sul","dello","dallo","nello","sullo","della","dalla","nella","sulla","delle","nelle","dalle","sulle"}
    count2 = sum(1 for w in text.lower().split() if w in articles)
    value = 0.1 if count2 == 0 else 0.9 if count2 >= 3 else 0.7
    return count2, value

def check_strings(text):
    tris = ["che","chi","cia","cie","cio","ciu","ghe","ghi","gia","già","gio","giò","giu","giù",
            "gna","gne","gni","gno","gnu","gli","glia","glie","glio","gliu","iù"]
    text_l = text.lower()
    count3 = sum(text_l.count(t) for t in tris)
    value = 0.3 if count3 == 0 else 0.9 if count3 >= 3 else 0.7
    return count3, value

def avg_word_length(word_list):
    avg = sum(len(w) for w in word_list) / len(word_list)
    value = 0.3 if avg < 4.5 else 0.9 if avg > 6.5 else 0.7
    return avg, value

def check_accents(word_list):
    accents = "àèéìòù"
    count5 = sum(1 for w in word_list if any(c in accents for c in w))
    value = 0.2 if count5 == 0 else 0.9 if count5 >= 2 else 0.6
    return count5, value



# funzione neurone per la geenrazione dell'output neurale
def compute_neuron_output(values, weights, bias, num, value2, value3):
    output = sum(v * w for v, w in zip(values, weights))
    if num < 10 and (value2 >= 0.7 or value3 >= 0.7):
        output += 0.05
    if output >= 0.6:
        output += bias
    return output



# funzione di valutazione degli output
def evaluate(weights, bias=0.05, cutoff=0.65):
    correct = 0
    for text, label in dataset:
        num, words = count_words(text)
        _, v1 = check_vowels_before_spaces(text, num)
        _, v2 = check_articles(text)
        _, v3 = check_strings(text)
        _, v4 = avg_word_length(words)
        _, v5 = check_accents(words)
        values = [v1, v2, v3, v4, v5]

        out = compute_neuron_output(values, weights, bias, num, v2, v3)
        pred = 1 if out >= cutoff else 0
        if pred == label:
            correct += 1

    return correct / len(dataset)



# generazione casuale e test di vettori di pesi per gli input neurali
def tune(n=50):
    best = {"weights": None, "accuracy": 0}
    for _ in range(n):
        raw = [random.random() for _ in range(5)]
        total = sum(raw)
        weights = [r / total for r in raw]
        acc = evaluate(weights)
        if acc > best["accuracy"]:
            best = {"weights": weights, "accuracy": acc}
    return best



# main e comunicazione del risultato ottenuto
if __name__ == "__main__":
    print("Tuning in corso…")
    best = tune(1000)
    print(f"Miglior combinazione trovata: weights = {[round(w,3) for w in best['weights']]} con accuracy = {best['accuracy']:.2%}")
