import time
from datetime import datetime, date 
import os #pour supprimer les fichiers
import csv 
import numpy as np
import pytz

#lecture du des ballons
with open("/Users/grillot/Downloads/Re_ Flux Node Red sondes-5/SMA.csv", 'r', encoding='latin-1') as fichier:  # à remplacer par le bon chemin d'accès et le bon nom
    lecteur_csv = csv.reader(fichier, delimiter = ',')
    listes_init = list(lecteur_csv) #on met le fichier sous forme de liste mais problème : ça donne des caractères 
    
    listes = []
    to_write = []
    for i in range(0, len(listes_init)):
        if listes_init[i] != ['Time', '', 'SOC', '', '', '', 'SB 408', '', '', '', 'SB 599', '', '', '', 'SB 677', '', '']:
            listes.append([listes_init[i][0], float(listes_init[i][2]), float(listes_init[i][2]), float(listes_init[i][6]), float(listes_init[i][6]), float(listes_init[i][10]), float(listes_init[i][10]), float(listes_init[i][14]), float(listes_init[i][14])])

to_write = listes
print(to_write)

for i in range(len(to_write)-1, 0, -1):
    to_write[i][1] -= to_write[i-1][2]
    if to_write[i][4] == 0 and to_write[i-1][4] !=0:
        to_write[i][3] = 0 
        to_write[i][4] = 0
    else:
        to_write[i][3] -= to_write[i-1][4]

    if to_write[i][6] == 0 and to_write[i-1][6] !=0:
        to_write[i][5] = 0 
        to_write[i][6] = 0
    else:
        to_write[i][5] -= to_write[i-1][6]

    if  to_write[i][8] == 0 and to_write[i-1][8] !=0:
        to_write[i][7] = 0
        to_write[i][8] = 0
    else:
        to_write[i][7] -= to_write[i-1][8]

for i in range(len(to_write)):
    timestamp = to_write[i][0]
    timestamp_seconds = float(timestamp) / 1000.0
    dt_utc = datetime.utcfromtimestamp(timestamp_seconds)
    utc_zone = pytz.utc
    dt_utc = utc_zone.localize(dt_utc)
    paris_zone = pytz.timezone('Europe/Paris')
    dt_paris = dt_utc.astimezone(paris_zone)

    to_write[i][0] = dt_paris.strftime('%Y-%m-%d %H:%M:%S')
    to_write[i][0]  = datetime.strptime(to_write[i][0], '%Y-%m-%d %H:%M:%S')

if(not os.path.isdir('data')):
    os.mkdir('data')
    


for i in range(len(to_write)):
    date = to_write[i][0]
    path = "data/%04d/%02d/SMA_%02d.csv"%(date.year, date.month, date.day)

    #Si le dossier correspondant a l'annee n'existe pas, on le crée
    if(not os.path.isdir('data/'+str(date.year))):
        os.mkdir('data/'+str(date.year))
    #de meme pour le mois
    if(not os.path.isdir("data/%04d/%02d"%(date.year, date.month))):
        os.mkdir("data/%04d/%02d"%(date.year, date.month))

    if(not os.path.exists(path)):
        with open(path, 'w') as fichier:
            #Ouverture du fichier
            spam_writer = csv.writer(fichier, delimiter=';', lineterminator="\n")
            #On ajoute la ligne du debut comme le fichier n'existait pas
            spam_writer.writerow(['Heure (HH:MM:SS)'] +
                                ['Variation de la charge de la batterie sur 1h'] +
                                ['Charge de la batterie'] +
                                ['SunnyBoy1 sur 1h'] +
                                ['SunnyBoy1 sur la journée'] +
                                ['SunnyBoy2 sur 1h'] +
                                ['SunnyBoy2 sur la journée'] +
                                ['SunnyBoy3 sur 1h'] +
                                ['SunnyBoy3 sur la journée'] +
                                ['Energie_tot consommée sur 1h'])

            spam_writer.writerow(to_write[i] + [np.sum([to_write[i][3], to_write[i][5], to_write[i][7]])])


    elif os.path.exists(path):
        with open(path, 'r') as fichier:
            # Ouverture du fichier
            lecteur_csv = csv.reader(fichier, delimiter=';')
            listes = list(lecteur_csv)  # Met le fichier sous forme de liste de listes
            n = len(listes)

            if len(listes) > 1:
                to_write[0][1] -= float(listes[-1][2])
                to_write[0][3] -= float(listes[-1][4])
                to_write[0][5] -= float(listes[-1][6])
                to_write[0][7] -= float(listes[-1][8])

            if n >= 2:
                # Réouvrir le fichier en mode ajout pour ajouter les données
                with open(path, 'a') as fichier_ajout:
                    spam_writer = csv.writer(fichier_ajout, delimiter=';', lineterminator="\n")
                    spam_writer.writerow(to_write[i] + [np.sum([to_write[i][3], to_write[i][5], to_write[i][7]])])

#os.remove("/Users/grillot/Downloads/Re_ Flux Node Red sondes-4/SMA.csv") #pour supprimer le fichier données (marche que si il existe)