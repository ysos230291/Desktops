import subprocess


x = subprocess.run("wmic bios get serialnumber", shell = True, capture_output = True, text = True)
lineas = x.stdout.splitlines()
serial = lineas[2].lower()
subprocess.run(f"echo {serial} > serialobtain.txt",shell = True)
print(serial)
