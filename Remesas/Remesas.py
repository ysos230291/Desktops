from customtkinter import *
from customtkinter import CTkImage
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import *
import mysql.connector
import subprocess
from PIL import Image 
from tkcalendar import *
#import pandas as pd 
#import copy
#import shutil
#import sqlite3
#import os
#import json
#from tkinter import filedialog


conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""    
    )
cursor = conn.cursor()
sql = ""

fecha_actual = datetime.now().date()

def estilos_tablas():
    # ******************************* creando los estilos para  las tablas del software
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
            background="#1e1e1e",
            foreground="#dcdcdc",
            fieldbackground="#1e1e1e",
            bordercolor="#3a3a3a",
            lightcolor="#1e1e1e",
            darkcolor="#1e1e1e",
            rowheight=28,
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
        )

        style.configure("Treeview.Heading",
            background="#2a2a2a",
            foreground="#a0a0a0",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padding=(5, 5),
        )

        style.map("Treeview",
            background=[("selected", "#2d4f6e"), ("active", "#2a2a2a")],
            foreground=[("selected", "#ffffff"), ("active", "#ffffff")],
        )

        style.map("Treeview.Heading",
            background=[("active", "#3a3a3a"), ("pressed", "#444444")],
            foreground=[("active", "#ffffff")],
        )

        style.configure("Treeview.Cell",
            padding=(5, 2),
        )

        style.configure("Vertical.TScrollbar",
            background="#2a2a2a",
            troughcolor="#1e1e1e",
            arrowcolor="#888888",
            bordercolor="#1e1e1e",
            lightcolor="#2a2a2a",
            darkcolor="#2a2a2a",
        )

        style.map("Vertical.TScrollbar",
            background=[("active", "#3a3a3a"), ("pressed", "#444444")],
            arrowcolor=[("active", "#ffffff")],
        )

        style.configure("Horizontal.TScrollbar",
            background="#2a2a2a",
            troughcolor="#1e1e1e",
            arrowcolor="#888888",
            bordercolor="#1e1e1e",
            lightcolor="#2a2a2a",
            darkcolor="#2a2a2a",
        )

        style.map("Horizontal.TScrollbar",
            background=[("active", "#3a3a3a"), ("pressed", "#444444")],
            arrowcolor=[("active", "#ffffff")],
        )  


# ***************************************************************************************
# **************** Creando Usuario, Base de Datos y Tablas de Admin necesarias **********
# ***************************************************************************************



ususario_remesas_is_created = False
base_data_is_created = False
table_usuarios_is_created = False
usuario_remesas_is_created = False
table_licencias_is_created = False

# ********************** creando usuario admin ******************************

try:
    sql = """CREATE USER 'remesas'@'localhost' IDENTIFIED BY '123456';"""
    cursor.execute(sql)
    conn.commit()
except:
    ususario_remesas_is_created = True

sql = """GRANT ALL PRIVILEGES ON *.* TO 'remesas'@'localhost' REQUIRE NONE WITH GRANT OPTION MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0; """
cursor.execute(sql)
conn.commit()

conn.close()

conn = mysql.connector.connect(
    host = "localhost",
    user = "remesas",
    password = "123456",
    )
cursor = conn.cursor()

# ******* creando la base de datos remesas ***********
try:
    sql = """CREATE DATABASE remesas CHARACTER SET = utf8mb4 COLLATE utf8mb4_spanish_ci;"""
    cursor.execute(sql)
    conn.commit()
    base_data_is_created = True
except:
    base_data_is_created = True

conn = mysql.connector.connect(
    host = "localhost",
    user = "remesas",
    password = "123456",
    database = "remesas"
    )
cursor = conn.cursor()


# *********** creando tabla usuarios **********

try:
    sql = """CREATE TABLE  usuarios (Usuario VARCHAR(50), Password VARCHAR(50))"""
    cursor.execute(sql)
    conn.commit()
    table_usuarios_is_created = True
except:
    table_usuarios_is_created = True

conn = mysql.connector.connect(
    host = "localhost",
    user = "remesas",
    password = "123456",
    database = "remesas"
    )
cursor = conn.cursor()

usuario_inicial = []
sql = """ SELECT Usuario FROM usuarios """
cursor.execute(sql)

for usser in cursor:
    usuario_inicial.append(usser)

for index in range(len(usuario_inicial)):
    if usuario_inicial[index][0] == "remesas":
        usuario_remesas_is_created = True

if usuario_remesas_is_created == False:
    try:
        sql = """INSERT INTO usuarios (Usuario,Password) VALUES ("remesas","123456")"""
        cursor.execute(sql)
        conn.commit()
        
        usuario_remesas_is_created = True
    except:
        usuario_remesas_is_created = True


# ************** creando tabla licencias ***************

