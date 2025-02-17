# Simulazione Montecarlo di un esame PET

L'acronimo *PET* sta per **Positron Emission Tomography**, si tratta di un esame utilizzato in medicina nucleare che permette un mapping completo dei processi funzionali all'interno dell'organismo del paziente. Si basa sulla rilevazione di una coppia di fotoni da 511 keV che si propaghino in direzioni diametralemente opposte e sulla successiva ricostruzione della sorgente responsabile dell'emissione di queste particelle. Nel progetto in esame si è voluto simulare lo svolgimento di questa particolare tecnica di imaging biomedico andando a generare gli eventi di interesse attraverso le tecniche Montecarlo, per poi ricostruire la posizione della sorgente dai dati così ottenuti.

# Organizzazione del progetto

## Pet.py
Il modulo **pet.py** è alla base di ciascuno script, in esso si definiscono le classi e le funzioni che permettono di implementare la simulazione di un esame pet:
- classe tomografo: definisce l'oggetto che contiene i parametri costruttivi e operativi del sistema;
- funzione punti_emissione: restituisce le coordinate (x, y) rispetto al centro del sistema dei punti di emissione dei
  fotoni ricostruiti a partire dal segnale sui rilevatori;
- funzione simula: a partire dai dati ottenuti da punti_emissione fornisce una ricostruzione grafica della sorgente.
- funzione grafici_controllo: permette di visualizzare, là dove necessario, la distribuzione angolare dei fotoni e i punti di intersezione con la circonferenza di rilevatori, così da accertarsi che non vi siano problemi in fase di generazione.

## Moduli Confronto
Gli altri script python rappresentano invece degli esempi di misura diagnostica in cui si sono variati i parametri operativi e costruttivi:
- **Confronto_rilevatori.py**: si confronta il risultato diagnostico di due sistemi con parametri identici ad eccezione del numero di rilevatori;
- **Confronto_risoluzione.py**: si confronta il risultato diagnostico di due sistemi con parametri identici ad eccezione della risoluzione temporale.

## Modulo con input dati dall' utente
Lo script utente.py invece fa sì che i parametri che definiscono l'oggetto tomografo, da cui parte la simulazione, siano inseriti dall'utente, automaticamente
in questo file viene chiamata la funzione simula che restituisce il grafico della sorgente ricostruita.
Quando si inserisce la stringa che identifica il radiofarmaco usato si possono scegliere due opzioni:
  - *"F18"* per il Fluoro 18;
  - *"G68"* per il Gallio 68; 

se si inserisce una stringa differente viene stampato un messaggio di errore e l'esecuzione del programma non avviene correttamente.
