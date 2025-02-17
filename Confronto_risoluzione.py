import numpy as np
import matplotlib.pyplot as plt
from numpy import random
import pandas as pd
import scipy
import math
import matplotlib.colors as mcolors
from scipy.stats import gaussian_kde
import pet
from scipy.stats import gaussian_kde

'''
In questo script si confrontano due sistemi con eguali parametri
ma uno ha una risoluzione temporale 1000 volte più precisa dell'altro.
'''

t1 = pet.tomografo(1000, 25, -5, 5, 10e-9, 10, 'F18')
t2 = pet.tomografo(1000, 25, -5, 5, 0.01e-9, 10, 'F18')

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Supponiamo che res1x, res1y, res2x, res2y siano già definiti
res1x, res1y = pet.punti_emissione(t1)
res2x, res2y = pet.punti_emissione(t2)

# Calcola la densità dei punti per entrambi i dataset
xy1 = np.vstack([res1x, res1y])
density1 = gaussian_kde(xy1)(xy1)

xy2 = np.vstack([res2x, res2y])
density2 = gaussian_kde(xy2)(xy2)

# Ordina i punti in base alla densità (opzionale, migliora la visualizzazione)
idx1 = density1.argsort()
res1x, res1y, density1 = res1x[idx1], res1y[idx1], density1[idx1]

idx2 = density2.argsort()
res2x, res2y, density2 = res2x[idx2], res2y[idx2], density2[idx2]

# Crea il grafico con due sottotrame
fig, ax = plt.subplots(1, 2, figsize=(20, 20))

# Prima sottotrama
ax[0].set_title('Posizione sorgente: ({:}, {:})'.format(t1.posizione_x, t1.posizione_y))
scatter1 = ax[0].scatter(res1x, res1y, c=density1, cmap='viridis', s=20, label='Risoluzione: {:}s'.format(t1.risoluzione))
circle_ril1 = plt.Circle((0, 0), t1.raggio, fill=False, edgecolor='blue', linestyle='--', label='Raggio rilevazione')
ax[0].add_patch(circle_ril1)
ax[0].set_xlabel('X (m)')
ax[0].set_ylabel('Y (m)')
ax[0].legend()
plt.colorbar(scatter1, ax=ax[0], label='Densità')

# Seconda sottotrama
ax[1].set_title('Posizione sorgente: ({:}, {:})'.format(t2.posizione_x, t2.posizione_y))
scatter2 = ax[1].scatter(res2x, res2y, c=density2, cmap='viridis', s=20, label='Risoluzione: {:}s'.format(t2.risoluzione))
circle_ril2 = plt.Circle((0, 0), t2.raggio, fill=False, edgecolor='blue', linestyle='--', label='Raggio rilevazione')
ax[1].add_patch(circle_ril2)
ax[1].set_xlabel('X (m)')
ax[1].set_ylabel('Y (m)')
ax[1].legend()
plt.colorbar(scatter2, ax=ax[1], label='Densità')

plt.show()

