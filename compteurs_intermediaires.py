import time
import datetime
import os #pour supprimer les fichiers
import csv 


#lecture du fourneau bouilleur
with open("/Users/grillot/Documents/Projet Montchauvel/donnees.csv", 'r', encoding='latin-1') as fichier:
    lecteur_csv = csv.reader(fichier, delimiter = ';')
    listes = list(lecteur_csv) #on met le fichier sous forme de liste de listes mais problème : ça donne des caractères 

    ''' on supprime les 34 premières lignes pour avoir les données du fourneau bouilleur '''
    listes_fb = listes[36:70]

    print(listes_fb)
    print(len(listes_fb))


#lecture du thermique solaire
with open("/Users/grillot/Documents/Projet Montchauvel/donnees.csv", 'r', encoding='latin-1') as fichier:
    lecteur_csv = csv.reader(fichier, delimiter = ';')
    listes = list(lecteur_csv) #on met le fichier sous forme de liste de listes

    ''' on supprime les 34*4 premières lignes pour avoir les données du thermique solaire'''
    listes_ts = listes[2+34*4:2+34*5]

    print(listes_ts)
    print(len(listes_ts))


#Chemin d'acces du .csv qu'on crée
day = datetime.date.today()
path = "data/%04d/%02d/th_%02d.csv"%(day.year, day.month, day.day)
print(path)
    
if(not os.path.isdir('data')):
    os.mkdir('data')
    
#Si le dossier correspondant a l'annee n'existe pas, on le crée
if(not os.path.isdir('data/'+str(day.year))):
    os.mkdir('data/'+str(day.year))
#de meme pour le mois
if(not os.path.isdir("data/%04d/%02d"%(day.year, day.month))):
    os.mkdir("data/%04d/%02d"%(day.year, day.month))
        
path = "data/%04d/%02d/th_%02d.csv"%(day.year, day.month, day.day)
h = datetime.datetime.now().hour
m = datetime.datetime.now().minute

to_write = ["%02d:%02d:00"%(h, m)]+[float(listes_ts[0][7])] + [float(listes_ts[14][7])] + [float(listes_ts[10][7])] + [float(listes_ts[11][7])] + [float(listes_ts[12][7])] + [float(listes_ts[13][7])] + [float(listes_ts[32][7])] + [float(listes_fb[0][7])] + [float(listes_fb[14][7])] + [float(listes_fb[10][7])] + [float(listes_fb[11][7])] + [float(listes_fb[12][7])] + [float(listes_fb[13][7])] + [float(listes_fb[32][7])]

if(not os.path.exists(path)):
    with open(path, 'w') as fichier:
        #Ouverture du fichier
        spam_writer = csv.writer(fichier, delimiter=';', lineterminator="\n")
        #On ajoute la ligne du debut comme le fichier n'existait pas
        spam_writer.writerow(['Heure (HH:MM:SS)'] +
                            ['Energie instantanée incrémentée TS (kWh)'] +
                            ['Puissance TS (W)'] +
                            ['Débit volumique TS (l/h)'] +
                            ['T_entrée TS (°C)'] +
                            ['T_sortie TS (°C)'] +
                            ['Diff entrée-sortie TS (K)'] +
                            ['Energie dépensée le dernier mois TS (kWh)']+
                            ['Energie instantanée incrémentée FB (kWh)'] +
                            ['Puissance FB (W)'] +
                            ['Débit volumique FB (l/h)'] +
                            ['T_entrée FB (°C)'] +
                            ['T_sortie FB (°C)'] +
                            ['Diff entrée-sortie FB (K)'] +
                            ['Energie dépensée le dernier mois FB (kWh)'] +
                            ['Energie instantanée TS (kWh)'] +
                            ['Energie instantanée FB (kWh)'])

        to_write += [0] + [0] #on rajoute la première valeur du tableau au pif parce que pour le moment on ne peut pas faire la différence
        spam_writer.writerow(to_write)

elif os.path.exists(path):
    with open(path, 'r') as fichier:
        # Ouverture du fichier
        lecteur_csv = csv.reader(fichier, delimiter=';')
        listes = list(lecteur_csv)  # Met le fichier sous forme de liste de listes
        n = len(listes)
        print(listes)

        if n >= 2:
            to_write += [float(listes[n-1][1]) - to_write[1]] + [float(listes[n-1][8]) - to_write[8]]
            # Réouvrir le fichier en mode ajout pour ajouter les données
            with open(path, 'a') as fichier_ajout:
                spam_writer = csv.writer(fichier_ajout, delimiter=';', lineterminator="\n")
                spam_writer.writerow(to_write)

os.remove("donnees.csv") #pour supprimer le fichier données (marche que si il existe)