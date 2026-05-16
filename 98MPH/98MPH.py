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
import os

fecha_actual = datetime.now().date()
fecha_hora_actual = datetime.now()
fecha_hora_actual = fecha_hora_actual.strftime("%Y-%m-%d %I:%M:%S %p")

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
    sql = """ CREATE TABLE `clientes` (`ID` int(11) NOT NULL, `Nombre` varchar(50) NOT NULL, `Apellido 1` varchar(50) NOT NULL, `Apellido 2` varchar(50) NOT NULL, `Modalidad` varchar(50) NOT NULL, `Trabajador` varchar(50) NOT NULL, `Telefono` varchar(50) NOT NULL,  `Ultima_Asistencia` varchar(50) NOT NULL,  `Fecha_Pago` date NOT NULL) ENGINE=InnoDB """
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
    sql = """ CREATE TABLE `pagos` (`id_pago` int(11) NOT NULL, `fecha` date NOT NULL,  `id` int(11) NOT NULL,  `nombre_completo` varchar(50) NOT NULL,  `modalidad` varchar(50) NOT NULL,  `Trabajador` varchar(50) NOT NULL,  `pagar_activacion` varchar(50) NOT NULL,  `importe` int(11) NOT NULL,  `pago_entrenador` int(11) NOT NULL) ENGINE=InnoDB """
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

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/1.jpg"), size = (400,200))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################     

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

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/7.jpg"), size = (300,200))  

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
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/lobby.jpg"), size = (1300,700))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################         
        
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

        def pago_entrenadores():
            pe = PagoEntrenadores()

        def atrasados():
            atr = Atrasados()

        def balance():
            bal = Balance()

        economia_menu = Menu(self.menu, tearoff = 0)   
        economia_menu.add_command(label="Balance",command=balance)        
        economia_menu.add_command(label="Pago Entrenadores",command=pago_entrenadores)
        economia_menu.add_command(label="Pagos Atrasados",command=atrasados)

        def entrenadores_lobby():
            ent = Entrenadores()

        def adm_extras_lobby():
            ent = Extras()

        def adm_modalidades_lobby():
            ent = Modalidades()
        
        administrativo_menu = Menu(self.menu, tearoff = 0)
        administrativo_menu.add_command(label="Entrenadores ",command=entrenadores_lobby)          
        administrativo_menu.add_command(label="Extras",command=adm_extras_lobby)          
        administrativo_menu.add_command(label="Modalidades",command=adm_modalidades_lobby)          

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
            cp = ControlPagos()

        def ejecutar_extra_lobby():
            ee = EjecutarExtra()       

        def clientes_lobby():
            nc = Clientes()

        def salva_lobby():           
            
            # Abrir diálogo para elegir dónde guardar el respaldo
            ruta_guardado = filedialog.asksaveasfilename(
                defaultextension=".sql",
                filetypes=[
                    ("Archivos SQL", "*.sql"),
                    ("Todos los archivos", "*.*")
                ],
                initialfile=f"gym_98mph_{fecha_actual}.sql",
                title="Guardar respaldo de la base de datos"
            )
            
            # Si el usuario canceló, salir
            if not ruta_guardado:
                return
            
            try:
                # Ruta de mysqldump en XAMPP (ajusta si es necesario)
                ruta_mysqldump = "C:/xampp/mysql/bin/mysqldump.exe"
                
                # Comando correcto: mysqldump -u root gym_98mph > archivo.sql
                comando = f'"{ruta_mysqldump}" -u root gym_98mph > "{ruta_guardado}"'
                
                # Ejecutar el comando
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                
                # Verificar que el archivo se creó y tiene contenido
                if os.path.exists(ruta_guardado) and os.path.getsize(ruta_guardado) > 0:
                    tamaño_kb = os.path.getsize(ruta_guardado) / 1024
                    messagebox.showinfo("Éxito", f"✅ Respaldo creado exitosamente!\n\n📁 Archivo: {ruta_guardado}\n📊 Tamaño: {tamaño_kb:.2f} KB")
                else:
                    error_msg = resultado.stderr if resultado.stderr else "No se pudo crear el respaldo"
                    messagebox.showerror("Error", f"❌ Error al crear respaldo:\n{error_msg}")
                    
            except FileNotFoundError:
                messagebox.showerror("Error", "No se encontró mysqldump.exe\nVerifica la ruta: C:/xampp/mysql/bin/mysqldump.exe")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error al crear respaldo:\n{str(e)}")


        self.menu.add_cascade (label="Recepcion", command=asistencia_pago_cliente_lobby)
        self.menu.add_cascade (label="Extras", command=ejecutar_extra_lobby)
        self.menu.add_cascade (label="Control Pagos", command=control_pagos_lobby)        
        self.menu.add_cascade (label="Clientes", command = clientes_lobby) 
        self.menu.add_cascade (label="Economia", menu = economia_menu)               
        self.menu.add_cascade (label="Administrativo", menu = administrativo_menu)               
        self.menu.add_cascade (label="Salva", command=salva_lobby)               
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

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (400,300))  

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

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (400,300))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################      

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

                    # para que se ponga en rojo si esta atrasado
                    if fecha_actual > index[8]:
                        self.label_pago.configure(fg_color="red")   

                    else:
                        self.label_pago.configure(fg_color="transparent")                


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
            global fecha_hora_actual
            fecha_hora_actual = datetime.now()
            fecha_hora_actual = fecha_hora_actual.strftime("%Y-%m-%d %I:%M:%S %p")

            conf = messagebox.askokcancel("Confirmar","Se va a tomar la asistencia")
            if conf:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = f""" UPDATE `clientes` SET `Ultima_Asistencia`='{fecha_hora_actual}' WHERE `ID` = {self.texto_buscar_por_id.get()} """
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

                sql = """SELECT MAX(id_pago) FROM `pagos`;"""
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

                sql = f""" INSERT INTO `pagos`(`id_pago`,`fecha`, `id`, `nombre_completo`, `modalidad`, `Trabajador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{id_pago}','{fecha_actual}','{self.texto_buscar_por_id.get()}','{nombre_completo}','{modalidad}','{trabajador}','NO','{pago_importe}','{pago_entrenador}') """
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

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/logo3.jpg"), size = (800,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################                

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


# **********************************************************************************
# ************************************ Extra ***************************************
# **********************************************************************************