conn = mysql.connector.connect(
    host = "localhost",
    user = "remesas",
    password = "123456",
    database = "remesas"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `remesas`.`licencias` (`codigo_lic` VARCHAR(50) NOT NULL , `pass_economia` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    table_licencias_is_created = True  

# ******************** Creando Tabla Cuentas *******************

conn = mysql.connector.connect(
    host = "localhost",
    user = "remesas",
    password = "123456",
    database = "remesas"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `remesas`.`cuentas` (`Id` INT(11) NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `Fondo` FLOAT NOT NULL) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# ******************** Creando Tabla Remeseros *******************

conn = mysql.connector.connect(
    host = "localhost",
    user = "remesas",
    password = "123456",
    database = "remesas"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `remesas`.`remeseros` (`Id` INT(11) NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `Fondo` FLOAT NOT NULL) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ******************** Creando Tabla Recargas *******************

conn = mysql.connector.connect(
    host = "localhost",
    user = "remesas",
    password = "123456",
    database = "remesas"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `remesas`.`recargas` (`Id` INT(11) NOT NULL, `Fecha` DATE NOT NULL, `Tipo` CHAR NOT NULL, `Id_Cliente` INT(11) NOT NULL, `Nombre` VARCHAR(50) NOT NULL, `Fondo` FLOAT NOT NULL) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ******************** Creando Tabla Envios *******************

conn = mysql.connector.connect(
    host = "localhost",
    user = "remesas",
    password = "123456",
    database = "remesas"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `remesas`.`envios` (`Id` INT(11) NOT NULL, `Fecha` DATE NOT NULL, `Nombre` VARCHAR(50) NOT NULL, `Monto` FLOAT NOT NULL, `Ganacia` FLOAT NOT NULL, `Cuenta` VARCHAR(50) NOT NULL, `Remesero` VARCHAR(50) NOT NULL) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    temp = True



#*************************************************************************************
#************************trabajo con ventana Autenticacion ***************************
#*************************************************************************************

class Autenticacion(CTk):
    def __init__(self):
        super().__init__()
        self.title("Autenticacion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 400
        hventana = 200
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("400x200")
        self.resizable(False,False)            
        self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico')  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo1.jpg"), size = (400,200))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)        

        ################# textos y entradas ##################

        self.label_usuario = CTkLabel(self,text="Usuario:", font=("Times New Roman",16), fg_color = "black")
        self.label_usuario.place(x = 63 , y = 20)

        self.texto_usuario = CTkEntry(self)
        self.texto_usuario.place(x = 200 , y = 20)
        
        self.label_usuariolabel_pass = CTkLabel(self,text="Contraseña:", font=("Times New Roman",16), fg_color = "black")
        self.label_usuariolabel_pass.place(x = 40 , y = 70)       

        self.texto_pass = CTkEntry(self, show="*")
        self.texto_pass.place(x = 200 , y = 70)
        
        global autorizacion
        autorizacion = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "remesas",
            password = "123456",
            database = "remesas"
            )
        cursor = conn.cursor()
        sql = """SELECT Usuario, Password FROM usuarios"""
        cursor.execute(sql)
        for index in cursor:
            autorizacion.append(index)

        def codigo_btn_iniciar():
            # ******************** control de vencimiento *****************
            lic = ""

            conn = mysql.connector.connect(
            host = "localhost",
            user = "remesas",
            password = "123456",
            database = "remesas"
            )
            cursor = conn.cursor()


            sql = """SELECT codigo_lic FROM licencias """
            cursor.execute(sql)
            

            for index in cursor:
                lic = index[0]

            

            if lic == "":
                autenticacion.withdraw()
                nueva_licencia = NuevaLicencia()

            else:
                abecedario_normal = "qwertyuiopasdfghjklñzxcvbnm0123456789"
                abecedario_enc = "qwyu678iopamghj012ñ3sdfertklzxcvbn459"

                lista_abe_normal = list(abecedario_normal)
                lista_abe_enc = list(abecedario_enc)

                texto_encriptado = lic
                texto_normal = "" 

                lista_normal = []
                lista_enc = list(texto_encriptado)
            

                for i in range(len(lista_enc)):
                    for j in range(len(lista_abe_enc)):
                        if lista_enc[i] == lista_abe_enc[j]:
                            lista_normal.append(lista_abe_normal[j])

                
                for index in range(len(lista_normal)):
                    texto_normal += lista_normal[index]

                        
                # ahora ver que voy a hacer con la info clara

                try:
                    fecha = []
                            
                    fecha.append(int(texto_normal[16:20]))
                    fecha.append(int(texto_normal[23:25]))
                    fecha.append(int(texto_normal[28:30]))
                    global fecha_vencimiento
                    fecha_vencimiento = date(fecha[0],fecha[1],fecha[2])
                except:
                    error = messagebox.showinfo("Error","La lic no es correcta")

                autenticar_usuario = False
                autenticar_pass = False
                
                for index in range(len(autorizacion)):
                    if self.texto_usuario.get() == autorizacion[index][0]:
                        autenticar_usuario = True
                        if self.texto_pass.get() == autorizacion[index][1]:
                            autenticar_pass = True
                            autenticacion.withdraw()

                            if fecha_vencimiento < fecha_actual:
                                self.withdraw()
                                self.texto_usuario.delete(0,END)
                                self.texto_pass.delete(0,END)
                                nueva_licencia = NuevaLicencia()
                                


                            else:
                                self.withdraw()
                                self.texto_usuario.delete(0,END)
                                self.texto_pass.delete(0,END)
                                lobby = Lobby()                     
                                

                if autenticar_usuario == False:
                    error = messagebox.showwarning("Error","Usuario incorrecto")
                else:
                    if autenticar_pass == False:
                        error = messagebox.showwarning("Error","Contraseña incorrecta")

        self.btn_iniciar = CTkButton(self,text="Iniciar",command=codigo_btn_iniciar, width = 200)
        self.btn_iniciar.place(x = 100 , y = 160)

# ****************************************************************************************
# ********************************** nueva_licencia **************************************
# ****************************************************************************************

class NuevaLicencia(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Licencia")
        self.geometry("300x200")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 300
        hventana = 200
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo1.jpg"), size = (300,200))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################         

        self.label = CTkLabel(self, text = "Introduzca la licencia nueva", font=("Times New Roman",14))
        self.label.place(x = 60 , y = 20)        

        self.texto = CTkEntry(self, width = 200)
        self.texto.place(x = 60 , y = 80)   


        def codigo_btn_aceptar_nueva_licencia():

            #  desencriptando el codigo para validar licencia
            # el codigo debe tener un formato como el del siguiente ejemplo:
            # nuevalicenciaaño2025-mes01-dia01serial5cd028cgmk 
            # solo cambiamos los numeros de año , mes , dia y serial lo demas se mantiene igual
            

            #try:
            # *********** ver el numero de serie de la pc *****************

            x = subprocess.run("wmic bios get serialnumber", shell = True, capture_output = True, text = True)
            lineas = x.stdout.splitlines()
            serial_cmd = lineas[2].lower()
            serial_cmd = serial_cmd.rstrip(" ")

            # ************* desencriptado **********************************

            abecedario_normal = "qwertyuiopasdfghjklñzxcvbnm0123456789"
            abecedario_enc = "qwyu678iopamghj012ñ3sdfertklzxcvbn459"

            lista_abe_normal = list(abecedario_normal)
            lista_abe_enc = list(abecedario_enc)

            texto_encriptado = self.texto.get()
            texto_normal = "" 

            lista_normal = []
            lista_enc = list(texto_encriptado)
        

            for i in range(len(lista_enc)):
                for j in range(len(lista_abe_enc)):
                    if lista_enc[i] == lista_abe_enc[j]:
                        lista_normal.append(lista_abe_normal[j])

            
            for index in range(len(lista_normal)):
                texto_normal += lista_normal[index]

                
            
            # ahora ver que voy a hacer con la info clara

            fecha = []
            serial_txt = texto_normal[36:]
            
            fecha.append(int(texto_normal[16:20]))
            fecha.append(int(texto_normal[23:25]))
            fecha.append(int(texto_normal[28:30]))

            global fecha_vencimiento
            fecha_vencimiento = date(fecha[0],fecha[1],fecha[2])   
                                
            
            if serial_cmd == serial_txt:

                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()

                sql = """SELECT codigo_lic FROM `licencias` """
                cursor.execute(sql)
                conn.commit

                licencia_vacia = True

                for index in cursor:
                    if index == None:
                        licencia_vacia = True
                    else:
                        licencia_vacia = False

                

                if licencia_vacia:
                    sql = f""" INSERT INTO `licencias`(`codigo_lic`) VALUES ('{texto_encriptado}')"""
                    cursor.execute(sql)
                    conn.commit()

                else:
                                
                    sql = f""" UPDATE `licencias` SET `codigo_lic` = '{texto_encriptado}'"""
                    cursor.execute(sql)
                    conn.commit()


                if fecha_vencimiento < fecha_actual:
                    error = messagebox.showinfo("Error", "Licencia Inservible") 
                    
                else:
                    self.destroy()
                    lobby = Lobby()            
                    
                    
            else:
                error = messagebox.showinfo("Error", "Licencia Inservible. Estas en una pc incorrecta") 
                
            #except:
            #    error = messagebox.showinfo("Error", "Licencia Inservible")

        def cancelar_nueva_lic():            
            self.destroy()                                            

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=codigo_btn_aceptar_nueva_licencia, width = 100 , height = 30)
        self.btn_aceptar.place(x = 30 , y = 160 )

        self.btn_aceptar = CTkButton(self,text="Cancelar",command=cancelar_nueva_lic, width = 100 , height = 30)
        self.btn_aceptar.place(x = 170 , y = 160 )




# *******************************************************************************************
# ********************************* Trabajo con Lobby ***************************************
# *******************************************************************************************
class Lobby(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.geometry("1300x700")        
        self.title("Remesas")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))
        self.resizable(False,False)   

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo3.jpg"), size = (1300,700))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################          
        
        firma = "Vence (" + str(fecha_vencimiento) + ")"
        self.label_remesas = CTkLabel(self, text = firma, font=("Times New Roman",16))
        self.label_remesas.place(x = 1150, y = 650)

        self.menu = Menu(self)
        self.config(menu=self.menu, width="200", height="100")  

        def envios_lobby():
            env = Envios()    

        def control_envios():
            ce = ControlEnvios()

        def control_recargas():
            cr = ControlRecargas()

        def nueva_cuenta_lobby():
            nc = NuevaCuenta()     

        def ver_cuentas_lobby():
            vc = VerCuenta() 

        def nuevo_remesero_lobby():
            nr = NuevoRemesero() 

        def ver_remeseros_lobby():
            vr = VerRemesero() 

        def consulta_totales_lobby():
            ct = ConsultasTotales() 

        def consulta_real_lobby():
            ct = ConsultaReal() 

        def salva_lobby():
            # 1. Carpeta destino
            carpeta_respaldos = r"D:/Remesas/respaldos"
            os.makedirs(carpeta_respaldos, exist_ok=True)

            # 2. Nombre del archivo = fecha del día
            archivo = os.path.join(carpeta_respaldos, f"{fecha_actual}.sql")

            # 3. Ruta de mysqldump en XAMPP
            ruta_mysqldump = r"C:\xampp\mysql\bin\mysqldump.exe"

            try:
                # 4. Ejecutar el volcado
                comando = [
                    ruta_mysqldump,
                    "-u", "remesas",
                    "-p123456",
                    "--databases", "remesas",
                    "--routines",
                    "--events",
                    "--triggers",
                    "--add-drop-database",
                    f"--result-file={archivo}"
                ]

                resultado = subprocess.run(
                    comando,
                    capture_output=True,
                    text=True,
                    shell=False
                )

                # 5. Verificar resultado
                if resultado.returncode == 0 and os.path.exists(archivo):
                    messagebox.showinfo(
                        "Respaldo exitoso",
                        f"La base de datos se guardó correctamente en:\n{archivo}"
                    )
                else:
                    messagebox.showerror(
                        "Error al respaldar",
                        f"No se pudo crear la salva.\n\nDetalle:\n{resultado.stderr}"
                    )

            except FileNotFoundError:
                messagebox.showerror("Error","No se pudo exportar la salva")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")

        def agregar_usuario():
            usuario_agregar = UsuarioAgregar()
            
        def eliminar_usuario():                        
            eliminar_usuario = EliminarUsuario() 
         
        def agregar_nueva_licencia():                         
            nueva_licencia = NuevaLicencia()  

        def cerrar_cesion():
            self.destroy()
            autenticacion.deiconify() 
            
        def cerrar_programa(): 
            self.quit()                  
            self.destroy()
            autenticacion.destroy()
            quit()      

         # para que se cierre todo el programa si cerramos esta ventana 
        self.protocol("WM_DELETE_WINDOW", cerrar_programa)   

        cuentas_menu = Menu(self.menu, tearoff = 0)   
        cuentas_menu.add_command(label="Nueva", command = nueva_cuenta_lobby)                                     
        cuentas_menu.add_command(label="Ver", command = ver_cuentas_lobby)    

        remeseros_menu = Menu(self.menu, tearoff = 0)   
        remeseros_menu.add_command(label="Nuevo", command = nuevo_remesero_lobby)                                     
        remeseros_menu.add_command(label="Ver", command = ver_remeseros_lobby)  

        consultas_menu = Menu(self.menu, tearoff = 0)   
        consultas_menu.add_command(label="Totales", command = consulta_totales_lobby)  
        consultas_menu.add_command(label="Real", command = consulta_real_lobby)  

        control_menu = Menu(self.menu, tearoff = 0)   
        control_menu.add_command(label="Control Envios", command = control_envios)                        
        control_menu.add_command(label="Control Recargas", command = control_recargas)                        

        usuario_menu = Menu(self.menu, tearoff = 0)
        usuario_menu.add_command(label="Agregar", command = agregar_usuario)
        usuario_menu.add_command(label="Eliminar", command = eliminar_usuario)

        licencia_menu = Menu(self.menu, tearoff = 0)
        licencia_menu.add_command(label="Nueva", command = agregar_nueva_licencia)

        salir_menu = Menu(self.menu, tearoff = 0)
        salir_menu.add_command(label="Cerrar Cesion", command = cerrar_cesion)
        salir_menu.add_command(label="Cerrar Programa", command = cerrar_programa)
        
        self.menu.add_cascade (label="Envios", command = envios_lobby) 
        self.menu.add_cascade (label="Cuentas", menu = cuentas_menu)
        self.menu.add_cascade (label="Remeseros", menu = remeseros_menu)
        self.menu.add_cascade (label="Controles", menu = control_menu)                       
        self.menu.add_cascade (label="Consultas", menu = consultas_menu)                       
        self.menu.add_cascade (label="Salva", command = salva_lobby)               
        self.menu.add_cascade(label="Usuarios", menu = usuario_menu)
        self.menu.add_cascade(label = "Licencia", menu = licencia_menu)
        self.menu.add_cascade(label="Salir", menu = salir_menu)




# ******************************************************************************************
# ********************************* usuarios_agregar **************************************
# ******************************************************************************************

class UsuarioAgregar(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agregar Usuario") 
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 400
        hventana = 300
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("400x300")
        self.resizable(False,False)        
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))    

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo5.jpg"), size = (400,300))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################       

        # *********************** Label ****************************************

        self.label_nombre = CTkLabel(self,text = "Usuario:", font=("Times New Roman",14))
        self.label_nombre.place(x = 50 , y = 50)        

        self.label_pass = CTkLabel(self,text = "Contraseña:", font=("Times New Roman",14))
        self.label_pass.place(x = 50 , y = 90)
        
        self.label_confirmar = CTkLabel(self,text = "Confirmar:", font=("Times New Roman",14))
        self.label_confirmar.place(x = 50 , y = 130)
        
        # *********************** Entry ***************************************

        self.texto_nombre = CTkEntry(self)
        self.texto_nombre.place(x = 200 , y = 55)

        self.texto_pass = CTkEntry(self, show="*")
        self.texto_pass.place(x = 200 , y = 95)
        
        self.texto_confirmar = CTkEntry(self, show="*")
        self.texto_confirmar.place(x = 200 , y = 135)

        def codigo_btn_aceptar_usuarios_agregar():
            try:
                if self.texto_pass.get() == self.texto_confirmar.get():
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()

                    sql = """ INSERT INTO usuarios (Usuario, Password) VALUES (%s, %s) """
                    valores = (self.texto_nombre.get(),self.texto_pass.get())
                    cursor.execute(sql, valores)
                    conn.commit()
                    
                    autorizacion.append((self.texto_nombre.get(),self.texto_pass.get()))
                    self.destroy()
                    
                else:
                    error = messagebox.showwarning("Error","Confirmacion incorrecta")
                    if error == True:
                        self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo agregar el ususario")

            
            
        def codigo_btn_cancelar_usuarios_agregar():
            self.destroy()
            
        self.btn_aceptar = CTkButton(self,text="Aceptar",command=codigo_btn_aceptar_usuarios_agregar, width = 150 , height = 30)
        self.btn_aceptar.place(x = 30 , y = 200)        

        self.btn_cancelar = CTkButton(self,text="Cancelar",command=codigo_btn_cancelar_usuarios_agregar, width = 150 , height = 30)
        self.btn_cancelar.place(x = 220 , y = 200)


# ******************************************************************************************
# ******************************** usuarios_eliminar ***************************************
# ******************************************************************************************

class EliminarUsuario(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Eliminar")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 400
        hventana = 300
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("400x300")
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo5.jpg"), size = (400,300))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################            
        
        items_usuarios = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "remesas",
            password = "123456",
            database = "remesas"
            )
        cursor = conn.cursor()

        sql = """SELECT `Usuario` FROM `usuarios`;"""
        cursor.execute(sql)
        for index in cursor:
            items_usuarios.append(index[0])


        texto_nombre_usuario_eliminar = CTkComboBox(self, values=items_usuarios)
        texto_nombre_usuario_eliminar.set("Usuario...")
        texto_nombre_usuario_eliminar.place(x = 150 , y = 100)     


        def codigo_btn_eliminar_usuarios_eliminar():
            try:
                if texto_nombre_usuario_eliminar.get() == "remesas":
                    error = messagebox.showinfo("Error", "Ese usuario no puede eliminarse")
                else:
                    for i in autorizacion:
                        if texto_nombre_usuario_eliminar.get() == i[0]:
                                    
                            cuidado = messagebox.askokcancel("Delete","Se borrara el Usuario")
                            
                            if cuidado:
                                usuario_existe = False
                                indice_a_elminar = 0
                                
                                for index in range(len(autorizacion)):
                                    if texto_nombre_usuario_eliminar.get() == autorizacion[index][0]:
                                        indice_a_elminar = index
                                        usuario_existe = True

                                if usuario_existe == True:
                                    autorizacion.pop(indice_a_elminar)
                                    
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "remesas",
                                    password = "123456",
                                    database = "remesas"
                                    )
                                cursor = conn.cursor()
                                
                                usuario = texto_nombre_usuario_eliminar.get()   

                                sql = f"""DELETE FROM `usuarios` WHERE Usuario="{usuario}" """
                                cursor.execute(sql)
                                conn.commit()

                                self.destroy()


            except:
                error = messagebox.showinfo("Error","No se pudo eliminar el usuario")

        def codigo_btn_cancelar_usuarios_eliminar():
            self.destroy()
            
        self.btn_eliminar = CTkButton(self,text="Eliminar",command=codigo_btn_eliminar_usuarios_eliminar, width = 150 , height = 30)
        self.btn_eliminar.place(x = 50 , y = 200)
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=codigo_btn_cancelar_usuarios_eliminar, width = 150 , height = 30)
        self.btn_cancelar.place(x = 220 , y = 200)  


# **********************************************************************************
# *******************************  Nuevo Remesero **********************************
# **********************************************************************************

class NuevoRemesero(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Nuevo Remesero") 
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 300
        hventana = 300
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico')) 

        self.texto_remesero = CTkEntry(self, placeholder_text="Nombre ...",width=300)
        self.texto_remesero.pack(pady = 5)

        def insertar_remesero():
            conf = messagebox.askokcancel("Confirmar","Se va a Insertar este remesero")
            if conf:
                #try:
                # encontrar el id del remesero
                id_remesero = 1
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()

                sql = """SELECT MAX(Id) FROM `remeseros`;"""
                cursor.execute(sql)
                for index in cursor:
                    if index[0] == None:
                        pass
                    else:
                        id_remesero = index[0] + 1 

                # agregar le info a la bd 
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()
                sql = f""" INSERT INTO `remeseros`(`Id`, `Nombre`, `Fondo`) VALUES ('{id_remesero}','{self.texto_remesero.get()}','0') """
                cursor.execute(sql)
                conn.commit()

                self.destroy()
                #except:
                #    messagebox.showerror("Error","Hubo algun error al entrar al remesero")

        self.btn = CTkButton(self, text="Insertar", command=insertar_remesero)
        self.btn.pack(pady = 10) 


# **********************************************************************************
# ******************************** ver remesero ************************************
# **********************************************************************************

class VerRemesero(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Ver Remesero")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 500
        hventana = 500
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("500x500") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo4.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas()    

        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Fondo"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Nombre", width = 300, anchor="center")
        self.tabla.column("Fondo", width = 100, anchor="center")        

        self.tabla.place(x = 100, y = 50)        
        self.tabla.config(height = 15)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Fondo", text = "Fondo")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla():
            try:
                self.tabla.delete(*self.tabla.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()
    
                sql = f""" SELECT * FROM `remeseros` """
                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],)) 
            except:
                messagebox.showerror("Error","Hubo problemas al actualizar la pagina")

        llenar_tabla()

        # vamos a tener un click derecho para modificar, eliminar y recargar
        def eliminar():
            string = f"Se va a eliminar a {nombre_remesero} de la Base de Datos"
            conf = messagebox.askokcancel("Confirmar",string)
            if conf:
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" DELETE FROM `remeseros` WHERE `Id` = {id_remesero} """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()
                except:
                    messagebox.showerror("Error","No se pudo eliminar el Remesero de la Base de Datos")

        def recargar():
            temp = CTkToplevel()
            temp.title("Reabastecer") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 200
            hventana = 200
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico')) 

            text = f"Vamos a recargar a {nombre_remesero}"

            temp.label = CTkLabel(temp,text=text)
            temp.label.pack(pady=5)

            temp.texto_cantidad = CTkEntry(temp, placeholder_text="Monto ...")
            temp.texto_cantidad.pack(pady=5)

            def recargar():
                string = f"Vamos a recargar al remesero {nombre_remesero}"
                conf = messagebox.askokcancel("Confirmar",string)
                if conf:
                    try:
                        # registremos la recarga 
                        id_recarga = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "remesas",
                            password = "123456",
                            database = "remesas"
                            )
                        cursor = conn.cursor()
    
                        sql = """SELECT MAX(Id) FROM `recargas`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass
                            else:
                                id_recarga = index[0] + 1 

                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "remesas",
                            password = "123456",
                            database = "remesas"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `recargas`(`Id`, `Fecha`, `Tipo`, `Id_Cliente`, `Nombre`, `Fondo`) VALUES ('{id_recarga}','{fecha_actual}','R','{id_remesero}','{nombre_remesero}','{temp.texto_cantidad.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # aumentemos el fondo del remesero
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "remesas",
                            password = "123456",
                            database = "remesas"
                            )
                        cursor = conn.cursor()

                        sql = f""" UPDATE `remeseros` SET `Fondo`= `Fondo` + '{float(temp.texto_cantidad.get())}' WHERE `Id` = {id_remesero} """
                        cursor.execute(sql)
                        conn.commit()

                        temp.destroy()
                        llenar_tabla()
                    except:
                        error = messagebox.showerror("Error","No se pudo recargar al remesero")

            temp.btn_reabastecer = CTkButton(temp,text="Recargar", command=recargar)
            temp.btn_reabastecer.pack(pady=10)  
        
        def modificar():
            temp = CTkToplevel()
            temp.title("Reabastecer") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 200
            hventana = 200
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico')) 

            text = f"Vamos a modificar a {nombre_remesero}"

            temp.label = CTkLabel(temp,text=text)
            temp.label.pack(pady=5)

            temp.texto_nombre = CTkEntry(temp, placeholder_text="Nombre ...")
            temp.texto_nombre.pack(pady=5)

            temp.texto_monto = CTkEntry(temp, placeholder_text="Monto ...")
            temp.texto_monto.pack(pady=5)

            def modificar_remesero():
                conf = messagebox.askokcancel("Confirmar","Se va a modificar este remesero")
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()

                    sql = f""" UPDATE `remeseros` SET `Nombre`='{temp.texto_nombre.get()}',`Fondo`='{temp.texto_monto.get()}' WHERE `Id` = {id_remesero} """
                    cursor.execute(sql)
                    conn.commit()

                    temp.destroy()
                    llenar_tabla()

            temp.btn = CTkButton(temp, text="Modificar",command=modificar_remesero)
            temp.btn.pack(pady=5)

            # ahora vamos a ubicar la info que estaba anteriormente
            def mostrar():
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `remeseros` WHERE `Id` = {id_remesero} """
                cursor.execute(sql)
                for index in cursor:
                    temp.texto_nombre.insert(0,index[1])
                    temp.texto_monto.insert(0,index[2])

            mostrar()

        self.menu = Menu(self,tearoff=0)
        self.menu.add_command(label="Modificar",command=modificar)
        self.menu.add_command(label="Recargar",command=recargar)
        self.menu.add_command(label="Eliminar",command=eliminar)        

        def mostrar_menu_volumen(event):  
            global  id_remesero 
            global nombre_remesero        
            item = self.tabla.identify_row(event.y)
            if item:
                self.tabla.selection_set(item)                
                self.menu.post(event.x_root,event.y_root)
                id_remesero = self.tabla.item(item, "text")      
                nombre_remesero = self.tabla.item(item, "values")[0]      

        self.tabla.bind("<Button-3>",mostrar_menu_volumen)


