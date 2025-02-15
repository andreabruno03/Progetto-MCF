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
In questo script si confrontano due sistemi con eguali parametri
ma uno ha una risoluzione temporale 1000 volte più precisa dell'altro.
'''

t1 = pet.tomografo(1000, 25, -5, 5, 10e-9, 35, 'F18')
t2 = pet.tomografo(1000, 25, -5, 5, 0.01e-9, 35, 'F18')

t1x, t1y = pet.punti_emissione(t1)
t2x, t2y = pet.punti_emissione(t2)

circle_ril1 = plt.Circle((0, 0), t1.raggio, fill=False, label='Circonferenza rilevatori')
circle_ril2 = plt.Circle((0, 0), t2.raggio, fill=False, label='Circonferenza rilevatori')


fig, ax = plt.subplots(1, 2, figsize=(20, 20))
ax[0].set_title('Posizione sorgente: ({:}, {:})'.format(t1.posizione_x, t1.posizione_y))
ax[1].set_title('Posizione sorgente: ({:}, {:})'.format(t1.posizione_x, t1.posizione_y))
ax[0].scatter(t1x, t1y, label='Risoluzione: {:}'.format(t1.risoluzione), alpha=0.5)
ax[0].add_patch(circle_ril1)
ax[1].scatter(t2x, t2y, label='Risoluzione: {:}'.format(t2.risoluzione), alpha=0.5)
ax[1].add_patch(circle_ril2)
ax[0].legend()
ax[1].legend()
ax[0].set_xlabel('X (m)')
ax[0].set_ylabel('Y (m)')
ax[1].set_xlabel('X (m)')
ax[1].set_ylabel('Y (m)')
plt.show()
