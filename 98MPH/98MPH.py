from customtkinter import *
from customtkinter import CTkImage
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import *
import mysql.connector
import subprocess
from PIL import Image , ImageTk
from openpyxl import *
import pandas as pd 
from tkcalendar import *
import copy
from dateutil.relativedelta import relativedelta

fecha_actual = datetime.now().date()

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""    
    )
cursor = conn.cursor()
sql = ""

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

ususario_gym_98mph_is_created = False
base_data_is_created = False
table_usuarios_is_created = False
usuario_gym_98mph_is_created = False
table_licencias_is_created = False

# ********************** creando usuario admin ******************************

try:
    sql = """CREATE USER 'gym_98mph'@'localhost' IDENTIFIED BY '123456';"""
    cursor.execute(sql)
    conn.commit()
except:
    ususario_gym_98mph_is_created = True

sql = """GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' REQUIRE NONE WITH GRANT OPTION MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0; """
cursor.execute(sql)
conn.commit()

conn.close()

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    )
cursor = conn.cursor()

# ******* creando la base de datos gym_98mph ***********
try:
    sql = """CREATE DATABASE gym_98mph CHARACTER SET = utf8mb4 COLLATE utf8mb4_spanish_ci;"""
    cursor.execute(sql)
    conn.commit()
    base_data_is_created = True
except:
    base_data_is_created = True

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "gym_98mph"
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
    user = "root",
    password = "",
    database = "gym_98mph"
    )
cursor = conn.cursor()

usuario_inicial = []
sql = """ SELECT Usuario FROM usuarios """
cursor.execute(sql)

for usser in cursor:
    usuario_inicial.append(usser)

for index in range(len(usuario_inicial)):
    if usuario_inicial[index][0] == "gym_98mph":
        usuario_gym_98mph_is_created = True

if usuario_gym_98mph_is_created == False:
    try:
        sql = """INSERT INTO usuarios (Usuario,Password) VALUES ("gym_98mph","123456")"""
        cursor.execute(sql)
        conn.commit()
        
        usuario_gym_98mph_is_created = True
    except:
        usuario_gym_98mph_is_created = True


# ************** creando tabla licencias ***************

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "gym_98mph"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `gym_98mph`.`licencias` (`codigo_lic` VARCHAR(50) NOT NULL , `pass_economia` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    table_licencias_is_created = True


# *********************** creando tabla clientes 
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "gym_98mph"
    )
cursor = conn.cursor()

try:
    sql = """ CREATE TABLE `clientes` (`ID` int(11) NOT NULL, `Nombre` varchar(50) NOT NULL, `Apellido 1` varchar(50) NOT NULL, `Apellido 2` varchar(50) NOT NULL, `Modalidad` varchar(50) NOT NULL, `Trabajador` varchar(50) NOT NULL, `Telefono` varchar(50) NOT NULL,  `Ultima_Asistencia` date NOT NULL,  `Fecha_Pago` date NOT NULL) ENGINE=InnoDB """
    cursor.execute(sql)
    conn.commit()
except:
    pass

# *********************** creando tabla entrenadores 
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "gym_98mph"
    )
cursor = conn.cursor()

try:
    sql = """ CREATE TABLE `entrenadores` ( `nombre` varchar(50) NOT NULL) ENGINE=InnoDB """
    cursor.execute(sql)
    conn.commit()
except:
    pass

# *********************** creando tabla extra
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "gym_98mph"
    )
cursor = conn.cursor()

try:
    sql = """ CREATE TABLE `extra` (`extra` varchar(50) NOT NULL, `precio` int(11) NOT NULL, `pago entrenador` int(11) NOT NULL) ENGINE=InnoDB """
    cursor.execute(sql)
    conn.commit()
except:
    pass

# *********************** creando tabla modalidad
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "gym_98mph"
    )
cursor = conn.cursor()

try:
    sql = """ CREATE TABLE `modalidad` ( `modalidad` varchar(50) NOT NULL, `precio` int(11) NOT NULL, `pago_entrenador` int(11) NOT NULL) ENGINE=InnoDB """
    cursor.execute(sql)
    conn.commit()
except:
    pass

