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



ususario_condesa_is_created = False
base_data_is_created = False
table_usuarios_is_created = False
usuario_condesa_is_created = False
table_licencias_is_created = False

# ********************** creando usuario admin ******************************

try:
    sql = """CREATE USER 'condesa'@'localhost' IDENTIFIED BY '123456';"""
    cursor.execute(sql)
    conn.commit()
except:
    ususario_condesa_is_created = True

sql = """GRANT ALL PRIVILEGES ON *.* TO 'condesa'@'localhost' REQUIRE NONE WITH GRANT OPTION MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0; """
cursor.execute(sql)
conn.commit()

conn.close()

conn = mysql.connector.connect(
    host = "localhost",
    user = "condesa",
    password = "123456",
    )
cursor = conn.cursor()

# ******* creando la base de datos condesa ***********
try:
    sql = """CREATE DATABASE condesa CHARACTER SET = utf8mb4 COLLATE utf8mb4_spanish_ci;"""
    cursor.execute(sql)
    conn.commit()
    base_data_is_created = True
except:
    base_data_is_created = True

conn = mysql.connector.connect(
    host = "localhost",
    user = "condesa",
    password = "123456",
    database = "condesa"
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
    user = "condesa",
    password = "123456",
    database = "condesa"
    )
cursor = conn.cursor()

usuario_inicial = []
sql = """ SELECT Usuario FROM usuarios """
cursor.execute(sql)

for usser in cursor:
    usuario_inicial.append(usser)

for index in range(len(usuario_inicial)):
    if usuario_inicial[index][0] == "condesa":
        usuario_condesa_is_created = True

if usuario_condesa_is_created == False:
    try:
        sql = """INSERT INTO usuarios (Usuario,Password) VALUES ("condesa","123456")"""
        cursor.execute(sql)
        conn.commit()
        
        usuario_condesa_is_created = True
    except:
        usuario_condesa_is_created = True


# ************** creando tabla licencias ***************

