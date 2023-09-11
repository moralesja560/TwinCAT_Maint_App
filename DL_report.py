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

# 6
database['input diameter'] = 0
# 7
database['output diameter'] = 0
# 8
database['hour'] = database['timestamp'].dt.hour
# 9
database["Day/Night"] = "c"
# 10
database["Status"] = "d"




for x in range(0,database['timestamp'].count()):
	print(database.iloc[x,0])
	for y in range(0,dl_prod['start'].count()):
		if database.iat[x,0] >= dl_prod.iat[y,36] and database.iat[x,0] <= dl_prod.iat[y,37]:
			database.iat[x,6] = dl_prod.iat[y,6]
			database.iat[x,7] = dl_prod.iat[y,17]
			break

	if database.iat[x,8] >= 7 and  database.iat[x,8] <= 19:
		database.iat[x,9] = "Day"
	else:
		database.iat[x,9] = "Night"
	if database.iat[x,1] == 0 and database.iat[x,4] == 0:
		database.iat[x,10] = "Stopped"
	else:
		database.iloc[x,10] = "Run"



# diametro
database['reduction ratio'] = (database['output diameter']-database['input diameter'])/database['input diameter']
#velocidad
database['speed ratio'] = (database['Vel Actual']-database['Vel Teórica'])/database['Vel Teórica']



database.to_csv(resource_path("images/finished_db.csv"),index=False)

