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
from ttkwidgets.autocomplete import AutocompleteEntry,AutocompleteCombobox, AutocompleteEntryListbox

fecha_actual = datetime.now().date()
num_directivo = 0

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""    
    )
cursor = conn.cursor()
sql = ""

# ***************************************************************************************
# **************** Creando Usuario, Base de Datos y Tablas de Admin necesarias **********
# ***************************************************************************************

# ********************** creando usuario admin ******************************

try:
    sql = """CREATE USER 'mychurch'@'localhost' IDENTIFIED BY '123456';"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

sql = """GRANT ALL PRIVILEGES ON *.* TO 'mychurch'@'localhost' REQUIRE NONE WITH GRANT OPTION MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0; """
cursor.execute(sql)
conn.commit()

conn.close()

conn = mysql.connector.connect(
    host = "localhost",
    user = "mychurch",
    password = "123456",
    )
cursor = conn.cursor()

# ******* creando la base de datos mychurch ***********
try:
    sql = """CREATE DATABASE mychurch CHARACTER SET = utf8mb4 COLLATE utf8mb4_spanish_ci;"""
    cursor.execute(sql)
    conn.commit()    
except:
    pass

conn = mysql.connector.connect(
    host = "localhost",
    user = "mychurch",
    password = "123456",
    database = "mychurch"
    )
cursor = conn.cursor()

# *********** creando tabla usuarios **********
try:
    sql = """CREATE TABLE  usuarios (Usuario VARCHAR(50), Password VARCHAR(50))"""
    cursor.execute(sql)
    conn.commit()    
except:
    pass

# ***************** usuario admin ysos ********************
usuario_ysos_is_created = False
usuario_inicial = []
conn = mysql.connector.connect(
    host = "localhost",
    user = "mychurch",
    password = "123456",
    database = "mychurch"
    )
cursor = conn.cursor()
sql = """ SELECT Usuario FROM usuarios """
cursor.execute(sql)

for usser in cursor:
    usuario_inicial.append(usser)

for index in range(len(usuario_inicial)):
    if usuario_inicial[index][0] == "ysos":
        usuario_ysos_is_created = True

if usuario_ysos_is_created == False:
    try:
        sql = """INSERT INTO usuarios (Usuario,Password) VALUES ("ysos","123456")"""
        cursor.execute(sql)
        conn.commit()       
    except:
        pass

# ************** creando tabla licencias ***************

conn = mysql.connector.connect(
    host = "localhost",
    user = "mychurch",
    password = "123456",
    database = "mychurch"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `mychurch`.`licencias` (`codigo_lic` VARCHAR(50) NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

# ******************** Creando Tabla Personas *******************
try:
    sql = """ CREATE TABLE `mychurch`.`personas` (`Id` INT NOT NULL , `Nombre` VARCHAR(50) NOT NULL ,
     `Apellido 1` VARCHAR(50) NOT NULL , `Apellido 2` VARCHAR(50) NOT NULL , `Edad` INT NOT NULL , 
     `Direccion` VARCHAR(200) NOT NULL , `Telefono` INT NOT NULL , `Bautizado` VARCHAR(10) NOT NULL , 
     `Miembro` VARCHAR(10) NOT NULL , `Organizacion` VARCHAR(50) NOT NULL, `fecha_diezmo_vencido` DATE NOT NULL, 
     `fecha_conversion` DATE NOT NULL, `fecha_bautismo` DATE NOT NULL , `Oficio` VARCHAR(50) NOT NULL  ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

# **************** creando tabla inventario ****************
try:
    sql = """ CREATE TABLE `mychurch`.`inventario` (`Id` INT NOT NULL , `Nombre` VARCHAR(50) NOT NULL , `Cantidad` INT NOT NULL , `Inmueble` VARCHAR(50) NOT NULL , `Area` VARCHAR(50) NOT NULL , `Detalles` VARCHAR(100) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla areas **********************
try:
    sql = """ CREATE TABLE `mychurch`.`inmuebles` (`nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla organizaciones **********************
try:
    sql = """ CREATE TABLE `mychurch`.`organizaciones` (`nombre` VARCHAR(50) NOT NULL , `edad_inicial` INT NOT NULL , `edad_final` INT NOT NULL, `sexo` VARCHAR(10) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla concepto salidas **********************
try:
    sql = """ CREATE TABLE `mychurch`.`concepto_salidas` (`nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla concepto entradas **********************
try:
    sql = """ CREATE TABLE `mychurch`.`concepto_entradas` (`nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla monedas **********************
try:
    sql = """ CREATE TABLE `mychurch`.`monedas` (`nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass


#  ********************* creando tabla entradas **********************
try:
    sql = """ CREATE TABLE `mychurch`.`entradas` (`Id` INT NOT NULL , `fecha` DATE NOT NULL , `descripcion` VARCHAR(50) NOT NULL , `servicio` VARCHAR(50) NOT NULL , `monto` DOUBLE NOT NULL , `moneda` VARCHAR(20) NOT NULL ) ENGINE = InnoDB"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla salidas **********************
try:
    sql = """ CREATE TABLE `mychurch`.`salidas` (`Id` INT NOT NULL , `fecha` DATE NOT NULL , `descripcion` VARCHAR(50) NOT NULL , `concepto` VARCHAR(50) NOT NULL , `monto` DOUBLE NOT NULL , `moneda` VARCHAR(20) NOT NULL ) ENGINE = InnoDB"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla DIEZMOS **********************
try:
    sql = """ CREATE TABLE `mychurch`.`diezmo` (`id` INT NOT NULL , `fecha` DATE NOT NULL , `sobre` INT NOT NULL , `nombre` VARCHAR(50) NOT NULL , `apellido 1` VARCHAR(50) NOT NULL , `apellido 2` VARCHAR(50) NOT NULL , `fecha_vencido` DATE NOT NULL , `monto` DOUBLE NOT NULL , `moneda` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass


#  ********************* creando tabla Directivos **********************
try:
    sql = """ CREATE TABLE `mychurch`.`directivos` (`Id` INT NOT NULL ,`area` VARCHAR(50) NOT NULL , `cargo` VARCHAR(50) NOT NULL , `nombre` VARCHAR(100) NOT NULL , `apellido1` VARCHAR(50) NOT NULL , `apellido2` VARCHAR(50) NOT NULL , `edad` INT NOT NULL , `telefono` VARCHAR(50) NOT NULL , `direccion` VARCHAR(200) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla Areas de Trabajo **********************
try:
    sql = """ CREATE TABLE `mychurch`.`areas_trabajo` (`nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla Alabanza ******************************
try:
    sql = """ CREATE TABLE `mychurch`.`alabanza` (`Id` INT NOT NULL , `integrante` VARCHAR(100) NOT NULL , `puesto` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla Danza ******************************
try:
    sql = """ CREATE TABLE `mychurch`.`danza` (`Id` INT NOT NULL , `integrante` VARCHAR(100) NOT NULL , `puesto` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla Teatro ******************************
try:
    sql = """ CREATE TABLE `mychurch`.`teatro` (`Id` INT NOT NULL , `integrante` VARCHAR(100) NOT NULL , `puesto` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

#  ********************* creando tabla Audio ******************************
try:
    sql = """ CREATE TABLE `mychurch`.`audio` (`Id` INT NOT NULL , `integrante` VARCHAR(100) NOT NULL , `puesto` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass



#***********************************************************************************
#************************trabajo con ventana Autenticacion *************************
#***********************************************************************************

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
        self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico') #cambiar 


        ############ agregar el fondo de pantalla #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (400,200))  

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
            user = "mychurch",
            password = "123456",
            database = "mychurch"
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

# **********************************************************************************
# ********************************** nueva_licencia ********************************
# **********************************************************************************

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
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
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
                fecha_vencimiento = date(fecha[0],fecha[1],fecha[2])   
                                    
                
                if serial_cmd == serial_txt:

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
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


# **********************************************************************************
# ********************************* Trabajo con Lobby ******************************
# **********************************************************************************
class Lobby(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.geometry("1300x700")        
        self.title("MyChurch")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.resizable(False,False) 

        # **************************** fondo *****************************************************
        try:            
            self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (1300,700))                  
            
            label_imagen_lobby = CTkLabel(self, image = self.imagen, text = "")
            label_imagen_lobby.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error","No se encontro foto")
        
        firma = "Vence (" + str(fecha_vencimiento) + ")"
        self.label_ = CTkLabel(self, text = firma, font=("Times New Roman",16))
        self.label_.place(x = 1150, y = 650)

        def agregar_hermanos():
            agregar_hermano = AgregarHermano()
               

        def consultas_hermanos():
            consultas_hermano = ConsultarHermanos()

        def admon():
            adm = ADMON()         

        def tesoreria_lobby():
            tes = Tesoreria()                

        def inmuebles_lobby():
            inmuebles = Inmuebles()  

        def areas_trabajo_lobby():
            areas = AreasTrabajo()      

        def organizaciones():
            organizacion = Organizacion()  

        def conceptos_salidas_lobby():
            concepto_salida = ConceptosSalidas()

        def conceptos_entradas_lobby():
            conceptos_entradas = ConceptosEntradas()   

        def monedas_lobby():
            monedas = Monedas()         

        def finanzas_lobby():
            fin = Finanzas() 
        
        def agregar_nueva_licencia():                         
            nueva_licencia = NuevaLicencia()
        
        def agregar_usuario():
            usuario_agregar = UsuarioAgregar()
            
        def eliminar_usuario():                        
            eliminar_usuario = EliminarUsuario()  

        def directiva_pastor_lobby(): 
            global num_directivo          
            num_directivo = 1
            direct = Directiva()

        def directiva_presidente_lobby():
            global num_directivo          
            num_directivo = 2
            direct = Directiva()

        def directiva_vice_lobby():
            global num_directivo          
            num_directivo = 3
            direct = Directiva()

        def directiva_secretario_lobby():
            global num_directivo          
            num_directivo = 4
            direct = Directiva()

        def directiva_financista_lobby():
            global num_directivo          
            num_directivo = 5
            direct = Directiva()

        def directiva_estadistica_lobby():
            global num_directivo          
            num_directivo = 6
            direct = Directiva()

        def directiva_tesorero_lobby():
            global num_directivo          
            num_directivo = 7
            direct = Directiva()

        def control_areas_trabajo__lobby():
            areas_trabajo = ControlAreasTrabajo()

        def organizaciones__lobby():
            organizacion = Organizaciones()

        def cerrar_cesion():
            self.destroy()
            autenticacion.deiconify()            
            
        def cerrar_programa(): 
                self.quit()   


        self.menu = Menu(self)
        self.config(menu=self.menu, width="200", height="100")

        jtl_menu = Menu(self.menu, tearoff = 0)   
        jtl_menu.add_command(label="Pastor", command = directiva_pastor_lobby)
        jtl_menu.add_command(label="Presidente", command = directiva_presidente_lobby)
        jtl_menu.add_command(label="Vice Presidente", command = directiva_vice_lobby)
        jtl_menu.add_command(label="Sacretario", command = directiva_secretario_lobby)
        jtl_menu.add_command(label="Financista", command = directiva_financista_lobby)
        jtl_menu.add_command(label="Estadistica", command = directiva_estadistica_lobby)
        jtl_menu.add_command(label="Tesorero", command = directiva_tesorero_lobby)
        jtl_menu.add_command(label="Tesoreria", command = tesoreria_lobby)
        jtl_menu.add_command(label="Finanzas", command = finanzas_lobby)
        jtl_menu.add_command(label="Areas de Trabajo", command = control_areas_trabajo__lobby)
        jtl_menu.add_command(label="Organizaciones", command = organizaciones__lobby)
        jtl_menu.add_command(label="ADMON", command = admon)

        hermanos_menu = Menu(self.menu, tearoff = 0)   
        hermanos_menu.add_command(label="Agregar ", command = agregar_hermanos)
        hermanos_menu.add_command(label="Consultas ", command = consultas_hermanos)       

        organizativo_menu = Menu(self.menu, tearoff = 0)   
        organizativo_menu.add_command(label="Areas de Trabajo ", command = areas_trabajo_lobby)
        organizativo_menu.add_command(label="Inmuebles ", command = inmuebles_lobby)
        organizativo_menu.add_command(label="Organizaciones ", command = organizaciones) 
        organizativo_menu.add_command(label="Conceptos Salidas ", command = conceptos_salidas_lobby) 
        organizativo_menu.add_command(label="Conceptos Entradas ", command = conceptos_entradas_lobby)  
        organizativo_menu.add_command(label="Monedas ", command = monedas_lobby)       

        usuario_menu = Menu(self.menu, tearoff = 0)
        usuario_menu.add_command(label="Agregar", command = agregar_usuario)
        usuario_menu.add_command(label="Eliminar", command = eliminar_usuario)

        licencia_menu = Menu(self.menu, tearoff = 0)
        licencia_menu.add_command(label="Nueva", command = agregar_nueva_licencia)

        salir_menu = Menu(self.menu, tearoff = 0)
        salir_menu.add_command(label="Cerrar Cesion", command = cerrar_cesion)
        salir_menu.add_command(label="Cerrar Programa", command = cerrar_programa)    

        self.menu.add_cascade (label="JTL", menu = jtl_menu)
        self.menu.add_cascade (label="Hermanos", menu = hermanos_menu)         
        self.menu.add_cascade (label="Organizativo", menu = organizativo_menu)        
        self.menu.add_cascade (label="Usuario", menu = usuario_menu)
        self.menu.add_cascade (label="Licencia", menu = licencia_menu)
        self.menu.add_cascade (label="Salir", menu = salir_menu)


# **********************************************************************************
# ********************************* usuarios_agregar *******************************
# **********************************************************************************

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
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))  
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
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
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


# **********************************************************************************
# ******************************** usuarios_eliminar *******************************
# **********************************************************************************

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
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (400,300))                            
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_nombre = CTkLabel(self,text = "Usuario:", font=("Times New Roman",14))
        self.label_nombre.place(x = 100 , y = 100)
        
        items_usuarios = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Usuario` FROM `usuarios`;"""
        cursor.execute(sql)
        for index in cursor:
            items_usuarios.append(index[0])


        texto_nombre_usuario_eliminar = ttk.Combobox(self)
        texto_nombre_usuario_eliminar.place(x = 200 , y = 105)
        texto_nombre_usuario_eliminar['values'] = items_usuarios


        def codigo_btn_eliminar_usuarios_eliminar():
            try:
                if texto_nombre_usuario_eliminar.get() == "ysos":
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
                                    user = "mychurch",
                                    password = "123456",
                                    database = "mychurch"
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
        

# **********************************************************************************
# **************************** Inmuebles  ******************************************
# **********************************************************************************

class Inmuebles(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Inmuebles")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,600))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        global tabla_inmuebles
        tabla_inmuebles = ttk.Treeview(self)
        tabla_inmuebles.column("#0", width = 200)
        
        tabla_inmuebles.place(x = 100, y = 100)
        tabla_inmuebles.config(height = 10)
        tabla_inmuebles.heading("#0", text = "Inmuebles")
        
        scrollbar = CTkScrollbar(self, command = tabla_inmuebles.yview, width = 18)
        scrollbar.place(in_ = tabla_inmuebles, relheigh = 1, relx = 1)

        tabla_inmuebles.config(yscrollcommand = scrollbar.set)


        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `inmuebles`;"""
        cursor.execute(sql)

        for index in cursor:
            tabla_inmuebles.insert("",END, text = index[0])
            

        def agregar_inmuebles():
            agregar_inmueble = AgregarInmueble()
            

        def eliminar_inmuebles():
            eliminar_inmueble = EliminarInmueble()


        def cerrar_inmueble():
            self.destroy()

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar_inmuebles, width = 100, height = 30)
        self.btn_agregar.place(x = 150, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar_inmuebles, width = 100, height = 30)
        self.btn_eliminar.place(x = 550, y = 400)        

        self.btn_cerrar = CTkButton(self, text = "Cerrar", command = cerrar_inmueble, width = 200, height = 30)
        self.btn_cerrar.place(x = 300, y = 500)


# **********************************************************************************
# **************************** Areas de Trabajo  ***********************************
# **********************************************************************************

class AreasTrabajo(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Areas de Trabajo")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,600))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        global tabla_area
        tabla_area = ttk.Treeview(self)
        tabla_area.column("#0", width = 200)
        
        tabla_area.place(x = 100, y = 100)
        tabla_area.config(height = 10)
        tabla_area.heading("#0", text = "Area")
        
        scrollbar = CTkScrollbar(self, command = tabla_area.yview, width = 18)
        scrollbar.place(in_ = tabla_area, relheigh = 1, relx = 1)

        tabla_area.config(yscrollcommand = scrollbar.set)


        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `areas_trabajo`;"""
        cursor.execute(sql)

        for index in cursor:
            tabla_area.insert("",END, text = index[0])
            

        def agregar_areas():
            agregar_area = AgregarAreaTrabajo()
            

        def eliminar_areas():
            eliminar_area = EliminarAreaTrabajo()


        def cerrar_areas():
            self.destroy()

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar_areas, width = 100, height = 30)
        self.btn_agregar.place(x = 150, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar_areas, width = 100, height = 30)
        self.btn_eliminar.place(x = 550, y = 400)        

        self.btn_cerrar = CTkButton(self, text = "Cerrar", command = cerrar_areas, width = 200, height = 30)
        self.btn_cerrar.place(x = 300, y = 500)


# **********************************************************************************
# ************************* Agregar Area de Trabajo ********************************
# **********************************************************************************

class AgregarAreaTrabajo(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agegar Area de Trabajo")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))       

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                    
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_nueva = CTkLabel(self, text = "Nueva Area", font=("Times New Roman",16))
        self.label_nueva.place(x = 100, y = 70)                  

        self.text_nueva = CTkEntry(self)
        self.text_nueva.place(x = 100, y = 160)
        

        def confirmar_agregar_areas():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""INSERT INTO `areas_trabajo` (`nombre`) VALUES ('{self.text_nueva.get()}');"""
                cursor.execute(sql)
                conn.commit()

                tabla_area.insert("", END, text = f'{self.text_nueva.get()}')
                self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo agregar el area")


        def cancelar_agregar_areas():
            self.destroy()

        self.btn_confirmar_agregar = CTkButton(self, text = "Agregar", command = confirmar_agregar_areas, width = 200, height = 30)
        self.btn_confirmar_agregar.place(x = 100, y = 300)        

        self.btn_cancelar_agregar = CTkButton(self, text = "Cancelar", command = cancelar_agregar_areas, width = 200, height = 30)
        self.btn_cancelar_agregar.place(x = 400, y = 300)


# **********************************************************************************
# *************************** Eliminar Areas ***************************************
# **********************************************************************************

class EliminarAreaTrabajo(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Eliminar Area de Trabajo")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                       
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label = CTkLabel(self, text = "Eliminar Area", font=("Times New Roman",16))
        self.label.place(x = 250, y = 70)
        

        items_modalidad = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()
        sql = """SELECT `nombre` FROM `areas_trabajo`;"""
        cursor.execute(sql)

        for index in cursor:
            items_modalidad.append(index[0])            
        
        self.text = ttk.Combobox(self, width = 30)
        self.text.place(x = 250, y = 160)        
        self.text['values'] = items_modalidad    
        

        def eliminar_areas():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""DELETE FROM `areas_trabajo` WHERE nombre = '{self.text.get()}'"""
                cursor.execute(sql)
                conn.commit()
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar el area")

        # ****************** actualizar tabla modalidad ***************************
            tabla_area.delete(*tabla_area.get_children())  # esto borra toda la tabla 

            sql = """SELECT * FROM `areas_trabajo`;"""
            cursor.execute(sql)

            for index in cursor:
                tabla_area.insert("",END, text = index[0])

            self.destroy()

            
        def cancelar_eliminar_areas():
            self.destroy()

        self.btn_confirmar = CTkButton(self, text = "Eliminar", command = eliminar_areas, width = 200, height = 30)
        self.btn_confirmar.place(x = 100, y = 300)        

        self.btn_cancelar = CTkButton(self, text = "Cancelar", command = cancelar_eliminar_areas, width = 200, height = 30)
        self.btn_cancelar.place(x = 400, y = 300)


# **********************************************************************************
# ************************* Agregar Inmueble ***************************************
# **********************************************************************************

class AgregarInmueble(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agegar Inmueble")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))       

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                    
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_nueva = CTkLabel(self, text = "Nuevo Inmueble", font=("Times New Roman",16))
        self.label_nueva.place(x = 100, y = 70)                  

        self.text_nueva = CTkEntry(self)
        self.text_nueva.place(x = 100, y = 160)
        

        def confirmar_agregar_inmuebles():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""INSERT INTO `inmuebles` (`nombre`) VALUES ('{self.text_nueva.get()}');"""
                cursor.execute(sql)
                conn.commit()

                tabla_inmuebles.insert("", END, text = f'{self.text_nueva.get()}')
                self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo agregar la modalidad")


        def cancelar_agregar_inmuebles():
            self.destroy()

        self.btn_confirmar_agregar = CTkButton(self, text = "Agregar", command = confirmar_agregar_inmuebles, width = 200, height = 30)
        self.btn_confirmar_agregar.place(x = 100, y = 300)        

        self.btn_cancelar_agregar = CTkButton(self, text = "Cancelar", command = cancelar_agregar_inmuebles, width = 200, height = 30)
        self.btn_cancelar_agregar.place(x = 400, y = 300)


# **********************************************************************************
# *************************** Eliminar Inmueble ************************************
# **********************************************************************************

class EliminarInmueble(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Eliminar Inmueble")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                       
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label = CTkLabel(self, text = "Eliminar Area", font=("Times New Roman",16))
        self.label.place(x = 250, y = 70)
        

        items_modalidad = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()
        sql = """SELECT `nombre` FROM `inmuebles`;"""
        cursor.execute(sql)

        for index in cursor:
            items_modalidad.append(index[0])            
        
        self.text = ttk.Combobox(self, width = 30)
        self.text.place(x = 250, y = 160)        
        self.text['values'] = items_modalidad    
        

        def eliminar_areas():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""DELETE FROM `inmuebles` WHERE nombre = '{self.text.get()}'"""
                cursor.execute(sql)
                conn.commit()
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar el inmueble")

        # ****************** actualizar tabla modalidad ***************************
            tabla_inmuebles.delete(*tabla_inmuebles.get_children())  # esto borra toda la tabla 

            sql = """SELECT * FROM `inmuebles`;"""
            cursor.execute(sql)

            for index in cursor:
                tabla_inmuebles.insert("",END, text = index[0])

            self.destroy()

            
        def cancelar_eliminar_areas():
            self.destroy()

        self.btn_confirmar = CTkButton(self, text = "Eliminar", command = eliminar_areas, width = 200, height = 30)
        self.btn_confirmar.place(x = 100, y = 300)        

        self.btn_cancelar = CTkButton(self, text = "Cancelar", command = cancelar_eliminar_areas, width = 200, height = 30)
        self.btn_cancelar.place(x = 400, y = 300)

# **********************************************************************************
# **************************** Organizaciones  *************************************
# **********************************************************************************

class Organizacion(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Organizacion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,600))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        global tabla_organizacion
        tabla_organizacion = ttk.Treeview(self, columns = ("Edad Inicial","Edad Final","Sexo"))
        tabla_organizacion.column("#0", width = 200)
        tabla_organizacion.column("Edad Inicial", width = 100)
        tabla_organizacion.column("Edad Final", width = 100)
        tabla_organizacion.column("Sexo", width = 100)
        
        tabla_organizacion.place(x = 100, y = 100)
        tabla_organizacion.config(height = 10)
        tabla_organizacion.heading("#0", text = "Nombre")
        tabla_organizacion.heading("Edad Inicial", text = "Edad Inicial")
        tabla_organizacion.heading("Edad Final", text = "Edad Final")
        tabla_organizacion.heading("Sexo", text = "Sexo")
        
        scrollbar = CTkScrollbar(self, command = tabla_organizacion.yview, width = 18)
        scrollbar.place(in_ = tabla_organizacion, relheigh = 1, relx = 1)

        tabla_organizacion.config(yscrollcommand = scrollbar.set)


        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `organizaciones`;"""
        cursor.execute(sql)

        for index in cursor:
            tabla_organizacion.insert("",END, text = index[0], values = (index[1],index[2]))
            

        def agregar_organizaciones():
            agregar_organizacion = AgregarOrganizacion()
            

        def eliminar_organizaciones():
            eliminar_organizacion = EliminarOrganizacion()


        def cerrar_organizaciones():
            self.destroy()

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar_organizaciones, width = 100, height = 30)
        self.btn_agregar.place(x = 150, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar_organizaciones, width = 100, height = 30)
        self.btn_eliminar.place(x = 550, y = 400)        

        self.btn_cerrar = CTkButton(self, text = "Cerrar", command = cerrar_organizaciones, width = 200, height = 30)
        self.btn_cerrar.place(x = 300, y = 500)


# **********************************************************************************
# ************************* Agregar Organizaciones *********************************
# **********************************************************************************

class AgregarOrganizacion(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agegar Organizacion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))       

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                    
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_nombre = CTkLabel(self, text = "Nueva Organizacion", font=("Times New Roman",16))
        self.label_nombre.place(x = 100, y = 70)                  

        self.text_nombre = CTkEntry(self)
        self.text_nombre.place(x = 100, y = 160)

        self.label_inicial = CTkLabel(self, text = "Edad Inicial", font=("Times New Roman",16))
        self.label_inicial.place(x = 250, y = 70)                  

        self.text_inicial = CTkEntry(self)
        self.text_inicial.place(x = 250, y = 160)

        self.label_final = CTkLabel(self, text = "Edad Final", font=("Times New Roman",16))
        self.label_final.place(x = 400, y = 70)                  

        self.text_final = CTkEntry(self)
        self.text_final.place(x = 400, y = 160)

        self.label_sexo = CTkLabel(self, text = "Sexo (M o F o T)", font=("Times New Roman",16))
        self.label_sexo.place(x = 550, y = 70)                  

        self.text_sexo = CTkEntry(self)
        self.text_sexo.place(x = 550, y = 160)
        

        def confirmar_agregar_orgnizaciones():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f""" INSERT INTO `organizaciones`(`nombre`, `edad_inicial`, `edad_final`, `sexo`) VALUES ('{self.text_nombre.get()}','{self.text_inicial.get()}','{self.text_final.get()}','{self.text_sexo.get()}') """
                cursor.execute(sql)
                conn.commit()

                tabla_organizacion.insert("", END, text = f'{self.text_nombre.get()}', values = (f'{self.text_inicial.get()}',f'{self.text_final.get()}',f'{self.text_sexo.get()}')) 
                self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo agregar la organizacion")


        def cancelar_agregar_organizaciones():
            self.destroy()

        self.btn_confirmar_agregar = CTkButton(self, text = "Agregar", command = confirmar_agregar_orgnizaciones, width = 200, height = 30)
        self.btn_confirmar_agregar.place(x = 100, y = 300)        

        self.btn_cancelar_agregar = CTkButton(self, text = "Cancelar", command = cancelar_agregar_organizaciones, width = 200, height = 30)
        self.btn_cancelar_agregar.place(x = 400, y = 300)

# **********************************************************************************
# *************************** Eliminar Organizaciones ******************************
# **********************************************************************************

class EliminarOrganizacion(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Eliminar Organizacion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                       
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label = CTkLabel(self, text = "Eliminar Area", font=("Times New Roman",16))
        self.label.place(x = 250, y = 70)
        

        items_organizaciones = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()
        sql = """SELECT `nombre` FROM `organizaciones`;"""
        cursor.execute(sql)

        for index in cursor:
            items_organizaciones.append(index[0])            
        
        self.text = ttk.Combobox(self, width = 30)
        self.text.place(x = 250, y = 160)        
        self.text['values'] = items_organizaciones    
        

        def eliminar_organizaciones():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""DELETE FROM `organizaciones` WHERE nombre = '{self.text.get()}'"""
                cursor.execute(sql)
                conn.commit()
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar la organizacion")

        # ****************** actualizar tabla organizaciones ***************************
            tabla_organizacion.delete(*tabla_organizacion.get_children())  # esto borra toda la tabla 

            sql = """SELECT * FROM `organizaciones`;"""
            cursor.execute(sql)

            for index in cursor:
                tabla_organizacion.insert("",END, text = index[0], values = (index[1],index[2]))

            self.destroy()

            
        def cancelar_eliminar_organizaciones():
            self.destroy()

        self.btn_confirmar = CTkButton(self, text = "Eliminar", command = eliminar_organizaciones, width = 200, height = 30)
        self.btn_confirmar.place(x = 100, y = 300)        

        self.btn_cancelar = CTkButton(self, text = "Cancelar", command = cancelar_eliminar_organizaciones, width = 200, height = 30)
        self.btn_cancelar.place(x = 400, y = 300)


# **********************************************************************************
# **************************** Conceptos Salidas  **********************************
# **********************************************************************************

class ConceptosSalidas(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Conceptos Salida")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,600))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        global tabla_concepto_salidas
        tabla_concepto_salidas = ttk.Treeview(self)
        tabla_concepto_salidas.column("#0", width = 200)
        
        tabla_concepto_salidas.place(x = 100, y = 100)
        tabla_concepto_salidas.config(height = 10)
        tabla_concepto_salidas.heading("#0", text = "Conceptos Salidas")
        
        scrollbar = CTkScrollbar(self, command = tabla_concepto_salidas.yview, width = 18)
        scrollbar.place(in_ = tabla_concepto_salidas, relheigh = 1, relx = 1)

        tabla_concepto_salidas.config(yscrollcommand = scrollbar.set)


        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `concepto_salidas`;"""
        cursor.execute(sql)

        for index in cursor:
            tabla_concepto_salidas.insert("",END, text = index[0])
            

        def agregar_concepto_salidas():
            agregar_concepto_salida = AgregarConceptoSalida()
            

        def eliminar_concepto_salidas():
            eliminar_concepto_salida = EliminarConceptoSalida()


        def cerrar_concepto_salidas():
            self.destroy()

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar_concepto_salidas, width = 100, height = 30)
        self.btn_agregar.place(x = 150, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar_concepto_salidas, width = 100, height = 30)
        self.btn_eliminar.place(x = 550, y = 400)        

        self.btn_cerrar = CTkButton(self, text = "Cerrar", command = cerrar_concepto_salidas, width = 200, height = 30)
        self.btn_cerrar.place(x = 300, y = 500)


# **********************************************************************************
# ************************* Agregar Concepto Salida ********************************
# **********************************************************************************

class AgregarConceptoSalida(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agegar Concepto Salida")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))       

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                    
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_nueva = CTkLabel(self, text = "Nuevo Concepto de Salida", font=("Times New Roman",16))
        self.label_nueva.place(x = 100, y = 70)                  

        self.text_nueva = CTkEntry(self)
        self.text_nueva.place(x = 100, y = 160)
        

        def confirmar_agregar_concepto_salidas():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""INSERT INTO `concepto_salidas` (`nombre`) VALUES ('{self.text_nueva.get()}');"""
                cursor.execute(sql)
                conn.commit()

                tabla_concepto_salidas.insert("", END, text = f'{self.text_nueva.get()}')
                self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo agregar el concepto")


        def cancelar_agregar_concepto_salidas():
            self.destroy()

        self.btn_confirmar_agregar = CTkButton(self, text = "Agregar", command = confirmar_agregar_concepto_salidas, width = 200, height = 30)
        self.btn_confirmar_agregar.place(x = 100, y = 300)        

        self.btn_cancelar_agregar = CTkButton(self, text = "Cancelar", command = cancelar_agregar_concepto_salidas, width = 200, height = 30)
        self.btn_cancelar_agregar.place(x = 400, y = 300)

# **********************************************************************************
# *************************** Eliminar Concepto Salida *****************************
# **********************************************************************************

class EliminarConceptoSalida(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Eliminar Concepto Salida")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                       
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label = CTkLabel(self, text = "Eliminar Concepto de Salida", font=("Times New Roman",16))
        self.label.place(x = 250, y = 70)
        

        items_modalidad = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()
        sql = """SELECT `nombre` FROM `concepto_salidas`;"""
        cursor.execute(sql)

        for index in cursor:
            items_modalidad.append(index[0])            
        
        self.text = ttk.Combobox(self, width = 30)
        self.text.place(x = 250, y = 160)        
        self.text['values'] = items_modalidad    
        

        def eliminar_concepto_salidas():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""DELETE FROM `concepto_salidas` WHERE nombre = '{self.text.get()}'"""
                cursor.execute(sql)
                conn.commit()
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar el concepto")

        # ****************** actualizar tabla organizaciones ***************************
            tabla_concepto_salidas.delete(*tabla_concepto_salidas.get_children())  # esto borra toda la tabla 

            sql = """SELECT * FROM `concepto_salidas`;"""
            cursor.execute(sql)

            for index in cursor:
                tabla_concepto_salidas.insert("",END, text = index[0])

            self.destroy()

            
        def cancelar_eliminar_concepto_salidas():
            self.destroy()

        self.btn_confirmar = CTkButton(self, text = "Eliminar", command = eliminar_concepto_salidas, width = 200, height = 30)
        self.btn_confirmar.place(x = 100, y = 300)        

        self.btn_cancelar = CTkButton(self, text = "Cancelar", command = cancelar_eliminar_concepto_salidas, width = 200, height = 30)
        self.btn_cancelar.place(x = 400, y = 300)


# **********************************************************************************
# **************************** Conceptos Entradas  *********************************
# **********************************************************************************

class ConceptosEntradas(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Conceptos de Entradas")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,600))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        global tabla_concepto_entradas
        tabla_concepto_entradas = ttk.Treeview(self)
        tabla_concepto_entradas.column("#0", width = 200)
        
        tabla_concepto_entradas.place(x = 100, y = 100)
        tabla_concepto_entradas.config(height = 10)
        tabla_concepto_entradas.heading("#0", text = "Conceptos Entradas")
        
        scrollbar = CTkScrollbar(self, command = tabla_concepto_entradas.yview, width = 18)
        scrollbar.place(in_ = tabla_concepto_entradas, relheigh = 1, relx = 1)

        tabla_concepto_entradas.config(yscrollcommand = scrollbar.set)


        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `concepto_entradas`;"""
        cursor.execute(sql)

        for index in cursor:
            tabla_concepto_entradas.insert("",END, text = index[0])
            

        def agregar_concepto_entradas():
            agregar_concepto_entrada = AgregarConceptoEntrada()
            

        def eliminar_concepto_entradas():
            eliminar_concepto_entrada = EliminarConceptoEntrada()


        def cerrar_concepto_entradas():
            self.destroy()

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar_concepto_entradas, width = 100, height = 30)
        self.btn_agregar.place(x = 150, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar_concepto_entradas, width = 100, height = 30)
        self.btn_eliminar.place(x = 550, y = 400)        

        self.btn_cerrar = CTkButton(self, text = "Cerrar", command = cerrar_concepto_entradas, width = 200, height = 30)
        self.btn_cerrar.place(x = 300, y = 500)


# **********************************************************************************
# ************************* Agregar Concepto Entradas ******************************
# **********************************************************************************

class AgregarConceptoEntrada(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agegar Concepto de Entrada")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))       

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                    
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_nueva = CTkLabel(self, text = "Nuevo Concepto de Entrada", font=("Times New Roman",16))
        self.label_nueva.place(x = 100, y = 70)                  

        self.text_nueva = CTkEntry(self)
        self.text_nueva.place(x = 100, y = 160)
        

        def confirmar_agregar_concepto_entradas():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""INSERT INTO `concepto_entradas` (`nombre`) VALUES ('{self.text_nueva.get()}');"""
                cursor.execute(sql)
                conn.commit()

                tabla_concepto_entradas.insert("", END, text = f'{self.text_nueva.get()}')
                self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo agregar el concepto")


        def cancelar_agregar_concepto_entradas():
            self.destroy()

        self.btn_confirmar_agregar = CTkButton(self, text = "Agregar", command = confirmar_agregar_concepto_entradas, width = 200, height = 30)
        self.btn_confirmar_agregar.place(x = 100, y = 300)        

        self.btn_cancelar_agregar = CTkButton(self, text = "Cancelar", command = cancelar_agregar_concepto_entradas, width = 200, height = 30)
        self.btn_cancelar_agregar.place(x = 400, y = 300)

# **********************************************************************************
# *************************** Eliminar Concepto Entradas ***************************
# **********************************************************************************

class EliminarConceptoEntrada(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Eliminar Concepto de Entrada")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                       
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label = CTkLabel(self, text = "Eliminar Concepto de Salida", font=("Times New Roman",16))
        self.label.place(x = 250, y = 70)
        

        items_modalidad = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()
        sql = """SELECT `nombre` FROM `concepto_entradas`;"""
        cursor.execute(sql)

        for index in cursor:
            items_modalidad.append(index[0])            
        
        self.text = ttk.Combobox(self, width = 30)
        self.text.place(x = 250, y = 160)        
        self.text['values'] = items_modalidad    
        

        def eliminar_concepto_entradas():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""DELETE FROM `concepto_entradas` WHERE nombre = '{self.text.get()}'"""
                cursor.execute(sql)
                conn.commit()
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar el concepto")

        # ****************** actualizar tabla organizaciones ***************************
            tabla_concepto_entradas.delete(*tabla_concepto_entradas.get_children())  # esto borra toda la tabla 

            sql = """SELECT * FROM `concepto_entradas`;"""
            cursor.execute(sql)

            for index in cursor:
                tabla_concepto_entradas.insert("",END, text = index[0])

            self.destroy()

            
        def cancelar_eliminar_concepto_entradas():
            self.destroy()

        self.btn_confirmar = CTkButton(self, text = "Eliminar", command = eliminar_concepto_entradas, width = 200, height = 30)
        self.btn_confirmar.place(x = 100, y = 300)        

        self.btn_cancelar = CTkButton(self, text = "Cancelar", command = cancelar_eliminar_concepto_entradas, width = 200, height = 30)
        self.btn_cancelar.place(x = 400, y = 300)

# **********************************************************************************
# **********************************  Monedas  *************************************
# **********************************************************************************

class Monedas(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Monedas")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,600))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        global tabla_monedas
        tabla_monedas = ttk.Treeview(self)
        tabla_monedas.column("#0", width = 200)
        
        tabla_monedas.place(x = 100, y = 100)
        tabla_monedas.config(height = 10)
        tabla_monedas.heading("#0", text = "Monedas")
        
        scrollbar = CTkScrollbar(self, command = tabla_monedas.yview, width = 18)
        scrollbar.place(in_ = tabla_monedas, relheigh = 1, relx = 1)

        tabla_monedas.config(yscrollcommand = scrollbar.set)


        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `monedas`;"""
        cursor.execute(sql)

        for index in cursor:
            tabla_monedas.insert("",END, text = index[0])
            

        def agregar_moneda():
            agregar_monedas = AgregarMoneda()
            

        def eliminar_moneda():
            eliminar_monedas = EliminarMoneda()


        def cerrar_moneda():
            self.destroy()

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar_moneda, width = 100, height = 30)
        self.btn_agregar.place(x = 150, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar_moneda, width = 100, height = 30)
        self.btn_eliminar.place(x = 550, y = 400)        

        self.btn_cerrar = CTkButton(self, text = "Cerrar", command = cerrar_moneda, width = 200, height = 30)
        self.btn_cerrar.place(x = 300, y = 500)


# **********************************************************************************
# ************************* Agregar Moneda *****************************************
# **********************************************************************************

class AgregarMoneda(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agegar Moneda")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))       

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                    
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_nueva = CTkLabel(self, text = "Nueva Moneda", font=("Times New Roman",16))
        self.label_nueva.place(x = 100, y = 70)                  

        self.text_nueva = CTkEntry(self)
        self.text_nueva.place(x = 100, y = 160)
        

        def confirmar_agregar_concepto_entradas():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""INSERT INTO `monedas` (`nombre`) VALUES ('{self.text_nueva.get()}');"""
                cursor.execute(sql)
                conn.commit()

                tabla_monedas.insert("", END, text = f'{self.text_nueva.get()}')
                self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo agregar la moneda")


        def cancelar_agregar_concepto_entradas():
            self.destroy()

        self.btn_confirmar_agregar = CTkButton(self, text = "Agregar", command = confirmar_agregar_concepto_entradas, width = 200, height = 30)
        self.btn_confirmar_agregar.place(x = 100, y = 300)        

        self.btn_cancelar_agregar = CTkButton(self, text = "Cancelar", command = cancelar_agregar_concepto_entradas, width = 200, height = 30)
        self.btn_cancelar_agregar.place(x = 400, y = 300)

# **********************************************************************************
# *************************** Eliminar Moneda **************************************
# **********************************************************************************

class EliminarMoneda(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Eliminar Moneda")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,400))                       
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label = CTkLabel(self, text = "Eliminar Moneda", font=("Times New Roman",16))
        self.label.place(x = 250, y = 70)
        

        items_moneda = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()
        sql = """SELECT `nombre` FROM `monedas`;"""
        cursor.execute(sql)

        for index in cursor:
            items_moneda.append(index[0])            
        
        self.text = ttk.Combobox(self, width = 30)
        self.text.place(x = 250, y = 160)        
        self.text['values'] = items_moneda    
        

        def confirmar_eliminar_moneda():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f"""DELETE FROM `monedas` WHERE nombre = '{self.text.get()}'"""
                cursor.execute(sql)
                conn.commit()
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar el concepto")

        # ****************** actualizar tabla organizaciones ***************************
            tabla_monedas.delete(*tabla_monedas.get_children())  # esto borra toda la tabla 

            sql = """SELECT * FROM `monedas`;"""
            cursor.execute(sql)

            for index in cursor:
                tabla_monedas.insert("",END, text = index[0])

            self.destroy()

            
        def cancelar_eliminar_moneda():
            self.destroy()

        self.btn_confirmar = CTkButton(self, text = "Eliminar", command = confirmar_eliminar_moneda, width = 200, height = 30)
        self.btn_confirmar.place(x = 100, y = 300)        

        self.btn_cancelar = CTkButton(self, text = "Cancelar", command = cancelar_eliminar_moneda, width = 200, height = 30)
        self.btn_cancelar.place(x = 400, y = 300)


# **********************************************************************************
# ***************************** agregar inventario *********************************
# **********************************************************************************

class AgregarInventario(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agregar Inventario")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (600,600))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 600)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")
        
        ultimo_id_inventario = StringVar()
        ultimo_id_inventario.set("")

        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT MAX(ID) FROM `inventario`;"""
        cursor.execute(sql)
        
        for index in cursor:                
            ultimo_id_inventario.set(index[0])

        self.label_ultimo_id_inventario = CTkLabel(self, textvariable = ultimo_id_inventario)
        self.label_ultimo_id_inventario.place(x = 650, y = 70) 

        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 738, y = 70) 
        
        texto_id_agregar_inventario = CTkEntry(self)
        texto_id_agregar_inventario.place(x = 800, y = 70)       

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 110)  
        
        texto_nombre_agregar_inventario = CTkEntry(self)
        texto_nombre_agregar_inventario.place(x = 800, y = 110)     

        self.label_cantidad = CTkLabel(self,text="Cantidad:", font=("Times New Roman",16))
        self.label_cantidad.place(x = 692, y = 150) 
        
        texto_cantidad_agregar_inventario = CTkEntry(self)
        texto_cantidad_agregar_inventario.place(x = 800, y = 150) 

        self.label_inmueble = CTkLabel(self,text="Inmueble:", font=("Times New Roman",16))
        self.label_inmueble.place(x = 692, y = 190) 

        items_inmueble = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `inmuebles`;"""
        cursor.execute(sql)
        for index in cursor:
            items_inmueble.append(index[0])
        
        texto_inmueble_agregar_inventario = CTkComboBox(self, values = items_inmueble)
        texto_inmueble_agregar_inventario.set("Seleccionar")
        texto_inmueble_agregar_inventario.place(x = 800, y = 190)  

        self.label_area = CTkLabel(self,text="Area:", font=("Times New Roman",16))
        self.label_area.place(x = 692, y = 230) 

        items_area = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `areas_trabajo`;"""
        cursor.execute(sql)
        for index in cursor:
            items_area.append(index[0])
        
        texto_area_agregar_inventario = CTkComboBox(self, values = items_area)
        texto_area_agregar_inventario.set("Seleccionar")
        texto_area_agregar_inventario.place(x = 800, y = 230)          

        self.label_detalles = CTkLabel(self,text="Detalles:", font=("Times New Roman",16))
        self.label_detalles.place(x = 692, y = 270) 
        
        texto_detalles_agregar_inventario = CTkTextbox(self,width=300, height=100)
        texto_detalles_agregar_inventario.place(x = 650, y = 270)

        def confirmar_agregar_inventario():
            try:
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = """SELECT ID FROM inventario;"""
                cursor.execute(sql)


                id_repetido = False
                

                for index in cursor:        
            
                    if int(texto_id_agregar_inventario.get()) == index[0]:
                        id_repetido = True

                if id_repetido == False:   
                    confirmar = messagebox.askokcancel("Confirmar", "¿ Desea agregar el nuevo inventario ?")
                    if confirmar == True:                        
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()
                        
                        
                        sql = f"""  INSERT INTO `inventario`(`Id`, `Nombre`, `Cantidad`, `Inmueble`, `Area`, `Detalles`) VALUES ('{int(texto_id_agregar_inventario.get())}','{texto_nombre_agregar_inventario.get()}','{int(texto_cantidad_agregar_inventario.get())}','{texto_inmueble_agregar_inventario.get()}','{texto_area_agregar_inventario.get()}','{texto_detalles_agregar_inventario.get(1.0,END)}') """
                        cursor.execute(sql)
                        conn.commit()

                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = """SELECT MAX(ID) FROM `inventario`;"""
                    cursor.execute(sql)
                    
                    for index in cursor:                
                        ultimo_id_inventario.set(index[0]) 

                    texto_id_agregar_inventario.delete(0,END)
                    texto_nombre_agregar_inventario.delete(0,END)
                    texto_cantidad_agregar_inventario.delete(0,END)
                    texto_inmueble_agregar_inventario.set("Seleccionar")
                    texto_area_agregar_inventario.set("Seleccionar")
                    texto_detalles_agregar_inventario.delete(1.0,END)

                else:
                    error = messagebox.showinfo("Error", "Ese ID ya existe")
            except:
                error = messagebox.showinfo("Error","Escribe bien los datos")
            
                
            
        def cancelar_agregar_cliente():            
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=confirmar_agregar_inventario, width = 150, height = 40)
        self.btn_aceptar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_agregar_cliente, width = 150, height = 40)
        self.btn_cancelar.place(x=820 ,y=500 )


# **********************************************************************************
# ********************************* consultas inventarios **************************
# **********************************************************************************
class ConsultarInventario(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Consultas Inventario")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (800,600))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        global tabla_inventario
        tabla_inventario = ttk.Treeview(self, columns = ("Nombre","Cantidad","Inmueble","Area","Detalles"))
        tabla_inventario.column("#0", width = 50)
        tabla_inventario.column("Nombre", width = 200)
        tabla_inventario.column("Cantidad", width = 100)
        tabla_inventario.column("Inmueble", width = 100)
        tabla_inventario.column("Area", width = 100)
        tabla_inventario.column("Detalles", width = 200)
        
        tabla_inventario.place(x = 100, y = 200)
        tabla_inventario.config(height = 10)
        tabla_inventario.heading("#0", text = "Id")
        tabla_inventario.heading("Nombre", text = "Nombre")
        tabla_inventario.heading("Cantidad", text = "Cantidad")
        tabla_inventario.heading("Inmueble", text = "Inmueble")
        tabla_inventario.heading("Area", text = "Area")
        tabla_inventario.heading("Detalles", text = "Detalles")
        
        scrollbar = CTkScrollbar(self, command = tabla_inventario.yview, width = 18)
        scrollbar.place(in_ = tabla_inventario, relheigh = 1, relx = 1)

        tabla_inventario.config(yscrollcommand = scrollbar.set)       

        def seleccionar_indice(event):
            for item in tabla_inventario.selection():  
                global id_inv                              
                id_inv = copy.deepcopy(str(tabla_inventario.item(item,"text")))         
                
                
        tabla_inventario.bind("<<TreeviewSelect>>", seleccionar_indice)

        opcion_radio_btn_consulta_inventario = IntVar()

        self.radio_btn_nombre = CTkRadioButton(self, variable = opcion_radio_btn_consulta_inventario, value = 1, text="Por Nombre")
        self.radio_btn_nombre.place(x = 100 , y = 50)

        items_nombres = []        
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `inventario` ORDER BY `nombre`;"""
        cursor.execute(sql)
        for index in cursor:
            items_nombres.append(index[0])  

        string_nombre = StringVar()
        string_nombre.set("")

        self.nombre_consultar_inventario = CTkEntry(self, textvariable = string_nombre)                
        self.nombre_consultar_inventario.place(x = 100, y = 80)

        def escoger_nombre(event):
            new = CTkToplevel()        
            new.title("Escoger Nombre") 
            new.entry = AutocompleteEntryListbox(new, width = 60, completevalues=items_nombres)
            new.entry.pack()
            def seleccionar():
                string_nombre.set(new.entry.get())
                new.destroy()

            new.btn = CTkButton(new, command=seleccionar, text = "Seleccionar")
            new.btn.pack()             

        self.nombre_consultar_inventario.bind("<Double-Button-1>", escoger_nombre)


        self.radio_btn_inmueble = CTkRadioButton(self, variable = opcion_radio_btn_consulta_inventario, value = 2, text="Por Inmueble")
        self.radio_btn_inmueble.place(x = 600 , y = 50)

        items_inmueble = []
        items_inmueble.append("Todas")
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `inmuebles`;"""
        cursor.execute(sql)
        for index in cursor:
            items_inmueble.append(index[0])        
        
        self.combo_areas_consulta_inventario = CTkComboBox(self, values = items_inmueble)
        self.combo_areas_consulta_inventario.set("Todas")
        self.combo_areas_consulta_inventario.place(x = 600 , y = 80)

        def buscar_consulta():            
            tabla_inventario.delete(*tabla_inventario.get_children())

            # ***********************************************************************************************

            if opcion_radio_btn_consulta_inventario.get() == 1:

                if self.nombre_consultar_inventario.get() == "":
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = """SELECT * FROM `inventario`;"""
                    cursor.execute(sql)

                    for index in cursor:
                        tabla_inventario.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5]))

                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = f"""SELECT * FROM `inventario` WHERE Nombre = "{self.nombre_consultar_inventario.get()}";"""
                    cursor.execute(sql)

                    for index in cursor:
                        tabla_inventario.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5]))


            # ************************************************************************************************
                
            elif opcion_radio_btn_consulta_inventario.get() == 2:    

                if self.combo_areas_consulta_inventario.get() == "Todas":

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = """SELECT * FROM `inventario`;"""
                    cursor.execute(sql)

                    for index in cursor:
                        tabla_inventario.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5]))

                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = f"""SELECT * FROM `inventario` WHERE Area = "{self.combo_areas_consulta_inventario.get()}";"""
                    cursor.execute(sql)

                    for index in cursor:
                        tabla_inventario.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5]))


            # ***************************************************************************************
            else:                                          
                
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = """SELECT * FROM `inventario`;"""
                cursor.execute(sql)

                for index in cursor:
                    tabla_inventario.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5]))
            
            

        self.btn_buscar = CTkButton(self, height=50, text="Buscar",command=buscar_consulta, width=400)
        self.btn_buscar.place(x = 200, y = 350)

        def eliminar_inventario():
            if id_inv == 0:
                error = messagebox.askokcancel("Error", "Selecciona algun elemento")
            
            else:                
                confirmar = messagebox.askokcancel("Confirmar", "¿ Desea eliminar el inventario ?")
                if confirmar == True:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `inventario` WHERE Id = {id_inv} """
                    cursor.execute(sql)
                    conn.commit()

                    
                

        self.btn_eliminar = CTkButton(self, height=50, width=200, text="Eliminar",command=eliminar_inventario)
        self.btn_eliminar.place(x = 100 , y = 450)

        def modificar_inventario(): 
            if id_inv == 0:
                error = messagebox.askokcancel("Error", "Selecciona algun elemento")
            
            else:
                confirmar = messagebox.askokcancel("Confirmar", "¿ Desea modificar el inventario ?")

                global str_texto_id_modificar_inventario
                str_texto_id_modificar_inventario = StringVar()

                global str_texto_nombre_modificar_inventario
                str_texto_nombre_modificar_inventario = StringVar()

                global str_texto_cantidad_modificar_inventario
                str_texto_cantidad_modificar_inventario = StringVar() 

                global str_texto_inmueble_modificar_inventario
                str_texto_inmueble_modificar_inventario = StringVar()

                global str_texto_area_modificar_inventario
                str_texto_area_modificar_inventario = StringVar()

                global str_texto_detalles_modificar_inventario
                str_texto_detalles_modificar_inventario = StringVar()

                if confirmar == True:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `inventario` WHERE Id = {id_inv};  """
                    cursor.execute(sql)
                    for index in cursor:
                        str_texto_id_modificar_inventario.set(str(index[0]))
                        str_texto_nombre_modificar_inventario.set(index[1])
                        str_texto_cantidad_modificar_inventario.set(str(index[2]))
                        str_texto_inmueble_modificar_inventario.set(index[3])
                        str_texto_area_modificar_inventario.set(index[4])
                        str_texto_detalles_modificar_inventario.set(index[5])

                    modificando_inventario = ModificarInventario()    



        self.btn_modificar = CTkButton(self, width=200 ,height=50, text="Modificar",command=modificar_inventario)
        self.btn_modificar.place(x = 500 , y = 450)

        #**********************************************************************************************************************
        def exportar_excel():
            try:
                rows = []
                for item in tabla_inventario.get_children():
                    rows.append(tabla_inventario.item(item)['values'])
                
                df = pd.DataFrame(rows, columns=["Nombre", "Cantidad", "Inmueble", "Detalles"])                
                df.to_excel(f"D:/MyCurch/Inventario {fecha_actual}.xlsx", index=False)
                error = messagebox.showinfo("Exportar", "Exportado a Excel")                

            except:
                error = messagebox.showinfo("Error","Algun dato introducido no esta bien y no se puede exportar")

        self.btn_exportar_excel = CTkButton(self, command = exportar_excel, text = "Exportar a Excel", width = 30, height = 40)
        self.btn_exportar_excel.place(x = 350, y = 500)
        
        #***********************************************************************************************************************


# **********************************************************************************
# ***************************** modificar inventario *******************************
# **********************************************************************************

class ModificarInventario(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Modificar Inventario")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes inventario/{id_inv}.jpg"), size = (600,600))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 600)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (600,600))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 600)
            self.label_imagen.place(x = 0 , y = 0)       

        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 738, y = 70) 
        
        texto_id_modificar_inventario = CTkEntry(self, textvariable = str_texto_id_modificar_inventario)
        texto_id_modificar_inventario.place(x = 800, y = 70)       

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 110)  
        
        texto_nombre_modificar_inventario = CTkEntry(self, textvariable = str_texto_nombre_modificar_inventario)
        texto_nombre_modificar_inventario.place(x = 800, y = 110)     

        self.label_cantidad = CTkLabel(self,text="Cantidad:", font=("Times New Roman",16))
        self.label_cantidad.place(x = 692, y = 150)  
        
        texto_cantidad_modificar_inventario = CTkEntry(self, textvariable=str_texto_cantidad_modificar_inventario)
        texto_cantidad_modificar_inventario.place(x = 800, y = 150) 

        self.label_inmueble = CTkLabel(self,text="Inmueble:", font=("Times New Roman",16))
        self.label_inmueble.place(x = 692, y = 190) 

        items_inmueble = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `inmuebles`;"""
        cursor.execute(sql)
        for index in cursor:
            items_inmueble.append(index[0]) 

        texto_inmueble_modificar_inventario = CTkComboBox(self, values = items_inmueble,)
        texto_inmueble_modificar_inventario.set(str_texto_inmueble_modificar_inventario.get())
        texto_inmueble_modificar_inventario.place(x = 800, y = 190) 


        self.label_area = CTkLabel(self,text="Area:", font=("Times New Roman",16))
        self.label_area.place(x = 692, y = 230) 

        items_area = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `inmuebles`;"""
        cursor.execute(sql)
        for index in cursor:
            items_area.append(index[0])  

        texto_area_modificar_inventario = CTkComboBox(self, values = items_area,)
        texto_area_modificar_inventario.set(str_texto_area_modificar_inventario.get())
        texto_area_modificar_inventario.place(x = 800, y = 230)          

        self.label_detalles = CTkLabel(self,text="Detalles:", font=("Times New Roman",16))
        self.label_detalles.place(x = 692, y = 270) 

        texto_detalles_modificar_inventario = CTkTextbox(self,width=300, height=100)  
        texto_detalles_modificar_inventario.insert("0.0",str_texto_detalles_modificar_inventario.get())     
        texto_detalles_modificar_inventario.place(x = 650, y = 270)

        def confirmar_modificar_inventario():
            if id_inv == 0:
                error = messagebox.askokcancel("Error", "Selecciona algun elemento")
            
            else:
                try: 
                    confirmar = messagebox.askokcancel("Confirmar", "¿ Desea modificar el nuevo inventario ?")
                    if confirmar == True:                        
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "mychurch",
                            password = "123456",
                            database = "mychurch"
                            )
                        cursor = conn.cursor()                    
                                            
                        sql = f""" UPDATE `inventario` SET `Id`='{int(texto_id_modificar_inventario.get())}',`Nombre`='{texto_nombre_modificar_inventario.get()}',`Cantidad`='{int(texto_cantidad_modificar_inventario.get())}',`Inmueble`='{texto_inmueble_modificar_inventario.get()}',`Area`='{texto_area_modificar_inventario.get()}',`Detalles`='{texto_detalles_modificar_inventario.get(1.0,END)}' WHERE Id = {id_inv} """
                        cursor.execute(sql)
                        conn.commit()    

                        tabla_inventario.delete(*tabla_inventario.get_children())
                        
                        self.destroy()                                                             
                        
                    
                except:
                    error = messagebox.showinfo("Error","No se pudo modificar los datos")     
                
            
        def cancelar_modificar_cliente():            
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=confirmar_modificar_inventario, width = 150, height = 40)
        self.btn_aceptar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_modificar_cliente, width = 150, height = 40)
        self.btn_cancelar.place(x=820 ,y=500 )                      



# **********************************************************************************
# *************************************** Agregar Entradas *************************
# **********************************************************************************

class AgregarEntradas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agregar Entrada")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (600,600))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 600)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        ultimo_id_entrada = 0

        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT MAX(ID) FROM `entradas`;"""
        cursor.execute(sql)
        
        for index in cursor:             
            if index[0] == None:
                ultimo_id_entrada = 0                
            else:
               ultimo_id_entrada = index[0] 

        

        self.label_fecha = CTkLabel(self,text="Fecha:", font=("Times New Roman",16))
        self.label_fecha.place(x = 650, y = 70) 

        self.texto_fecha = CTkEntry(self)
        self.texto_fecha.place(x = 750, y = 70)  

        # ********************* para escoger la fecha ********************
        def seleccionar_fecha():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.texto_fecha.delete(0,END)               
                fecha_select = cal.get_date()
                self.texto_fecha.insert(0,str(fecha_select)) 
                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha = CTkButton(self, text="...",command=seleccionar_fecha, width = 30, height = 27)
        self.btn_seleccionar_fecha.place(x = 900, y = 70)

        self.label_descripcion = CTkLabel(self,text="Descripcion:", font=("Times New Roman",16))
        self.label_descripcion.place(x = 650, y = 130) 

        conceptos_entradas = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `concepto_entradas`;"""
        cursor.execute(sql)
        for index in cursor:
            conceptos_entradas.append(index[0])

        
        self.texto_descripcion = CTkComboBox(self, values = conceptos_entradas)
        self.texto_descripcion.set("")
        self.texto_descripcion.place(x = 750, y = 130) 

        self.label_servicio = CTkLabel(self,text="Servicio:", font=("Times New Roman",16))
        self.label_servicio.place(x = 650, y = 190)  
        
        self.texto_servicio = CTkEntry(self)
        self.texto_servicio.place(x = 750, y = 190) 

        self.label_monto = CTkLabel(self,text="Monto:", font=("Times New Roman",16))
        self.label_monto.place(x = 650, y = 250)  
        
        self.texto_monto = CTkEntry(self)
        self.texto_monto.place(x = 750, y = 250) 

        self.label_moneda = CTkLabel(self,text="Moneda:", font=("Times New Roman",16))
        self.label_moneda.place(x = 650, y = 310)  
        
        monedas = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `monedas`;"""
        cursor.execute(sql)
        for index in cursor:
            monedas.append(index[0])

        
        self.texto_monedas = CTkComboBox(self, values = monedas)
        self.texto_monedas.set("")
        self.texto_monedas.place(x = 750, y = 310)

        def ejecutar_entrada():
            confirmar = messagebox.askokcancel("Confirmar", "Confirmar entrada")
            if confirmar == True:                        
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()
                
                
                sql = f""" INSERT INTO `entradas`(`Id`,`fecha`, `descripcion`, `servicio`, `monto`, `moneda`) VALUES ('{ultimo_id_entrada + 1}','{self.texto_fecha.get()}','{self.texto_descripcion.get()}','{self.texto_servicio.get()}','{self.texto_monto.get()}','{self.texto_monedas.get()}') """
                cursor.execute(sql)
                conn.commit()

                self.destroy()


        def cancelar_entrada():            
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=ejecutar_entrada, width = 150, height = 40)
        self.btn_aceptar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_entrada, width = 150, height = 40)
        self.btn_cancelar.place(x=820 ,y=500 )


        
# **********************************************************************************
# ********************************** Consultas Entrada Mensual *********************
# **********************************************************************************

class ConsultarEntradaMensual(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Consulta Entrada Mensual")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1300x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (1300,700))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        self.tabla = ttk.Treeview(self, columns = ("Fecha","Descripcion","Servicio","Monto","Moneda"))
        self.tabla.column("#0", width = 50)
        self.tabla.column("Fecha", width = 100)
        self.tabla.column("Descripcion", width = 300)
        self.tabla.column("Servicio", width = 300)
        self.tabla.column("Monto", width = 100)
        self.tabla.column("Moneda", width = 100)
        
        self.tabla.place(x = 300, y = 200)
        self.tabla.config(height = 20)
        self.tabla.heading("#0", text = "Id")
        self.tabla.heading("Fecha", text = "Fecha")
        self.tabla.heading("Descripcion", text = "Descripcion")
        self.tabla.heading("Servicio", text = "Servicio")
        self.tabla.heading("Monto", text = "Monto")
        self.tabla.heading("Moneda", text = "Moneda")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)    


        self.labelmes = CTkLabel(self, text="Mes", font=("Times New Roman",16))                
        self.labelmes.place(x = 140, y = 50)
        
        self.mes = CTkEntry(self, width=40)                
        self.mes.place(x = 130, y = 80)

        self.anio = CTkEntry(self,width=80)                
        self.anio.place(x = 180, y = 80)    

        self.label_moneda = CTkLabel(self, text="Moneda")
        self.label_moneda.place(x = 1000 , y = 50)              

        monedas = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `monedas`;"""
        cursor.execute(sql)
        for index in cursor:
            monedas.append(index[0])

        
        self.texto_moneda = CTkComboBox(self, values = monedas)
        self.texto_moneda.set("")
        self.texto_moneda.place(x = 1000, y = 80) 

        self.label_total1 = CTkLabel(self, text="Total:", font=("Times New Roman",16))
        self.label_total1.place(x = 1050, y = 400) 

        self.total = StringVar()
        self.total.set("")

        self.label_total = CTkLabel(self, textvariable = self.total, font=("Times New Roman",16))
        self.label_total.place(x = 1050, y = 450)  

        self.mon = StringVar()
        self.mon.set("")

        self.label_moneda = CTkLabel(self, textvariable = self.mon, font=("Times New Roman",16))
        self.label_moneda.place(x = 1250, y = 450)  

        def seleccionar_fecha():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.mes.delete(0,END)
                self.anio.delete(0,END)                                              

                self.mes.insert(0,str(cal.get_date()[5:7])) 
                self.anio.insert(0,str(cal.get_date()[0:4]))                

                calendario.destroy()                                
                

            btn = CTkButton(calendario, text="Seleccionar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha = CTkButton(self, text="Fecha",command=seleccionar_fecha, width = 60, height = 27)
        self.btn_seleccionar_fecha.place(x = 600, y = 70)


        def balance_mensual():

            try:

                self.tabla.delete(*self.tabla.get_children())

                # *********************** hallemos fecha inicial y final *******************************

                anio = int(self.anio.get())
                mes = int(self.mes.get())
                fecha_inicio = str(date(anio,mes,1))

                fecha_final = date(anio,mes,1) 

                if mes == 12:
                    fecha_final = date(anio + 1, 1, 1)
                else:
                    fecha_final = date(anio,mes + 1,1) 

                fecha_final = str(fecha_final)            

                monto_total = 0
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `entradas` WHERE fecha >= "{fecha_inicio}" AND fecha < "{fecha_final}" AND moneda = "{self.texto_moneda.get()}" ORDER BY fecha ASC; """
                cursor.execute(sql) 
                
                for index in cursor:  
                    monto_total += index[4]               
                    self.tabla.insert("",END, text = index[0], values = (str(index[1]),index[2],index[3],str(index[4]),self.texto_moneda.get()))

                self.total.set(str(monto_total))
                self.mon.set(self.texto_moneda.get())
            
            except:
                error = messagebox.showinfo("Error", "Escribe bien los datos para buscar")
        
        
        self.btn_balance = CTkButton(self, text="Balance",command=balance_mensual, width = 600, height = 40)
        self.btn_balance.place(x = 350, y = 520) 

        #**********************************************************************************************************************
        def exportar_excel():
            try:
                rows = []
                for item in self.tabla.get_children():
                    rows.append(self.tabla.item(item)['values'])
                
                df = pd.DataFrame(rows, columns=["Fecha", "Descripcion", "Servicio", "Monto", "Moneda"])                
                df.to_excel(f"D:/MyCurch/Balance Entradas Mensual mes {self.mes.get()} año {self.anio.get()}.xlsx", index=False)
                error = messagebox.showinfo("Exportar", "Exportado a Excel")                

            except:
                error = messagebox.showinfo("Error","Algun dato introducido no esta bien y no se puede exportar")

        self.btn_exportar_excel = CTkButton(self, command = exportar_excel, text = "Exportar a Excel", width = 30, height = 40)
        self.btn_exportar_excel.place(x = 1100, y = 620)
        
        #***********************************************************************************************************************



# **********************************************************************************
# ********************************** Consultas Entrada Anual ***********************
# **********************************************************************************

class ConsultarEntradaAnual(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Consulta Entrada Anual")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (800,700))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        self.tabla = ttk.Treeview(self, columns = ("Descripcion","Monto","Moneda"))
        self.tabla.column("#0", width = 50)        
        self.tabla.column("Descripcion", width = 300)        
        self.tabla.column("Monto", width = 150)
        self.tabla.column("Moneda", width = 100)
        
        self.tabla.place(x = 170, y = 200)
        self.tabla.config(height = 20)

        self.tabla.heading("#0", text = "Id")        
        self.tabla.heading("Descripcion", text = "Descripcion")        
        self.tabla.heading("Monto", text = "Monto")
        self.tabla.heading("Moneda", text = "Moneda")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)        
        

        self.label_mensual = CTkLabel(self, text="Año")
        self.label_mensual.place(x = 70 , y = 50)   

        self.label_moneda = CTkLabel(self, text="Moneda")
        self.label_moneda.place(x = 600 , y = 50)          

        self.anual = CTkEntry(self)                
        self.anual.place(x = 70, y = 80)        

        monedas = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `monedas`;"""
        cursor.execute(sql)
        for index in cursor:
            monedas.append(index[0])

        
        self.texto_moneda = CTkComboBox(self, values = monedas)
        self.texto_moneda.set("")
        self.texto_moneda.place(x = 600, y = 80) 

        self.label_total1 = CTkLabel(self, text="Total:", font=("Times New Roman",16))
        self.label_total1.place(x = 650, y = 400) 

        self.total = StringVar()
        self.total.set("")

        self.label_total = CTkLabel(self, textvariable = self.total, font=("Times New Roman",16))
        self.label_total.place(x = 650, y = 450)  

        self.mon = StringVar()
        self.mon.set("")

        self.label_moneda = CTkLabel(self, textvariable = self.mon, font=("Times New Roman",16))
        self.label_moneda.place(x = 750, y = 450)  


        def balance():
            self.tabla.delete(*self.tabla.get_children())

            # ***************** ubicar fecha inicial y final para hacer el recorrido en la base de datos *********************            
            
            try:
                fecha_inicial = str(self.anual.get()) + "-01-01"

                if int(fecha_actual.year) == int(self.anual.get()):
                    fecha = fecha_actual + timedelta(1)              # esto es para que me incluya las entradas de hoy mas adelante
                    fecha_final = str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)
                    

                elif int(fecha_actual.year) > int(self.anual.get()):
                    fecha_final = str(int(self.anual.get())+1)+"-01-01"
                    

                else:
                    error = messagebox.showinfo("Error", "No ha llegado esa fecha todavia")

                
                listado_descripciones = []
                listado_descripciones.append("Diezmo")
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `concepto_entradas` """
                cursor.execute(sql)

                for index in cursor:
                    listado_descripciones.append(index[0])   

                monto_total = 0         
                                       

                for desc in listado_descripciones:                                                                 
                    monto_local = 0                     
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `entradas` WHERE fecha>="{fecha_inicial}" AND fecha<"{fecha_final}" AND moneda = "{self.texto_moneda.get()}" AND descripcion = "{desc}";  """
                    cursor.execute(sql)

                    for index in cursor:
                        monto_local += index[4] 
                        monto_total += index[4]  

                    if monto_local > 0: 
                        self.tabla.insert("",END, text = "", values = (desc,monto_local,self.texto_moneda.get())) 
                    else:
                        pass

                    self.total.set(str(monto_total))
                    self.mon.set(self.texto_moneda.get())

            except:
                error = messagebox.showinfo("Error", "Escribe todos los datos correctamenmte") 

        self.btn_balance = CTkButton(self, text="Balance",command=balance, width = 400, height = 40)
        self.btn_balance.place(x = 200, y = 520)

        #**********************************************************************************************************************
        def exportar_excel():
            try:
                rows = []
                for item in self.tabla.get_children():
                    rows.append(self.tabla.item(item)['values'])
                
                df = pd.DataFrame(rows, columns=["Descripcion", "Monto", "Moneda"])                
                df.to_excel(f"D:/MyCurch/Balance Entradas Anual año {self.anual.get()}.xlsx", index=False)
                error = messagebox.showinfo("Exportar", "Exportado a Excel")                

            except:
                error = messagebox.showinfo("Error","Algun dato introducido no esta bien y no se puede exportar")

        self.btn_exportar_excel = CTkButton(self, command = exportar_excel, text = "Exportar a Excel", width = 30, height = 40)
        self.btn_exportar_excel.place(x = 650, y = 620)
        
        #***********************************************************************************************************************





# **********************************************************************************
# *************************************** Agregar Salidas **************************
# **********************************************************************************

class AgregarSalidas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agregar Salidas")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 3.jpg"), size = (600,600))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 600)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")


        ultimo_id_salida = 0

        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT MAX(ID) FROM `salidas`;"""
        cursor.execute(sql)
        
        for index in cursor:             
            if index[0] == None:
                ultimo_id_salida = 0                
            else:
               ultimo_id_salida = index[0] 


        self.label_fecha = CTkLabel(self,text="Fecha:", font=("Times New Roman",16))
        self.label_fecha.place(x = 650, y = 70) 

        self.texto_fecha = CTkEntry(self)
        self.texto_fecha.place(x = 750, y = 70)  

        # ********************* para escoger la fecha ********************
        def seleccionar_fecha():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.texto_fecha.delete(0,END)               
                fecha_select = cal.get_date()
                self.texto_fecha.insert(0,str(fecha_select)) 
                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha = CTkButton(self, text="...",command=seleccionar_fecha, width = 30, height = 27)
        self.btn_seleccionar_fecha.place(x = 900, y = 70)

        self.label_descripcion = CTkLabel(self,text="Descripcion:", font=("Times New Roman",16))
        self.label_descripcion.place(x = 650, y = 130) 

        conceptos_salidas = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `concepto_salidas`;"""
        cursor.execute(sql)
        for index in cursor:
            conceptos_salidas.append(index[0])

        
        self.texto_descripcion = CTkComboBox(self, values = conceptos_salidas)
        self.texto_descripcion.set("")
        self.texto_descripcion.place(x = 750, y = 130) 

        self.label_concepto = CTkLabel(self,text="Concepto:", font=("Times New Roman",16))
        self.label_concepto.place(x = 650, y = 190)  
        
        self.texto_concepto = CTkEntry(self)
        self.texto_concepto.place(x = 750, y = 190) 

        self.label_monto = CTkLabel(self,text="Monto:", font=("Times New Roman",16))
        self.label_monto.place(x = 650, y = 250)  
        
        self.texto_monto = CTkEntry(self)
        self.texto_monto.place(x = 750, y = 250) 

        self.label_moneda = CTkLabel(self,text="Moneda:", font=("Times New Roman",16))
        self.label_moneda.place(x = 650, y = 310)  
        
        monedas = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `monedas`;"""
        cursor.execute(sql)
        for index in cursor:
            monedas.append(index[0])

        
        self.texto_monedas = CTkComboBox(self, values = monedas)
        self.texto_monedas.set("")
        self.texto_monedas.place(x = 750, y = 310)

        def ejecutar_salida():
            confirmar = messagebox.askokcancel("Confirmar", "Confirmar salida")
            if confirmar == True:                        
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()
                
                
                sql = f""" INSERT INTO `salidas`(`Id`, `fecha`, `descripcion`, `concepto`, `monto`, `moneda`) VALUES ('{ultimo_id_salida + 1}','{self.texto_fecha.get()}','{self.texto_descripcion.get()}','{self.texto_concepto.get()}','{self.texto_monto.get()}','{self.texto_monedas.get()}') """
                cursor.execute(sql)
                conn.commit()

                self.destroy()


        def cancelar_salida():            
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=ejecutar_salida, width = 150, height = 40)
        self.btn_aceptar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_salida, width = 150, height = 40)
        self.btn_cancelar.place(x=820 ,y=500 )


# **********************************************************************************
# ********************************** Consultas Salidas Mensual *********************
# **********************************************************************************

class ConsultarSalidaMensual(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Consulta Salida Mensual")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1300x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (1300,700))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        self.tabla = ttk.Treeview(self, columns = ("Fecha","Descripcion","Concepto","Monto","Moneda"))
        self.tabla.column("#0", width = 50)
        self.tabla.column("Fecha", width = 100)
        self.tabla.column("Descripcion", width = 300)
        self.tabla.column("Concepto", width = 300)
        self.tabla.column("Monto", width = 100)
        self.tabla.column("Moneda", width = 100)
        
        self.tabla.place(x = 300, y = 200)
        self.tabla.config(height = 20)
        self.tabla.heading("#0", text = "Id")
        self.tabla.heading("Fecha", text = "Fecha")
        self.tabla.heading("Descripcion", text = "Descripcion")
        self.tabla.heading("Concepto", text = "Concepto")
        self.tabla.heading("Monto", text = "Monto")
        self.tabla.heading("Moneda", text = "Moneda")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)    


        self.labelmes = CTkLabel(self, text="Mes", font=("Times New Roman",16))                
        self.labelmes.place(x = 140, y = 50)
        
        self.mes = CTkEntry(self, width=40)                
        self.mes.place(x = 130, y = 80)

        self.anio = CTkEntry(self,width=80)                
        self.anio.place(x = 180, y = 80)    

        self.label_moneda = CTkLabel(self, text="Moneda")
        self.label_moneda.place(x = 1000 , y = 50)  

               

        monedas = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `monedas`;"""
        cursor.execute(sql)
        for index in cursor:
            monedas.append(index[0])

        
        self.texto_moneda = CTkComboBox(self, values = monedas)
        self.texto_moneda.set("")
        self.texto_moneda.place(x = 1000, y = 80) 

        self.label_total1 = CTkLabel(self, text="Total:", font=("Times New Roman",16))
        self.label_total1.place(x = 1050, y = 400) 

        self.total = StringVar()
        self.total.set("")

        self.label_total = CTkLabel(self, textvariable = self.total, font=("Times New Roman",16))
        self.label_total.place(x = 1050, y = 450)  

        self.mon = StringVar()
        self.mon.set("")

        self.label_moneda = CTkLabel(self, textvariable = self.mon, font=("Times New Roman",16))
        self.label_moneda.place(x = 1250, y = 450)  

        def seleccionar_fecha():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.mes.delete(0,END)
                self.anio.delete(0,END)                                              

                self.mes.insert(0,str(cal.get_date()[5:7])) 
                self.anio.insert(0,str(cal.get_date()[0:4]))                

                calendario.destroy()                                
                

            btn = CTkButton(calendario, text="Seleccionar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha = CTkButton(self, text="Fecha",command=seleccionar_fecha, width = 60, height = 27)
        self.btn_seleccionar_fecha.place(x = 600, y = 70)


        def balance_mensual():

            try:

                self.tabla.delete(*self.tabla.get_children())

                # *********************** hallemos fecha inicial y final *******************************

                anio = int(self.anio.get())
                mes = int(self.mes.get())
                fecha_inicio = str(date(anio,mes,1))

                fecha_final = date(anio,mes,1) 

                if mes == 12:
                    fecha_final = date(anio + 1, 1, 1)
                else:
                    fecha_final = date(anio,mes + 1,1) 

                fecha_final = str(fecha_final)            

                monto_total = 0
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `salidas` WHERE fecha >= "{fecha_inicio}" AND fecha < "{fecha_final}" AND moneda = "{self.texto_moneda.get()}" ORDER BY fecha ASC; """
                cursor.execute(sql) 
                
                for index in cursor:  
                    monto_total += index[4]               
                    self.tabla.insert("",END, text = index[0], values = (str(index[1]),index[2],index[3],str(index[4]),self.texto_moneda.get()))

                self.total.set(str(monto_total))
                self.mon.set(self.texto_moneda.get())
            
            except:
                error = messagebox.showinfo("Error", "Escribe bien los datos para buscar")
        
        
        self.btn_balance = CTkButton(self, text="Balance",command=balance_mensual, width = 600, height = 40)
        self.btn_balance.place(x = 350, y = 520) 

        #**********************************************************************************************************************
        def exportar_excel():
            try:
                rows = []
                for item in self.tabla.get_children():
                    rows.append(self.tabla.item(item)['values'])
                
                df = pd.DataFrame(rows, columns=["Fecha", "Descripcion", "Concepto", "Monto", "Moneda"])                
                df.to_excel(f"D:/MyCurch/Consulta Salidas mes {self.mes.get()} {self.anio.get()}.xlsx", index=False)
                error = messagebox.showinfo("Exportar", "Exportado a Excel")                

            except:
                error = messagebox.showinfo("Error","Algun dato introducido no esta bien y no se puede exportar")

        self.btn_exportar_excel = CTkButton(self, command = exportar_excel, text = "Exportar a Excel", width = 30, height = 40)
        self.btn_exportar_excel.place(x = 1100, y = 620)
        
        #***********************************************************************************************************************


# **********************************************************************************
# ********************************** Consultas Salidas Anual ***********************
# **********************************************************************************

class ConsultarSalidaAnual(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Consulta Salida Anual")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (800,700))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)
        
        self.tabla = ttk.Treeview(self, columns = ("Descripcion","Monto","Moneda"))
        self.tabla.column("#0", width = 50)        
        self.tabla.column("Descripcion", width = 300)        
        self.tabla.column("Monto", width = 150)
        self.tabla.column("Moneda", width = 100)
        
        self.tabla.place(x = 170, y = 200)
        self.tabla.config(height = 20)

        self.tabla.heading("#0", text = "Id")        
        self.tabla.heading("Descripcion", text = "Descripcion")        
        self.tabla.heading("Monto", text = "Monto")
        self.tabla.heading("Moneda", text = "Moneda")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)        
        

        self.label_mensual = CTkLabel(self, text="Año")
        self.label_mensual.place(x = 70 , y = 50)   

        self.label_moneda = CTkLabel(self, text="Moneda")
        self.label_moneda.place(x = 600 , y = 50)          

        self.anual = CTkEntry(self)                
        self.anual.place(x = 70, y = 80)        

        monedas = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `monedas`;"""
        cursor.execute(sql)
        for index in cursor:
            monedas.append(index[0])

        
        self.texto_moneda = CTkComboBox(self, values = monedas)
        self.texto_moneda.set("")
        self.texto_moneda.place(x = 600, y = 80) 

        self.label_total1 = CTkLabel(self, text="Total:", font=("Times New Roman",16))
        self.label_total1.place(x = 650, y = 400) 

        self.total = StringVar()
        self.total.set("")

        self.label_total = CTkLabel(self, textvariable = self.total, font=("Times New Roman",16))
        self.label_total.place(x = 650, y = 450)  

        self.mon = StringVar()
        self.mon.set("")

        self.label_moneda = CTkLabel(self, textvariable = self.mon, font=("Times New Roman",16))
        self.label_moneda.place(x = 750, y = 450)  


        def balance():
            self.tabla.delete(*self.tabla.get_children())

            # ***************** ubicar fecha inicial y final para hacer el recorrido en la base de datos *********************            
            
            try:
                fecha_inicial = str(self.anual.get()) + "-01-01"

                if int(fecha_actual.year) == int(self.anual.get()):
                    fecha = fecha_actual + timedelta(1)              # esto es para que me incluya las entradas de hoy mas adelante
                    fecha_final = str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)
                    

                elif int(fecha_actual.year) > int(self.anual.get()):
                    fecha_final = str(int(self.anual.get())+1)+"-01-01"
                    

                else:
                    error = messagebox.showinfo("Error", "No ha llegado esa fecha todavia")

                
                listado_descripciones = []
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `concepto_salidas` """
                cursor.execute(sql)

                for index in cursor:
                    listado_descripciones.append(index[0])   

                monto_total = 0                         

                for desc in listado_descripciones:                                            
                    monto_local = 0 
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `salidas` WHERE fecha>="{fecha_inicial}" AND fecha<"{fecha_final}" AND moneda = "{self.texto_moneda.get()}" AND descripcion = "{desc}";  """
                    cursor.execute(sql)

                    for index in cursor:
                        monto_local += index[4] 
                        monto_total += index[4]  

                    if monto_local > 0: 
                        self.tabla.insert("",END, text = "", values = (desc,monto_local,self.texto_moneda.get())) 
                    else:
                        pass

                    self.total.set(str(monto_total))
                    self.mon.set(self.texto_moneda.get())

            except:
                error = messagebox.showinfo("Error", "Escribe todos los datos correctamenmte") 

        self.btn_balance = CTkButton(self, text="Balance",command=balance, width = 400, height = 40)
        self.btn_balance.place(x = 200, y = 520)

        #**********************************************************************************************************************
        def exportar_excel():
            try:
                rows = []
                for item in self.tabla.get_children():
                    rows.append(self.tabla.item(item)['values'])
                
                df = pd.DataFrame(rows, columns=["Descripcion", "Monto", "Moneda"])                
                df.to_excel(f"D:/MyCurch/Consulta Salidas año {self.anual.get()}.xlsx", index=False)
                error = messagebox.showinfo("Exportar", "Exportado a Excel")                

            except:
                error = messagebox.showinfo("Error","Algun dato introducido no esta bien y no se puede exportar")

        self.btn_exportar_excel = CTkButton(self, command = exportar_excel, text = "Exportar a Excel", width = 30, height = 40)
        self.btn_exportar_excel.place(x = 650, y = 620)
        
        #***********************************************************************************************************************


# **********************************************************************************
# ********************************** Agregar Hermano *******************************
# **********************************************************************************

class AgregarHermano(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agregar Hermano")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (600,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 700)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        
        ultimo_id = StringVar()
        ultimo_id.set("")

        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT MAX(ID) FROM `personas`;"""
        cursor.execute(sql)
        
        for index in cursor:                
            ultimo_id.set(index[0])

        label_ultimo_id = CTkLabel(self, textvariable = ultimo_id)
        label_ultimo_id.place(x = 650, y = 30) 

        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 738, y = 30) 
        
        self.texto_id = CTkEntry(self)
        self.texto_id.place(x = 800, y = 30) 

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 70)   
        
        self.texto_nombre = CTkEntry(self)
        self.texto_nombre.place(x = 800, y = 70)

        self.label_apellido1 = CTkLabel(self,text="Apellido1:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 704, y = 110)   
        
        self.texto_apellido1 = CTkEntry(self)
        self.texto_apellido1.place(x = 800, y = 110) 

        self.label_apellido2 = CTkLabel(self,text="Apellido2:", font=("Times New Roman",16))
        self.label_apellido2.place(x = 704, y = 150)   
        
        self.texto_apellido2 = CTkEntry(self)
        self.texto_apellido2.place(x = 800, y = 150)   

        self.label_edad = CTkLabel(self,text="Edad:", font=("Times New Roman",16))
        self.label_edad.place(x = 704, y = 190)   
        
        self.texto_edad = CTkEntry(self)
        self.texto_edad.place(x = 800, y = 190)               

        self.label_telefono = CTkLabel(self,text="Telefono:", font=("Times New Roman",16))
        self.label_telefono.place(x = 704, y = 230)   
        
        self.texto_telefono = CTkEntry(self)
        self.texto_telefono.place(x = 800, y = 230)

        self.label_oficio = CTkLabel(self,text="Oficio:", font=("Times New Roman",16))
        self.label_oficio.place(x = 704, y = 270)   
        
        self.texto_oficio = CTkEntry(self)
        self.texto_oficio.place(x = 800, y = 270)

        self.label_diezmo_vencido = CTkLabel(self,text="Diezmo Vencido:", font=("Times New Roman",16))
        self.label_diezmo_vencido.place(x = 685, y = 310)   
        
        self.texto_fecha_diezmo_vencido = CTkEntry(self)
        self.texto_fecha_diezmo_vencido.place(x = 800, y = 310) 

        # ********************* para escoger la fecha de diezmos vencidos ********************
        def seleccionar_fecha_diezmo_vencido():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.texto_fecha_diezmo_vencido.delete(0,END)               
                fecha_select = cal.get_date()
                self.texto_fecha_diezmo_vencido.insert(0,str(fecha_select)) 
                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha_diezmo_vencido = CTkButton(self, text="...",command=seleccionar_fecha_diezmo_vencido, width = 30, height = 27)
        self.btn_seleccionar_fecha_diezmo_vencido.place(x = 950, y = 310)

        self.label_fecha_conversion = CTkLabel(self,text="Fecha Conversion:", font=("Times New Roman",16))
        self.label_fecha_conversion.place(x = 680, y = 350)   
        
        self.texto_fecha_conversion = CTkEntry(self)
        self.texto_fecha_conversion.place(x = 800, y = 350) 

        # ********************* para escoger la fecha conversion ********************
        def seleccionar_fecha_conversion():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.texto_fecha_conversion.delete(0,END)               
                fecha_select = cal.get_date()
                self.texto_fecha_conversion.insert(0,str(fecha_select)) 
                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha_conversion = CTkButton(self, text="...",command=seleccionar_fecha_conversion, width = 30, height = 27)
        self.btn_seleccionar_fecha_conversion.place(x = 950, y = 350)


        self.label_fecha_bautismo = CTkLabel(self,text="Fecha Bautismo:", font=("Times New Roman",16))
        self.label_fecha_bautismo.place(x = 685, y = 390)   
        
        self.texto_fecha_bautismo = CTkEntry(self)
        self.texto_fecha_bautismo.place(x = 800, y = 390) 

        # ********************* para escoger la fecha conversion ********************
        def seleccionar_fecha_bautismo():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.texto_fecha_bautismo.delete(0,END)               
                fecha_select = cal.get_date()
                self.texto_fecha_bautismo.insert(0,str(fecha_select)) 
                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha_conversion = CTkButton(self, text="...",command=seleccionar_fecha_bautismo, width = 30, height = 27)
        self.btn_seleccionar_fecha_conversion.place(x = 950, y = 390)

        bautizado = IntVar()
        bau = "NO"
        self.radio_bautizado= CTkCheckBox(self, variable = bautizado, text="Bautizado")
        self.radio_bautizado.place(x= 650, y=430)

        miembro = IntVar()
        miemb = "NO"
        self.radio_miembro= CTkCheckBox(self, variable = miembro, text="Miembro")
        self.radio_miembro.place(x= 830, y=430)

        sexo = IntVar()        
        self.radio_hombre= CTkRadioButton(self, variable = sexo,value=1, text="Hombre")
        self.radio_hombre.place(x= 650, y=470)
               
        self.radio_mujer= CTkRadioButton(self, variable = sexo,value=2, text="Mujer")
        self.radio_mujer.place(x= 830, y=470)

        self.label_direccion = CTkLabel(self,text="Direccion:", font=("Times New Roman",16))
        self.label_direccion.place(x = 704, y = 510)   
        
        self.texto_direccion = CTkTextbox(self, width=300, height=100)
        self.texto_direccion.place(x = 650, y = 540)

        def confirmar_agregar_hermano():
            confirmar = messagebox.askquestion("Confirmar","¿Deseas agregar este hermano a la base de datos?")
            if confirmar == "yes":
                # ***************** verificar que no se repite el id ***********************
                id_repetido = False
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = """SELECT ID FROM `personas`;"""
                cursor.execute(sql)
                
                

                for index in cursor:        
            
                    if int(self.texto_id.get()) == index[0]:
                        id_repetido = True

                if id_repetido == False: 
                    # *************** verificar que escribieron id y nombre al menos ******************
                    if self.texto_id.get() != "" and self.texto_nombre.get() != "" and self.texto_apellido1.get() != "" and self.texto_apellido2.get() != "":

                        # *********** encontrar la organizacion a la que pertenece a partir de la edad ***************
                        sex = ""              

                        if sexo.get() == 1:
                            sex = "M"                                

                        elif sexo.get() == 2:
                            sex = "F"

                        organ = ""
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()                        
                        
                        sql = f""" SELECT * FROM `organizaciones` """
                        cursor.execute(sql)                        

                        for index in cursor:
                            if int(self.texto_edad.get()) <= index[2] and int(self.texto_edad.get()) >= index[1]:
                                if index[3] == "T":
                                    organ = index[0]
                                else:
                                    if sex == index[3]:
                                        organ = index[0]

                        if bautizado.get() == 1:
                            bau = "SI"
                        elif bautizado.get() == 0:
                            bau = "NO"
                        if miembro.get() == 1:
                            miemb = "SI" 
                        elif miembro.get() == 0:
                            miemb = "NO"                            
                        
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()
                        
                        
                        sql = f""" INSERT INTO `personas`(`Id`, `Nombre`, `Apellido 1`, `Apellido 2`, `Edad`, `Direccion`, `Telefono`, `Bautizado`, `Miembro`, `Organizacion`, `fecha_diezmo_vencido`, `fecha_conversion`, `fecha_bautismo`, `Oficio`) 
                        VALUES ('{self.texto_id.get()}','{self.texto_nombre.get()}','{self.texto_apellido1.get()}','{self.texto_apellido2.get()}','{self.texto_edad.get()}','{self.texto_direccion.get(1.0,END)}','{self.texto_telefono.get()}','{bau}','{miemb}','{organ}','{self.texto_fecha_diezmo_vencido.get()}','{self.texto_fecha_conversion.get()}','{self.texto_fecha_bautismo.get()}','{self.texto_oficio.get()}') """
                        cursor.execute(sql)
                        conn.commit()
                    else:
                        error = messagebox.showinfo("Error","Necesitas escribir al menos el ID, el Nombre y los Apellidos")

                    self.destroy()                   
                        

        self.btn_agregar = CTkButton(self,text="Agregar",command=confirmar_agregar_hermano,height=40,width=200)
        self.btn_agregar.place(x=700,y=640)


# **********************************************************************************
# ********************************** Diezmos ***************************************
# **********************************************************************************

class Diezmos(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Diezmos")
        self.geometry("300x200")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 300
        hventana = 200
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
       

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (300,200))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        

        def retrasos_diezmo():
            consultar_retrasos = ConsultarRetrasosDiezmos()

        def consultas_diezmo():
            consulta_diezmos = ConsultarDiezmos()


        

        self.btn_consultar = CTkButton(self,text="Consultar",command=consultas_diezmo, width = 100 , height = 40)
        self.btn_consultar.place(x = 30 , y = 100 )

        self.btn_retrasos = CTkButton(self,text="Retrasos",command=retrasos_diezmo, width = 100 , height = 40)
        self.btn_retrasos.place(x = 170 , y = 100 )


# **********************************************************************************
# ********************************** Retrasos Diezmos ******************************
# **********************************************************************************

class ConsultarRetrasosDiezmos(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Consulta Retrasos Diezmos")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (800,700))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_fecha = CTkLabel(self, text="Fecha Limite:")
        self.label_fecha.place(x = 70 , y = 50) 

        self.texto_fecha = CTkEntry(self)                
        self.texto_fecha.place(x = 70, y = 80) 

        # ********************* para escoger la fecha ********************
        def seleccionar_fecha():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.texto_fecha.delete(0,END)               
                fecha_select = cal.get_date()
                self.texto_fecha.insert(0,str(fecha_select)) 
                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha = CTkButton(self, text="...",command=seleccionar_fecha, width = 30, height = 27)
        self.btn_seleccionar_fecha.place(x = 210, y = 80)

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo","Telefono","Organizacion","Vencido Hasta"))
        self.tabla.column("#0", width = 50)        
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("Telefono", width = 100) 
        self.tabla.column("Organizacion", width = 200)       
        self.tabla.column("Vencido Hasta", width = 150)        
        
        self.tabla.place(x = 100, y = 200)
        self.tabla.config(height = 20)

        self.tabla.heading("#0", text = "Id")        
        self.tabla.heading("Nombre Completo", text = "Nombre Completo") 
        self.tabla.heading("Telefono", text = "Telefono")
        self.tabla.heading("Organizacion", text = "Organizacion")       
        self.tabla.heading("Vencido Hasta", text = "Vencido Hasta")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set) 

        def buscar_retrasos():
            self.tabla.delete(*self.tabla.get_children())
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT `Id`, `Nombre`, `Apellido 1`, `Apellido 2`, `Telefono`, `Organizacion`, `fecha_diezmo_vencido` 
                FROM `personas` WHERE fecha_diezmo_vencido <= "{self.texto_fecha.get()}"; """
                cursor.execute(sql)

                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1] + " " + index[2] + " " + index[3],index[4],index[5],index[6]))

            except:
                error = messagebox.showinfo("Error","No se pudo buscar")


        self.btn_buscar = CTkButton(self, text="Buscar",command=buscar_retrasos, width = 400, height = 40)
        self.btn_buscar.place(x = 200, y = 520)

        #**********************************************************************************************************************
        def exportar_excel():
            try:
                rows = []
                for item in self.tabla.get_children():
                    rows.append(self.tabla.item(item)['values'])
                
                df = pd.DataFrame(rows, columns=["Nombre Completo", "Telefono", "Organizacion", "Vencido Hasta"])                
                df.to_excel(f"D:/MyCurch/Retrasos Diezmo {fecha_actual} .xlsx", index=False)
                error = messagebox.showinfo("Exportar", "Exportado a Excel")                

            except:
                error = messagebox.showinfo("Error","Algun dato introducido no esta bien y no se puede exportar")

        self.btn_exportar_excel = CTkButton(self, command = exportar_excel, text = "Exportar a Excel", width = 30, height = 40)
        self.btn_exportar_excel.place(x = 650, y = 620)
        
        #***********************************************************************************************************************


# **********************************************************************************
# ********************************** Agregar Diezmos *******************************
# **********************************************************************************

class AgregarDiezmo(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agregar Diezmo")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (600,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 700)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        self.label_sobre = CTkLabel(self,text="Sobre:", font=("Times New Roman",16))
        self.label_sobre.place(x = 738, y = 70) 
        
        self.texto_sobre = CTkEntry(self)
        self.texto_sobre.place(x = 800, y = 70) 

        self.label_fecha = CTkLabel(self,text="Fecha:", font=("Times New Roman",16))
        self.label_fecha.place(x = 738, y = 110) 
        
        self.texto_fecha = CTkEntry(self)
        self.texto_fecha.place(x = 800, y = 110)

        # ********************* para escoger la fecha ********************
        def seleccionar_fecha():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.texto_fecha.delete(0,END)               
                fecha_select = cal.get_date()
                self.texto_fecha.insert(0,str(fecha_select)) 
                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha = CTkButton(self, text="...",command=seleccionar_fecha, width = 30, height = 27)
        self.btn_seleccionar_fecha.place(x = 950, y = 110)         

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 150) 

        nombre = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Nombre` FROM `personas` ORDER by `Nombre`;"""
        cursor.execute(sql)
        for index in cursor:
            nombre.append(index[0])  
        
        self.texto_nombre = CTkComboBox(self, values=nombre)
        self.texto_nombre.set("")
        self.texto_nombre.place(x = 800, y = 150)

        self.label_apellido1 = CTkLabel(self,text="Apellido1:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 704, y = 190) 

        apellido1 = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Apellido 1` FROM `personas` ORDER by `Apellido 1`;"""
        cursor.execute(sql)
        for index in cursor:
            apellido1.append(index[0])   
        
        self.texto_apellido1 = CTkComboBox(self, values=apellido1)
        self.texto_apellido1.set("")
        self.texto_apellido1.place(x = 800, y = 190) 

        self.label_apellido2 = CTkLabel(self,text="Apellido2:", font=("Times New Roman",16))        
        self.label_apellido2.place(x = 704, y = 230)   

        apellido2 = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Apellido 2` FROM `personas` ORDER by `Apellido 2`;"""
        cursor.execute(sql)
        for index in cursor:
            apellido2.append(index[0])
        
        self.texto_apellido2 = CTkComboBox(self,values=apellido2)
        self.texto_apellido2.set("")
        self.texto_apellido2.place(x = 800, y = 230)

        self.label_servicio = CTkLabel(self,text="Servicio:", font=("Times New Roman",16))
        self.label_servicio.place(x = 704, y = 270)   
        
        self.texto_servicio = CTkEntry(self)
        self.texto_servicio.place(x = 800, y = 270)  

        self.label_mes = CTkLabel(self,text="Vencido Hasta:", font=("Times New Roman",16))
        self.label_mes.place(x = 700, y = 310)   
        
        self.texto_fecha_mes_vencido = CTkEntry(self)
        self.texto_fecha_mes_vencido.place(x = 800, y = 310)   

        # ********************* para escoger la fecha ********************
        def seleccionar_fecha_mes_vencido():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.texto_fecha_mes_vencido.delete(0,END)               
                fecha_select = cal.get_date()
                self.texto_fecha_mes_vencido.insert(0,str(fecha_select)) 
                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha_mes_vencido = CTkButton(self, text="...",command=seleccionar_fecha_mes_vencido, width = 30, height = 27)
        self.btn_seleccionar_fecha_mes_vencido.place(x = 950, y = 310)

        self.label_monto = CTkLabel(self,text="Monto:", font=("Times New Roman",16))
        self.label_monto.place(x = 704, y = 350) 

        self.texto_monto = CTkEntry(self)        
        self.texto_monto.place(x = 800, y = 350)

        self.label_monedas = CTkLabel(self,text="Moneda:", font=("Times New Roman",16))
        self.label_monedas.place(x = 704, y = 390) 

        moneda = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `monedas`;"""
        cursor.execute(sql)
        for index in cursor:
            moneda.append(index[0])          
        
        self.texto_monedas = CTkComboBox(self, values = moneda)
        self.texto_monedas.set("")
        self.texto_monedas.place(x = 800, y = 390)  

        def diezmar():
            # *************** buscar el id indicado para la entrada **************
            new_id_entrada = 0
            conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
            cursor = conn.cursor()

            sql = """SELECT MAX(ID) FROM `entradas`;"""
            cursor.execute(sql)
            
            for index in cursor:  
                if index[0] != None:
                    new_id_entrada = index[0]
            new_id_entrada += 1 # aseguro asi que el id sea uno mas de el ulimo que halla              


            # ************************ generar la entrada **********************
            conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
            cursor = conn.cursor()

            sql = f""" INSERT INTO `entradas`(`Id`, `fecha`, `descripcion`, `servicio`, `monto`, `moneda`) 
            VALUES ('{new_id_entrada}','{self.texto_fecha.get()}','Diezmo','{self.texto_servicio.get()}','{self.texto_monto.get()}','{self.texto_monedas.get()}') """
            cursor.execute(sql)
            conn.commit()

            # ************************ generar el diezmo **********************
            # *************** buscar el id indicado para la entrada **************
            new_id_diezmo = 0
            conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
            cursor = conn.cursor()

            sql = """SELECT MAX(ID) FROM `diezmo`;"""
            cursor.execute(sql)
            
            for index in cursor:  
                if index[0] != None:
                    new_id_diezmo = index[0]
            new_id_diezmo += 1 # aseguro asi que el id sea uno mas de el ulimo que halla 

            conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
            cursor = conn.cursor()

            sql = f""" INSERT INTO `diezmo`(`id`, `fecha`, `sobre`, `nombre`, `apellido 1`, `apellido 2`, `fecha_vencido`, `monto`, `moneda`) 
            VALUES ('{new_id_diezmo}','{self.texto_fecha.get()}','{self.texto_sobre.get()}','{self.texto_nombre.get()}','{self.texto_apellido1.get()}','{self.texto_apellido2.get()}','{self.texto_fecha_mes_vencido.get()}','{self.texto_monto.get()}','{self.texto_monedas.get()}') """
            cursor.execute(sql)
            conn.commit()

            # ***************** cambiar fecha vencido en la tabla personas ************
            conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
            cursor = conn.cursor()

            sql = f""" UPDATE `personas` SET `fecha_diezmo_vencido`='{self.texto_fecha_mes_vencido.get()}' 
            WHERE `Nombre`='{self.texto_nombre.get()}' AND `Apellido 1`='{self.texto_apellido1.get()}' AND `Apellido 2`='{self.texto_apellido2.get()}' """
            cursor.execute(sql)
            conn.commit()

            self.destroy()


        self.btn_diezmar = CTkButton(self,text="Diezmar",command=diezmar,height=40,width=200)
        self.btn_diezmar.place(x=700,y=600)

# **********************************************************************************
# ********************************** Consulta Diezmos ******************************
# **********************************************************************************

class ConsultarDiezmos(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Consulta Diezmos")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (800,700))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_fecha = CTkLabel(self, text="Fecha Hasta Hoy:")
        self.label_fecha.place(x = 70 , y = 50) 

        self.texto_fecha = CTkEntry(self)                
        self.texto_fecha.place(x = 70, y = 80) 

        self.label_nombre = CTkLabel(self, text="Nombre:")
        self.label_nombre.place(x = 350 , y = 50) 

        nombre = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Nombre` FROM `personas` ORDER by `Nombre`;"""
        cursor.execute(sql)
        for index in cursor:
            nombre.append(index[0])  
        
        self.texto_nombre = CTkComboBox(self, values=nombre)
        self.texto_nombre.set("")                
        self.texto_nombre.place(x = 350, y = 80) 

        self.label_apellido1 = CTkLabel(self, text="Apellido 1:")
        self.label_apellido1.place(x = 500 , y = 50) 

        apellido1 = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Apellido 1` FROM `personas` ORDER by `Apellido 1`;"""
        cursor.execute(sql)
        for index in cursor:
            apellido1.append(index[0])   
        
        self.texto_apellido1 = CTkComboBox(self, values=apellido1)
        self.texto_apellido1.set("")               
        self.texto_apellido1.place(x = 500, y = 80) 

        self.label_apellido2 = CTkLabel(self, text="Apellido 2:")
        self.label_apellido2.place(x = 650 , y = 50) 

        apellido2 = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Apellido 2` FROM `personas` ORDER by `Apellido 2`;"""
        cursor.execute(sql)
        for index in cursor:
            apellido2.append(index[0])
        
        self.texto_apellido2 = CTkComboBox(self,values=apellido2)
        self.texto_apellido2.set("")               
        self.texto_apellido2.place(x = 650, y = 80)

        # ********************* para escoger la fecha ********************
        def seleccionar_fecha():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.texto_fecha.delete(0,END)               
                fecha_select = cal.get_date()
                self.texto_fecha.insert(0,str(fecha_select)) 
                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha = CTkButton(self, text="...",command=seleccionar_fecha, width = 30, height = 27)
        self.btn_seleccionar_fecha.place(x = 210, y = 80)

        self.tabla = ttk.Treeview(self, columns = ("Sobre","Fecha","Nombre Completo","Monto","Moneda"))
        self.tabla.column("#0", width = 50)
        self.tabla.column("Sobre", width = 50) 
        self.tabla.column("Fecha", width = 100)        
        self.tabla.column("Nombre Completo", width = 300)        
        self.tabla.column("Monto", width = 100)       
        self.tabla.column("Moneda", width = 70)        
        
        self.tabla.place(x = 180, y = 250)
        self.tabla.config(height = 20)

        self.tabla.heading("#0", text = "Id")        
        self.tabla.heading("Sobre", text = "Sobre") 
        self.tabla.heading("Fecha", text = "Fecha") 
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")         
        self.tabla.heading("Monto", text = "Monto")       
        self.tabla.heading("Moneda", text = "Moneda")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set) 

        def buscar_diezmo():
            self.tabla.delete(*self.tabla.get_children())
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT `id`, `fecha`, `sobre`, `nombre`, `apellido 1`, `apellido 2`, `monto`, `moneda` FROM `diezmo` 
                WHERE `fecha` >= "{self.texto_fecha.get()}" AND `nombre` = "{self.texto_nombre.get()}" AND `apellido 1` = "{self.texto_apellido1.get()}" AND `apellido 2` = "{self.texto_apellido2.get()}"; """
                cursor.execute(sql)

                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[2],index[1],index[3] + " " + index[4]+ " " + index[5], index[6],index[7]))

            except:
                error = messagebox.showinfo("Error","No se pudo buscar")


        self.btn_buscar = CTkButton(self, text="Buscar",command=buscar_diezmo, width = 400, height = 40)
        self.btn_buscar.place(x = 200, y = 570)

        #**********************************************************************************************************************
        def exportar_excel():
            try:
                rows = []
                for item in self.tabla.get_children():
                    rows.append(self.tabla.item(item)['values'])
                
                df = pd.DataFrame(rows, columns=["Sobre","Fecha", "Nombre Completo", "Monto", "Moneda"])                
                df.to_excel(f"D:/MyCurch/Consulta Diezmo {self.texto_nombre.get()} {self.texto_apellido1.get()} {self.texto_apellido2.get()} desde {self.texto_fecha.get()} hasta {fecha_actual} .xlsx", index=False)
                error = messagebox.showinfo("Exportar", "Exportado a Excel")                

            except:
                error = messagebox.showinfo("Error","Algun dato introducido no esta bien y no se puede exportar")

        self.btn_exportar_excel = CTkButton(self, command = exportar_excel, text = "Exportar a Excel", width = 30, height = 40)
        self.btn_exportar_excel.place(x = 650, y = 620)
        
        #***********************************************************************************************************************


# **********************************************************************************
# ********************************** Consulta Hermanos *****************************
# **********************************************************************************

class ConsultarHermanos(CTkToplevel):      
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Consulta Hermanos")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (800,700))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)        
        
        opcion = IntVar()

        self.radio_org = CTkRadioButton(self, text="Organizacion:", variable=opcion, value=1)
        self.radio_org.place(x = 70 , y = 50) 

        org = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Nombre` FROM `organizaciones` ORDER by `Nombre`;"""
        cursor.execute(sql)
        for index in cursor:
            org.append(index[0]) 

        self.texto_org = CTkComboBox(self, values=org)   
        self.texto_org.set("")             
        self.texto_org.place(x = 70, y = 80)        

        self.radio_nombre = CTkRadioButton(self, text="Nombre:", variable=opcion, value=2)
        self.radio_nombre.place(x = 350 , y = 50) 

        nombre = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Nombre` FROM `personas` ORDER by `Nombre`;"""
        cursor.execute(sql)
        for index in cursor:
            nombre.append(index[0])  
        
        self.texto_nombre = CTkComboBox(self, values=nombre)
        self.texto_nombre.set("")                
        self.texto_nombre.place(x = 350, y = 80) 

        self.label_apellido1 = CTkLabel(self, text="Apellido 1:")
        self.label_apellido1.place(x = 500 , y = 50) 

        apellido1 = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Apellido 1` FROM `personas` ORDER by `Apellido 1`;"""
        cursor.execute(sql)
        for index in cursor:
            apellido1.append(index[0])   
        
        self.texto_apellido1 = CTkComboBox(self, values=apellido1)
        self.texto_apellido1.set("")               
        self.texto_apellido1.place(x = 500, y = 80) 

        self.label_apellido2 = CTkLabel(self, text="Apellido 2:")
        self.label_apellido2.place(x = 650 , y = 50) 

        apellido2 = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `Apellido 2` FROM `personas` ORDER by `Apellido 2`;"""
        cursor.execute(sql)
        for index in cursor:
            apellido2.append(index[0])
        
        self.texto_apellido2 = CTkComboBox(self,values=apellido2)
        self.texto_apellido2.set("")               
        self.texto_apellido2.place(x = 650, y = 80)

        self.tabla = ttk.Treeview(self, columns = ("Nombre","Apellido 1","Apellido 2"))
        self.tabla.column("#0", width = 50)
        self.tabla.column("Nombre", width = 200) 
        self.tabla.column("Apellido 1", width = 200)        
        self.tabla.column("Apellido 2", width = 200)                
        
        self.tabla.place(x = 180, y = 200)
        self.tabla.config(height = 20)

        self.tabla.heading("#0", text = "Id")        
        self.tabla.heading("Nombre", text = "Nombre") 
        self.tabla.heading("Apellido 1", text = "Apellido 1") 
        self.tabla.heading("Apellido 2", text = "Apellido 2")         
                

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set) 

        def consultar_hemano():
            self.tabla.delete(*self.tabla.get_children())
            if opcion.get() == 1:
                if self.texto_org.get()=="":
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT `Id`, `Nombre`, `Apellido 1`, `Apellido 2` FROM `personas`  """
                    cursor.execute(sql)

                    for index in cursor:
                        self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3]))

                else:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT `Id`, `Nombre`, `Apellido 1`, `Apellido 2` FROM `personas` WHERE `Organizacion` = "{self.texto_org.get()}";  """
                    cursor.execute(sql)

                    for index in cursor:
                        self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3]))                    

            elif opcion.get() == 2:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT `Id`, `Nombre`, `Apellido 1`, `Apellido 2` 
                FROM `personas` WHERE `Nombre` = "{self.texto_nombre.get()}" AND `Apellido 1` = "{self.texto_apellido1.get()}" AND `Apellido 2` = "{self.texto_apellido2.get()}"; """
                cursor.execute(sql)

                for index in cursor:
                    self.tabla.insert("",END, text = index[0], values = (index[1],index[2],index[3]))
            else:
                error = messagebox.showinfo("Error","Escoja una opcion de busqueda")
        
        def seleccionar_indice(event):
            for item in self.tabla.selection():  
                global id_herm                              
                id_herm = copy.deepcopy(str(self.tabla.item(item,"text")))                 
                
                
        self.tabla.bind("<<TreeviewSelect>>", seleccionar_indice)  
        

        def modificar_hermano():
            modificacion = messagebox.askokcancel("Confirmar","¿Desea modificar la informacion del hermano?") 
            if modificacion == True:                
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `personas` WHERE Id = {id_herm}; """
                cursor.execute(sql)

                for index in cursor:
                    global id_hermano
                    id_hermano = index[0]

                    global nombre_hermano
                    nombre_hermano = index[1]

                    global apellido1_hermano
                    apellido1_hermano = index[2]

                    global appellido2_hermano
                    appellido2_hermano = index[3]

                    global edad_hermano
                    edad_hermano = index[4]

                    global organizacion_hermano
                    organizacion_hermano = index[9]

                    global telefono_hermano
                    telefono_hermano = index[6]

                    global vencido_hermano
                    vencido_hermano = index[10]

                    global oficio_hermano
                    oficio_hermano = index[13]

                    global bautizado_hermano

                    if index[7] == "SI":                        
                        bautizado_hermano = 1
                    if index[7] == "NO":                        
                        bautizado_hermano = 0

                    global miembro_hermano

                    if index[8] == "SI":                        
                        miembro_hermano = 1
                    if index[8] == "NO":                        
                        miembro_hermano = 0
                    
                    global direccion_hermano
                    direccion_hermano = index[5]

                    ventana_modificacion = ModificarHermano()                    



        def eliminar_hermano():            
            eliminacion = messagebox.askokcancel("Confirmar","¿Desea eliminar la informacion del hermano?")
            if eliminacion == True: 
                try:               
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `personas` WHERE Id = {id_herm} """
                    cursor.execute(sql)
                    conn.commit()
                    
                except:
                    error = messagebox.showinfo("Error","No se pudo eliminar al hermano")
            


        self.btn_consultar = CTkButton(self, text="Consultar",command=consultar_hemano, width = 400, height = 40)
        self.btn_consultar.place(x = 200, y = 500)

        self.btn_modificar = CTkButton(self, text="Modificar",command=modificar_hermano, height = 40)
        self.btn_modificar.place(x = 100, y = 600)

        self.btn_eliminar = CTkButton(self, text="Eliminar",command=eliminar_hermano, height = 40)
        self.btn_eliminar.place(x = 600, y = 600)

        #**********************************************************************************************************************
        def exportar_excel():
            if opcion.get() == 1:
                try:
                    rows = []
                    for item in self.tabla.get_children():
                        rows.append(self.tabla.item(item)['values'])
                    
                    df = pd.DataFrame(rows, columns=["Nombre", "Apellido 1", "Apellido 2"])                
                    df.to_excel(f"D:/MyCurch/Consulta Hermanos {self.texto_org.get()}.xlsx", index=False)
                    error = messagebox.showinfo("Exportar", "Exportado a Excel")                

                except:
                    error = messagebox.showinfo("Error","Algun dato introducido no esta bien y no se puede exportar")
            else:
                error = messagebox.showinfo("Error","Se va a exportar a Excel cuando la busqueda sea por organizaciones")

        self.btn_exportar_excel = CTkButton(self, command = exportar_excel, text = "Exportar a Excel", width = 30, height = 40)
        self.btn_exportar_excel.place(x = 340, y = 620)
        
        #***********************************************************************************************************************


# **********************************************************************************
# ********************************** Modificar Hermanos ****************************
# **********************************************************************************

class ModificarHermano(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Modificar Hermano")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes hermanos/{id_hermano}.jpg"), size = (600,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 700)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        
        ultimo_id = StringVar()
        ultimo_id.set("")

        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT MAX(ID) FROM `personas`;"""
        cursor.execute(sql)
        
        for index in cursor:                
            ultimo_id.set(index[0])

        label_ultimo_id = CTkLabel(self, textvariable=ultimo_id)
        label_ultimo_id.place(x = 650, y = 30) 

        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 738, y = 30) 
        
        self.texto_id = CTkEntry(self)
        self.texto_id.insert(0,id_hermano)
        self.texto_id.place(x = 800, y = 30) 

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 70)   
        
        self.texto_nombre = CTkEntry(self)
        self.texto_nombre.insert(0,nombre_hermano)
        self.texto_nombre.place(x = 800, y = 70)

        self.label_apellido1 = CTkLabel(self,text="Apellido1:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 704, y = 110)   
        
        self.texto_apellido1 = CTkEntry(self)
        self.texto_apellido1.insert(0,apellido1_hermano)
        self.texto_apellido1.place(x = 800, y = 110) 

        self.label_apellido2 = CTkLabel(self,text="Apellido2:", font=("Times New Roman",16))
        self.label_apellido2.place(x = 704, y = 150)   
        
        self.texto_apellido2 = CTkEntry(self)
        self.texto_apellido2.insert(0,appellido2_hermano)
        self.texto_apellido2.place(x = 800, y = 150)   

        self.label_edad = CTkLabel(self,text="Edad:", font=("Times New Roman",16))
        self.label_edad.place(x = 704, y = 190)   
        
        self.texto_edad = CTkEntry(self)
        self.texto_edad.insert(0,edad_hermano)
        self.texto_edad.place(x = 800, y = 190)   

        self.label_organizacion = CTkLabel(self,text="Organizacion:", font=("Times New Roman",16))
        self.label_organizacion.place(x = 704, y = 230)         
        
        org = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `organizaciones`;"""
        cursor.execute(sql)
        for index in cursor:
            org.append(index[0])                  
        
        self.texto_organizacion = CTkComboBox(self, values = org)
        self.texto_organizacion.set(organizacion_hermano)
        self.texto_organizacion.place(x = 800, y = 230)        

        self.label_telefono = CTkLabel(self,text="Telefono:", font=("Times New Roman",16))
        self.label_telefono.place(x = 704, y = 270)   
        
        self.texto_telefono = CTkEntry(self)
        self.texto_telefono.insert(0,telefono_hermano)
        self.texto_telefono.place(x = 800, y = 270)

        self.label_oficio = CTkLabel(self,text="Oficio:", font=("Times New Roman",16))
        self.label_oficio.place(x = 704, y = 310)   
        
        self.texto_oficio = CTkEntry(self)
        self.texto_oficio.insert(0,oficio_hermano)
        self.texto_oficio.place(x = 800, y = 310)

        self.label_diezmo_vencido = CTkLabel(self,text="Diezmo Vencido:", font=("Times New Roman",16))
        self.label_diezmo_vencido.place(x = 685, y = 350)   
        
        self.texto_fecha = CTkEntry(self)
        self.texto_fecha.insert(0,vencido_hermano)
        self.texto_fecha.place(x = 800, y = 350) 

        # ********************* para escoger la fecha ********************
        def seleccionar_fecha():
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
            calendario.after(200, lambda: calendario.attributes('-topmost', False))

            cal = Calendar(calendario, selectmode = "day", date_pattern="yyyy-mm-dd")
            cal.pack()

            def fecha():
                self.texto_fecha.delete(0,END)               
                fecha_select = cal.get_date()
                self.texto_fecha.insert(0,str(fecha_select)) 
                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()


        self.btn_seleccionar_fecha = CTkButton(self, text="...",command=seleccionar_fecha, width = 30, height = 27)
        self.btn_seleccionar_fecha.place(x = 950, y = 350)

        bautizado = IntVar()
        bautizado.set(bautizado_hermano)
        bau = "NO"
        self.check_bautizado= CTkCheckBox(self, variable = bautizado, text="Bautizado")
        self.check_bautizado.place(x= 650, y=390)

        miembro = IntVar()
        miembro.set(miembro_hermano)
        miemb = "NO"
        self.check_miembro= CTkCheckBox(self, variable = miembro, text="Miembro")
        self.check_miembro.place(x= 830, y=390)

        self.label_direccion = CTkLabel(self,text="Direccion:", font=("Times New Roman",16))
        self.label_direccion.place(x = 704, y = 430)   
        
        self.texto_direccion = CTkTextbox(self, width=300, height=100)
        self.texto_direccion.insert(1.0,direccion_hermano)
        self.texto_direccion.place(x = 650, y = 460)

        def confirmar_modificar_hermano():
            confirmar = messagebox.askokcancel("Confirmar","¿Deseas modificar la informacion de este hermano en la base de datos?")
            if confirmar == True:                
                    # *************** verificar que escribieron id y nombre al menos ******************
                    if self.texto_id.get() != "" and self.texto_nombre.get() != "" and self.texto_apellido1.get() != "" and self.texto_apellido2.get() != "":
                        if bautizado.get() == 1:
                            bau = "SI"
                        elif bautizado.get() == 0:
                            bau = "NO"
                        if miembro.get() == 1:
                            miemb = "SI" 
                        elif miembro.get() == 0:
                            miemb = "NO"                                                  
                        
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()
                        
                        
                        sql = f""" UPDATE `personas` SET `Id`='{self.texto_id.get()}',`Nombre`='{self.texto_nombre.get()}',
                        `Apellido 1`='{self.texto_apellido1.get()}',`Apellido 2`='{self.texto_apellido2.get()}',`Edad`='{self.texto_edad.get()}',
                        `Direccion`='{self.texto_direccion.get(1.0,END)}',`Telefono`='{self.texto_telefono.get()}',`Bautizado`='{bau}',
                        `Miembro`='{miemb}',`Organizacion`='{self.texto_organizacion.get()}',`fecha_diezmo_vencido`='{self.texto_fecha.get()}' 
                        WHERE Id = {id_herm} """
                        cursor.execute(sql)
                        conn.commit()

                        self.destroy()

                    else:
                        error = messagebox.showinfo("Error","Necesitas escribir al menos el ID, el Nombre y los Apellidos")                     


        self.btn_modificar = CTkButton(self,text="Modificar",command=confirmar_modificar_hermano,height=40,width=200)
        self.btn_modificar.place(x=700,y=600)


# **********************************************************************************
# *************************************** ADMON ************************************
# **********************************************************************************

class ADMON(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Administracion")
        self.geometry("500x350")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 500
        hventana = 350
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
       

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (500,350))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)


        def agregar_inventarios():
            agregar_inventario = AgregarInventario()       

        def consultar_inventarios():
            global id_inv
            id_inv = 0
            consultar_inventario = ConsultarInventario()   

        

        self.btn_agregar_inventario = CTkButton(self,text="Agregar Inventario",command=agregar_inventarios, width = 150 , height = 60)
        self.btn_agregar_inventario.place(x = 50 , y = 150 )

        self.btn_anual = CTkButton(self,text="Consultar Inventario",command=consultar_inventarios, width = 150 , height = 60)
        self.btn_anual.place(x = 290 , y = 150 )



# **********************************************************************************
# *************************************** Finanzas *********************************
# **********************************************************************************

class Finanzas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Finanzas")
        self.geometry("500x350")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 500
        hventana = 350
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
       

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (500,350))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)


        def agregar_entrada():
            agregar_entradas = AgregarEntradas()     

        def agregar_diezmo():
            agregar_diezmos = AgregarDiezmo() 
        

        self.btn_agregar_entrada = CTkButton(self,text="Agregar Entrada",command=agregar_entrada, width = 150 , height = 60)
        self.btn_agregar_entrada.place(x = 50 , y = 150 )

        self.btn_anual = CTkButton(self,text="Agregar Diezmo",command=agregar_diezmo, width = 150 , height = 60)
        self.btn_anual.place(x = 290 , y = 150 )


# **********************************************************************************
# *************************************** Tesoreria ********************************
# **********************************************************************************

class Tesoreria(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Tesoreria")
        self.geometry("500x350")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 500
        hventana = 350
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
       

        self.imagen = CTkImage(Image.open("D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (500,350))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_entrada = CTkLabel(self, text="Entradas")
        self.label_entrada.place(x=90,y=50)

        self.label_entrada = CTkLabel(self, text="Diezmos")
        self.label_entrada.place(x=230,y=50)

        self.label_salida = CTkLabel(self, text="Salidas")
        self.label_salida.place(x=400,y=50)            


        def entrada_mensual(): 
            consultar_entrada_mensual = ConsultarEntradaMensual()                

        def entrada_anual():
            consultar_entrada_anual = ConsultarEntradaAnual()           

        def diezmo_consulta():
            consulta_diezmos = ConsultarDiezmos()

        def diezmo_retrasos():
            consultar_retrasos = ConsultarRetrasosDiezmos()           

        def salida_mensual():
            consultar_salida_mensual = ConsultarSalidaMensual()

        def salida_anual():
            consultar_salida_anual = ConsultarSalidaAnual()

        def salida_agregar():
            agregar_salidas = AgregarSalidas()

        
             
        

        self.btn_entrada_mensual = CTkButton(self,text="Consulta Mensual",command=entrada_mensual, width = 100 , height = 40)
        self.btn_entrada_mensual.place(x = 50 , y = 150 )

        self.btn_entrada_anual = CTkButton(self,text="Consulta Anual",command=entrada_anual, width = 100 , height = 40)
        self.btn_entrada_anual.place(x = 50 , y = 200 )

        self.btn_diezmo_consulta = CTkButton(self,text="Consulta Diezmo",command=diezmo_consulta, width = 100 , height = 40)
        self.btn_diezmo_consulta.place(x = 200 , y = 150 )

        self.btn_diezmo_retrasos = CTkButton(self,text="Retrasos Diezmo",command=diezmo_retrasos, width = 100 , height = 40)
        self.btn_diezmo_retrasos.place(x = 200 , y = 200 )

        self.btn_salida_mensual = CTkButton(self,text="Consulta Mensual",command=salida_mensual, width = 100 , height = 40)
        self.btn_salida_mensual.place(x = 360 , y = 150 )

        self.btn_salida_anual = CTkButton(self,text="Consulta Anual",command=salida_anual, width = 100 , height = 40)
        self.btn_salida_anual.place(x = 360 , y = 200 )

        self.btn_salida_agregar = CTkButton(self,text="Agregar",command=salida_agregar, width = 100 , height = 40)
        self.btn_salida_agregar.place(x = 360 , y = 250 )
        


# **********************************************************************************
# ********************************** Directiva  ************************************
# **********************************************************************************

class Directiva(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Directiva")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes directivos/{num_directivo}.jpg"), size = (600,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 700)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (600,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 700)
            self.label_imagen.place(x = 0 , y = 0)

        self.label_id = CTkLabel(self,text="Id:", font=("Times New Roman",16))
        self.label_id.place(x = 650, y = 70) 
        
        self.texto_id = CTkEntry(self)
        self.texto_id.place(x = 750, y = 70) 
        self.texto_id.insert(0,num_directivo)

        self.label_area = CTkLabel(self,text="Area:", font=("Times New Roman",16))
        self.label_area.place(x = 650, y = 110) 
        
        self.texto_area = CTkEntry(self)
        self.texto_area.place(x = 750, y = 110)

        self.label_cargo = CTkLabel(self,text="Cargo:", font=("Times New Roman",16))
        self.label_cargo.place(x = 650, y = 150)   
        
        self.texto_cargo = CTkEntry(self)
        self.texto_cargo.place(x = 750, y = 150)

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 650, y = 190)   
        
        self.texto_nombre = CTkEntry(self)
        self.texto_nombre.place(x = 750, y = 190) 

        self.label_apellido1 = CTkLabel(self,text="Apellido1:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 650, y = 230)   
        
        self.texto_apellido1 = CTkEntry(self)
        self.texto_apellido1.place(x = 750, y = 230)   

        self.label_apellido2 = CTkLabel(self,text="Apellido2:", font=("Times New Roman",16))
        self.label_apellido2.place(x = 650, y = 270)   
        
        self.texto_apellido2 = CTkEntry(self)
        self.texto_apellido2.place(x = 750, y = 270)               

        self.label_edad = CTkLabel(self,text="Edad:", font=("Times New Roman",16))
        self.label_edad.place(x = 650, y = 310)   
        
        self.texto_edad = CTkEntry(self)
        self.texto_edad.place(x = 750, y = 310)

        self.label_telefono = CTkLabel(self,text="Telefono:", font=("Times New Roman",16))
        self.label_telefono.place(x = 650, y = 350)   
        
        self.texto_telefono = CTkEntry(self)
        self.texto_telefono.place(x = 750, y = 350)

        self.label_direccion = CTkLabel(self,text="Direccion:", font=("Times New Roman",16))
        self.label_direccion.place(x = 650, y = 390)   
        
        self.texto_direccion = CTkTextbox(self, width=300, height=100)
        self.texto_direccion.place(x = 650, y = 420)

        # **************************** llenar info solicitada ****************************
        try:
            conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
            cursor = conn.cursor()           
            
            sql = f""" SELECT * FROM `directivos` WHERE Id = {num_directivo}; """
            cursor.execute(sql)

            for index in cursor:                
                self.texto_area.insert(0,index[1])
                self.texto_cargo.insert(0,index[2])
                self.texto_nombre.insert(0,index[3])
                self.texto_apellido1.insert(0,index[4])
                self.texto_apellido2.insert(0,index[5])
                self.texto_edad.insert(0,index[6])
                self.texto_telefono.insert(0,index[7])
                self.texto_direccion.insert(1.0,index[8])            

        except:
            error = messagebox.showinfo("Error","No se encontro la informacion en la base de datos")


        def modificar_directivo():
            confirmar = messagebox.askokcancel("Confirmar","¿Desea modificar la informacion de este directivo?")
            if confirmar == True:
                # ************ ver si ese id esta en la base de datos ***************
                id_esta = False
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()                      
                
                sql = f""" SELECT `Id` FROM `directivos`;  """
                cursor.execute(sql)

                for index in cursor:
                    if index[0] == num_directivo:
                        id_esta = True

                if id_esta:
                    # ************* si esta el id es update *****************
                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                    cursor = conn.cursor()                      
                    
                    sql = f""" UPDATE `directivos` SET 
                    `Id`='{self.texto_id.get()}'
                    ,`area`='{self.texto_area.get()}'
                    ,`cargo`='{self.texto_cargo.get()}'
                    ,`nombre`='{self.texto_nombre.get()}'
                    ,`apellido1`='{self.texto_apellido1.get()}'
                    ,`apellido2`='{self.texto_apellido2.get()}'
                    ,`edad`='{self.texto_edad.get()}'
                    ,`telefono`='{self.texto_telefono.get()}'
                    ,`direccion`='{self.texto_direccion.get(1.0,END)}'
                    WHERE Id = {self.texto_id.get()} """
                    
                    cursor.execute(sql)
                    conn.commit() 

                    self.destroy()



                else:
                    # ************* si el id no esta es insert **************
                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "mychurch",
                    password = "123456",
                    database = "mychurch"
                    )
                    cursor = conn.cursor()                      
                    
                    sql = f""" INSERT INTO `directivos`(`Id`, `area`, `cargo`, `nombre`, `apellido1`, `apellido2`, `edad`, `telefono`, `direccion`) 
                    VALUES ('{self.texto_id.get()}'
                    ,'{self.texto_area.get()}'
                    ,'{self.texto_cargo.get()}'
                    ,'{self.texto_nombre.get()}'
                    ,'{self.texto_apellido1.get()}'
                    ,'{self.texto_apellido2.get()}'
                    ,'{self.texto_edad.get()}'
                    ,'{self.texto_telefono.get()}'
                    ,'{self.texto_direccion.get(1.0,END)}') """
                    cursor.execute(sql)
                    conn.commit() 
                    
                    self.destroy()
            

        self.btn_modificar = CTkButton(self,text="Modificar",command=modificar_directivo,height=40,width=200)
        self.btn_modificar.place(x=700,y=640)



# **********************************************************************************
# ********************************** Control Areas de Trabajo  *********************
# **********************************************************************************

class ControlAreasTrabajo(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Areas de Trabajo")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (600,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 700)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (600,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 700)
            self.label_imagen.place(x = 0 , y = 0)
        
        def liturgia():
            ventana = Liturgia()
        
        self.btn_Liturgia = CTkButton(self,text="Liturgia",command=liturgia,height=40,width=200)
        self.btn_Liturgia.place(x=650,y=70)

        def educacion_cristiana():
            pass
        
        self.btn_ec = CTkButton(self,text="Educacion Cristiana",command=educacion_cristiana,height=40,width=200)
        self.btn_ec.place(x=650,y=130)

        def actividades_laicas():
            pass
        
        self.btn_al = CTkButton(self,text="Actividades Laicas",command=actividades_laicas,height=40,width=200)
        self.btn_al.place(x=650,y=190)

        def evangelismo():
            pass
        
        self.btn_ev = CTkButton(self,text="Evangelismo",command=evangelismo,height=40,width=200)
        self.btn_ev.place(x=650,y=250)


# **********************************************************************************
# ********************************** Organizaciones  *******************************
# **********************************************************************************

class Organizaciones(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Organizaciones")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 2.jpg"), size = (600,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 700)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (600,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 700)
            self.label_imagen.place(x = 0 , y = 0)
        
        
        def lms():
            pass
        
        self.btn_LMS = CTkButton(self,text="LMS",command=lms,height=40,width=200)
        self.btn_LMS.place(x=650,y=70)

        def lmj():
            pass
        
        self.btn_lmj = CTkButton(self,text="LMJ",command=lmj,height=40,width=200)
        self.btn_lmj.place(x=650,y=130)

        def fmaj():
            pass
        
        self.btn_fmaj = CTkButton(self,text="FMAJ",command=fmaj,height=40,width=200)
        self.btn_fmaj.place(x=650,y=190)

        def fmm():
            pass
        
        self.btn_fmm = CTkButton(self,text="FMM",command=fmm,height=40,width=200)
        self.btn_fmm.place(x=650,y=250)

        def fmh():
            pass
        
        self.btn_fmm = CTkButton(self,text="FMH",command=fmh,height=40,width=200)
        self.btn_fmm.place(x=650,y=310)


# **********************************************************************************
# ********************************** Liturgia  *************************************
# **********************************************************************************

class Liturgia(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Liturgia")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes directivos/8.jpg"), size = (200,200))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 200, height = 200)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (200,200))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 200, height = 200)
            self.label_imagen.place(x = 0 , y = 0)

        # **************************************************************************************
        try:                        
            self.imagen2 = CTkImage(Image.open(f"D:/MyCurch/imagenes liturgia/liturgia1.jpg"), size = (220,220))             
        except:
            self.imagen2 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (220,220))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen2, text = "", width = 220, height = 220)
            self.label_imagen2.place(x = 0 , y = 480)

        # **************************************************************************************
        # **************************************************************************************
        try:                        
            self.imagen3 = CTkImage(Image.open(f"D:/MyCurch/imagenes liturgia/liturgia2.jpg"), size = (220,220))             
        except:
            self.imagen3 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (220,220))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen3, text = "", width = 220, height = 220)
            self.label_imagen2.place(x = 220 , y = 480)

        # **************************************************************************************
        # **************************************************************************************
        try:                        
            self.imagen4 = CTkImage(Image.open(f"D:/MyCurch/imagenes liturgia/liturgia3.jpg"), size = (220,220))             
        except:
            self.imagen4 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (220,220))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen3, text = "", width = 220, height = 220)
            self.label_imagen2.place(x = 440 , y = 480)

        # **************************************************************************************
        # **************************************************************************************
        try:                        
            self.imagen5 = CTkImage(Image.open(f"D:/MyCurch/imagenes liturgia/liturgia2.jpg"), size = (220,220))             
        except:
            self.imagen5 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (220,220))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen3, text = "", width = 220, height = 220)
            self.label_imagen2.place(x = 660 , y = 480)

        # **************************************************************************************

        self.label_titulo = CTkLabel(self,text="Lider de Liturgia:", font=("Times New Roman",24))
        self.label_titulo.place(x=250,y=20)

        self.label_nombre1 = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre1.place(x=250,y=100)

        nombre = StringVar()
        num_directivo=8        # el numero de directivo asociado aliturgia es el 8

        conn = mysql.connector.connect(
        host = "localhost",
        user = "mychurch",
        password = "123456",
        database = "mychurch"
        )
        cursor = conn.cursor()

        sql = f""" SELECT `nombre`, `apellido1`, `apellido2` FROM `directivos` WHERE Id = {num_directivo}; """
        cursor.execute(sql)

        for index in cursor:
            nombre.set(index[0]+" "+index[1]+" "+index[2])         

        self.label_nombre2 = CTkLabel(self, textvariable = nombre)
        self.label_nombre2.place(x=320,y=100)

        def refresh():
            conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
            cursor = conn.cursor()

            sql = f""" SELECT `nombre`, `apellido1`, `apellido2` FROM `directivos` WHERE Id = {num_directivo}; """
            cursor.execute(sql)

            for index in cursor:
                nombre.set(index[0]+" "+index[1]+" "+index[2]) 

        self.btn_refresh = CTkButton(self,text="Refresh", command=refresh, width=20)
        self.btn_refresh.place(x=500,y=100)

        def cambiar_nombre():
            global num_directivo
            num_directivo = 8
            ventana = Directiva()

        self.btn_cambiar = CTkButton(self,text="Cambiar Nombre", command=cambiar_nombre)
        self.btn_cambiar.place(x=250,y=140)

        self.label_nombre2 = CTkLabel(self, text="Ministerios:", font=("Times New Roman",18))
        self.label_nombre2.place(x=50,y=250)

        def alabanza():
            ventana = Alabanza()

        self.btn_alabanza = CTkButton(self,text="Alabanza",command=alabanza)
        self.btn_alabanza.place(x=50,y=300)

        def danza():
            ventana = Danza()

        self.btn_danza = CTkButton(self,text="Danza",command=danza)
        self.btn_danza.place(x=50,y=340)

        def teatro():
            ventana = Teatro()

        self.btn_teatro = CTkButton(self,text="Teatro",command=teatro)
        self.btn_teatro.place(x=50,y=380)

        def audio():
            ventana = Audio()

        self.btn_audio = CTkButton(self,text="Audio",command=audio)
        self.btn_audio.place(x=50,y=420)

        self.label_nombre2 = CTkLabel(self, text="Inventario:", font=("Times New Roman",18))
        self.label_nombre2.place(x=300,y=250)

        tabla_inventario = ttk.Treeview(self, columns = ("Nombre","Cantidad","Inmueble","Area","Detalles"))
        tabla_inventario.column("#0", width = 50)
        tabla_inventario.column("Nombre", width = 200)
        tabla_inventario.column("Cantidad", width = 100)
        tabla_inventario.column("Inmueble", width = 100)
        tabla_inventario.column("Area", width = 100)
        tabla_inventario.column("Detalles", width = 200)
        
        tabla_inventario.place(x = 300, y = 350)
        tabla_inventario.config(height = 10)

        tabla_inventario.heading("#0", text = "Id")
        tabla_inventario.heading("Nombre", text = "Nombre")
        tabla_inventario.heading("Cantidad", text = "Cantidad")
        tabla_inventario.heading("Inmueble", text = "Inmueble")
        tabla_inventario.heading("Area", text = "Area")
        tabla_inventario.heading("Detalles", text = "Detalles")

        scrollbar = CTkScrollbar(self, command = tabla_inventario.yview, width = 18)
        scrollbar.place(in_ = tabla_inventario, relheigh = 1, relx = 1)

        tabla_inventario.config(yscrollcommand = scrollbar.set) 

        conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
        cursor = conn.cursor()

        sql = f""" SELECT * FROM `inventario` WHERE Area = "Liturgia" ORDER BY Id ASC; """
        cursor.execute(sql)

        for index in cursor:
            tabla_inventario.insert("",END, text = index[0], values = (index[1],index[2],index[3],index[4],index[5]))

        def doble_click(event):
            for item in tabla_inventario.selection():  
                global id_inv                              
                id_inv = copy.deepcopy(str(tabla_inventario.item(item,"text")))   
                
                confirmar = messagebox.askokcancel("Confirmar", "¿ Desea modificar el inventario ?")

                global str_texto_id_modificar_inventario
                str_texto_id_modificar_inventario = StringVar()

                global str_texto_nombre_modificar_inventario
                str_texto_nombre_modificar_inventario = StringVar()

                global str_texto_cantidad_modificar_inventario
                str_texto_cantidad_modificar_inventario = StringVar() 

                global str_texto_inmueble_modificar_inventario
                str_texto_inmueble_modificar_inventario = StringVar()

                global str_texto_area_modificar_inventario
                str_texto_area_modificar_inventario = StringVar()

                global str_texto_detalles_modificar_inventario
                str_texto_detalles_modificar_inventario = StringVar()

                if confirmar == True:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `inventario` WHERE Id = {id_inv};  """
                    cursor.execute(sql)
                    for index in cursor:
                        str_texto_id_modificar_inventario.set(str(index[0]))
                        str_texto_nombre_modificar_inventario.set(index[1])
                        str_texto_cantidad_modificar_inventario.set(str(index[2]))
                        str_texto_inmueble_modificar_inventario.set(index[3])
                        str_texto_area_modificar_inventario.set(index[4])
                        str_texto_detalles_modificar_inventario.set(index[5])

                    modificando_inventario = ModificarInventario()                 
                
        tabla_inventario.bind("<Double-1>", doble_click)



# **********************************************************************************
# ********************************** Alabanza  *************************************
# **********************************************************************************

class Alabanza(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Alabanza")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes alabanza/lider.jpg"), size = (200,200))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 200, height = 200)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (200,200))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 200, height = 200)
            self.label_imagen.place(x = 0 , y = 0)

        # **************************************************************************************

        try:                        
            self.imagen2 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/alabanza.jpg"), size = (500,500))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen2, text = "", width = 500, height = 500)
            self.label_imagen2.place(x = 500 , y = 200)
        except:
            self.imagen2 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (500,500))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen2, text = "", width = 500, height = 500)
            self.label_imagen2.place(x = 500 , y = 200)

        # ***************************************************************************************

        self.label_titulo = CTkLabel(self,text="Lider de Alabanza:", font=("Times New Roman",24))
        self.label_titulo.place(x=250,y=20)

        self.label_nombre1 = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre1.place(x=250,y=100)

        nombre = StringVar()        

        conn = mysql.connector.connect(
        host = "localhost",
        user = "mychurch",
        password = "123456",
        database = "mychurch"
        )
        cursor = conn.cursor()

        sql = f""" SELECT `integrante` FROM `alabanza` WHERE `puesto`="Lider" """
        cursor.execute(sql)

        for index in cursor:
            nombre.set(index[0])       

        self.label_nombre2 = CTkLabel(self, textvariable = nombre)
        self.label_nombre2.place(x=320,y=100)

        def refresh():
            conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
            cursor = conn.cursor()

            sql = f""" SELECT `integrante` FROM `alabanza` WHERE `puesto`="Lider" """
            cursor.execute(sql)

            for index in cursor:
                nombre.set(index[0])

        self.btn_refresh = CTkButton(self,text="Refresh", command=refresh, width=20)
        self.btn_refresh.place(x=500,y=100)

        tabla_alabanza = ttk.Treeview(self, columns = ("Integrante","Puesto"))
        tabla_alabanza.column("#0", width = 50)
        tabla_alabanza.column("Integrante", width = 300)
        tabla_alabanza.column("Puesto", width = 200)        
        
        tabla_alabanza.place(x = 50, y = 300)
        tabla_alabanza.config(height = 10)

        tabla_alabanza.heading("#0", text = "Id")
        tabla_alabanza.heading("Integrante", text = "Integrante")
        tabla_alabanza.heading("Puesto", text = "Puesto")        

        scrollbar = CTkScrollbar(self, command = tabla_alabanza.yview, width = 18)
        scrollbar.place(in_ = tabla_alabanza, relheigh = 1, relx = 1)

        tabla_alabanza.config(yscrollcommand = scrollbar.set) 

        def seleccionar_indice(event):
            for item in tabla_alabanza.selection():  
                global id_alabanza                              
                id_alabanza = copy.deepcopy(str(tabla_alabanza.item(item,"text")))         
                
                
        tabla_alabanza.bind("<<TreeviewSelect>>", seleccionar_indice)

        # llenar la tabla de los integrantes de la alabanza
        conn = mysql.connector.connect(
        host = "localhost",
        user = "mychurch",
        password = "123456",
        database = "mychurch"
        )
        cursor = conn.cursor()

        sql = f""" SELECT * FROM `alabanza` ORDER BY Id ASC """
        cursor.execute(sql)

        for index in cursor:
            tabla_alabanza.insert("",END, text = index[0], values = (index[1],index[2]))

        # agregar y eliminar integrantes

        self.label_agregar = CTkLabel(self,text="Para Agregar:")
        self.label_agregar.place(x=50,y=440)

        self.entry_id = CTkEntry(self,width=50)
        self.entry_id.place(x=150,y=440)

        self.entry_integrante = CTkEntry(self,width=200)
        self.entry_integrante.place(x=210,y=440)

        self.entry_puesto = CTkEntry(self,width=70)
        self.entry_puesto.place(x=420,y=440)

        def agregar():
            if self.entry_id.get() != "" and self.entry_integrante.get() != "" and self.entry_puesto.get() != "":  
                # controlar que no haya id repetido
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" SELECT `Id` FROM `alabanza`; """
                cursor.execute(sql)

                id_repetido = False

                for index in cursor:                    
                    if int(self.entry_id.get()) == index[0]:
                        id_repetido = True
                        

                if id_repetido:
                    error =  messagebox.showerror("Error","Id repetido")
                        
                else:
                    conf =  messagebox.askokcancel("Confirmacion","Se va a agregar el integrante")
                    if conf == True:
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `alabanza`(`Id`, `integrante`, `puesto`) VALUES ('{self.entry_id.get()}','{self.entry_integrante.get()}','{self.entry_puesto.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # refresh a la tabla 
                        tabla_alabanza.delete(*tabla_alabanza.get_children())
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()

                        sql = f""" SELECT * FROM `alabanza` ORDER BY Id ASC """
                        cursor.execute(sql)

                        for index in cursor:
                            tabla_alabanza.insert("",END, text = index[0], values = (index[1],index[2]))

                        # borrar los campos de agregar
                        self.entry_id.delete(0,END) 
                        self.entry_integrante.delete(0,END) 
                        self.entry_puesto.delete(0,END) 
            else:                
                conf =  messagebox.askokcancel("Error","Escriba la informacion en los campos antes de agregar")

        self.btn_agregar = CTkButton(self, text="Agregar",command=agregar)
        self.btn_agregar.place(x=100,y=480)

        def eliminar():
            conf =  messagebox.askokcancel("Confirmacion","Se va a eliminar el integrante")
            if conf == True:
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" DELETE FROM `alabanza` WHERE id = {id_alabanza} """
                cursor.execute(sql)
                conn.commit()

                # refresh a la tabla alabanza
                tabla_alabanza.delete(*tabla_alabanza.get_children())
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `alabanza` ORDER BY Id ASC """
                cursor.execute(sql)

                for index in cursor:
                    tabla_alabanza.insert("",END, text = index[0], values = (index[1],index[2]))

        self.btn_eliminar = CTkButton(self, text="Eliminar",command=eliminar)
        self.btn_eliminar.place(x=250,y=480)



# **********************************************************************************
# ********************************** Danza  ****************************************
# **********************************************************************************

class Danza(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Danza")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes danza/lider.jpg"), size = (200,200))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 200, height = 200)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (200,200))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 200, height = 200)
            self.label_imagen.place(x = 0 , y = 0)

        # **************************************************************************************

        try:                        
            self.imagen2 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/danza.jpg"), size = (500,500))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen2, text = "", width = 500, height = 500)
            self.label_imagen2.place(x = 500 , y = 200)
        except:
            self.imagen2 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (500,500))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen2, text = "", width = 500, height = 500)
            self.label_imagen2.place(x = 500 , y = 200)

        # ***************************************************************************************

        self.label_titulo = CTkLabel(self,text="Lider del Ministerio de Danza:", font=("Times New Roman",24))
        self.label_titulo.place(x=250,y=20)

        self.label_nombre1 = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre1.place(x=250,y=100)

        nombre = StringVar()        

        conn = mysql.connector.connect(
        host = "localhost",
        user = "mychurch",
        password = "123456",
        database = "mychurch"
        )
        cursor = conn.cursor()

        sql = f""" SELECT `integrante` FROM `danza` WHERE `puesto`="Lider" """
        cursor.execute(sql)

        for index in cursor:
            nombre.set(index[0])       

        self.label_nombre2 = CTkLabel(self, textvariable = nombre)
        self.label_nombre2.place(x=320,y=100)

        def refresh():
            conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
            cursor = conn.cursor()

            sql = f""" SELECT `integrante` FROM `danza` WHERE `puesto`="Lider" """
            cursor.execute(sql)

            for index in cursor:
                nombre.set(index[0])

        self.btn_refresh = CTkButton(self,text="Refresh", command=refresh, width=20)
        self.btn_refresh.place(x=500,y=100)

        tabla_danza = ttk.Treeview(self, columns = ("Integrante","Puesto"))
        tabla_danza.column("#0", width = 50)
        tabla_danza.column("Integrante", width = 300)
        tabla_danza.column("Puesto", width = 200)        
        
        tabla_danza.place(x = 50, y = 300)
        tabla_danza.config(height = 10)

        tabla_danza.heading("#0", text = "Id")
        tabla_danza.heading("Integrante", text = "Integrante")
        tabla_danza.heading("Puesto", text = "Puesto")        

        scrollbar = CTkScrollbar(self, command = tabla_danza.yview, width = 18)
        scrollbar.place(in_ = tabla_danza, relheigh = 1, relx = 1)

        tabla_danza.config(yscrollcommand = scrollbar.set) 

        def seleccionar_indice(event):
            for item in tabla_danza.selection():  
                global id_danza                             
                id_danza = copy.deepcopy(str(tabla_danza.item(item,"text")))         
                
                
        tabla_danza.bind("<<TreeviewSelect>>", seleccionar_indice)

        # llenar la tabla de los integrantes de la alabanza
        conn = mysql.connector.connect(
        host = "localhost",
        user = "mychurch",
        password = "123456",
        database = "mychurch"
        )
        cursor = conn.cursor()

        sql = f""" SELECT * FROM `danza` ORDER BY Id ASC """
        cursor.execute(sql)

        for index in cursor:
            tabla_danza.insert("",END, text = index[0], values = (index[1],index[2]))

        # agregar y eliminar integrantes

        self.label_agregar = CTkLabel(self,text="Para Agregar:")
        self.label_agregar.place(x=50,y=440)

        self.entry_id = CTkEntry(self,width=50)
        self.entry_id.place(x=150,y=440)

        self.entry_integrante = CTkEntry(self,width=200)
        self.entry_integrante.place(x=210,y=440)

        self.entry_puesto = CTkEntry(self,width=70)
        self.entry_puesto.place(x=420,y=440)

        def agregar():
            if self.entry_id.get() != "" and self.entry_integrante.get() != "" and self.entry_puesto.get() != "":  
                # controlar que no haya id repetido
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" SELECT `Id` FROM `danza`; """
                cursor.execute(sql)

                id_repetido = False

                for index in cursor:                    
                    if int(self.entry_id.get()) == index[0]:
                        id_repetido = True
                        

                if id_repetido:
                    error =  messagebox.showerror("Error","Id repetido")
                        
                else:
                    conf =  messagebox.askokcancel("Confirmacion","Se va a agregar el integrante")
                    if conf == True:
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `danza`(`Id`, `integrante`, `puesto`) VALUES ('{self.entry_id.get()}','{self.entry_integrante.get()}','{self.entry_puesto.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # refresh a la tabla 
                        tabla_danza.delete(*tabla_danza.get_children())
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()

                        sql = f""" SELECT * FROM `danza` ORDER BY Id ASC """
                        cursor.execute(sql)

                        for index in cursor:
                            tabla_danza.insert("",END, text = index[0], values = (index[1],index[2]))

                        # borrar los campos de agregar
                        self.entry_id.delete(0,END) 
                        self.entry_integrante.delete(0,END) 
                        self.entry_puesto.delete(0,END) 
            else:                
                conf =  messagebox.askokcancel("Error","Escriba la informacion en los campos antes de agregar")

        self.btn_agregar = CTkButton(self, text="Agregar",command=agregar)
        self.btn_agregar.place(x=100,y=480)

        def eliminar():
            conf =  messagebox.askokcancel("Confirmacion","Se va a eliminar el integrante")
            if conf == True:
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" DELETE FROM `danza` WHERE id = {id_danza} """
                cursor.execute(sql)
                conn.commit()

                # refresh a la tabla alabanza
                tabla_danza.delete(*tabla_danza.get_children())
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `danza` ORDER BY Id ASC """
                cursor.execute(sql)

                for index in cursor:
                    tabla_danza.insert("",END, text = index[0], values = (index[1],index[2]))

        self.btn_eliminar = CTkButton(self, text="Eliminar",command=eliminar)
        self.btn_eliminar.place(x=250,y=480)



# **********************************************************************************
# ********************************** Teatro  ***************************************
# **********************************************************************************

class Teatro(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Teatro")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes teatro/lider.jpg"), size = (200,200))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 200, height = 200)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (200,200))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 200, height = 200)
            self.label_imagen.place(x = 0 , y = 0)

        # **************************************************************************************

        try:                        
            self.imagen2 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/teatro.jpg"), size = (500,500))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen2, text = "", width = 500, height = 500)
            self.label_imagen2.place(x = 500 , y = 200)
        except:
            self.imagen2 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (500,500))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen2, text = "", width = 500, height = 500)
            self.label_imagen2.place(x = 500 , y = 200)

        # ***************************************************************************************

        self.label_titulo = CTkLabel(self,text="Lider del Ministerio de Teatro:", font=("Times New Roman",24))
        self.label_titulo.place(x=250,y=20)

        self.label_nombre1 = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre1.place(x=250,y=100)

        nombre = StringVar()        

        conn = mysql.connector.connect(
        host = "localhost",
        user = "mychurch",
        password = "123456",
        database = "mychurch"
        )
        cursor = conn.cursor()

        sql = f""" SELECT `integrante` FROM `teatro` WHERE `puesto`="Lider" """
        cursor.execute(sql)

        for index in cursor:
            nombre.set(index[0])       

        self.label_nombre2 = CTkLabel(self, textvariable = nombre)
        self.label_nombre2.place(x=320,y=100)

        def refresh():
            conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
            cursor = conn.cursor()

            sql = f""" SELECT `integrante` FROM `teatro` WHERE `puesto`="Lider" """
            cursor.execute(sql)

            for index in cursor:
                nombre.set(index[0])

        self.btn_refresh = CTkButton(self,text="Refresh", command=refresh, width=20)
        self.btn_refresh.place(x=500,y=100)

        tabla_teatro = ttk.Treeview(self, columns = ("Integrante","Puesto"))
        tabla_teatro.column("#0", width = 50)
        tabla_teatro.column("Integrante", width = 300)
        tabla_teatro.column("Puesto", width = 200)        
        
        tabla_teatro.place(x = 50, y = 300)
        tabla_teatro.config(height = 10)

        tabla_teatro.heading("#0", text = "Id")
        tabla_teatro.heading("Integrante", text = "Integrante")
        tabla_teatro.heading("Puesto", text = "Puesto")        

        scrollbar = CTkScrollbar(self, command = tabla_teatro.yview, width = 18)
        scrollbar.place(in_ = tabla_teatro, relheigh = 1, relx = 1)

        tabla_teatro.config(yscrollcommand = scrollbar.set) 

        def seleccionar_indice(event):
            for item in tabla_teatro.selection():  
                global id_danza                             
                id_danza = copy.deepcopy(str(tabla_teatro.item(item,"text")))         
                
                
        tabla_teatro.bind("<<TreeviewSelect>>", seleccionar_indice)

        # llenar la tabla de los integrantes de la alabanza
        conn = mysql.connector.connect(
        host = "localhost",
        user = "mychurch",
        password = "123456",
        database = "mychurch"
        )
        cursor = conn.cursor()

        sql = f""" SELECT * FROM `teatro` ORDER BY Id ASC """
        cursor.execute(sql)

        for index in cursor:
            tabla_teatro.insert("",END, text = index[0], values = (index[1],index[2]))

        # agregar y eliminar integrantes

        self.label_agregar = CTkLabel(self,text="Para Agregar:")
        self.label_agregar.place(x=50,y=440)

        self.entry_id = CTkEntry(self,width=50)
        self.entry_id.place(x=150,y=440)

        self.entry_integrante = CTkEntry(self,width=200)
        self.entry_integrante.place(x=210,y=440)

        self.entry_puesto = CTkEntry(self,width=70)
        self.entry_puesto.place(x=420,y=440)

        def agregar():
            if self.entry_id.get() != "" and self.entry_integrante.get() != "" and self.entry_puesto.get() != "":  
                # controlar que no haya id repetido
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" SELECT `Id` FROM `teatro`; """
                cursor.execute(sql)

                id_repetido = False

                for index in cursor:                    
                    if int(self.entry_id.get()) == index[0]:
                        id_repetido = True
                        

                if id_repetido:
                    error =  messagebox.showerror("Error","Id repetido")
                        
                else:
                    conf =  messagebox.askokcancel("Confirmacion","Se va a agregar el integrante")
                    if conf == True:
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `teatro`(`Id`, `integrante`, `puesto`) VALUES ('{self.entry_id.get()}','{self.entry_integrante.get()}','{self.entry_puesto.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # refresh a la tabla 
                        tabla_teatro.delete(*tabla_teatro.get_children())
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()

                        sql = f""" SELECT * FROM `teatro` ORDER BY Id ASC """
                        cursor.execute(sql)

                        for index in cursor:
                            tabla_teatro.insert("",END, text = index[0], values = (index[1],index[2]))

                        # borrar los campos de agregar
                        self.entry_id.delete(0,END) 
                        self.entry_integrante.delete(0,END) 
                        self.entry_puesto.delete(0,END) 
            else:                
                conf =  messagebox.askokcancel("Error","Escriba la informacion en los campos antes de agregar")

        self.btn_agregar = CTkButton(self, text="Agregar",command=agregar)
        self.btn_agregar.place(x=100,y=480)

        def eliminar():
            conf =  messagebox.askokcancel("Confirmacion","Se va a eliminar el integrante")
            if conf == True:
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" DELETE FROM `teatro` WHERE id = {id_danza} """
                cursor.execute(sql)
                conn.commit()

                # refresh a la tabla alabanza
                tabla_teatro.delete(*tabla_teatro.get_children())
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `teatro` ORDER BY Id ASC """
                cursor.execute(sql)

                for index in cursor:
                    tabla_teatro.insert("",END, text = index[0], values = (index[1],index[2]))

        self.btn_eliminar = CTkButton(self, text="Eliminar",command=eliminar)
        self.btn_eliminar.place(x=250,y=480)


# **********************************************************************************
# ********************************** Audio  ****************************************
# **********************************************************************************

class Audio(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Audio")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/MyCurch/imagenes funcionamiento/church.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes audio/lider.jpg"), size = (200,200))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 200, height = 200)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            self.imagen = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (200,200))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 200, height = 200)
            self.label_imagen.place(x = 0 , y = 0)

        # **************************************************************************************

        try:                        
            self.imagen2 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/audio.jpg"), size = (500,500))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen2, text = "", width = 500, height = 500)
            self.label_imagen2.place(x = 500 , y = 200)
        except:
            self.imagen2 = CTkImage(Image.open(f"D:/MyCurch/imagenes funcionamiento/iglesia 1.jpg"), size = (500,500))      

            self.label_imagen2 = CTkLabel(self, image = self.imagen2, text = "", width = 500, height = 500)
            self.label_imagen2.place(x = 500 , y = 200)

        # ***************************************************************************************

        self.label_titulo = CTkLabel(self,text="Lider del Ministerio del Audio:", font=("Times New Roman",24))
        self.label_titulo.place(x=250,y=20)

        self.label_nombre1 = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre1.place(x=250,y=100)

        nombre = StringVar()        

        conn = mysql.connector.connect(
        host = "localhost",
        user = "mychurch",
        password = "123456",
        database = "mychurch"
        )
        cursor = conn.cursor()

        sql = f""" SELECT `integrante` FROM `audio` WHERE `puesto`="Lider" """
        cursor.execute(sql)

        for index in cursor:
            nombre.set(index[0])       

        self.label_nombre2 = CTkLabel(self, textvariable = nombre)
        self.label_nombre2.place(x=320,y=100)

        def refresh():
            conn = mysql.connector.connect(
            host = "localhost",
            user = "mychurch",
            password = "123456",
            database = "mychurch"
            )
            cursor = conn.cursor()

            sql = f""" SELECT `integrante` FROM `audio` WHERE `puesto`="Lider" """
            cursor.execute(sql)

            for index in cursor:
                nombre.set(index[0])

        self.btn_refresh = CTkButton(self,text="Refresh", command=refresh, width=20)
        self.btn_refresh.place(x=500,y=100)

        tabla_audio = ttk.Treeview(self, columns = ("Integrante","Puesto"))
        tabla_audio.column("#0", width = 50)
        tabla_audio.column("Integrante", width = 300)
        tabla_audio.column("Puesto", width = 200)        
        
        tabla_audio.place(x = 50, y = 300)
        tabla_audio.config(height = 10)

        tabla_audio.heading("#0", text = "Id")
        tabla_audio.heading("Integrante", text = "Integrante")
        tabla_audio.heading("Puesto", text = "Puesto")        

        scrollbar = CTkScrollbar(self, command = tabla_audio.yview, width = 18)
        scrollbar.place(in_ = tabla_audio, relheigh = 1, relx = 1)

        tabla_audio.config(yscrollcommand = scrollbar.set) 

        def seleccionar_indice(event):
            for item in tabla_audio.selection():  
                global id_danza                             
                id_danza = copy.deepcopy(str(tabla_audio.item(item,"text")))         
                
                
        tabla_audio.bind("<<TreeviewSelect>>", seleccionar_indice)

        # llenar la tabla de los integrantes de la alabanza
        conn = mysql.connector.connect(
        host = "localhost",
        user = "mychurch",
        password = "123456",
        database = "mychurch"
        )
        cursor = conn.cursor()

        sql = f""" SELECT * FROM `audio` ORDER BY Id ASC """
        cursor.execute(sql)

        for index in cursor:
            tabla_audio.insert("",END, text = index[0], values = (index[1],index[2]))

        # agregar y eliminar integrantes

        self.label_agregar = CTkLabel(self,text="Para Agregar:")
        self.label_agregar.place(x=50,y=440)

        self.entry_id = CTkEntry(self,width=50)
        self.entry_id.place(x=150,y=440)

        self.entry_integrante = CTkEntry(self,width=200)
        self.entry_integrante.place(x=210,y=440)

        self.entry_puesto = CTkEntry(self,width=70)
        self.entry_puesto.place(x=420,y=440)

        def agregar():
            if self.entry_id.get() != "" and self.entry_integrante.get() != "" and self.entry_puesto.get() != "":  
                # controlar que no haya id repetido
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" SELECT `Id` FROM `audio`; """
                cursor.execute(sql)

                id_repetido = False

                for index in cursor:                    
                    if int(self.entry_id.get()) == index[0]:
                        id_repetido = True
                        

                if id_repetido:
                    error =  messagebox.showerror("Error","Id repetido")
                        
                else:
                    conf =  messagebox.askokcancel("Confirmacion","Se va a agregar el integrante")
                    if conf == True:
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `audio`(`Id`, `integrante`, `puesto`) VALUES ('{self.entry_id.get()}','{self.entry_integrante.get()}','{self.entry_puesto.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        # refresh a la tabla 
                        tabla_audio.delete(*tabla_audio.get_children())
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "mychurch",
                        password = "123456",
                        database = "mychurch"
                        )
                        cursor = conn.cursor()

                        sql = f""" SELECT * FROM `audio` ORDER BY Id ASC """
                        cursor.execute(sql)

                        for index in cursor:
                            tabla_audio.insert("",END, text = index[0], values = (index[1],index[2]))

                        # borrar los campos de agregar
                        self.entry_id.delete(0,END) 
                        self.entry_integrante.delete(0,END) 
                        self.entry_puesto.delete(0,END) 
            else:                
                conf =  messagebox.askokcancel("Error","Escriba la informacion en los campos antes de agregar")

        self.btn_agregar = CTkButton(self, text="Agregar",command=agregar)
        self.btn_agregar.place(x=100,y=480)

        def eliminar():
            conf =  messagebox.askokcancel("Confirmacion","Se va a eliminar el integrante")
            if conf == True:
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" DELETE FROM `audio` WHERE id = {id_danza} """
                cursor.execute(sql)
                conn.commit()

                # refresh a la tabla alabanza
                tabla_audio.delete(*tabla_audio.get_children())
                conn = mysql.connector.connect(
                host = "localhost",
                user = "mychurch",
                password = "123456",
                database = "mychurch"
                )
                cursor = conn.cursor()

                sql = f""" SELECT * FROM `audio` ORDER BY Id ASC """
                cursor.execute(sql)

                for index in cursor:
                    tabla_audio.insert("",END, text = index[0], values = (index[1],index[2]))

        self.btn_eliminar = CTkButton(self, text="Eliminar",command=eliminar)
        self.btn_eliminar.place(x=250,y=480)

        

        

        



















































autenticacion = Autenticacion()
autenticacion.mainloop()