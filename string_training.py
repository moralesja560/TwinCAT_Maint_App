import sys
import os
import math
import pandas as pd


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def avg_total_cut(pn):
	try:
		pn = int(pn)
	except:
		pn = str(pn)
	finally:
		pn_db_df = pd.read_csv(resource_path("images/pn_db.csv"))
		resulting_df = pn_db_df['Part_Number'] == pn
		pn_total_qty = pn_db_df.loc[resulting_df, 'Springs'].mean()
	

	if math.isnan(pn_total_qty):
		pn_total_qty = 1000

	return pn_total_qty


aaa = avg_total_cut(90151339)

print(aaa)