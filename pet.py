import numpy as np
import matplotlib.pyplot as plt
from numpy import random
import pandas as pd
import scipy
import math
import matplotlib.colors as mcolors
from scipy.stats import gaussian_kde

c = 299792458 #velocità della luce

class tomografo:
    '''
    La classe ha cinque parametri che la definiscono:

    nrilev: numero di rivelatori del tomografo considerato
    raggio: raggio della circonferenze su cui sono disposti i rivelatori
    posizione: posizione della sorgente rispetto al centro della circonferenza
    risoluzione: risoluzione temporale dei rivelatori
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
        if nrilev < 0:
            raise ValueError('Valore numero rivelatori non supportato')
        self.raggio = raggio
        if raggio < 0:
            raise ValueError('Valore raggio non valido')
        self.posizione_x = posizione_x
        if posizione_x >= raggio:
            raise ValueError('Coordinate sorgente non valide')
        self.posizione_y = posizione_y
        if posizione_y >= raggio:
            raise ValueError('Coordinate sorgente non valide')
        self.risoluzione = risoluzione
        if risoluzione < 0:
            raise ValueError('Valore risoluzione non valido')
        self.tempo = tempo
        if tempo < 0:
            raise ValueError('Valore di tempo non valido')
        self.radiof = radiof
    def __str__(self):
        return '-- Tomografo -- \n Numero rivelatori: {:} \n Raggio: {:} \n Posizione sorgente: {:} \n Risoluzione temporale: {:} \n Tempo: {:}'.format(self.nrilev, self.raggio, self.posizione_x , self.risoluzione, self.tempo)
    def __centr__(self):
        res = self.posizione
        return res
def numero_eventi(t):
    '''
    La funzione calcola il numero di eventi per la simulazione 

    - t è un oggetto della classe tomografo
    - restituisce il numero di eventi da considerare per la simulazione
    '''
    if t.radiof == 'F18':
        nevents =  1e5 * pow(math.e, - t.tempo / (109*60)) 
        return nevents
    if t.radiof == 'G68':
        nevents =  1e5 * pow(math.e, -t.tempo / (68*60)) 
        return nevents
    else:
        raise ValueError('Stringa per radiofarmaco non supportata')
    

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
    nevents = numero_eventi(t)

    theta_start = np.random.uniform(0, 360, int(nevents))

    #trasformo i valori in radianti per i calcoli

    '''
    Determinazione punti di arrivo fotoni

    Nel caso in cui la sorgente si trova in una posizione spostata rispetto al centro, l'angolo di partenza
    dei fotoni non corrisponde esattamente all'angolo che identifica il rilevatore interessato dall'arrivo
    della particella, ovvero l'angolo rispetto al centro del sistema. Bisogna infatti considerare un effetto 
    di proiezione geometrica e determinare quindi il punto di intersezione tra la retta passante per la sorgente,
    avente coefficiente angolare proprio dato dall'angolo di partenza, e la circonferenza dei rivelatori.

    Si è quindi risolto un sistma lineare di secondo grado, si avevano in totale due valori possibili per la coordinata
    x del punto di intersezione e due valori per quella y; la scelta di una coppia di questi piuttosto che un'altra
    è dipesa dal "quadrante" in cui ci si trova, in ultima istanza quindi dal valore di theta_start.
    '''


    m = np.tan((theta_start))
    # coefficienti per risolvere sistema
    A = np.power(m, 2) + 1
    B = 2 * m * (- m * t.posizione_x + t.posizione_y)
    C = pow(t.posizione_y, 2) - 2 * m * t.posizione_x * t.posizione_y - pow(t.raggio, 2) + (np.power(m, 2) * pow(t.posizione_x, 2))
    delta = np.power(B, 2) - (4 * A * C)

    theta_sx = np.arctan2(t.posizione_y, (t.posizione_x + t.raggio))
    theta_sx = np.degrees(theta_sx)
    if theta_sx < 0:
        theta_sx += 360
    
    theta_dx = np.arctan2(t.posizione_y, (t.posizione_x - t.raggio))
    theta_dx = np.degrees(theta_dx)
    if theta_dx < 0:
        theta_dx += 360
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

    theta_ril = np.append(theta_ril1, theta_ril2)


    # considerando il numero di rivelatori la risoluzione è data da
    ris = 360 / t.nrilev
    # quantizzazione array degli angoli
    theta_eff1 = np.round(theta_ril1 / ris) * ris
    theta_eff2 = np.round(theta_ril2 / ris) * ris

    theta_eff = np.append(theta_eff1, theta_eff2)

    '''
    Definizione tempi
    Il tempo di arrivo dei fotoni dipende naturalmente dalla distanza tra il punto di arrivo considerato
    e la sorgente.
    '''
    x1_eff = t.raggio * np.cos((theta_eff1))
    y1_eff = t.raggio * np.sin((theta_eff1))

    x2_eff = t.raggio * np.cos((theta_eff2))
    y2_eff = t.raggio * np.sin((theta_eff2))

    time1 = np.sqrt(np.power(x1 - t.posizione_x, 2) + np.power(y1 - t.posizione_y, 2)) / c 
    time2 = np.sqrt(np.power(x2 - t.posizione_x, 2) + np.power(y2 - t.posizione_y, 2)) / c

    time1 = np.round(time1 / t.risoluzione) * t.risoluzione
    time2 = np.round(time2 / t.risoluzione) * t.risoluzione

    delta_time = np.random.normal(8e-9, 3e-9, len(theta_start))

    time1 = time1 + delta_time
    time2 = time2 + delta_time
    '''
    Seconda parte: Analisi dei risultati

    Rilevatore
    Una volta simulato il fenomeno fisico di annichilazione bisogna osservare come il rilevatore riesce
    a ricostruire ciò che sta succedendo.  Per ciascuna coppia di fotoni si è quindi calcolata la 
    differenza di percorso tra i due fotoni, la metà di questo valore rappresenta di quanto è spostato
    il punto di emissione rispetto al punto medio del segmento che unisce i due rivelatori.

    Una volta calcolato tale spostamento si sono ricavate le componenti lungo x e lungo y di quest'ultimo
    usando l'angolo di inclinazione della retta che passa per i due rivelatori coinvolti.

    '''

    delta_s = (time1 - time2) * c / 2
    delta_y = y1_eff - y2_eff
    delta_x = x1_eff - x2_eff

    angolo = np.arctan2(delta_y, delta_x)

    x_s = (delta_s) * np.cos(angolo)
    y_s = (delta_s) * np.sin(angolo)

    x_m = (x1 + x2) / 2
    y_m = (y1 + y2) / 2

    x_a = x_m - x_s
    y_a = y_m - y_s


    return x_a, y_a
def grafici_controllo(t):
    '''
    La funzione non aggiunge nullo di nuovo alla precedente, ma permette di visualizzare
    la distribuzione angolare dei fotoni e i loro punti di intersezione con la circonferenza dei rivelatori
    '''

    theta_s = math.atan2(t.posizione_y, t.posizione_x) #angolo sorgente rispetto al centro del sistema
    theta_s = math.degrees(theta_s)
    if theta_s < 0:
        theta_s += 360

    nevents = numero_eventi(t)

    theta_start = np.random.uniform(0, 360, int(nevents))
    
    m = np.tan((theta_start))
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

    theta_ril = np.append(theta_ril1, theta_ril2)
    # considerando il numero di rivelatori la risoluzione è data da
    ris = 360 / t.nrilev
    # quantizzazione array degli angoli
    theta_eff1 = np.round(theta_ril1 / ris) * ris
    theta_eff2 = np.round(theta_ril2 / ris) * ris

    theta_eff = np.append(theta_eff1, theta_eff2)

    fig, ax = plt.subplots(3, 1, figsize=(10, 8))
    ax[0].set_title('Distribuzione angolare fotoni \n  Numero rivelatori: {:} -- Risoluzione: {:}s -- Durata Misura: {:}s -- \n Radiofarmaco :{:}'.format(t.nrilev, t.risoluzione, t.tempo, t.radiof), 
                    color='darkred')
    n1, bins1, patches1 = ax[1].hist(theta_ril, 100, [0, 360], label='Angolo rivelatori')
    n2, bins2, patches2 = ax[2].hist(theta_eff, 100, [0, 360], label='Angolo rivelatori con correzione per risoluzione')
    n3, bins3, patches3 = ax[0].hist(theta_start, 100, [0, 360], label='Angolo di partenza dalla sorgente')
    ax[0].legend()
    ax[1].legend()
    ax[2].legend()
    ax[0].set_xlabel(r'$\theta_{start}$')
    ax[1].set_xlabel(r'$\theta_{rivelatori}$')
    ax[2].set_xlabel(r'$\theta_{risoluzione}$')
    plt.subplots_adjust(hspace=0.3)
    plt.show()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.scatter(x1, y1, label='Punti fotone 1', alpha=0.5)
    plt.scatter(x2, y2, label='Punti fotone 2', alpha=0.5)
    circle_ril = plt.Circle((0, 0), t.raggio, fill=False, label='Circonferenza rivelatori')
    ax.add_patch(circle_ril)
    plt.legend()
    plt.title('Punti di intersezione circonferenza rivelatori e fotoni \n Numero rivelatori: {:} -- Risoluzione: {:}s'.format(t.nrilev, t.risoluzione))
    plt.xlabel('X(m)')
    plt.ylabel('Y(m)')
    plt.show()

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
        circle_ril = plt.Circle((0, 0), t.raggio, fill=False, label='Circonferenza rivelatori')
        plt.title('Ricostruzione sorgente - Posizione sorgente: ({:}, {:})'.format(t.posizione_x, t.posizione_y))
        plt.scatter(x_a, y_a, c='mediumblue', cmap='viridis', label='Punti di emissione fotoni')
        ax.add_patch(circle_ril)
        plt.legend(fontsize=15)
        plt.xlabel('X(m)')
        plt.ylabel('Y(m)')
        plt.show()
    # il colore del grafico cambia in funzione della maggiore concentrazione di punti 
    else:  
        xy = np.vstack([x_a,y_a])
        z = gaussian_kde(xy)(xy)
        fig, ax = plt.subplots(figsize=(10, 8))
        circle_ril = plt.Circle((0, 0), t.raggio, fill=False, label='Circonferenza rivelatori')
        plt.title('Ricostruzione sorgente - Posizione sorgente: ({:}, {:}) \n Numero rivelatori: {:} -- Risoluzione: {:}s'.format(t.posizione_x, t.posizione_y, t.nrilev, t.risoluzione))
        plt.scatter(x_a, y_a, c=z, cmap='viridis', label='Punti di emissione fotoni')
        ax.add_patch(circle_ril)
        plt.legend(fontsize=15)
        plt.xlabel('X(m)')
        plt.ylabel('Y(m)')
        plt.colorbar(label='Densità')
        plt.show()
