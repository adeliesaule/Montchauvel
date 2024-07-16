import pandas as pd
import numpy as np 
import datetime
import os 


current_day = datetime.date.today()
day = current_day - datetime.timedelta(days=1)
print(day)
path = "data/%04d/%02d/th_%02d.csv"%(day.year, day.month, day.day)
print(path)
    

pathMAISON = "data/%04d/%02d/sondes_maison_%02d.csv"%(day.year, day.month, day.day)
pathBALLON = "data/%04d/%02d/sondes_ballons_%02d.csv"%(day.year, day.month, day.day)
pathSMA = "data/%04d/%02d/SMA_%02d.csv"%(day.year, day.month, day.day)
pathCTH = "data/%04d/%02d/th_%02d.csv"%(day.year, day.month, day.day)


dataframe_BALLON = pd.read_csv(pathBALLON, encoding='latin-1', sep=';')
dataframe_MAISON = pd.read_csv(pathMAISON, encoding='latin-1', sep=';')
dataframe_MAISON['Heure (HH:MM:SS)'] = dataframe_BALLON['Heure (HH:MM:SS)']

dataframe_BALLON = dataframe_BALLON.set_index('Heure (HH:MM:SS)')
dataframe_MAISON = dataframe_MAISON.set_index('Heure (HH:MM:SS)')

dataframe_BALLON = dataframe_BALLON[["Ballon3"]]
dataframe_MAISON = dataframe_MAISON[["Maison1", "Maison2"]]

dataframe_temps = dataframe_MAISON.join(dataframe_BALLON, how = 'outer')


dataframe_SMA = pd.read_csv(pathSMA, encoding='latin-1', sep=';')
dataframe_SMA = dataframe_SMA.set_index('Heure (HH:MM:SS)')
dataframe_SMA = dataframe_SMA[["Charge de la batterie", "Energie_tot consommée sur 1h"]]
dataframe_SMA = dataframe_SMA.rename(columns={"Energie_tot consommée sur 1h": "Energie instantanée SunnyBoy (kWh)"})


path_parts = pathCTH.split('/')
year = int(path_parts[3])
month = int(path_parts[4])
day = int(path_parts[5].split('_')[1].split('.')[0])


dataframe_CTH = pd.read_csv(pathCTH, encoding='latin-1', sep=';')
dataframe_CTH = dataframe_CTH.set_index('Heure (HH:MM:SS)')

dataframe_CTH['date'] = pd.to_datetime(f"{year}-{month:02d}-{day:02d} " + dataframe_CTH.index.astype(str))
dataframe_CTH = dataframe_CTH.set_index('date')

c = 4180.0
rho = 1000.0

dataframe_CTH["Puissance calculée TS"] = dataframe_CTH["Diff entrée-sortie TS (K)"].mul(dataframe_CTH["Débit volumique TS (l/h)"]) * c * rho * 2.77778e-7
dataframe_CTH["Energie calculée TS"] = dataframe_CTH["Puissance calculée TS"] / (6 * 1000) 

dataframe_CTH["Puissance calculée FB"] = dataframe_CTH["Diff entrée-sortie FB (K)"].mul(dataframe_CTH["Débit volumique FB (l/h)"]) * c * rho * 2.77778e-7
dataframe_CTH["Energie calculée FB"] = dataframe_CTH["Puissance calculée FB"] / (6 * 1000) 

df = dataframe_CTH[['Energie calculée TS', 'Energie calculée FB']]
df.index = pd.to_datetime(df.index)

df_resampled = df.resample('H').sum()
df_resampled.index = df_resampled.index + pd.Timedelta(minutes=30)
df_resampled['dates'] = df_resampled.index


dataframe_temps.index = pd.to_datetime(dataframe_temps.index)
dataframe_SMA.index = pd.to_datetime(dataframe_SMA.index)

dataframe_SMA['date'] = dataframe_SMA.index
dataframe_temps['date'] = dataframe_temps.index


# Fusionner les DataFrames en utilisant la date la plus proche
merged_df = pd.merge_asof(dataframe_SMA, dataframe_temps, on='date', direction='nearest')
merged_df = merged_df.set_index('date')
merged_df['dates'] = merged_df.index

merged_final = pd.merge_asof(df_resampled, merged_df, on='dates', direction='nearest')
merged_final = merged_final.set_index('dates')

#day_precedent = day - datetime.timedelta(days=1)

# Création du fichier CSV final 
path_final = "data_final/%04d/%02d/final_%02d.csv"%(day.year, day.month, day.day)
# Extraire le répertoire du chemin
directory = os.path.dirname(path_final)

# Vérifier si le répertoire existe, sinon le créer
if not os.path.exists(directory):
    os.makedirs(directory)

merged_final.to_csv(path_final)
