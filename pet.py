import numpy as np
import matplotlib.pyplot as plt
from numpy import random
import pandas as pd
import scipy
import tomografo


t1 = tomografo.tomografo(100, 10, [0, 0], 0.0000001, 60*45)
print(t1)
nevents = t1.tempo / 2400 * 1710
print(nevents)


'''
Definizione sciami di fotoni
Nel processo di annichilazione elettrone positrone vengono prodotto coppie di fotoni da 511 KeV in 
direzioni diametralmente opposte. Nel ciclo for sottostante si usano le tecniche montecarlo per definire 
i due array che identificheranno questi due distinti sciami di fotoni 
'''
photons_up = np.zeros(int(nevents))
photons_down = np.zeros(int(nevents))
for i in range(0, int(nevents)):
    u = random.normal(90, 30)
    photons_up[i] = u
    d = random.normal(270, 30)
    photons_down[i] = d

fig, ax = plt.subplots(2, 1, figsize=(10, 8))

n1, bins1, patches1 = ax[0].hist(photons_up, 100, range=[0, 180], color='red')
n2, bins2, patches2 = ax[1].hist(photons_down, 100, range=[180, 360], color='blue')
ax[1].invert_yaxis()
plt.show()

'''
Rilevatore
Una volta simulato il fenomeno fisico di annichilazione bisogna osservare come il rilevatore riesce
a ricostruire ciò che sta succedendo. Nella parte di codice che segue si definisce da prima
un array di tempi inerenti al momento in cui un fotone colpisce un rilevatore.
'''

time_hit_up = np.linspace(0, t1.tempo, int(nevents))
time_hit_down = np.linspace(0, t1.tempo, int(nevents))
for i in range(0, int(nevents)):
    u = random.normal(0, 3e-9)
    time_hit_up[i] = time_hit_up[i] + u
    d = random.normal(0, 3e-9)
    time_hit_down[i] = time_hit_down[i] + d


time = np.append(time_hit_up, time_hit_down)
time = np.sort(time)


photons = np.append(photons_up, photons_down)

'''
Adesso quello che si potrebbe fare è definire un dizionario in maniera tale da associare a ciascun tempo
un angolo di provenienza, gli eventi di hit saranno quelli per cui a una differenza temporale molto piccola
due eventi con angoli di provenienza diametralmente opposti vengono rilevati
'''
events_up = {
    'theta' : photons_up,
    'time' : time_hit_up
}
events_down = {
    'theta' : photons_down,
    'time' : time_hit_down
}

tabular = pd.DataFrame(columns=['Theta_up', 'Time_up', 'Theta_down', 'Time_down'])
tabular['Theta_up'] = photons_up
tabular['Time_up'] = time_hit_up
tabular['Theta_down'] = photons_down
tabular['Time_down'] = time_hit_down
print(tabular)

theta_hit_up = np.empty(0)
theta_hit_down = np.empty(0)
distance = np.empty(0)

for i in range(0, len(photons_up)):
    if((abs(photons_down[i]-photons_up[i]) <= 195) & (abs((photons_down[i]-photons_up[i]) >= 165) & 
       (abs(time_hit_up[i]-time_hit_down[i])<=1e-9))):
        theta_hit_up = np.append(theta_hit_up, photons_up[i])
        theta_hit_down = np.append(theta_hit_down, photons_down[i])

for i in range(0, len(theta_hit_down)):
    r = abs(0.5 - (theta_hit_up[i] / (theta_hit_down[i] - theta_hit_up[i])))
    distance = np.append(distance, r)

print(theta_hit_up)
print(theta_hit_down)
radius = np.zeros(len(theta_hit_up))
for r in radius:
    r = t1.raggio


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection='polar')
for i in range(0, len(theta_hit_up)):
    arr = np.array([theta_hit_up[i], theta_hit_down[i]])
    ax.errorbar(arr, radius[0:2], color='red')
ax.set_title("Pretty polar error bars")
plt.show()

print(theta_hit_down-theta_hit_up)
print(distance.size) 

x = np.sin(theta_hit_up)

#Grafico sinogramma
fig, ax = plt.subplots(figsize=(10, 8))
plt.title('Sinogramma')
plt.errorbar(distance, theta_hit_up, fmt='o', color='green')
plt.xlabel('Minima distanza LOR-Centro')
plt.ylabel(r'Angolo $\theta$')
plt.xlim(-0.150)
plt.show()
'''
Il problema è come ricostruire l'immagine della sorgente, ovvero come faccio a determinare 
la posizione di origine dei fotoni a partire dalle LOR ricostruite
'''