# **********************************************************************************
# *******************************  Nueva Cuenta **********************************
# **********************************************************************************

class NuevaCuenta(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Nueva Cuenta") 
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 300
        hventana = 300
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico')) 

        self.texto_cuenta = CTkEntry(self, placeholder_text="Nombre ...",width=300)
        self.texto_cuenta.pack(pady = 5)

        def insertar_cuenta():
            conf = messagebox.askokcancel("Confirmar","Se va a Insertar este remesero")
            if conf:
                try:
                    # encontrar el id del remesero
                    id_cuenta = 1
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()

                    sql = """SELECT MAX(Id) FROM `cuentas`;"""
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == None:
                            pass
                        else:
                            id_cuenta = index[0] + 1 

                    # agregar le info a la bd 
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()
                    sql = f""" INSERT INTO `cuentas`(`Id`, `Nombre`, `Fondo`) VALUES ('{id_cuenta}','{self.texto_cuenta.get()}','0') """
                    cursor.execute(sql)
                    conn.commit()

                    self.destroy()
                except:
                    messagebox.showerror("Error","Hubo algun error al entrar la cuenta")

        self.btn = CTkButton(self, text="Insertar", command=insertar_cuenta)
        self.btn.pack(pady = 10) 



# **********************************************************************************
# ******************************** ver remesero ************************************
# **********************************************************************************

class VerCuenta(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Ver Cuenta")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 500
        hventana = 500
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("500x500") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo4.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas()    

        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Fondo"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Nombre", width = 300, anchor="center")
        self.tabla.column("Fondo", width = 100, anchor="center")        

        self.tabla.place(x = 100, y = 50)        
        self.tabla.config(height = 15)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Fondo", text = "Fondo")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla():
            try:
                self.tabla.delete(*self.tabla.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()
    
                sql = f""" SELECT * FROM `cuentas` """
                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],)) 
            except:
                messagebox.showerror("Error","Hubo problemas al actualizar la tabla")

        llenar_tabla()

        # vamos a tener un click derecho para modificar, eliminar y recargar
        def eliminar():
            string = f"Se va a eliminar a {nombre_cuenta} de la Base de Datos"
            conf = messagebox.askokcancel("Confirmar",string)
            if conf:
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" DELETE FROM `cuentas` WHERE `Id` = {id_cuenta} """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()
                except:
                    messagebox.showerror("Error","No se pudo eliminar la cuenta de la Base de Datos")

        def recargar():
            temp = CTkToplevel()
            temp.title("Reabastecer") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 200
            hventana = 200
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico')) 

            text = f"Vamos a recargar a {nombre_cuenta}"

            temp.label = CTkLabel(temp,text=text)
            temp.label.pack(pady=5)

            temp.texto_cantidad = CTkEntry(temp, placeholder_text="Monto ...")
            temp.texto_cantidad.pack(pady=5)

            def recargar():
                string = f"Vamos a recargar la cuenta {nombre_cuenta}"
                conf = messagebox.askokcancel("Confirmar",string)
                if conf:
                    try:
                        # registremos la recarga 
                        id_recarga = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "remesas",
                            password = "123456",
                            database = "remesas"
                            )
                        cursor = conn.cursor()
    
                        sql = """SELECT MAX(Id) FROM `recargas`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass
                            else:
                                id_recarga = index[0] + 1 

                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "remesas",
                            password = "123456",
                            database = "remesas"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `recargas`(`Id`, `Fecha`, `Tipo`, `Id_Cliente`, `Nombre`, `Fondo`) VALUES ('{id_recarga}','{fecha_actual}','C','{id_cuenta}','{nombre_cuenta}','{temp.texto_cantidad.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # aumentemos el fondo del remesero
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "remesas",
                            password = "123456",
                            database = "remesas"
                            )
                        cursor = conn.cursor()

                        sql = f""" UPDATE `cuentas` SET `Fondo`= `Fondo` + '{float(temp.texto_cantidad.get())}' WHERE `Id` = {id_cuenta} """
                        cursor.execute(sql)
                        conn.commit()

                        temp.destroy()
                        llenar_tabla()
                    except:
                        error = messagebox.showerror("Error","No se pudo recargar la cuenta")

            temp.btn_reabastecer = CTkButton(temp,text="Recargar", command=recargar)
            temp.btn_reabastecer.pack(pady=10)  
        
        def modificar():
            temp = CTkToplevel()
            temp.title("Reabastecer") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 200
            hventana = 200
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico')) 

            text = f"Vamos a modificar a {nombre_cuenta}"

            temp.label = CTkLabel(temp,text=text)
            temp.label.pack(pady=5)

            temp.texto_nombre = CTkEntry(temp, placeholder_text="Nombre ...")
            temp.texto_nombre.pack(pady=5)

            temp.texto_monto = CTkEntry(temp, placeholder_text="Monto ...")
            temp.texto_monto.pack(pady=5)

            def modificar_remesero():
                conf = messagebox.askokcancel("Confirmar","Se va a modificar esta cuenta")
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()

                    sql = f""" UPDATE `cuentas` SET `Nombre`='{temp.texto_nombre.get()}',`Fondo`='{temp.texto_monto.get()}' WHERE `Id` = {id_cuenta} """
                    cursor.execute(sql)
                    conn.commit()

                    temp.destroy()
                    llenar_tabla()

            temp.btn = CTkButton(temp, text="Modificar",command=modificar_remesero)
            temp.btn.pack(pady=5)

            # ahora vamos a ubicar la info que estaba anteriormente
            def mostrar():
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `cuentas` WHERE `Id` = {id_cuenta} """
                cursor.execute(sql)
                for index in cursor:
                    temp.texto_nombre.insert(0,index[1])
                    temp.texto_monto.insert(0,index[2])

            mostrar()

        self.menu = Menu(self,tearoff=0)
        self.menu.add_command(label="Modificar",command=modificar)
        self.menu.add_command(label="Recargar",command=recargar)
        self.menu.add_command(label="Eliminar",command=eliminar)        

        def mostrar_menu_volumen(event):  
            global  id_cuenta 
            global nombre_cuenta        
            item = self.tabla.identify_row(event.y)
            if item:
                self.tabla.selection_set(item)                
                self.menu.post(event.x_root,event.y_root)
                id_cuenta = self.tabla.item(item, "text")      
                nombre_cuenta = self.tabla.item(item, "values")[0]      

        self.tabla.bind("<Button-3>",mostrar_menu_volumen)




