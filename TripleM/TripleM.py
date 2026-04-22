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



ususario_triplem_is_created = False
base_data_is_created = False
table_usuarios_is_created = False
usuario_triplem_is_created = False
table_licencias_is_created = False

# ********************** creando usuario admin ******************************

try:
    sql = """CREATE USER 'triplem'@'localhost' IDENTIFIED BY '123456';"""
    cursor.execute(sql)
    conn.commit()
except:
    ususario_triplem_is_created = True

sql = """GRANT ALL PRIVILEGES ON *.* TO 'triplem'@'localhost' REQUIRE NONE WITH GRANT OPTION MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0; """
cursor.execute(sql)
conn.commit()

conn.close()

conn = mysql.connector.connect(
    host = "localhost",
    user = "triplem",
    password = "123456",
    )
cursor = conn.cursor()

# ******* creando la base de datos triplem ***********
try:
    sql = """CREATE DATABASE triplem CHARACTER SET = utf8mb4 COLLATE utf8mb4_spanish_ci;"""
    cursor.execute(sql)
    conn.commit()
    base_data_is_created = True
except:
    base_data_is_created = True

conn = mysql.connector.connect(
    host = "localhost",
    user = "triplem",
    password = "123456",
    database = "triplem"
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
    user = "triplem",
    password = "123456",
    database = "triplem"
    )
cursor = conn.cursor()

usuario_inicial = []
sql = """ SELECT Usuario FROM usuarios """
cursor.execute(sql)

for usser in cursor:
    usuario_inicial.append(usser)

for index in range(len(usuario_inicial)):
    if usuario_inicial[index][0] == "triplem":
        usuario_triplem_is_created = True

if usuario_triplem_is_created == False:
    try:
        sql = """INSERT INTO usuarios (Usuario,Password) VALUES ("triplem","123456")"""
        cursor.execute(sql)
        conn.commit()
        
        usuario_triplem_is_created = True
    except:
        usuario_triplem_is_created = True


# ************** creando tabla licencias ***************

