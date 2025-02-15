import numpy as np
import matplotlib.pyplot as plt
from numpy import random
import pandas as pd
import scipy
import math
import matplotlib.colors as mcolors
from scipy.stats import gaussian_kde
import pet



'''
Parametri iniziali
Per implementare questa simulazione si è definito la classe tomografo nel modulo
tomography precedentemente importato. I parametri che definisco l'oggetto tomografo
vengono inseriti dall'utente.
'''

N = input('Selezionare numero rilevatori: ')
R = input('Selezionare raggio circonferenza: ')
X = input('Coordinata x della sorgente: ')
Y = input('Coordinata y della sorgente: ')
dt = input('Risoluzione temporale (secondi): ')
durata = input('Durata misura (minuti): ')
r = input('Radiofarmaco: ')

N = float(N)
R = float(R)
X = float(X)
Y = float(Y)
dt = float(dt)
durata = float(durata)

t1 = pet.tomografo(N, R, X, Y, dt, durata*60, r)
pet.simula(t1)







 