# **********************************************************************************
# ********************************** Envios ****************************************
# **********************************************************************************

class Envios(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Envios")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo2.jpg"), size = (600,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        # ************************** Labels *************************              
        
        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 630, y = 70) 
        
        self.texto_nombre = CTkEntry(self)
        self.texto_nombre.place(x = 800, y = 70)       

        self.label_monto = CTkLabel(self,text="Monto:", font=("Times New Roman",16))
        self.label_monto.place(x = 630, y = 110)  

        self.texto_monto = CTkEntry(self)
        self.texto_monto.place(x = 800, y = 110) 

        self.label_ganancia = CTkLabel(self,text="Ganancia:", font=("Times New Roman",16))
        self.label_ganancia.place(x = 630, y = 150)  

        self.texto_ganancia = CTkEntry(self)
        self.texto_ganancia.place(x = 800, y = 150) 

        self.label_ganancia_b = CTkLabel(self,text="Ganancia Banco:", font=("Times New Roman",16))
        self.label_ganancia_b.place(x = 630, y = 190)  

        self.texto_ganancia_b = CTkEntry(self)
        self.texto_ganancia_b.place(x = 800, y = 190) 

        self.label_ganancia_r = CTkLabel(self,text="Ganancia Remesero:", font=("Times New Roman",16))
        self.label_ganancia_r.place(x = 630, y = 230)  

        self.texto_ganancia_r = CTkEntry(self)
        self.texto_ganancia_r.place(x = 800, y = 230) 

        self.label_cuenta = CTkLabel(self,text="Cuenta:", font=("Times New Roman",16))
        self.label_cuenta.place(x = 630, y = 270) 

        # aqui hay que buscar el listado de cuentas 

        cuentas = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "remesas",
            password = "123456",
            database = "remesas"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `cuentas`;"""
        cursor.execute(sql)
        for index in cursor:
            cuentas.append(index[1])

        self.texto_cuentas = CTkComboBox(self, values=cuentas)
        self.texto_cuentas.set("...")
        self.texto_cuentas.place(x = 800, y = 270)

        self.label_remesero = CTkLabel(self,text="Remesero:", font=("Times New Roman",16))
        self.label_remesero.place(x = 630, y = 310) 

        # aqui hay que buscar el listado de cuentas 

        remesero = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "remesas",
            password = "123456",
            database = "remesas"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `remeseros`;"""
        cursor.execute(sql)
        for index in cursor:
            remesero.append(index[1])

        self.texto_remesero = CTkComboBox(self, values=remesero)
        self.texto_remesero.set("...")
        self.texto_remesero.place(x = 800, y = 310)

        def ejecutar_envio():
            permiso = False
            # primero asegurarnos que escriban en todos los campos 
            if self.texto_remesero.get() == "..." or self.texto_cuentas.get() == "..." or self.texto_ganancia.get() == "" or self.texto_monto.get() == "" or self.texto_nombre.get() == "" :
                pass
            else:
                permiso = True

            # pedir confirmacion
            if permiso:
                conf = messagebox.askokcancel("Confirmar","Se va a ejecutar el envio")
                if conf:
                    try:
                        # buscar el id del envio
                        id_envio = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "remesas",
                            password = "123456",
                            database = "remesas"
                            )
                        cursor = conn.cursor()
        
                        sql = """SELECT MAX(Id) FROM `envios`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass
                            else:
                                id_envio = index[0] + 1 

                        # ahora ponemos el envio en la bd 
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "remesas",
                            password = "123456",
                            database = "remesas"
                            )
                        cursor = conn.cursor()
                
                        sql = f""" INSERT INTO `envios`(`Id`, `Fecha`, `Nombre`, `Monto`, `Ganacia`, `Cuenta`, `Remesero`) VALUES ('{id_envio}','{fecha_actual}','{self.texto_nombre.get()}','{self.texto_monto.get()}','{self.texto_ganancia.get()}','{self.texto_cuentas.get()}','{self.texto_remesero.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # ahora hay que restar el monto y las ganancias de la cuenta 
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "remesas",
                            password = "123456",
                            database = "remesas"
                            )
                        cursor = conn.cursor()
                
                        sql = f""" UPDATE `cuentas` SET `Fondo`=`Fondo` - '{self.texto_monto.get()}' - '{self.texto_ganancia_b.get()}' - '{self.texto_ganancia_r.get()}' WHERE `Nombre` = '{self.texto_cuentas.get()}' """
                        cursor.execute(sql)
                        conn.commit()

                        # ahora restar el monto del remesero y sumarle su ganancia
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "remesas",
                            password = "123456",
                            database = "remesas"
                            )
                        cursor = conn.cursor()
                
                        sql = f""" UPDATE `remeseros` SET `Fondo`= `Fondo` - '{self.texto_monto.get()}' + '{self.texto_ganancia_r.get()}' WHERE `Nombre` = '{self.texto_remesero.get()}' """
                        cursor.execute(sql)
                        conn.commit()


                        # ahora limpiamos los campos 
                        self.texto_nombre.delete(0,END)
                        self.texto_monto.delete(0,END)
                        self.texto_ganancia.delete(0,END)
                        self.texto_ganancia_r.delete(0,END)
                        self.texto_ganancia_b.delete(0,END)
                        self.texto_cuentas.set("...")
                        self.texto_remesero.set("...")
                    except:
                        messagebox.showerror("Error","Hubo algun error en el proceso")

        self.btn_ejecutar = CTkButton(self,text="Enviar",command=ejecutar_envio, width = 300, height = 40)
        self.btn_ejecutar.place(x=650 ,y=500 )

        