# *********************** creando tabla pagos
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "gym_98mph"
    )
cursor = conn.cursor()

try:
    sql = """ CREATE TABLE `pagos` (  `fecha` date NOT NULL,  `id` int(11) NOT NULL,  `nombre_completo` varchar(50) NOT NULL,  `modalidad` varchar(50) NOT NULL,  `Trabajador` varchar(50) NOT NULL,  `pagar_activacion` varchar(50) NOT NULL,  `importe` int(11) NOT NULL,  `pago_entrenador` int(11) NOT NULL) ENGINE=InnoDB """
    cursor.execute(sql)
    conn.commit()
except:
    pass
    
    
#*************************************************************************************
#********************************** Autenticacion ************************************
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
        self.iconbitmap("D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico")        

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

        sql = """SELECT Usuario, Password FROM usuarios"""

        cursor.execute(sql)
        for index in cursor:
            autorizacion.append(index)

        def codigo_btn_iniciar():
            # ******************** control de vencimiento *****************
            lic = ""

            conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "gym_98mph"
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
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        self.label = CTkLabel(self, text = "Introduzca la licencia nueva", font=("Times New Roman",14))
        self.label.place(x = 60 , y = 20)        

        self.texto = CTkEntry(self, width = 200)
        self.texto.place(x = 60 , y = 80)   


        def codigo_btn_aceptar_nueva_licencia():

            #  desencriptando el codigo para validar licencia
            # el codigo debe tener un formato como el del siguiente ejemplo:
            # nuevalicenciaaño2025-mes01-dia01serial5cd028cgmk 
            # solo cambiamos los numeros de año , mes , dia y serial lo demas se mantiene igual
            

            try:
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
                        user = "root",
                        password = "",
                        database = "gym_98mph"
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
                
            except:
                error = messagebox.showinfo("Error", "Licencia Inservible")

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
        self.title("98 MPH")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))
        self.resizable(False,False)          
        
        firma = "Vence (" + str(fecha_vencimiento) + ")"
        self.label_gym_98mph = CTkLabel(self, text = firma, font=("Times New Roman",16))
        self.label_gym_98mph.place(x = 1150, y = 650)

        def cerrar_programa(): 
            self.quit()                  
            self.destroy()
            autenticacion.destroy()
            quit()  

        # para que se cierre todo el programa si cerramos esta ventana 
        self.protocol("WM_DELETE_WINDOW", cerrar_programa) 

        def cerrar_cesion():
            self.destroy()
            autenticacion.deiconify() 

        self.menu = Menu(self)
        self.config(menu=self.menu, width="200", height="100")

        economia_menu = Menu(self.menu, tearoff = 0)   
        economia_menu.add_command(label="Balance ")
        economia_menu.add_command(label="Modalidad ")
        economia_menu.add_command(label="Agregos")
        economia_menu.add_command(label="Pago Entrenadores ")
        economia_menu.add_command(label="Pagos Atrasados")
        
        entrenadores_menu = Menu(self.menu, tearoff = 0)
        entrenadores_menu.add_command(label="Listado ")  

        agregos_menu = Menu(self.menu, tearoff = 0)
        agregos_menu.add_command(label="Contratar")
        agregos_menu.add_command(label="Modificar")
        agregos_menu.add_command(label="Despedir") 

        def agregar_usuario():
            usuario_agregar = UsuarioAgregar()
            
        def eliminar_usuario():                        
            eliminar_usuario = EliminarUsuario()        

        usuario_menu = Menu(self.menu, tearoff = 0)
        usuario_menu.add_command(label="Agregar", command=agregar_usuario)
        usuario_menu.add_command(label="Eliminar", command=eliminar_usuario)

        def agregar_nueva_licencia():                         
            nueva_licencia = NuevaLicencia()  

        def asistencia_pago_cliente_lobby():
            asistemcia_pago = AsistenciaYPago() 

        def control_pagos_lobby():
            pass 

        def extra_lobby():
            pass  

        def entrenadores_lobby():
            ent = Entrenadores()

        def nuevo_cliente_lobby():
            nc = Clientes()


        self.menu.add_cascade (label="Recepcion", command=asistencia_pago_cliente_lobby)
        self.menu.add_cascade (label="Control Pagos", command=control_pagos_lobby)
        self.menu.add_cascade (label="Extras", command=extra_lobby)
        self.menu.add_cascade (label="Entrenadores", command=entrenadores_lobby)
        self.menu.add_cascade (label="Clientes", command = nuevo_cliente_lobby) 
        self.menu.add_cascade (label="Economia", menu = economia_menu)               
        self.menu.add_cascade(label="Usuarios", menu = usuario_menu)
        self.menu.add_cascade(label = "Licencia", command= agregar_nueva_licencia)
        self.menu.add_cascade(label="Cerrar", command = cerrar_cesion)



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
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

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
                        user = "root",
                        password = "",
                        database = "gym_98mph"
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
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        self.label_nombre = CTkLabel(self,text = "Usuario:", font=("Times New Roman",14))
        self.label_nombre.place(x = 100 , y = 100)
        
        items_usuarios = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "gym_98mph"
            )
        cursor = conn.cursor()

        sql = """SELECT `Usuario` FROM `usuarios`;"""
        cursor.execute(sql)
        for index in cursor:
            items_usuarios.append(index[0])

        texto_nombre_usuario_eliminar = CTkComboBox(self, values=items_usuarios)
        texto_nombre_usuario_eliminar.place(x = 200 , y = 100) 


        def codigo_btn_eliminar_usuarios_eliminar():
            try:
                if texto_nombre_usuario_eliminar.get() == "gym_98mph":
                    error = messagebox.showinfo("Error", "Ese usuario no puede eliminarse")
                else:
                    for i in autorizacion:
                        if texto_nombre_usuario_eliminar.get() == i[0]:
                                    
                            cuidado = messagebox.askquestion("Delete","Se borrara el Usuario")
                            
                            if cuidado == "yes":
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
                                    user = "root",
                                    password = "",
                                    database = "gym_98mph"
                                    )
                                cursor = conn.cursor()
                                
                                usuario = texto_nombre_usuario_eliminar.get()   

                                sql = f"""DELETE FROM `usuarios` WHERE Usuario="{usuario}" """
                                cursor.execute(sql)
                                conn.commit()
                                texto_nombre_usuario_eliminar.delete(0,END)

                                ################ actualizar el listado de usuarios ###################

                                items_usuarios = []
                                sql = """SELECT `Usuario` FROM `usuarios`;"""
                                cursor.execute(sql)
                                for index in cursor:
                                    items_usuarios.append(index[0])

                                texto_nombre_usuario_eliminar['values'] = items_usuarios
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar el usuario")
                        


        def codigo_btn_cancelar_usuarios_eliminar():
            self.destroy()
            
        self.btn_eliminar = CTkButton(self,text="Eliminar",command=codigo_btn_eliminar_usuarios_eliminar, width = 150 , height = 30)
        self.btn_eliminar.place(x = 50 , y = 200)
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=codigo_btn_cancelar_usuarios_eliminar, width = 150 , height = 30)
        self.btn_cancelar.place(x = 220 , y = 200)  




