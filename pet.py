import numpy as np
import matplotlib.pyplot as plt
from numpy import random
import pandas as pd
import scipy
import math
import matplotlib.colors as mcolors
from scipy.stats import gaussian_kde

class tomografo:
    '''

    La classe ha cinque parametri che la definiscono:

    nrilev: numero di rilevatori del tomografo considerato
    raggio: raggio della circonferenze su cui sono disposti i rilevatori
    posizione: posizione della sorgente rispetto al centro della circonferenza
    risoluzione: risoluzione temporale dei rilevatori
    tempo: durata della misura diagnostica
    radiof: indica l'emivita del radiofarmaco scelto, due possibili valori sono possibili:
            - Fluoro 18 con emivita 109 minuti, per usarlo la stringa è F18
            - Gallio 68 con emivita 68 minuti, per usarlo la stringa è G68
            

    Sono presenti due metodi oltre il costruttore:
    __str__: permette una rappresentazione grafica apposita per un oggetto di questa classe
    __centr__: restituisce la poisizione della sorgente

    '''
    def __init__(self, nrilev, raggio, posizione_x, posizione_y, risoluzione, tempo, radiof):
        self.nrilev = nrilev
        self.raggio = raggio
        self.posizione_x = posizione_x
        self.posizione_y = posizione_y
        self.risoluzione = risoluzione
        self.tempo = tempo
        self.radiof = radiof
    def __str__(self):
        return '-- Tomografo -- \n Numero rilevatori: {:} \n Raggio: {:} \n Posizione sorgente: {:} \n Risoluzione temporale: {:} \n Tempo: {:}'.format(self.nrilev, self.raggio, self.posizione_x , self.risoluzione, self.tempo)
    def __centr__(self):
        res = self.posizione
        return res