# **********************************************************************************
# ****************************  Consulta Totales ***********************************
# **********************************************************************************

class ConsultasTotales(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Consultas Totales")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))   

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)          

        ###################################################  

        # aqui haremos 2 tablas, una para las cuentas y otra para los remeseros
        estilos_tablas()    

        self.label1 = CTkLabel(self, text="Cuentas")  
        self.label1.place(x = 200, y = 200)  
        
        self.tabla_cuentas = ttk.Treeview(self, columns = ("Nombre", "Recarga", "Enviado", "Ganacia"), show="headings")
        self.tabla_cuentas.column("#0", width = 100, anchor="center")
        self.tabla_cuentas.column("Nombre", width = 200, anchor="center")               
        self.tabla_cuentas.column("Recarga", width = 100, anchor="center")        
        self.tabla_cuentas.column("Enviado", width = 100, anchor="center")        
        self.tabla_cuentas.column("Ganacia", width = 100, anchor="center")        

        self.tabla_cuentas.place(x = 50, y = 300)        
        self.tabla_cuentas.config(height = 10)

        self.tabla_cuentas.heading("#0", text = "Id")
        self.tabla_cuentas.heading("Nombre", text = "Nombre")                
        self.tabla_cuentas.heading("Recarga", text = "Recarga")        
        self.tabla_cuentas.heading("Enviado", text = "Enviado")        
        self.tabla_cuentas.heading("Ganacia", text = "Ganacia")        

        scrollbar = CTkScrollbar(self, command = self.tabla_cuentas.yview, width = 18)
        scrollbar.place(in_ = self.tabla_cuentas, relheigh = 1, relx = 1)

        self.tabla_cuentas.config(yscrollcommand = scrollbar.set)

        # ----------------------------------------------------------------------------
        self.label2 = CTkLabel(self, text="Remeseros")  
        self.label2.place(x = 700, y = 200)  
        
        self.tabla_remeseros = ttk.Treeview(self, columns = ("Nombre", "Recarga", "Enviado", "Ganacia"), show="headings")
        self.tabla_remeseros.column("#0", width = 100, anchor="center")
        self.tabla_remeseros.column("Nombre", width = 200, anchor="center")                
        self.tabla_remeseros.column("Recarga", width = 100, anchor="center")        
        self.tabla_remeseros.column("Enviado", width = 100, anchor="center")        
        self.tabla_remeseros.column("Ganacia", width = 100, anchor="center")        

        self.tabla_remeseros.place(x = 650, y = 300)        
        self.tabla_remeseros.config(height = 10)

        self.tabla_remeseros.heading("#0", text = "Id")
        self.tabla_remeseros.heading("Nombre", text = "Nombre")                
        self.tabla_remeseros.heading("Recarga", text = "Recarga")        
        self.tabla_remeseros.heading("Enviado", text = "Enviado")        
        self.tabla_remeseros.heading("Ganacia", text = "Ganacia")        

        scrollbar2 = CTkScrollbar(self, command = self.tabla_remeseros.yview, width = 18)
        scrollbar2.place(in_ = self.tabla_remeseros, relheigh = 1, relx = 1)

        self.tabla_remeseros.config(yscrollcommand = scrollbar2.set)
        # --------------------------------------------------------------
        # ahora hay que llenar las tablas 
        def llenar_tabla_cuentas():  
            self.tabla_cuentas.delete(*self.tabla_cuentas.get_children())          
            # verifiquemos que las fechas estan dadas
            if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                pass

            else:
                # vamos a crear una lista de listas para mostrar toda la info
                cuentas = []
                # primero vamos a ubicar los nombres de las cuentas 
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()
            
                    sql = f""" SELECT e.Cuenta, COALESCE(r.Total_Recarga,0), e.Total_Enviado, e.Total_Ganancia FROM (SELECT Cuenta, SUM(Monto) AS Total_Enviado, SUM(Ganacia) AS Total_Ganancia FROM envios WHERE Fecha >= "{self.texto_fecha_inicial.get()}" AND Fecha < "{self.texto_fecha_final.get()}" GROUP BY Cuenta) AS e LEFT JOIN (SELECT Nombre, SUM(Fondo) AS Total_Recarga FROM recargas WHERE Fecha >= "{self.texto_fecha_inicial.get()}" AND Fecha < "{self.texto_fecha_final.get()}" AND Tipo = "C" GROUP BY Nombre) AS r ON r.Nombre = e.Cuenta """
                    cursor.execute(sql)
                    for index in cursor:
                        cuentas.append([index[0],index[1],index[2],index[3]])

                    # ahora toca mostrar en la tabla la info de la lista cuentas 
                    for cuenta in cuentas:                
                        self.tabla_cuentas.insert("",END, text = "", values = (cuenta[0],cuenta[1],cuenta[2],cuenta[3],)) 
                
                except:
                    messagebox.showerror("Error","Hubo algun error para actualizar la info")                   
        

        def llenar_tabla_remeseros():
            self.tabla_remeseros.delete(*self.tabla_remeseros.get_children())
            # verifiquemos que las fechas estan dadas
            if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                pass
            else:
                # vamos a crear una lista de listas para mostrar toda la info
                remeseros = []
                # primero vamos a ubicar los nombres de las cuentas 
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()
            
                    sql = f""" SELECT e.Remesero, COALESCE(r.Total_Recarga,0), e.Total_Enviado, e.Total_Ganancia FROM (SELECT Remesero, SUM(Monto) AS Total_Enviado, SUM(Ganacia) AS Total_Ganancia FROM envios WHERE Fecha >= "{self.texto_fecha_inicial.get()}" AND Fecha < "{self.texto_fecha_final.get()}" GROUP BY Remesero) AS e LEFT JOIN (SELECT Nombre, SUM(Fondo) AS Total_Recarga FROM recargas WHERE Fecha >= "{self.texto_fecha_inicial.get()}" AND Fecha < "{self.texto_fecha_final.get()}" AND Tipo = "R" GROUP BY Nombre) AS r ON r.Nombre = e. Remesero """
                    cursor.execute(sql)
                    for index in cursor:
                        remeseros.append([index[0],index[1],index[2],index[3]])

                    # ahora toca mostrar en la tabla la info de la lista remeseros 
                    for rem in remeseros:                
                        self.tabla_remeseros.insert("",END, text = "", values = (rem[0],rem[1],rem[2],rem[3],)) 
                
                except:
                    messagebox.showerror("Error","Hubo algun error para actualizar la info")

        def llenar_labels():           
            # hallar el total enviado y ganado
            conn = mysql.connector.connect(
                host = "localhost",
                user = "remesas",
                password = "123456",
                database = "remesas"
                )
            cursor = conn.cursor()

            sql = f""" SELECT  SUM(`Monto`), SUM(`Ganacia`) FROM `envios` WHERE Fecha >= "{self.texto_fecha_inicial.get()}" AND Fecha < "{self.texto_fecha_final.get()}" """
            cursor.execute(sql)
            for index in cursor:
                str_total_enviado.set(index[0])
                str_total_ganado.set(index[1])         

        self.label1_enviado = CTkLabel(self,text="Total Enviado:")
        self.label1_enviado.place(x=600,y=50) 

        str_total_enviado = StringVar()
        str_total_enviado.set("0")

        self.label2_enviado = CTkLabel(self,textvariable=str_total_enviado)
        self.label2_enviado.place(x=710,y=50) 

        self.label1_ganado = CTkLabel(self,text="Total Ganado:")
        self.label1_ganado.place(x=600,y=90) 

        str_total_ganado = StringVar()
        str_total_ganado.set("0")

        self.label2_ganado = CTkLabel(self,textvariable=str_total_ganado)
        self.label2_ganado.place(x=710,y=90) 

        # ahora pondremos el control de fechas 
        self.label_fechas = CTkLabel(self,text="---------- Control de fechas ----------")
        self.label_fechas.place(x=50,y=50) 

        self.texto_fecha_inicial = CTkEntry(self,placeholder_text="Fecha inicial ...")
        self.texto_fecha_inicial.place(x=50,y=90) 

        def fecha_inicial():
            calendario = CTkToplevel()
            calendario.title("Calendario") 
            htotal = calendario.winfo_screenheight()
            wtotal = calendario.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            calendario.geometry(f"+{posx}+{posy}")
            calendario.lift()
            calendario.attributes('-topmost', True)
            calendario.after(200, lambda: self.attributes('-topmost', False))  

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()  

            def fecha():
                self.texto_fecha_inicial.delete(0,END)
                fecha_select = cal.get_date()
                self.texto_fecha_inicial.insert(0,str(fecha_select))  
                llenar_tabla_cuentas()
                llenar_tabla_remeseros()   
                llenar_labels()            
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_inicial = CTkButton(self,text="...",command=fecha_inicial, width = 27, height = 27)
        self.btn_fecha_inicial.place(x=200 ,y=90 )

        self.texto_fecha_final = CTkEntry(self,placeholder_text="Fecha final ...")
        self.texto_fecha_final.place(x=50,y=130) 

        def fecha_final():
            calendario = CTkToplevel()
            calendario.title("Calendario") 
            htotal = calendario.winfo_screenheight()
            wtotal = calendario.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            calendario.geometry(f"+{posx}+{posy}")
            calendario.lift()
            calendario.attributes('-topmost', True)
            calendario.after(200, lambda: self.attributes('-topmost', False))  

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()  

            def fecha():
                self.texto_fecha_final.delete(0,END)
                fecha_select = cal.get_date()
                self.texto_fecha_final.insert(0,str(fecha_select))  
                llenar_tabla_cuentas()
                llenar_tabla_remeseros()
                llenar_labels()               
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_fecha_final = CTkButton(self,text="...",command=fecha_final, width = 27, height = 27)
        self.btn_fecha_final.place(x=200 ,y=130 )



