import time
from datetime import datetime
import os #pour supprimer les fichiers
import csv 
import pytz


#lecture des sondes de la maison
with open("/Users/grillot/Downloads/Sondes/temp_maison.csv", 'r', encoding='latin-1') as fichier:
    lecteur_csv = csv.reader(fichier, delimiter = ',')
    listes_maison = list(lecteur_csv) #on met le fichier sous forme de liste de listes mais problème : ça donne des caractères 



#lecture des sondes du ballon
with open("/Users/grillot/Downloads/Sondes/temp_ballons.csv", 'r', encoding='latin-1') as fichier:
    lecteur_csv = csv.reader(fichier, delimiter = ',')
    listes_ballons = list(lecteur_csv) #on met le fichier sous forme de liste de listes


for i in range(len(listes_maison)):
    date = listes_maison[i][0]

    utc_zone = pytz.utc
    paris_zone = pytz.timezone('Europe/Paris')

    dt_utc = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    dt_utc = utc_zone.localize(dt_utc)
    dt_paris = dt_utc.astimezone(paris_zone)
    formatted_date_paris = dt_paris.strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.strptime(formatted_date_paris, '%Y-%m-%d %H:%M:%S')

    path = "data/%04d/%02d/sondes_maison_%02d.csv"%(date.year, date.month, date.day)

    to_write = [date]+[float(listes_maison[i][j]) for j in range(1, 7)] 

    if(not os.path.isdir('data')):
        os.mkdir('data')
        
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
                                ['Maison1'] +
                                ['Maison2'] +
                                ['Maison3'] +
                                ['Maison4'] +
                                ['Maison5'] +
                                ['Maison6'])


            spam_writer.writerow(to_write)

    elif os.path.exists(path):
        # Réouvrir le fichier en mode ajout pour ajouter les données
        with open(path, 'a') as fichier_ajout:
            spam_writer = csv.writer(fichier_ajout, delimiter=';', lineterminator="\n")
            spam_writer.writerow(to_write)


for i in range(len(listes_ballons)):
    date = listes_ballons[i][0]

    utc_zone = pytz.utc
    paris_zone = pytz.timezone('Europe/Paris')

    dt_utc = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    dt_utc = utc_zone.localize(dt_utc)
    dt_paris = dt_utc.astimezone(paris_zone)
    formatted_date_paris = dt_paris.strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.strptime(formatted_date_paris, '%Y-%m-%d %H:%M:%S')

    path = "data/%04d/%02d/sondes_ballons_%02d.csv"%(date.year, date.month, date.day)

    to_write = [date]+[float(listes_ballons[i][j]) for j in range(1, 5)] 

    if(not os.path.isdir('data')):
        os.mkdir('data')
        
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
                                ['Ballon1'] +
                                ['Ballon2'] +
                                ['Ballon3'] +
                                ['Ballon4'])

            spam_writer.writerow(to_write)

    elif os.path.exists(path):
        # Réouvrir le fichier en mode ajout pour ajouter les données
        with open(path, 'a') as fichier_ajout:
            spam_writer = csv.writer(fichier_ajout, delimiter=';', lineterminator="\n")
            spam_writer.writerow(to_write)

"""
os.remove("/Users/grillot/Downloads/Re_ Flux Node Red sondes-4/Sondes/temp_ballons.csv")
os.remove("/Users/grillot/Downloads/Re_ Flux Node Red sondes-4/Sondes/temp_maison.csv")
"""