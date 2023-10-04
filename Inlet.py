import pyads
import sys
import threading
import time
import sys
from dotenv import load_dotenv
import os
from urllib.request import Request, urlopen
import json
from urllib.parse import quote
import datetime
import csv
import random
import pandas as pd
from datetime import datetime

load_dotenv()
token_Tel = os.getenv('TOK_EN_BOT')
Jorge_Morales = os.getenv('JORGE_MORALES')


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

def send_message(user_id, text,token):
	global json_respuesta
	url = f"https://api.telegram.org/{token}/sendMessage?chat_id={user_id}&text={text}"
	#resp = requests.get(url)
	#hacemos la petición
	try:
		respuesta  = urlopen(Request(url))
	except Exception as e:
		print(f"Ha ocurrido un error al enviar el mensaje: {e}")
	else:
		#recibimos la información
		cuerpo_respuesta = respuesta.read()
		# Procesamos la respuesta json
		json_respuesta = json.loads(cuerpo_respuesta.decode("utf-8"))
		print("mensaje enviado exitosamente")

def state_recover():
	ruta_state = resource_path("images/last_state.csv")
	file_exists = os.path.exists(ruta_state)
	if file_exists == True:
		pass
	else:
		with open(ruta_state,"w+") as f:
			f.write(f"False,False,False,False")		

	with open(resource_path("images/last_state.csv")) as file:
		type(file)
		csvreader = csv.reader(file)
		#header = []
		#header = next(csvreader)
		#header
		rows2 = []
		for row in csvreader:
			rows2.append(row)

		
		fmb46_state = eval(rows2[0][0])
		fmb01_state  = eval(rows2[0][1])
		ful103_state = eval(rows2[0][2])
		fmb12_state = eval(rows2[0][3])
		return fmb46_state,fmb01_state,ful103_state,fmb12_state

def state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state):
	ruta_state = resource_path("images/last_state.csv")

	with open(ruta_state, "w+") as file_object:

		file_object.write(f"'{fmb46_state}','{fmb01_state}','{ful103_state}','{fmb12_state}'")

##--------------------the thread itself--------------#