# *****************************************************************************************
# ******************************** Asistencia y Pago **************************************
# *****************************************************************************************

class AsistenciaYPago(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Asistencia Cliente")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1300x700") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        try:
            global imagen_asistencia_cliente
            imagen_asistencia_cliente = CTkImage(Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/interrogante.jpg"), size = (700,700))
            
            self.label_imagen = CTkLabel(self, image = imagen_asistencia_cliente, width = 700, height = 700, text = "")
            self.label_imagen.place(x = 0 , y = 0)

        except:
            error = messagebox.showinfo("Error","No se encontro foto")


        def buscar_id(event):
            try:                   
                # si el buscador por id esta vacio 
                string_nombre.set("Este Id no esta asignado")
                string_modalidad.set("") 
                string_entrenador.set("") 
                string_pago.set("") 
                string_ultima_asistencia.set("") 
                string_telefono.set("")

                global imagen_asistencia_cliente
                imagen_asistencia_cliente = CTkImage(Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/interrogante.jpg"), size = (700,700))

                self.label_imagen = CTkLabel(self, image = imagen_asistencia_cliente, width = 700, height = 700, text = "")
                self.label_imagen.place(x = 0 , y = 0)   
                
                # mostramos la info del cliente
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `clientes` WHERE `ID` = {self.texto_buscar_por_id.get()} """
                cursor.execute(sql) 
                for index in cursor:
                    string_nombre.set(index[1] + " " + index[2] + " " + index[3])
                    string_modalidad.set("Modalidad: " + index[4]) 
                    string_entrenador.set("Entrenador: " + index[5]) 
                    string_pago.set("Paga: " + str(index[8])) 
                    string_ultima_asistencia.set("Ultima Asistencia: " + str(index[7])) 
                    string_telefono.set("Telefono: " + str(index[6]))               

                # mostramos la foto del cliente 

                try:
                    string = f"D:/gym_98MPH/fotos_gym/gym_Clientes/{self.texto_buscar_por_id.get()}.jpg"                    
                    imagen_asistencia_cliente = CTkImage(Image.open(string), size = (700,700))   

                    self.label_imagen = CTkLabel(self, image = imagen_asistencia_cliente, width = 700, height = 700, text = "")
                    self.label_imagen.place(x = 0 , y = 0)                  
                    
                except:
                    pass   

                self.texto_buscar_por_nombre.delete(0,END)                             

            except:
                pass        


        def buscar_nombre(event): 
            global vent_nombre
            try:
                vent_nombre.destroy()
            except:
                pass

            vent_nombre = CTkToplevel()
            vent_nombre.title("Buscar por Nombre") 
            htotal = vent_nombre.winfo_screenheight()
            wtotal = vent_nombre.winfo_screenwidth()
            wventana = 300
            hventana = 400
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            vent_nombre.geometry(f"+{posx}+{posy}")
            vent_nombre.lift()
            vent_nombre.attributes('-topmost', True)
            vent_nombre.after(200, lambda: vent_nombre.attributes('-topmost', False)) 
            vent_nombre.after(250, lambda: vent_nombre.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico')) 

            estilos_tablas()

            # vamos a hacer la tabla para mostrar el nombre completo 
            tabla = ttk.Treeview(vent_nombre, columns = ("Nombre Completo",),show="headings")
            tabla.column("#0", width = 40)
            tabla.column("Nombre Completo", width = 300,anchor="center")
            
            tabla.pack()            

            tabla.heading("#0", text = "Id")
            tabla.heading("Nombre Completo", text = "Nombre Completo",anchor="center")            

            scrollbar = CTkScrollbar(vent_nombre, command = tabla.yview, width = 18)
            scrollbar.place(in_ = tabla, relheigh = 1, relx = 1)

            tabla.config(yscrollcommand = scrollbar.set)

            # ahora hay que llenar la tabla con los nombres y apellidos correctos 
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "gym_98MPH"
                )
            cursor = conn.cursor()

            sql = f""" SELECT `Id`, `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE `Nombre` LIKE '%{self.texto_buscar_por_nombre.get()}%' OR `Apellido 1` LIKE '%{self.texto_buscar_por_nombre.get()}%' OR `Apellido 2` LIKE '%{self.texto_buscar_por_nombre.get()}%' """
            cursor.execute(sql) 
            for index in cursor:
                tabla.insert("",END, text = index[0], values=(index[1] + " " + index[2] + " " + index[3],))

            # ahora cuando demos 2ble click en el nombre seleccionado se mostrara su info
            def seleccion_nombre(event):                
                # vamos a capturar el codigo del numero que vamos a reabastecer
                seleccion = tabla.selection()
                if seleccion:
                    item = seleccion[0]                
                    id_cliente = tabla.item(item, "text") 

                self.texto_buscar_por_id.delete(0,END)
                self.texto_buscar_por_id.insert(0,id_cliente)
                buscar_id(True)
                vent_nombre.destroy()

            tabla.bind("<Double-1>", seleccion_nombre)

        # ********************* buscadores 

        self.texto_buscar_por_id = CTkEntry(self, placeholder_text="Buscar por Id ...")
        self.texto_buscar_por_id.place(x = 730, y = 30)

        self.texto_buscar_por_id.bind("<KeyRelease>", buscar_id) 

        self.texto_buscar_por_nombre = CTkEntry(self, placeholder_text="Buscar por Nombre ...")
        self.texto_buscar_por_nombre.place(x = 1100, y = 30)

        self.texto_buscar_por_nombre.bind("<KeyRelease>", buscar_nombre) 


        # info del cliente 

        string_nombre = StringVar()
        string_nombre.set("Nombre y Apellidos")

        self.label_nombre = CTkLabel(self,textvariable = string_nombre, font=("Times New Roman",18))
        self.label_nombre.place(x = 730, y = 200)

        string_modalidad = StringVar()
        string_modalidad.set("Modalidad") 

        self.label_modalidad = CTkLabel(self,textvariable = string_modalidad, font=("Times New Roman",18))
        self.label_modalidad.place(x = 730, y = 240)

        string_entrenador = StringVar()
        string_entrenador.set("Entrenador") 

        self.label_entrenador = CTkLabel(self,textvariable = string_entrenador, font=("Times New Roman",18))
        self.label_entrenador.place(x = 730, y = 280)

        string_pago = StringVar()
        string_pago.set("Proximo Pago")

        self.label_pago = CTkLabel(self,textvariable = string_pago, font=("Times New Roman",18))
        self.label_pago.place(x = 730, y = 320)
        
        string_ultima_asistencia = StringVar()
        string_ultima_asistencia.set("Ultima Asistencia")

        self.label_ultima_asistencia = CTkLabel(self,textvariable = string_ultima_asistencia, font=("Times New Roman",18))
        self.label_ultima_asistencia.place(x = 730, y = 360) 

        string_telefono = StringVar()
        string_telefono.set("Telefono")

        self.label_ultima_asistencia = CTkLabel(self,textvariable = string_telefono, font=("Times New Roman",18))
        self.label_ultima_asistencia.place(x = 730, y = 400) 

        # ahora vamos a mostrar el boton de asistencia 
        def asistencia():
            conf = messagebox.askokcancel("Confirmar","Se va a tomar la asistencia")
            if conf:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = f""" UPDATE `clientes` SET `Ultima_Asistencia`='{fecha_actual}' WHERE `ID` = {self.texto_buscar_por_id.get()} """
                cursor.execute(sql)
                conn.commit()

                buscar_id(True)

        self.btn_asistencia = CTkButton(self,text="Asistencia",command=asistencia,width=200,height=50)
        self.btn_asistencia.place(x=730, y= 500)

        def pagar():
            conf = messagebox.askokcancel("Confirmar","Se va a cobrar al cliente")
            if conf:
                # busquemos la info que se agregara en el pago
                # busquemos el id del pago
                
                id_pago = 1
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = """SELECT MAX(id) FROM `pagos`;"""
                cursor.execute(sql)
                for index in cursor:
                    if index[0] == None:
                        pass

                    else:
                        id_pago = index[0] + 1  

                # busquemos la info del cliente 
                modalidad = ""
                nombre_completo = ""
                trabajador = ""
                fecha_pago = ""
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `clientes` WHERE `ID` = {self.texto_buscar_por_id.get()} """
                cursor.execute(sql)
                for index in cursor:
                    modalidad = index[4]
                    nombre_completo = index[1] + " " + index[2] + " " + index[3]
                    trabajador = index[5]
                    fecha_pago = index[8]

                fecha_pago = fecha_pago + relativedelta(months=1)

                # busquemos cuanto pagara de importe y al entrenador 
                pago_importe = 0
                pago_entrenador = 0
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `modalidad` WHERE `modalidad` = "{modalidad}" """
                cursor.execute(sql)
                for index in cursor:
                    pago_importe = index[1]
                    pago_entrenador = index[2]

                # ahora hagamos el pago
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = f""" INSERT INTO `pagos`(`fecha`, `id`, `nombre_completo`, `modalidad`, `Trabajador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{fecha_actual}','{id_pago}','{nombre_completo}','{modalidad}','{trabajador}','NO','{pago_importe}','{pago_entrenador}') """
                cursor.execute(sql)
                conn.commit()

                # ahora hay que modificar la fecha del proximo pago en la tabla clientes
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = f""" UPDATE `clientes` SET `Ultima_Asistencia`='{fecha_actual}',`Fecha_Pago`='{fecha_pago}' WHERE `ID` = {self.texto_buscar_por_id.get()} """
                cursor.execute(sql)
                conn.commit()

                # ahora actualizar la ventana 
                buscar_id(True)                

        self.btn_pagar = CTkButton(self,text="Pagar",command=pagar,width=200,height=50)
        self.btn_pagar.place(x=1000, y= 500)



# **********************************************************************************
# ***************************** Entrenadores ***************************************
# **********************************************************************************

class Entrenadores(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Entrenadores")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))                

        estilos_tablas()  

        self.tabla = ttk.Treeview(self, columns = ())
        self.tabla.column("#0", width = 500)

        self.tabla.place(x = 100, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Entrenadores")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def on_click(event):            
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                nombre = self.tabla.item(item, "text") 

            # ahora eliminar el entrenador
            try:
                string = f"Vas a eliminar a {nombre} de los entrenadores"
                conf = messagebox.askokcancel("Confirmar",string)    
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98MPH"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `entrenadores` WHERE `nombre` = "{nombre}" """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()

                    term = messagebox.showinfo("Terminado","Se ha eliminado el trabajador")
                    nombre_trabajadores = None

            except:
                error = messagebox.showerror("Error","Selecciona un trabajador para eliminar") 

        self.tabla.bind("<Double-1>", on_click)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "gym_98MPH"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `entrenadores`;"""
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

            temp.texto_nombre = CTkEntry(temp, placeholder_text="Entrenador ...")
            temp.texto_nombre.pack(pady = 10)

            def aceptar():
                if temp.texto_nombre.get() == "":
                    error = messagebox.showerror("Error","Debes escribir algun nombre")
                else:
                    # vemos que no se repita el trabajador
                    repetido = False
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98MPH"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `entrenadores` """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == temp.texto_nombre.get():
                            repetido = True
                            error = messagebox.showerror("Error","Ese trabajador ya existe")

                    if not repetido:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "gym_98MPH"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `entrenadores`(`Nombre`) VALUES ('{temp.texto_nombre.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla()

                        term = messagebox.showinfo("Terminado","Se ha agregado el entrenador")
                        temp.destroy()

            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)              


        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 50)
        self.btn_agregar.place(x = 100, y = 400)      






























# ************************* estoy trabajando 




# **********************************************************************************
# ********************************** Nuevo Cliente *********************************
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
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 


        # ************************** Seccion Modificar y Eliminar ********************
        self.label1 = CTkLabel(self,text="-------------------- Modificar o Eliminar --------------------", font=("Times New Roman",16))
        self.label1.place(x = 100, y = 30) 

        # ******************** buscador
        self.texto_buscar_id = CTkEntry(self, placeholder_text="Buscar por id ...")
        self.texto_buscar_id.place(x = 100, y = 110) 

        self.texto_buscar_nombre = CTkEntry(self, placeholder_text="Buscar por nombre ...")
        self.texto_buscar_nombre.place(x = 330, y = 110) 

        # ******************** tabla 
        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Modalidad", "Entrenador"), show="headings")
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre", width = 300)
        self.tabla.column("Modalidad", width = 100)
        self.tabla.column("Entrenador", width = 100)        

        self.tabla.place(x = 100, y = 200)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Modalidad", text = "Modalidad")
        self.tabla.heading("Entrenador", text = "Entrenador")
        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "gym_98MPH"
                )
            cursor = conn.cursor()

            if self.texto_buscar_id.get() == "":
                sql = f""" SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2`, `Modalidad`, `Trabajador` FROM `clientes` WHERE `Nombre` LIKE '%{self.texto_buscar_nombre.get()}%' OR `Apellido 1` LIKE '%{self.texto_buscar_nombre.get()}%' OR `Apellido 2` LIKE '%{self.texto_buscar_nombre.get()}%' """
            
            else:
                sql = f""" SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2`, `Modalidad`, `Trabajador` FROM `clientes` WHERE `ID` = '{self.texto_buscar_id.get()}' AND (`Nombre` LIKE '%{self.texto_buscar_nombre.get()}%' OR `Apellido 1` LIKE '%{self.texto_buscar_nombre.get()}%' OR `Apellido 2` LIKE '%{self.texto_buscar_nombre.get()}%') """
            cursor.execute(sql)
            for index in cursor:                
                self.tabla.insert("",END, text = index[0], values=(index[1] + " " + index[2] + " " + index[3],index[4],index[5],))

        llenar_tabla(True)

        self.texto_buscar_id.bind("<KeyRelease>", llenar_tabla) 
        self.texto_buscar_nombre.bind("<KeyRelease>", llenar_tabla) 





        # ************************** Seccion Agregar cliente  *************************      
        self.label2 = CTkLabel(self,text="-------------------- Agregar Cliente --------------------", font=("Times New Roman",16))
        self.label2.place(x = 650, y = 30)  

        ultimo_id = StringVar()
        ultimo_id.set("")

        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "gym_98MPH"
            )
        cursor = conn.cursor()

        sql = """SELECT MAX(ID) FROM `clientes`;"""
        cursor.execute(sql)        
        for index in cursor:                
            ultimo_id.set(index[0])

        if ultimo_id is None:
            ultimo_id = "No hay clientes"

        label_ultimo_id = CTkLabel(self, textvariable = ultimo_id)
        label_ultimo_id.place(x = 650, y = 70)         

        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 738, y = 70)   

        self.texto_id = CTkEntry(self)
        self.texto_id.place(x = 800, y = 70)     

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 110) 
        
        self.texto_nombre = CTkEntry(self)
        self.texto_nombre.place(x = 800, y = 110)      

        self.label_apellido1 = CTkLabel(self,text="Apellido 1:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 692, y = 150)  
    
        self.texto_apellido1 = CTkEntry(self)
        self.texto_apellido1.place(x = 800, y = 150)            

        self.label_apellido2 = CTkLabel(self,text="Apellido 2:", font=("Times New Roman",16))
        self.label_apellido2.place(x = 692, y = 190)  

        self.texto_apellido2 = CTkEntry(self)
        self.texto_apellido2.place(x = 800, y = 190)           

        self.label_modalidad = CTkLabel(self,text="Modalidad:", font=("Times New Roman",16))
        self.label_modalidad.place(x = 684, y = 230)  

        items_modalidad = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "gym_98MPH"
            )
        cursor = conn.cursor()

        sql = """SELECT `modalidad` FROM `modalidad`"""
        cursor.execute(sql)
        for index in cursor:
            items_modalidad.append(index[0])
        
        self.texto_modalidad = CTkComboBox(self, values=items_modalidad)
        self.texto_modalidad.set("")              
        self.texto_modalidad.place(x = 800, y = 230)                

        self.label_entrenador = CTkLabel(self,text="Entrenador:", font=("Times New Roman",16))
        self.label_entrenador.place(x = 681, y = 270) 

        items_entrenador = []
        sql = """SELECT * FROM `entrenadores`"""
        cursor.execute(sql)
        for index in cursor:
            items_entrenador.append(index[0])
        
        self.texto_entrenador = CTkComboBox(self,values=items_entrenador)
        self.texto_entrenador.set("")
        self.texto_entrenador.place(x = 800, y = 270)              

        self.label_ultima_asistencia = CTkLabel(self,text="Ultima Asistencia:", font=("Times New Roman",16))
        self.label_ultima_asistencia.place(x = 650, y = 310) 
        
        self.texto_asistencia = CTkEntry(self)
        self.texto_asistencia.place(x = 800, y = 310)              

        self.label_fecha_pago = CTkLabel(self,text="Pago:", font=("Times New Roman",16))
        self.label_fecha_pago.place(x = 725, y = 350) 
        
        self.texto_fecha_pago = CTkEntry(self)
        self.texto_fecha_pago.place(x = 800, y = 350)              

        self.label_telefono = CTkLabel(self,text="Telefono:", font=("Times New Roman",16))
        self.label_telefono.place(x = 700, y = 390)
        
        self.texto_telefono = CTkEntry(self)
        self.texto_telefono.place(x = 800, y = 390)  

        # ***************** Botones ************************
        def btn_fecha_agregar_cliente(): 

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
                self.texto_asistencia.delete(0,END)
                self.texto_fecha_pago.delete(0,END)

                fecha_select = cal.get_date()
                fecha = datetime.strptime(fecha_select, "%Y-%m-%d").date()              
                nueva_fecha = fecha + relativedelta(months=1)                

                self.texto_asistencia.insert(0,str(fecha_select))
                self.texto_fecha_pago.insert(0,str(nueva_fecha))

                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()       
            
        
        self.btn_fecha = CTkButton(self,text="...",command=btn_fecha_agregar_cliente, width = 27, height = 27)
        self.btn_fecha.place(x=950 ,y=310 )

        def agregar_cliente():
            # verifica que no dejen en blanco los campos importantes 
            avanzar = False
            if self.texto_fecha_pago.get() == "" or self.texto_asistencia.get() == "" or self.texto_entrenador.get() == "" or self.texto_modalidad.get() == "" or self.texto_apellido2.get() == "" or self.texto_apellido1.get() == "" or self.texto_nombre.get() == "" or self.texto_id.get() == "":
                error = messagebox.showerror("Error","Debe llenar todos los campos importantes")
            else:
                avanzar = True
            
            # verificar que el id no este repetido
            if avanzar:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT COUNT(`ID`) FROM `clientes` WHERE `ID` = {self.texto_id.get()} """
                cursor.execute(sql)
                for index in cursor:
                    if index[0] == 0:
                        pass
                    else:
                        avanzar = False
                        error = messagebox.showerror("Error","El id esta repetido")                
            
            # insertar el cliente en la bd 
            if avanzar:
                conf = messagebox.askokcancel("Confirmar","Se va a agregar el cliente a la base de datos")
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98MPH"
                        )
                    cursor = conn.cursor()

                    sql = f""" INSERT INTO `clientes`(`ID`, `Nombre`, `Apellido 1`, `Apellido 2`, `Modalidad`, `Trabajador`, `Telefono`, `Ultima_Asistencia`, `Fecha_Pago`) VALUES ('{self.texto_id.get()}','{self.texto_nombre.get()}','{self.texto_apellido1.get()}','{self.texto_apellido2.get()}','{self.texto_modalidad.get()}','{self.texto_entrenador.get()}','{self.texto_telefono.get()}','{self.texto_asistencia.get()}','{self.texto_fecha_pago.get()}') """
                    cursor.execute(sql)
                    conn.commit()

                    # ********************************** ahora generar el pago inicial de este cliente
                    # busquemos el id del pago
                    id_pago = 1
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98MPH"
                        )
                    cursor = conn.cursor()

                    sql = """SELECT MAX(id) FROM `pagos`;"""
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == None:
                            pass

                        else:
                            id_pago = index[0] + 1 
                    
                    # ahora hay que buscar el importe  y el pago al entrenador 
                    importe = 0
                    entrenador = 0
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98MPH"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT `precio`, `pago_entrenador` FROM `modalidad` WHERE `modalidad`  = "{self.texto_modalidad.get()}" """
                    cursor.execute(sql)
                    for index in cursor:
                        importe = index[0]
                        entrenador = index[1]                   


                    # ahora montamos el pago en la bd                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98MPH"
                        )
                    cursor = conn.cursor()

                    sql = f""" INSERT INTO `pagos`(`fecha`, `id`, `nombre_completo`, `modalidad`, `Trabajador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{fecha_actual}','{id_pago}','{self.texto_nombre.get() + " " + self.texto_apellido1.get() + " " + self.texto_apellido2.get()}','{self.texto_modalidad.get()}','{self.texto_entrenador.get()}','NO','{importe}','{entrenador}') """
                    cursor.execute(sql)
                    conn.commit()

                    self.destroy()   

        self.btn_aceptar = CTkButton(self,text="Agregar Cliente",command=agregar_cliente, width = 150, height = 40)
        self.btn_aceptar.place(x=730 ,y=500 )
        
        
































autenticacion = Autenticacion()
autenticacion.mainloop()
