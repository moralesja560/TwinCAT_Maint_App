import pyads
import time

# connect to the PLC
plc = pyads.Connection('10.65.96.38.1.1', 801)

# open the connection
plc.open()

# read the device name and the version
device_name, version = plc.read_device_info()
print(str(device_name) + ' ' + str(version))

print(f"Connected?: {plc.is_open}") #debugging statement, optional
print(f"Local Address? : {plc.get_local_address()}") #debugging statement, optional


var_handle46_2 = plc.get_handle('.FMB12_Coil_Count_INT')
var_handle46_5 = plc.get_handle('.FMB12_Coil_Progress_Prozent')
var_handle01_2 = plc.get_handle('.FUL103_Coil_Count_INT')
var_handle01_5 = plc.get_handle('.FUL103_Coil_Progress_Prozent')

run_count_46 = 1000
run_count_01 = 22
actual_sp_46 = 500
coil_total_pcs_46 = 2500
actual_sp_01 = 250
coil_total_pcs_01 = 2250

plc.write_by_name('',run_count_46, plc_datatype=pyads.PLCTYPE_INT,handle=var_handle46_2)
plc.write_by_name('',run_count_01, plc_datatype=pyads.PLCTYPE_INT,handle=var_handle01_2)
plc.write_by_name('',(actual_sp_46/coil_total_pcs_46*100), plc_datatype=pyads.PLCTYPE_REAL,handle=var_handle46_5)
plc.write_by_name('',(actual_sp_01/coil_total_pcs_01*100), plc_datatype=pyads.PLCTYPE_REAL,handle=var_handle01_5)


plc.release_handle(var_handle46_2)
plc.release_handle(var_handle46_5)
plc.release_handle(var_handle01_2)
plc.release_handle(var_handle01_5)

plc.close()

plc = pyads.Connection('10.65.96.38.1.1', 801)

# open the connection
plc.open()


var_list = ['.FMB12_Coil_Count_INT', '.FMB12_Coil_Progress_Prozent', '.FUL103_Coil_Count_INT']
dicc = plc.read_list_by_name(var_list)

print(dicc)
x = dicc[".FMB12_Coil_Count_INT"]

print(x)

plc.close()



