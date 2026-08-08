from customtkinter import *
from customtkinter import CTkImage
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from datetime import *
import mysql.connector
import subprocess
from PIL import Image , ImageTk
import pandas as pd 
from tkcalendar import *
import copy
import shutil
import sqlite3
import os
import json



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



ususario_lilly_is_created = False
base_data_is_created = False
table_usuarios_is_created = False
usuario_lilly_is_created = False
table_licencias_is_created = False

# ********************** creando usuario admin ******************************

try:
    sql = """CREATE USER 'lilly'@'localhost' IDENTIFIED BY '123456';"""
    cursor.execute(sql)
    conn.commit()
except:
    ususario_lilly_is_created = True

sql = """GRANT ALL PRIVILEGES ON *.* TO 'lilly'@'localhost' REQUIRE NONE WITH GRANT OPTION MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0; """
cursor.execute(sql)
conn.commit()

conn.close()

conn = mysql.connector.connect(
    host = "localhost",
    user = "lilly",
    password = "123456",
    )
cursor = conn.cursor()

# ******* creando la base de datos lilly ***********
try:
    sql = """CREATE DATABASE lilly CHARACTER SET = utf8mb4 COLLATE utf8mb4_spanish_ci;"""
    cursor.execute(sql)
    conn.commit()
    base_data_is_created = True
except:
    base_data_is_created = True

conn = mysql.connector.connect(
    host = "localhost",
    user = "lilly",
    password = "123456",
    database = "lilly"
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
    user = "lilly",
    password = "123456",
    database = "lilly"
    )
cursor = conn.cursor()

usuario_inicial = []
sql = """ SELECT Usuario FROM usuarios """
cursor.execute(sql)

for usser in cursor:
    usuario_inicial.append(usser)

for index in range(len(usuario_inicial)):
    if usuario_inicial[index][0] == "lilly":
        usuario_lilly_is_created = True

if usuario_lilly_is_created == False:
    try:
        sql = """INSERT INTO usuarios (Usuario,Password) VALUES ("lilly","123456")"""
        cursor.execute(sql)
        conn.commit()
        
        usuario_lilly_is_created = True
    except:
        usuario_lilly_is_created = True


# ************** creando tabla licencias ***************

conn = mysql.connector.connect(
    host = "localhost",
    user = "lilly",
    password = "123456",
    database = "lilly"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `lilly`.`licencias` (`codigo_lic` VARCHAR(50) NOT NULL , `pass_economia` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    table_licencias_is_created = True   



# ******************** Creando Tabla productos *******************

conn = mysql.connector.connect(
    host = "localhost",
    user = "lilly",
    password = "123456",
    database = "lilly"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `lilly`.`productos` (`Codigo` INT(11) NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `CostoUsd` FLOAT NOT NULL,`Precio` FLOAT NOT NULL, `Cantidad` FLOAT NOT NULL, `Categoria` VARCHAR(50) NOT NULL, `Minimo` INT NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    temp = True



# ******************** Creando Tabla carrito *******************

conn = mysql.connector.connect(
    host = "localhost",
    user = "lilly",
    password = "123456",
    database = "lilly"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `lilly`.`carrito` (`Codigo` VARCHAR(50) NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `CostoUsd` FLOAT NOT NULL,`Precio` FLOAT NOT NULL, `Cantidad` FLOAT NOT NULL, `Categoria` VARCHAR(50) NOT NULL  ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    temp = True



# ********************** creando tabla entradas ***********************************
try:
    sql = """CREATE TABLE `lilly`.`entradas` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL,`Codigo` INT NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `CostoUsd` FLOAT NOT NULL, `Cantidad` FLOAT NOT NULL,`Categoria` VARCHAR(50) NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True



# ********************** creando tabla salidas ***********************************
try:
    sql = """CREATE TABLE `lilly`.`salidas` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL,`Codigo` INT NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `CostoUsd` FLOAT NOT NULL, `Precio` FLOAT NOT NULL, `Cantidad` FLOAT NOT NULL, `Envia` VARCHAR(50) NOT NULL, `Recibe` VARCHAR(50) NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ********************** creando tabla para gastos asociados ***********************************
try:
    sql = """CREATE TABLE `lilly`.`asociados` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL, `Concepto` VARCHAR(100) NOT NULL, `Monto` FLOAT NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ********************** creando tabla para gastos salario ***********************************
try:
    sql = """CREATE TABLE `lilly`.`salarios` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL, `Concepto` VARCHAR(100) NOT NULL, `Monto` FLOAT NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ********************** creando tabla regalos ***********************************
try:
    sql = """CREATE TABLE `lilly`.`regalos` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL,`Codigo` INT NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `CostoUsd` FLOAT NOT NULL, `Precio` FLOAT NOT NULL, `Cantidad` INT NOT NULL, `Categoria` VARCHAR(50) NOT NULL, `Concepto` VARCHAR(50) NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# *************************** creando tabla categorias ****************************
try:
    sql = """CREATE TABLE `lilly`.`categorias` (`Nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True



# *************************** creando tabla trabajadores ****************************
try:
    sql = """CREATE TABLE `lilly`.`trabajadores` (`Nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# *************************** creando tabla envia ****************************
try:
    sql = """CREATE TABLE `lilly`.`envia` (`Id` INT NOT NULL,`Nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# *************************** creando tabla recibe ****************************
try:
    sql = """CREATE TABLE `lilly`.`recibe` (`Id` INT NOT NULL, `Nombre` VARCHAR(50) NOT NULL, `Direccion` VARCHAR(100) NOT NULL, `Telefono` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# *************************** creando tabla tarifas ****************************
try:
    sql = """CREATE TABLE `lilly`.`tarifas` (`USD` FLOAT NOT NULL, `EUR` FLOAT NOT NULL, `EUR-USD` FLOAT NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# *************************** creando tabla mensajerias ****************************
try:
    sql = """CREATE TABLE `lilly`.`mensajeria` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL, `Monto` FLOAT NOT NULL ) ENGINE = InnoDB;"""
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
        self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo1.jpg"), size = (400,200))  

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
            user = "lilly",
            password = "123456",
            database = "lilly"
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
            user = "lilly",
            password = "123456",
            database = "lilly"
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
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo1.jpg"), size = (300,200))  

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
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
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
        self.title("Lilly")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))
        self.resizable(False,False)   

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo3.jpg"), size = (1300,700))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################          
        
        firma = "Vence (" + str(fecha_vencimiento) + ")"
        self.label_lilly = CTkLabel(self, text = firma, font=("Times New Roman",16))
        self.label_lilly.place(x = 1150, y = 650)

        self.menu = Menu(self)
        self.config(menu=self.menu, width="200", height="100")        

        def nuevo_producto_lobby():
            np = NuevoProducto()

        def reabastecer_lobby():
            reab = Reabastecer()

        def ventas_lobby():
            vent = Ventas()

        def control_venta():
            # vamos a ponerle seguridad a los controles 
            temp = CTkToplevel()
            temp.title("Seguridad") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

            temp.texto_pass = CTkEntry(temp, placeholder_text="Contraseña ...", show="*")
            temp.texto_pass.pack(pady=5)

            def aceptar():
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = """ SELECT `pass_economia` FROM `licencias` """
                cursor.execute(sql)
                for index in cursor:
                    if index[0] == temp.texto_pass.get():
                        temp.destroy()
                        cont_vent = ControlVentas()
                    else:
                        messagebox.showerror("Error","La contraseña no es correcta")


            temp.btn_cambiar = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn_cambiar.pack(pady=10)  

            def modificar():
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = """ SELECT `pass_economia` FROM `licencias` """
                cursor.execute(sql)
                for index in cursor:
                    if index[0] == temp.texto_pass.get():
                        temp.destroy()
                        root = CTkToplevel()
                        root.title("Cambiar Contraseña") 
                        htotal = root.winfo_screenheight()
                        wtotal = root.winfo_screenwidth()
                        wventana = 300
                        hventana = 300
                        posx = round(wtotal/2-wventana/2)
                        posy = round(htotal/2-hventana/2)
                        root.geometry(f"+{posx}+{posy}")
                        root.lift()
                        root.attributes('-topmost', True)
                        root.after(200, lambda: root.attributes('-topmost', False)) 
                        root.after(250, lambda: root.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                        root.texto_pass = CTkEntry(root, placeholder_text="Nueva Contraseña ...")
                        root.texto_pass.pack(pady=5)

                        root.texto_confirmar = CTkEntry(root, placeholder_text="Confirmar Contraseña ...")
                        root.texto_confirmar.pack(pady=5)

                        def modificar_pass():
                            if root.texto_pass.get() == root.texto_confirmar.get():
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "lilly",
                                    password = "123456",
                                    database = "lilly"
                                    )
                                cursor = conn.cursor()

                                sql = f""" UPDATE `licencias` SET `pass_economia`='{root.texto_pass.get()}'  """
                                cursor.execute(sql)
                                conn.commit()
                                root.destroy()

                            else:
                                messagebox.showerror("Error","No coinciden las contraseñas escritas")

                        root.btn_cambiar = CTkButton(root, text="Modificar", command=modificar_pass)
                        root.btn_cambiar.pack(pady=10) 


            temp.btn_cambiar = CTkButton(temp, text="Modificar", command=modificar)
            temp.btn_cambiar.pack(pady=10)             

        def control_regalo():
            # vamos a ponerle seguridad a los controles 
            temp = CTkToplevel()
            temp.title("Seguridad") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

            temp.texto_pass = CTkEntry(temp, placeholder_text="Contraseña ...", show="*")
            temp.texto_pass.pack(pady=5)

            def aceptar():
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = """ SELECT `pass_economia` FROM `licencias` """
                cursor.execute(sql)
                for index in cursor:
                    if index[0] == temp.texto_pass.get():
                        temp.destroy()
                        cont_reg = ControlRegalos()
                    else:
                        messagebox.showerror("Error","La contraseña no es correcta")


            temp.btn_cambiar = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn_cambiar.pack(pady=10)  

            def modificar():
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = """ SELECT `pass_economia` FROM `licencias` """
                cursor.execute(sql)
                for index in cursor:
                    if index[0] == temp.texto_pass.get():
                        temp.destroy()
                        root = CTkToplevel()
                        root.title("Cambiar Contraseña") 
                        htotal = root.winfo_screenheight()
                        wtotal = root.winfo_screenwidth()
                        wventana = 300
                        hventana = 300
                        posx = round(wtotal/2-wventana/2)
                        posy = round(htotal/2-hventana/2)
                        root.geometry(f"+{posx}+{posy}")
                        root.lift()
                        root.attributes('-topmost', True)
                        root.after(200, lambda: root.attributes('-topmost', False)) 
                        root.after(250, lambda: root.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                        root.texto_pass = CTkEntry(root, placeholder_text="Nueva Contraseña ...")
                        root.texto_pass.pack(pady=5)

                        root.texto_confirmar = CTkEntry(root, placeholder_text="Confirmar Contraseña ...")
                        root.texto_confirmar.pack(pady=5)

                        def modificar_pass():
                            if root.texto_pass.get() == root.texto_confirmar.get():
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "lilly",
                                    password = "123456",
                                    database = "lilly"
                                    )
                                cursor = conn.cursor()

                                sql = f""" UPDATE `licencias` SET `pass_economia`='{root.texto_pass.get()}'  """
                                cursor.execute(sql)
                                conn.commit()
                                root.destroy()

                            else:
                                messagebox.showerror("Error","No coinciden las contraseñas escritas")

                        root.btn_cambiar = CTkButton(root, text="Modificar", command=modificar_pass)
                        root.btn_cambiar.pack(pady=10) 


            temp.btn_cambiar = CTkButton(temp, text="Modificar", command=modificar)
            temp.btn_cambiar.pack(pady=10)               

        def almacen_lobby():
            alm = Almacen()

        def control_salarios_lobby():
            cs = ConsultaSalarios()

        def control_asociados_lobby():
            ca = ConsultaAsociados()

        def consulta_totales_lobby():
            cons = ConsultaTotales()

        def salarios_lobby():
            sal = Salarios()

        def asociados_lobby():
            aso = Asociados()

        def trabajadores_lobby():
            tra = Trabajadores()
        
        def categorias_lobby():
            cat = Categorias()        
        
        def tarifas_lobby():
            pr = Tarifas()

        def deficit_lobby():
            de = Deficit()

        def envian_lobby():
            de = Envian()

        def reciben_lobby():
            de = Reciben()

        def clientes_lobby():
            cli = Clientes()

        def salva_lobby():            
            # Crear carpeta de respaldos si no existe
            carpeta_respaldo = "D:/lilly/respaldos"
            if not os.path.exists(carpeta_respaldo):
                os.makedirs(carpeta_respaldo)
            
            # Nombre del archivo con fecha_actual
            nombre_archivo = f"lilly_{fecha_actual}.sql"
            ruta_completa = os.path.join(carpeta_respaldo, nombre_archivo)
            
            # Ruta de mysqldump en XAMPP
            ruta_mysqldump = "C:/xampp/mysql/bin/mysqldump.exe"
            
            try:
                # Comando con ruta completa
                comando = f'"{ruta_mysqldump}" -u lilly -p123456 lilly > "{ruta_completa}"'
                
                # Ejecutar el comando
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                
                # Verificar que el archivo se creó y tiene contenido
                if os.path.exists(ruta_completa) and os.path.getsize(ruta_completa) > 0:
                    messagebox.showinfo("Éxito", f"Respaldo creado exitosamente:\n{ruta_completa}\nTamaño: {os.path.getsize(ruta_completa)} bytes")
                else:
                    # Mostrar error detallado
                    error_msg = resultado.stderr if resultado.stderr else "No se pudo crear el respaldo"
                    messagebox.showerror("Error", f"Error al crear respaldo:\n{error_msg}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear respaldo:\n{str(e)}")
        
        def agregar_usuario():
            usuario_agregar = UsuarioAgregar()
            
        def eliminar_usuario():                        
            eliminar_usuario = EliminarUsuario()             

        def agregar_nueva_licencia():                         
            nueva_licencia = NuevaLicencia()

        def exportar_web_lobby():            
            try:
                # Crear la carpeta si no existe
                carpeta = "D:/Lilly/respaldos"
                if not os.path.exists(carpeta):
                    os.makedirs(carpeta)
                
                # Nombre del archivo usando la fecha_actual existente
                nombre_archivo = f"productos_{fecha_actual}.json"
                ruta_completa = os.path.join(carpeta, nombre_archivo)
                
                # Conectar a la base de datos
                conn = mysql.connector.connect(
                    host="localhost",
                    user="lilly",
                    password="123456",
                    database="lilly"
                )
                cursor = conn.cursor()
                
                # Consultar los productos
                sql = """SELECT Codigo, Nombre, Precio, Cantidad, Categoria FROM productos"""
                cursor.execute(sql)
                
                # Crear la lista de productos
                productos = []
                for row in cursor:
                    producto = {
                        "Codigo": row[0],
                        "Nombre": row[1],
                        "Precio": float(row[2]) if row[2] is not None else 0,
                        "Cantidad": float(row[3]) if row[3] is not None else 0,
                        "Categoria": row[4]
                    }
                    productos.append(producto)
                
                # Guardar el archivo JSON
                with open(ruta_completa, 'w', encoding='utf-8') as f:
                    json.dump(productos, f, ensure_ascii=False, indent=4)
                
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Éxito", f"Archivo JSON generado exitosamente:\n{ruta_completa}")
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error de Base de Datos", f"No se pudo conectar a la base de datos:\n{str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar el archivo:\n{str(e)}")

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

        control_menu = Menu(self.menu, tearoff = 0)   
        control_menu.add_command(label="Control Regalo", command = control_regalo)                                     
        control_menu.add_command(label="Control Venta", command = control_venta)            

        gastos_menu = Menu(self.menu, tearoff = 0)   
        gastos_menu.add_command(label="Asociados", command = asociados_lobby)                                     
        gastos_menu.add_command(label="Salarios", command = salarios_lobby) 

        consultas_menu = Menu(self.menu, tearoff = 0)   
        consultas_menu.add_command(label="Totales", command = consulta_totales_lobby)        
        consultas_menu.add_command(label="Almacen", command = almacen_lobby)        
        consultas_menu.add_command(label="Salarios", command = control_salarios_lobby)        
        consultas_menu.add_command(label="Asociados", command = control_asociados_lobby)        
        consultas_menu.add_command(label="Deficit", command = deficit_lobby)        
        consultas_menu.add_command(label="Clientes", command = clientes_lobby)        
        
        entradas_menu = Menu(self.menu, tearoff = 0)
        entradas_menu.add_command(label="Nuevo Producto", command = nuevo_producto_lobby)                     
        entradas_menu.add_command(label="Reabastecer", command = reabastecer_lobby) 

        administrativo_menu = Menu(self.menu, tearoff = 0)
        administrativo_menu.add_command(label="Categorias", command = categorias_lobby)        
        administrativo_menu.add_command(label="Trabajadores", command = trabajadores_lobby) 
        administrativo_menu.add_command(label="Envian", command = envian_lobby) 
        administrativo_menu.add_command(label="Reciben", command = reciben_lobby) 
        administrativo_menu.add_command(label="Tarifas", command = tarifas_lobby)                            

        usuario_menu = Menu(self.menu, tearoff = 0)
        usuario_menu.add_command(label="Agregar", command = agregar_usuario)
        usuario_menu.add_command(label="Eliminar", command = eliminar_usuario)

        licencia_menu = Menu(self.menu, tearoff = 0)
        licencia_menu.add_command(label="Nueva", command = agregar_nueva_licencia)

        salir_menu = Menu(self.menu, tearoff = 0)
        salir_menu.add_command(label="Cerrar Cesion", command = cerrar_cesion)
        salir_menu.add_command(label="Cerrar Programa", command = cerrar_programa)
        
        self.menu.add_cascade (label="Ventas", command = ventas_lobby) 
        self.menu.add_cascade (label="Control", menu = control_menu)
        self.menu.add_cascade (label="Gastos", menu = gastos_menu)
        self.menu.add_cascade (label="Consultas", menu = consultas_menu)
        self.menu.add_cascade (label="Entradas", menu = entradas_menu)                       
        self.menu.add_cascade (label="Administrativo", menu = administrativo_menu)                 
        self.menu.add_cascade (label="Salva", command = salva_lobby)        
        self.menu.add_cascade (label="Web", command = exportar_web_lobby)        
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
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))    

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo5.jpg"), size = (400,300))  

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
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
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
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo5.jpg"), size = (400,300))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################            
        
        items_usuarios = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "lilly",
            password = "123456",
            database = "lilly"
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
                if texto_nombre_usuario_eliminar.get() == "lilly":
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
                                    user = "lilly",
                                    password = "123456",
                                    database = "lilly"
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
# ***************************** Trabajadores ****************************************
# **********************************************************************************

class Trabajadores(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Trabajadores")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))     

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (800,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################        

        estilos_tablas()  

        self.tabla = ttk.Treeview(self, columns = ())
        self.tabla.column("#0", width = 500)

        self.tabla.place(x = 100, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Trabajadores")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def on_click(event):
            global nombre_trabajadores
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                nombre_trabajadores = self.tabla.item(item, "text")                

        self.tabla.bind("<ButtonRelease-1>", on_click)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `trabajadores`;"""
            cursor.execute(sql)

            for index in cursor:
                self.tabla.insert("",END, text = index[0])

        llenar_tabla()


        def agregar():           
            temp = CTkToplevel()
            temp.title("Agregar") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False))  
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

            temp.texto_nombre = CTkEntry(temp, placeholder_text="Trabajador ...")
            temp.texto_nombre.pack(pady = 10)

            def aceptar():
                if temp.texto_nombre.get() == "":
                    error = messagebox.showerror("Error","Debes escribir algun nombre")
                else:
                    # vemos que no se repita el trabajador
                    repetido = False
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `trabajadores` """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == temp.texto_nombre.get():
                            repetido = True
                            error = messagebox.showerror("Error","Ese trabajador ya existe")

                    if not repetido:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `trabajadores`(`Nombre`) VALUES ('{temp.texto_nombre.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla()

                        term = messagebox.showinfo("Terminado","Se ha agregado el trabajador")
                        temp.destroy()

            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)


        def eliminar():
            global nombre_trabajadores           
            try:
                string = f"Vas a eliminar a {nombre_trabajadores} de los trabajadores"
                conf = messagebox.askokcancel("Confirmar",string)    
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `trabajadores` WHERE `Nombre` = "{nombre_trabajadores}" """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()

                    term = messagebox.showinfo("Terminado","Se ha eliminado el trabajador")
                    nombre_trabajadores = None

            except:
                error = messagebox.showerror("Error","Selecciona un trabajador para eliminar") 


        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 50)
        self.btn_agregar.place(x = 100, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar, width = 200, height = 50)
        self.btn_eliminar.place(x = 500, y = 400) 



# **********************************************************************************
# ***************************** Categorias *****************************************
# **********************************************************************************

class Categorias(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Categorias")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))      

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (800,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################         

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ())
        self.tabla.column("#0", width = 500)

        self.tabla.place(x = 100, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Categorias")

        scrollbar_entrenadores = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar_entrenadores.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar_entrenadores.set)        

        def on_click(event):
            global nombre_categoria
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                nombre_categoria = self.tabla.item(item, "text")                

        self.tabla.bind("<ButtonRelease-1>", on_click)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `categorias`;"""
            cursor.execute(sql)

            for index in cursor:
                self.tabla.insert("",END, text = index[0])

        llenar_tabla()

        def agregar():           
            temp = CTkToplevel()
            temp.title("Agregar") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))  

            temp.texto_nombre = CTkEntry(temp, placeholder_text="Categoria ...")
            temp.texto_nombre.pack(pady = 10)

            def aceptar():
                if temp.texto_nombre.get() == "":
                    error = messagebox.showerror("Error","Debes escribir algun nombre para la categoria que quieres agregar")
                else:
                    # vemos que no se repita la categoria
                    repetido = False
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `categorias` """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == temp.texto_nombre.get():
                            repetido = True
                            error = messagebox.showerror("Error","Esa categoria ya existe")

                    if not repetido:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `categorias`(`Nombre`) VALUES ('{temp.texto_nombre.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla()

                        term = messagebox.showinfo("Terminado","Se ha creado la Categoria")
                        temp.destroy()

            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)


        def eliminar():
            global nombre_categoria            
            try:
                string = f"Vas a eliminar a {nombre_categoria} de las categorias"
                conf = messagebox.askokcancel("Confirmar",string)    
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `categorias` WHERE `Nombre` = "{nombre_categoria}" """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()

                    term = messagebox.showinfo("Terminado","Se ha eliminado la Categoria")
                    nombre_categoria = None

            except:
                error = messagebox.showerror("Error","Selecciona una categoria para eliminar")                    

       

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 30)
        self.btn_agregar.place(x = 100, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar, width = 200, height = 30)
        self.btn_eliminar.place(x = 500, y = 400)    


# **********************************************************************************
# ********************************* Envian *****************************************
# **********************************************************************************

class Envian(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Envian")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))      

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (800,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################         

        estilos_tablas()  

        self.tabla = ttk.Treeview(self, columns = ())
        self.tabla.column("#0", width = 500)

        self.tabla.place(x = 100, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Nombre")

        scrollbar_entrenadores = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar_entrenadores.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar_entrenadores.set)  

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `envia`;"""
            cursor.execute(sql)

            for index in cursor:
                self.tabla.insert("",END, text = index[1])

        llenar_tabla()

        def agregar():           
            temp = CTkToplevel()
            temp.title("Agregar") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))  

            temp.texto_nombre = CTkEntry(temp, placeholder_text="Nombre...")
            temp.texto_nombre.pack(pady = 10)

            def aceptar():
                if temp.texto_nombre.get() == "":
                    error = messagebox.showerror("Error","Debes escribir algun nombre")
                else:
                    # vemos que no se repita la categoria
                    repetido = False
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `envia` """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == temp.texto_nombre.get():
                            repetido = True
                            error = messagebox.showerror("Error","Esa nombre ya existe")

                    if not repetido:
                        # encontrarle el id 
                        id_entrada = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = """SELECT MAX(Id) FROM `envia`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass

                            else:
                                id_entrada = index[0] + 1

                        # agregarlo en la bd 
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()                        

                        sql = f""" INSERT INTO `envia`(`Id`, `Nombre`) VALUES ('{id_entrada}','{temp.texto_nombre.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla()

                        term = messagebox.showinfo("Terminado","Se ha agregado")
                        temp.destroy()

            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 30)
        self.btn_agregar.place(x = 100, y = 400)  

        def double_click(event):            
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                nombre = self.tabla.item(item, "text") 

            conf = messagebox.askokcancel("Confirmar","Se va a eliminar") 
            if conf:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = f""" DELETE FROM `envia` WHERE `Nombre` = "{nombre}" """
                cursor.execute(sql)
                conn.commit()

                llenar_tabla()              

        self.tabla.bind("<Double-1>", double_click)


# **********************************************************************************
# ******************************** Reciben *****************************************
# **********************************************************************************

class Reciben(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Reciben")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))      

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (800,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################         

        estilos_tablas()  

        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Direccion", "Telefono"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre", width = 200)
        self.tabla.column("Direccion", width = 100)
        self.tabla.column("Telefono", width = 100)
        
        self.tabla.place(x = 50, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Direccion", text = "Direccion")
        self.tabla.heading("Telefono", text = "Telefono")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `recibe`;"""
            cursor.execute(sql)

            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],)) 

        llenar_tabla()

        def agregar():           
            temp = CTkToplevel()
            temp.title("Agregar") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))  

            temp.texto_nombre = CTkEntry(temp, placeholder_text="Nombre...")
            temp.texto_nombre.pack(pady = 10)

            temp.texto_direccion = CTkEntry(temp, placeholder_text="Direccion...")
            temp.texto_direccion.pack(pady = 10)

            temp.texto_telefono = CTkEntry(temp, placeholder_text="Telefono...")
            temp.texto_telefono.pack(pady = 10)

            def aceptar():
                if temp.texto_nombre.get() == "" or temp.texto_direccion.get() == "" or temp.texto_telefono.get() == "":
                    error = messagebox.showerror("Error","Debes llenar los campos")
                else:                    
                    # encontrarle el id 
                    id_entrada = 1
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()

                    sql = """SELECT MAX(Id) FROM `recibe`;"""
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == None:
                            pass

                        else:
                            id_entrada = index[0] + 1

                    # agregarlo en la bd 
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                        

                    sql = f""" INSERT INTO `recibe`(`Id`, `Nombre`, `Direccion`, `Telefono`) VALUES ('{id_entrada}','{temp.texto_nombre.get()}','{temp.texto_direccion.get()}','{temp.texto_telefono.get()}') """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()

                    term = messagebox.showinfo("Terminado","Se ha agregado")
                    temp.destroy()

            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 30)
        self.btn_agregar.place(x = 100, y = 400)  

        def double_click(event):            
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                id_recibe = self.tabla.item(item, "text") 

            conf = messagebox.askokcancel("Confirmar","Se va a eliminar") 
            if conf:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = f""" DELETE FROM `recibe` WHERE `Id` = "{id_recibe}" """
                cursor.execute(sql)
                conn.commit()

                llenar_tabla()              

        self.tabla.bind("<Double-1>", double_click)












        

