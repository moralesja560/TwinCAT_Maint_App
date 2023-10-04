import pyads
import csv
import time
import sys, os
from datetime import datetime
import pandas as pd


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def My_Documents(location):
	import ctypes.wintypes
		#####-----This section discovers My Documents default path --------
		#### loop the "location" variable to find many paths, including AppData and ProgramFiles
	CSIDL_PERSONAL = location       # My Documents
	SHGFP_TYPE_CURRENT = 0   # Get current, not default value
	buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
	ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
	#####-------- please use buf.value to store the data in a variable ------- #####
	#add the text filename at the end of the path
	temp_docs = buf.value
	return temp_docs

def write_log(coil_status):
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	#print("date and time =", dt_string)	
	mis_docs = My_Documents(5)
	ruta = str(mis_docs)+ r"\coil_sensor.txt"
	pd_ruta = str(mis_docs)+ r"\coil_sensor.csv"
	file_exists = os.path.exists(ruta)
	pd_file_exists = os.path.exists(pd_ruta)
	if file_exists == True:
		with open(ruta, "a+") as file_object:
			# Move read cursor to the start of file.
			file_object.seek(0)
			# If file is not empty then append '\n'
			data = file_object.read(100)
			if len(data) > 0 :
				file_object.write("\n")
				file_object.write(f" timestamp: {dt_string}, FMB_46_Coil: {coil_sensor_46}, FMB_01_Coil: {coil_sensor_01}, Automatic_01: {Automatic_01}, Automatic_46: {Automatic_46}, Num_Parte_46: {pn_46},Num_Parte_01: {pn_01}")
	else:
		with open(ruta,"w+") as f:
				f.write(f" timestamp: {dt_string}, FMB_46_Coil: {coil_sensor_46}, FMB_01_Coil: {coil_sensor_01}, Automatic_01: {Automatic_01}, Automatic_46: {Automatic_46}, Num_Parte_46: {pn_46},Num_Parte_01: {pn_01}")

	#check if pandas DataFrame exists to load the stuff or to create with dummy data.
	if pd_file_exists:
		pd_log = pd.read_csv(pd_ruta)
	else:
		pd_log = pd.DataFrame(pd_dict)

	new_row = {'timestamp' : [dt_string], 'FMB_46_Coil' : [coil_sensor_46], 'FMB_01_Coil' : [coil_sensor_01], 'Automatic_01' : [Automatic_01], 'Automatic_46' : [Automatic_46], 'Num_Parte_46' : [pn_46], 'Num_Parte_01' : [pn_01]}
	new_row_pd = pd.DataFrame(new_row)
	pd_concat = pd.concat([pd_log,new_row_pd])
	pd_concat.to_csv(pd_ruta,index=False)


#Pandas DataFrame dictionaries
pd_dict = {'timestamp' : ['0'], 'FMB_46_Coil' : ['0'], 'FMB_01_Coil' : ['0'], 'Automatic_01' : ['0'], 'Automatic_46' : ['0'], 'Num_Parte_46' : ['0'], 'Num_Parte_01' : ['0']}







# connect to the PLC
plc = pyads.Connection('10.65.96.38.1.1', 801,'10.65.96.38')

# open the connection
plc.open()

# read the device name and the version
device_name, version = plc.read_device_info()
print(str(device_name) + ' ' + str(version))

print(f"Connected?: {plc.is_open}") #debugging statement, optional
print(f"Local Address? : {plc.get_local_address()}") #debugging statement, optional

p_state = False

while True:
	#read a boolean
	coil_status = plc.read_by_name('.Dummy12', pyads.PLCTYPE_BOOL)
	if p_state != coil_status:
		print(f"variable changed from {p_state} to {coil_status}")
		p_state = coil_status
		write_log(coil_status)
	time.sleep(2)
	

	



plc.close()
