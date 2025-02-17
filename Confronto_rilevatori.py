import numpy as np
import matplotlib.pyplot as plt
from numpy import random
import scipy
import pet

'''
Esempio 1:
- La posizione della sorgente è in (10, 10)
- Il numero di rilevatori varia tra 100, 1000, 10000
- La risoluzione temporale è di 1e-9 s
- La durata è sempre di 45 minuti
- Il raggio della circonferenza 20 metri
'''
N1 = 10
N2 = 100
N3 = 1000
R = 20
X = 5
Y = 5
dt = 1e-9
durata = 45
r = 'F18'


t1 = pet.tomografo(N1, R, X, Y, dt, durata*60, r)
t2 = pet.tomografo(N2, R, X, Y, dt, durata*60, r)
t3 = pet.tomografo(N3, R, X, Y, dt, durata*60, r)

pet.simula(t1)
pet.simula(t2)
pet.simula(t3)

