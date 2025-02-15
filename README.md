# Organizzazione progetto

## Pet.py
Il modulo pet.py è alla base di ciascuno script, in esso si definiscono le classi e le funzioni che permettono di implementare la simulazione
di un esame pet:
- classe tomografo: definisce l'oggetto che contiene i parametri costruttivi e operativi del sistema;
- funzione punti_emissione: restituisce le coordinate (x, y) rispetto al centro del sistema dei punti di emissione dei
  fotoni ricostruiti a partire dal segnale sui rilevatori;
- funzione simula: a partire dai dati ottenuti da punti_emissione fornisce una ricostruzione grafica della sorgente.

## Moduli Confronto
Gli altri script python rappresentano invece degli esempi di misura diagnostica in cui si sono variati i parametri operativi e costruttivi:
- '''Confronto_rilevatori.py''': si confronta il risultato diagnostico di due sistemi con parametri identici ad eccezione del numero di rilevatori;
- Confronto_risoluzione.py: si confronta il risultato diagnostico di due sistemi con parametri identici ad eccezione della risoluzione temporale.

## Modulo con input dati dall' utente
Lo script utente.py invece fa sì che i parametri che definiscono l'oggetto tomografo, da cui parte la simulazione, siano inseriti dall'utente, automaticamente
in questo file viene chiamata la funzione simula che restituisce il grafico della sorgente ricostruita.
- Quando si inserisce la stringa che identifica il radiofarmaco usato si possono scegliere due opzioni:
  1. "F18" per il Fluoro 18
  2. "G68" per il Gallio 68
  se si inserisce una stringa differente viene stampato un messaggio di errore e l'esecuzione del programma non funziona.