conn = mysql.connector.connect(
    host = "localhost",
    user = "triplem",
    password = "123456",
    database = "triplem"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `triplem`.`licencias` (`codigo_lic` VARCHAR(50) NOT NULL , `pass_economia` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    table_licencias_is_created = True   


# ******************** Creando Tabla productos *******************
try:
    sql = """CREATE TABLE `triplem`.`productos` (`Codigo` INT NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `CostoUsd` FLOAT NOT NULL, `Cantidad` INT NOT NULL, `Categoria` VARCHAR(50) NOT NULL  ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ********************** creando tabla entradas ***********************************
try:
    sql = """CREATE TABLE `triplem`.`entradas` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL,`Codigo` INT NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `CostoUsd` FLOAT NOT NULL, `Cantidad` INT NOT NULL,`Categoria` VARCHAR(50) NOT NULL, `Proveedor` VARCHAR(50) NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# ********************** creando tabla salidas ***********************************
try:
    sql = """CREATE TABLE `triplem`.`salidas` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL,`Codigo` INT NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `CostoUsd` FLOAT NOT NULL, `CostoCup` FLOAT NOT NULL, `Precio` FLOAT NOT NULL, `Cantidad` INT NOT NULL, `Cliente` VARCHAR(50) NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# *************************** creando tabla categorias ****************************
try:
    sql = """CREATE TABLE `triplem`.`categorias` (`Nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# *************************** creando tabla proveedores ****************************
try:
    sql = """CREATE TABLE `triplem`.`proveedores` (`Nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# *************************** creando tabla tarifas ****************************
try:
    sql = """CREATE TABLE `triplem`.`tarifas` (`USD` FLOAT NOT NULL, `EUR` FLOAT NOT NULL, `EUR-USD` FLOAT NOT NULL ) ENGINE = InnoDB;"""
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
        self.iconbitmap("D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico")


        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/logo3.jpg"), size = (400,200))  

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

        sql = """SELECT Usuario, Password FROM usuarios"""

        cursor.execute(sql)
        for index in cursor:
            autorizacion.append(index)

        def codigo_btn_iniciar():
            # ******************** control de vencimiento *****************
            lic = ""

            conn = mysql.connector.connect(
            host = "localhost",
            user = "triplem",
            password = "123456",
            database = "triplem"
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
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
       

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/logo3.jpg"), size = (300,200))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

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
                    user = "triplem",
                    password = "123456",
                    database = "triplem"
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
        self.title("Triple M")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.resizable(False,False)   
        
        
        # **************************** fondo *****************************************************
        try:            
            self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/lobby.jpg"), size = (1300,700))                  
            
            label_imagen_lobby = CTkLabel(self, image = self.imagen, text = "")
            label_imagen_lobby.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error","No se encontro foto")
        
        firma = "Vence (" + str(fecha_vencimiento) + ")"
        self.label_triplem = CTkLabel(self, text = firma, font=("Times New Roman",16))
        self.label_triplem.place(x = 1150, y = 650)

        self.menu = Menu(self)
        self.config(menu=self.menu, width="200", height="100")        

        def nuevo_producto_lobby():
            np = NuevoProducto()

        def reabastecer_lobby():
            reab = Reabastecer()

        def salidas_lobby():
            pass

        def almacen_lobby():
            pass

        def categorias_lobby():
            cat = Categorias()

        def proveedores_lobby():
            pr = Proveedores()
        
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
            

        consultas_menu = Menu(self.menu, tearoff = 0)   
        consultas_menu.add_command(label="Almacen", command = almacen_lobby)        
        
        entradas_menu = Menu(self.menu, tearoff = 0)
        entradas_menu.add_command(label="Nuevo Producto", command = nuevo_producto_lobby)                     
        entradas_menu.add_command(label="Reabastecer", command = reabastecer_lobby)                     

        usuario_menu = Menu(self.menu, tearoff = 0)
        usuario_menu.add_command(label="Agregar", command = agregar_usuario)
        usuario_menu.add_command(label="Eliminar", command = eliminar_usuario)

        licencia_menu = Menu(self.menu, tearoff = 0)
        licencia_menu.add_command(label="Nueva", command = agregar_nueva_licencia)

        salir_menu = Menu(self.menu, tearoff = 0)
        salir_menu.add_command(label="Cerrar Cesion", command = cerrar_cesion)
        salir_menu.add_command(label="Cerrar Programa", command = cerrar_programa)
        
        self.menu.add_cascade (label="Consultas", menu = consultas_menu)
        self.menu.add_cascade (label="Entradas", menu = entradas_menu)
        self.menu.add_cascade (label="Salidas", command = salidas_lobby)        
        self.menu.add_cascade (label="Categorias", command = categorias_lobby)
        self.menu.add_cascade (label="Proveedores", command = proveedores_lobby)
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
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (400,300))                            
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

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
                        user = "triplem",
                        password = "123456",
                        database = "triplem"
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
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (400,300))                            
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)        
        
        items_usuarios = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "triplem",
            password = "123456",
            database = "triplem"
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
                if texto_nombre_usuario_eliminar.get() == "triplem":
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
                                    user = "triplem",
                                    password = "123456",
                                    database = "triplem"
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
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_agregar_cliente.jpg"), size = (600,600))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 600)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")
        

        # ************************** Labels *************************        

        self.label_codigo = CTkLabel(self,text="Codigo:", font=("Times New Roman",16))
        self.label_codigo.place(x = 630, y = 70)   

        self.texto_codigo = CTkEntry(self)
        self.texto_codigo.place(x = 750, y = 70)     

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 630, y = 110) 
        
        self.texto_nombre = CTkEntry(self)
        self.texto_nombre.place(x = 750, y = 110)       

        self.label_costo_usd = CTkLabel(self,text="Costo Lote Usd:", font=("Times New Roman",16))
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

            tar1 = 0           
            tar2 = 0           
            tar3 = 0 

            conn = mysql.connector.connect(
                host = "localhost",
                user = "triplem",
                password = "123456",
                database = "triplem"
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
                        self.texto_costo_usd.insert(0,resultado)
                        temp.destroy()

                    else:
                        resultado = round(float(temp.texto_eur.get())*tar3,2)
                        self.texto_costo_usd.insert(0,resultado)
                        temp.destroy()


            temp.btn_cambiar = CTkButton(temp, text="Cambiar", command=cambiar)
            temp.btn_cambiar.pack(pady=10)           

        self.btn_cambio = CTkButton(self,text="...", width=30,command=cambio)      
        self.btn_cambio.place(x = 900, y = 150)  

        self.label_cantidad = CTkLabel(self,text="Cantidad:", font=("Times New Roman",16))
        self.label_cantidad.place(x = 630, y = 190)  

        self.texto_cantidad = CTkEntry(self)
        self.texto_cantidad.place(x = 750, y = 190)  

        self.label_proveedor = CTkLabel(self,text="Proveedor:", font=("Times New Roman",16))
        self.label_proveedor.place(x = 630, y = 230)  

        proveedores = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "triplem",
            password = "123456",
            database = "triplem"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `proveedores`;"""
        cursor.execute(sql)
        for index in cursor:
            proveedores.append(index[0])

        self.texto_proveedores = CTkComboBox(self, values=proveedores)
        self.texto_proveedores.set("...")
        self.texto_proveedores.place(x = 750, y = 230)  

        self.label_categoria = CTkLabel(self,text="Categoria:", font=("Times New Roman",16))
        self.label_categoria.place(x = 630, y = 270)  

        categorias = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "triplem",
            password = "123456",
            database = "triplem"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `categorias`;"""
        cursor.execute(sql)
        for index in cursor:
            categorias.append(index[0])

        self.texto_categoria = CTkComboBox(self, values=categorias)
        self.texto_categoria.set("...")
        self.texto_categoria.place(x = 750, y = 270)         



        def agregar_producto():
            try:
                # verificar que no se repite el codigo en la bd 
                repetido = False
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "triplem",
                    password = "123456",
                    database = "triplem"
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
                            user = "triplem",
                            password = "123456",
                            database = "triplem"
                            )
                        cursor = conn.cursor()                    

                        sql = f""" INSERT INTO `productos`(`Codigo`, `Nombre`, `CostoUsd`, `Cantidad`, `Categoria`) VALUES ('{self.texto_codigo.get()}','{self.texto_nombre.get()}','{self.texto_costo_usd.get()}','{self.texto_cantidad.get()}','{self.texto_categoria.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # hallemos el id de la entrada
                        id_entrada = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "triplem",
                            password = "123456",
                            database = "triplem"
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
                            user = "triplem",
                            password = "123456",
                            database = "triplem"
                            )
                        cursor = conn.cursor()                    

                        sql = f""" INSERT INTO `entradas`(`Id`, `Fecha`, `Codigo`, `Nombre`, `CostoUsd`, `Cantidad`, `Categoria`, `Proveedor`) VALUES ('{id_entrada}','{fecha_actual}','{self.texto_codigo.get()}','{self.texto_nombre.get()}','{self.texto_costo_usd.get()}','{self.texto_cantidad.get()}','{self.texto_categoria.get()}','{self.texto_proveedores.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # limpiar los campos 
                        self.texto_codigo.delete(0,END)
                        self.texto_nombre.delete(0,END)
                        self.texto_costo_usd.delete(0,END)
                        self.texto_cantidad.delete(0,END)
                        self.texto_proveedores.set("...")
                        self.texto_categoria.set("...")
        
            except:
                error = messagebox.showerror("Error","Hubo problemas para agregar el producto")
            
                
            
        def cancelar():            
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=agregar_producto, width = 150, height = 40)
        self.btn_aceptar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar, width = 150, height = 40)
        self.btn_cancelar.place(x=820 ,y=500 )



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
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 


        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/entrenadores.jpg"), size = (800,600))      
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)    

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ())
        self.tabla.column("#0", width = 500)

        self.tabla.place(x = 200, y = 100)        
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
                user = "triplem",
                password = "123456",
                database = "triplem"
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
                        user = "triplem",
                        password = "123456",
                        database = "triplem"
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
                            user = "triplem",
                            password = "123456",
                            database = "triplem"
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
                        user = "triplem",
                        password = "123456",
                        database = "triplem"
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
                     

        def cerrar():
            self.destroy()

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 30)
        self.btn_agregar.place(x = 100, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar, width = 200, height = 30)
        self.btn_eliminar.place(x = 500, y = 400)        

        self.btn_cerrar = CTkButton(self, text = "Cerrar", command = cerrar, width = 300, height = 50)
        self.btn_cerrar.place(x = 250, y = 500)



