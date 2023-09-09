import pandas as pd
import os,sys
import csv
from datetime import datetime
import numpy as np


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# cargamos los CSV
database = pd.read_csv(resource_path("images/registro_corriente_df.csv"))
dl_prod = pd.read_csv(resource_path("images/drawing_db.csv"))

# convertimos la información de arranque

dl_prod['hour start'] = dl_prod['production start'].str.slice(13,18)
dl_prod['hour end'] = dl_prod['production end'].str.slice(13,18)
dl_prod['day start'] = dl_prod['production start'].str.slice(0,10)
dl_prod['day end'] = dl_prod['production end'].str.slice(0,10)

dl_prod['start'] = pd.to_datetime(dl_prod['day start'] +" " + dl_prod['hour start'])
dl_prod['end'] = pd.to_datetime(dl_prod['day end'] +" " + dl_prod['hour end'])

database['timestamp'] = pd.to_datetime(database['timestamp'])

#agregar la columna de input diameter

database['input diameter'] = 0
database['output diameter'] = 0
database['hour'] = database['timestamp'].dt.hour
database["Day/Night"] = "c"


print(datetime.now())
for x in range(0,database['timestamp'].count()):
	for y in range(0,dl_prod['start'].count()):
		if database.iloc[x,0] >= dl_prod.iloc[y,36] and database.iloc[x,0] <= dl_prod.iloc[y,37]:
			database.iloc[x,6] = dl_prod.iloc[y,6]
			database.iloc[x,7] = dl_prod.iloc[y,17]

for i in range(0,database['timestamp'].count()):
	if database.iloc[i,8] >= 7 and  database.iloc[i,8] <= 19:
		database.iloc[i,9] = "Day"
	else:
		database.iloc[i,9] = "Night"
	
"""
faltan las relaciones de diametro y de velocidad, ademas del status de tiempo muerto: Current = 0 y velocidad actual = 0 


"""


print(datetime.now())           





database.to_csv(resource_path("images/finished_db.csv"),index=False)