# **********************************************************************************
# ***************************** Tarifas ********************************************
# **********************************************************************************

class Tarifas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Tarifas")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 300
        hventana = 300
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("300x300") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))    

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (300,300))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################        

        self.label_usd = CTkLabel(self,text="USD: ")   
        self.label_usd.place(x=30,y=30)   

        self.label_eur = CTkLabel(self,text="EUR: ")   
        self.label_eur.place(x=30,y=70) 

        self.label_combinado = CTkLabel(self,text="EUR - USD: ")   
        self.label_combinado.place(x=30,y=110) 

        combinado = StringVar()
        combinado.set("")

        self.label_combinado2 = CTkLabel(self,textvariable = combinado)   
        self.label_combinado2.place(x=130,y=110) 

        self.texto_usd = CTkEntry(self, width=70)
        self.texto_usd.place(x=130,y=30)

        self.texto_eur = CTkEntry(self, width=70)
        self.texto_eur.place(x=130,y=70)

        # mostremos los precios que tienen las tarifas actuales 
        def mostrar_tarifa():
            self.texto_usd.delete(0,END)
            self.texto_eur.delete(0,END)
            
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM `tarifas` """
            cursor.execute(sql)
            for index in cursor:
                self.texto_usd.insert(0,index[0])
                self.texto_eur.insert(0,index[1])
                combinado.set(index[2])
        mostrar_tarifa()

        def modificar():
            # hay que ver si hay que insertar (si no hay nada) o modificar
            vacio = False
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = f""" SELECT COUNT(`USD`) FROM `tarifas`; """
            cursor.execute(sql)
            for index in cursor:
                if index[0] == 0:
                    vacio = True

            if vacio:
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()

                    sql = f""" INSERT INTO `tarifas`(`USD`, `EUR`, `EUR-USD`) VALUES ('{self.texto_usd.get()}','{self.texto_eur.get()}','{float(self.texto_eur.get())/float(self.texto_usd.get())}') """
                    cursor.execute(sql)
                    conn.commit()

                    concluido = messagebox.showinfo("Completado","Se han modificado las tarifas") 
                    mostrar_tarifa()

                except:
                    error = messagebox.showerror("Error","No se pudieron modificar las tarifas")

            else:
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()

                    sql = f""" UPDATE `tarifas` SET `USD`='{self.texto_usd.get()}',`EUR`='{self.texto_eur.get()}',`EUR-USD`='{float(self.texto_eur.get())/float(self.texto_usd.get())}' """
                    cursor.execute(sql)
                    conn.commit()

                    concluido = messagebox.showinfo("Completado","Se han modificado las tarifas") 
                    mostrar_tarifa()
                except:
                    error = messagebox.showerror("Error","No se pudieron modificar las tarifas")

        self.btn_modificar = CTkButton(self, text="Modificar", command=modificar)
        self.btn_modificar.place(x=90,y=200)


# **********************************************************************************
# ******************************** Nuevo Producto **********************************
# **********************************************************************************

class NuevoProducto(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Nuevo Producto")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo2.jpg"), size = (600,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################          

        # ************************** Labels *************************   
         
        # ************************ para saber por donde voy         
        ultimo_id = StringVar()

        label_ultimo_id = CTkLabel(self, textvariable = ultimo_id)
        label_ultimo_id.place(x = 630, y = 30) 

        def actualizar_id():
            ultimo_id.set("")

            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = """SELECT MAX(Codigo) FROM `productos`;"""
            cursor.execute(sql)            
            for index in cursor:                
                ultimo_id.set(index[0])            

        actualizar_id()

        self.label_codigo = CTkLabel(self,text="Codigo:", font=("Times New Roman",16))
        self.label_codigo.place(x = 630, y = 70)   

        self.texto_codigo = CTkEntry(self)
        self.texto_codigo.place(x = 750, y = 70)     

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 630, y = 110) 
        
        self.texto_nombre = CTkEntry(self)
        self.texto_nombre.place(x = 750, y = 110)       

        self.label_costo_usd = CTkLabel(self,text="Costo:", font=("Times New Roman",16))
        self.label_costo_usd.place(x = 630, y = 150)  

        self.texto_costo_usd = CTkEntry(self)
        self.texto_costo_usd.place(x = 750, y = 150) 

        def cambio():
            temp = CTkToplevel()
            temp.title("Cambio de Moneda") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

            tar1 = 0           
            tar2 = 0           
            tar3 = 0 

            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `tarifas`;"""
            cursor.execute(sql)
            for index in cursor:
                tar1 = index[0]
                tar2 = index[1]
                tar3 = index[2]

            tarifa = f"Tarifa:  1USD = {tar1}CUP,  1EUR = {tar2}CUP, 1EUR = {tar3}CUP"                      

            temp.label_tarifa = CTkLabel(temp,text=tarifa, font=("Times New Roman",16))
            temp.label_tarifa.pack(pady=10)

            temp.texto_cup = CTkEntry(temp, placeholder_text="CUP ...")
            temp.texto_cup.pack(pady=5)

            temp.texto_eur = CTkEntry(temp, placeholder_text="EUR ...")
            temp.texto_eur.pack(pady=5)

            def cambiar():
                if temp.texto_cup.get() == "" and temp.texto_eur.get() == "":
                    error = messagebox.showerror("Error", "Debes escribir en algun campo la cantidad a cambiar")

                elif temp.texto_cup.get() != "" and temp.texto_eur.get() != "":
                    error = messagebox.showerror("Error", "Debes escribir solo en un campo, no en ambos")

                else:
                    if temp.texto_cup.get() != "":
                        resultado = round(float(temp.texto_cup.get())/tar1,2)
                        self.texto_costo_usd.delete(0,END)
                        self.texto_costo_usd.insert(0,resultado)
                        temp.destroy()

                    else:
                        resultado = round(float(temp.texto_eur.get())*tar3,2)
                        self.texto_costo_usd.delete(0,END)
                        self.texto_costo_usd.insert(0,resultado)
                        temp.destroy()


            temp.btn_cambiar = CTkButton(temp, text="Cambiar", command=cambiar)
            temp.btn_cambiar.pack(pady=10)           

        self.btn_cambio = CTkButton(self,text="...", width=30,command=cambio)      
        self.btn_cambio.place(x = 900, y = 150)  

        self.label_precio = CTkLabel(self,text="Precio:", font=("Times New Roman",16))
        self.label_precio.place(x = 630, y = 190)  

        self.texto_precio = CTkEntry(self)
        self.texto_precio.place(x = 750, y = 190) 

        self.label_cantidad = CTkLabel(self,text="Cantidad:", font=("Times New Roman",16))
        self.label_cantidad.place(x = 630, y = 230)  

        self.texto_cantidad = CTkEntry(self)
        self.texto_cantidad.place(x = 750, y = 230)

        self.label_categoria = CTkLabel(self,text="Categoria:", font=("Times New Roman",16))
        self.label_categoria.place(x = 630, y = 270)  

        categorias = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "lilly",
            password = "123456",
            database = "lilly"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `categorias`;"""
        cursor.execute(sql)
        for index in cursor:
            categorias.append(index[0])

        self.texto_categoria = CTkComboBox(self, values=categorias)
        self.texto_categoria.set("...")
        self.texto_categoria.place(x = 750, y = 270)  

        self.label_minimo = CTkLabel(self,text="Minimo:", font=("Times New Roman",16))
        self.label_minimo.place(x = 630, y = 310) 

        self.texto_minimo = CTkEntry(self)        
        self.texto_minimo.place(x = 750, y = 310) 

        def agregar_producto():
            try:
                # verificar que no se repite el codigo en la bd 
                repetido = False
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT COUNT(`Codigo`) FROM `productos` WHERE `Codigo` = {self.texto_codigo.get()}; """
                cursor.execute(sql)
                for index in cursor:                
                    if index[0] > 0:
                        repetido = True

                if repetido:
                    error = messagebox.showerror("Error","Ese codigo ya existe en la base de datos")
                else:
                    # pedir confirmacion para agrear el producto
                    conf = messagebox.askokcancel("Confirmar","Vamos a agregar el producto a la base de datos")
                    if conf:
                        # agregar el producto en la bd 
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor() 
                        sql = f""" INSERT INTO `productos`(`Codigo`, `Nombre`, `CostoUsd`, `Precio`, `Cantidad`, `Categoria`, `Minimo`) VALUES ('{self.texto_codigo.get()}','{self.texto_nombre.get()}','{self.texto_costo_usd.get()}','{self.texto_precio.get()}','{self.texto_cantidad.get()}','{self.texto_categoria.get()}','{self.texto_minimo.get()}')  """
                        cursor.execute(sql)
                        conn.commit()

                        # hallemos el id de la entrada
                        id_entrada = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = """SELECT MAX(Id) FROM `entradas`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass

                            else:
                                id_entrada = index[0] + 1                    

                        # agregar la entrada a la bd 
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()                    

                        sql = f""" INSERT INTO `entradas`(`Id`, `Fecha`, `Codigo`, `Nombre`, `CostoUsd`, `Cantidad`, `Categoria`) VALUES ('{id_entrada}','{fecha_actual}','{self.texto_codigo.get()}','{self.texto_nombre.get()}','{self.texto_costo_usd.get()}','{self.texto_cantidad.get()}','{self.texto_categoria.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # limpiar los campos 
                        self.texto_codigo.delete(0,END)
                        self.texto_nombre.delete(0,END)
                        self.texto_costo_usd.delete(0,END)
                        self.texto_precio.delete(0,END)
                        self.texto_cantidad.delete(0,END)                        
                        self.texto_categoria.set("...")
                        self.texto_minimo.delete(0,END)
                        actualizar_id()
        
            except:
                error = messagebox.showerror("Error","Hubo problemas para agregar el producto")          

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=agregar_producto, width = 300, height = 40)
        self.btn_aceptar.place(x=650 ,y=500 )