conn = mysql.connector.connect(
    host = "localhost",
    user = "condesa",
    password = "123456",
    database = "condesa"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `condesa`.`licencias` (`codigo_lic` VARCHAR(50) NOT NULL , `pass_economia` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    table_licencias_is_created = True   


# *************************** creando tabla categorias ****************************
try:
    sql = """CREATE TABLE `condesa`.`categorias` (`Nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# *************************** creando tabla categorias_productos ****************************
try:
    sql = """CREATE TABLE `condesa`.`categorias_productos` (`Nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ******************** Creando Tabla productos *******************

conn = mysql.connector.connect(
    host = "localhost",
    user = "condesa",
    password = "123456",
    database = "condesa"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `condesa`.`insumos` (`Codigo` INT(11) NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `Costo` FLOAT NOT NULL, `Cantidad` FLOAT NOT NULL, `U/M` VARCHAR(50) NOT NULL, `Categoria` VARCHAR(50) NOT NULL) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ********************** creando tabla entradas ***********************************
try:
    sql = """CREATE TABLE `condesa`.`entradas` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL,`Codigo` INT NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `Costo` FLOAT NOT NULL, `Cantidad` FLOAT NOT NULL,`Categoria` VARCHAR(50) NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ******************** Creando Tabla productos *******************

conn = mysql.connector.connect(
    host = "localhost",
    user = "condesa",
    password = "123456",
    database = "condesa"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `condesa`.`productos` (`Codigo` INT(11) NOT NULL, `Nombre` VARCHAR(50) NOT NULL, `Costo` FLOAT NOT NULL,`Precio` FLOAT NOT NULL, `Categoria` VARCHAR(50) NOT NULL, `Insumo1` INT(11) NOT NULL, `Cantidad1` FLOAT NOT NULL, `Insumo2` INT(11) NOT NULL, `Cantidad2` FLOAT NOT NULL, `Insumo3` INT(11) NOT NULL, `Cantidad3` FLOAT NOT NULL, `Insumo4` INT(11) NOT NULL, `Cantidad4` FLOAT NOT NULL, `Insumo5` INT(11) NOT NULL, `Cantidad5` FLOAT NOT NULL, `Insumo6` INT(11) NOT NULL, `Cantidad6` FLOAT NOT NULL, `Insumo7` INT(11) NOT NULL, `Cantidad7` FLOAT NOT NULL, `Insumo8` INT(11) NOT NULL, `Cantidad8` FLOAT NOT NULL, `Insumo9` INT(11) NOT NULL, `Cantidad9` FLOAT NOT NULL, `Insumo10` INT(11) NOT NULL, `Cantidad10` FLOAT NOT NULL) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ********************** creando tabla salidas ***********************************
try:
    sql = """CREATE TABLE `condesa`.`salidas` (`Id` INT(11) NOT NULL, `Fecha` DATE NOT NULL,`Codigo` INT(11) NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `Costo` FLOAT NOT NULL, `Precio` FLOAT NOT NULL, `Cantidad` INT NOT NULL, `Categoria` VARCHAR(50) NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# ********************** creando tabla regalos ***********************************
try:
    sql = """CREATE TABLE `condesa`.`regalos` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL,`Codigo` VARCHAR(50) NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `Costo` FLOAT NOT NULL, `Precio` FLOAT NOT NULL, `Cantidad` INT NOT NULL, `Concepto` VARCHAR(50) NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True


# ********************** creando tabla para gastos asociados ***********************************
try:
    sql = """CREATE TABLE `condesa`.`asociados` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL, `Concepto` VARCHAR(100) NOT NULL, `Monto` FLOAT NOT NULL) ENGINE = InnoDB;"""
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
        self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico')  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo1.jpg"), size = (400,200))  

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
            user = "condesa",
            password = "123456",
            database = "condesa"
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
            user = "condesa",
            password = "123456",
            database = "condesa"
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
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo1.jpg"), size = (300,200))  

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
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
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
        self.title("Condesa")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))
        self.resizable(False,False)   

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo3.jpg"), size = (1300,700))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################          
        
        firma = "Vence (" + str(fecha_vencimiento) + ")"
        self.label_condesa = CTkLabel(self, text = firma, font=("Times New Roman",16))
        self.label_condesa.place(x = 1150, y = 650)

        self.menu = Menu(self)
        self.config(menu=self.menu, width="200", height="100") 


        ########################## ahora los botones del lobby  

        # ------------------------ ventas
        def ventas_lobby():
            v = Ventas()

        # ------------------------ devoluciones
        def devolucion_regalo_lobby():
            cr = ControlRegalos()

        def devolucion_venta_lobby():
            cv = ControlVentas()

        # ----------------------- consultas
        def consulta_totales_lobby():
            ct = ConsultaTotales()

        # ----------------------- gastos
        def asociados_lobby():
            a = Asociados()

        # ----------------------- productos
        def nuevo_producto_lobby():
            np = NuevoProducto()

        def modificar_producto_lobby():
            mp = ModificarProducto()

        # ----------------------- insumos

        def ver_modificar_lobby():
            ni = Insumos()

        def nuevo_insumo_lobby():
            ni = NuevoInsumo()

        def reabastecer_lobby():
            reab = Reabastecer()

        # -------------------- categorias

        def categorias_lobby():
            cat = Categorias() 

        def categorias_productos():
            cat_prod = CategoriasProductos()


        def salva_lobby():            
            # Crear carpeta de respaldos si no existe
            carpeta_respaldo = "D:/condesa/respaldos"
            if not os.path.exists(carpeta_respaldo):
                os.makedirs(carpeta_respaldo)
            
            # Nombre del archivo con fecha_actual
            nombre_archivo = f"condesa_{fecha_actual}.sql"
            ruta_completa = os.path.join(carpeta_respaldo, nombre_archivo)
            
            # Ruta de mysqldump en XAMPP
            ruta_mysqldump = "C:/xampp/mysql/bin/mysqldump.exe"
            
            try:
                # Comando con ruta completa
                comando = f'"{ruta_mysqldump}" -u condesa -p123456 condesa > "{ruta_completa}"'
                
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

        devoluciones_menu = Menu(self.menu, tearoff = 0)   
        devoluciones_menu.add_command(label="Devolver Regalo", command = devolucion_regalo_lobby)                                     
        devoluciones_menu.add_command(label="Devolver Venta", command = devolucion_venta_lobby)  

        productos_menu = Menu(self.menu, tearoff = 0)   
        productos_menu.add_command(label="Ver y Modificar", command = modificar_producto_lobby)                                     
        productos_menu.add_command(label="Nuevo Producto", command = nuevo_producto_lobby)            

        gastos_menu = Menu(self.menu, tearoff = 0)   
        gastos_menu.add_command(label="Asociados", command = asociados_lobby)   

        consultas_menu = Menu(self.menu, tearoff = 0)   
        consultas_menu.add_command(label="Totales", command = consulta_totales_lobby)

        entradas_menu = Menu(self.menu, tearoff = 0)
        entradas_menu.add_command(label="Ver y Modificar", command = ver_modificar_lobby)                     
        entradas_menu.add_command(label="Nuevo Insumo", command = nuevo_insumo_lobby)                     
        entradas_menu.add_command(label="Reabastecer", command = reabastecer_lobby) 

        administrativo_menu = Menu(self.menu, tearoff = 0)
        administrativo_menu.add_command(label="Categorias Insumos", command = categorias_lobby)                         
        administrativo_menu.add_command(label="Categorias Productos", command = categorias_productos)                         

        usuario_menu = Menu(self.menu, tearoff = 0)
        usuario_menu.add_command(label="Agregar", command = agregar_usuario)
        usuario_menu.add_command(label="Eliminar", command = eliminar_usuario)

        licencia_menu = Menu(self.menu, tearoff = 0)
        licencia_menu.add_command(label="Nueva", command = agregar_nueva_licencia)

        salir_menu = Menu(self.menu, tearoff = 0)
        salir_menu.add_command(label="Cerrar Cesion", command = cerrar_cesion)
        salir_menu.add_command(label="Cerrar Programa", command = cerrar_programa)
        
        self.menu.add_cascade (label="Ventas", command = ventas_lobby) 
        self.menu.add_cascade (label="Devoluciones", menu = devoluciones_menu)
        self.menu.add_cascade (label="Consultas", menu = consultas_menu)
        self.menu.add_cascade (label="Gastos", menu = gastos_menu)
        self.menu.add_cascade (label="Productos", menu = productos_menu)
        self.menu.add_cascade (label="Insumos", menu = entradas_menu)                       
        self.menu.add_cascade (label="Administrativo", menu = administrativo_menu)                 
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
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))    

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo5.jpg"), size = (400,300))  

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
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
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
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo5.jpg"), size = (400,300))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################            
        
        items_usuarios = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "condesa",
            password = "123456",
            database = "condesa"
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
                if texto_nombre_usuario_eliminar.get() == "condesa":
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
                                    user = "condesa",
                                    password = "123456",
                                    database = "condesa"
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
# ***************************** Categorias *****************************************
# **********************************************************************************

class Categorias(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Categorias Insumos")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))      

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo.jpg"), size = (800,600))  

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
                user = "condesa",
                password = "123456",
                database = "condesa"
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
            temp.after(250, lambda: temp.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))  

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
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
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
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
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
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
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
# ***************************** Categorias Productos *******************************
# **********************************************************************************

class CategoriasProductos(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Categorias Productos")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))      

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo.jpg"), size = (800,600))  

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
                user = "condesa",
                password = "123456",
                database = "condesa"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `categorias_productos`;"""
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
            temp.after(250, lambda: temp.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))  

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
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `categorias_productos` """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == temp.texto_nombre.get():
                            repetido = True
                            error = messagebox.showerror("Error","Esa categoria ya existe")

                    if not repetido:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `categorias_productos`(`Nombre`) VALUES ('{temp.texto_nombre.get()}') """
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
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `categorias_productos` WHERE `Nombre` = "{nombre_categoria}" """
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
# ******************************** Nuevo Insumo **********************************
# **********************************************************************************

class NuevoInsumo(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Nuevo Insumo")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo2.jpg"), size = (600,600))  

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
                user = "condesa",
                password = "123456",
                database = "condesa"
                )
            cursor = conn.cursor()

            sql = """SELECT MAX(Codigo) FROM `insumos`;"""
            cursor.execute(sql)            
            for index in cursor:                
                ultimo_id.set(index[0])            

        actualizar_id()            

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 630, y = 70) 
        
        self.texto_nombre = CTkEntry(self)
        self.texto_nombre.place(x = 750, y = 70)       

        self.label_costo = CTkLabel(self,text="Costo:", font=("Times New Roman",16))
        self.label_costo.place(x = 630, y = 110)  

        self.texto_costo = CTkEntry(self)
        self.texto_costo.place(x = 750, y = 110)         

        self.label_um = CTkLabel(self,text="U/M:", font=("Times New Roman",16))
        self.label_um.place(x = 630, y = 150)  

        self.texto_um = CTkEntry(self)
        self.texto_um.place(x = 750, y = 150) 

        self.label_cantidad = CTkLabel(self,text="Cantidad:", font=("Times New Roman",16))
        self.label_cantidad.place(x = 630, y = 190)  

        self.texto_cantidad = CTkEntry(self)
        self.texto_cantidad.place(x = 750, y = 190)

        self.label_categoria = CTkLabel(self,text="Categoria:", font=("Times New Roman",16))
        self.label_categoria.place(x = 630, y = 230)  

        categorias = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "condesa",
            password = "123456",
            database = "condesa"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `categorias`;"""
        cursor.execute(sql)
        for index in cursor:
            categorias.append(index[0])

        self.texto_categoria = CTkComboBox(self, values=categorias)
        self.texto_categoria.set("...")
        self.texto_categoria.place(x = 750, y = 230)          

        def agregar_producto():
            # pedir confirmacion para agrear el producto
            conf = messagebox.askokcancel("Confirmar","Vamos a agregar el producto a la base de datos")
            if conf:
                try:
                    # hallemos el id del insumo
                    id_insumo = 1
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()

                    sql = """SELECT MAX(Codigo) FROM `insumos`;"""
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == None:
                            pass
                        else:
                            id_insumo = index[0] + 1 

                    # agregar el producto en la bd 
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor() 
                    sql = f""" INSERT INTO `insumos`(`Codigo`, `Nombre`, `Costo`, `Cantidad`, `U/M`, `Categoria`) VALUES ('{id_insumo}','{self.texto_nombre.get()}','{self.texto_costo.get()}','{self.texto_cantidad.get()}','{self.texto_um.get()}','{self.texto_categoria.get()}') """
                    cursor.execute(sql)
                    conn.commit()

                    # ahora agregamos la entrada  
                    # hallemos el id de la entrada
                    id_entrada = 1
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
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
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()                    

                    sql = f""" INSERT INTO `entradas`(`Id`, `Fecha`, `Codigo`, `Nombre`, `Costo`, `Cantidad`, `Categoria`) VALUES ('{id_entrada}','{fecha_actual}','{id_insumo}','{self.texto_nombre.get()}','{self.texto_costo.get()}','{self.texto_cantidad.get()}','{self.texto_categoria.get()}') """
                    cursor.execute(sql)
                    conn.commit()

                    # limpiar los campos                     
                    self.texto_nombre.delete(0,END)
                    self.texto_costo.delete(0,END)
                    self.texto_um.delete(0,END)
                    self.texto_cantidad.delete(0,END)                        
                    self.texto_categoria.set("...")                    
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
        self.title("Reabastecer Insumo")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo4.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Costo", "Cantidad", "U/M", "Categoria"))
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Nombre", width = 200, anchor="center")
        self.tabla.column("Costo", width = 100, anchor="center")
        self.tabla.column("Cantidad", width = 100, anchor="center")
        self.tabla.column("U/M", width = 100, anchor="center")        
        self.tabla.column("Categoria", width = 100, anchor="center")

        self.tabla.place(x = 50, y = 200)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Costo", text = "Costo")
        self.tabla.heading("Cantidad", text = "Cantidad")
        self.tabla.heading("U/M", text = "U/M")        
        self.tabla.heading("Categoria", text = "Categoria")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_reabastecer(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "condesa",
                password = "123456",
                database = "condesa"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM insumos WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%'; """
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
            temp.after(250, lambda: temp.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico')) 

            temp.texto_cantidad = CTkEntry(temp, placeholder_text="Cantidad ...")
            temp.texto_cantidad.pack(pady=5)

            def reabastecer_insumo():
                string = f"Vamos a reabastecer el producto de codigo {codigo}"
                conf = messagebox.askokcancel("Confirmar",string)
                if conf:
                    try:
                        # llevemos los resultados a la base de datos
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
                            )
                        cursor = conn.cursor()

                        sql = f""" UPDATE `insumos` SET `Cantidad`= `Cantidad` + '{temp.texto_cantidad.get()}' WHERE `Codigo` = "{codigo}" """
                        cursor.execute(sql)
                        conn.commit()

                        temp.destroy()
                        llenar_reabastecer(True)
                    except:
                        error = messagebox.showerror("Error","No se pudo reabastecer el producto")

            temp.btn_reabastecer = CTkButton(temp,text="Reabastecer", command=reabastecer_insumo)
            temp.btn_reabastecer.pack(pady=10)  

        self.tabla.bind("<Double-1>", reabastecer)



# **********************************************************************************
# ************************************* Insumos ************************************
# **********************************************************************************

class Insumos(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Insumos")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Costo", "U/M", "Cantidad", "Categoria"))
        self.tabla.column("#0", width = 75, anchor="center")
        self.tabla.column("Nombre", width = 200, anchor="center")
        self.tabla.column("Costo", width = 100, anchor="center")
        self.tabla.column("U/M", width = 75, anchor="center")
        self.tabla.column("Cantidad", width = 75, anchor="center")
        self.tabla.column("Categoria", width = 200, anchor="center")        

        self.tabla.place(x = 50, y = 200)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Costo", text = "Costo")
        self.tabla.heading("U/M", text = "U/M")
        self.tabla.heading("Cantidad", text = "Cantidad")
        self.tabla.heading("Categoria", text = "Categoria")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        # vamos a mostrar el equivalente en dinero a los productos que hay en almacen
        string = StringVar() 
        string.set("En Almacen:")        

        def alctualizar_equivalencia():
            conn = mysql.connector.connect(
                host = "localhost",
                user = "condesa",
                password = "123456",
                database = "condesa"
                )
            cursor = conn.cursor()

            sql = f""" SELECT SUM(`Costo`*`Cantidad`) FROM `insumos`; """
            cursor.execute(sql)
            for index in cursor:
                string.set("En Almacen: " + f"{index[0]} ")

        alctualizar_equivalencia()

        self.label_equivalente = CTkLabel(self,textvariable = string)
        self.label_equivalente.place(x=700,y=50)

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "condesa",
                password = "123456",
                database = "condesa"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM insumos WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%' ORDER BY `Codigo`; """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[4],index[3],index[5],))         

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
            temp.after(250, lambda: temp.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))  

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
                root.after(250, lambda: root.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico')) 

                ############ agregar el fondo de pantalla #########
      
                root.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo.jpg"), size = (600,600))  

                root.label_image = CTkLabel(root, image = root.imagen, text = "")  
                root.label_image.place(x = 0, y = 0)      

                #######################################################   

                # ************************** Labels *************************              

                root.label_nombre = CTkLabel(root,text="Nombre:", font=("Times New Roman",16))
                root.label_nombre.place(x = 630, y = 70) 
                
                root.texto_nombre = CTkEntry(root)
                root.texto_nombre.place(x = 750, y = 70)       

                root.label_costo = CTkLabel(root,text="Costo:", font=("Times New Roman",16))
                root.label_costo.place(x = 630, y = 110)  

                root.texto_costo = CTkEntry(root)
                root.texto_costo.place(x = 750, y = 110)                 

                root.label_um = CTkLabel(root,text="U/M:", font=("Times New Roman",16))
                root.label_um.place(x = 630, y = 150)  

                root.texto_um = CTkEntry(root)
                root.texto_um.place(x = 750, y = 150)   

                root.label_cantidad = CTkLabel(root,text="Cantidad:", font=("Times New Roman",16))
                root.label_cantidad.place(x = 630, y = 190)  

                root.texto_cantidad = CTkEntry(root)
                root.texto_cantidad.place(x = 750, y = 190)                 

                root.label_categoria = CTkLabel(root,text="Categoria:", font=("Times New Roman",16))
                root.label_categoria.place(x = 630, y = 230)  

                categorias = []
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()

                sql = """SELECT * FROM `categorias`;"""
                cursor.execute(sql)
                for index in cursor:
                    categorias.append(index[0])

                root.texto_categoria = CTkComboBox(root, values=categorias)
                root.texto_categoria.set("...")
                root.texto_categoria.place(x = 750, y = 230)                

                # vamos a llenar los campos con la info que ya existe en la base de datos
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `insumos` WHERE `Codigo` = "{codigo_almacen}" """
                cursor.execute(sql)
                for index in cursor:                                        
                    root.texto_nombre.insert(0,index[1]) 
                    root.texto_costo.insert(0,index[2])
                    root.texto_um.insert(0,index[4]) 
                    root.texto_cantidad.insert(0,index[3])                    
                    root.texto_categoria.set(index[5])                     
                    


                def modificar_producto():
                    try:
                        conf = messagebox.askokcancel("Confirmar","Vamos a modificar el producto en la base de datos")
                        if conf:                            
                            # modificar el producto en la bd 
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()                    

                            sql = f""" UPDATE `insumos` SET `Nombre`='{root.texto_nombre.get()}',`Costo`='{root.texto_costo.get()}',`U/M`='{root.texto_um.get()}',`Cantidad`='{root.texto_cantidad.get()}',`Categoria`='{root.texto_categoria.get()}' WHERE `Codigo` = "{codigo_almacen}"; """
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
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
                            )
                        cursor = conn.cursor()

                        sql = f""" DELETE FROM `insumos` WHERE `Codigo` = "{codigo_almacen}" """
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
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo2.jpg"), size = (600,200))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)      

        #######################################################   
        
        # ************************** Labels *************************   
                 
        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 630, y = 20) 
        
        self.texto_nombre = CTkEntry(self)
        self.texto_nombre.place(x = 750, y = 20)       

        self.label_costo = CTkLabel(self,text="Costo:", font=("Times New Roman",16))
        self.label_costo.place(x = 630, y = 60) 

        string_costo = StringVar()
        string_costo.set("0") 

        self.texto_costo = CTkLabel(self,textvariable=string_costo, font=("Times New Roman",16))
        self.texto_costo.place(x = 750, y = 60) 

        self.label_precio = CTkLabel(self,text="Precio:", font=("Times New Roman",16))
        self.label_precio.place(x = 630, y = 100)  

        self.texto_precio = CTkEntry(self)
        self.texto_precio.place(x = 750, y = 100) 

        self.label_costoxprecio = CTkLabel(self,text="C / P:", font=("Times New Roman",16))
        self.label_costoxprecio.place(x = 630, y = 140) 

        string_costoxprecio = StringVar()
        string_costoxprecio.set("0") 

        self.texto_costoxprecio = CTkLabel(self,textvariable=string_costoxprecio, font=("Times New Roman",16))
        self.texto_costoxprecio.place(x = 750, y = 140) 

        def cxp(event):            
            string_costoxprecio.set(float(string_costo.get())/float(self.texto_precio.get()))

        self.texto_precio.bind("<KeyRelease>", cxp) 

        self.label_categoria = CTkLabel(self,text="Categoria:", font=("Times New Roman",16))
        self.label_categoria.place(x = 630, y = 180)  

        categorias = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "condesa",
            password = "123456",
            database = "condesa"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `categorias_productos`;"""
        cursor.execute(sql)
        for index in cursor:
            categorias.append(index[0])

        self.texto_categoria = CTkComboBox(self, values=categorias)
        self.texto_categoria.set("...")
        self.texto_categoria.place(x = 750, y = 180)  

        self.label_div = CTkLabel(self,text="**************************************** Seccion Insumos ****************************************", font=("Times New Roman",16))
        self.label_div.place(x = 150, y =220) 

        # funciones para calcular el costo total del producto segun sus insumos
        def calc1():                
            if self.texto_ins1.get() == "":
                return 0
            else:
                if self.texto_cant1.get()=="":
                    cost = 0
                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {self.texto_ins1.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        cost = float(self.texto_cant1.get())*index[0]

                return cost

        def calc2():                
            if self.texto_ins2.get() == "":
                return 0
            else:
                if self.texto_cant2.get()=="":
                    cost = 0
                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {self.texto_ins2.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        cost = float(self.texto_cant2.get())*index[0]

                return cost

        def calc3():                
            if self.texto_ins3.get() == "":
                return 0
            else:
                if self.texto_cant3.get()=="":
                    cost = 0
                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {self.texto_ins3.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        cost = float(self.texto_cant3.get())*index[0]

                return cost

        def calc4():                
            if self.texto_ins4.get() == "":
                return 0
            else:
                if self.texto_cant4.get()=="":
                    cost = 0
                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {self.texto_ins4.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        cost = float(self.texto_cant4.get())*index[0]

                return cost

        def calc5():                
            if self.texto_ins5.get() == "":
                return 0
            else:
                if self.texto_cant5.get()=="":
                    cost = 0
                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {self.texto_ins5.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        cost = float(self.texto_cant5.get())*index[0]

                return cost

        def calc6():                
            if self.texto_ins6.get() == "":
                return 0
            else:
                if self.texto_cant6.get()=="":
                    cost = 0
                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {self.texto_ins6.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        cost = float(self.texto_cant6.get())*index[0]

                return cost

        def calc7():                
            if self.texto_ins7.get() == "":
                return 0
            else:
                if self.texto_cant7.get()=="":
                    cost = 0
                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {self.texto_ins7.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        cost = float(self.texto_cant7.get())*index[0]

                return cost

        def calc8():                
            if self.texto_ins8.get() == "":
                return 0
            else:
                if self.texto_cant8.get()=="":
                    cost = 0
                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {self.texto_ins8.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        cost = float(self.texto_cant8.get())*index[0]

                return cost

        def calc9():                
            if self.texto_ins9.get() == "":
                return 0
            else:
                if self.texto_cant9.get()=="":
                    cost = 0
                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {self.texto_ins9.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        cost = float(self.texto_cant9.get())*index[0]

                return cost

        def calc10():                
            if self.texto_ins10.get() == "":
                return 0
            else:
                if self.texto_cant10.get()=="":
                    cost = 0
                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()
        
                    sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {self.texto_ins10.get()} """
                    cursor.execute(sql)
                    for index in cursor:
                        cost = float(self.texto_cant10.get())*index[0]

                return cost

        def calc(opcion):
            if opcion == 1:
                return calc1()
            if opcion == 2:
                return calc2()
            if opcion == 3:
                return calc3()
            if opcion == 4:
                return calc4()
            if opcion == 5:
                return calc5()
            if opcion == 6:
                return calc6()
            if opcion == 7:
                return calc7()
            if opcion == 8:
                return calc8()
            if opcion == 9:
                return calc9()
            if opcion == 10:
                return calc10()

        def calcular_costo(event):
            costo = 0
            for i in range(1, 11):
                costo += calc(i)
            string_costo.set(str(costo))
            

        # --------------- seleccion de insumos
        def seleccionar_insumo(opcion):
            # aqui vamos a llenar la info del insumo 1 
            # hay que crear una ventana donde mostremos los insumos y podamos escoger el que queremos ahi 
            temp = CTkToplevel()
            temp.title("Seleccionar Insumo") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()            
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False)) 
            temp.after(250, lambda: temp.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico')) 

            def llenar(event):
                temp.tabla.delete(*temp.tabla.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()
    
                sql = f""" SELECT * FROM insumos WHERE  `Nombre` LIKE '%{temp.texto_buscador_nombre.get()}%'; """
                cursor.execute(sql)
                for index in cursor:
                    temp.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],))  

            # buscador
            temp.texto_buscador_nombre = CTkEntry(temp,placeholder_text="Buscar por Nombre ...")
            temp.texto_buscador_nombre.pack(pady=10)

            temp.texto_buscador_nombre.bind("<KeyRelease>", llenar) 

            # tabla de insumos
            estilos_tablas()        
                    
            temp.tabla = ttk.Treeview(temp, columns = ("Nombre", "Costo", "Cantidad", "U/M", "Categoria"), show="headings")
            temp.tabla.column("#0", width = 75, anchor="center")
            temp.tabla.column("Nombre", width = 200, anchor="center")
            temp.tabla.column("Costo", width = 100, anchor="center")
            temp.tabla.column("Cantidad", width = 75, anchor="center")
            temp.tabla.column("U/M", width = 75, anchor="center")            
            temp.tabla.column("Categoria", width = 200, anchor="center")        
    
            temp.tabla.pack(pady=10)        
            temp.tabla.config(height = 10)
    
            temp.tabla.heading("#0", text = "Codigo")
            temp.tabla.heading("Nombre", text = "Nombre")
            temp.tabla.heading("Costo", text = "Costo")
            temp.tabla.heading("Cantidad", text = "Cantidad")
            temp.tabla.heading("U/M", text = "U/M")            
            temp.tabla.heading("Categoria", text = "Categoria")        
    
            temp.scrollbar = CTkScrollbar(temp, command = temp.tabla.yview, width = 18)
            temp.scrollbar.place(in_ = temp.tabla, relheigh = 1, relx = 1)
    
            temp.tabla.config(yscrollcommand = temp.scrollbar.set)

            llenar(True)

            # ahora hay que seleccionar el insumo con 2ble click
            def escoger(event):                              
                # vamos a capturar el codigo del numero que vamos a reabastecer
                seleccion = temp.tabla.selection()
                if seleccion:
                    item = seleccion[0]                
                    cod = temp.tabla.item(item, "text")  
                    medida = temp.tabla.item(item, "values")[3] 

                # ahora vamos a escribir los datos en la ventana exterior
                if opcion == 1:
                    self.texto_ins1.delete(0,END)
                    string_ins1.set("")
                    self.texto_ins1.insert(0,cod)
                    string_ins1.set(medida)

                elif opcion == 2:
                    self.texto_ins2.delete(0,END)
                    string_ins2.set("")
                    self.texto_ins2.insert(0,cod)
                    string_ins2.set(medida)

                elif opcion == 3:
                    self.texto_ins3.delete(0,END)
                    string_ins3.set("")
                    self.texto_ins3.insert(0,cod)
                    string_ins3.set(medida)

                elif opcion == 4:
                    self.texto_ins4.delete(0,END)
                    string_ins4.set("")
                    self.texto_ins4.insert(0,cod)
                    string_ins4.set(medida)

                elif opcion == 5:
                    self.texto_ins5.delete(0,END)
                    string_ins5.set("")
                    self.texto_ins5.insert(0,cod)
                    string_ins5.set(medida)

                elif opcion == 6:
                    self.texto_ins6.delete(0,END)
                    string_ins6.set("")
                    self.texto_ins6.insert(0,cod)
                    string_ins6.set(medida)

                elif opcion == 7:
                    self.texto_ins7.delete(0,END)
                    string_ins7.set("")
                    self.texto_ins7.insert(0,cod)
                    string_ins7.set(medida)

                elif opcion == 8:
                    self.texto_ins8.delete(0,END)
                    string_ins8.set("")
                    self.texto_ins8.insert(0,cod)
                    string_ins8.set(medida)

                elif opcion == 9:
                    self.texto_ins9.delete(0,END)
                    string_ins9.set("")
                    self.texto_ins9.insert(0,cod)
                    string_ins9.set(medida)

                elif opcion == 10:
                    self.texto_ins10.delete(0,END)
                    string_ins10.set("")
                    self.texto_ins10.insert(0,cod)
                    string_ins10.set(medida)

                calcular_costo(True)

                temp.destroy()               

            temp.tabla.bind("<Double-1>", escoger)

        string_ins1 = StringVar()
        string_ins2 = StringVar()
        string_ins3 = StringVar()
        string_ins4 = StringVar()
        string_ins5 = StringVar()
        string_ins6 = StringVar()
        string_ins7 = StringVar()
        string_ins8 = StringVar()
        string_ins9 = StringVar()
        string_ins10 = StringVar()

        #--------------- 1

        def sel1():
            seleccionar_insumo(1)

        self.btn_ins1 = CTkButton(self,text="Insumo1", command=sel1, width=75)
        self.btn_ins1.place(x = 100, y = 260) 

        self.texto_ins1 = CTkEntry(self,placeholder_text="codigo...", width=60)
        self.texto_ins1.place(x = 190, y = 260)         

        self.texto_cant1 = CTkEntry(self,placeholder_text="cantidad...", width=70)
        self.texto_cant1.place(x = 260, y = 260)  

        self.texto_cant1.bind("<KeyRelease>", calcular_costo)    

        self.label_um_ins1 = CTkLabel(self, textvariable= string_ins1, font=("Times New Roman",16))
        self.label_um_ins1.place(x = 340, y = 260) 

        #--------------- 2

        def sel2():
            seleccionar_insumo(2)

        self.btn_ins2 = CTkButton(self,text="Insumo2", command=sel2, width=75)
        self.btn_ins2.place(x = 100, y = 300) 

        self.texto_ins2 = CTkEntry(self,placeholder_text="codigo...", width=60)
        self.texto_ins2.place(x = 190, y = 300)         

        self.texto_cant2 = CTkEntry(self,placeholder_text="cantidad...", width=70)
        self.texto_cant2.place(x = 260, y = 300)  

        self.texto_cant2.bind("<KeyRelease>", calcular_costo) 

        self.label_um_ins2 = CTkLabel(self, textvariable= string_ins2, font=("Times New Roman",16))
        self.label_um_ins2.place(x = 340, y = 300) 

        #--------------- 3

        def sel3():
            seleccionar_insumo(3)

        self.btn_ins3 = CTkButton(self,text="Insumo3", command=sel3, width=75)
        self.btn_ins3.place(x = 100, y = 340) 

        self.texto_ins3 = CTkEntry(self,placeholder_text="codigo...", width=60)
        self.texto_ins3.place(x = 190, y = 340)         

        self.texto_cant3 = CTkEntry(self,placeholder_text="cantidad...", width=70)
        self.texto_cant3.place(x = 260, y = 340)  

        self.texto_cant3.bind("<KeyRelease>", calcular_costo) 

        self.label_um_ins3 = CTkLabel(self, textvariable= string_ins3, font=("Times New Roman",16))
        self.label_um_ins3.place(x = 340, y = 340) 

        #--------------- 4

        def sel4():
            seleccionar_insumo(4)

        self.btn_ins4 = CTkButton(self,text="Insumo4", command=sel4, width=75)
        self.btn_ins4.place(x = 100, y = 380) 

        self.texto_ins4 = CTkEntry(self,placeholder_text="codigo...", width=60)
        self.texto_ins4.place(x = 190, y = 380)         

        self.texto_cant4 = CTkEntry(self,placeholder_text="cantidad...", width=70)
        self.texto_cant4.place(x = 260, y = 380)  

        self.texto_cant4.bind("<KeyRelease>", calcular_costo) 

        self.label_um_ins4 = CTkLabel(self, textvariable= string_ins4, font=("Times New Roman",16))
        self.label_um_ins4.place(x = 340, y = 380)  

        #--------------- 5

        def sel5():
            seleccionar_insumo(5)

        self.btn_ins5 = CTkButton(self,text="Insumo5", command=sel5, width=75)
        self.btn_ins5.place(x = 100, y = 420) 

        self.texto_ins5 = CTkEntry(self,placeholder_text="codigo...", width=60)
        self.texto_ins5.place(x = 190, y = 420)         

        self.texto_cant5 = CTkEntry(self,placeholder_text="cantidad...", width=70)
        self.texto_cant5.place(x = 260, y = 420) 

        self.texto_cant5.bind("<KeyRelease>", calcular_costo)  

        self.label_um_ins5 = CTkLabel(self, textvariable= string_ins5, font=("Times New Roman",16))
        self.label_um_ins5.place(x = 340, y = 420)  

        #--------------- 6

        def sel6():
            seleccionar_insumo(6)

        self.btn_ins6 = CTkButton(self,text="Insumo6", command=sel6, width=75)
        self.btn_ins6.place(x = 650, y = 260) 

        self.texto_ins6 = CTkEntry(self,placeholder_text="codigo...", width=60)
        self.texto_ins6.place(x = 740, y = 260)         

        self.texto_cant6 = CTkEntry(self,placeholder_text="cantidad...", width=70)
        self.texto_cant6.place(x = 810, y = 260) 

        self.texto_cant6.bind("<KeyRelease>", calcular_costo)  

        self.label_um_ins6 = CTkLabel(self, textvariable= string_ins6, font=("Times New Roman",16))
        self.label_um_ins6.place(x = 890, y = 260)  

        #--------------- 7

        def sel7():
            seleccionar_insumo(7)

        self.btn_ins7 = CTkButton(self,text="Insumo7", command=sel7, width=75)
        self.btn_ins7.place(x = 650, y = 300) 

        self.texto_ins7 = CTkEntry(self,placeholder_text="codigo...", width=60)
        self.texto_ins7.place(x = 740, y = 300)         

        self.texto_cant7 = CTkEntry(self,placeholder_text="cantidad...", width=70)
        self.texto_cant7.place(x = 810, y = 300)  

        self.texto_cant7.bind("<KeyRelease>", calcular_costo) 

        self.label_um_ins7 = CTkLabel(self, textvariable= string_ins7, font=("Times New Roman",16))
        self.label_um_ins7.place(x = 890, y = 300)  

        #--------------- 8

        def sel8():
            seleccionar_insumo(8)

        self.btn_ins8 = CTkButton(self,text="Insumo8", command=sel8, width=75)
        self.btn_ins8.place(x = 650, y = 340) 

        self.texto_ins8 = CTkEntry(self,placeholder_text="codigo...", width=60)
        self.texto_ins8.place(x = 740, y = 340)         

        self.texto_cant8 = CTkEntry(self,placeholder_text="cantidad...", width=70)
        self.texto_cant8.place(x = 810, y = 340)  

        self.texto_cant8.bind("<KeyRelease>", calcular_costo) 

        self.label_um_ins8 = CTkLabel(self, textvariable= string_ins8, font=("Times New Roman",16))
        self.label_um_ins8.place(x = 890, y = 340)  

        #--------------- 9

        def sel9():
            seleccionar_insumo(9)

        self.btn_ins9 = CTkButton(self,text="Insumo9", command=sel9, width=75)
        self.btn_ins9.place(x = 650, y = 380) 

        self.texto_ins9 = CTkEntry(self,placeholder_text="codigo...", width=60)
        self.texto_ins9.place(x = 740, y = 380)         

        self.texto_cant9 = CTkEntry(self,placeholder_text="cantidad...", width=70)
        self.texto_cant9.place(x = 810, y = 380) 

        self.texto_cant9.bind("<KeyRelease>", calcular_costo)  

        self.label_um_ins9 = CTkLabel(self, textvariable= string_ins9, font=("Times New Roman",16))
        self.label_um_ins9.place(x = 890, y = 380)         

        #--------------- 10

        def sel10():
            seleccionar_insumo(10)

        self.btn_ins10 = CTkButton(self,text="Insumo10", command=sel10, width=75)
        self.btn_ins10.place(x = 650, y = 420) 

        self.texto_ins10 = CTkEntry(self,placeholder_text="codigo...", width=60)
        self.texto_ins10.place(x = 740, y = 420)         

        self.texto_cant10 = CTkEntry(self,placeholder_text="cantidad...", width=70)
        self.texto_cant10.place(x = 810, y = 420) 

        self.texto_cant10.bind("<KeyRelease>", calcular_costo)  

        self.label_um_ins10 = CTkLabel(self, textvariable= string_ins10, font=("Times New Roman",16))
        self.label_um_ins10.place(x = 890, y = 420) 

        def agregar_producto():
            # confirmar
            conf = messagebox.askokcancel("Confirmar","Se va a agregar el producto")
            if conf:
                avanzar = False
                try:
                    if self.texto_precio.get() == "":
                        pass
                    else:
                        float(self.texto_precio.get())  

                    if self.texto_ins1.get() == "":
                        pass
                    else:                
                        float(self.texto_ins1.get())

                    if self.texto_cant1.get() == "":
                        pass
                    else:                        
                        float(self.texto_cant1.get())

                    if self.texto_ins2.get() == "":
                        pass
                    else:
                        float(self.texto_ins2.get())

                    if self.texto_cant2.get() == "":
                        pass
                    else:                
                        float(self.texto_cant2.get())

                    if self.texto_ins3.get() == "":
                        pass
                    else:
                        float(self.texto_ins3.get())

                    if self.texto_cant3.get() == "":
                        pass
                    else:
                        float(self.texto_cant3.get())

                    if self.texto_ins4.get() == "":
                        pass
                    else:
                        float(self.texto_ins4.get())

                    if self.texto_cant4.get() == "":
                        pass
                    else:
                        float(self.texto_cant4.get())

                    if self.texto_ins5.get() == "":
                        pass
                    else:
                        float(self.texto_ins5.get())

                    if self.texto_cant5.get() == "":
                        pass
                    else:
                        float(self.texto_cant5.get())

                    if self.texto_ins6.get() == "":
                        pass
                    else:
                        float(self.texto_ins6.get())

                    if self.texto_cant6.get() == "":
                        pass
                    else:
                        float(self.texto_cant6.get())

                    if self.texto_ins7.get() == "":
                        pass
                    else:
                        float(self.texto_ins7.get())

                    if self.texto_cant7.get() == "":
                        pass
                    else:
                        float(self.texto_cant7.get())

                    if self.texto_ins8.get() == "":
                        pass
                    else:
                        float(self.texto_ins8.get())

                    if self.texto_cant8.get() == "":
                        pass
                    else:
                        float(self.texto_cant8.get())

                    if self.texto_ins9.get() == "":
                        pass
                    else:
                        float(self.texto_ins9.get())

                    if self.texto_cant9.get() == "":
                        pass
                    else:
                        float(self.texto_cant9.get())

                    if self.texto_ins10.get() == "":
                        pass
                    else:
                        float(self.texto_ins10.get())

                    if self.texto_cant10.get() == "":
                        pass
                    else:
                        float(self.texto_cant10.get())                    

                    avanzar = True

                except:
                    error = messagebox.showerror("Error","Verifica los datos que escribiste")

                if self.texto_nombre.get() == "" or self.texto_precio.get() == "" or self.texto_categoria.get() == "":
                    error = messagebox.showerror("Error","Debes llenar los campor de arriba")
                    avanzar = False

                if avanzar:
                    try:
                        # encontremos el codigo del producto                
                        id_producto = 1
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
                            )
                        cursor = conn.cursor()

                        sql = """SELECT MAX(Codigo) FROM `productos`;"""
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == None:
                                pass
                            else:
                                id_producto = index[0] + 1 

                        # vamos a darle entrada a la bd 
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `productos`(`Codigo`, `Nombre`, `Costo`, `Precio`, `Categoria`, `Insumo1`, `Cantidad1`, `Insumo2`, `Cantidad2`, `Insumo3`, `Cantidad3`, `Insumo4`, `Cantidad4`, `Insumo5`, `Cantidad5`, `Insumo6`, `Cantidad6`, `Insumo7`, `Cantidad7`, `Insumo8`, `Cantidad8`, `Insumo9`, `Cantidad9`, `Insumo10`, `Cantidad10`) VALUES ('{id_producto}','{self.texto_nombre.get()}','{float(string_costo.get())}','{self.texto_precio.get()}','{self.texto_categoria.get()}','{self.texto_ins1.get()}','{self.texto_cant1.get()}','{self.texto_ins2.get()}','{self.texto_cant2.get()}','{self.texto_ins3.get()}','{self.texto_cant3.get()}','{self.texto_ins4.get()}','{self.texto_cant4.get()}','{self.texto_ins5.get()}','{self.texto_cant5.get()}','{self.texto_ins6.get()}','{self.texto_cant6.get()}','{self.texto_ins7.get()}','{self.texto_cant7.get()}','{self.texto_ins8.get()}','{self.texto_cant8.get()}','{self.texto_ins9.get()}','{self.texto_cant9.get()}','{self.texto_ins10.get()}','{self.texto_cant10.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        self.destroy()

                    except:
                        error = messagebox.showerror("Error","No se pudo agregar el producto")


        self.btn_agregar = CTkButton(self,text="Agregar Producto", command=agregar_producto, width=300, height=50)
        self.btn_agregar.place(x = 350, y = 500) 


# **********************************************************************************
# ****************************** Modificar Producto ********************************
# **********************************************************************************

class ModificarProducto(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Productos")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 600
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("600x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        def llenar(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "condesa",
                password = "123456",
                database = "condesa"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM productos WHERE  `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%'; """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],))  

        # buscador
        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por Nombre ...")
        self.texto_buscador_nombre.pack(pady=10)

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar) 

        # tabla de insumos
        estilos_tablas()        
                
        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Costo", "Precio", "Categoria"), show="headings")
        self.tabla.column("#0", width = 75, anchor="center")
        self.tabla.column("Nombre", width = 200, anchor="center")
        self.tabla.column("Costo", width = 100, anchor="center")
        self.tabla.column("Precio", width = 100, anchor="center")                   
        self.tabla.column("Categoria", width = 200, anchor="center")        

        self.tabla.pack(pady=10)        
        self.tabla.config(height = 20)

        self.tabla.heading("#0", text = "Codigo")
        self.tabla.heading("Nombre", text = "Nombre")
        self.tabla.heading("Costo", text = "Costo")
        self.tabla.heading("Precio", text = "Precio")                  
        self.tabla.heading("Categoria", text = "Categoria")        

        self.scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        self.scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = self.scrollbar.set)

        llenar(True)

        def doble_click(event):
            global codigo_producto
            
            # vamos a capturar el codigo del producto
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                codigo_producto = self.tabla.item(item, "text") 

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
            temp.after(250, lambda: temp.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico')) 

            def eliminar():                
                conf = messagebox.askokcancel("Confirmar","Vamos a eliminar el producto")
                if conf:
                    try:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
                            )
                        cursor = conn.cursor()

                        sql = f""" DELETE FROM `productos` WHERE `Codigo` = "{codigo_producto}" """
                        cursor.execute(sql)
                        conn.commit()

                        llenar(True)                        
                        temp.destroy()
                    
                    except:
                        error = messagebox.showerror("Error","No se pudo eliminar el producto")            

            temp.btn_eliminar = CTkButton(temp,text="Eliminar", command=eliminar)
            temp.btn_eliminar.pack(pady=20) 

            def modificar():
                temp.destroy()
                vent1 = CTkToplevel()
                vent1.title("Modificar Producto")    
                htotal = vent1.winfo_screenheight()
                wtotal = vent1.winfo_screenwidth()
                wventana = 1000
                hventana = 600
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                vent1.geometry(f"+{posx}+{posy}")
                vent1.geometry("1000x600") 
                vent1.resizable(False,False)
                vent1.after(250, lambda: vent1.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
                vent1.lift()
                vent1.attributes('-topmost', True)
                vent1.after(200, lambda: vent1.attributes('-topmost', False)) 
        
                ############ agregar el fondo de pantalla #########
                
                vent1.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo2.jpg"), size = (600,200))  
        
                vent1.label_image = CTkLabel(vent1, image = vent1.imagen, text = "")  
                vent1.label_image.place(x = 0, y = 0)      
        
                #######################################################  

                # ************************** Labels *************************   
                
                vent1.label_nombre = CTkLabel(vent1,text="Nombre:", font=("Times New Roman",16))
                vent1.label_nombre.place(x = 630, y = 20) 
                
                vent1.texto_nombre = CTkEntry(vent1)
                vent1.texto_nombre.place(x = 750, y = 20)       
        
                vent1.label_costo = CTkLabel(vent1,text="Costo:", font=("Times New Roman",16))
                vent1.label_costo.place(x = 630, y = 60) 
        
                string_costo = StringVar()
                string_costo.set("0") 
        
                vent1.texto_costo = CTkLabel(vent1,textvariable=string_costo, font=("Times New Roman",16))
                vent1.texto_costo.place(x = 750, y = 60) 
        
                vent1.label_precio = CTkLabel(vent1,text="Precio:", font=("Times New Roman",16))
                vent1.label_precio.place(x = 630, y = 100)  
        
                vent1.texto_precio = CTkEntry(vent1)
                vent1.texto_precio.place(x = 750, y = 100) 

                vent1.label_costoxprecio = CTkLabel(vent1,text="C / P:", font=("Times New Roman",16))
                vent1.label_costoxprecio.place(x = 630, y = 140) 
        
                string_costoxprecio = StringVar()
                string_costoxprecio.set("0") 
        
                vent1.texto_costoxprecio = CTkLabel(vent1,textvariable=string_costoxprecio, font=("Times New Roman",16))
                vent1.texto_costoxprecio.place(x = 750, y = 140) 
        
                def cxp(event):            
                    string_costoxprecio.set(float(string_costo.get())/float(vent1.texto_precio.get()))
        
                vent1.texto_precio.bind("<KeyRelease>", cxp) 
        
                vent1.label_categoria = CTkLabel(vent1,text="Categoria:", font=("Times New Roman",16))
                vent1.label_categoria.place(x = 630, y = 180)  
        
                categorias = []
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()
        
                sql = """SELECT * FROM `categorias_productos`;"""
                cursor.execute(sql)
                for index in cursor:
                    categorias.append(index[0])
        
                vent1.texto_categoria = CTkComboBox(vent1, values=categorias)
                vent1.texto_categoria.set("...")
                vent1.texto_categoria.place(x = 750, y = 180)  

                vent1.label_div = CTkLabel(vent1,text="**************************************** Seccion Insumos ****************************************", font=("Times New Roman",16))
                vent1.label_div.place(x = 150, y =220)  

                # funciones para calcular el costo total del producto segun sus insumos
                def calc1():                
                    if vent1.texto_ins1.get() == "":
                        return 0
                    else:
                        if vent1.texto_cant1.get()=="":
                            cost = 0
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
                
                            sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {vent1.texto_ins1.get()} """
                            cursor.execute(sql)
                            for index in cursor:
                                cost = float(vent1.texto_cant1.get())*index[0]
        
                        return cost
        
                def calc2():                
                    if vent1.texto_ins2.get() == "":
                        return 0
                    else:
                        if vent1.texto_cant2.get()=="":
                            cost = 0
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
                
                            sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {vent1.texto_ins2.get()} """
                            cursor.execute(sql)
                            for index in cursor:
                                cost = float(vent1.texto_cant2.get())*index[0]
        
                        return cost
        
                def calc3():                
                    if vent1.texto_ins3.get() == "":
                        return 0
                    else:
                        if vent1.texto_cant3.get()=="":
                            cost = 0
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
                
                            sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {vent1.texto_ins3.get()} """
                            cursor.execute(sql)
                            for index in cursor:
                                cost = float(vent1.texto_cant3.get())*index[0]
        
                        return cost
        
                def calc4():                
                    if vent1.texto_ins4.get() == "":
                        return 0
                    else:
                        if vent1.texto_cant4.get()=="":
                            cost = 0
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
                
                            sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {vent1.texto_ins4.get()} """
                            cursor.execute(sql)
                            for index in cursor:
                                cost = float(vent1.texto_cant4.get())*index[0]
        
                        return cost
        
                def calc5():                
                    if vent1.texto_ins5.get() == "":
                        return 0
                    else:
                        if vent1.texto_cant5.get()=="":
                            cost = 0
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
                
                            sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {vent1.texto_ins5.get()} """
                            cursor.execute(sql)
                            for index in cursor:
                                cost = float(vent1.texto_cant5.get())*index[0]
        
                        return cost
        
                def calc6():                
                    if vent1.texto_ins6.get() == "":
                        return 0
                    else:
                        if vent1.texto_cant6.get()=="":
                            cost = 0
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
                
                            sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {vent1.texto_ins6.get()} """
                            cursor.execute(sql)
                            for index in cursor:
                                cost = float(vent1.texto_cant6.get())*index[0]
        
                        return cost
        
                def calc7():                
                    if vent1.texto_ins7.get() == "":
                        return 0
                    else:
                        if vent1.texto_cant7.get()=="":
                            cost = 0
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
                
                            sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {vent1.texto_ins7.get()} """
                            cursor.execute(sql)
                            for index in cursor:
                                cost = float(vent1.texto_cant7.get())*index[0]
        
                        return cost
        
                def calc8():                
                    if vent1.texto_ins8.get() == "":
                        return 0
                    else:
                        if vent1.texto_cant8.get()=="":
                            cost = 0
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
                
                            sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {vent1.texto_ins8.get()} """
                            cursor.execute(sql)
                            for index in cursor:
                                cost = float(vent1.texto_cant8.get())*index[0]
        
                        return cost
        
                def calc9():                
                    if vent1.texto_ins9.get() == "":
                        return 0
                    else:
                        if vent1.texto_cant9.get()=="":
                            cost = 0
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
                
                            sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {vent1.texto_ins9.get()} """
                            cursor.execute(sql)
                            for index in cursor:
                                cost = float(vent1.texto_cant9.get())*index[0]
        
                        return cost
        
                def calc10():                
                    if vent1.texto_ins10.get() == "":
                        return 0
                    else:
                        if vent1.texto_cant10.get()=="":
                            cost = 0
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
                
                            sql = f""" SELECT  `Costo` FROM `insumos` WHERE `Codigo` = {vent1.texto_ins10.get()} """
                            cursor.execute(sql)
                            for index in cursor:
                                cost = float(vent1.texto_cant10.get())*index[0]
        
                        return cost
        
                def calc(opcion):
                    if opcion == 1:
                        return calc1()
                    if opcion == 2:
                        return calc2()
                    if opcion == 3:
                        return calc3()
                    if opcion == 4:
                        return calc4()
                    if opcion == 5:
                        return calc5()
                    if opcion == 6:
                        return calc6()
                    if opcion == 7:
                        return calc7()
                    if opcion == 8:
                        return calc8()
                    if opcion == 9:
                        return calc9()
                    if opcion == 10:
                        return calc10()
        
                def calcular_costo(event):
                    costo = 0
                    for i in range(1, 11):
                        costo += calc(i)
                    string_costo.set(str(costo))


                # --------------- seleccion de insumos
                def seleccionar_insumo(opcion):
                    # aqui vamos a llenar la info del insumo 1 
                    # hay que crear una ventana donde mostremos los insumos y podamos escoger el que queremos ahi 
                    vent2 = CTkToplevel()
                    vent2.title("Seleccionar Insumo") 
                    htotal = vent2.winfo_screenheight()
                    wtotal = vent2.winfo_screenwidth()            
                    posx = round(wtotal/2-wventana/2)
                    posy = round(htotal/2-hventana/2)
                    vent2.geometry(f"+{posx}+{posy}")
                    vent2.lift()
                    vent2.attributes('-topmost', True)
                    vent2.after(200, lambda: vent2.attributes('-topmost', False)) 
                    vent2.after(250, lambda: vent2.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico')) 
        
                    def llenar2(event):
                        vent2.tabla.delete(*vent2.tabla.get_children())
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
                            )
                        cursor = conn.cursor()
            
                        sql = f""" SELECT * FROM insumos WHERE  `Nombre` LIKE '%{vent2.texto_buscador_nombre.get()}%'; """
                        cursor.execute(sql)
                        for index in cursor:
                            vent2.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],))  
        
                    # buscador
                    vent2.texto_buscador_nombre = CTkEntry(vent2,placeholder_text="Buscar por Nombre ...")
                    vent2.texto_buscador_nombre.pack(pady=10)
        
                    vent2.texto_buscador_nombre.bind("<KeyRelease>", llenar2) 
        
                    # tabla de insumos
                    estilos_tablas()        
                            
                    vent2.tabla = ttk.Treeview(vent2, columns = ("Nombre", "Costo", "Precio", "U/M", "Categoria"), show="headings")
                    vent2.tabla.column("#0", width = 75, anchor="center")
                    vent2.tabla.column("Nombre", width = 200, anchor="center")
                    vent2.tabla.column("Costo", width = 100, anchor="center")
                    vent2.tabla.column("Precio", width = 75, anchor="center")
                    vent2.tabla.column("U/M", width = 75, anchor="center")            
                    vent2.tabla.column("Categoria", width = 200, anchor="center")        
            
                    vent2.tabla.pack(pady=10)        
                    vent2.tabla.config(height = 10)
            
                    vent2.tabla.heading("#0", text = "Codigo")
                    vent2.tabla.heading("Nombre", text = "Nombre")
                    vent2.tabla.heading("Costo", text = "Costo")
                    vent2.tabla.heading("Precio", text = "Precio")
                    vent2.tabla.heading("U/M", text = "U/M")            
                    vent2.tabla.heading("Categoria", text = "Categoria")        
            
                    vent2.scrollbar = CTkScrollbar(vent2, command = vent2.tabla.yview, width = 18)
                    vent2.scrollbar.place(in_ = vent2.tabla, relheigh = 1, relx = 1)
            
                    vent2.tabla.config(yscrollcommand = vent2.scrollbar.set)
        
                    llenar2(True)
        
                    # ahora hay que seleccionar el insumo con 2ble click
                    def escoger(event):                              
                        # vamos a capturar el codigo del numero que vamos a reabastecer
                        seleccion = vent2.tabla.selection()
                        if seleccion:
                            item = seleccion[0]                
                            cod = vent2.tabla.item(item, "text")  
                            medida = vent2.tabla.item(item, "values")[3] 
        
                        # ahora vamos a escribir los datos en la ventana exterior
                        if opcion == 1:
                            vent1.texto_ins1.delete(0,END)
                            string_ins1.set("")
                            vent1.texto_ins1.insert(0,cod)
                            string_ins1.set(medida)
        
                        elif opcion == 2:
                            vent1.texto_ins2.delete(0,END)
                            string_ins2.set("")
                            vent1.texto_ins2.insert(0,cod)
                            string_ins2.set(medida)
        
                        elif opcion == 3:
                            vent1.texto_ins3.delete(0,END)
                            string_ins3.set("")
                            vent1.texto_ins3.insert(0,cod)
                            string_ins3.set(medida)
        
                        elif opcion == 4:
                            vent1.texto_ins4.delete(0,END)
                            string_ins4.set("")
                            vent1.texto_ins4.insert(0,cod)
                            string_ins4.set(medida)
        
                        elif opcion == 5:
                            vent1.texto_ins5.delete(0,END)
                            string_ins5.set("")
                            vent1.texto_ins5.insert(0,cod)
                            string_ins5.set(medida)
        
                        elif opcion == 6:
                            vent1.texto_ins6.delete(0,END)
                            string_ins6.set("")
                            vent1.texto_ins6.insert(0,cod)
                            string_ins6.set(medida)
        
                        elif opcion == 7:
                            vent1.texto_ins7.delete(0,END)
                            string_ins7.set("")
                            vent1.texto_ins7.insert(0,cod)
                            string_ins7.set(medida)
        
                        elif opcion == 8:
                            vent1.texto_ins8.delete(0,END)
                            string_ins8.set("")
                            vent1.texto_ins8.insert(0,cod)
                            string_ins8.set(medida)
        
                        elif opcion == 9:
                            vent1.texto_ins9.delete(0,END)
                            string_ins9.set("")
                            vent1.texto_ins9.insert(0,cod)
                            string_ins9.set(medida)
        
                        elif opcion == 10:
                            vent1.texto_ins10.delete(0,END)
                            string_ins10.set("")
                            vent1.texto_ins10.insert(0,cod)
                            string_ins10.set(medida)
        
                        calcular_costo(True)
        
                        vent2.destroy()               
        
                    vent2.tabla.bind("<Double-1>", escoger)
        
                string_ins1 = StringVar()
                string_ins2 = StringVar()
                string_ins3 = StringVar()
                string_ins4 = StringVar()
                string_ins5 = StringVar()
                string_ins6 = StringVar()
                string_ins7 = StringVar()
                string_ins8 = StringVar()
                string_ins9 = StringVar()
                string_ins10 = StringVar()


                #--------------- 1
                
                def sel1():
                    seleccionar_insumo(1)
        
                vent1.btn_ins1 = CTkButton(vent1,text="Insumo1", command=sel1, width=75)
                vent1.btn_ins1.place(x = 100, y = 260) 
        
                vent1.texto_ins1 = CTkEntry(vent1,placeholder_text="codigo...", width=60)
                vent1.texto_ins1.place(x = 190, y = 260)         
        
                vent1.texto_cant1 = CTkEntry(vent1,placeholder_text="cantidad...", width=70)
                vent1.texto_cant1.place(x = 260, y = 260)  
        
                vent1.texto_cant1.bind("<KeyRelease>", calcular_costo)    
        
                vent1.label_um_ins1 = CTkLabel(vent1, textvariable= string_ins1, font=("Times New Roman",16))
                vent1.label_um_ins1.place(x = 340, y = 260) 
        
                #--------------- 2
        
                def sel2():
                    seleccionar_insumo(2)
        
                vent1.btn_ins2 = CTkButton(vent1,text="Insumo2", command=sel2, width=75)
                vent1.btn_ins2.place(x = 100, y = 300) 
        
                vent1.texto_ins2 = CTkEntry(vent1,placeholder_text="codigo...", width=60)
                vent1.texto_ins2.place(x = 190, y = 300)         
        
                vent1.texto_cant2 = CTkEntry(vent1,placeholder_text="cantidad...", width=70)
                vent1.texto_cant2.place(x = 260, y = 300)  
        
                vent1.texto_cant2.bind("<KeyRelease>", calcular_costo) 
        
                vent1.label_um_ins2 = CTkLabel(vent1, textvariable= string_ins2, font=("Times New Roman",16))
                vent1.label_um_ins2.place(x = 340, y = 300) 
        
                #--------------- 3
        
                def sel3():
                    seleccionar_insumo(3)
        
                vent1.btn_ins3 = CTkButton(vent1,text="Insumo3", command=sel3, width=75)
                vent1.btn_ins3.place(x = 100, y = 340) 
        
                vent1.texto_ins3 = CTkEntry(vent1,placeholder_text="codigo...", width=60)
                vent1.texto_ins3.place(x = 190, y = 340)         
        
                vent1.texto_cant3 = CTkEntry(vent1,placeholder_text="cantidad...", width=70)
                vent1.texto_cant3.place(x = 260, y = 340)  
        
                vent1.texto_cant3.bind("<KeyRelease>", calcular_costo) 
        
                vent1.label_um_ins3 = CTkLabel(vent1, textvariable= string_ins3, font=("Times New Roman",16))
                vent1.label_um_ins3.place(x = 340, y = 340) 
        
                #--------------- 4
        
                def sel4():
                    seleccionar_insumo(4)
        
                vent1.btn_ins4 = CTkButton(vent1,text="Insumo4", command=sel4, width=75)
                vent1.btn_ins4.place(x = 100, y = 380) 
        
                vent1.texto_ins4 = CTkEntry(vent1,placeholder_text="codigo...", width=60)
                vent1.texto_ins4.place(x = 190, y = 380)         
        
                vent1.texto_cant4 = CTkEntry(vent1,placeholder_text="cantidad...", width=70)
                vent1.texto_cant4.place(x = 260, y = 380)  
        
                vent1.texto_cant4.bind("<KeyRelease>", calcular_costo) 
        
                vent1.label_um_ins4 = CTkLabel(vent1, textvariable= string_ins4, font=("Times New Roman",16))
                vent1.label_um_ins4.place(x = 340, y = 380)  
        
                #--------------- 5
        
                def sel5():
                    seleccionar_insumo(5)
        
                vent1.btn_ins5 = CTkButton(vent1,text="Insumo5", command=sel5, width=75)
                vent1.btn_ins5.place(x = 100, y = 420) 
        
                vent1.texto_ins5 = CTkEntry(vent1,placeholder_text="codigo...", width=60)
                vent1.texto_ins5.place(x = 190, y = 420)         
        
                vent1.texto_cant5 = CTkEntry(vent1,placeholder_text="cantidad...", width=70)
                vent1.texto_cant5.place(x = 260, y = 420) 
        
                vent1.texto_cant5.bind("<KeyRelease>", calcular_costo)  
        
                vent1.label_um_ins5 = CTkLabel(vent1, textvariable= string_ins5, font=("Times New Roman",16))
                vent1.label_um_ins5.place(x = 340, y = 420)  
        
                #--------------- 6
        
                def sel6():
                    seleccionar_insumo(6)
        
                vent1.btn_ins6 = CTkButton(vent1,text="Insumo6", command=sel6, width=75)
                vent1.btn_ins6.place(x = 650, y = 260) 
        
                vent1.texto_ins6 = CTkEntry(vent1,placeholder_text="codigo...", width=60)
                vent1.texto_ins6.place(x = 740, y = 260)         
        
                vent1.texto_cant6 = CTkEntry(vent1,placeholder_text="cantidad...", width=70)
                vent1.texto_cant6.place(x = 810, y = 260) 
        
                vent1.texto_cant6.bind("<KeyRelease>", calcular_costo)  
        
                vent1.label_um_ins6 = CTkLabel(vent1, textvariable= string_ins6, font=("Times New Roman",16))
                vent1.label_um_ins6.place(x = 890, y = 260)  
        
                #--------------- 7
        
                def sel7():
                    seleccionar_insumo(7)
        
                vent1.btn_ins7 = CTkButton(vent1,text="Insumo7", command=sel7, width=75)
                vent1.btn_ins7.place(x = 650, y = 300) 
        
                vent1.texto_ins7 = CTkEntry(vent1,placeholder_text="codigo...", width=60)
                vent1.texto_ins7.place(x = 740, y = 300)         
        
                vent1.texto_cant7 = CTkEntry(vent1,placeholder_text="cantidad...", width=70)
                vent1.texto_cant7.place(x = 810, y = 300)  
        
                vent1.texto_cant7.bind("<KeyRelease>", calcular_costo) 
        
                vent1.label_um_ins7 = CTkLabel(vent1, textvariable= string_ins7, font=("Times New Roman",16))
                vent1.label_um_ins7.place(x = 890, y = 300)  
        
                #--------------- 8
        
                def sel8():
                    seleccionar_insumo(8)
        
                vent1.btn_ins8 = CTkButton(vent1,text="Insumo8", command=sel8, width=75)
                vent1.btn_ins8.place(x = 650, y = 340) 
        
                vent1.texto_ins8 = CTkEntry(vent1,placeholder_text="codigo...", width=60)
                vent1.texto_ins8.place(x = 740, y = 340)         
        
                vent1.texto_cant8 = CTkEntry(vent1,placeholder_text="cantidad...", width=70)
                vent1.texto_cant8.place(x = 810, y = 340)  
        
                vent1.texto_cant8.bind("<KeyRelease>", calcular_costo) 
        
                vent1.label_um_ins8 = CTkLabel(vent1, textvariable= string_ins8, font=("Times New Roman",16))
                vent1.label_um_ins8.place(x = 890, y = 340)  
        
                #--------------- 9
        
                def sel9():
                    seleccionar_insumo(9)
        
                vent1.btn_ins9 = CTkButton(vent1,text="Insumo9", command=sel9, width=75)
                vent1.btn_ins9.place(x = 650, y = 380) 
        
                vent1.texto_ins9 = CTkEntry(vent1,placeholder_text="codigo...", width=60)
                vent1.texto_ins9.place(x = 740, y = 380)         
        
                vent1.texto_cant9 = CTkEntry(vent1,placeholder_text="cantidad...", width=70)
                vent1.texto_cant9.place(x = 810, y = 380) 
        
                vent1.texto_cant9.bind("<KeyRelease>", calcular_costo)  
        
                vent1.label_um_ins9 = CTkLabel(vent1, textvariable= string_ins9, font=("Times New Roman",16))
                vent1.label_um_ins9.place(x = 890, y = 380)         
        
                #--------------- 10
        
                def sel10():
                    seleccionar_insumo(10)
        
                vent1.btn_ins10 = CTkButton(vent1,text="Insumo10", command=sel10, width=75)
                vent1.btn_ins10.place(x = 650, y = 420) 
        
                vent1.texto_ins10 = CTkEntry(vent1,placeholder_text="codigo...", width=60)
                vent1.texto_ins10.place(x = 740, y = 420)         
        
                vent1.texto_cant10 = CTkEntry(vent1,placeholder_text="cantidad...", width=70)
                vent1.texto_cant10.place(x = 810, y = 420) 
        
                vent1.texto_cant10.bind("<KeyRelease>", calcular_costo)  
        
                vent1.label_um_ins10 = CTkLabel(vent1, textvariable= string_ins10, font=("Times New Roman",16))
                vent1.label_um_ins10.place(x = 890, y = 420) 


                def modificar_producto():
                    # confirmar
                    conf = messagebox.askokcancel("Confirmar","Se va a agregar el producto")
                    if conf:
                        avanzar = False
                        try:
                            if vent1.texto_precio.get() == "":
                                pass
                            else:
                                float(vent1.texto_precio.get())  
        
                            if vent1.texto_ins1.get() == "":
                                pass
                            else:                
                                float(vent1.texto_ins1.get())
        
                            if vent1.texto_cant1.get() == "":
                                pass
                            else:                        
                                float(vent1.texto_cant1.get())
        
                            if vent1.texto_ins2.get() == "":
                                pass
                            else:
                                float(vent1.texto_ins2.get())
        
                            if vent1.texto_cant2.get() == "":
                                pass
                            else:                
                                float(vent1.texto_cant2.get())
        
                            if vent1.texto_ins3.get() == "":
                                pass
                            else:
                                float(vent1.texto_ins3.get())
        
                            if vent1.texto_cant3.get() == "":
                                pass
                            else:
                                float(vent1.texto_cant3.get())
        
                            if vent1.texto_ins4.get() == "":
                                pass
                            else:
                                float(vent1.texto_ins4.get())
        
                            if vent1.texto_cant4.get() == "":
                                pass
                            else:
                                float(vent1.texto_cant4.get())
        
                            if vent1.texto_ins5.get() == "":
                                pass
                            else:
                                float(vent1.texto_ins5.get())
        
                            if vent1.texto_cant5.get() == "":
                                pass
                            else:
                                float(vent1.texto_cant5.get())
        
                            if vent1.texto_ins6.get() == "":
                                pass
                            else:
                                float(vent1.texto_ins6.get())
        
                            if vent1.texto_cant6.get() == "":
                                pass
                            else:
                                float(vent1.texto_cant6.get())
        
                            if vent1.texto_ins7.get() == "":
                                pass
                            else:
                                float(vent1.texto_ins7.get())
        
                            if vent1.texto_cant7.get() == "":
                                pass
                            else:
                                float(vent1.texto_cant7.get())
        
                            if vent1.texto_ins8.get() == "":
                                pass
                            else:
                                float(vent1.texto_ins8.get())
        
                            if vent1.texto_cant8.get() == "":
                                pass
                            else:
                                float(vent1.texto_cant8.get())
        
                            if vent1.texto_ins9.get() == "":
                                pass
                            else:
                                float(vent1.texto_ins9.get())
        
                            if vent1.texto_cant9.get() == "":
                                pass
                            else:
                                float(vent1.texto_cant9.get())
        
                            if vent1.texto_ins10.get() == "":
                                pass
                            else:
                                float(vent1.texto_ins10.get())
        
                            if vent1.texto_cant10.get() == "":
                                pass
                            else:
                                float(vent1.texto_cant10.get())                    
        
                            avanzar = True
        
                        except:
                            error = messagebox.showerror("Error","Verifica los datos que escribiste")
        
                        if vent1.texto_nombre.get() == "" or vent1.texto_precio.get() == "" or vent1.texto_categoria.get() == "":
                            error = messagebox.showerror("Error","Debes llenar los campor de arriba")
                            avanzar = False

                        if avanzar:
                            try:
                                # vamos a modificar en la bd 
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "condesa",
                                    password = "123456",
                                    database = "condesa"
                                    )
                                cursor = conn.cursor()
        
                                sql = f""" UPDATE `productos` SET `Nombre`='{vent1.texto_nombre.get()}',`Costo`='{float(string_costo.get())}',`Precio`='{vent1.texto_precio.get()}',`Categoria`='{vent1.texto_categoria.get()}',`Insumo1`='{vent1.texto_ins1.get()}',`Cantidad1`='{vent1.texto_cant1.get()}',`Insumo2`='{vent1.texto_ins2.get()}',`Cantidad2`='{vent1.texto_cant2.get()}',`Insumo3`='{vent1.texto_ins3.get()}',`Cantidad3`='{vent1.texto_cant3.get()}',`Insumo4`='{vent1.texto_ins4.get()}',`Cantidad4`='{vent1.texto_cant4.get()}',`Insumo5`='{vent1.texto_ins5.get()}',`Cantidad5`='{vent1.texto_cant5.get()}',`Insumo6`='{vent1.texto_ins6.get()}',`Cantidad6`='{vent1.texto_cant6.get()}',`Insumo7`='{vent1.texto_ins7.get()}',`Cantidad7`='{vent1.texto_cant7.get()}',`Insumo8`='{vent1.texto_ins8.get()}',`Cantidad8`='{vent1.texto_cant8.get()}',`Insumo9`='{vent1.texto_ins9.get()}',`Cantidad9`='{vent1.texto_cant9.get()}',`Insumo10`='{vent1.texto_ins10.get()}',`Cantidad10`='{vent1.texto_cant10.get()}' WHERE `Codigo` = {codigo_producto} """
                                cursor.execute(sql)
                                conn.commit()

                                llenar(True)        
                                vent1.destroy()
        
                            except:
                                error = messagebox.showerror("Error","No se pudo agregar el producto")

                vent1.btn_modificar = CTkButton(vent1,text="Modificar Producto", command=modificar_producto, width=300, height=50)
                vent1.btn_modificar.place(x = 350, y = 500) 

                # ahora vamos a mostrar la info que estaba anteriormente                
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `productos` WHERE `Codigo` = {codigo_producto} """
                cursor.execute(sql)
                for index in cursor:
                    vent1.texto_nombre.insert(0,index[1])
                    string_costo.set(index[2])
                    vent1.texto_precio.insert(0,index[3])
                    vent1.texto_categoria.set(index[4])

                    if index[5] == 0:
                        pass
                    else:
                        vent1.texto_ins1.insert(0,index[5])

                    if index[6] == 0:
                        pass
                    else:
                        vent1.texto_cant1.insert(0,index[6])

                    if index[7] == 0:
                        pass
                    else:
                        vent1.texto_ins2.insert(0,index[7])

                    if index[8] == 0:
                        pass
                    else:
                        vent1.texto_cant2.insert(0,index[8])

                    if index[9] == 0:
                        pass
                    else:
                        vent1.texto_ins3.insert(0,index[9])

                    if index[10] == 0:
                        pass
                    else:
                        vent1.texto_cant3.insert(0,index[10])

                    if index[11] == 0:
                        pass
                    else:
                        vent1.texto_ins4.insert(0,index[11])

                    if index[12] == 0:
                        pass
                    else:
                        vent1.texto_cant4.insert(0,index[12])

                    if index[13] == 0:
                        pass
                    else:
                        vent1.texto_ins5.insert(0,index[13])

                    if index[14] == 0:
                        pass
                    else:
                        vent1.texto_cant5.insert(0,index[14])

                    if index[15] == 0:
                        pass
                    else:
                        vent1.texto_ins6.insert(0,index[15])

                    if index[16] == 0:
                        pass
                    else:
                        vent1.texto_cant6.insert(0,index[16])

                    if index[17] == 0:
                        pass
                    else:
                        vent1.texto_ins7.insert(0,index[17])

                    if index[18] == 0:
                        pass
                    else:
                        vent1.texto_cant7.insert(0,index[18])

                    if index[19] == 0:
                        pass
                    else:
                        vent1.texto_ins8.insert(0,index[19])

                    if index[20] == 0:
                        pass
                    else:
                        vent1.texto_cant8.insert(0,index[20])

                    if index[21] == 0:
                        pass
                    else:
                        vent1.texto_ins9.insert(0,index[21])

                    if index[22] == 0:
                        pass
                    else:
                        vent1.texto_cant9.insert(0,index[22])

                    if index[23] == 0:
                        pass
                    else:
                        vent1.texto_ins10.insert(0,index[23])

                    if index[24] == 0:
                        pass
                    else:
                        vent1.texto_cant10.insert(0,index[24])

                string_costoxprecio.set(float(string_costo.get())/float(vent1.texto_precio.get()))

            temp.btn_modificar = CTkButton(temp,text="Modificar", command=modificar)
            temp.btn_modificar.pack(pady=20)  
            

        self.tabla.bind("<Double-1>", doble_click) 



# **********************************************************************************
# ***********************************  Ventas **************************************
# **********************************************************************************

class Ventas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Ventas")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)          

        ###################################################

        estilos_tablas() 
        
        self.label_productos = CTkLabel(self,text="Productos") 
        self.label_productos.place(x=80,y=40) 

        self.tabla = ttk.Treeview(self, columns = ("Nombre", "Costo", "Precio", "Categoria"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Nombre", width = 200, anchor="center")
        self.tabla.column("Costo", width = 100, anchor="center")
        self.tabla.column("Precio", width = 100, anchor="center")        
        self.tabla.column("Categoria", width = 200, anchor="center")

        self.tabla.place(x = 20, y = 100)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Codigo", anchor="center")
        self.tabla.heading("Nombre", text = "Nombre", anchor="center")
        self.tabla.heading("Costo", text = "Costo", anchor="center")
        self.tabla.heading("Precio", text = "Precio", anchor="center")        
        self.tabla.heading("Categoria", text = "Categoria", anchor="center")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_ventas(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "condesa",
                password = "123456",
                database = "condesa"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM productos WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%'; """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],))  

        self.label_buscador = CTkLabel(self,text="------------------------------ Buscador ------------------------------")
        self.label_buscador.place(x=650,y=80)

        self.texto_buscador_codigo = CTkEntry(self,placeholder_text="Buscar por codigo ...",width=250)
        self.texto_buscador_codigo.place(x=650,y=120)          

        self.texto_buscador_codigo.bind("<KeyRelease>", llenar_ventas) 

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por nombre ...",width=250)
        self.texto_buscador_nombre.place(x=650,y=160) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_ventas ) 

        llenar_ventas(True)

        # cuando demos 2ble click abriremos una ventana para hacer la venta o regalo
        
        def venta(event):
            global codigo
            global values
            # vamos a capturar el codigo del numero que vamos a reabastecer
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                codigo = self.tabla.item(item, "text")  
                values = self.tabla.item(item, "values") 

            temp = CTkToplevel()
            temp.title("Vender") 
            htotal = temp.winfo_screenheight()
            wtotal = temp.winfo_screenwidth()
            wventana = 200
            hventana = 400
            posx = round(wtotal/2-wventana/2)
            posy = round(htotal/2-hventana/2)
            temp.geometry(f"200x400+{posx}+{posy}")
            temp.lift()
            temp.attributes('-topmost', True)
            temp.after(200, lambda: temp.attributes('-topmost', False))
            temp.after(250, lambda: temp.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))             

            temp.texto_concepto_del_regalo = CTkEntry(temp, placeholder_text="Concepto del Regalo ...")

            opcion = IntVar(value=1)

            def radio_select():
                if opcion.get() == 1:  
                    temp.texto_concepto_del_regalo.pack_forget()

                elif opcion.get() == 2:
                    temp.texto_concepto_del_regalo.pack(pady=5)

            temp.radio_vender = CTkRadioButton(temp, text="Vender",command=radio_select, variable=opcion, value=1)
            temp.radio_vender.pack(pady=10)               

            temp.radio_regalar = CTkRadioButton(temp, text="Regalar",command=radio_select, variable=opcion, value=2)
            temp.radio_regalar.pack(pady=10)

            temp.texto_cantidad = CTkEntry(temp, placeholder_text="Cantidad ...")
            temp.texto_cantidad.pack(pady=5)

            def salida():
                if opcion.get() == 1:          # es una venta
                    string = f"Vas a vender {temp.texto_cantidad.get()} {values[0]}"
                    conf = messagebox.askokcancel("Confirmar",string)
                    if conf: 
                        try:
                            # quitemos los insumos consumidos en el almacen
                            ic  = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]   # aqui haremos una lista de los insumos y su cantidad                     

                            # primero veamos cuales son los insumos consumidos y sus cantidades respectivas
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()

                            sql = f""" SELECT `Insumo1`, `Cantidad1`, `Insumo2`, `Cantidad2`, `Insumo3`, `Cantidad3`, `Insumo4`, `Cantidad4`, `Insumo5`, `Cantidad5`, `Insumo6`, `Cantidad6`, `Insumo7`, `Cantidad7`, `Insumo8`, `Cantidad8`, `Insumo9`, `Cantidad9`, `Insumo10`, `Cantidad10` FROM `productos` WHERE `Codigo` = {codigo}"""
                            cursor.execute(sql)
                            for index in cursor:
                                if index[0] == 0:
                                    pass
                                else:
                                    ic[0][0] = index[0]
                                    ic[0][1] = index[1]

                                if index[2] == 0:
                                    pass
                                else:
                                    ic[1][0] = index[2]
                                    ic[1][1] = index[3]

                                if index[4] == 0:
                                    pass
                                else:
                                    ic[2][0] = index[4]
                                    ic[2][1] = index[5]

                                if index[6] == 0:
                                    pass
                                else:
                                    ic[3][0] = index[6]
                                    ic[3][1] = index[7]

                                if index[8] == 0:
                                    pass
                                else:
                                    ic[4][0] = index[8]
                                    ic[4][1] = index[9]

                                if index[10] == 0:
                                    pass
                                else:
                                    ic[5][0] = index[10]
                                    ic[5][1] = index[11]

                                if index[12] == 0:
                                    pass
                                else:
                                    ic[6][0] = index[12]
                                    ic[6][1] = index[13]

                                if index[14] == 0:
                                    pass
                                else:
                                    ic[7][0] = index[14]
                                    ic[7][1] = index[15]

                                if index[16] == 0:
                                    pass
                                else:
                                    ic[8][0] = index[16]
                                    ic[8][1] = index[17]

                                if index[18] == 0:
                                    pass
                                else:
                                    ic[9][0] = index[18]
                                    ic[9][1] = index[19]                         

                            # ahora vamos a restar las cantidades de los insumos usados 
                            for i in ic:   
                                if  i[0] == 0:
                                    pass
                                else:
                                    proceder = False
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "condesa",
                                        password = "123456",
                                        database = "condesa"
                                        )
                                    cursor = conn.cursor()
            
                                    sql = f""" SELECT `Cantidad` FROM `insumos` WHERE `Codigo` = {i[0]} """
                                    cursor.execute(sql)
                                    for index in cursor:
                                        if float(index[0]) >= float(temp.texto_cantidad.get())*float(i[1]):
                                            proceder = True
                                        else:
                                            error = messagebox.showerror("Error","No alcansan los insumos para vender el producto")

                                    if proceder:
                                        # restamos los insumos vendidos
                                        conn = mysql.connector.connect(
                                            host = "localhost",
                                            user = "condesa",
                                            password = "123456",
                                            database = "condesa"
                                            )
                                        cursor = conn.cursor()
                
                                        sql = f""" UPDATE `insumos` SET `Cantidad`= `Cantidad` - '{float(temp.texto_cantidad.get())*float(i[1])}' WHERE `Codigo` = {i[0]} """
                                        cursor.execute(sql)
                                        conn.commit()

                            # encontremos el id de la salida 
                            id_salida = 1
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
    
                            sql = """SELECT MAX(Id) FROM `salidas`;"""
                            cursor.execute(sql)
                            for index in cursor:
                                if index[0] == None:
                                    pass
    
                                else:
                                    id_salida = index[0] + 1 
    
                            # agreguemos la salida en la bd 
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
    
                            sql = f""" INSERT INTO `salidas`(`Id`, `Fecha`, `Codigo`, `Nombre`, `Costo`, `Precio`, `Cantidad`, `Categoria`) VALUES ('{id_salida}','{fecha_actual}','{codigo}','{values[0]}','{values[1]}','{values[2]}','{temp.texto_cantidad.get()}','{values[3]}') """
                            cursor.execute(sql)
                            conn.commit()

                            llenar_ventas(True)
                            temp.destroy()

                        except:
                            error = messagebox.showerror("Error","No se completo la venta \n Revise los datos introducidos")

                elif opcion.get() == 2:        # es un regalo
                    string = f"Vas a reagalar {temp.texto_cantidad.get()} {values[0]}"
                    conf = messagebox.askokcancel("Confirmar",string)
                    if conf:
                        try:
                            # verificamos que tengamos insumos suficientes para hacer el regalo                        
                            ic  = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]   # aqui haremos una lista de los insumos y su cantidad                     

                            # primero veamos cuales son los insumos consumidos y sus cantidades respectivas
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()

                            sql = f""" SELECT `Insumo1`, `Cantidad1`, `Insumo2`, `Cantidad2`, `Insumo3`, `Cantidad3`, `Insumo4`, `Cantidad4`, `Insumo5`, `Cantidad5`, `Insumo6`, `Cantidad6`, `Insumo7`, `Cantidad7`, `Insumo8`, `Cantidad8`, `Insumo9`, `Cantidad9`, `Insumo10`, `Cantidad10` FROM `productos` WHERE `Codigo` = {codigo}"""
                            cursor.execute(sql)
                            for index in cursor:
                                if index[0] == 0:
                                    pass
                                else:
                                    ic[0][0] = index[0]
                                    ic[0][1] = index[1]

                                if index[2] == 0:
                                    pass
                                else:
                                    ic[1][0] = index[2]
                                    ic[1][1] = index[3]

                                if index[4] == 0:
                                    pass
                                else:
                                    ic[2][0] = index[4]
                                    ic[2][1] = index[5]

                                if index[6] == 0:
                                    pass
                                else:
                                    ic[3][0] = index[6]
                                    ic[3][1] = index[7]

                                if index[8] == 0:
                                    pass
                                else:
                                    ic[4][0] = index[8]
                                    ic[4][1] = index[9]

                                if index[10] == 0:
                                    pass
                                else:
                                    ic[5][0] = index[10]
                                    ic[5][1] = index[11]

                                if index[12] == 0:
                                    pass
                                else:
                                    ic[6][0] = index[12]
                                    ic[6][1] = index[13]

                                if index[14] == 0:
                                    pass
                                else:
                                    ic[7][0] = index[14]
                                    ic[7][1] = index[15]

                                if index[16] == 0:
                                    pass
                                else:
                                    ic[8][0] = index[16]
                                    ic[8][1] = index[17]

                                if index[18] == 0:
                                    pass
                                else:
                                    ic[9][0] = index[18]
                                    ic[9][1] = index[19]                         

                            # ahora vamos a restar las cantidades de los insumos usados 
                            for i in ic:   
                                if  i[0] == 0:
                                    pass
                                else:
                                    proceder = False
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "condesa",
                                        password = "123456",
                                        database = "condesa"
                                        )
                                    cursor = conn.cursor()
            
                                    sql = f""" SELECT `Cantidad` FROM `insumos` WHERE `Codigo` = {i[0]} """
                                    cursor.execute(sql)
                                    for index in cursor:
                                        if float(index[0]) >= float(temp.texto_cantidad.get())*float(i[1]):
                                            proceder = True
                                        else:
                                            error = messagebox.showerror("Error","No alcansan los insumos para regalar el producto")

                                    if proceder:
                                        # restamos los insumos regalados
                                        conn = mysql.connector.connect(
                                            host = "localhost",
                                            user = "condesa",
                                            password = "123456",
                                            database = "condesa"
                                            )
                                        cursor = conn.cursor()
                
                                        sql = f""" UPDATE `insumos` SET `Cantidad`= `Cantidad` - '{float(temp.texto_cantidad.get())*float(i[1])}' WHERE `Codigo` = {i[0]} """
                                        cursor.execute(sql)
                                        conn.commit()

                            # encontremos el id del regalo 
                            id_regalo = 1
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()
    
                            sql = """SELECT MAX(Id) FROM `regalos`;"""
                            cursor.execute(sql)
                            for index in cursor:
                                if index[0] == None:
                                    pass
    
                                else:
                                    id_regalo = index[0] + 1 

                            # agreguemos el regalo en la bd 
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()

                            sql = f""" INSERT INTO `regalos`(`Id`, `Fecha`, `Codigo`, `Nombre`, `Costo`, `Precio`, `Cantidad`, `Concepto`) VALUES ('{id_regalo}','{fecha_actual}','{codigo}','{values[0]}','{values[1]}','{values[2]}','{temp.texto_cantidad.get()}','{temp.texto_concepto_del_regalo.get()}') """
                            cursor.execute(sql)
                            conn.commit()

                            llenar_ventas(True)
                            temp.destroy()

                        except:
                            error = messagebox.showerror("Error","No se completo el regalo \n Revise los datos introducidos")
                        

            temp.btn_vender = CTkButton(temp,text="Aceptar",command=salida)
            temp.btn_vender.pack(pady=20,side="bottom")

        self.tabla.bind("<Double-1>", venta)



