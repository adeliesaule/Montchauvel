import time
import datetime
import csv 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import  numpy as np
import pandas as pd 


listes = []
for i in range(21, 31):
    with open("data_final/" + str(i) + ".csv", 'r', encoding='latin-1') as fichier:
        lecteur_csv = csv.reader(fichier, delimiter = ',')
        if i == 21:
            listes += list(lecteur_csv) #on met le fichier sous forme de liste de listes mais problème : ça donne des caractères
        else:
            listes += list(lecteur_csv)[1:]


for i in range(1, 7):
    with open("data_final/" + str(0) + str(i) + ".csv", 'r', encoding='latin-1') as fichier:
        lecteur_csv = csv.reader(fichier, delimiter = ',')
        listes += list(lecteur_csv)[1:]

dates = [listes[i][0] for i in range(1, len(listes))]
energie_FB = [float(listes[i][2]) for i in range(1, len(listes))]
energie_TS = [float(listes[i][1]) for i in range(1, len(listes))]
charge_batterie = [float(listes[i][3]) for i in range(1, len(listes))]
energie_sunnyboy = [float(listes[i][4]) / 1000 for i in range(1, len(listes))]
maison1 = [float(listes[i][5]) for i in range(1, len(listes))]
maison2 = [float(listes[i][6]) for i in range(1, len(listes))]
ballon3 = [float(listes[i][7]) for i in range(1, len(listes))]
#puissance_PV = [float(listes[i][4]) / 1000 * 6 for i in range(1, len(listes))]
energie_sunnyboy[75:99] = [energie_sunnyboy[i] / 2 for i in range(75, 99)]
energie_tot = [energie_FB[i] + energie_TS[i] + energie_sunnyboy[i] for i in range(len(energie_FB))]
energie_nécessaire = [0.150] * len(energie_FB) ##énergie en kWh


data = {
    'energie_FB': energie_FB,
    'energie_TS': energie_TS,
    'energie_tot_sunnyboy': energie_sunnyboy,
    'energie_tot': energie_tot,
    'energie_nécessaire': energie_nécessaire,
    'charge_batterie': charge_batterie,
    'maison1': maison1,
    'maison2': maison2,
    'ballon3': ballon3,
    #'puissance_PV': puissance_PV
}

df = pd.DataFrame(data)
columns = df.columns


date_obj = [datetime.datetime.strptime(dates[i], '%Y-%m-%d %H:%M:%S') for i in range(len(dates))]
time_part = [date_obj[i].strftime('%H:%M:%S') for i in range(len(date_obj))]
new_dates = [datetime.datetime.strptime(time_part[0], '%H:%M:%S') + datetime.timedelta(hours = i) for i in  range(len(time_part))]


# Création de la figure et des sous-graphiques
fig, axs = plt.subplots(1, 2, figsize=(15, 8))  # 6 lignes et 3 colonnes de sous-graphiques

# Boucle pour tracer chaque série de données
for i, ax in enumerate(axs.flat):
    if i == 0:  # S'assurer qu'on ne dépasse pas le nombre de colonnes
        ax.plot(new_dates, df[columns[2]], label=columns[2])
        ax.plot(new_dates, df[columns[4]], label=columns[4])
        ax.set_xlabel('Date')
        ax.set_ylabel('Énergie PV (kWh)')
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45)
        ax.set_title("Production électrique")
        ax.legend()
        ax.set_ylim(0, 2.5)

        ax2 = ax.twinx()
        ax2.set_ylabel('Charge batterie (%)')
        ax2.plot(new_dates, df[columns[5]], label=columns[5], color = 'red')
        ax2.set_ylim(0, 100)
        ax2.legend()

    if i == 1:  # S'assurer qu'on ne dépasse pas le nombre de colonnes
        ax.plot(new_dates, df[columns[6]], label=columns[6])
        ax.plot(new_dates, df[columns[7]], label=columns[7])
        ax.plot(new_dates, df[columns[8]], label=columns[8])
        ax.set_xlabel('Date')
        ax.set_ylabel('Température (°C)')
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45)
        ax.set_title("Production thermique")
        ax.legend()

        ax2 = ax.twinx()
        ax2.set_ylabel('Énergie TS et FB (kWh)')
        ax2.plot(new_dates, df[columns[0]], label=columns[0], color = 'red')
        ax2.plot(new_dates, df[columns[1]], label=columns[1], color = "black")
        #ax2.plot(new_dates, df[columns[9]], label=columns[9], color = "purple")
        ax2.set_ylim(-5, 10)
        ax2.legend()

for ax in axs.flat:
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
plt.tight_layout()
        
# Ajuster l'espacement entre les sous-graphiques


# Afficher la figure
plt.show()