# **********************************************************************************
# ******************************  Control Envios ***********************************
# **********************************************************************************

class ControlEnvios(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Control Envios")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo4.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)          

        ###################################################

        estilos_tablas() 

        self.tabla = ttk.Treeview(self, columns = ("Fecha", "Nombre", "Monto", "Ganancia", "Cuenta", "Remesero"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")        
        self.tabla.column("Nombre", width = 200, anchor="center")
        self.tabla.column("Monto", width = 100, anchor="center")        
        self.tabla.column("Ganancia", width = 100, anchor="center")        
        self.tabla.column("Cuenta", width = 100, anchor="center")
        self.tabla.column("Remesero", width = 200, anchor="center")

        self.tabla.place(x = 200, y = 100)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")        
        self.tabla.heading("Nombre", text = "Nombre", anchor="center")
        self.tabla.heading("Monto", text = "Monto", anchor="center")        
        self.tabla.heading("Ganancia", text = "Ganancia", anchor="center")        
        self.tabla.heading("Cuenta", text = "Cuenta", anchor="center")
        self.tabla.heading("Remesero", text = "Remesero", anchor="center")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def eliminar():
            conf = messagebox.askokcancel("Confirmar","Se va a eliminar el envio seleccionado")
            if conf:
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" DELETE FROM `envios` WHERE `Id` = {id_envio} """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()

                except:
                    messagebox.showerror("Error", "No se pudo eliminar el envio")

        self.menu = Menu(self,tearoff=0)        
        self.menu.add_command(label="Eliminar",command=eliminar) 

        def click_derecho(event):
            global  id_envio                    
            item = self.tabla.identify_row(event.y)
            if item:
                self.tabla.selection_set(item)                
                self.menu.post(event.x_root,event.y_root)
                id_envio = self.tabla.item(item, "text")                  

        self.tabla.bind("<Button-3>",click_derecho)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `envios` ORDER BY `Fecha` DESC, `Id` DESC  """
                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],index[6],)) 

            except:
                messagebox.showerror("Error","No se pudo actualizar la tabla")

        llenar_tabla()



# **********************************************************************************
# *****************************  Control Recargas **********************************
# **********************************************************************************

class ControlRecargas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Control Recargas")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo4.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)          

        ###################################################

        estilos_tablas() 

        self.tabla = ttk.Treeview(self, columns = ("Fecha", "Tipo", "Id_Cliente", "Nombre", "Fondo"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")        
        self.tabla.column("Tipo", width = 200, anchor="center")
        self.tabla.column("Id_Cliente", width = 100, anchor="center")        
        self.tabla.column("Nombre", width = 100, anchor="center")        
        self.tabla.column("Fondo", width = 100, anchor="center")        

        self.tabla.place(x = 200, y = 100)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")        
        self.tabla.heading("Tipo", text = "Tipo", anchor="center")
        self.tabla.heading("Id_Cliente", text = "Id_Cliente", anchor="center")        
        self.tabla.heading("Nombre", text = "Nombre", anchor="center")        
        self.tabla.heading("Fondo", text = "Fondo", anchor="center")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def eliminar():
            conf = messagebox.askokcancel("Confirmar","Se va a eliminar el envio seleccionado")
            if conf:
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "remesas",
                        password = "123456",
                        database = "remesas"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" DELETE FROM `recargas` WHERE `Id` = {id_envio} """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()

                except:
                    messagebox.showerror("Error", "No se pudo eliminar la recarga")

        self.menu = Menu(self,tearoff=0)        
        self.menu.add_command(label="Eliminar",command=eliminar) 

        def click_derecho(event):
            global  id_envio                    
            item = self.tabla.identify_row(event.y)
            if item:
                self.tabla.selection_set(item)                
                self.menu.post(event.x_root,event.y_root)
                id_envio = self.tabla.item(item, "text")                  

        self.tabla.bind("<Button-3>",click_derecho)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `recargas` ORDER BY `Fecha` DESC, `Id` DESC  """
                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],)) 

            except:
                messagebox.showerror("Error","No se pudo actualizar la tabla")

        llenar_tabla()




# **********************************************************************************
# *****************************  Consulta Reales ***********************************
# **********************************************************************************

class ConsultaReal(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Consultas Real")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/remesas/imagenes funcionamiento/remesas_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))   

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/remesas/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)          

        ###################################################  

        estilos_tablas()  

        # tabla remesero  
        
        self.tabla_remesero = ttk.Treeview(self, columns = ("Nombre", "Fondo"), show="headings")
        self.tabla_remesero.column("#0", width = 100, anchor="center")
        self.tabla_remesero.column("Nombre", width = 300, anchor="center")
        self.tabla_remesero.column("Fondo", width = 100, anchor="center")        

        self.tabla_remesero.place(x = 100, y = 120)        
        self.tabla_remesero.config(height = 15)

        self.tabla_remesero.heading("#0", text = "Codigo")
        self.tabla_remesero.heading("Nombre", text = "Nombre")
        self.tabla_remesero.heading("Fondo", text = "Fondo")        

        scrollbar = CTkScrollbar(self, command = self.tabla_remesero.yview, width = 18)
        scrollbar.place(in_ = self.tabla_remesero, relheigh = 1, relx = 1)

        self.tabla_remesero.config(yscrollcommand = scrollbar.set)

        def llenar_tabla_remesero():
            try:
                self.tabla_remesero.delete(*self.tabla_remesero.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()
    
                sql = f""" SELECT * FROM `remeseros` """
                cursor.execute(sql)
                for index in cursor:
                    self.tabla_remesero.insert("",END, text = index[0], values = (index[1],index[2],)) 
            except:
                messagebox.showerror("Error","Hubo problemas al actualizar la pagina")

        llenar_tabla_remesero()

        # tabla cuentas 

        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Fondo"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Nombre", width = 300, anchor="center")
        self.tabla.column("Fondo", width = 100, anchor="center")        

        self.tabla.place(x = 700, y = 120)        
        self.tabla.config(height = 15)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Fondo", text = "Fondo")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla_cuentas():
            try:
                self.tabla.delete(*self.tabla.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "remesas",
                    password = "123456",
                    database = "remesas"
                    )
                cursor = conn.cursor()
    
                sql = f""" SELECT * FROM `cuentas` """
                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],)) 
            except:
                messagebox.showerror("Error","Hubo problemas al actualizar la tabla")

        llenar_tabla_cuentas()

        # ahora los totales 
        total_cuentas  = StringVar()
        total_remeseros  = StringVar()    

        try:
            conn = mysql.connector.connect(
                host = "localhost",
                user = "remesas",
                password = "123456",
                database = "remesas"
                )
            cursor = conn.cursor()

            sql = f""" SELECT SUM(`Fondo`) FROM `cuentas`  """
            cursor.execute(sql)
            for index in cursor:
                total_cuentas.set(index[0])
        except:
            messagebox.showerror("Error","Hubo problemas al calcular los totales")    

        try:
            conn = mysql.connector.connect(
                host = "localhost",
                user = "remesas",
                password = "123456",
                database = "remesas"
                )
            cursor = conn.cursor()

            sql = f""" SELECT SUM(`Fondo`) FROM `remeseros`  """
            cursor.execute(sql)
            for index in cursor:
                total_remeseros.set(index[0])
        except:
            messagebox.showerror("Error","Hubo problemas al calcular los totales")  

        self.texto_total_cuentas = CTkLabel(self, text = "Cuentas  (Total: " + total_cuentas.get() + " )")
        self.texto_total_cuentas.place(x=650, y=50)

        self.texto_total_remeseros = CTkLabel(self, text = "Remeseros  (Total: " + total_remeseros.get() + " )")
        self.texto_total_remeseros.place(x=150, y=50)
        















        














conn.close()
autenticacion = Autenticacion()
autenticacion.mainloop()