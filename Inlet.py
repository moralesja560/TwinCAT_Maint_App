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
import math
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

		if 'True' in rows2[0][0]:
			fmb46_state = True
		else:
			fmb46_state = False

		if 'True' in rows2[0][1]:
			fmb01_state = True
		else:
			fmb01_state = False

		if 'True' in rows2[0][2]:
			ful103_state = True
		else:
			ful103_state = False

		if 'True' in rows2[0][3]:
			fmb12_state = True
		else:
			fmb12_state = False
		return fmb46_state,fmb01_state,ful103_state,fmb12_state

def state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state):
	ruta_state = resource_path("images/last_state.csv")

	with open(ruta_state, "w+") as file_object:

		file_object.write(f"{fmb46_state},{fmb01_state},{ful103_state},{fmb12_state}")

def pn_state_recover():
	ruta_state_pn = resource_path("images/pn_last_state.csv")
	file_exists = os.path.exists(ruta_state_pn)
	if file_exists == True:
		pass
	else:
		with open(ruta_state_pn,"w+") as f:
			f.write(f"A,A,A,A")		

	with open(resource_path("images/pn_last_state.csv")) as file:
		type(file)
		csvreader = csv.reader(file)
		#header = []
		#header = next(csvreader)
		#header
		rows2 = []
		for row in csvreader:
			rows2.append(row)

		fmb46_pn_state = rows2[0][0]
		fmb01_pn_state = rows2[0][1]
		ful103_pn_state = rows2[0][2]
		fmb12_pn_state = rows2[0][3]
		run_count_46 = int(rows2[0][4])
		run_count_01 = int(rows2[0][5])
		run_count_103 = int(rows2[0][6])
		run_count_12 = int(rows2[0][7])



		return fmb46_pn_state,fmb01_pn_state,ful103_pn_state,fmb12_pn_state,run_count_46,run_count_01,run_count_103,run_count_12

def pn_state_save(fmb46_pn_state,fmb01_pn_state,ful103_pn_state,fmb12_pn_state,run_count_46,run_count_01,run_count_103,run_count_12):
	ruta_state = resource_path("images/pn_last_state.csv")

	with open(ruta_state, "w+") as file_object:

		file_object.write(f"{fmb46_pn_state},{fmb01_pn_state},{ful103_pn_state},{fmb12_pn_state},{run_count_46},{run_count_01},{run_count_103},{run_count_12}")

def cut_state_recover():
	ruta_state_pn = resource_path("images/cut_last_state.csv")
	file_exists = os.path.exists(ruta_state_pn)
	if file_exists == True:
		pass
	else:
		with open(ruta_state_pn,"w+") as f:
			f.write(f"0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")		

	with open(resource_path("images/cut_last_state.csv")) as file:
		type(file)
		csvreader = csv.reader(file)
		#header = []
		#header = next(csvreader)
		#header
		rows2 = []
		for row in csvreader:
			rows2.append(row)

		actual_sp_46 = int(rows2[0][0])
		actual_sp_01 = int(rows2[0][1])
		actual_sp_103 = int(rows2[0][2])
		actual_sp_12 = int(rows2[0][3])
		start_cut_coil_46 = int(rows2[0][4])
		start_cut_coil_01= int(rows2[0][5])
		start_cut_coil_103= int(rows2[0][6])
		start_cut_coil_12= int(rows2[0][7])
		max_cut_46= int(rows2[0][8])
		max_cut_01= int(rows2[0][9])
		max_cut_103= int(rows2[0][10])
		max_cut_12= int(rows2[0][11])
		fmb46_pn_state = rows2[0][12]
		fmb01_pn_state = rows2[0][13]
		ful103_pn_state = rows2[0][14]
		fmb12_pn_state = rows2[0][15]
		run_count_46 = int(rows2[0][16])
		run_count_01 = int(rows2[0][17])
		run_count_103 = int(rows2[0][18])
		run_count_12 = int(rows2[0][19])

		return actual_sp_46,actual_sp_01,actual_sp_103,actual_sp_12,start_cut_coil_46,start_cut_coil_01,start_cut_coil_103,start_cut_coil_12,max_cut_46,max_cut_01,max_cut_103,max_cut_12,fmb46_pn_state,fmb01_pn_state,ful103_pn_state,fmb12_pn_state,run_count_46,run_count_01,run_count_103,run_count_12