# **********************************************************************************
# *****************************  Control Regalos ***********************************
# **********************************************************************************

class ControlRegalos(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Devolucion Regalos")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo4.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)          

        ###################################################

        estilos_tablas()  
        
        self.tabla = ttk.Treeview(self, columns = ("Fecha","Codigo", "Nombre", "Costo", "Precio", "Cantidad", "Concepto"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")
        self.tabla.column("Codigo", width = 75, anchor="center")
        self.tabla.column("Nombre", width = 200, anchor="center")
        self.tabla.column("Costo", width = 100, anchor="center")
        self.tabla.column("Precio", width = 100, anchor="center")
        self.tabla.column("Cantidad", width = 75, anchor="center")
        self.tabla.column("Concepto", width = 200, anchor="center")

        self.tabla.place(x = 50, y = 200)        
        self.tabla.config(height = 11)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Codigo", text = "Codigo", anchor="center")
        self.tabla.heading("Nombre", text = "Nombre", anchor="center")
        self.tabla.heading("Costo", text = "Costo", anchor="center")
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
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()

                if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                    sql = f""" SELECT * FROM regalos WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%' ORDER BY `Fecha` DESC """

                else:
                    sql = f""" SELECT * FROM regalos WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%' and `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" ORDER BY `Fecha` DESC """

                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],index[6],index[7],))  
            except:
                error = messagebox.showerror("Error","No se pudo actualizar la tabla")

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
                llenar_tabla(True)
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
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_fecha_final = CTkButton(self,text="...",command=fecha_final, width = 27, height = 27)
        self.btn_fecha_final.place(x=200 ,y=130 )

        self.label_buscador = CTkLabel(self,text="---------- Buscador ----------")
        self.label_buscador.place(x=300,y=50)

        self.texto_buscador_codigo = CTkEntry(self,placeholder_text="Buscar por codigo ...")
        self.texto_buscador_codigo.place(x=300,y=90)          

        self.texto_buscador_codigo.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por nombre ...")
        self.texto_buscador_nombre.place(x=300,y=130) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla )  

        llenar_tabla(True)

        # ahora la posibilidad de eliminar el pago con doble click
        def eliminar_regalo(event): 
            global id_regalo
            global values
            # vamos a capturar el id del regalo que vamos a eliminar
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                id_regalo = self.tabla.item(item, "text")  
                values = self.tabla.item(item, "values")            

            conf = messagebox.askokcancel("Confirmar","Se va a cancelar este regalo") 
            if conf: 
                try:
                    # primero debemos devolver el regalo al almacen
                    # vamos a encontrar los insumos y las cantidades 
                    ic = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()               

                    sql = f""" SELECT `Insumo1`, `Cantidad1`, `Insumo2`, `Cantidad2`, `Insumo3`, `Cantidad3`, `Insumo4`, `Cantidad4`, `Insumo5`, `Cantidad5`, `Insumo6`, `Cantidad6`, `Insumo7`, `Cantidad7`, `Insumo8`, `Cantidad8`, `Insumo9`, `Cantidad9`, `Insumo10`, `Cantidad10` FROM `productos` WHERE `Codigo` = {values[1]} """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == 0:
                            pass
                        else:
                            ic[0][0] = index[0]
                            ic[0][1] = index[1]

                        if index[2] == 0:
                            pass
                        else:
                            ic[1][0] = index[2]
                            ic[1][1] = index[3]

                        if index[4] == 0:
                            pass
                        else:
                            ic[2][0] = index[4]
                            ic[2][1] = index[5]

                        if index[6] == 0:
                            pass
                        else:
                            ic[3][0] = index[6]
                            ic[3][1] = index[7]

                        if index[8] == 0:
                            pass
                        else:
                            ic[4][0] = index[8]
                            ic[4][1] = index[9]

                        if index[10] == 0:
                            pass
                        else:
                            ic[5][0] = index[10]
                            ic[5][1] = index[11]

                        if index[12] == 0:
                            pass
                        else:
                            ic[6][0] = index[12]
                            ic[6][1] = index[13]

                        if index[14] == 0:
                            pass
                        else:
                            ic[7][0] = index[14]
                            ic[7][1] = index[15]

                        if index[16] == 0:
                            pass
                        else:
                            ic[8][0] = index[16]
                            ic[8][1] = index[17]

                        if index[18] == 0:
                            pass
                        else:
                            ic[9][0] = index[18]
                            ic[9][1] = index[19]                

                    # ahora vamos a sumar las cantidades de los insumos devueltos 
                    for i in ic:   
                        if  i[0] == 0:
                            pass
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()

                            sql = f""" UPDATE `insumos` SET `Cantidad`= `Cantidad` + '{float(values[5])*float(i[1])}' WHERE `Codigo` = {i[0]} """
                            cursor.execute(sql)
                            conn.commit()

                    # ahora vamos a borrar en la tabla regalo
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `regalos` WHERE `Id` = {id_regalo} """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla(True)

                except:
                    error = messagebox.showerror("Error","Hubo problemas al eliminar el regalo") 

        self.tabla.bind("<Double-1>", eliminar_regalo)



# **********************************************************************************
# ******************************  Control Ventas ***********************************
# **********************************************************************************

class ControlVentas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Devolucion Ventas")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo4.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)          

        ###################################################

        estilos_tablas()  

        self.tabla = ttk.Treeview(self, columns = ("Fecha","Codigo", "Nombre", "Costo", "Precio", "Cantidad", "Categoria"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")
        self.tabla.column("Codigo", width = 75, anchor="center")
        self.tabla.column("Nombre", width = 200, anchor="center")
        self.tabla.column("Costo", width = 100, anchor="center")        
        self.tabla.column("Precio", width = 75, anchor="center")        
        self.tabla.column("Cantidad", width = 75, anchor="center")
        self.tabla.column("Categoria", width = 200, anchor="center")

        self.tabla.place(x = 100, y = 200)        
        self.tabla.config(height = 11)

        self.tabla.heading("#0", text = "Id", anchor="center")
        self.tabla.heading("Fecha", text = "Fecha", anchor="center")
        self.tabla.heading("Codigo", text = "Codigo", anchor="center")
        self.tabla.heading("Nombre", text = "Nombre", anchor="center")
        self.tabla.heading("Costo", text = "Costo", anchor="center")        
        self.tabla.heading("Precio", text = "Precio", anchor="center")        
        self.tabla.heading("Cantidad", text = "Cantidad", anchor="center")
        self.tabla.heading("Categoria", text = "Categoria", anchor="center")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        def llenar_tabla(event):
            try:
                self.tabla.delete(*self.tabla.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()

                if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                    sql = f""" SELECT * FROM salidas WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%' ORDER BY `Fecha` DESC """

                else:
                    sql = f""" SELECT * FROM salidas WHERE `Codigo` LIKE '%{self.texto_buscador_codigo.get()}%' and `Nombre` LIKE '%{self.texto_buscador_nombre.get()}%' and `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" ORDER BY `Fecha` DESC """

                cursor.execute(sql)
                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5],index[6],index[7],))  

            except:
                error = messagebox.showerror("Error","No se pudo actualizar la tabla")


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


        self.label_buscador = CTkLabel(self,text="---------- Buscador ----------")
        self.label_buscador.place(x=600,y=50)

        self.texto_buscador_codigo = CTkEntry(self,placeholder_text="Buscar por codigo ...")
        self.texto_buscador_codigo.place(x=600,y=90)          

        self.texto_buscador_codigo.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_nombre = CTkEntry(self,placeholder_text="Buscar por nombre ...")
        self.texto_buscador_nombre.place(x=600,y=130) 

        self.texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla )

        llenar_tabla(True)

        def eliminar_venta(event): 
            global id_venta
            global values

            # vamos a capturar el id del regalo que vamos a eliminar
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                id_venta = self.tabla.item(item, "text")  
                values = self.tabla.item(item, "values")

            conf = messagebox.askokcancel("Confirmar","Se va a cancelar esta venta") 
            if conf:
                try:
                    # primero debemos los insumos de la venta al almacen
                    # vamos a encontrar los insumos y las cantidades 
                    ic = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()               

                    sql = f""" SELECT `Insumo1`, `Cantidad1`, `Insumo2`, `Cantidad2`, `Insumo3`, `Cantidad3`, `Insumo4`, `Cantidad4`, `Insumo5`, `Cantidad5`, `Insumo6`, `Cantidad6`, `Insumo7`, `Cantidad7`, `Insumo8`, `Cantidad8`, `Insumo9`, `Cantidad9`, `Insumo10`, `Cantidad10` FROM `productos` WHERE `Codigo` = {values[1]} """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == 0:
                            pass
                        else:
                            ic[0][0] = index[0]
                            ic[0][1] = index[1]

                        if index[2] == 0:
                            pass
                        else:
                            ic[1][0] = index[2]
                            ic[1][1] = index[3]

                        if index[4] == 0:
                            pass
                        else:
                            ic[2][0] = index[4]
                            ic[2][1] = index[5]

                        if index[6] == 0:
                            pass
                        else:
                            ic[3][0] = index[6]
                            ic[3][1] = index[7]

                        if index[8] == 0:
                            pass
                        else:
                            ic[4][0] = index[8]
                            ic[4][1] = index[9]

                        if index[10] == 0:
                            pass
                        else:
                            ic[5][0] = index[10]
                            ic[5][1] = index[11]

                        if index[12] == 0:
                            pass
                        else:
                            ic[6][0] = index[12]
                            ic[6][1] = index[13]

                        if index[14] == 0:
                            pass
                        else:
                            ic[7][0] = index[14]
                            ic[7][1] = index[15]

                        if index[16] == 0:
                            pass
                        else:
                            ic[8][0] = index[16]
                            ic[8][1] = index[17]

                        if index[18] == 0:
                            pass
                        else:
                            ic[9][0] = index[18]
                            ic[9][1] = index[19]                

                    # ahora vamos a sumar las cantidades de los insumos devueltos 
                    for i in ic:   
                        if  i[0] == 0:
                            pass
                        else:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "condesa",
                                password = "123456",
                                database = "condesa"
                                )
                            cursor = conn.cursor()

                            sql = f""" UPDATE `insumos` SET `Cantidad`= `Cantidad` + '{float(values[5])*float(i[1])}' WHERE `Codigo` = {i[0]} """
                            cursor.execute(sql)
                            conn.commit()

                    # ahora vamos a eliminar la venta de su tabla 
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `salidas` WHERE `Id` = {id_venta} """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla(True)

                except:
                    error = messagebox.showerror("Error","Hubo problemas al eliminar la venta")         

        self.tabla.bind("<Double-1>", eliminar_venta)





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
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo3.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)          

        ###################################################

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ("Fecha","Concepto", "Monto"), show="headings")
        self.tabla.column("#0", width = 100, anchor="center")
        self.tabla.column("Fecha", width = 100, anchor="center")
        self.tabla.column("Concepto", width = 500, anchor="center")
        self.tabla.column("Monto", width = 100, anchor="center")        

        self.tabla.place(x = 150, y = 60)        
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
                user = "condesa",
                password = "123456",
                database = "condesa"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM `asociados` ORDER BY `Fecha` DESC  LIMIT 50"""
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3],))

        llenar_tabla() 

        def eliminar(event):
            global id_asociado
            # vamos a capturar el codigo del numero que vamos a reabastecer
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                id_asociado = self.tabla.item(item, "text")  

            conf  = messagebox.askokcancel("Confirmar","Se va a eliminar el gasto asociado")
            if conf:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()

                sql = f""" DELETE FROM `asociados` WHERE `Id` = {id_asociado} """
                cursor.execute(sql)
                conn.commit()

                llenar_tabla()


        self.tabla.bind("<Double-1>", eliminar)

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
            temp.after(250, lambda: temp.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico')) 

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
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
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
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
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
        self.after(250, lambda: self.iconbitmap('D:/condesa/imagenes funcionamiento/condesa_icono.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))   

        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/condesa/imagenes funcionamiento/fondo.jpg"), size = (1000,600))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 0, y = 0)          

        ###################################################  

        self.label_informaciones = CTkLabel(self, text="---------- Informaciones ----------")
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

        self.label_costos = CTkLabel(self, text="Total Costos: ")
        self.label_costos.place(x=500,y=180)

        string_costos = StringVar()
        string_costos.set("0")

        self.label_costos2 = CTkLabel(self, textvariable=string_costos)
        self.label_costos2.place(x=700,y=180)

        self.label_ganancia = CTkLabel(self, text="Total Ganancias: ")
        self.label_ganancia.place(x=500,y=220)

        string_ganancia = StringVar()
        string_ganancia.set("0")

        self.label_ganancia2 = CTkLabel(self, textvariable=string_ganancia)
        self.label_ganancia2.place(x=700,y=220)

        self.label_mas_vende = CTkLabel(self, text="Producto Mas Vendido: ")
        self.label_mas_vende.place(x=500,y=260)

        string_mas_vende = StringVar()
        string_mas_vende.set("0")

        self.label_mas_vende2 = CTkLabel(self, textvariable=string_mas_vende)
        self.label_mas_vende2.place(x=700,y=260)

        self.label_menos_vende = CTkLabel(self, text="Producto Menos Vendido: ")
        self.label_menos_vende.place(x=500,y=300)

        string_menos_vende = StringVar()
        string_menos_vende.set("0")

        self.label_menos_vende2 = CTkLabel(self, textvariable=string_menos_vende)
        self.label_menos_vende2.place(x=700,y=300)

        self.label_mas_ganancia = CTkLabel(self, text="Producto Mas Ganancia: ")
        self.label_mas_ganancia.place(x=500,y=340)

        string_mas_ganancia = StringVar()
        string_mas_ganancia.set("0")

        self.label_mas_ganancia2 = CTkLabel(self, textvariable=string_mas_ganancia)
        self.label_mas_ganancia2.place(x=700,y=340)

        self.label_menos_ganancia = CTkLabel(self, text="Producto Menos Ganancia: ")
        self.label_menos_ganancia.place(x=500,y=380)

        string_menos_ganancia = StringVar()
        string_menos_ganancia.set("0")

        self.label_menos_ganancia2 = CTkLabel(self, textvariable=string_menos_ganancia)
        self.label_menos_ganancia2.place(x=700,y=380)

        # ahora vamos a generar la funcion para mostrar los datos 
        def consulta():
            if self.texto_fecha_final.get() == "" or self.texto_fecha_inicial.get() == "":
                pass
            else:
                #################################################
                # primero vamos a hallar el total de ingresos
                ingresos = 0
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()                                       
                sql = f""" SELECT  `Precio`, `Cantidad` FROM `salidas` WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                cursor.execute(sql)
                for index in cursor:
                    ingresos += index[0]*index[1]
                

                string_ingresos.set(round(ingresos,2))

                ####################################################
                
                # ahora veremos total de gastos asociados 
                asociados = 0
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()                    
                sql = f""" SELECT `Monto` FROM `asociados` WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                cursor.execute(sql)
                for index in cursor:
                    asociados += index[0]

                string_gastos.set(round(asociados,2))

                ####################################################
                
                # ahora veamos el total de costos 
                costos = 0
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()                    
                sql = f""" SELECT  `Costo`, `Cantidad` FROM `salidas` WHERE `Fecha` >= "{self.texto_fecha_inicial.get()}" and `Fecha` < "{self.texto_fecha_final.get()}" """
                cursor.execute(sql)
                for index in cursor:
                    costos += index[0]*index[1]

                string_costos.set(round(costos, 2))

                ########################################################
                
                # ahora veamos las ganancias 
                ganancias = ingresos - asociados - costos
                string_ganancia.set(round(ganancias, 2))

                ########################################################
                
                # ahora el producto mas vendido 
                nombre = ""
                cantidad = 0
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()                    
                sql = f""" SELECT Codigo, Nombre, SUM(Cantidad) AS total_unidades_vendidas FROM salidas WHERE Fecha BETWEEN "{self.texto_fecha_inicial.get()}" AND "{self.texto_fecha_final.get()}" GROUP BY Codigo, Nombre ORDER BY total_unidades_vendidas DESC LIMIT 1; """
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
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()                    
                sql = f""" SELECT Codigo, Nombre, SUM(Cantidad) AS total_unidades_vendidas FROM salidas WHERE Fecha BETWEEN "{self.texto_fecha_inicial.get()}" AND "{self.texto_fecha_final.get()}" GROUP BY Codigo, Nombre ORDER BY total_unidades_vendidas ASC LIMIT 1; """
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
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()                    
                sql = f""" SELECT Codigo, Nombre, SUM((Precio - Costo) * Cantidad) AS ganancia_total FROM salidas WHERE Fecha BETWEEN "{self.texto_fecha_inicial.get()}" AND "{self.texto_fecha_final.get()}" GROUP BY Codigo, Nombre ORDER BY ganancia_total DESC LIMIT 1; """
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
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()                    
                sql = f""" SELECT Codigo, Nombre, SUM((Precio - Costo) * Cantidad) AS ganancia_total FROM salidas WHERE Fecha BETWEEN "{self.texto_fecha_inicial.get()}" AND "{self.texto_fecha_final.get()}" GROUP BY Codigo, Nombre ORDER BY ganancia_total ASC LIMIT 1; """
                cursor.execute(sql)
                for index in cursor:
                    nombre = index[1]
                    ganancia = index[2]

                string = f" ({round(ganancia, 2)})"
                string_menos_ganancia.set(nombre + string)

                ############################################################


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

        def trayectoria_insumos():
            # ********** validar que las fechas esten puestas **********
            if self.texto_fecha_inicial.get() == "" or self.texto_fecha_final.get() == "":
                error = messagebox.showerror("Error","Debes seleccionar la fecha inicial y la fecha final")
                return

            fecha_inicial = self.texto_fecha_inicial.get()
            fecha_final = self.texto_fecha_final.get()

            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "condesa",
                    password = "123456",
                    database = "condesa"
                    )
                cursor = conn.cursor()

                # ********** traemos todos los insumos **********
                sql = """ SELECT `Codigo`, `Nombre`, `Costo`, `Cantidad`, `U/M` FROM `insumos` ORDER BY `Codigo`; """
                cursor.execute(sql)

                insumos = []
                for index in cursor:
                    insumos.append({
                        "codigo": index[0],
                        "nombre": index[1],
                        "costo": index[2],
                        "cant_final_real": index[3],
                        "um": index[4]
                    })

                # ********** por cada insumo calculamos entradas y salidas del periodo **********
                for insumo in insumos:
                    cod = insumo["codigo"]

                    # ----- cant que entro en el periodo (tabla entradas) -----
                    cant_entro = 0
                    conn2 = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor2 = conn2.cursor()

                    sql = f""" SELECT `Cantidad` FROM `entradas` WHERE `Codigo` = {cod} AND `Fecha` >= "{fecha_inicial}" AND `Fecha` < "{fecha_final}" """
                    cursor2.execute(sql)
                    for index in cursor2:
                        cant_entro += index[0]

                    # ----- cant que salio en el periodo (por ventas) -----
                    # las salidas se guardan con el codigo del PRODUCTO, no del insumo
                    # entonces hay que revisar cada producto vendido y ver si usa este insumo
                    cant_salio = 0

                    conn3 = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor3 = conn3.cursor()

                    sql = f""" SELECT `Codigo`, `Cantidad` FROM `salidas` WHERE `Fecha` >= "{fecha_inicial}" AND `Fecha` < "{fecha_final}" """
                    cursor3.execute(sql)

                    salidas_periodo = []
                    for index in cursor3:
                        salidas_periodo.append((index[0], index[1]))

                    for salida in salidas_periodo:
                        cod_prod = salida[0]
                        cant_vendida = salida[1]

                        # buscamos en el producto si usa este insumo y cuanto
                        conn4 = mysql.connector.connect(
                            host = "localhost",
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
                            )
                        cursor4 = conn4.cursor()

                        sql = f""" SELECT `Insumo1`, `Cantidad1`, `Insumo2`, `Cantidad2`, `Insumo3`, `Cantidad3`, `Insumo4`, `Cantidad4`, `Insumo5`, `Cantidad5`, `Insumo6`, `Cantidad6`, `Insumo7`, `Cantidad7`, `Insumo8`, `Cantidad8`, `Insumo9`, `Cantidad9`, `Insumo10`, `Cantidad10` FROM `productos` WHERE `Codigo` = {cod_prod} """
                        cursor4.execute(sql)

                        for row in cursor4:
                            pares = [
                                (row[0], row[1]), (row[2], row[3]),
                                (row[4], row[5]), (row[6], row[7]),
                                (row[8], row[9]), (row[10], row[11]),
                                (row[12], row[13]), (row[14], row[15]),
                                (row[16], row[17]), (row[18], row[19])
                            ]
                            for ins, cant in pares:
                                if ins == cod and cant != 0:
                                    cant_salio += cant_vendida * cant

                        conn4.close()

                    # ----- cant que salio por regalos -----
                    conn5 = mysql.connector.connect(
                        host = "localhost",
                        user = "condesa",
                        password = "123456",
                        database = "condesa"
                        )
                    cursor5 = conn5.cursor()

                    sql = f""" SELECT `Codigo`, `Cantidad` FROM `regalos` WHERE `Fecha` >= "{fecha_inicial}" AND `Fecha` < "{fecha_final}" """
                    cursor5.execute(sql)

                    regalos_periodo = []
                    for index in cursor5:
                        regalos_periodo.append((index[0], index[1]))

                    for regalo in regalos_periodo:
                        cod_prod = regalo[0]
                        cant_regalada = regalo[1]

                        conn6 = mysql.connector.connect(
                            host = "localhost",
                            user = "condesa",
                            password = "123456",
                            database = "condesa"
                            )
                        cursor6 = conn6.cursor()

                        sql = f""" SELECT `Insumo1`, `Cantidad1`, `Insumo2`, `Cantidad2`, `Insumo3`, `Cantidad3`, `Insumo4`, `Cantidad4`, `Insumo5`, `Cantidad5`, `Insumo6`, `Cantidad6`, `Insumo7`, `Cantidad7`, `Insumo8`, `Cantidad8`, `Insumo9`, `Cantidad9`, `Insumo10`, `Cantidad10` FROM `productos` WHERE `Codigo` = {cod_prod} """
                        cursor6.execute(sql)

                        for row in cursor6:
                            pares = [
                                (row[0], row[1]), (row[2], row[3]),
                                (row[4], row[5]), (row[6], row[7]),
                                (row[8], row[9]), (row[10], row[11]),
                                (row[12], row[13]), (row[14], row[15]),
                                (row[16], row[17]), (row[18], row[19])
                            ]
                            for ins, cant in pares:
                                if ins == cod and cant != 0:
                                    cant_salio += cant_regalada * cant

                        conn6.close()

                    # ----- cant inicial del periodo -----
                    # cant final real - entro + salio  = cant inicial
                    cant_inicial = insumo["cant_final_real"] - cant_entro + cant_salio

                    insumo["cant_inicial"] = cant_inicial
                    insumo["cant_entro"] = cant_entro
                    insumo["cant_salio"] = cant_salio
                    insumo["cant_final"] = insumo["cant_final_real"]

                    conn2.close()
                    conn3.close()
                    conn5.close()

                conn.close()

                # ********** ordenamos: primero los que tienen movimiento, al final los que estan en cero **********
                insumos.sort(key=lambda x: (x["cant_entro"] == 0 and x["cant_salio"] == 0))

                # ********** armamos el DataFrame y exportamos a Excel **********
                datos = []
                for insumo in insumos:
                    datos.append({
                        "Codigo": insumo["codigo"],
                        "Nombre": insumo["nombre"],
                        "Costo": insumo["costo"],
                        "U/M": insumo["um"],
                        "Cant Inicial": insumo["cant_inicial"],
                        "Cant Entro": insumo["cant_entro"],
                        "Cant Salió": insumo["cant_salio"],
                        "Cant Final": insumo["cant_final"]
                    })

                df = pd.DataFrame(datos)

                # ********** carpeta y nombre del archivo **********
                carpeta_respaldo = "D:/condesa/respaldos"
                if not os.path.exists(carpeta_respaldo):
                    os.makedirs(carpeta_respaldo)

                nombre_archivo = f"TI {fecha_inicial}-{fecha_final}.xlsx"
                ruta_completa = os.path.join(carpeta_respaldo, nombre_archivo)

                df.to_excel(ruta_completa, index=False)

                messagebox.showinfo("Éxito", f"Archivo creado exitosamente:\n{ruta_completa}")

            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema al generar la trayectoria:\n{str(e)}")

        self.btn_trayectoria = CTkButton(self,text="Trayectoria Insumos",command=trayectoria_insumos)
        self.btn_trayectoria.place(x=50 ,y=200 )





conn.close()
autenticacion = Autenticacion()
autenticacion.mainloop()