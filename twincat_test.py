import pyads
import csv
import time

# connect to the PLC
plc = pyads.Connection('10.65.96.102.1.1', 801)

# open the connection
plc.open()

# read the device name and the version
device_name, version = plc.read_device_info()
print(str(device_name) + ' ' + str(version))

print(f"Connected?: {plc.is_open}") #debugging statement, optional
print(f"Local Address? : {plc.get_local_address()}") #debugging statement, optional
#symbols = plc.get_all_symbols()
"""
with open('names.csv', 'w') as csvfile:
    fieldnames = ['Name', 'Value', 'Comment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for s in symbols:
        try:
            writer.writerow({'Name': s.name, 'Value': s.value, 'Comment': s.comment})
            #print(s.name, ": ", s.read(), " // ", s.comment)

        except Exception as e:
            print(e)
            #print(plc.get_symbol(index_group=s.index_group, index_offset=1,plc_datatype="BOOL").name)
            #print(s.name, ": Failed")
            pass
plc.close()
"""



"""
#read a boolean
bReadCommand = plc.read_by_name('B_ASI_1.I_Betriebsart_Auto', pyads.PLCTYPE_BOOL)
print(bReadCommand)

#write ack
plc.write_by_name('Ethernet.bACKFromPython', bReadCommand)
"""
#read int number
var_handle = plc.get_handle('.I_FMB46_Ringsensor')

for i in range(0,5):
    int_number = plc.read_by_name('', pyads.PLCTYPE_BOOL, handle=var_handle)
    print(int_number)
    time.sleep(3)

plc.release_handle(var_handle)
"""
#read real number
real_number = plc.read_by_name('Ethernet.fMyRealNumber', pyads.PLCTYPE_REAL)
print(real_number)
"""
#read string
#plc.write_by_name('PB_Stueckzahl.ADS_Label_Incoming_Ping',101,pyads.PLCTYPE_INT)
#message_from_twincat = plc.read_by_name('PB_Stueckzahl.ADS_Label_Outgoing_Ping', pyads.PLCTYPE_INT)

#print(message_from_twincat)
"""
#write string
if len(message_from_twincat) > 1:
    message_to_twincat = 'El super mono'
    plc.write_by_name('Ethernet.sMessageFromPython', message_to_twincat, plc_datatype=pyads.PLCTYPE_STRING)

	# close connection
"""
plc.close()