# **********************************************************************************
# ************************** Reabastecer Producto **********************************
# **********************************************************************************

class Reabastecer(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Reabastecer Producto")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo4.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Costo Usd", "Precio", "Cantidad", "Categoria"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre", width = 200)
        self.tabla.column("Costo Usd", width = 100)
        self.tabla.column("Precio", width = 100)
        self.tabla.column("Cantidad", width = 100)
        self.tabla.column("Categoria", width = 100)

        self.tabla.place(x = 50, y = 200)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Costo Usd", text = "Costo Usd")
        self.tabla.heading("Precio", text = "Precio")
        self.tabla.heading("Cantidad", text = "Cantidad")
        self.tabla.heading("Categoria", text = "Categoria")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_reabastecer(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM productos WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%'; """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],))         

        # vamos a hacer un buscador 

        self.label_buscador = CTkLabel(self,text="------------------------------ Buscador ------------------------------",bg_color="black")
        self.label_buscador.place(x=50,y=50)


        self.texto_buscador_codigo = CTkEntry(self,placeholder_text="Buscar por codigo ...")
        self.texto_buscador_codigo.place(x=50,y=90)          

        self.texto_buscador_codigo.bind("<KeyRelease>", llenar_reabastecer) 

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por nombre ...")
        self.texto_buscador_nombre.place(x=200,y=90) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_reabastecer )   

        llenar_reabastecer(True)

        # cuando demos 2ble click abriremos una ventana para hacer el reabastecimiento a ese producto seleccionado
        def reabastecer(event):
            global codigo
            # vamos a capturar el codigo del numero que vamos a reabastecer
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                codigo = self.tabla.item(item, "text")  

            # vamos a crear la ventana modal
            temp = CTkToplevel()
            temp.title("Reabastecer") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 200
            hventana = 200
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"200x200+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

            def convertir():
                root = CTkToplevel()
                root.title("Cambio de Moneda") 
                htotal = root.winfo_screenheight()
                wtotal = root.winfo_screenwidth()
                wventana = 300
                hventana = 300
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                root.geometry(f"+{posx}+{posy}")
                root.lift()
                root.attributes('-topmost', True)
                root.after(200, lambda: root.attributes('-topmost', False)) 
                root.after(250, lambda: root.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                tar1 = 0           
                tar2 = 0           
                tar3 = 0 

                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = """SELECT * FROM `tarifas`;"""
                cursor.execute(sql)
                for index in cursor:
                    tar1 = index[0]
                    tar2 = index[1]
                    tar3 = index[2]

                tarifa = f"Tarifa:  1USD = {tar1}CUP,  1EUR = {tar2}CUP, 1EUR = {tar3}CUP"                      

                root.label_tarifa = CTkLabel(root,text=tarifa, font=("Times New Roman",16))
                root.label_tarifa.pack(pady=10)

                root.texto_cup = CTkEntry(root, placeholder_text="CUP ...")
                root.texto_cup.pack(pady=5)

                root.texto_eur = CTkEntry(root, placeholder_text="EUR ...")
                root.texto_eur.pack(pady=5)

                def cambiar():
                    temp.texto_costo_usd.delete(0,END)
                    if root.texto_cup.get() == "" and root.texto_eur.get() == "":
                        error = messagebox.showerror("Error", "Debes escribir en algun campo la cantidad a cambiar")

                    elif root.texto_cup.get() != "" and root.texto_eur.get() != "":
                        error = messagebox.showerror("Error", "Debes escribir solo en un campo, no en ambos")

                    else:
                        if root.texto_cup.get() != "":
                            resultado = round(float(root.texto_cup.get())/tar1,2)
                            temp.texto_costo_usd.insert(0,resultado)
                            root.destroy()

                        else:
                            resultado = round(float(root.texto_eur.get())*tar3,2)
                            temp.texto_costo_usd.insert(0,resultado)
                            root.destroy()


                root.btn_cambiar = CTkButton(root, text="Cambiar e Insertar", command=cambiar)
                root.btn_cambiar.pack(pady=10) 


            temp.btn_cambio = CTkButton(temp,text="Cambio Moneda", command=convertir)
            temp.btn_cambio.pack(pady=5)

            temp.texto_costo_usd = CTkEntry(temp, placeholder_text="Costo en usd ...")
            temp.texto_costo_usd.pack(pady=5)            

            temp.texto_cantidad = CTkEntry(temp, placeholder_text="Cantidad ...")
            temp.texto_cantidad.pack(pady=5)

            def reabastecer_producto():
                string = f"Vamos a reestablecer el producto de codigo {codigo}"
                conf = messagebox.askokcancel("Confirmar",string)
                if conf:
                    try:
                        # aqui haremos 2 cambios en la bd, la cantidad que habra del producto y su costo en usd
                        # para saber el promedio del costo
                        costo_antes = 0
                        cant_antes = 0
                        promedio = 0

                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = f""" SELECT `CostoUsd`, `Cantidad` FROM `productos` WHERE `Codigo` = "{codigo}"; """
                        cursor.execute(sql)
                        for index in cursor:
                            costo_antes = index[0]
                            cant_antes = index[1]

                        numerador = costo_antes*cant_antes + float(temp.texto_costo_usd.get())*float(temp.texto_cantidad.get())
                        denominador = cant_antes + float(temp.texto_cantidad.get())

                        promedio = numerador/denominador

                        # llevemos los resultados a la base de datos
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = f""" UPDATE `productos` SET `CostoUsd`='{promedio}',`Cantidad`= `Cantidad` + '{temp.texto_cantidad.get()}' WHERE `Codigo` = "{codigo}" """
                        cursor.execute(sql)
                        conn.commit()

                        temp.destroy()
                        llenar_reabastecer(True)

                    except:
                        error = messagebox.showerror("Error","No se pudo reabastecer el producto")

            temp.btn_reabastecer = CTkButton(temp,text="Reabastecer", command=reabastecer_producto)
            temp.btn_reabastecer.pack(pady=10)                          

        self.tabla.bind("<Double-1>", reabastecer)




# **********************************************************************************
# **********************************  Asociados ************************************
# **********************************************************************************

class Asociados(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Gastos Asociados")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        estilos_tablas()   

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo2.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################        
        
        self.tabla = ttk.Treeview(self, columns = ("Fecha","Concepto", "Monto"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")
        self.tabla.column("Concepto", width = 500, anchor="center")
        self.tabla.column("Monto", width = 100, anchor="center")        

        self.tabla.place(x = 150, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Concepto", text = "Concepto", anchor="center")
        self.tabla.heading("Monto", text = "Monto", anchor="center")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set) 

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM `asociados` WHERE `Fecha` = "{fecha_actual}"; """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],))

        llenar_tabla()        

        def agregar():
            temp = CTkToplevel()
            temp.title("Agregar") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False))  
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

            temp.texto_concepto = CTkEntry(temp, placeholder_text="Concepto ...",width=300)
            temp.texto_concepto.pack(pady = 5)

            temp.texto_monto = CTkEntry(temp, placeholder_text="Monto ...",width=300)
            temp.texto_monto.pack(pady = 5)

            def aceptar_asociado():
                try:
                    conf = messagebox.askokcancel("Confirmar","Se va a agregar el gasto")
                    if conf:
                        # primero encontrar el id que le vamos a dar al gasto asociado
                        id_asociado = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = """SELECT MAX(Id) FROM `asociados`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass

                            else:
                                id_asociado = index[0] + 1  


                        # agregar el gasto asociado a la bd
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `asociados`(`Id`, `Fecha`, `Concepto`, `Monto`) VALUES ('{id_asociado}','{fecha_actual}','{temp.texto_concepto.get()}','{temp.texto_monto.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla()
                        temp.destroy()

                except:
                    error = messagebox.showerror("Error","No se pudo agregar el gasto asociado")

            temp.btn = CTkButton(temp, text="Aceptar Asociado", command=aceptar_asociado)
            temp.btn.pack(pady = 10)  

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 500, height = 50)
        self.btn_agregar.place(x = 270, y = 400)       





# **********************************************************************************
# **********************************  Salarios *************************************
# **********************************************************************************

class Salarios(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Gastos Salarios")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas() 

        self.tabla = ttk.Treeview(self, columns = ("Fecha","Concepto", "Monto"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")
        self.tabla.column("Concepto", width = 400, anchor="center")
        self.tabla.column("Monto", width = 75, anchor="center")        

        self.tabla.place(x = 50, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Concepto", text = "Concepto", anchor="center")
        self.tabla.heading("Monto", text = "Monto", anchor="center")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def escoger_concepto(event): 
            global concepto_salario

            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                    
                concepto_salario = self.tabla.item(item, "values")[1] 

            self.texto_buscador_nombre.delete(0,END)
            self.texto_buscador_nombre.insert(0,concepto_salario)

            llenar_tabla(True)

        self.tabla.bind("<Double-1>", escoger_concepto)


        def llenar_tabla(event):
            try:
                self.tabla.delete(*self.tabla.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                    sql = f""" SELECT * FROM salarios WHERE `Concepto` LIKE '%{self.texto_buscador_nombre.get()}%' """

                else:
                    sql = f""" SELECT * FROM salarios WHERE `Concepto` LIKE '%{self.texto_buscador_nombre.get()}%' and `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """

                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],))  
            except:
                error = messagebox.showerror("Error","No se pudo actualizar la tabla")

        self.label_fechas = CTkLabel(self,text="---------- Control de fechas ----------")
        self.label_fechas.place(x=750,y=80) 

        self.texto_fecha_inicial = CTkEntry(self,placeholder_text="Fecha inicial ...")
        self.texto_fecha_inicial.place(x=750,y=120) 

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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_inicial = CTkButton(self,text="...",command=fecha_inicial, width = 27, height = 27)
        self.btn_fecha_inicial.place(x=900 ,y=120 )

        self.texto_fecha_final = CTkEntry(self,placeholder_text="Fecha final ...")
        self.texto_fecha_final.place(x=750,y=160) 

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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_fecha_final = CTkButton(self,text="...",command=fecha_final, width = 27, height = 27)
        self.btn_fecha_final.place(x=900 ,y=160 )

        self.label_buscador = CTkLabel(self,text="---------- Buscador ----------")
        self.label_buscador.place(x=750,y=220)        

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por Concepto ...")
        self.texto_buscador_nombre.place(x=750,y=260) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla )  

        llenar_tabla(True)

        def agregar():
            temp = CTkToplevel()
            temp.title("Agregar") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False))  
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

            trabajadores = []
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM `trabajadores` """
            cursor.execute(sql)
            for index in cursor:
                trabajadores.append(index[0])

            temp.texto_trabajador = CTkComboBox(temp, values=trabajadores,width=300)
            temp.texto_trabajador.set("Escoge Trabajador ...")
            temp.texto_trabajador.pack(pady = 5)

            temp.texto_monto = CTkEntry(temp, placeholder_text="Monto ...",width=250)
            temp.texto_monto.pack(pady = 5)

            def cambio_moneda():
                vent = CTkToplevel()
                vent.title("Cambio de Moneda") 
                htotal = vent.winfo_screenheight()
                wtotal = vent.winfo_screenwidth()
                wventana = 300
                hventana = 300
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                vent.geometry(f"+{posx}+{posy}")
                vent.lift()
                vent.attributes('-topmost', True)
                vent.after(200, lambda: vent.attributes('-topmost', False)) 
                vent.after(250, lambda: vent.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                tar1 = 0           
                tar2 = 0           
                tar3 = 0 

                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = """SELECT * FROM `tarifas`;"""
                cursor.execute(sql)
                for index in cursor:
                    tar1 = index[0]
                    tar2 = index[1]
                    tar3 = index[2]

                tarifa = f"Tarifa:  1USD = {tar1}CUP,  1EUR = {tar2}CUP, 1EUR = {tar3}CUP"                      

                vent.label_tarifa = CTkLabel(vent,text=tarifa, font=("Times New Roman",16))
                vent.label_tarifa.pack(pady=10)

                vent.texto_cup = CTkEntry(vent, placeholder_text="CUP ...")
                vent.texto_cup.pack(pady=5)

                vent.texto_eur = CTkEntry(vent, placeholder_text="EUR ...")
                vent.texto_eur.pack(pady=5)

                def cambiar():
                    if vent.texto_cup.get() == "" and vent.texto_eur.get() == "":
                        error = messagebox.showerror("Error", "Debes escribir en algun campo la cantidad a cambiar")

                    elif vent.texto_cup.get() != "" and vent.texto_eur.get() != "":
                        error = messagebox.showerror("Error", "Debes escribir solo en un campo, no en ambos")

                    else:
                        if vent.texto_cup.get() != "":
                            temp.texto_monto.delete(0,END)
                            resultado = round(float(vent.texto_cup.get())/tar1,2)
                            temp.texto_monto.insert(0,resultado)
                            vent.destroy()

                        else:
                            temp.texto_monto.delete(0,END)
                            resultado = round(float(vent.texto_eur.get())*tar3,2)
                            temp.texto_monto.insert(0,resultado)
                            vent.destroy()


                vent.btn_cambiar = CTkButton(vent, text="Cambiar", command=cambiar)
                vent.btn_cambiar.pack(pady=10)  

            temp.btn_cambio = CTkButton(temp, text="Cambiar",command=cambio_moneda)
            temp.btn_cambio.pack()

            def aceptar_salario():
                try:
                    conf = messagebox.askokcancel("Confirmar","Se va a agregar el gasto")
                    if conf:
                        # primero encontrar el id que le vamos a dar al gasto asociado
                        id_salario = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = """SELECT MAX(Id) FROM `salarios`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass

                            else:
                                id_salario = index[0] + 1  


                        # agregar el gasto asociado a la bd
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `salarios`(`Id`, `Fecha`, `Concepto`, `Monto`) VALUES ('{id_salario}','{fecha_actual}','{temp.texto_trabajador.get()}','{temp.texto_monto.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla(True)
                        temp.destroy()

                except:
                    error = messagebox.showerror("Error","No se pudo agregar el salario")

            temp.btn = CTkButton(temp, text="Aceptar Salario", command=aceptar_salario)
            temp.btn.pack(pady = 10)

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 500, height = 50)
        self.btn_agregar.place(x = 50, y = 450) 

        # ahora eliminar un salario

        def double_click(event):            
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                id_salario = self.tabla.item(item, "text") 

            conf = messagebox.askokcancel("Confirmar","Se va a eliminar") 
            if conf:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = f""" DELETE FROM `salarios` WHERE `Id` = "{id_salario}" """
                cursor.execute(sql)
                conn.commit()

                llenar_tabla(True)              

        self.tabla.bind("<Double-1>", double_click)

        
        

# **********************************************************************************
# ************************************  Almacen ************************************
# **********************************************************************************

class Almacen(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Almacen")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Costo Usd", "Precio", "Cantidad", "Categoria", "Minimo"))
        self.tabla.column("#0", width = 75)
        self.tabla.column("Nombre", width = 200)
        self.tabla.column("Costo Usd", width = 100)
        self.tabla.column("Precio", width = 75)
        self.tabla.column("Cantidad", width = 75)
        self.tabla.column("Categoria", width = 100)
        self.tabla.column("Minimo", width = 75)

        self.tabla.place(x = 50, y = 200)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Costo Usd", text = "Costo Usd")
        self.tabla.heading("Precio", text = "Precio")
        self.tabla.heading("Cantidad", text = "Cantidad")
        self.tabla.heading("Categoria", text = "Categoria")
        self.tabla.heading("Minimo", text = "Minimo")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        # vamos a mostrar el equivalente en dinero a los productos que hay en almacen
        string = StringVar() 
        string.set("En Almacen:")        

        def alctualizar_equivalencia():
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = f""" SELECT SUM(`CostoUsd`*`Cantidad`) FROM `productos`; """
            cursor.execute(sql)
            for index in cursor:
                string.set("En Almacen: " + f"{index[0]} " + "USD")

        alctualizar_equivalencia()

        self.label_equivalente = CTkLabel(self,textvariable = string)
        self.label_equivalente.place(x=700,y=50)

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM productos WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%' ORDER BY `Codigo` ASC; """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],index[6],))         

        # vamos a hacer un buscador 

        self.label_buscador = CTkLabel(self,text="------------------------------ Buscador ------------------------------")
        self.label_buscador.place(x=50,y=50)


        self.texto_buscador_codigo = CTkEntry(self,placeholder_text="Buscar por codigo ...")
        self.texto_buscador_codigo.place(x=50,y=90)          

        self.texto_buscador_codigo.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por nombre ...")
        self.texto_buscador_nombre.place(x=200,y=90) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla) 

        def doble_click(event):
            global codigo_almacen
            global nombre_almacen
            # vamos a capturar el codigo del producto
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                codigo_almacen = self.tabla.item(item, "text") 
                nombre_almacen = self.tabla.item(item, "values")[0]


            # vamos a crear la ventana modal
            temp = CTkToplevel()
            temp.title("Selección") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 200
            hventana = 200
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"200x200+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))  

            def modificar():
                root = CTkToplevel()
                root.title("Modificar") 
                htotal = root.winfo_screenheight()
                wtotal = root.winfo_screenwidth()
                wventana = 1000
                hventana = 600
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                root.geometry(f"+{posx}+{posy}")
                root.geometry("1000x600") 
                root.lift()
                root.attributes('-topmost', True)
                root.after(200, lambda: root.attributes('-topmost', False)) 
                root.after(250, lambda: root.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                ############ agregar el fondo de pantalla #########
      
                root.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (600,600))  

                root.label_image = CTkLabel(root, image = root.imagen, text = "")  
                root.label_image.place(x = 0, y = 0)      

                #######################################################   

                # ************************** Labels *************************              

                root.label_nombre = CTkLabel(root,text="Nombre:", font=("Times New Roman",16))
                root.label_nombre.place(x = 630, y = 70) 
                
                root.texto_nombre = CTkEntry(root)
                root.texto_nombre.place(x = 750, y = 70)       

                root.label_costo_usd = CTkLabel(root,text="Costo Usd:", font=("Times New Roman",16))
                root.label_costo_usd.place(x = 630, y = 110)  

                root.texto_costo_usd = CTkEntry(root)
                root.texto_costo_usd.place(x = 750, y = 110) 

                def cambio():
                    vent = CTkToplevel()
                    vent.title("Cambio de Moneda") 
                    htotal = vent.winfo_screenheight()
                    wtotal = vent.winfo_screenwidth()
                    wventana = 300
                    hventana = 300
                    posx = round(wtotal/2-wventana/2)
                    posy = round(htotal/2-hventana/2)
                    vent.geometry(f"+{posx}+{posy}")
                    vent.lift()
                    vent.attributes('-topmost', True)
                    vent.after(200, lambda: vent.attributes('-topmost', False)) 
                    vent.after(250, lambda: vent.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                    tar1 = 0           
                    tar2 = 0           
                    tar3 = 0 

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()

                    sql = """SELECT * FROM `tarifas`;"""
                    cursor.execute(sql)
                    for index in cursor:
                        tar1 = index[0]
                        tar2 = index[1]
                        tar3 = index[2]

                    tarifa = f"Tarifa:  1USD = {tar1}CUP,  1EUR = {tar2}CUP, 1EUR = {tar3}CUP"                      

                    vent.label_tarifa = CTkLabel(vent,text=tarifa, font=("Times New Roman",16))
                    vent.label_tarifa.pack(pady=10)

                    vent.texto_cup = CTkEntry(vent, placeholder_text="CUP ...")
                    vent.texto_cup.pack(pady=5)

                    vent.texto_eur = CTkEntry(vent, placeholder_text="EUR ...")
                    vent.texto_eur.pack(pady=5)

                    def cambiar():
                        if vent.texto_cup.get() == "" and vent.texto_eur.get() == "":
                            error = messagebox.showerror("Error", "Debes escribir en algun campo la cantidad a cambiar")

                        elif vent.texto_cup.get() != "" and vent.texto_eur.get() != "":
                            error = messagebox.showerror("Error", "Debes escribir solo en un campo, no en ambos")

                        else:
                            if vent.texto_cup.get() != "":
                                root.texto_costo_usd.delete(0,END)
                                resultado = round(float(vent.texto_cup.get())/tar1,2)
                                root.texto_costo_usd.insert(0,resultado)
                                vent.destroy()

                            else:
                                root.texto_costo_usd.delete(0,END)
                                resultado = round(float(vent.texto_eur.get())*tar3,2)
                                root.texto_costo_usd.insert(0,resultado)
                                vent.destroy()


                    vent.btn_cambiar = CTkButton(vent, text="Cambiar", command=cambiar)
                    vent.btn_cambiar.pack(pady=10)           

                root.btn_cambio = CTkButton(root,text="...", width=30,command=cambio)      
                root.btn_cambio.place(x = 900, y = 110) 

                root.label_precio = CTkLabel(root,text="Precio:", font=("Times New Roman",16))
                root.label_precio.place(x = 630, y = 150)  

                root.texto_precio = CTkEntry(root)
                root.texto_precio.place(x = 750, y = 150)   

                root.label_cantidad = CTkLabel(root,text="Cantidad:", font=("Times New Roman",16))
                root.label_cantidad.place(x = 630, y = 190)  

                root.texto_cantidad = CTkEntry(root)
                root.texto_cantidad.place(x = 750, y = 190)                 

                root.label_categoria = CTkLabel(root,text="Categoria:", font=("Times New Roman",16))
                root.label_categoria.place(x = 630, y = 230)  

                categorias = []
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = """SELECT * FROM `categorias`;"""
                cursor.execute(sql)
                for index in cursor:
                    categorias.append(index[0])

                root.texto_categoria = CTkComboBox(root, values=categorias)
                root.texto_categoria.set("...")
                root.texto_categoria.place(x = 750, y = 230)

                root.label_minimo = CTkLabel(root,text="Minimo:", font=("Times New Roman",16))
                root.label_minimo.place(x = 630, y = 270)  

                root.texto_minimo = CTkEntry(root)
                root.texto_minimo.place(x = 750, y = 270) 

                # vamos a llenar los campos con la info que ya existe en la base de datos
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `productos` WHERE `Codigo` = "{codigo_almacen}" """
                cursor.execute(sql)
                for index in cursor:                                        
                    root.texto_nombre.insert(0,index[1]) 
                    root.texto_costo_usd.insert(0,index[2])
                    root.texto_cantidad.insert(0,index[4])                    
                    root.texto_categoria.set(index[5])
                    root.texto_minimo.insert(0,index[6]) 
                    root.texto_precio.insert(0,index[3]) 


                def modificar_producto():
                    try:
                        conf = messagebox.askokcancel("Confirmar","Vamos a modificar el producto en la base de datos")
                        if conf:                            
                            # modificar el producto en la bd 
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "lilly",
                                password = "123456",
                                database = "lilly"
                                )
                            cursor = conn.cursor()                    

                            sql = f""" UPDATE `productos` SET `Codigo`='{root.texto_codigo.get()}',`Nombre`='{root.texto_nombre.get()}',`CostoUsd`='{root.texto_costo_usd.get()}',`Precio`='{root.texto_precio.get()}',`Cantidad`='{root.texto_cantidad.get()}',`Categoria`='{root.texto_categoria.get()}',`Minimo`='{root.texto_minimo.get()}' WHERE `Codigo` = "{codigo_almacen}";"""
                            cursor.execute(sql)
                            conn.commit()                           

                            completado = messagebox.showinfo("Completado","Se modifico el producto")

                            llenar_tabla(True)
                            alctualizar_equivalencia()
                            root.destroy()
                            temp.destroy()

                    except:
                        error = messagebox.showerror("Error","No se ha podido modificar el producto")

                root.btn_modificar = CTkButton(root,text="Modificar",command=modificar_producto, width = 150, height = 40)
                root.btn_modificar.place(x=650 ,y=500 )

            temp.btn_modificar = CTkButton(temp,text="Modificar", command=modificar)
            temp.btn_modificar.pack(pady=20)   

            def eliminar():
                string = f"Vamos a eliminar el producto: {nombre_almacen}"
                conf = messagebox.askokcancel("Confirmar",string)
                if conf:
                    try:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = f""" DELETE FROM `productos` WHERE `Codigo` = "{codigo_almacen}" """
                        cursor.execute(sql)
                        conn.commit()

                        alctualizar_equivalencia()
                        llenar_tabla(True)
                        temp.destroy()
                    
                    except:
                        error = messagebox.showerror("Error","No se pudo eliminar el producto")

            temp.btn_eliminar = CTkButton(temp,text="Eliminar", command=eliminar)
            temp.btn_eliminar.pack(pady=20) 



        self.tabla.bind("<Double-1>", doble_click)  

        llenar_tabla(True)


# **********************************************************************************
# *****************************  Consulta Salarios **********************************
# **********************************************************************************

class ConsultaSalarios(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Consulta Salarios")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas() 

        self.tabla = ttk.Treeview(self, columns = ("Fecha","Concepto", "Monto"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")
        self.tabla.column("Concepto", width = 400, anchor="center")
        self.tabla.column("Monto", width = 75, anchor="center")        

        self.tabla.place(x = 20, y = 100)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Concepto", text = "Concepto", anchor="center")
        self.tabla.heading("Monto", text = "Monto", anchor="center")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def escoger_concepto(event): 
            global concepto_salario

            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                    
                concepto_salario = self.tabla.item(item, "values")[1] 

            self.texto_buscador_nombre.delete(0,END)
            self.texto_buscador_nombre.insert(0,concepto_salario)

            llenar_tabla(True)

        self.tabla.bind("<Double-1>", escoger_concepto)


        def llenar_tabla(event):
            try:
                self.tabla.delete(*self.tabla.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                    sql = f""" SELECT * FROM salarios WHERE `Concepto` LIKE '%{self.texto_buscador_nombre.get()}%' """

                else:
                    sql = f""" SELECT * FROM salarios WHERE `Concepto` LIKE '%{self.texto_buscador_nombre.get()}%' and `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """

                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],))  
            except:
                error = messagebox.showerror("Error","No se pudo actualizar la tabla")

        self.label_fechas = CTkLabel(self,text="---------- Control de fechas ----------")
        self.label_fechas.place(x=750,y=80) 

        self.texto_fecha_inicial = CTkEntry(self,placeholder_text="Fecha inicial ...")
        self.texto_fecha_inicial.place(x=750,y=120) 

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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_inicial = CTkButton(self,text="...",command=fecha_inicial, width = 27, height = 27)
        self.btn_fecha_inicial.place(x=900 ,y=120 )

        self.texto_fecha_final = CTkEntry(self,placeholder_text="Fecha final ...")
        self.texto_fecha_final.place(x=750,y=160) 

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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_fecha_final = CTkButton(self,text="...",command=fecha_final, width = 27, height = 27)
        self.btn_fecha_final.place(x=900 ,y=160 )

        self.label_buscador = CTkLabel(self,text="---------- Buscador ----------")
        self.label_buscador.place(x=750,y=220)        

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por Concepto ...")
        self.texto_buscador_nombre.place(x=750,y=260) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla )  

        llenar_tabla(True)




# **********************************************************************************
# *****************************  Consulta Asociados ********************************
# **********************************************************************************

class ConsultaAsociados(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Consulta Asociados")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas() 

        self.tabla = ttk.Treeview(self, columns = ("Fecha","Concepto", "Monto"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")
        self.tabla.column("Concepto", width = 400, anchor="center")
        self.tabla.column("Monto", width = 75, anchor="center")        

        self.tabla.place(x = 20, y = 100)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Concepto", text = "Concepto", anchor="center")
        self.tabla.heading("Monto", text = "Monto", anchor="center")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def escoger_concepto(event): 
            global concepto_asociado

            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                    
                concepto_asociado = self.tabla.item(item, "values")[1] 

            self.texto_buscador_nombre.delete(0,END)
            self.texto_buscador_nombre.insert(0,concepto_asociado)

            llenar_tabla(True)

        self.tabla.bind("<Double-1>", escoger_concepto)


        def llenar_tabla(event):
            try:
                self.tabla.delete(*self.tabla.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                    sql = f""" SELECT * FROM asociados WHERE `Concepto` LIKE '%{self.texto_buscador_nombre.get()}%' """

                else:
                    sql = f""" SELECT * FROM asociados WHERE `Concepto` LIKE '%{self.texto_buscador_nombre.get()}%' and `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """

                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],))  
            except:
                error = messagebox.showerror("Error","No se pudo actualizar la tabla")

        self.label_fechas = CTkLabel(self,text="---------- Control de fechas ----------")
        self.label_fechas.place(x=750,y=80) 

        self.texto_fecha_inicial = CTkEntry(self,placeholder_text="Fecha inicial ...")
        self.texto_fecha_inicial.place(x=750,y=120) 

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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_inicial = CTkButton(self,text="...",command=fecha_inicial, width = 27, height = 27)
        self.btn_fecha_inicial.place(x=900 ,y=120 )

        self.texto_fecha_final = CTkEntry(self,placeholder_text="Fecha final ...")
        self.texto_fecha_final.place(x=750,y=160) 

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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_fecha_final = CTkButton(self,text="...",command=fecha_final, width = 27, height = 27)
        self.btn_fecha_final.place(x=900 ,y=160 )

        self.label_buscador = CTkLabel(self,text="---------- Buscador ----------")
        self.label_buscador.place(x=750,y=220)        

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por Concepto ...")
        self.texto_buscador_nombre.place(x=750,y=260) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla )  

        llenar_tabla(True)




# **********************************************************************************
# ***********************************  Ventas **************************************
# **********************************************************************************

class Ventas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Ventas")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1200
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1200x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (1200,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas()  

        # *************** Seccion de la tabla productos      

        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Costo USD", "Precio", "Cantidad", "Categoria"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Nombre", width = 200, anchor="center")
        self.tabla.column("Costo USD", width = 75, anchor="center")
        self.tabla.column("Precio", width = 75, anchor="center")
        self.tabla.column("Cantidad", width = 75, anchor="center")
        self.tabla.column("Categoria", width = 100, anchor="center")

        self.tabla.place(x = 40, y = 120)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Codigo", anchor="center")
        self.tabla.heading("Nombre", text = "Nombre", anchor="center")
        self.tabla.heading("Costo USD", text = "Costo USD", anchor="center")
        self.tabla.heading("Precio", text = "Precio", anchor="center")
        self.tabla.heading("Cantidad", text = "Cantidad", anchor="center")
        self.tabla.heading("Categoria", text = "Categoria", anchor="center")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def actualizar_productos(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()           
            sql = f""" SELECT * FROM productos WHERE `Nombre` LIKE '%{self.texto_buscador.get()}%' """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],)) 


        # ***************** buscador 
        self.texto_buscador = CTkEntry(self, width=200)     
        self.texto_buscador.place(x=45,y=50)  

        self.texto_buscador.bind("<KeyRelease>", actualizar_productos) 

        actualizar_productos(True)


        # ********************** seccion carrito 
        self.tabla_carrito = ttk.Treeview(self, columns = ("Nombre", "Costo USD", "Precio", "Cantidad", "Categoria"), show="headings")
        self.tabla_carrito.column("#0", width = 100, anchor="center")
        self.tabla_carrito.column("Nombre", width = 200, anchor="center")
        self.tabla_carrito.column("Costo USD", width = 75, anchor="center")
        self.tabla_carrito.column("Precio", width = 75, anchor="center")
        self.tabla_carrito.column("Cantidad", width = 75, anchor="center")
        self.tabla_carrito.column("Categoria", width = 100, anchor="center")

        self.tabla_carrito.place(x = 620, y = 120)        
        self.tabla_carrito.config(height = 10)

        self.tabla_carrito.heading("#0", text = "Codigo", anchor="center")
        self.tabla_carrito.heading("Nombre", text = "Nombre", anchor="center")
        self.tabla_carrito.heading("Costo USD", text = "Costo USD", anchor="center")
        self.tabla_carrito.heading("Precio", text = "Precio", anchor="center")
        self.tabla_carrito.heading("Cantidad", text = "Cantidad", anchor="center")
        self.tabla_carrito.heading("Categoria", text = "Categoria", anchor="center")

        scrollbar2 = CTkScrollbar(self, command = self.tabla_carrito.yview, width = 18)
        scrollbar2.place(in_ = self.tabla_carrito, relheigh = 1, relx = 1)

        self.tabla_carrito.config(yscrollcommand = scrollbar2.set)

        def actualizar_carrito(event):            
            self.tabla_carrito.delete(*self.tabla_carrito.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()           
            sql = f""" SELECT * FROM carrito """
            cursor.execute(sql)
            for index in cursor:
                self.tabla_carrito.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],)) 

        # ******************* hagamos el label del total, costo y ganancia
        self.label_total1 = CTkLabel(self,text = "Precio: ")
        self.label_total1.place(x=650,y = 430)
        
        total = StringVar()
        total.set("0")

        self.label_total = CTkLabel(self,textvariable = total)
        self.label_total.place(x=800,y = 430)

        self.label_costo = CTkLabel(self,text = "Costo: ")
        self.label_costo.place(x=650,y = 470)
        
        costo = StringVar()
        costo.set("0")

        self.label_costo = CTkLabel(self,textvariable = costo)
        self.label_costo.place(x=800,y = 470)

        self.label_ganancia = CTkLabel(self,text = "Ganancia: ")
        self.label_ganancia.place(x=650,y = 510)
        
        ganancia = StringVar()
        ganancia.set("0")

        self.label_ganancia = CTkLabel(self,textvariable = ganancia)
        self.label_ganancia.place(x=800,y = 510)

        def actualizar_total():
            # mostremos el total en el label que esta debajo
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()           
            sql = f""" SELECT SUM(`Precio`*`Cantidad`) FROM `carrito` """
            cursor.execute(sql)
            for index in cursor:
                if index[0] is None:
                    total.set("0") 
                    num_total = 0    
                else:
                    total.set(round(index[0],2)) 
                    num_total = index[0]            
            
            # -------------------------------------------

            # mostremos el costo en el label que esta debajo
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()           
            sql = f""" SELECT SUM(`CostoUsd`*`Cantidad`) FROM `carrito` """
            cursor.execute(sql)
            for index in cursor:
                if index[0] is None:
                    costo.set("0") 
                    num_costo = 0    
                else:
                    costo.set(round(index[0],2)) 
                    num_costo = index[0]               

            # -------------------------------------------- 
            # ahora mostremos la ganancia
            ganancia.set(round(num_total - num_costo,2)) 


        def limpiar_carrito():
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()           
            sql = f""" DELETE FROM `carrito` """
            cursor.execute(sql)
            conn.commit()

        # ********************** ahora vamos a mandar productos al carrito
        def mandar_al_carrito(event):
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                    
                cod = self.tabla.item(item, "text")
                values = self.tabla.item(item, "values")

            # vamos a crear una ventana para poner la cantidad que voy a comprar
            temp = CTkToplevel()
            temp.title("Al Carrito") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 300
            hventana = 300
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False))  
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

            temp.texto_cantidad = CTkEntry(temp, placeholder_text="Cantidad ...")
            temp.texto_cantidad.pack(pady = 10)

            def aceptar():
                # verifiquemos que no sobrevendas un producto
                alcansa = True
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()           
                sql = f""" SELECT `Cantidad` FROM `productos` WHERE `Codigo` = {cod} """
                cursor.execute(sql)
                for index in cursor:
                    if index[0] >= float(temp.texto_cantidad.get()):
                        pass                    
                    else:
                        alcansa = False
                        error = messagebox.showerror("Error","No tienes esa cantidad en almacen")
                        temp.destroy()

                if alcansa:
                    if temp.texto_cantidad.get() == "":
                        error = messagebox.showerror("Error","Debes escribir alguna cantidad")
                    
                    else:                    
                        conf = messagebox.askokcancel("Confirmar","Vas a mandar el producto al carrito")
                        if conf:
                            # hay que verificar si es un producto que ya estaba en el carrito o no para agregarlo o aumentarle la cantidad
                            esta = False
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "lilly",
                                password = "123456",
                                database = "lilly"
                                )
                            cursor = conn.cursor()           
                            sql = f""" SELECT `Codigo` FROM `carrito`  """
                            cursor.execute(sql)
                            for index in cursor:
                                if index[0] == cod:
                                    esta = True
                                    break

                            if esta:
                                # ***************************** aumentemos la cantidad del producto en el carrito 
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "lilly",
                                    password = "123456",
                                    database = "lilly"
                                    )
                                cursor = conn.cursor()           
                                sql = f""" UPDATE `carrito` SET `Cantidad`= `Cantidad` + '{temp.texto_cantidad.get()}' WHERE `Codigo` = {cod} """
                                cursor.execute(sql)
                                conn.commit()


                                # ***************************** ahora descontamos la cantidad del almacen 
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "lilly",
                                    password = "123456",
                                    database = "lilly"
                                    )
                                cursor = conn.cursor()           
                                sql = f""" UPDATE `productos` SET `Cantidad`= `Cantidad` - '{temp.texto_cantidad.get()}' WHERE `Codigo` = {cod} """
                                cursor.execute(sql)
                                conn.commit()                                

                                # ******************************* actualizaciones
                                actualizar_productos(True)
                                actualizar_carrito(True)
                                actualizar_total()

                                temp.destroy()

                            else:
                                # ************************* primero lo mandamos a la tabla carrito a la bd 
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "lilly",
                                    password = "123456",
                                    database = "lilly"
                                    )
                                cursor = conn.cursor()           
                                sql = f""" INSERT INTO `carrito`(`Codigo`, `Nombre`, `CostoUsd`, `Precio`, `Cantidad`, `Categoria`) VALUES ('{cod}','{values[0]}','{values[1]}','{values[2]}','{temp.texto_cantidad.get()}','{values[4]}') """
                                cursor.execute(sql)
                                conn.commit()

                                # ***************************** ahora descontamos la cantidad del almacen 
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "lilly",
                                    password = "123456",
                                    database = "lilly"
                                    )
                                cursor = conn.cursor()           
                                sql = f""" UPDATE `productos` SET `Cantidad`= `Cantidad` - '{temp.texto_cantidad.get()}' WHERE `Codigo` = {cod} """
                                cursor.execute(sql)
                                conn.commit()                            

                                # ******************************* actualizaciones
                                actualizar_productos(True)
                                actualizar_carrito(True)
                                actualizar_total()

                                temp.destroy()



            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)


        self.tabla.bind("<Double-1>", mandar_al_carrito)


        def devolver(codigo,cantidad):
            # devolver el producto al almacen
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()           
            sql = f""" UPDATE `productos` SET `Cantidad`= `Cantidad` + '{cantidad}' WHERE `Codigo` = {codigo} """
            cursor.execute(sql)
            conn.commit()

            # quitar el producto del carrito
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()           
            sql = f""" DELETE FROM `carrito` WHERE `Codigo` = {codigo} """
            cursor.execute(sql)
            conn.commit()           


        def cancelar_producto(event):
            seleccion = self.tabla_carrito.selection()
            if seleccion:
                item = seleccion[0]                    
                cod = self.tabla_carrito.item(item, "text")                
                cant = self.tabla_carrito.item(item, "values")[3]                              

            conf = messagebox.askokcancel("Confirmar","Se va a devolver el producto al almacen")
            if conf:
                # devolver el producto
                devolver(cod,cant)

            # actualizar las tablas
            actualizar_carrito(True)
            actualizar_productos(True)
            actualizar_total()

        self.tabla_carrito.bind("<Double-1>", cancelar_producto)

        def vaciar_carrito():            
            # haremos un listado de los codigos de los productos y los iremos devolviendo todos 
            productos = []
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()           
            sql = f""" SELECT `Codigo`, `Cantidad` FROM `carrito`  """
            cursor.execute(sql)
            for index in cursor:
                productos.append([index[0],index[1]])

            for prod in productos:
                devolver(prod[0],prod[1])


            # actualizar las tablas
            actualizar_carrito(True)
            actualizar_productos(True)
            actualizar_total()

        def vaciar():
            conf = messagebox.askokcancel("Confirmar","Se va a vaciar el carrito")
            if conf:
                vaciar_carrito()


        imagen_vaciar = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/cesta2.jpg"), size = (150,75)) 

        self.buttom_vaciar = CTkButton(self, text="",image=imagen_vaciar, command=vaciar)
        self.buttom_vaciar.place(x=800,y=30)

        vaciar_carrito()

        # ******************* ahora regalar los productos del carrito
        def regalar():
            # si el carrito esta vacio no deberia hac nada 
            vacio = False
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()           
            sql = f""" SELECT COUNT(`Codigo`) FROM `carrito` """
            cursor.execute(sql)
            for index in cursor:
                if index[0] == 0:
                    vacio = True

            if vacio:
                info = messagebox.showinfo("Vacio","El carrito esta vacio")

            else:
                # hagamos ventana modal para agregar el concepto
                temp = CTkToplevel()
                temp.title("Regalar") 
                htotal = temp.winfo_screenheight()
                wtotal = temp.winfo_screenwidth()
                wventana = 300
                hventana = 300
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                temp.geometry(f"+{posx}+{posy}")
                temp.lift()
                temp.attributes('-topmost', True)
                temp.after(200, lambda: temp.attributes('-topmost', False)) 
                temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                temp.texto_concepto = CTkEntry(temp, placeholder_text="Concepto ...", width=200)
                temp.texto_concepto.pack(pady=5)

                def aceptar():
                    conf = messagebox.askokcancel("Confirmar","Se van a regalar los productos del carrito")
                    if conf:
                        # hallemos el id del regalo
                        id_regalo = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = """SELECT MAX(Id) FROM `regalos`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass
                            else:
                                id_regalo = index[0] + 1 

                        # hacemos listado con los productos del carrito 
                        productos  = []
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()           
                        sql = f""" SELECT * FROM `carrito` """
                        cursor.execute(sql)
                        for index in cursor:
                            productos.append([index[0],index[1],index[2],index[3],index[4],index[5]])

                        # agregamos todos los productos a la tabla regalos
                        for prod in productos:
                            # agregamos los productos 
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "lilly",
                                password = "123456",
                                database = "lilly"
                                )
                            cursor = conn.cursor()           
                            sql = f""" INSERT INTO `regalos`(`Id`, `Fecha`, `Codigo`, `Nombre`, `CostoUsd`, `Precio`, `Cantidad`, `Categoria`, `Concepto`) VALUES ('{id_regalo}','{fecha_actual}','{prod[0]}','{prod[1]}','{prod[2]}','{prod[3]}','{prod[4]}','{prod[5]}','{temp.texto_concepto.get()}') """
                            cursor.execute(sql)
                            conn.commit()

                        # limpiamos el carrito
                        limpiar_carrito()

                        # actualizar las tablas
                        actualizar_carrito(True)
                        actualizar_productos(True)
                        actualizar_total()
                        temp.destroy()

                temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
                temp.btn.pack(pady = 10)

        imagen_regalar = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/regalo.jpg"), size = (150,75)) 

        self.btn_regalar = CTkButton(self,image=imagen_regalar,command=regalar, text="", width=150, height=75)
        self.btn_regalar.place(x=100,y=450)


        def vender():
            # si el carrito esta vacio no deberia hacer nada 
            vacio = False
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()           
            sql = f""" SELECT COUNT(`Codigo`) FROM `carrito` """
            cursor.execute(sql)
            for index in cursor:
                if index[0] == 0:
                    vacio = True

            if vacio:
                info = messagebox.showinfo("Vacio","El carrito esta vacio")

            else:
                # hagamos ventana modal para agregar los que envian y reciben
                temp = CTkToplevel()
                temp.title("Regalar") 
                htotal = temp.winfo_screenheight()
                wtotal = temp.winfo_screenwidth()
                wventana = 300
                hventana = 300
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                temp.geometry(f"+{posx}+{posy}")
                temp.lift()
                temp.attributes('-topmost', True)
                temp.after(200, lambda: temp.attributes('-topmost', False)) 
                temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                # ************************ envia 

                temp.label_envia = CTkLabel(temp, text="---------- Envia ----------")
                temp.label_envia.pack(pady=5)                

                temp.texto_envia = CTkEntry(temp,width=200,placeholder_text="Envia...")                
                temp.texto_envia.pack(pady=5)

                # ahora mostrar opciones cuando escribo
                def opciones_envia(event):
                    global vent_envian
                    try:
                        vent_envian.destroy()
                        vent_envian = None
                    except:
                        pass
                    
                    # mostraremos una ventana con los nombres y al dar 2ble click se agreara la persona 
                    vent_envian = CTkToplevel()
                    vent_envian.title("Regalar") 
                    htotal = vent_envian.winfo_screenheight()
                    wtotal = vent_envian.winfo_screenwidth()
                    wventana = 550
                    hventana = 300
                    posx = round(wtotal/2-wventana/2)
                    posy = round(htotal/2-hventana/2)
                    vent_envian.geometry(f"+{posx}+{posy}")
                    vent_envian.lift()
                    vent_envian.attributes('-topmost', True)
                    vent_envian.after(200, lambda: vent_envian.attributes('-topmost', False)) 
                    vent_envian.after(250, lambda: vent_envian.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                    tabla_envian = ttk.Treeview(vent_envian)
                    tabla_envian.column("#0", width = 100, anchor="center")                    

                    tabla_envian.pack(pady=5)                    

                    tabla_envian.heading("#0", text = "Nombre", anchor="center")                    

                    scrollbar3 = CTkScrollbar(vent_envian, command = tabla_envian.yview, width = 18)
                    scrollbar3.place(in_ = tabla_envian, relheigh = 1, relx = 1)

                    tabla_envian.config(yscrollcommand = scrollbar3.set)

                    # ahora llenar la tabla 
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()           
                    sql = f""" SELECT `Nombre` FROM `envia` WHERE `Nombre` LIKE '%{temp.texto_envia.get()}%'; """
                    cursor.execute(sql)
                    for index in cursor:                        
                        tabla_envian.insert("",END, text = index[0],)

                    # ahora al dar 2ble click se escribira el nombre en el campo
                    def escribir_envia(event):
                        global vent_envian
                        
                        temp.texto_envia.delete(0,END)
                        seleccion = tabla_envian.selection()
                        if seleccion:
                            item = seleccion[0]                
                            envia = tabla_envian.item(item, "text") 

                        temp.texto_envia.insert(0,envia)
                        vent_envian.destroy()   
                        vent_envian = None                 
                        
                    tabla_envian.bind("<Double-1>", escribir_envia)              


                temp.texto_envia.bind("<KeyRelease>", opciones_envia) 

                def guardar_envia():
                    if temp.texto_envia.get() == "":
                        error = messagebox.showerror("Error","Debes agregar algun nombre para  poder guardar")

                    else:
                        conf = messagebox.askokcancel("Confirmacion", "Se va a agregar a la bd")
                        if conf:
                            id_envia = 1
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "lilly",
                                password = "123456",
                                database = "lilly"
                                )
                            cursor = conn.cursor()

                            sql = """SELECT MAX(Id) FROM `envia`;"""
                            cursor.execute(sql)
                            for index in cursor:
                                if index[0] == None:
                                    pass
                                else:
                                    id_envia = index[0] + 1 

                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "lilly",
                                password = "123456",
                                database = "lilly"
                                )
                            cursor = conn.cursor()           
                            sql = f""" INSERT INTO `envia`(`Id`, `Nombre`) VALUES ('{id_envia}','{temp.texto_envia.get()}') """
                            cursor.execute(sql)
                            conn.commit()

                            temp.texto_envia.set("")

                temp.btn_guardar_envia = CTkButton(temp, text="Guardar", command=guardar_envia)
                temp.btn_guardar_envia.pack(pady = 5)

                # **************************************** recibe

                temp.label_recibe = CTkLabel(temp, text="---------- Recibe ----------")
                temp.label_recibe.pack(pady=(30,5))                               

                temp.texto_recibe = CTkEntry(temp,width=200,placeholder_text="Recibe...")                             
                temp.texto_recibe.pack(pady=5)  

                temp.texto_direccion = CTkEntry(temp, placeholder_text="Direccion ...", width=200)
                temp.texto_direccion.pack(pady=5)

                temp.texto_telefono = CTkEntry(temp, placeholder_text="Telefono ...", width=200)
                temp.texto_telefono.pack(pady=5)

                # vamos a autocompletar el campo
                def opciones_recibe(event):
                    global vent_reciben
                    try:
                        vent_reciben.destroy()
                        vent_reciben = None
                    except:
                        pass
                    
                    # mostraremos una ventana con los nombres y al dar 2ble click se agreara la persona 
                    vent_reciben = CTkToplevel()
                    vent_reciben.title("Regalar") 
                    htotal = vent_reciben.winfo_screenheight()
                    wtotal = vent_reciben.winfo_screenwidth()
                    wventana = 550
                    hventana = 300
                    posx = round(wtotal/2-wventana/2)
                    posy = round(htotal/2-hventana/2)
                    vent_reciben.geometry(f"+{posx}+{posy}")
                    vent_reciben.lift()
                    vent_reciben.attributes('-topmost', True)
                    vent_reciben.after(200, lambda: vent_reciben.attributes('-topmost', False)) 
                    vent_reciben.after(250, lambda: vent_reciben.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                    tabla_reciben = ttk.Treeview(vent_reciben)
                    tabla_reciben.column("#0", width = 100, anchor="center")                    

                    tabla_reciben.pack(pady=5)                    

                    tabla_reciben.heading("#0", text = "Nombre", anchor="center")                    

                    scrollbar3 = CTkScrollbar(vent_reciben, command = tabla_reciben.yview, width = 18)
                    scrollbar3.place(in_ = tabla_reciben, relheigh = 1, relx = 1)

                    tabla_reciben.config(yscrollcommand = scrollbar3.set)

                    # ahora llenar la tabla 
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()           
                    sql = f""" SELECT `Nombre` FROM `recibe` WHERE `Nombre` LIKE '%{temp.texto_recibe.get()}%'; """
                    cursor.execute(sql)
                    for index in cursor:                        
                        tabla_reciben.insert("",END, text = index[0],)

                    # ahora al dar 2ble click se escribira el nombre en el campo
                    def escribir_recibe(event):
                        global vent_reciben                        
                        temp.texto_recibe.delete(0,END)                        
                        temp.texto_direccion.delete(0,END) 
                        temp.texto_telefono.delete(0,END) 

                        seleccion = tabla_reciben.selection()
                        if seleccion:
                            item = seleccion[0]                
                            recibe = tabla_reciben.item(item, "text") 

                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()           
                        sql = f""" SELECT * FROM `recibe` WHERE `Nombre` = "{recibe}" """
                        cursor.execute(sql)
                        for index in cursor: 
                            temp.texto_recibe.insert(0,index[1])
                            temp.texto_direccion.insert(0,index[2])
                            temp.texto_telefono.insert(0,index[3])

                        vent_reciben.destroy()   
                        vent_reciben = None                 
                        
                    tabla_reciben.bind("<Double-1>", escribir_recibe)              


                temp.texto_recibe.bind("<KeyRelease>", opciones_recibe)        

                def guardar_recibe():
                    if temp.texto_recibe.get() == "" or temp.texto_direccion.get()== "" or temp.texto_telefono.get()== "":
                        error = messagebox.showerror("Error","Debes llenar todos los campos para  poder guardar")
                    else:
                        conf = messagebox.askokcancel("Confirmacion", "Se va a agregar a la bd")
                        if conf:
                            id_recibe = 1
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "lilly",
                                password = "123456",
                                database = "lilly"
                                )
                            cursor = conn.cursor()

                            sql = """SELECT MAX(Id) FROM `recibe`;"""
                            cursor.execute(sql)
                            for index in cursor:
                                if index[0] == None:
                                    pass
                                else:
                                    id_recibe = index[0] + 1 

                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "lilly",
                                password = "123456",
                                database = "lilly"
                                )
                            cursor = conn.cursor()           
                            sql = f""" INSERT INTO `recibe`(`Id`, `Nombre`, `Direccion`, `Telefono`) VALUES ('{id_recibe}','{temp.texto_recibe.get()}','{temp.texto_direccion.get()}','{temp.texto_telefono.get()}') """
                            cursor.execute(sql)
                            conn.commit()

                            temp.texto_recibe.set("")
                            temp.texto_direccion.delete(0,END)
                            temp.texto_telefono.delete(0,END)

                temp.btn_guardar_recibe = CTkButton(temp, text="Guardar", command=guardar_recibe)
                temp.btn_guardar_recibe.pack(pady = 5)

                temp.label_mensajeria = CTkLabel(temp, text="---------- Mensajeria ----------")
                temp.label_mensajeria.pack(pady=5)                

                temp.texto_mensajeria = CTkEntry(temp,width=200,placeholder_text="Monto...")                
                temp.texto_mensajeria.pack(pady=5)

                def ejecutar_venta():
                    conf = messagebox.askokcancel("Confirmar","Se van a vender los productos del carrito")
                    if conf:
                        # llevemos la mensajeria a la bd 
                        id_mens = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = """SELECT MAX(Id) FROM `mensajeria`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass
                            else:
                                id_mens = index[0] + 1 

                        # llevemos la mensajeria a la bd 
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `mensajeria`(`Id`, `Fecha`, `Monto`) VALUES ('{id_mens}','{fecha_actual}','{temp.texto_mensajeria.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # hallemos el id de la venta
                        id_venta = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()

                        sql = """SELECT MAX(Id) FROM `salidas`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass
                            else:
                                id_venta = index[0] + 1 

                        # hacemos listado con los productos del carrito 
                        productos  = []
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()           
                        sql = f""" SELECT * FROM `carrito` """
                        cursor.execute(sql)
                        for index in cursor:
                            productos.append([index[0],index[1],index[2],index[3],index[4],index[5]])

                        # agregamos todos los productos a la tabla regalos
                        for prod in productos:
                            # agregamos los productos 
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "lilly",
                                password = "123456",
                                database = "lilly"
                                )
                            cursor = conn.cursor()           
                            sql = f""" INSERT INTO `salidas`(`Id`, `Fecha`, `Codigo`, `Nombre`, `CostoUsd`, `Precio`, `Cantidad`, `Envia`, `Recibe`) 
                                    VALUES ('{id_venta}','{fecha_actual}','{prod[0]}','{prod[1]}','{prod[2]}','{prod[3]}','{prod[4]}','{temp.texto_envia.get()}','{temp.texto_recibe.get()}') """
                            cursor.execute(sql)
                            conn.commit()

                        # ahora hagamos el tiket en txt
                        # Abrir ventana para elegir donde guardar el archivo
                        archivo_txt = filedialog.asksaveasfilename(
                            defaultextension=".txt",
                            filetypes=[("Archivos de texto", "*.txt")],
                            title="Guardar comprobante de venta"
                        )

                        if archivo_txt:
                            with open(archivo_txt, "w") as f:
                                # Escribir datos de quien ENVIA
                                f.write("DATOS DE QUIEN ENVIA:\n")
                                f.write("----------------------------------------\n")
                                f.write(f"Nombre: {temp.texto_envia.get()}\n")
                                f.write("\n")
                                
                                # Escribir datos de quien RECIBE
                                f.write("DATOS DE QUIEN RECIBE:\n")
                                f.write("----------------------------------------\n")
                                f.write(f"Nombre: {temp.texto_recibe.get()}\n")
                                f.write(f"Direccion: {temp.texto_direccion.get()}\n")
                                f.write(f"Telefono: {temp.texto_telefono.get()}\n")
                                f.write("\n")
                                
                                # Escribir los productos y cantidades
                                f.write("PRODUCTOS VENDIDOS:\n")
                                f.write("----------------------------------------\n")
                                for prod in productos:                                    
                                    f.write(f" {prod[4]}  {prod[1]}\n")                                                      
                            
                            messagebox.showinfo("Exito", f"Comprobante guardado en:\n{archivo_txt}")

                        # actualizar las tablas
                        limpiar_carrito()
                        actualizar_carrito(True)
                        actualizar_productos(True)
                        actualizar_total()
                        temp.destroy()  

                temp.btn_ejecutar = CTkButton(temp, text="Ejecutar Venta", command=ejecutar_venta)
                temp.btn_ejecutar.pack(pady = 30)  

        imagen_vender = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/pagar.jpg"), size = (150,75)) 

        self.btn_vender = CTkButton(self,text="", image=imagen_vender,command=vender, width=150,height=75)
        self.btn_vender.place(x=900,y=450)