def punti_emissione(t):
    '''
    Funzione che permette di simulare un esame pet 
    - t è un oggetto della classe tomografo

    - La funzione a partire dai parametri operativi definiti in t effettua una simulazione 
    restituendo i due array che identificano le coordinate x e y ricostruite 
    dei punti di emissione dei fotoni
    '''

    '''
    Il numero di eventi è stato ricavato dalla formula per l'attività del fluoro 18 o del gallio 68.
    In particolare il valore è stato calcolato usando la formula per il numero
    di nuclei di un elemento radioattivo che decadono nell'unità di tempo, considerando un'attività iniziale
    di 1e6 Bq e un intervallo di tempo pari a quello della misura diagnostica.
    '''
    if t.radiof == 'F18':
        nevents =  1e5 * pow(math.e, - t.tempo / (109*60)) 
    if t.radiof == 'G68':
        nevents =  1e5 * pow(math.e, -t.tempo / (68*60)) 
    theta_s = math.atan2(t.posizione_y, t.posizione_x) #angolo sorgente rispetto al centro del sistema
    theta_s = math.degrees(theta_s)
    if theta_s < 0:
        theta_s += 360

    c = 299792458 #velocità della luce
    '''
    Prima parte: Simulazione Montecarlo
    Nello svolgimento di un esame pet il decadimento del radiofarmaco usato porta alla formazione
    di un positrone, il quale non appena incontra un elettrone annichilisce rilasciando due fotoni da 511 KeV che si 
    propagano in direzioni diametralmente opposte.
    '''

    theta_start = np.random.uniform(0, 360, int(nevents))

    #trasformo i valori in radianti per i calcoli

    '''
    Determinazione punti di arrivo fotoni

    Nel caso in cui la sorgente si trova in una posizione spostata rispetto al centro, l'angolo di partenza
    dei fotoni non corrisponde esattamente all'angolo che identifica il rilevatore interessato dall'arrivo
    della particella, ovvero l'angolo rispetto al centro del sistema. Bisogna infatti considerare un effetto 
    di proiezione geometrica e determinare quindi il punto di intersezione tra la retta passante per la sorgente,
    avente coefficiente angolare proprio dato dall'angolo di partenza, e la circonferenza dei rilevatori.

    Si è quindi risolto un sistma lineare di secondo grado, si avevano in totale due valori possibili per la coordinata
    x del punto di intersezione e due valori per quella y; la scelta di una coppia di questi piuttosto che un'altra
    è dipesa dal "quadrante" in cui ci si trova, in ultima istanza quindi dal valore di theta_start.
    '''


    m = np.tan(theta_start)
    # coefficienti per risolvere sistema
    A = np.power(m, 2) + 1
    B = 2 * m * (- m * t.posizione_x + t.posizione_y)
    C = pow(t.posizione_y, 2) - 2 * m * t.posizione_x * t.posizione_y - pow(t.raggio, 2) + (np.power(m, 2) * pow(t.posizione_x, 2))
    delta = np.power(B, 2) - (4 * A * C)

    #array da riempire
    x1 = np.zeros(len(theta_start))
    y1 = np.zeros(len(theta_start))
    x2 = np.zeros(len(theta_start))
    y2 = np.zeros(len(theta_start))
    for i in range(0, len(theta_start)):
        if (t.posizione_x == 0) and (t.posizione_y == 0):
            if (theta_start[i] <= 45):
                x1[i] = (-B[i] + math.sqrt(delta[i])) / (2*A[i])
                x2[i] = (-B[i] - math.sqrt(delta[i])) / (2*A[i])
                y1[i] = math.sqrt(pow(t.raggio, 2) - pow(x1[i], 2))
                y2[i] = - math.sqrt(pow(t.raggio, 2) - pow(x2[i], 2)) 
            elif (45 < theta_start[i] <= 135):
                x1[i] = (-B[i] + math.sqrt(delta[i])) / (2*A[i])
                x2[i] = (-B[i] - math.sqrt(delta[i])) / (2*A[i])
                y1[i] = - math.sqrt(pow(t.raggio, 2) - pow(x1[i], 2))
                y2[i] = math.sqrt(pow(t.raggio, 2) - pow(x2[i], 2))
            elif (135 < theta_start[i] <= 225):
                x1[i] = (-B[i] + math.sqrt(delta[i])) / (2*A[i])
                x2[i] = (-B[i] - math.sqrt(delta[i])) / (2*A[i])
                y1[i] = math.sqrt(pow(t.raggio, 2) - pow(x1[i], 2))
                y2[i] = - math.sqrt(pow(t.raggio, 2) - pow(x2[i], 2)) 
            else:
                x1[i] = (-B[i] + math.sqrt(delta[i])) / (2*A[i])
                x2[i] = (-B[i] - math.sqrt(delta[i])) / (2*A[i])
                y1[i] = - math.sqrt(pow(t.raggio, 2) - pow(x1[i], 2))
                y2[i] = math.sqrt(pow(t.raggio, 2) - pow(x2[i], 2))
        else:
            if (theta_start[i] <= theta_s):
                x1[i] = (-B[i] + math.sqrt(delta[i])) / (2*A[i])
                x2[i] = (-B[i] - math.sqrt(delta[i])) / (2*A[i])
                y1[i] = math.sqrt(pow(t.raggio, 2) - pow(x1[i], 2))
                y2[i] = - math.sqrt(pow(t.raggio, 2) - pow(x2[i], 2)) 
            elif (theta_s < theta_start[i] <= (180-theta_s)):
                x1[i] = (-B[i] + math.sqrt(delta[i])) / (2*A[i])
                x2[i] = (-B[i] - math.sqrt(delta[i])) / (2*A[i])
                y1[i] = - math.sqrt(pow(t.raggio, 2) - pow(x1[i], 2))
                y2[i] = math.sqrt(pow(t.raggio, 2) - pow(x2[i], 2))
            elif ((180-theta_s) < theta_start[i] <= (180+theta_s)):
                x1[i] = (-B[i] + math.sqrt(delta[i])) / (2*A[i])
                x2[i] = (-B[i] - math.sqrt(delta[i])) / (2*A[i])
                y1[i] = math.sqrt(pow(t.raggio, 2) - pow(x1[i], 2))
                y2[i] = - math.sqrt(pow(t.raggio, 2) - pow(x2[i], 2)) 
            else:
                x1[i] = (-B[i] + math.sqrt(delta[i])) / (2*A[i])
                x2[i] = (-B[i] - math.sqrt(delta[i])) / (2*A[i])
                y1[i] = - math.sqrt(pow(t.raggio, 2) - pow(x1[i], 2))
                y2[i] = math.sqrt(pow(t.raggio, 2) - pow(x2[i], 2))

    theta_ril1 = np.arctan2(y1, x1)
    theta_ril1 = np.degrees(theta_ril1)
    theta_ril1[theta_ril1 < 0] += 360

    theta_ril2 = np.arctan2(y2, x2)
    theta_ril2 = np.degrees(theta_ril2)
    theta_ril2[theta_ril2 < 0] += 360

    # considerando il numero di rilevatori la risoluzione è data da
    ris = 360 / t.nrilev
    # quantizzazione array degli angoli
    theta_eff1 = np.round(theta_ril1 / ris) * ris
    theta_eff2 = np.round(theta_ril2 / ris) * ris

    theta_ril = np.append(theta_ril1, theta_ril2)
    theta_eff = np.append(theta_eff1, theta_eff2)

    '''
    Definizione tempi
    Il tempo di arrivo dei fotoni dipende naturalmente dalla distanza tra il punto di arrivo considerato
    e la sorgente.
    '''
    x1_eff = t.raggio * np.cos(theta_eff1)
    y1_eff = t.raggio * np.sin(theta_eff1)

    x2_eff = t.raggio * np.cos(theta_eff2)
    y2_eff = t.raggio * np.sin(theta_eff2)

    time1 = np.sqrt(np.power(x1 - t.posizione_x, 2) + np.power(y1 - t.posizione_y, 2)) / c 
    time2 = np.sqrt(np.power(x2 - t.posizione_x, 2) + np.power(y2 - t.posizione_y, 2)) / c

    time1 = np.round(time1 / t.risoluzione) * t.risoluzione
    time2 = np.round(time2 / t.risoluzione) * t.risoluzione

    delta_time = np.random.normal(8e-8, 3e-9, len(theta_start))

    time1 = time1 + delta_time
    time2 = time2 + delta_time
    '''
    Seconda parte: Analisi dei risultati

    Rilevatore
    Una volta simulato il fenomeno fisico di annichilazione bisogna osservare come il rilevatore riesce
    a ricostruire ciò che sta succedendo.  Per ciascuna coppia di fotoni si è quindi calcolata la 
    differenza di percorso tra i due fotoni, la metà di questo valore rappresenta di quanto è spostato
    il punto di emissione rispetto al punto medio del segmento che unisce i due rilevatori.

    Una volta calcolato tale spostamento si sono ricavate le componenti lungo x e lungo y di quest'ultimo
    usando l'angolo di inclinazione della retta che passa per i due rilevatori coinvolti.

    '''

    delta_s = (time1 - time2) * c / 2
    delta_y = y1_eff - y2_eff
    delta_x = x1_eff - x2_eff

    c = np.arctan2(delta_y, delta_x)
    c = np.degrees(c)
    c[c < 0] += 360

    x_s = (delta_s) * np.cos(c)
    y_s =  (delta_s) * np.sin(c)

    x_m = (x1 + x2) / 2
    y_m = (y1 + y2) / 2

    x_a = x_m - x_s
    y_a = y_m - y_s


    return x_a, y_a