def cut_state_save(actual_sp_46,actual_sp_01,actual_sp_103,actual_sp_12,start_cut_coil_46,start_cut_coil_01,start_cut_coil_103,start_cut_coil_12,max_cut_46,max_cut_01,max_cut_103,max_cut_12,fmb46_pn_state,fmb01_pn_state,ful103_pn_state,fmb12_pn_state,run_count_46,run_count_01,run_count_103,run_count_12):
	ruta_state = resource_path("images/cut_last_state.csv")

	with open(ruta_state, "w+") as file_object:

		file_object.write(f"{actual_sp_46},{actual_sp_01},{actual_sp_103},{actual_sp_12},{start_cut_coil_46},{start_cut_coil_01},{start_cut_coil_103},{start_cut_coil_12},{max_cut_46},{max_cut_01},{max_cut_103},{max_cut_12},{fmb46_pn_state},{fmb01_pn_state},{ful103_pn_state},{fmb12_pn_state},{run_count_46},{run_count_01},{run_count_103},{run_count_12}")


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
	elif pn_total_qty < 0:
		pn_total_qty = abs(pn_total_qty)
	return pn_total_qty

##--------------------the thread itself--------------#

class hilo1(threading.Thread):
	#thread init procedure
	# i think we pass optional variables to use them inside the thread
	def __init__(self):
		threading.Thread.__init__(self)
		self._stop_event = threading.Event()
	#the actual thread function
	def run(self):
		# in case of failure, these will recover current info
		fmb46_state,fmb01_state,ful103_state,fmb12_state = state_recover()
		actual_sp_46,actual_sp_01,actual_sp_103,actual_sp_12,start_cut_coil_46,start_cut_coil_01,start_cut_coil_103,start_cut_coil_12,max_cut_46,max_cut_01,max_cut_103,max_cut_12,fmb46_pn_state,fmb01_pn_state,ful103_pn_state,fmb12_pn_state,run_count_46,run_count_01,run_count_103,run_count_12 = cut_state_recover()

		coil_total_pcs_12  = avg_total_cut(fmb12_pn_state)
		coil_total_pcs_103 = avg_total_cut(ful103_pn_state)
		coil_total_pcs_01 = avg_total_cut(fmb01_pn_state)
		coil_total_pcs_46 = avg_total_cut(fmb46_pn_state)


		plc.open()
		plc1.open()

		#Handles section
		var_handle46_1 = plc.get_handle('.I_FMB46_Ringsensor')
		var_handle46_2 = plc.get_handle('.FMB46_Coil_Count_INT')
		var_handle46_3 = plc.get_handle('.TP_IW_FMB46_Setup_Part_Number')	
		var_handle46_4 = plc.get_handle('.Day_Spring_Count_FMB1_46')
		var_handle46_5 = plc.get_handle('.FMB46_Coil_Progress_Prozent')

		var_handle01_1 = plc.get_handle('.I_FMB1_Ringsensor')
		var_handle01_2 = plc.get_handle('.FMB1_Coil_Count_INT')
		var_handle01_3 = plc.get_handle('.TP_IW_FMB1_Setup_Part_Number')	
		var_handle01_4 = plc.get_handle('.Day_Spring_Count_FMB1_1')
		var_handle01_5 = plc.get_handle('.FMB1_Coil_Progress_Prozent')

		var_handle103_1 = plc1.get_handle('.I_FUL103_Ringsensor')
		var_handle103_2 = plc1.get_handle('.FUL103_Coil_Count_INT')
		var_handle103_3 = plc1.get_handle('.TP_IW_FMB22_Setup_Part_Number')	
		var_handle103_4 = plc1.get_handle('.Day_Spring_Count_FMB22')
		var_handle103_5 = plc1.get_handle('.FUL103_Coil_Progress_Prozent')
		
		var_handle12_1 = plc1.get_handle('.I_FMB12_Ringsensor')
		var_handle12_2 = plc1.get_handle('.FMB12_Coil_Count_INT')
		var_handle12_3 = plc1.get_handle('.TP_IW_FMB12_Setup_Part_Number')	
		var_handle12_4 = plc1.get_handle('.Day_Spring_Count_FMB12')
		var_handle12_5 = plc1.get_handle('.FMB12_Coil_Progress_Prozent')


		while True:
			try:
				#Coil Sensor
				coil_sensor_46 = plc.read_by_name("", plc_datatype=pyads.PLCTYPE_BOOL,handle=var_handle46_1)
				coil_sensor_01 = plc.read_by_name("", plc_datatype=pyads.PLCTYPE_BOOL,handle=var_handle01_1)
				coil_sensor_103 = plc1.read_by_name("", plc_datatype=pyads.PLCTYPE_BOOL,handle=var_handle103_1)
				coil_sensor_12 = plc1.read_by_name("", plc_datatype=pyads.PLCTYPE_BOOL,handle=var_handle12_1)
				#Part Number
				pn_46 = plc.read_by_name("", plc_datatype=pyads.PLCTYPE_STRING,handle=var_handle46_3)
				pn_01 = plc.read_by_name("", plc_datatype=pyads.PLCTYPE_STRING,handle=var_handle01_3)
				pn_12 = plc1.read_by_name("", plc_datatype=pyads.PLCTYPE_STRING,handle=var_handle12_3)
				pn_103 = plc1.read_by_name("", plc_datatype=pyads.PLCTYPE_STRING,handle=var_handle103_3)
				#Daily Counter to track coil performance
				cut_46 = plc.read_by_name("", plc_datatype=pyads.PLCTYPE_UINT,handle=var_handle46_4)
				cut_01 = plc.read_by_name("", plc_datatype=pyads.PLCTYPE_UINT,handle=var_handle01_4)
				cut_12 = plc1.read_by_name("", plc_datatype=pyads.PLCTYPE_UINT,handle=var_handle12_4)
				cut_103 = plc1.read_by_name("", plc_datatype=pyads.PLCTYPE_UINT,handle=var_handle103_4)

			except Exception as e:
				print(e)
				try:
					plc.release_handle(var_handle46_1)
					plc.release_handle(var_handle46_2)
					plc.release_handle(var_handle46_3)
					plc.release_handle(var_handle46_4)
					plc.release_handle(var_handle46_5)

					plc.release_handle(var_handle01_1)
					plc.release_handle(var_handle01_2)
					plc.release_handle(var_handle01_3)
					plc.release_handle(var_handle01_4)
					plc.release_handle(var_handle01_5)
				except:
					pass
				print(f"handles1 released")
				try:
					plc1.release_handle(var_handle12_1)
					plc1.release_handle(var_handle12_2)
					plc1.release_handle(var_handle12_3)
					plc1.release_handle(var_handle12_4)
					plc1.release_handle(var_handle12_5)

					plc1.release_handle(var_handle103_1)
					plc1.release_handle(var_handle103_2)
					plc1.release_handle(var_handle103_3)
					plc1.release_handle(var_handle103_4)
					plc1.release_handle(var_handle103_5)
				except:
					pass
				print("handles2 released")
				plc.close()
				plc1.close()
				break
			else:
				pass

			#-----------SECTION 2: Monitor machine status to log the information---------------------------
			#FUL103
			if ful103_state != coil_sensor_103:
				# if false means that coil is starting
				if ful103_state == False:
					#1 we write the report
					write_report('Start','FUL103', ful103_pn_state,cut_103)
					#we change the machine state
					ful103_state = coil_sensor_103
					#2 we write the machine status in case comm is lost
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
					#3 optional: we inform of happened stuff
					send_message(Jorge_Morales,quote(f"Inicio de rollo: FUL103"),token_Tel)
					print(f"Inicio de rollo: FUL103")
					# 5 we update the coil count 
					run_count_103 +=1
					# 6 We store the day cuts (Acc cuts for today)
					start_cut_coil_103 = cut_103
					actual_sp_103 = 0
					coil_total_pcs_103 = avg_total_cut(ful103_pn_state)
				#if true means that coil finished.
				elif ful103_state == True:
					#1 we write the report that the coil has finished. We use pn_state to report the saved value in case the actual value has been changed
					write_report('End','FUL103', ful103_pn_state,cut_103)
					#2. we change the value to False to receive the info from the sensor.
					ful103_state = coil_sensor_103
					#3.- we send the message that the coil has finished
					send_message(Jorge_Morales,quote(f"Fin de rollo: FUL103"),token_Tel)
					print(f"Fin de rollo: FUL103")
					#4.- We store the info
					pn_database_log(ful103_pn_state,actual_sp_103)
					#5 we check for part number change
					if ful103_pn_state != pn_103:
						# reset the coil amount
						run_count_103 = 0
						ful103_pn_state = pn_103
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
			#FMB12
			if fmb12_state != coil_sensor_12:
				# if false means that coil is starting
				if fmb12_state == False:
					write_report('Start','FMB12', fmb12_pn_state,cut_12)
					fmb12_state = coil_sensor_12
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
					send_message(Jorge_Morales,quote(f"Inicio de rollo: FMB12"),token_Tel)
					print(f"Inicio de rollo: FMB12")
					# 5 we update the coil count 
					run_count_12 +=1
					# 6 We store the day cuts (Acc cuts for today)
					start_cut_coil_12 = cut_12
					actual_sp_12 = 0
					coil_total_pcs_12 = avg_total_cut(fmb12_pn_state)
				elif fmb12_state == True:
					#1 we write the report that the coil has finished. We use pn_state to report the saved value in case the actual value has been changed
					write_report('End','FMB12', fmb12_pn_state,cut_12)
					#2. we change the value to False to receive the info from the sensor.
					fmb12_state = coil_sensor_12
					#3.- we send the message that the coil has finished
					send_message(Jorge_Morales,quote(f"Fin de rollo: FMB12"),token_Tel)
					print(f"Fin de rollo: FMB12")
					#4.- We store the info
					pn_database_log(fmb12_pn_state,actual_sp_12)
					#5 we check for part number change
					if fmb12_pn_state  != pn_12:
						# reset the counter
						run_count_12 = 0
						fmb12_pn_state = pn_12					
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
			#FMB01
			if fmb01_state != coil_sensor_01:
				# if false means that coil is starting
				if fmb01_state == False:
					write_report('Start','FMB1', fmb01_pn_state,cut_01)
					fmb01_state = coil_sensor_01
					send_message(Jorge_Morales,quote(f"Inicio de rollo: FMB1"),token_Tel)
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
					print(f"Inicio de rollo: FMB1")
					# 5 we update the coil count 
					run_count_01 +=1
					# 6 We store the day cuts (Acc cuts for today)
					start_cut_coil_01 = cut_01
					actual_sp_01 = 0
					coil_total_pcs_01 = avg_total_cut(fmb01_pn_state)
				elif fmb01_state == True:
					#1 we write the report that the coil has finished. We use pn_state to report the saved value in case the actual value has been changed
					write_report('End','FMB1', fmb01_pn_state,cut_01)
					#2. we change the value to False to receive the info from the sensor.
					fmb01_state = coil_sensor_01
					#3.- we send the message that the coil has finished
					send_message(Jorge_Morales,quote(f"Fin de rollo: FMB1"),token_Tel)
					print(f"Fin de rollo: FMB1")
					#4.- We store the info
					pn_database_log(fmb01_pn_state,actual_sp_01)
					#5 we check for part number change
					if fmb01_pn_state  != pn_01:
						# reset the counter
						run_count_01 = 0
						fmb01_pn_state = pn_01			
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)		
			#FMB46
			if fmb46_state != coil_sensor_46:
				# if false means that coil is starting
				if fmb46_state == False:
					write_report('Start','FMB46', pn_46,cut_46)
					fmb46_state = coil_sensor_46
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)
					send_message(Jorge_Morales,quote(f"Inicio de rollo: FMB46"),token_Tel)
					print(f"Inicio de rollo: FMB46")
					# 5 we update the coil count 
					run_count_46 +=1
					# 6 We store the day cuts (Acc cuts for today)
					start_cut_coil_46 = cut_46
					actual_sp_46 = 0
					coil_total_pcs_46 = avg_total_cut(pn_46)
				elif fmb46_state == True:
					#1 we write the report that the coil has finished. We use pn_state to report the saved value in case the actual value has been changed
					write_report('End','FMB46', fmb46_pn_state,cut_46)
					#2. we change the value to False to receive the info from the sensor.
					fmb46_state = coil_sensor_46
					#3.- we send the message that the coil has finished
					send_message(Jorge_Morales,quote(f"Fin de rollo: FMB46"),token_Tel)
					print(f"Fin de rollo: FMB46")
					#4.- We store the info
					pn_database_log(fmb46_pn_state,actual_sp_46)
					#5 we check for part number change
					if fmb46_pn_state  != pn_46:
						# reset the counter
						run_count_46 = 0
						fmb46_pn_state = pn_46	
					state_save(fmb46_state,fmb01_state,ful103_state,fmb12_state)	
			#-----------SECTION 3: Pieces per coil monitoring---------------------------

			#FUL-103 pieces count
			if cut_103 >= start_cut_coil_103:
				actual_sp_103 = cut_103 - start_cut_coil_103
				max_cut_103 = cut_103
			else:
				actual_sp_103 = max_cut_103 + cut_103 - start_cut_coil_103

			#FMB12 pieces count
			if cut_12 >= start_cut_coil_12:
				actual_sp_12 = cut_12 - start_cut_coil_12
				max_cut_12 = cut_12
			else:
				actual_sp_12 = max_cut_12 + cut_12 - start_cut_coil_12

			#FMB46 pieces count
			if cut_46 >= start_cut_coil_46:
				actual_sp_46 = cut_46 - start_cut_coil_46
				max_cut_46 = cut_46
			else:
				actual_sp_46 = max_cut_46 + cut_46 - start_cut_coil_46
			#FMB01 pieces count
			if cut_01 >= start_cut_coil_01:
				actual_sp_01 = cut_01 - start_cut_coil_01
				max_cut_01 = cut_01
			else:
				actual_sp_01 = max_cut_01 + cut_01 - start_cut_coil_01

			
			cut_state_save(actual_sp_46,actual_sp_01,actual_sp_103,actual_sp_12,start_cut_coil_46,start_cut_coil_01,start_cut_coil_103,start_cut_coil_12,max_cut_46,max_cut_01,max_cut_103,max_cut_12,fmb46_pn_state,fmb01_pn_state,ful103_pn_state,fmb12_pn_state,run_count_46,run_count_01,run_count_103,run_count_12)



			#-----------SECTION 4: coil progress write on PLC------------------------
			
			# Write coil count on PLC
			plc.write_by_name('',run_count_46, plc_datatype=pyads.PLCTYPE_INT,handle=var_handle46_2)
			plc.write_by_name('',run_count_01, plc_datatype=pyads.PLCTYPE_INT,handle=var_handle01_2)
			plc1.write_by_name('',run_count_103, plc_datatype=pyads.PLCTYPE_INT,handle=var_handle103_2)
			plc1.write_by_name('',run_count_12, plc_datatype=pyads.PLCTYPE_INT,handle=var_handle12_2)
			#Write progress
			plc.write_by_name('',(actual_sp_46/coil_total_pcs_46*100), plc_datatype=pyads.PLCTYPE_REAL,handle=var_handle46_5)
			plc.write_by_name('',(actual_sp_01/coil_total_pcs_01*100), plc_datatype=pyads.PLCTYPE_REAL,handle=var_handle01_5)
			plc1.write_by_name('',(actual_sp_103/coil_total_pcs_103*100), plc_datatype=pyads.PLCTYPE_REAL,handle=var_handle103_5)
			plc1.write_by_name('',(actual_sp_12/coil_total_pcs_12*100), plc_datatype=pyads.PLCTYPE_REAL,handle=var_handle12_5)			

			


			#-----------SECTION 5: print/log information---------------------------
			
			print(f"FMB-46 snsr/sta: {coil_sensor_46}/{fmb46_state}, coils: {run_count_46}, actual pcs: {actual_sp_46}, progress {(actual_sp_46/coil_total_pcs_46):.0%}")
			print(f"FMB-01 snsr/sta: {coil_sensor_01}/{fmb01_state}, coils: {run_count_01}, actual pcs: {actual_sp_01}, progress {(actual_sp_01/coil_total_pcs_01):.0%}")
			print(f"FUL-103 snsr/sta: {coil_sensor_103}/{ful103_state}, coils: {run_count_103}, actual pcs: {actual_sp_103}, progress {(actual_sp_103/coil_total_pcs_103):.0%}")
			print(f"FMB-12 snsr/sta: {coil_sensor_12}/{fmb12_state}, coils: {run_count_12}, actual pcs: {actual_sp_12}, progress {(actual_sp_12/coil_total_pcs_12):.0%}")
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
			print(f"{dt_string}")
			#write_log(coil_sensor_46,coil_sensor_01,Automatic_01,Automatic_46,pn_46,pn_01,coil_sensor_103,coil_sensor_12,Automatic_103,Automatic_12,pn_12,pn_103)
			time.sleep(5)

			if self.stopped == True:
				thread1.stop()
				try:
					plc.release_handle(var_handle46_1)
					plc.release_handle(var_handle46_2)
					plc.release_handle(var_handle46_3)
					plc.release_handle(var_handle46_4)
					plc.release_handle(var_handle46_5)

					plc.release_handle(var_handle01_1)
					plc.release_handle(var_handle01_2)
					plc.release_handle(var_handle01_3)
					plc.release_handle(var_handle01_4)
					plc.release_handle(var_handle01_5)
				except:
					pass
				print(f"handles1 released")
				try:
					plc1.release_handle(var_handle12_1)
					plc1.release_handle(var_handle12_2)
					plc1.release_handle(var_handle12_3)
					plc1.release_handle(var_handle12_4)
					plc1.release_handle(var_handle12_5)

					plc1.release_handle(var_handle103_1)
					plc1.release_handle(var_handle103_2)
					plc1.release_handle(var_handle103_3)
					plc1.release_handle(var_handle103_4)
					plc1.release_handle(var_handle103_5)
				except:
					pass
				print("handles2 released")
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

