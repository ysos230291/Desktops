import subprocess

perfiles = subprocess.run("netsh wlan show profile",shell = True,capture_output=True, text = True)
lineas = perfiles.stdout.splitlines()
linea_escogida = []
linea_perfil = []
p = []
passwords = []

# vamos a hallar los perfiles

for index in range(len(lineas)):
    if "Perfil de todos los usuarios" in lineas[index]:
        linea_escogida.append(lineas[index])
        
for index in range(len(linea_escogida)):
    i = linea_escogida[index].find(":")
    linea_perfil.append(linea_escogida[index][i + 2:len(linea_escogida[index])])


# vamos a hallar las claves de esos perfiles

for index in range(len(linea_perfil)):
    p.append(subprocess.run(f'netsh wlan show profile name="{linea_perfil[index]}" key=clear',shell=True,capture_output=True,text = True))

lineas.clear()
linea_escogida.clear()

for index in range(len(p)):
    lineas.append(p[index].stdout.splitlines())


for i in range(len(lineas)):
    for j in range(len(lineas[i])):
        if "Contenido de la clave" in lineas[i][j]:
            linea_escogida.append(lineas[i][j])

for index in range(len(linea_escogida)):
    i = linea_escogida[index].find(":")
    passwords.append(linea_escogida[index][i + 1:len(linea_escogida[index])]) 

string = []

for index in range(len(linea_perfil)):
    string.append(linea_perfil[index] + " ---- " + passwords[index])


subprocess.run("echo. > wifipass.txt",shell = True)

for index in range(len(string)):
   s = string[index]
   subprocess.run("echo "+s+" >> wifipass.txt",shell = True)

input("enter para salir")



 