# **********************************************************************************
# *****************************  Control Regalos ***********************************
# **********************************************************************************

class ControlRegalos(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Control Regalos")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1200
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1200x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo4.jpg"), size = (1200,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas()  

        self.tabla = ttk.Treeview(self, columns = ("Fecha","Codigo", "Nombre", "Costo USD", "Precio", "Cantidad", "Concepto"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")
        self.tabla.column("Codigo", width = 75, anchor="center")
        self.tabla.column("Nombre", width = 200, anchor="center")
        self.tabla.column("Costo USD", width = 75, anchor="center")        
        self.tabla.column("Precio", width = 75, anchor="center")        
        self.tabla.column("Cantidad", width = 75, anchor="center")
        self.tabla.column("Concepto", width = 200, anchor="center")

        self.tabla.place(x = 30, y = 100)        
        self.tabla.config(height = 11)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Codigo", text = "Codigo", anchor="center")
        self.tabla.heading("Nombre", text = "Nombre", anchor="center")
        self.tabla.heading("Costo USD", text = "Costo USD", anchor="center")        
        self.tabla.heading("Precio", text = "Precio", anchor="center")        
        self.tabla.heading("Cantidad", text = "Cantidad", anchor="center")
        self.tabla.heading("Concepto", text = "Concepto", anchor="center")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla(event):
            try:
                self.tabla.delete(*self.tabla.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                    sql = f""" SELECT * FROM regalos WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%' """

                else:
                    sql = f""" SELECT * FROM regalos WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%' and `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """

                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],index[6],index[8],))  
            except:
                error = messagebox.showerror("Error","No se pudo actualizar la tabla")


        self.label_fechas = CTkLabel(self,text="---------- Control de fechas ----------")
        self.label_fechas.place(x=900,y=80) 

        self.texto_fecha_inicial = CTkEntry(self,placeholder_text="Fecha inicial ...")
        self.texto_fecha_inicial.place(x=900,y=120) 

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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_inicial = CTkButton(self,text="...",command=fecha_inicial, width = 27, height = 27)
        self.btn_fecha_inicial.place(x=1050 ,y=120 )

        self.texto_fecha_final = CTkEntry(self,placeholder_text="Fecha final ...")
        self.texto_fecha_final.place(x=900,y=160) 

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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_fecha_final = CTkButton(self,text="...",command=fecha_final, width = 27, height = 27)
        self.btn_fecha_final.place(x=1050 ,y=160 )


        self.label_buscador = CTkLabel(self,text="---------- Buscador ----------")
        self.label_buscador.place(x=900,y=220)

        self.texto_buscador_codigo = CTkEntry(self,placeholder_text="Buscar por codigo ...")
        self.texto_buscador_codigo.place(x=900,y=260)          

        self.texto_buscador_codigo.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por nombre ...")
        self.texto_buscador_nombre.place(x=900,y=300) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla )  

        llenar_tabla(True)

        # ahora la posibilidad de eliminar el pago con doble click
        def eliminar_regalo(event): 
            global id_regalo            
            global codigo_regalo
            global cantidad_regalo

            # vamos a capturar el id del regalo que vamos a eliminar
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                id_regalo = self.tabla.item(item, "text")  
                codigo_regalo = self.tabla.item(item, "values")[1]                 
                cantidad_regalo = self.tabla.item(item, "values")[5]  

            conf = messagebox.askokcancel("Confirmar","Se va a cancelar este regalo") 
            if conf:
                # primero debemos devolver el regalo al almacen
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()               

                    sql = f""" UPDATE `productos` SET `Cantidad`= `Cantidad` + '{cantidad_regalo}' WHERE `Codigo` = "{codigo_regalo}"; """
                    cursor.execute(sql)
                    conn.commit()                

                except:
                    error = messagebox.showerror("Error","No se pudo devolver el producto al almacen") 

                # eliminamos el regalo de la base de datos
                try:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `regalos` WHERE `Id` = "{id_regalo}" and `Codigo` = {codigo_regalo} """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla(True)

                except:
                    error = messagebox.showerror("Error","No se pudo borrar el regalo de la base de datos") 

        self.tabla.bind("<Double-1>", eliminar_regalo)




# **********************************************************************************
# *****************************  Control Ventas ***********************************
# **********************************************************************************

class ControlVentas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Control Ventas")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1200
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1200x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (1200,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas()          

        self.tabla = ttk.Treeview(self, columns = ("Fecha","Envia", "Recibe", "Precio", "Costo", "Ganancia"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")
        self.tabla.column("Envia", width = 200, anchor="center")        
        self.tabla.column("Recibe", width = 200, anchor="center")
        self.tabla.column("Precio", width = 100, anchor="center") 
        self.tabla.column("Costo", width = 100, anchor="center")               
        self.tabla.column("Ganancia", width = 100, anchor="center")        

        self.tabla.place(x = 30, y = 200)        
        self.tabla.config(height = 11)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Envia", text = "Envia", anchor="center")
        self.tabla.heading("Recibe", text = "Recibe", anchor="center")
        self.tabla.heading("Precio", text = "Precio", anchor="center")        
        self.tabla.heading("Costo", text = "Costo", anchor="center")        
        self.tabla.heading("Ganancia", text = "Ganancia", anchor="center")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()
            if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                pass

            else:
                sql = f""" SELECT * FROM salidas WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                cursor.execute(sql)

            ventas_agrupadas = {}
            # Procesar cada registro
            for index in cursor:
                id_venta = index[0]
                
                if id_venta not in ventas_agrupadas:
                    ventas_agrupadas[id_venta] = {
                        'fecha': index[1],
                        'precio_total': 0,
                        'costo_total': 0,
                        'envia': index[7],
                        'recibe': index[8]
                    }
                
                # Acumular precios y costos
                ventas_agrupadas[id_venta]['precio_total'] += index[5] * index[6]
                ventas_agrupadas[id_venta]['costo_total'] += index[4] * index[6]
            
            # Insertar datos agrupados en la tabla
            for id_venta, datos in ventas_agrupadas.items():
                ganancia = datos['precio_total'] - datos['costo_total']
                self.tabla.insert("", END, text=id_venta, values=(
                    datos['fecha'],
                    datos['envia'],
                    datos['recibe'],
                    round(datos['precio_total'], 2),
                    round(datos['costo_total'], 2),
                    round(ganancia, 2)
                ))



        self.label_fechas = CTkLabel(self,text="---------- Control de fechas ----------")
        self.label_fechas.place(x=200,y=50) 

        self.texto_fecha_inicial = CTkEntry(self,placeholder_text="Fecha inicial ...")
        self.texto_fecha_inicial.place(x=200,y=90) 

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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_inicial = CTkButton(self,text="...",command=fecha_inicial, width = 27, height = 27)
        self.btn_fecha_inicial.place(x=350 ,y=90 )

        self.texto_fecha_final = CTkEntry(self,placeholder_text="Fecha final ...")
        self.texto_fecha_final.place(x=200,y=130) 

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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_fecha_final = CTkButton(self,text="...",command=fecha_final, width = 27, height = 27)
        self.btn_fecha_final.place(x=350 ,y=130 )        

        llenar_tabla(True)


        def modificar_venta(event):
            global id_venta                     

            # vamos a capturar el id de la venta 
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                id_venta = self.tabla.item(item, "text") 
                fecha_venta = self.tabla.item(item, "values")[0] 
                envia_venta = self.tabla.item(item, "values")[1] 
                recibe_venta = self.tabla.item(item, "values")[2] 

            # ahora vamos a mostrar una ventana con esta venta en especifico
            temp = CTkToplevel()
            temp.title("Control Venta Especifica") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 1000
            hventana = 600
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.geometry("1000x600") 
            temp.resizable(False,False)
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False))  

            estilos_tablas()  

            temp.tabla_especifica = ttk.Treeview(temp, columns = ("Fecha","Codigo", "Nombre", "Costo USD", "Precio", "Cantidad", "Envia", "Recibe"), show="headings")
            temp.tabla_especifica.column("#0", width = 100, anchor="center")
            temp.tabla_especifica.column("Fecha", width = 100, anchor="center")
            temp.tabla_especifica.column("Codigo", width = 75, anchor="center")
            temp.tabla_especifica.column("Nombre", width = 200, anchor="center")
            temp.tabla_especifica.column("Costo USD", width = 75, anchor="center")       
            temp.tabla_especifica.column("Precio", width = 75, anchor="center")        
            temp.tabla_especifica.column("Cantidad", width = 75, anchor="center")
            temp.tabla_especifica.column("Envia", width = 100, anchor="center")
            temp.tabla_especifica.column("Recibe", width = 100, anchor="center")

            temp.tabla_especifica.place(x = 50, y = 100)        
            temp.tabla_especifica.config(height = 11)

            temp.tabla_especifica.heading("#0", text = "Id", anchor="center")
            temp.tabla_especifica.heading("Fecha", text = "Fecha", anchor="center")
            temp.tabla_especifica.heading("Codigo", text = "Codigo", anchor="center")
            temp.tabla_especifica.heading("Nombre", text = "Nombre", anchor="center")
            temp.tabla_especifica.heading("Costo USD", text = "Costo USD", anchor="center")        
            temp.tabla_especifica.heading("Precio", text = "Precio", anchor="center")        
            temp.tabla_especifica.heading("Cantidad", text = "Cantidad", anchor="center")
            temp.tabla_especifica.heading("Envia", text = "Envia", anchor="center")
            temp.tabla_especifica.heading("Recibe", text = "Recibe", anchor="center")

            scrollbar = CTkScrollbar(temp, command = temp.tabla_especifica.yview, width = 18)
            scrollbar.place(in_ = temp.tabla_especifica, relheigh = 1, relx = 1)

            temp.tabla_especifica.config(yscrollcommand = scrollbar.set)

            def llenar_especifica(event):
                try:
                    temp.tabla_especifica.delete(*temp.tabla_especifica.get_children())
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                   
                    sql = f""" SELECT * FROM `salidas` WHERE `Id` = {id_venta} """
                    cursor.execute(sql)
                    for index in cursor:
                        temp.tabla_especifica.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],index[6],index[7],index[8],))  

                except:
                    error = messagebox.showerror("Error","No se pudo actualizar la tabla")

            llenar_especifica(True)

            def eliminar_producto(event):
                global id_especifica           
                global codigo_especifica           
                global cantidad_especifica           

                # vamos a capturar el id de la venta 
                seleccion = temp.tabla_especifica.selection()
                if seleccion:
                    item = seleccion[0]                
                    id_especifica = temp.tabla_especifica.item(item, "text") 
                    codigo_especifica = temp.tabla_especifica.item(item, "values")[1]
                    cantidad_especifica = temp.tabla_especifica.item(item, "values")[5]

                conf = messagebox.askokcancel("Confirmar","Se va a eliminar el producto de esta venta")
                if conf:
                    # primero devolvemos el producto al almacen
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                   
                    sql = f""" UPDATE `productos` SET `Cantidad` = `Cantidad` + '{cantidad_especifica}' WHERE `Codigo` = "{codigo_especifica}" """
                    cursor.execute(sql)
                    conn.commit()

                    # ahora eliminaremos producto de la compra hecha 
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                   
                    sql = f""" DELETE FROM `salidas` WHERE `Id` = {id_especifica} AND `Codigo` = "{codigo_especifica}" """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_especifica(True)
                    llenar_tabla(True)

            temp.tabla_especifica.bind("<Double-1>", eliminar_producto)

            # ahora vamos a dar la opcion de agregar un producto a la venta 
            def agregar_venta():
                # crearemos una nueva ventana para mostrar los productos a agregar
                root = CTkToplevel()
                root.title("Control Venta Especifica") 
                htotal = root.winfo_screenheight()
                wtotal = root.winfo_screenwidth()
                wventana = 600
                hventana = 600
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                root.geometry(f"+{posx}+{posy}")                
                root.resizable(False,False)
                root.after(250, lambda: root.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
                root.lift()
                root.attributes('-topmost', True)
                root.after(200, lambda: root.attributes('-topmost', False))  

                # ***************** buscador 
                root.texto_buscador = CTkEntry(root, width=200)     
                root.texto_buscador.pack(pady=20)

                estilos_tablas() 

                root.tabla = ttk.Treeview(root, columns = ("Nombre", "Costo USD", "Precio", "Cantidad", "Categoria"), show="headings")
                root.tabla.column("#0", width = 100, anchor="center")
                root.tabla.column("Nombre", width = 200, anchor="center")
                root.tabla.column("Costo USD", width = 75, anchor="center")
                root.tabla.column("Precio", width = 75, anchor="center")
                root.tabla.column("Cantidad", width = 75, anchor="center")
                root.tabla.column("Categoria", width = 100, anchor="center")

                root.tabla.pack(pady=20)        
                root.tabla.config(height = 10)

                root.tabla.heading("#0", text = "Codigo", anchor="center")
                root.tabla.heading("Nombre", text = "Nombre", anchor="center")
                root.tabla.heading("Costo USD", text = "Costo USD", anchor="center")
                root.tabla.heading("Precio", text = "Precio", anchor="center")
                root.tabla.heading("Cantidad", text = "Cantidad", anchor="center")
                root.tabla.heading("Categoria", text = "Categoria", anchor="center")

                scrollbar = CTkScrollbar(root, command = root.tabla.yview, width = 18)
                scrollbar.place(in_ = root.tabla, relheigh = 1, relx = 1)

                root.tabla.config(yscrollcommand = scrollbar.set)

                def actualizar_productos(event):
                    root.tabla.delete(*root.tabla.get_children())
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()           
                    sql = f""" SELECT * FROM productos WHERE `Nombre` LIKE '%{root.texto_buscador.get()}%' """
                    cursor.execute(sql)
                    for index in cursor:
                        root.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],)) 
                  

                root.texto_buscador.bind("<KeyRelease>", actualizar_productos) 
                actualizar_productos(True)

                # ahora vamos a agregar un producto 
                def agregar_producto_venta(event):
                    seleccion = root.tabla.selection()
                    if seleccion:
                        item = seleccion[0]                    
                        cod = root.tabla.item(item, "text")
                        values = root.tabla.item(item, "values")

                    # ahora debe haber una modal para ver la cantidad
                    vent = CTkToplevel()
                    vent.title("Cantidad") 
                    htotal = temp.winfo_screenheight()
                    wtotal = temp.winfo_screenwidth()
                    wventana = 300
                    hventana = 300
                    posx = round(wtotal/2-wventana/2)
                    posy = round(htotal/2-hventana/2)
                    vent.geometry(f"+{posx}+{posy}")
                    vent.lift()
                    vent.attributes('-topmost', True)
                    vent.after(200, lambda: vent.attributes('-topmost', False))  
                    vent.after(250, lambda: vent.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

                    vent.texto_cantidad = CTkEntry(vent, placeholder_text="Cantidad ...")
                    vent.texto_cantidad.pack(pady = 10)

                    def aceptar_producto():
                        # verifiquemos que no sobrevendas un producto
                        alcansa = True
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "lilly",
                            password = "123456",
                            database = "lilly"
                            )
                        cursor = conn.cursor()           
                        sql = f""" SELECT `Cantidad` FROM `productos` WHERE `Codigo` = "{cod}" """
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] >= float(vent.texto_cantidad.get()):
                                pass
                            else:
                                alcansa = False
                                error = messagebox.showerror("Error","No tienes esa cantidad en almacen")
                                vent.destroy()

                        if alcansa:
                            if vent.texto_cantidad.get() == "":
                                error = messagebox.showerror("Error","Debes escribir alguna cantidad")

                            else:                    
                                conf = messagebox.askokcancel("Confirmar","Vas a agregar este producto a la venta ya realizada")
                                if conf:
                                    # hay que verificar si es un producto que ya estaba en la venta o no para agregarlo o aumentarle la cantidad
                                    esta = False
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "lilly",
                                        password = "123456",
                                        database = "lilly"
                                        )
                                    cursor = conn.cursor()           
                                    sql = f""" SELECT COUNT(`Codigo`) FROM `salidas` WHERE `Id` = "{id_venta}" AND `Codigo` = "{cod}" """
                                    cursor.execute(sql)
                                    for index in cursor:
                                        if index[0] == 0:
                                            pass                                            
                                        else:
                                            esta = True

                                    if esta:                                        
                                        # ***************************** aumentemos la cantidad del producto en la venta
                                        conn = mysql.connector.connect(
                                            host = "localhost",
                                            user = "lilly",
                                            password = "123456",
                                            database = "lilly"
                                            )
                                        cursor = conn.cursor()           
                                        sql = f""" UPDATE `salidas` SET `Cantidad`= `Cantidad` + '{vent.texto_cantidad.get()}' WHERE `Id` = "{id_venta}" and `Codigo` = "{cod}" """
                                        cursor.execute(sql)
                                        conn.commit()

                                        # ***************************** ahora descontamos la cantidad del almacen 
                                        conn = mysql.connector.connect(
                                            host = "localhost",
                                            user = "lilly",
                                            password = "123456",
                                            database = "lilly"
                                            )
                                        cursor = conn.cursor()           
                                        sql = f""" UPDATE `productos` SET `Cantidad`= `Cantidad` - '{vent.texto_cantidad.get()}' WHERE `Codigo` = "{cod}" """
                                        cursor.execute(sql)
                                        conn.commit()

                                        # ******************************* actualizaciones
                                        actualizar_productos(True)
                                        llenar_tabla(True)
                                        llenar_especifica(True)

                                        vent.destroy()

                                    else:
                                        # ************************* primero lo mandamos a la salida  
                                        conn = mysql.connector.connect(
                                            host = "localhost",
                                            user = "lilly",
                                            password = "123456",
                                            database = "lilly"
                                            )
                                        cursor = conn.cursor()           
                                        sql = f""" INSERT INTO `salidas`(`Id`, `Fecha`, `Codigo`, `Nombre`, `CostoUsd`, `Precio`, `Cantidad`, `Envia`, `Recibe`) VALUES ('{id_venta}','{fecha_venta}','{cod}','{values[0]}','{values[1]}','{values[2]}','{vent.texto_cantidad.get()}','{envia_venta}','{recibe_venta}') """
                                        cursor.execute(sql)
                                        conn.commit()

                                        # ***************************** ahora descontamos la cantidad del almacen 
                                        conn = mysql.connector.connect(
                                            host = "localhost",
                                            user = "lilly",
                                            password = "123456",
                                            database = "lilly"
                                            )
                                        cursor = conn.cursor()           
                                        sql = f""" UPDATE `productos` SET `Cantidad`= `Cantidad` - '{vent.texto_cantidad.get()}' WHERE `Codigo` = "{cod}" """
                                        cursor.execute(sql)
                                        conn.commit()   

                                        # ******************************* actualizaciones
                                        actualizar_productos(True)
                                        llenar_tabla(True)
                                        llenar_especifica(True)

                                        vent.destroy()   


                    vent.btn = CTkButton(vent, text="Aceptar", command=aceptar_producto)
                    vent.btn.pack(pady = 10)

                root.tabla.bind("<Double-1>", agregar_producto_venta)
            

            temp.btn_agregar = CTkButton(temp,text="Agregar", command=agregar_venta)
            temp.btn_agregar.place(x=100,y=500)

        self.tabla.bind("<Double-1>", modificar_venta)