def pn_database_log(part_number,cuts):
	pd_ruta = resource_path("images/pn_db.csv")
	pd_file_exists = os.path.exists(pd_ruta)
	#check if pandas DataFrame exists to load the stuff or to create with dummy data.
	if cuts < 400:
		return
	if pd_file_exists:
		pd_log = pd.read_csv(pd_ruta)
	else:
		pd_log = pd.DataFrame(pd_dict3)

	new_row = {'Part_Number' : [part_number], 'Springs' : [cuts]}
	new_row_pd = pd.DataFrame(new_row)
	pd_concat = pd.concat([pd_log,new_row_pd])
	pd_concat.to_csv(pd_ruta,index=False)


#Pandas DataFrame dictionaries
pd_dict = {'timestamp' : ['0'], 'FMB_46_Coil' : ['0'], 'FMB_01_Coil' : ['0'], 'Automatic_01' : ['0'], 'Automatic_46' : ['0'], 'Num_Parte_46' : ['0'], 'Num_Parte_01' : ['0'], 'FMB_12_Coil' : ['0'], 'FUL_103_Coil' : ['0'], 'Automatic_12' : ['0'], 'Automatic_103' : ['0'], 'Num_Parte_12' : ['0'], 'Num_Parte_103' : ['0']}
pd_dict2 = {'timestamp' : ['0'], 'Type' : ['0'], 'Machine' : ['0'], 'Part_Number' : ['0'], 'Pieces': ['0']}
pd_dict3 = {'Part_Number' : ['0'], 'Springs': ['0']}

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