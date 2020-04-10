# DIA Requirements

1.Imagine:

* Per il prodotto ho pensato ad un capo di abbigliamento come le scarpe (se ne serve uno specifico le Stan Smith, sono scarpe versatili che un po’ chiunque potrebbe comprare). 

* Features (c’è scritto che devono essere binary)
  - Maschio/Femmina
  - Giovane/Adulto (10-20 anni / 20-30 anni)
  - Europeo/Americano
  - Studente/Lavoratore
  - Single/Sposato
  - ….

* Classes (relativo al campo dell’abbigliamento)
  - Sportivo (le features degli utenti potrebbero essere Giovane,Studente,Single)
  - Elegante (le features degli utenti potrebbero essere Adulto,Lavoratore)
  - Casual 

* Per quanto riguarda la conversion rate per ogni classe (grafico probabilità di acquisto/prezzo se non erro), direi che si può, una volta scelto il prodotto, partire dal suo prezzo originale e inventarsi una funzione (es. logaritmica) +/- un errore casuale che ne simuli l’andamento. Questo soprattutto perché non penso si riescano avere dati di questo tipo.

* Le sotto-campagne sono relative alle classi immagino

* Le “abrupt phases” credo serva solo a dividere l’analisi in tre tempi diversi in cui le classi cambiano il loro numero giornaliero di click

* Anche qui il numero giornaliero di click per budget allocated credo debba essere una funzione che decidiamo +/- un errore causale. 

Avere dei dati inventati, ma di cui abbiamo la funzione base a mio parere potrebbe essere molto più prezioso, in un primo momento, che avere dati reali che potrebbero essere soggetti a eventi a noi ignoti. Questo per capire se i nostri modelli possono essere attendibili. Successivamente una volta implementati gli algoritmi si potrebbe cercare altri dati per confermarne la bontà.