# **********************************************************************************
# ****************************  Consulta Totales ***********************************
# **********************************************************************************

class ConsultaTotales(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Consulta Totales")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))   

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/pagos1.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################         

        self.label_informaciones = CTkLabel(self, text="---------- Informaciones ----------", bg_color="black")
        self.label_informaciones.place(x=500,y=60)

        self.label_ingresos = CTkLabel(self, text="Total Ingresos: ")
        self.label_ingresos.place(x=500,y=100)

        string_ingresos = StringVar()
        string_ingresos.set("0")

        self.label_ingresos2 = CTkLabel(self, textvariable=string_ingresos)
        self.label_ingresos2.place(x=700,y=100)        

        self.label_gastos = CTkLabel(self, text="Total Gastos Asociados: ")
        self.label_gastos.place(x=500,y=140)

        string_gastos = StringVar()
        string_gastos.set("0")

        self.label_gastos2 = CTkLabel(self, textvariable=string_gastos)
        self.label_gastos2.place(x=700,y=140)

        self.label_salarios = CTkLabel(self, text="Total Salarios: ")
        self.label_salarios.place(x=500,y=180)

        string_salarios = StringVar()
        string_salarios.set("0")

        self.label_salarios2 = CTkLabel(self, textvariable=string_salarios)
        self.label_salarios2.place(x=700,y=180)

        self.label_costos = CTkLabel(self, text="Total Costos: ")
        self.label_costos.place(x=500,y=220)

        string_costos = StringVar()
        string_costos.set("0")

        self.label_costos2 = CTkLabel(self, textvariable=string_costos)
        self.label_costos2.place(x=700,y=220)

        self.label_regalo = CTkLabel(self, text="Regalos: ")
        self.label_regalo.place(x=500,y=260)

        string_regalo = StringVar()
        string_regalo.set("0")

        self.label_regalo2 = CTkLabel(self, textvariable=string_regalo)
        self.label_regalo2.place(x=700,y=260)

        self.label_ganancia = CTkLabel(self, text="Total Ganancias: ")
        self.label_ganancia.place(x=500,y=300)

        string_ganancia = StringVar()
        string_ganancia.set("0")

        self.label_ganancia2 = CTkLabel(self, textvariable=string_ganancia)
        self.label_ganancia2.place(x=700,y=300)

        self.label_mas_vende = CTkLabel(self, text="Producto Mas Vendido: ")
        self.label_mas_vende.place(x=500,y=340)

        string_mas_vende = StringVar()
        string_mas_vende.set("0")

        self.label_mas_vende2 = CTkLabel(self, textvariable=string_mas_vende)
        self.label_mas_vende2.place(x=700,y=340)

        self.label_menos_vende = CTkLabel(self, text="Producto Menos Vendido: ")
        self.label_menos_vende.place(x=500,y=380)

        string_menos_vende = StringVar()
        string_menos_vende.set("0")

        self.label_menos_vende2 = CTkLabel(self, textvariable=string_menos_vende)
        self.label_menos_vende2.place(x=700,y=380)

        self.label_mas_ganancia = CTkLabel(self, text="Producto Mas Ganancia: ")
        self.label_mas_ganancia.place(x=500,y=420)

        string_mas_ganancia = StringVar()
        string_mas_ganancia.set("0")

        self.label_mas_ganancia2 = CTkLabel(self, textvariable=string_mas_ganancia)
        self.label_mas_ganancia2.place(x=700,y=420)

        self.label_menos_ganancia = CTkLabel(self, text="Producto Menos Ganancia: ")
        self.label_menos_ganancia.place(x=500,y=460)

        string_menos_ganancia = StringVar()
        string_menos_ganancia.set("0")

        self.label_menos_ganancia2 = CTkLabel(self, textvariable=string_menos_ganancia)
        self.label_menos_ganancia2.place(x=700,y=460)        

        # ahora vamos a generar la funcion para mostrar los datos 
        def consulta():
            if self.texto_fecha_final.get() == "" or self.texto_fecha_inicial.get() == "":
                pass

            else:
                try:
                    # primero vamos a hallar el total de ingresos
                    ingresos = 0
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                    
                    sql = f""" SELECT  `Precio`, `Cantidad` FROM `salidas` WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                    cursor.execute(sql)
                    for index in cursor:                        
                        ingresos += index[0]*index[1]

                    # hay que sumarle las mensajerias
                    mensajeria = 0
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                    
                    sql = f""" SELECT  `Monto` FROM `mensajeria` WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                    cursor.execute(sql)
                    for index in cursor:                        
                        mensajeria += index[0]
                        

                    string_ingresos.set(round(ingresos + mensajeria,2))
                    ####################################################

                    # ahora veremos total de gastos asociados 
                    asociados = 0
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                    
                    sql = f""" SELECT `Monto` FROM `asociados` WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                    cursor.execute(sql)
                    for index in cursor:
                        asociados += index[0]

                    string_gastos.set(round(asociados,2))
                    ####################################################

                    # ahora veamos los gastos de los salarios
                    salarios = 0
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                    
                    sql = f""" SELECT `Monto` FROM `salarios` WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                    cursor.execute(sql)
                    for index in cursor:
                        salarios += index[0]

                    string_salarios.set(round(salarios,2))
                    ####################################################

                    # ahora veamos el total de costos 
                    costos_usd = 0
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                    
                    sql = f""" SELECT  `CostoUsd`, `Cantidad` FROM `salidas` WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                    cursor.execute(sql)
                    for index in cursor:
                        costos_usd += index[0]*index[1]

                    string_costos.set(round(costos_usd, 2))
                    ########################################################

                    # ahora los regalos
                    regalos = 0                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                    
                    sql = f""" SELECT `CostoUsd`, `Cantidad` FROM `regalos` WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                    cursor.execute(sql)
                    for index in cursor:
                        regalos += index[0]*index[1]  

                    string_regalo.set(regalos)

                    ############################################################

                    # ahora veamos las ganancias 
                    ganancias = ingresos - asociados - salarios - costos_usd - regalos
                    string_ganancia.set(round(ganancias, 2))
                    ########################################################

                    # ahora el producto mas vendido 
                    nombre = ""
                    cantidad = 0
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                    
                    sql = f""" SELECT Codigo, Nombre, SUM(Cantidad) AS total_unidades_vendidas FROM salidas WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" GROUP BY Codigo, Nombre ORDER BY total_unidades_vendidas DESC LIMIT 1; """
                    cursor.execute(sql)
                    for index in cursor:
                        nombre = index[1]
                        cantidad = index[2]

                    string = f" ({round(cantidad, 2)})"
                    string_mas_vende.set(nombre + string)
                    ##########################################################

                    # ahora el menos vendido
                    nombre = ""
                    cantidad = 0
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                    
                    sql = f""" SELECT Codigo, Nombre, SUM(Cantidad) AS total_unidades_vendidas FROM salidas WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" GROUP BY Codigo, Nombre ORDER BY total_unidades_vendidas ASC LIMIT 1; """
                    cursor.execute(sql)
                    for index in cursor:
                        nombre = index[1]
                        cantidad = index[2]

                    string = f" ({round(cantidad, 2)})"
                    string_menos_vende.set(nombre + string)

                    ########################################################################

                    # ahora el producto que mas ganancia genera 
                    nombre = ""
                    ganancia = 0
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                    
                    sql = f""" SELECT Codigo, Nombre, SUM((Precio - CostoUsd) * Cantidad) AS ganancia_total FROM salidas WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" GROUP BY Codigo, Nombre ORDER BY ganancia_total DESC LIMIT 1; """
                    cursor.execute(sql)
                    for index in cursor:
                        nombre = index[1]
                        ganancia = index[2]

                    string = f" ({round(ganancia, 2)})"
                    string_mas_ganancia.set(nombre + string)

                    ###############################################################

                    # ahora el que menos ganancia genera 
                    nombre = ""
                    ganancia = 0
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "lilly",
                        password = "123456",
                        database = "lilly"
                        )
                    cursor = conn.cursor()                    
                    sql = f""" SELECT Codigo, Nombre, SUM((Precio - CostoUsd) * Cantidad) AS ganancia_total FROM salidas WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" GROUP BY Codigo, Nombre ORDER BY ganancia_total ASC LIMIT 1; """
                    cursor.execute(sql)
                    for index in cursor:
                        nombre = index[1]
                        ganancia = index[2]

                    string = f" ({round(ganancia, 2)})"
                    string_menos_ganancia.set(nombre + string)

                    ############################################################

                    

                except:
                    error = messagebox.showerror("Error","No se ha podido mostrar todos los datos \n Revise la informacion escrita en los campos de las fechas")


        self.label_fechas = CTkLabel(self,text="---------- Control de fechas ----------", bg_color="black")
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
                consulta()               
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
                consulta()               
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_fecha_final = CTkButton(self,text="...",command=fecha_final, width = 27, height = 27)
        self.btn_fecha_final.place(x=200 ,y=130 )