class hilo1(threading.Thread):
	#thread init procedure
	# i think we pass optional variables to use them inside the thread
	def __init__(self):
		threading.Thread.__init__(self)
		self._stop_event = threading.Event()
	#the actual thread function
	def run(self):
		fmb46_state,fmb01_state,ful103_state,fmb12_state = state_recover()
		plc.open()
		plc1.open()
		while True:
			try:
				#Coil Sensor
				coil_sensor_46 = plc.read_by_name(".I_FMB46_Ringsensor", plc_datatype=pyads.PLCTYPE_BOOL)
				coil_sensor_01 = plc.read_by_name(".I_FMB1_Ringsensor", plc_datatype=pyads.PLCTYPE_BOOL)
				coil_sensor_103 = plc1.read_by_name(".I_FUL103_Ringsensor", plc_datatype=pyads.PLCTYPE_BOOL)
				coil_sensor_12 = plc1.read_by_name(".I_FMB12_Ringsensor", plc_datatype=pyads.PLCTYPE_BOOL)
				#Automatic Status
				Automatic_46 = plc.read_by_name(".I_WA1_Automatik", plc_datatype=pyads.PLCTYPE_BOOL)
				Automatic_01 = plc.read_by_name(".I_WA2_Automatik", plc_datatype=pyads.PLCTYPE_BOOL)
				Automatic_12 = plc1.read_by_name(".I_WA1_Automatik", plc_datatype=pyads.PLCTYPE_BOOL)
				Automatic_103 = plc1.read_by_name(".I_WA2_Automatik", plc_datatype=pyads.PLCTYPE_BOOL)				
				#Part Number
				pn_46 = plc.read_by_name(".TP_IW_FMB46_Setup_Part_Number", plc_datatype=pyads.PLCTYPE_STRING)
				pn_01 = plc.read_by_name(".TP_IW_FMB1_Setup_Part_Number", plc_datatype=pyads.PLCTYPE_STRING)
				pn_12 = plc1.read_by_name(".TP_IW_FMB12_Setup_Part_Number", plc_datatype=pyads.PLCTYPE_STRING)
				pn_103 = plc1.read_by_name(".TP_IW_FMB22_Setup_Part_Number", plc_datatype=pyads.PLCTYPE_STRING)
				#Daily Counter to track coil performance
				cut_01 = plc.read_by_name(".Day_Spring_Count_FMB1_1", plc_datatype=pyads.PLCTYPE_UINT)
				cut_46 = plc.read_by_name(".Day_Spring_Count_FMB1_46", plc_datatype=pyads.PLCTYPE_UINT)				
				cut_12 = plc1.read_by_name(".Day_Spring_Count_FMB12", plc_datatype=pyads.PLCTYPE_UINT)
				cut_103 = plc1.read_by_name(".Day_Spring_Count_FMB22", plc_datatype=pyads.PLCTYPE_UINT)

			except Exception as e:
				print(e)
				plc.close()
				plc1.close()
				break
			else:
				pass
			#writelog					
			write_log(coil_sensor_46,coil_sensor_01,Automatic_01,Automatic_46,pn_46,pn_01,coil_sensor_103,coil_sensor_12,Automatic_103,Automatic_12,pn_12,pn_103)
			print(fmb46_state,fmb01_state,ful103_state,fmb12_state)
			#SECTION TO CHECK FOR COIL FINISH
			#FUL103
			if ful103_state != coil_sensor_103:
				# if false means that coil is starting
				if ful103_state == False:
					write_report('Start','FUL103', pn_103,cut_103)
					ful103_state = coil_sensor_103
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
				elif ful103_state == True:
					write_report('End','FUL103', pn_103,cut_103)
					ful103_state = coil_sensor_103
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
			#FMB12
			if fmb12_state != coil_sensor_12:
				# if false means that coil is starting
				if fmb12_state == False:
					write_report('Start','FMB12', pn_12,cut_12)
					fmb12_state = coil_sensor_12
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
				elif fmb12_state == True:
					write_report('End','FMB12', pn_12,cut_12)
					fmb12_state = coil_sensor_12
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
			#FMB01
			if fmb01_state != coil_sensor_01:
				# if false means that coil is starting
				if fmb01_state == False:
					write_report('Start','FMB1', pn_01,cut_01)
					fmb01_state = coil_sensor_01
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
				elif fmb01_state == True:
					write_report('End','FMB1', pn_01,cut_01)
					fmb01_state = coil_sensor_01	
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)			
			#FMB46
			if fmb46_state != coil_sensor_46:
				# if false means that coil is starting
				if fmb46_state == False:
					write_report('Start','FMB46', pn_46,cut_46)
					fmb46_state = coil_sensor_46
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
				elif fmb46_state == True:
					write_report('End','FMB46', pn_46,cut_46)
					fmb46_state = coil_sensor_46
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)	
			#Update time
			time.sleep(2)

			if self.stopped == True:
				thread1.stop()
				plc.close()
				plc1.close()
				break
	
	def stop(self):
		print("si entre a stopear")
		self.stopped = True
		self._stop_event.set()


	def stopped(self):
		return self._stop_event.is_set()
#----------------------end of thread 1------------------#

#---------------Thread 2 Area----------------------#
class hilo2(threading.Thread):
	#thread init procedure
	# i think we pass optional variables to use them inside the thread
	def __init__(self,thread_name,opt_arg):
		threading.Thread.__init__(self)
		self.thread_name = thread_name
		self.opt_arg = opt_arg
		self._stop_event = threading.Event()
	#the actual thread function
	def run(self):
		#check for thread1 to keep running
		while True:
			if [t for t in threading.enumerate() if isinstance(t, hilo1)]:
				try:
					time.sleep(5)
				except:
					self._stop_event.set()
			else:
				print(f"A problem occurred... Restarting Thread 1")
				time.sleep(4)
				thread1 = hilo1()
				thread1.start()
				print(f"Thread 1 Started")
			
			if self._stop_event.is_set() == True:
				print("Thread 2 Stopped")
				break

	def stop(self):
		self._stop_event.set()

