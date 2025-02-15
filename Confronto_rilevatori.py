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

resx1, resy1 = pet.punti_emissione(t1)
resx2, resy2 = pet.punti_emissione(t2)
resx3, resy3 = pet.punti_emissione(t3)
circle_ril1 = plt.Circle((0, 0), R, fill=False, label='Circonferenza rilevatori')
circle_ril2 = plt.Circle((0, 0), R, fill=False, label='Circonferenza rilevatori')
circle_ril3 = plt.Circle((0, 0), R, fill=False, label='Circonferenza rilevatori')

fig, ax = plt.subplots(figsize=(10, 8))
plt.title('10 Rilevatori')
plt.scatter(resx1, resy1, alpha=0.5, label='Posizione sorgente: ({:}, {:})'.format(t1.posizione_x, t1.posizione_y))
plt.xlim(-R, R)
plt.ylim(-R, R)
ax.add_patch(circle_ril1)
plt.show()

fig, ax = plt.subplots(figsize=(10, 8))
plt.title('100 Rilevatori')
plt.scatter(resx2, resy2, alpha=0.5, label='Posizione sorgente: ({:}, {:})'.format(t1.posizione_x, t1.posizione_y))
plt.xlim(-R, R)
plt.ylim(-R, R)
ax.add_patch(circle_ril2)
plt.show()

fig, ax = plt.subplots(figsize=(10, 8))
plt.title('1000 Rilevatori')
plt.scatter(resx3, resy3, alpha=0.5, label='Posizione sorgente: ({:}, {:})'.format(t1.posizione_x, t1.posizione_y))
plt.xlim(-R, R)
plt.ylim(-R, R)
ax.add_patch(circle_ril3)
plt.show()