# **********************************************************************************
# ************************************  Almacen ************************************
# **********************************************************************************

class Deficit(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Deficit")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Costo Usd", "Precio", "Cantidad", "Categoria", "Minimo"))
        self.tabla.column("#0", width = 75)
        self.tabla.column("Nombre", width = 200)
        self.tabla.column("Costo Usd", width = 100)
        self.tabla.column("Precio", width = 75)
        self.tabla.column("Cantidad", width = 75)
        self.tabla.column("Categoria", width = 100)
        self.tabla.column("Minimo", width = 75)

        self.tabla.place(x = 50, y = 100)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Costo Usd", text = "Costo Usd")
        self.tabla.heading("Precio", text = "Precio")
        self.tabla.heading("Cantidad", text = "Cantidad")
        self.tabla.heading("Categoria", text = "Categoria")
        self.tabla.heading("Minimo", text = "Minimo")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM `productos` WHERE `Cantidad` <= `Minimo`; """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],index[6],))  

        llenar_tabla()

        # ahora un boton para que haga el txt
        def hacer_txt():
            deficit = []
            conn = mysql.connector.connect(
                host = "localhost",
                user = "lilly",
                password = "123456",
                database = "lilly"
                )
            cursor = conn.cursor()

            sql = f""" SELECT `Nombre`,`Cantidad`,`Minimo` FROM `productos` WHERE `Cantidad` <= `Minimo`; """
            cursor.execute(sql)
            for index in cursor:
                deficit.append([index[0],index[1],index[2]])

            archivo_txt = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt")],
                title="Guardar Productos en Deficit"
            )

            if archivo_txt:
                with open(archivo_txt, "w") as f:
                    # Escribir datos de quien ENVIA
                    f.write("PRODUCTOS EN DEFICIT:\n")
                    f.write("----------------------------------------\n")
                    
                    for defi in deficit:                                    
                        f.write(f"Nombre: {defi[0]}\n")
                        f.write(f"Cantidad: {defi[1]}\n")                                    
                        f.write(f"Minimo: {defi[2]}\n")                                    
                        f.write("----------------------------------------\n")                            
                
                messagebox.showinfo("Exito", f"Informacion guardada en:\n{archivo_txt}")           

        self.btn = CTkButton(self,text="Hacer Txt", command=hacer_txt)
        self.btn.place(x=50,y=450)



# **********************************************************************************
# ************************************  Clientes ************************************
# **********************************************************************************

class Clientes(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Clientes")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Lilly/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################  

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Envios", "Monto"))
        self.tabla.column("#0", width = 200)
        self.tabla.column("Envios", width = 100)
        self.tabla.column("Monto", width = 100)        

        self.tabla.place(x = 50, y = 240)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Cliente")
        self.tabla.heading("Envios", text = "Envios")
        self.tabla.heading("Monto", text = "Monto")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            if self.texto_fecha_final.get() == "" or self.texto_fecha_inicial.get() == "":
                pass

            else:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT `Envia`, COUNT(DISTINCT `Id`) AS CantidadEnvios, SUM(`Precio` * `Cantidad`) AS MontoTotal FROM `salidas` WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" GROUP BY `Envia` ORDER BY `CantidadEnvios` DESC; """
                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],))  

        self.label_fechas = CTkLabel(self,text="---------- Control de fechas ----------", bg_color="transparent")
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
                llenar_tabla()               
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
                llenar_tabla()               
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_fecha_final = CTkButton(self,text="...",command=fecha_final, width = 27, height = 27)
        self.btn_fecha_final.place(x=200 ,y=130 )

        # ahora configuremos para que al dar 2ble click desglose las ventas de esa persona que envia 
        def double_click(event):
            temp = CTkToplevel()
            temp.title("Desglose") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 1000
            hventana = 600
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"1000x600+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/lilly/imagenes funcionamiento/lilly_icono.ico')) 

            estilos_tablas()          

            tabla = ttk.Treeview(temp, columns = ("Fecha","Codigo", "Nombre", "Costo USD", "Precio", "Cantidad", "Envia", "Recibe"), show="headings")
            tabla.column("#0", width = 50, anchor="center")
            tabla.column("Fecha", width = 100, anchor="center")
            tabla.column("Codigo", width = 75, anchor="center")
            tabla.column("Nombre", width = 150, anchor="center")
            tabla.column("Costo USD", width = 75, anchor="center")       
            tabla.column("Precio", width = 75, anchor="center")        
            tabla.column("Cantidad", width = 75, anchor="center")
            tabla.column("Envia", width = 150, anchor="center")
            tabla.column("Recibe", width = 150, anchor="center")

            tabla.place(x = 50, y = 100)        
            tabla.config(height = 11)

            tabla.heading("#0", text = "Id", anchor="center")
            tabla.heading("Fecha", text = "Fecha", anchor="center")
            tabla.heading("Codigo", text = "Codigo", anchor="center")
            tabla.heading("Nombre", text = "Nombre", anchor="center")
            tabla.heading("Costo USD", text = "Costo USD", anchor="center")        
            tabla.heading("Precio", text = "Precio", anchor="center")        
            tabla.heading("Cantidad", text = "Cantidad", anchor="center")
            tabla.heading("Envia", text = "Envia", anchor="center")
            tabla.heading("Recibe", text = "Recibe", anchor="center")

            scrollbar2 = CTkScrollbar(temp, command = tabla.yview, width = 18)
            scrollbar2.place(in_ = tabla, relheigh = 1, relx = 1)

            tabla.config(yscrollcommand = scrollbar2.set)

            def llenar_temp():
                tabla.delete(*tabla.get_children())

                seleccion = self.tabla.selection()
                if seleccion:
                    item = seleccion[0]                
                    envia = self.tabla.item(item, "text") 
                
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "lilly",
                    password = "123456",
                    database = "lilly"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM salidas WHERE `Envia` = '{envia}' and `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                cursor.execute(sql)
                for index in cursor:
                    tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],index[6],index[7],index[8],))  

            llenar_temp()



        self.tabla.bind("<Double-1>", double_click)











conn.close()
autenticacion = Autenticacion()
autenticacion.mainloop()