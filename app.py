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

load_dotenv()
token_Tel = os.getenv('TOK_EN_BOT')
Jorge_Morales = os.getenv('JORGE_MORALES')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



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

def alarma_decoder(data):
	for x in range(len(data)):
		#print(data[x])
		if data[x] == '1':
			maquina = rows[x][1]
			print(f"Alarma en {maquina}")
			send_message(Jorge_Morales,quote(f"Alarma en {maquina}"),token_Tel)
			time.sleep(10)


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
		#symbol = plc.get_symbol("Ethernet.SD_Online_Printer_Send_String_Ethernet")
		#symbol.auto_update = True
		while True:
			time.sleep(0.5)
			data = plc.read_by_name("PB_Netzwerk.UDP_READY_STRING", plc_datatype=pyads.PLCTYPE_STRING)
			if "000000000000000000"  in data:
				#print(f"nada {data} {random.randint(1,500)}")
				pass
			else:
				print(f'ya pego {data}')
				alarma_decoder(data)
			
			if self._stop_event.is_set():
				# close connection
				print("saliendo")
				plc.close()
				break
	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()
#----------------------end of thread 1------------------#

if __name__ == '__main__':

	with open(resource_path("images/dir.csv")) as file:
		type(file)
		csvreader = csv.reader(file)
		#header = []
		#header = next(csvreader)
		rows = []
		for row in csvreader:
			rows.append(row)

	print(rows)

		
	# connect to the PLC
	#try:
	pyads.open_port()
	ams_net_id = pyads.get_local_address().netid
	print(ams_net_id)
	pyads.close_port()
	#plc = pyads.Connection('10.65.96.40.1.1', 801)
	plc=pyads.Connection('10.65.96.40.1.1', 801, '10.65.96.40')
	#except:
	#	print("No se pudo abrir la conexión")
	#	sys.exit()
	# open the connection
	#else:
	thread1 = hilo1()
	thread1.start()
	while True:
		stop_signal = input()
		if stop_signal == "T":
			thread1.stop()
			break