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

##--------------------the thread itself--------------#

class hilo1(threading.Thread):
	#thread init procedure
	# i think we pass optional variables to use them inside the thread
	def __init__(self):
		threading.Thread.__init__(self)
		self._stop_event = threading.Event()
	#the actual thread function
	def run(self):
		plc.open()		
		plc_dsa.open()
		while True:
			try:
				#corriente
				current = plc.read_by_name("PB_Ziehblock_Antriebe.Ziehblock_Current", plc_datatype=pyads.PLCTYPE_UINT)
				# micrometro de entrada
				diameter= plc_dsa.read_by_name("Main.Average_Dimension_REAL", plc_datatype=pyads.PLCTYPE_REAL)
				# velocidad de referencia'
				reference_speed = plc.read_by_name("PB_Ziehblock_Antriebe.Ziehblock_Reference_Value", plc_datatype=pyads.PLCTYPE_UINT)
				# velocidad actual'
				actual_speed = plc.read_by_name("PB_Ziehblock_Antriebe.Ziehblock_Actual_Value", plc_datatype=pyads.PLCTYPE_UINT)
				# temp de referencia UEKO
				reference_Temp = plc.read_by_name("PB_Ziehblock_Antriebe.Reference_UEKO_Drive_Temp", plc_datatype=pyads.PLCTYPE_INT)
			except Exception as e:
				#send_message(Jorge_Morales,quote(f"Falla de app: {e}. Si es el 1861, por favor conectarse al PLC via Twincat System Manager. Con eso se hace la conexión ADS"),token_Tel)
				print(e)
				plc.close()
				plc_dsa.close()
				break
			else:
				#writelog					
				write_log(current,diameter,reference_speed,actual_speed,reference_Temp)
				print(current,diameter,reference_speed,actual_speed,reference_Temp)
				time.sleep(3)

			if self._stop_event.is_set():
				# close connection
				print("saliendo")
				plc.close()
				plc_dsa.close()
				break
	def stop(self):
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

def write_log(current,diameter,reference_speed,actual_speed,reference_Temp):
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	#print("date and time =", dt_string)	
	mis_docs = My_Documents(5)
	ruta = str(mis_docs)+ r"\registro_corriente.txt"
	pd_ruta = str(mis_docs)+ r"\registro_corriente_df.csv"
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
				file_object.write(f" timestamp {dt_string}: Corriente: {current} diametro: {diameter},Vel Teórica: {reference_speed},Vel Actual: {actual_speed},Temp de Referencia: {reference_Temp}")
	else:
		with open(ruta,"w+") as f:
				f.write(f" timestamp {dt_string}: Corriente: {current} diametro: {diameter},Vel Teórica: {reference_speed},Vel Actual: {actual_speed},Temp de Referencia: {reference_Temp}")

	#check if pandas DataFrame exists to load the stuff or to create with dummy data.
	if pd_file_exists:
		pd_log = pd.read_csv(pd_ruta)
	else:
		pd_log = pd.DataFrame(pd_dict)

	new_row = {'timestamp' : [dt_string], 'current' : [current], 'diametro' : [diameter], 'Vel Teórica' : [reference_speed], 'Vel Actual' : [actual_speed], 'Temp de Referencia' : [reference_Temp]}
	new_row_pd = pd.DataFrame(new_row)
	pd_concat = pd.concat([pd_log,new_row_pd])
	pd_concat.to_csv(pd_ruta,index=False)


#Pandas DataFrame dictionaries
pd_dict = {'timestamp' : ['dummy'], 'current' : ['dummy'],	'diametro' : ['dummy'], 'Vel Teórica' : ['dummy'], 'Vel Actual' : ['dummy'], 'Temp de Referencia' : ['dummy']}



if __name__ == '__main__':

	# connect to the PLC
	try:
		pyads.open_port()
		ams_net_id = pyads.get_local_address().netid
		print(ams_net_id)
		pyads.close_port()
	#plc = pyads.Connection('10.65.96.40.1.1', 801)
		plc=pyads.Connection('10.65.96.81.1.1', 801, '10.65.96.81')
		plc_dsa = pyads.Connection('10.65.96.84.1.1', 801, '10.65.96.84')
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