def write_log(coil_sensor_46,coil_sensor_01,Automatic_01,Automatic_46,pn_46,pn_01,coil_sensor_103,coil_sensor_12,Automatic_103,Automatic_12,pn_12,pn_103):
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
				file_object.write(f" timestamp: {dt_string}, FMB_46_Coil: {coil_sensor_46}, FMB_01_Coil: {coil_sensor_01}, Automatic_01: {Automatic_01}, Automatic_46: {Automatic_46}, Num_Parte_46: {pn_46},Num_Parte_01: {pn_01}, FMB_12_Coil: {coil_sensor_12}, FUL103__Coil: {coil_sensor_103}, Automatic_12: {Automatic_12}, Automatic_103: {Automatic_103}, Num_Parte_12: {pn_12},Num_Parte_103: {pn_103}")
	else:
		with open(ruta,"w+") as f:
				f.write(f" timestamp: {dt_string}, FMB_46_Coil: {coil_sensor_46}, FMB_01_Coil: {coil_sensor_01}, Automatic_01: {Automatic_01}, Automatic_46: {Automatic_46}, Num_Parte_46: {pn_46},Num_Parte_01: {pn_01}, FMB_12_Coil: {coil_sensor_12}, FUL103__Coil: {coil_sensor_103}, Automatic_12: {Automatic_12}, Automatic_103: {Automatic_103}, Num_Parte_12: {pn_12},Num_Parte_103: {pn_103}")
	#check if pandas DataFrame exists to load the stuff or to create with dummy data.
	if pd_file_exists:
		pd_log = pd.read_csv(pd_ruta)
	else:
		pd_log = pd.DataFrame(pd_dict)

	new_row = {'timestamp' : [dt_string], 'FMB_46_Coil' : [coil_sensor_46], 'FMB_01_Coil' : [coil_sensor_01], 'Automatic_01' : [Automatic_01], 'Automatic_46' : [Automatic_46], 'Num_Parte_46' : [pn_46], 'Num_Parte_01' : [pn_01], 'FMB_12_Coil' : [coil_sensor_12], 'FUL_103_Coil' : [coil_sensor_103], 'Automatic_12' : [Automatic_12], 'Automatic_103' : [Automatic_103], 'Num_Parte_12' : [pn_12], 'Num_Parte_103' : [pn_103]}
	new_row_pd = pd.DataFrame(new_row)
	pd_concat = pd.concat([pd_log,new_row_pd])
	pd_concat.to_csv(pd_ruta,index=False)

def write_report(type,machine,part_number,cuts):
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	#print("date and time =", dt_string)	
	mis_docs = My_Documents(5)
	ruta = str(mis_docs)+ r"\machine_report.txt"
	pd_ruta = str(mis_docs)+ r"\machine_report.csv"
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
				file_object.write(f" timestamp: {dt_string}, Event: {type}, Machine: {machine}, Part_Number: {part_number}, Pieces: {cuts}")
	else:
		with open(ruta,"w+") as f:
				f.write(f" timestamp: {dt_string}, Event: {type}, Machine: {machine}, Part_Number: {part_number}, Pieces: {cuts}")
	#check if pandas DataFrame exists to load the stuff or to create with dummy data.
	if pd_file_exists:
		pd_log = pd.read_csv(pd_ruta)
	else:
		pd_log = pd.DataFrame(pd_dict2)

	new_row = {'timestamp' : [dt_string], 'Type' : [type], 'Machine' : [machine], 'Part_Number' : [part_number], 'Pieces' : [cuts]}
	new_row_pd = pd.DataFrame(new_row)
	pd_concat = pd.concat([pd_log,new_row_pd])
	pd_concat.to_csv(pd_ruta,index=False)


#Pandas DataFrame dictionaries
pd_dict = {'timestamp' : ['0'], 'FMB_46_Coil' : ['0'], 'FMB_01_Coil' : ['0'], 'Automatic_01' : ['0'], 'Automatic_46' : ['0'], 'Num_Parte_46' : ['0'], 'Num_Parte_01' : ['0'], 'FMB_12_Coil' : ['0'], 'FUL_103_Coil' : ['0'], 'Automatic_12' : ['0'], 'Automatic_103' : ['0'], 'Num_Parte_12' : ['0'], 'Num_Parte_103' : ['0']}
pd_dict2 = {'timestamp' : ['0'], 'Type' : ['0'], 'Machine' : ['0'], 'Part_Number' : ['0'], 'Pieces': ['0']}


if __name__ == '__main__':

	# connect to the PLC
	try:
		pyads.open_port()
		ams_net_id = pyads.get_local_address().netid
		print(ams_net_id)
		pyads.close_port()
		plc=pyads.Connection('10.65.96.102.1.1', 801, '10.65.96.102')
		plc1 = pyads.Connection('10.65.96.38.1.1', 801, '10.65.96.38')

	except:
		print("No se pudo abrir la conexión")
		sys.exit()
	 #open the connection
	else:
		pass
	thread1 = hilo1()
	thread1.start()
	thread2 = hilo2(thread_name="hilo2",opt_arg="h")
	thread2.start()
	while True:
		stop_signal = input()
		if stop_signal == "T":
			thread1.stop()
			thread2.stop()
		break