import time
import datetime
import csv 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import  numpy as np
from scipy.interpolate import CubicSpline


#Chemin d'acces du .csv qu'on crée
day = datetime.date.today()
path1 = "data/%04d/%02d/th_%02d.csv"%(day.year, day.month, day.day)
print(path1)

print(day.day - 1)

#lecture premier jour (on veut tracer sur les deux derniers jours)
with open("/Users/grillot/Documents/Projet Montchauvel/data/2024/05/th_06.csv", 'r', encoding='latin-1') as fichier: ##juste changer le chemin en ajoutant path1 ou path2
    lecteur_csv = csv.reader(fichier, delimiter = ';')
    listes1 = list(lecteur_csv) 
    n = len(listes1) 

# Soustraire un jour de la date d'aujourd'hui
day_precedent = day - datetime.timedelta(days=1)

# Construire le chemin d'accès pour le fichier CSV du jour précédent
path2 = "data/%04d/%02d/th_%02d.csv" % (day_precedent.year, day_precedent.month, day_precedent.day)
print(path2)

#lecture deuxième jour 
with open("/Users/grillot/Documents/Projet Montchauvel/data/2024/05/th_07.csv", 'r', encoding='latin-1') as fichier:
    lecteur_csv = csv.reader(fichier, delimiter = ';')
    listes2 = list(lecteur_csv) 

day_precedent2 = day - datetime.timedelta(days=2)
# Construire le chemin d'accès pour le fichier CSV du jour précédent
path3 = "data/%04d/%02d/th_%02d.csv" % (day_precedent2.year, day_precedent2.month, day_precedent2.day)
print(path3)

""""
#lecture troisième jour 
with open("/Users/grillot/Documents/Projet Montchauvel/data/2024/05/th_07.csv", 'r', encoding='latin-1') as fichier:
    lecteur_csv = csv.reader(fichier, delimiter = ';')
    listes = list(lecteur_csv) 
    listes3 = listes[n - 1:]
"""

energie_fb = [abs(float(listes2[i][-1])) for i in range(1, len(listes2))] + [abs(float(listes1[i][-1])) for i in range(1, len(listes1))] #+ [abs(float(listes3[i][-1])) for i in range(1, len(listes3))]
energie_ts = [abs(float(listes2[i][-2])) for i in range(1, len(listes2))] + [abs(float(listes1[i][-2])) for i in range(1, len(listes1))] #+ [abs(float(listes3[i][-2])) for i in range(1, len(listes3))]
temps = [datetime.datetime.strptime(listes2[i][0], '%H:%M:%S') for i in range(1, len(listes2))] + [datetime.datetime.strptime(listes1[i][0], '%H:%M:%S') + datetime.timedelta(days=1) for i in range(1, len(listes1))] #+ [datetime.datetime.strptime(listes3[i][0], '%H:%M:%S') + datetime.timedelta(days=1) for i in range(1, len(listes3))]

S_fb = [sum(energie_fb[i:i+12]) for i in range(0, len(energie_fb)-12, 12)]
S_ts = [sum(energie_ts[i:i+12]) for i in range(0, len(energie_ts)-12, 12)]

print(S_fb)

current_date = temps[0]
temps_two = [current_date + datetime.timedelta(hours= 2 * i) for i in range(1, 24)]


# Tracer les données
fig1, ax1 = plt.subplots(2,1,1)

# Tracer la courbe des valeurs originales
ax1.plot(temps, energie_fb, color='blue', label='Valeurs toutes les 10 minutes')
ax1.set_xlabel('Date')
ax1.set_ylabel('Valeur', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Tracer les bâtons représentant la somme des valeurs toutes les 2 heures
ax3 = ax1.twinx()
ax3.bar(temps_two, S_fb, width=0.085, color='red', alpha=0.4, label='Somme toutes les 2 heures')
ax3.set_ylabel('Somme des valeurs', color='red')
ax3.tick_params(axis='y', labelcolor='red')

fig1.tight_layout()
fig1.autofmt_xdate()
plt.title('Courbe des valeurs et histogramme des sommes sur 2 jours')
ax1.legend(loc='upper left')
ax3.legend(loc='upper right')
plt.show()

# Tracer les données
fig2, ax2 = plt.subplots(2,1,2)

# Tracer la courbe des valeurs originales
ax2.plot(temps, energie_fb, color='blue', label='Valeurs toutes les 10 minutes')
ax2.set_xlabel('Date')
ax2.set_ylabel('Valeur', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# Tracer les bâtons représentant la somme des valeurs toutes les 2 heures
ax4 = ax2.twinx()
ax4.bar(temps_two, S_fb, width=0.085, color='red', alpha=0.4, label='Somme toutes les 2 heures')
ax4.set_ylabel('Somme des valeurs', color='red')
ax4.tick_params(axis='y', labelcolor='red')

fig2.tight_layout()
fig2.autofmt_xdate()
plt.title('Courbe des valeurs et histogramme des sommes sur 2 jours')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.show()

"""

timestamps = np.array([date_obj.timestamp() for date_obj in temps])

degree = len(timestamps) - 1

cs_fb = CubicSpline(timestamps, energie_fb)
cs_ts = CubicSpline(timestamps, energie_ts)



new_dates = [temps[0] + datetime.timedelta(days=i) for i in range((temps[-1] - temps[0]).days + 1)]
new_timestamps = np.array([date.timestamp() for date in new_dates])

fb = cs_fb(new_timestamps)
ts = cs_ts(new_timestamps)


plt.subplot(2, 1, 1)
plt.scatter(temps, energie_fb, color='red', label='Points d\'origine')
plt.plot(new_dates, fb, color='blue', label='Polynôme interpolé')
plt.xlabel('Date')
plt.ylabel('Valeur')
plt.legend()

plt.subplot(2, 1, 2)
plt.scatter(temps, energie_ts, color='red', label='Points d\'origine')
plt.plot(new_dates, ts, color='blue', label='Polynôme interpolé')
plt.xlabel('Date')
plt.ylabel('Valeur')
plt.legend()
plt.show()
"""

"""
#Création du graphique
fig, ax = plt.subplots()

ax.plot(temps, energie_fb, label='Énergie Fourneau Bouillieur')
ax.plot(temps, energie_ts, label='Énergie Thermique Solaire')

ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

plt.xticks(rotation=45)

ax.set_xlabel('Temps')  
ax.set_ylabel('Energie instantanée')
ax.set_title('Énergie instantanée du fourneau bouillieur et de la thermique solaire')

fig.autofmt_xdate()

ax.legend()
plt.show()
"""