def simula(t):
    '''
    La funzione permette di avere una rappresentazione grafica della sorgente

    - t è un oggetto della classe tomografo
    Sfrutta la funzione precedente e rappresenta graficamente i punti di emissione
    che si ottengono con l'uso di punti_emissione.
    '''
    x_a, y_a = punti_emissione(t)
    if (t.posizione_x == 0) and (t.posizione_y == 0):
        fig, ax = plt.subplots(figsize=(10, 8))
        # nel titolo viene riportata anche la posizione in cui si è posta la sorgente in fase di simulazione
        circle_ril = plt.Circle((0, 0), t.raggio, fill=False, label='Circonferenza rilevatori')
        plt.title('Ricostruzione sorgente - Posizione sorgente: ({:}, {:})'.format(t.posizione_x, t.posizione_y))
        plt.scatter(x_a, y_a, c='mediumblue', label='Punti di emissione fotoni')
        plt.legend(fontsize=15)
        ax.add_patch(circle_ril)
        plt.xlabel('X(m)')
        plt.ylabel('Y(m)')
        plt.show()
    # il colore del grafico cambia in funzione della maggiore concentrazione di punti 
    else:  
        xy = np.vstack([x_a,y_a])
        z = gaussian_kde(xy)(xy)
        fig, ax = plt.subplots(figsize=(10, 8))
        circle_ril = plt.Circle((0, 0), t.raggio, fill=False, label='Circonferenza rilevatori')
        plt.title('Ricostruzione sorgente - Posizione sorgente: ({:}, {:})'.format(t.posizione_x, t.posizione_y))
        plt.scatter(x_a, y_a, c=z, label='Punti di emissione fotoni')
        plt.legend(fontsize=15)
        ax.add_patch(circle_ril)
        plt.xlabel('X(m)')
        plt.ylabel('Y(m)')
        plt.show()