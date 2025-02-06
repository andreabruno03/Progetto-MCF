import numpy as np
import matplotlib.pyplot as plt
from numpy import random
import pandas as pd
import scipy

class tomografo:
    '''

    La classe ha cinque parametri che la definiscono:

    nrilev: numero di rilevatori del tomografo considerato
    raggio: raggio della circonferenze su cui sono disposti i rilevatori
    posizione: posizione della sorgente rispetto al centro della circonferenza
    risoluzione: risoluzione temporale dei rilevatori
    tempo: durata della misura diagnostica

    Sono presenti due metodi oltre il costruttore:
    __str__: permette una rappresentazione grafica apposita per un oggetto di questa classe
    __centr__: restituisce la poisizione della sorgente

    '''
    def __init__(self, nrilev, raggio, posizione, risoluzione, tempo):
        self.nrilev = nrilev
        self.raggio = raggio
        self.posizione = np.array(posizione)
        self.risoluzione = risoluzione
        self.tempo = tempo
    def __str__(self):
        return '-- Tomografo -- \n Numero rilevatori: {:} \n Raggio: {:} \n Posizione sorgente: {:} \n Risoluzione temporale: {:} \n Tempo: {:}'.format(self.nrilev, self.raggio, self.posizione, self.risoluzione, self.tempo)
    def __centr__(self):
        res = self.posizione
        return res