# **********************************************************************************
# ***************************** Proveedores ****************************************
# **********************************************************************************

class Proveedores(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Proveedores")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 


        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/entrenadores.jpg"), size = (800,600))      
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)    

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ())
        self.tabla.column("#0", width = 500)

        self.tabla.place(x = 200, y = 100)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Proveedores")

        scrollbar_entrenadores = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar_entrenadores.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar_entrenadores.set)
        
        def on_click(event):
            global nombre_proveedores
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                nombre_proveedores = self.tabla.item(item, "text")                

        self.tabla.bind("<ButtonRelease-1>", on_click)

        def llenar_tabla():
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "triplem",
                password = "123456",
                database = "triplem"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `proveedores`;"""
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

            temp.texto_nombre = CTkEntry(temp, placeholder_text="Proveedores ...")
            temp.texto_nombre.pack(pady = 10)

            def aceptar():
                if temp.texto_nombre.get() == "":
                    error = messagebox.showerror("Error","Debes escribir algun nombre")
                else:
                    # vemos que no se repita la categoria
                    repetido = False
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "triplem",
                        password = "123456",
                        database = "triplem"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `proveedores` """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == temp.texto_nombre.get():
                            repetido = True
                            error = messagebox.showerror("Error","Ese proveedor ya existe")

                    if not repetido:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "triplem",
                            password = "123456",
                            database = "triplem"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `proveedores`(`Nombre`) VALUES ('{temp.texto_nombre.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla()

                        term = messagebox.showinfo("Terminado","Se ha agregado el proveedor")
                        temp.destroy()

            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)


        def eliminar():
            global nombre_proveedores           
            try:
                string = f"Vas a eliminar a {nombre_proveedores} de las categorias"
                conf = messagebox.askokcancel("Confirmar",string)    
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "triplem",
                        password = "123456",
                        database = "triplem"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `proveedores` WHERE `Nombre` = "{nombre_proveedores}" """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla()

                    term = messagebox.showinfo("Terminado","Se ha eliminado el proveedor")
                    nombre_proveedores = None

            except:
                error = messagebox.showerror("Error","Selecciona un proveedor para eliminar")                    

        

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 50)
        self.btn_agregar.place(x = 100, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar, width = 200, height = 50)
        self.btn_eliminar.place(x = 500, y = 400) 



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
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))         

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Costo Usd", "Cantidad", "Categoria"), show="headings")
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre", width = 100)
        self.tabla.column("Costo Usd", width = 100)
        self.tabla.column("Cantidad", width = 100)
        self.tabla.column("Categoria", width = 100)

        self.tabla.place(x = 100, y = 100)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Costo Usd", text = "Costo Usd")
        self.tabla.heading("Cantidad", text = "Cantidad")
        self.tabla.heading("Categoria", text = "Categoria")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)



























autenticacion = Autenticacion()
autenticacion.mainloop()