class Extras(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Extras")    
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

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/10.jpg"), size = (800,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################              

        estilos_tablas()  

        self.tabla = ttk.Treeview(self, columns = ("Precio","Pago Entrenador"))
        self.tabla.column("#0", width = 200)
        self.tabla.column("Precio", width = 100)
        self.tabla.column("Pago Entrenador", width = 150)

        self.tabla.place(x = 100, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Extra")
        self.tabla.heading("Precio", text = "Precio")
        self.tabla.heading("Pago Entrenador", text = "Pago Entrenador")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "gym_98MPH"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `extra`;"""
            cursor.execute(sql)

            for index in cursor:
                self.tabla.insert("",END, text = index[0], values=(index[1],index[2],))

        llenar_tabla()

        def on_click(event):            
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                nombre = self.tabla.item(item, "text") 

            # ahora eliminar la modalidad
            try:
                string = f"Vas a eliminar a {nombre} de los extras"
                conf = messagebox.askokcancel("Confirmar",string)    
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98MPH"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `extra` WHERE `extra` = "{nombre}" """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()
                    term = messagebox.showinfo("Terminado","Se ha eliminado la modalidad")
            except:
                error = messagebox.showerror("Error","Selecciona una modalidad para eliminar") 

        self.tabla.bind("<Double-1>", on_click)

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

            temp.texto_extra = CTkEntry(temp, placeholder_text="Extra ...")
            temp.texto_extra.pack(pady = 10)

            temp.texto_precio = CTkEntry(temp, placeholder_text="Pecio ...")
            temp.texto_precio.pack(pady = 10)

            temp.texto_entrenador = CTkEntry(temp, placeholder_text="Pago Entrenador ...")
            temp.texto_entrenador.pack(pady = 10)

            def aceptar():
                if temp.texto_extra.get() == "" or temp.texto_precio.get() == "" or temp.texto_entrenador.get() == "":
                    error = messagebox.showerror("Error","Debes llenar los campos")
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

                    sql = f""" SELECT * FROM `extra` """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == temp.texto_extra.get():
                            repetido = True
                            error = messagebox.showerror("Error","Ese extra ya existe")

                    if not repetido:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "gym_98MPH"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `extra`(`extra`, `precio`, `pago entrenador`) VALUES ('{temp.texto_extra.get()}','{temp.texto_precio.get()}','{temp.texto_entrenador.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla()

                        term = messagebox.showinfo("Terminado","Se ha agregado el entrenador")
                        temp.destroy()

            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)  
        
        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 50)
        self.btn_agregar.place(x = 100, y = 400) 
        


# **********************************************************************************
# ***************************** Modalidades ***************************************
# **********************************************************************************

class Modalidades(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Modalidades")    
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

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/10.jpg"), size = (800,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################                

        estilos_tablas()  

        self.tabla = ttk.Treeview(self, columns = ("Precio","Pago Entrenador"))
        self.tabla.column("#0", width = 200)
        self.tabla.column("Precio", width = 100)
        self.tabla.column("Pago Entrenador", width = 150)

        self.tabla.place(x = 100, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Modalidades")
        self.tabla.heading("Precio", text = "Precio")
        self.tabla.heading("Pago Entrenador", text = "Pago Entrenador")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "gym_98MPH"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `modalidad`;"""
            cursor.execute(sql)

            for index in cursor:
                self.tabla.insert("",END, text = index[0], values=(index[1],index[2],))

        llenar_tabla()

        def on_click(event):            
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                nombre = self.tabla.item(item, "text") 

            # ahora eliminar la modalidad
            try:
                string = f"Vas a eliminar a {nombre} de las modalidades"
                conf = messagebox.askokcancel("Confirmar",string)    
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98MPH"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `modalidad` WHERE `modalidad` = "{nombre}" """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()
                    term = messagebox.showinfo("Terminado","Se ha eliminado la modalidad")
            except:
                error = messagebox.showerror("Error","Selecciona una modalidad para eliminar") 

        self.tabla.bind("<Double-1>", on_click)

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

            temp.texto_modalidad = CTkEntry(temp, placeholder_text="Modalidad ...")
            temp.texto_modalidad.pack(pady = 10)

            temp.texto_precio = CTkEntry(temp, placeholder_text="Pecio ...")
            temp.texto_precio.pack(pady = 10)

            temp.texto_entrenador = CTkEntry(temp, placeholder_text="Pago Entrenador ...")
            temp.texto_entrenador.pack(pady = 10)

            def aceptar():
                if temp.texto_modalidad.get() == "" or temp.texto_precio.get() == "" or temp.texto_entrenador.get() == "":
                    error = messagebox.showerror("Error","Debes llenar los campos")
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

                    sql = f""" SELECT * FROM `modalidad` """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == temp.texto_modalidad.get():
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

                        sql = f""" INSERT INTO `modalidad`(`modalidad`, `precio`, `pago_entrenador`) VALUES ('{temp.texto_modalidad.get()}','{temp.texto_precio.get()}','{temp.texto_entrenador.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla()

                        term = messagebox.showinfo("Terminado","Se ha agregado el entrenador")
                        temp.destroy()

            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)  
        
        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 50)
        self.btn_agregar.place(x = 100, y = 400) 




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

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/7.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        ####################################################### 


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

        # ahora modificar o eliminar clientes 
        def on_click(event):
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                id_cliente = self.tabla.item(item, "text") 

            # ahora mostrar ventana para decidirr si elimino o modifico
            temp = CTkToplevel()
            temp.title("Opcicon") 
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

            def modificar():
                # mostramos la ventana para modificar
                mod = CTkToplevel()
                mod.title("Modificar Cliente")    
                htotal = mod.winfo_screenheight()
                wtotal = mod.winfo_screenwidth()
                wventana = 1000
                hventana = 600
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                mod.geometry(f"+{posx}+{posy}")
                mod.geometry("1000x600") 
                mod.resizable(False,False)
                mod.after(250, lambda: mod.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))   
                mod.lift()
                mod.attributes('-topmost', True)
                mod.after(200, lambda: mod.attributes('-topmost', False)) 

                ############ agregar el fondo de pantalla #########
      
                mod.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/1.jpg"), size = (1000,600))  

                mod.label_image = CTkLabel(mod, image = mod.imagen, text = "")  
                mod.label_image.place(x = 0, y = 0)      

                ####################################################### 

                # ******************* modificar cliente 
                mod.label_id = CTkLabel(mod,text="ID:", font=("Times New Roman",16))
                mod.label_id.place(x = 738, y = 70)   

                mod.texto_id = CTkEntry(mod)
                mod.texto_id.place(x = 800, y = 70)     

                mod.label_nombre = CTkLabel(mod,text="Nombre:", font=("Times New Roman",16))
                mod.label_nombre.place(x = 704, y = 110) 
                
                mod.texto_nombre = CTkEntry(mod)
                mod.texto_nombre.place(x = 800, y = 110)      

                mod.label_apellido1 = CTkLabel(mod,text="Apellido 1:", font=("Times New Roman",16))
                mod.label_apellido1.place(x = 692, y = 150)  
            
                mod.texto_apellido1 = CTkEntry(mod)
                mod.texto_apellido1.place(x = 800, y = 150)            

                mod.label_apellido2 = CTkLabel(mod,text="Apellido 2:", font=("Times New Roman",16))
                mod.label_apellido2.place(x = 692, y = 190)  

                mod.texto_apellido2 = CTkEntry(mod)
                mod.texto_apellido2.place(x = 800, y = 190)           

                mod.label_modalidad = CTkLabel(mod,text="Modalidad:", font=("Times New Roman",16))
                mod.label_modalidad.place(x = 684, y = 230)  

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
                
                mod.texto_modalidad = CTkComboBox(mod, values=items_modalidad)
                mod.texto_modalidad.set("")              
                mod.texto_modalidad.place(x = 800, y = 230)                

                mod.label_entrenador = CTkLabel(mod,text="Entrenador:", font=("Times New Roman",16))
                mod.label_entrenador.place(x = 681, y = 270) 

                items_entrenador = []
                sql = """SELECT * FROM `entrenadores`"""
                cursor.execute(sql)
                for index in cursor:
                    items_entrenador.append(index[0])
                
                mod.texto_entrenador = CTkComboBox(mod,values=items_entrenador)
                mod.texto_entrenador.set("")
                mod.texto_entrenador.place(x = 800, y = 270)              

                mod.label_ultima_asistencia = CTkLabel(mod,text="Ultima Asistencia:", font=("Times New Roman",16))
                mod.label_ultima_asistencia.place(x = 650, y = 310) 
                
                mod.texto_asistencia = CTkEntry(mod)
                mod.texto_asistencia.place(x = 800, y = 310)              

                mod.label_fecha_pago = CTkLabel(mod,text="Pago:", font=("Times New Roman",16))
                mod.label_fecha_pago.place(x = 725, y = 350) 
                
                mod.texto_fecha_pago = CTkEntry(mod)
                mod.texto_fecha_pago.place(x = 800, y = 350)              

                mod.label_telefono = CTkLabel(mod,text="Telefono:", font=("Times New Roman",16))
                mod.label_telefono.place(x = 700, y = 390)
                
                mod.texto_telefono = CTkEntry(mod)
                mod.texto_telefono.place(x = 800, y = 390)  

                # ***************** Botones ************************
                def btn_fecha_modificar_cliente(): 

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
                        mod.texto_asistencia.delete(0,END)
                        mod.texto_fecha_pago.delete(0,END)

                        fecha_select = cal.get_date()
                        fecha = datetime.strptime(fecha_select, "%Y-%m-%d").date()              
                        nueva_fecha = fecha + relativedelta(months=1)                

                        mod.texto_asistencia.insert(0,str(fecha_select))
                        mod.texto_fecha_pago.insert(0,str(nueva_fecha))

                        calendario.destroy()

                    btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
                    btn.pack()       
                    
                
                mod.btn_fecha2 = CTkButton(self,text="...",command=btn_fecha_modificar_cliente, width = 27, height = 27)
                mod.btn_fecha2.place(x=950 ,y=310 )

                # ahora vamos a mostrar los datos que estaban antes 
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()                   
                sql = f""" SELECT * FROM `clientes` WHERE `ID` = {id_cliente} """
                cursor.execute(sql)
                for index in cursor:
                    mod.texto_id.insert(0,index[0])
                    mod.texto_nombre.insert(0,index[1])
                    mod.texto_apellido1.insert(0,index[2])
                    mod.texto_apellido2.insert(0,index[3])
                    mod.texto_modalidad.set(index[4])
                    mod.texto_entrenador.set(index[5])
                    mod.texto_telefono.insert(0,index[6])
                    mod.texto_asistencia.insert(0,index[7])
                    mod.texto_fecha_pago.insert(0,index[8])

                def modificar_cliente():
                     conf = messagebox.askokcancel("Confirmar","Se va a modificar el cliente")
                     if conf:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "gym_98MPH"
                            )
                        cursor = conn.cursor()                   
                        sql = f""" UPDATE `clientes` SET `ID`='{mod.texto_id.get()}',`Nombre`='{mod.texto_nombre.get()}',`Apellido 1`='{mod.texto_apellido1.get()}',`Apellido 2`='{mod.texto_apellido2.get()}',`Modalidad`='{mod.texto_modalidad.get()}',`Trabajador`='{mod.texto_entrenador.get()}',`Telefono`='{mod.texto_telefono.get()}',`Ultima_Asistencia`='{mod.texto_asistencia.get()}',`Fecha_Pago`='{mod.texto_fecha_pago.get()}' WHERE `ID` = {id_cliente} """
                        cursor.execute(sql)
                        conn.commit()

                        mod.destroy()
                        temp.destroy()
                        llenar_tabla(True)

                mod.btn_moificar = CTkButton(mod,text="Modificar Cliente",command=modificar_cliente, width = 150, height = 40)
                mod.btn_moificar.place(x=730 ,y=500 )

            btn1 = CTkButton(temp,text="Modificar",command=modificar)
            btn1.pack(pady=20)

            def eliminar():
                conf = messagebox.askokcancel("Eliminar","Se va a eliminar el cliente")
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98MPH"
                        )
                    cursor = conn.cursor()                   
                    sql = f""" DELETE FROM `clientes` WHERE `ID` = {id_cliente} """
                    cursor.execute(sql)
                    conn.commit()

                    #**************** actualizar el ultimo_id
                    global ultimo_id
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

                    temp.destroy()
                    llenar_tabla(True)

            btn2 = CTkButton(temp,text="Eliminar",command=eliminar)
            btn2.pack(pady=20)

        self.tabla.bind("<Double-1>", on_click)

        # ************************** Seccion Agregar cliente  *************************  
        global fecha_hora_actual
        fecha_hora_actual = datetime.now()
        fecha_hora_actual = fecha_hora_actual.strftime("%Y-%m-%d %I:%M:%S %p")  

        self.label2 = CTkLabel(self,text="-------------------- Agregar Cliente --------------------", font=("Times New Roman",16))
        self.label2.place(x = 650, y = 30)  

        global ultimo_id
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
        self.texto_asistencia.insert(0,fecha_hora_actual)
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
                self.texto_fecha_pago.delete(0,END)

                fecha_select = cal.get_date()          
                self.texto_fecha_pago.insert(0,str(fecha_select))

                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()       
            
        
        self.btn_fecha = CTkButton(self,text="...",command=btn_fecha_agregar_cliente, width = 27, height = 27)
        self.btn_fecha.place(x=950 ,y=350 )

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

                    sql = """SELECT MAX(id_pago) FROM `pagos`;"""
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

                    sql = f""" INSERT INTO `pagos`(`id_pago`,`fecha`, `id`, `nombre_completo`, `modalidad`, `Trabajador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{id_pago}','{fecha_actual}','{self.texto_id.get()}','{self.texto_nombre.get() + " " + self.texto_apellido1.get() + " " + self.texto_apellido2.get()}','{self.texto_modalidad.get()}','{self.texto_entrenador.get()}','NO','{importe}','{entrenador}') """
                    cursor.execute(sql)
                    conn.commit()

                    self.destroy()   

        self.btn_aceptar = CTkButton(self,text="Agregar Cliente",command=agregar_cliente, width = 150, height = 40)
        self.btn_aceptar.place(x=730 ,y=500 )
        


# **********************************************************************************
# ********************************** Control Pagos *********************************
# **********************************************************************************
class ControlPagos(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Control Pagos") 
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700")
        self.resizable(False,False)        
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/2.jpg"), size = (1000,700))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        ####################################################### 

        self.texto_fecha = CTkEntry(self, placeholder_text="Fecha ...")
        self.texto_fecha.place(x=50,y=100) 

        self.texto_nombre = CTkEntry(self,placeholder_text="Buscar por Nombre...")
        self.texto_nombre.place(x=500,y=100) 

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Fecha","Id","Nombre Completo", "Modalidad", "Entrenador", "Importe", "P Entrenador"), show="headings")
        self.tabla.column("#0", width = 100)
        self.tabla.column("Fecha", width = 75)
        self.tabla.column("Id", width = 75)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("Modalidad", width = 100)
        self.tabla.column("Entrenador", width = 100)        
        self.tabla.column("Importe", width = 100)        
        self.tabla.column("P Entrenador", width = 100)        

        self.tabla.place(x = 50, y = 200)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id")
        self.tabla.heading("Fecha", text = "Fecha")
        self.tabla.heading("Id", text = "Id")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("Modalidad", text = "Modalidad")
        self.tabla.heading("Entrenador", text = "Entrenador")
        self.tabla.heading("Importe", text = "Importe")
        self.tabla.heading("P Entrenador", text = "P Entrenador")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def btn_fecha(): 
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
                self.texto_fecha.delete(0,END)
                self.texto_fecha.delete(0,END)
                fecha_select = cal.get_date()
                self.texto_fecha.insert(0,str(fecha_select)) 
                calendario.destroy()
                llenar_tabla(True)

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()             
        
        self.btn_fecha = CTkButton(self,text="...",command=btn_fecha, width = 27, height = 27)
        self.btn_fecha.place(x=200 ,y=100 )
        
        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "gym_98MPH"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM `pagos` WHERE `fecha` = "{self.texto_fecha.get()}" AND `nombre_completo` LIKE '%{self.texto_nombre.get()}%' """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values=(index[1],index[2],index[3],index[4],index[5],index[7],index[8],))
        
        self.texto_nombre.bind("<KeyRelease>", llenar_tabla) 

        def on_click(event):
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                id_pago = self.tabla.item(item, "text") 

            # ahora mostrar ventana para decidirr si elimino o modifico
            temp = CTkToplevel()
            temp.title("Opcicon") 
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

            def modificar():
                # mostramos la ventana para modificar
                mod = CTkToplevel()
                mod.title("Modificar Pago")    
                htotal = mod.winfo_screenheight()
                wtotal = mod.winfo_screenwidth()
                wventana = 1000
                hventana = 600
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                mod.geometry(f"+{posx}+{posy}")
                mod.geometry("1000x600") 
                mod.resizable(False,False)
                mod.after(250, lambda: mod.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))   
                mod.lift()
                mod.attributes('-topmost', True)
                mod.after(200, lambda: mod.attributes('-topmost', False)) 

                ############ agregar el fondo de pantalla #########
      
                mod.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/1.jpg"), size = (1000,600))  

                mod.label_image = CTkLabel(mod, image = mod.imagen, text = "")  
                mod.label_image.place(x = 0, y = 0)      

                ####################################################### 

                #********************* info
                mod.label_fecha = CTkLabel(mod,text="Fecha:", font=("Times New Roman",16))
                mod.label_fecha.place(x = 650, y = 50) 
                
                mod.texto_fecha = CTkEntry(mod)
                mod.texto_fecha.place(x = 800, y = 50)

                # ***************** Botones ************************
                def btn_fecha(): 
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
                        mod.texto_fecha.delete(0,END)
                        fecha_select = cal.get_date()
                        mod.texto_fecha.insert(0,str(fecha_select))
                        calendario.destroy()

                    btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
                    btn.pack()                 
                
                mod.btn_fecha2 = CTkButton(mod,text="...",command=btn_fecha, width = 27, height = 27)
                mod.btn_fecha2.place(x=950 ,y=50 )

                mod.label_id = CTkLabel(mod,text="Id cliente:", font=("Times New Roman",16))
                mod.label_id.place(x = 650, y = 90) 
                
                mod.texto_id = CTkEntry(mod)
                mod.texto_id.place(x = 800, y = 90)

                mod.label_nombre = CTkLabel(mod,text="Nombre Completo:", font=("Times New Roman",16))
                mod.label_nombre.place(x = 650, y = 130) 
                
                mod.texto_nombre = CTkEntry(mod)
                mod.texto_nombre.place(x = 800, y = 130)

                mod.label_modalidad = CTkLabel(mod,text="Modalidad:", font=("Times New Roman",16))
                mod.label_modalidad.place(x = 650, y = 170)  

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
                
                mod.texto_modalidad = CTkComboBox(mod, values=items_modalidad)
                mod.texto_modalidad.set("")              
                mod.texto_modalidad.place(x = 800, y = 170)  

                mod.label_entrenador = CTkLabel(mod,text="Entrenador:", font=("Times New Roman",16))
                mod.label_entrenador.place(x = 650, y = 210) 

                items_entrenador = []
                sql = """SELECT * FROM `entrenadores`"""
                cursor.execute(sql)
                for index in cursor:
                    items_entrenador.append(index[0])
                
                mod.texto_entrenador = CTkComboBox(mod,values=items_entrenador)
                mod.texto_entrenador.set("")
                mod.texto_entrenador.place(x = 800, y = 210)  

                mod.label_importe = CTkLabel(mod,text="Importe:", font=("Times New Roman",16))
                mod.label_importe.place(x = 650, y = 250) 
                
                mod.texto_importe = CTkEntry(mod)
                mod.texto_importe.place(x = 800, y = 250)

                mod.label_p_e = CTkLabel(mod,text="Pago Enrenador:", font=("Times New Roman",16))
                mod.label_p_e.place(x = 650, y = 290) 
                
                mod.texto_p_e = CTkEntry(mod)
                mod.texto_p_e.place(x = 800, y = 290)

                # ahora vamos a mostrar los datos que estaban antes 
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()                   
                sql = f""" SELECT * FROM `pagos` WHERE `id_pago` = {id_pago} """
                cursor.execute(sql)
                for index in cursor:
                    mod.texto_fecha.insert(0,index[1])
                    mod.texto_id.insert(0,index[2])                    
                    mod.texto_nombre.insert(0,index[3])                    
                    mod.texto_modalidad.set(index[4])
                    mod.texto_entrenador.set(index[5])
                    mod.texto_importe.insert(0,index[7])
                    mod.texto_p_e.insert(0,index[8])

                def modificar_pago():
                     conf = messagebox.askokcancel("Confirmar","Se va a modificar el pago")
                     if conf:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "gym_98MPH"
                            )
                        cursor = conn.cursor()                   
                        sql = f""" UPDATE `pagos` SET `fecha`='{mod.texto_fecha.get()}',`id`='{mod.texto_id.get()}',`nombre_completo`='{mod.texto_nombre.get()}',`modalidad`='{mod.texto_modalidad.get()}',`Trabajador`='{mod.texto_entrenador.get()}',`importe`='{mod.texto_importe.get()}',`pago_entrenador`='{mod.texto_p_e.get()}' WHERE `id_pago` = {id_pago}"""
                        cursor.execute(sql)
                        conn.commit()

                        mod.destroy()
                        temp.destroy()
                        llenar_tabla(True)

                mod.btn_moificar = CTkButton(mod,text="Modificar Pago",command=modificar_pago, width = 150, height = 40)
                mod.btn_moificar.place(x=730 ,y=500 )

            btn1 = CTkButton(temp,text="Modificar",command=modificar)
            btn1.pack(pady=20)

            def eliminar():
                conf = messagebox.askokcancel("Eliminar","Se va a eliminar el pago")
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98MPH"
                        )
                    cursor = conn.cursor()                   
                    sql = f""" DELETE FROM `pagos` WHERE `id_pago` = {id_pago} """
                    cursor.execute(sql)
                    conn.commit()                    

                    temp.destroy()
                    llenar_tabla(True)

            btn2 = CTkButton(temp,text="Eliminar",command=eliminar)
            btn2.pack(pady=20)

        self.tabla.bind("<Double-1>", on_click)



# **********************************************************************************
# ********************************* Ejecutar Extra *********************************
# **********************************************************************************
class EjecutarExtra(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Ejecutar Extra") 
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700")
        self.resizable(False,False)        
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/fondo_agregar_cliente.jpg"), size = (1000,700))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        ####################################################### 

        self.texto_id = CTkEntry(self, placeholder_text="Id cliente ...")
        self.texto_id.place(x=750,y=100)  

        self.texto_nombre = CTkEntry(self, placeholder_text="Nombre ...")
        self.texto_nombre.place(x=750,y=140) 

        item_extra = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "gym_98mph"
            )
        cursor = conn.cursor()

        sql = """ SELECT `extra` FROM `extra` """
        cursor.execute(sql)
        for index in cursor:
            item_extra.append(index[0])

        self.texto_extra = CTkComboBox(self, values=item_extra)
        self.texto_extra.set("Extra ...")
        self.texto_extra.place(x=750,y=180)

        item_trabajador = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "gym_98mph"
            )
        cursor = conn.cursor()

        sql = """ SELECT * FROM `entrenadores` """
        cursor.execute(sql)
        for index in cursor:
            item_trabajador.append(index[0])

        self.texto_trabajador = CTkComboBox(self, values=item_trabajador)
        self.texto_trabajador.set("Trabajador ...")
        self.texto_trabajador.place(x=750,y=220)

        def ejecutar_extra():
            conf = messagebox.askokcancel("Confirmar", "Se va a ejecutar el extra")
            if conf:
                # ************ buscamos el id del pago 
                id_pago = 1
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = """SELECT MAX(id_pago) FROM `pagos`;"""
                cursor.execute(sql)
                for index in cursor:
                    if index[0] == None:
                        pass

                    else:
                        id_pago = index[0] + 1  

                # ****************** buscamos el importe y pago al entrenador 
                importe = 0
                p_e = 0

                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98MPH"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `extra` WHERE `extra` = "{self.texto_extra.get()}" """
                cursor.execute(sql)
                for index in cursor:
                    importe = index[1]
                    p_e = index[2]


                # cuando el id es de un cliente enonces se toma el nombre de la bd, si el id es 0 entonces se usa el campo
                nombre_completo = ""
                if self.texto_id.get() == 0:
                    nombre_completo = self.texto_nombre.get()

                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "gym_98mph"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT  `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE `ID` = {self.texto_id.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        nombre_completo = index[0] + " " + index[1] + " " + index[2]



                # ***************** ejecutamos el pago
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "gym_98mph"
                    )
                cursor = conn.cursor()

                sql = f""" INSERT INTO `pagos`(`id_pago`, `fecha`, `id`, `nombre_completo`, `modalidad`, `Trabajador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{id_pago}','{fecha_actual}','{self.texto_id.get()}','{nombre_completo}','{self.texto_extra.get()}','{self.texto_trabajador.get()}','NO','{importe}','{p_e}') """
                cursor.execute(sql)
                conn.commit()

                self.destroy()

        self.btn_ejecutar = CTkButton(self,text="Ejecutar",command=ejecutar_extra)
        self.btn_ejecutar.place(x=750,y=300)





# **********************************************************************************
# ************************************ Atrasados ***********************************
# **********************************************************************************
class Atrasados(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Atrasados") 
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700")
        self.resizable(False,False)        
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/logo3.jpg"), size = (1000,700))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################  

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "Modalidad", "Entrenador", "Debe Pagar", "Atraso"))
        self.tabla.column("#0", width = 100)       
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("Modalidad", width = 100)
        self.tabla.column("Entrenador", width = 100)        
        self.tabla.column("Debe Pagar", width = 100)        
        self.tabla.column("Atraso", width = 150)        

        self.tabla.place(x = 50, y = 200)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id")        
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("Modalidad", text = "Modalidad")
        self.tabla.heading("Entrenador", text = "Entrenador")
        self.tabla.heading("Debe Pagar", text = "Debe Pagar")
        self.tabla.heading("Atraso", text = "Atraso (Dias)")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        self.texto_nombre = CTkEntry(self, placeholder_text="Nombre ...")
        self.texto_nombre.place(x=50,y=100) 

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "gym_98MPH"
                )
            cursor = conn.cursor()

            sql = f""" SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2`, `Modalidad`, `Trabajador`, `Fecha_Pago` FROM `clientes` WHERE `Fecha_Pago` < "{fecha_actual}" AND (`Nombre` LIKE '%{self.texto_nombre.get()}%' OR `Apellido 1` LIKE '%{self.texto_nombre.get()}%' OR `Apellido 2` LIKE '%{self.texto_nombre.get()}%') """
            cursor.execute(sql)
            for index in cursor:                   
                self.tabla.insert("",END, text = index[0], values=(index[1] + " " + index[2] + " " + index[3],index[4],index[5],index[6],(fecha_actual - index[6]).days,))                

        llenar_tabla(True)

        self.texto_nombre.bind("<KeyRelease>", llenar_tabla) 

        # ahora vamos a hacer el boton de exportar esa tabla 
        def exportar():
            try:
                rows = []
                for item in self.tabla.get_children():
                    # Obtener el text (primera columna) y los values (resto de columnas)
                    text = self.tabla.item(item)['text']
                    values = self.tabla.item(item)['values']
                    
                    # Combinar text + values en una sola fila
                    rows.append([text] + list(values))

                # Ajustar los nombres de columnas: ahora la primera es la del text
                df = pd.DataFrame(rows, columns=["ID", "Nombre Completo", "Modalidad", "Entrenador", "Debe Pagar", "Atraso (Dias)"])      
                
                # Nombre sugerido del archivo
                nombre_sugerido = "atrasados.xlsx"
                
                # Diálogo para guardar archivo
                ruta_guardado = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[
                        ("Archivos de Excel", "*.xlsx"),
                        ("Todos los archivos", "*.*")
                    ],
                    initialfile=nombre_sugerido,
                    title="Guardar archivo Excel"
                )
                
                # Si el usuario seleccionó una ruta (no canceló)
                if ruta_guardado:
                    df.to_excel(ruta_guardado, index=False)
                    messagebox.showinfo("Exportar", f"¡Exportado exitosamente!\n\nGuardado en:\n{ruta_guardado}")
                else:
                    messagebox.showinfo("Cancelado", "Exportación cancelada")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")


        self.btn = CTkButton(self,text="Exportar",command=exportar)
        self.btn.place(x=50,y=500)





# **********************************************************************************
# ****************************** Pago Entrenadores *********************************
# **********************************************************************************
class PagoEntrenadores(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Pago Entrenadores") 
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700")
        self.resizable(False,False)        
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/modificar cliente.jpg"), size = (1000,700))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        ####################################################### 

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Fecha","Id", "Nombre Completo", "Modalidad", "Entrenador", "Importe", "P Entrenador"),show="headings")
        self.tabla.column("#0", width = 100, anchor="center")       
        self.tabla.column("Fecha", width = 100, anchor="center")       
        self.tabla.column("Id", width = 100, anchor="center")       
        self.tabla.column("Nombre Completo", width = 300, anchor="center")
        self.tabla.column("Modalidad", width = 100, anchor="center")
        self.tabla.column("Entrenador", width = 100, anchor="center")        
        self.tabla.column("Importe", width = 100, anchor="center")        
        self.tabla.column("P Entrenador", width = 150, anchor="center")        

        self.tabla.place(x = 50, y = 200)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id_Pago", anchor="center")        
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Id", text = "Id", anchor="center")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo", anchor="center")
        self.tabla.heading("Modalidad", text = "Modalidad", anchor="center")
        self.tabla.heading("Entrenador", text = "Entrenador", anchor="center")
        self.tabla.heading("Importe", text = "Importe", anchor="center")
        self.tabla.heading("P Entrenador", text = "P Entrenador", anchor="center")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)        

        def llenar_tabla():
            v = 0
            b = 0
            i = 0
            e = 0
            t = 0            
            self.tabla.delete(*self.tabla.get_children())

            #******************** calculemos los totales 
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "gym_98MPH"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM `pagos` WHERE `fecha` >= "{self.texto_fecha_inicial.get()}" AND `fecha` < "{self.texto_fecha_final.get()}" AND `Trabajador` = "{self.texto_enrenador.get()}" """
            cursor.execute(sql)
            for index in cursor: 
                t+=index[8] 

                if index[4] == "Vip":
                    v+=index[8]

                elif index[4] == "Basico": 
                    b += index[8]

                elif index[4] == "Invitados":
                    i += index[8]

                else:
                    e += index[8]
                
                              
                self.tabla.insert("",END, text = index[0], values=(index[1],index[2],index[3],index[4],index[5],index[7],index[8],))     


            # llevemos los totales a los labels
            total_vip.set(f"Vip: {v}")
            total_basico.set(f"Basico: {b}")
            total_invitados.set(f"Invitados: {i}")
            total_extra.set(f"Extra: {e}")
            total.set(f"Total: {t}")

        
        self.texto_fecha_inicial = CTkEntry(self,placeholder_text="Fecha inicial ...")
        self.texto_fecha_inicial.insert(0,fecha_actual)
        self.texto_fecha_inicial.place(x=100,y=60) 

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
        self.btn_fecha_inicial.place(x=250 ,y=60 )

        self.texto_fecha_final = CTkEntry(self,placeholder_text="Fecha final ...")
        self.texto_fecha_final.insert(0,fecha_actual + timedelta(days=1))
        self.texto_fecha_final.place(x=100,y=100) 

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
        self.btn_fecha_final.place(x=250 ,y=100 )

        items_entrenador = []
        sql = """SELECT * FROM `entrenadores`"""
        cursor.execute(sql)
        for index in cursor:
            items_entrenador.append(index[0])

        def escoger_entrenador(event):
            llenar_tabla()

        self.texto_enrenador = CTkComboBox(self,values=items_entrenador,command=escoger_entrenador)
        self.texto_enrenador.set("Entrenador") 
        self.texto_enrenador.place(x=650,y=100) 

        # ahora vamos a configurar los totales que se muestran 
        total_vip = StringVar()
        total_vip.set("Vip: 0")

        self.label_vip = CTkLabel(self,textvariable=total_vip)
        self.label_vip.place(x=100,y=420)

        total_basico = StringVar()
        total_basico.set("Basico: 0")

        self.label_basico = CTkLabel(self,textvariable=total_basico)
        self.label_basico.place(x=100,y=460)

        total_invitados = StringVar()
        total_invitados.set("Invitados: 0")

        self.label_invitados = CTkLabel(self,textvariable=total_invitados)
        self.label_invitados.place(x=100,y=500)

        total_extra = StringVar()
        total_extra.set("Extra: 0")

        self.label_extra = CTkLabel(self,textvariable=total_extra)
        self.label_extra.place(x=100,y=540)

        total = StringVar()
        total.set("Total: 0")

        self.label_total = CTkLabel(self,textvariable=total)
        self.label_total.place(x=100,y=580)

        # ahora el boton de exportar la tabla 
        def exportar():
            try:
                if not self.tabla.get_children():
                    messagebox.showwarning("Sin datos", "No hay datos para exportar")
                    return
                
                rows = []
                for item in self.tabla.get_children():
                    values = self.tabla.item(item)['values']
                    rows.append(list(values))

                # DataFrame con las columnas que necesitas
                df = pd.DataFrame(rows, columns=["Fecha", "Id", "Nombre Completo", "Modalidad", "Entrenador", "Importe", "P Entrenador"])
                
                # Convertir columnas numéricas (si es necesario)
                df["Importe"] = pd.to_numeric(df["Importe"], errors='coerce')
                df["P Entrenador"] = pd.to_numeric(df["P Entrenador"], errors='coerce')
                
                # Calcular totales
                total_importe = df["Importe"].sum()
                total_p_entrenador = df["P Entrenador"].sum()
                
                # Agregar una fila vacía
                fila_vacia = pd.DataFrame([[""] * len(df.columns)], columns=df.columns)
                
                # Agregar fila de totales
                fila_totales = pd.DataFrame([["TOTAL", "", "", "", "", total_importe, total_p_entrenador]], columns=df.columns)
                
                # Concatenar: datos originales + fila vacía + totales
                df_final = pd.concat([df, fila_vacia, fila_totales], ignore_index=True)
                
                # Nombre sugerido del archivo
                nombre_sugerido = f"Pago {self.texto_enrenador.get()} {fecha_actual}.xlsx"
                
                # Diálogo para guardar archivo
                ruta_guardado = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[
                        ("Archivos de Excel", "*.xlsx"),
                        ("Todos los archivos", "*.*")
                    ],
                    initialfile=nombre_sugerido,
                    title="Guardar archivo Excel"
                )
                
                if ruta_guardado:
                    df_final.to_excel(ruta_guardado, index=False)
                    messagebox.showinfo("Exportar", f"¡Exportado exitosamente!\n\nGuardado en:\n{ruta_guardado}")
                else:
                    messagebox.showinfo("Cancelado", "Exportación cancelada")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")

        self.btn = CTkButton(self,text="Exportar",command=exportar)
        self.btn.place(x=600,y=500)


# **********************************************************************************
# ************************************** Balance ***********************************
# **********************************************************************************
class Balance(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Balance") 
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700")
        self.resizable(False,False)        
        self.after(250, lambda: self.iconbitmap('D:/gym_98MPH/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_98MPH/fotos_gym/gym_fondos/1.jpg"), size = (1000,700))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        ####################################################### 

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Fecha","Id", "Nombre Completo", "Modalidad", "Entrenador", "Importe", "P Entrenador"),show="headings")
        self.tabla.column("#0", width = 100, anchor="center")       
        self.tabla.column("Fecha", width = 100, anchor="center")       
        self.tabla.column("Id", width = 100, anchor="center")       
        self.tabla.column("Nombre Completo", width = 300, anchor="center")
        self.tabla.column("Modalidad", width = 100, anchor="center")
        self.tabla.column("Entrenador", width = 100, anchor="center")        
        self.tabla.column("Importe", width = 100, anchor="center")        
        self.tabla.column("P Entrenador", width = 150, anchor="center")        

        self.tabla.place(x = 50, y = 200)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Id_Pago", anchor="center")        
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Id", text = "Id", anchor="center")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo", anchor="center")
        self.tabla.heading("Modalidad", text = "Modalidad", anchor="center")
        self.tabla.heading("Entrenador", text = "Entrenador", anchor="center")
        self.tabla.heading("Importe", text = "Importe", anchor="center")
        self.tabla.heading("P Entrenador", text = "P Entrenador", anchor="center")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set) 

        def llenar_tabla():
            v = 0
            b = 0
            i = 0
            e = 0
            t = 0   

            ent_v = 0
            ent_b = 0
            ent_i = 0
            ent_e = 0
            ent_t = 0   

            self.tabla.delete(*self.tabla.get_children())

            #******************** calculemos los totales 
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "gym_98MPH"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM `pagos` WHERE `fecha` >= "{self.texto_fecha_inicial.get()}" AND `fecha` < "{self.texto_fecha_final.get()}" """
            cursor.execute(sql)
            for index in cursor: 
                # calculamos los totales
                t+=index[7] 

                if index[4] == "Vip":
                    v+=index[7]

                elif index[4] == "Basico": 
                    b += index[7]

                elif index[4] == "Invitados":
                    i += index[7]

                else:
                    e += index[7]  

                # calculamos los totales de los entrenadores
                ent_t+=index[8] 

                if index[4] == "Vip":
                    ent_v+=index[8]

                elif index[4] == "Basico": 
                    ent_b += index[8]

                elif index[4] == "Invitados":
                    ent_i += index[8]

                else:
                    ent_e += index[8]                                
                              
                self.tabla.insert("",END, text = index[0], values=(index[1],index[2],index[3],index[4],index[5],index[7],index[8],))  

            # llevemos los totales a los labels
            total_vip.set(f"Vip: {v}")
            total_basico.set(f"Basico: {b}")
            total_invitados.set(f"Invitados: {i}")
            total_extra.set(f"Extra: {e}")
            total.set(f"Total: {t}")

            # llevemos los totales de los entrenadores
            ent_vip.set(f"Vip: {ent_v}")
            ent_basico.set(f"Basico: {ent_b}")
            ent_invitados.set(f"Invitados: {ent_i}")
            ent_extra.set(f"Extra: {ent_e}")
            ent.set(f"Total: {ent_t}")


        self.texto_fecha_inicial = CTkEntry(self,placeholder_text="Fecha inicial ...")
        self.texto_fecha_inicial.insert(0,fecha_actual)
        self.texto_fecha_inicial.place(x=100,y=60) 

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
        self.btn_fecha_inicial.place(x=250 ,y=60 )

        self.texto_fecha_final = CTkEntry(self,placeholder_text="Fecha final ...")
        self.texto_fecha_final.insert(0,fecha_actual + timedelta(days=1))
        self.texto_fecha_final.place(x=100,y=100) 

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
        self.btn_fecha_final.place(x=250 ,y=100 )

        # ahora vamos a configurar los totales que se muestran 
        self.label1 = CTkLabel(self,text="---------- Totales ----------")
        self.label1.place(x=100,y=420)
        
        total_vip = StringVar()
        total_vip.set("Vip: 0")

        self.label_vip = CTkLabel(self,textvariable=total_vip)
        self.label_vip.place(x=100,y=460)

        total_basico = StringVar()
        total_basico.set("Basico: 0")

        self.label_basico = CTkLabel(self,textvariable=total_basico)
        self.label_basico.place(x=100,y=500)

        total_invitados = StringVar()
        total_invitados.set("Invitados: 0")

        self.label_invitados = CTkLabel(self,textvariable=total_invitados)
        self.label_invitados.place(x=100,y=540)

        total_extra = StringVar()
        total_extra.set("Extra: 0")

        self.label_extra = CTkLabel(self,textvariable=total_extra)
        self.label_extra.place(x=100,y=580)

        total = StringVar()
        total.set("Total: 0")

        self.label_total = CTkLabel(self,textvariable=total)
        self.label_total.place(x=100,y=620)


        # ahora vamos a configurar los totales que muestran lo que ganaron todos los entrenadores 
        self.label2 = CTkLabel(self,text="---------- Entrenadores ----------")
        self.label2.place(x=300,y=420)

        ent_vip = StringVar()
        ent_vip.set("Vip: 0")

        self.label_ent_vip = CTkLabel(self,textvariable=ent_vip)
        self.label_ent_vip.place(x=300,y=460)

        ent_basico = StringVar()
        ent_basico.set("Basico: 0")

        self.label_ent_basico = CTkLabel(self,textvariable=ent_basico)
        self.label_ent_basico.place(x=300,y=500)

        ent_invitados = StringVar()
        ent_invitados.set("Invitados: 0")

        self.label_ent_invitados = CTkLabel(self,textvariable=ent_invitados)
        self.label_ent_invitados.place(x=300,y=540)

        ent_extra = StringVar()
        ent_extra.set("Extra: 0")

        self.label_ent_extra = CTkLabel(self,textvariable=ent_extra)
        self.label_ent_extra.place(x=300,y=580)

        ent = StringVar()
        ent.set("Total: 0")

        self.label_ent_total = CTkLabel(self,textvariable=ent)
        self.label_ent_total.place(x=300,y=620)

        # ahora el boton de exportar la tabla 
        def exportar():
            try:
                if not self.tabla.get_children():
                    messagebox.showwarning("Sin datos", "No hay datos para exportar")
                    return
                
                rows = []
                for item in self.tabla.get_children():
                    values = self.tabla.item(item)['values']
                    rows.append(list(values))

                # DataFrame con las columnas que necesitas
                df = pd.DataFrame(rows, columns=["Fecha", "Id", "Nombre Completo", "Modalidad", "Entrenador", "Importe", "P Entrenador"])
                
                # Convertir columnas numéricas (si es necesario)
                df["Importe"] = pd.to_numeric(df["Importe"], errors='coerce')
                df["P Entrenador"] = pd.to_numeric(df["P Entrenador"], errors='coerce')
                
                # Calcular totales
                total_importe = df["Importe"].sum()
                total_p_entrenador = df["P Entrenador"].sum()
                
                # Agregar una fila vacía
                fila_vacia = pd.DataFrame([[""] * len(df.columns)], columns=df.columns)
                
                # Agregar fila de totales
                fila_totales = pd.DataFrame([["TOTAL", "", "", "", "", total_importe, total_p_entrenador]], columns=df.columns)
                
                # Concatenar: datos originales + fila vacía + totales
                df_final = pd.concat([df, fila_vacia, fila_totales], ignore_index=True)
                
                # Nombre sugerido del archivo
                nombre_sugerido = f"Balance {fecha_actual}.xlsx"
                
                # Diálogo para guardar archivo
                ruta_guardado = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[
                        ("Archivos de Excel", "*.xlsx"),
                        ("Todos los archivos", "*.*")
                    ],
                    initialfile=nombre_sugerido,
                    title="Guardar archivo Excel"
                )
                
                if ruta_guardado:
                    df_final.to_excel(ruta_guardado, index=False)
                    messagebox.showinfo("Exportar", f"¡Exportado exitosamente!\n\nGuardado en:\n{ruta_guardado}")
                else:
                    messagebox.showinfo("Cancelado", "Exportación cancelada")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")


        self.btn = CTkButton(self,text="Exportar",command=exportar)
        self.btn.place(x=600,y=500)

        llenar_tabla()



autenticacion = Autenticacion()
autenticacion.mainloop()
