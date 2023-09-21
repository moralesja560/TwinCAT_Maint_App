import pyads
import csv

# connect to the PLC
plc = pyads.Connection('10.65.96.73.1.1', 801)

# open the connection
plc.open()

# read the device name and the version
device_name, version = plc.read_device_info()
print(str(device_name) + ' ' + str(version))

print(f"Connected?: {plc.is_open}") #debugging statement, optional
print(f"Local Address? : {plc.get_local_address()}") #debugging statement, optional
symbols = plc.get_all_symbols()


with open('symbols.csv', 'w') as csvfile:
    fieldnames = ['Name', 'Value', 'Comment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for s in symbols:
        try:
            writer.writerow({'Name': s.name, 'Value': s.value, 'Comment': s.comment})

        except Exception as e:
            writer.writerow({'Name': s.name, 'Value': "ND", 'Comment': e})
plc.close()