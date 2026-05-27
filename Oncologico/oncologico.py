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
from ttkwidgets.autocomplete import AutocompleteEntry
import copy
from tkcalendar import *
import os

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

########################## conexion con base de datos ###########################
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""    
    )
cursor = conn.cursor()
sql = ""

########################### creando base de datos #################################

try:
    sql = """CREATE DATABASE oncologico CHARACTER SET = utf8mb4 COLLATE utf8mb4_spanish_ci;"""
    cursor.execute(sql)
    conn.commit()    
except:
    pass

######################### creando tabla areas #####################################

try:
    sql = """ CREATE TABLE `oncologico`.`areas` (`nombre` VARCHAR(100) NOT NULL ) ENGINE = InnoDB"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

############################ agregando todas las areas a la tabla areas #####################
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "oncologico"    
    )
cursor = conn.cursor()

admin_existe = False
sql = """SELECT * FROM `areas`"""
cursor.execute(sql)
for index in cursor:
    if index[0] == "admin":
        admin_existe = True
if admin_existe == False:
    sql = """ INSERT INTO `areas` (`nombre`) VALUES ('admin');"""
    cursor.execute(sql)
    conn.commit()

recepcion_existe = False
sql = """SELECT * FROM `areas`"""
cursor.execute(sql)
for index in cursor:
    if index[0] == "Recepcion":
        recepcion_existe = True
if recepcion_existe == False:
    sql = """ INSERT INTO `areas` (`nombre`) VALUES ('Recepcion');"""
    cursor.execute(sql)
    conn.commit()

medico_existe = False
sql = """SELECT * FROM `areas`"""
cursor.execute(sql)
for index in cursor:
    if index[0] == "Medico":
        medico_existe = True
if medico_existe == False:
    sql = """ INSERT INTO `areas` (`nombre`) VALUES ('Medico');"""
    cursor.execute(sql)
    conn.commit()

fisico_medico_existe = False
sql = """SELECT * FROM `areas`"""
cursor.execute(sql)
for index in cursor:
    if index[0] == "Fisico-Medico":
        fisico_medico_existe = True
if fisico_medico_existe == False:
    sql = """ INSERT INTO `areas` (`nombre`) VALUES ('Fisico-Medico');"""
    cursor.execute(sql)
    conn.commit()

tecnologo_existe = False
sql = """SELECT * FROM `areas`"""
cursor.execute(sql)
for index in cursor:
    if index[0] == "Tecnologo":
        tecnologo_existe = True
if tecnologo_existe == False:
    sql = """ INSERT INTO `areas` (`nombre`) VALUES ('Tecnologo');"""
    cursor.execute(sql)
    conn.commit()

############################## creando tabla usuarios #########################

try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "oncologico"    
        )
    cursor = conn.cursor()

    sql = """ CREATE TABLE `oncologico`.`usuarios` (`nombre` VARCHAR(100) NOT NULL , `pass` VARCHAR(100) NOT NULL, `area` VARCHAR(100) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

############################## agregando usuario ysos a usuarios #################
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "oncologico"    
    )
cursor = conn.cursor()

ysos_existe = False
sql = """SELECT * FROM `usuarios`"""
cursor.execute(sql)
for index in cursor:
    if index[0] == "ysos":
        ysos_existe = True
if ysos_existe == False:
    sql = """ INSERT INTO `usuarios`(`nombre`, `pass`, `area`) VALUES ('ysos','123456', 'admin')"""
    cursor.execute(sql)
    conn.commit()

################################ creando tabla licencia #############################
try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "oncologico"    
        )
    cursor = conn.cursor()

    sql = """ CREATE TABLE `oncologico`.`licencia` (`codigo` VARCHAR(100) NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

################################### control datos ###########################

municipios = ["Pinar del Río","Consolación del Sur","Viñales","Guane","Sandino","La Palma","San Luis","Los Palacios","San Juan y Martínez","Mantua","Minas de Matahambre","Ajeno"]
sexo = ["M","F"]
raza = ["Blanca","Negra","Mestiza"]

######################################## crear tabla pacientes #################################
try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "oncologico"    
        )
    cursor = conn.cursor()

    sql = """ CREATE TABLE `oncologico`.`pacientes` (`fecha_registro` DATE NOT NULL , `historia_clinica` VARCHAR(50) NOT NULL , `ci` VARCHAR(50) NOT NULL , `nombre` VARCHAR(50) NOT NULL , `1er_apellido` VARCHAR(50) NOT NULL , `2do_apellido` VARCHAR(50) NOT NULL , `edad` INT NOT NULL , `raza` VARCHAR(50) NOT NULL , `municipio` VARCHAR(50) NOT NULL , `sexo` VARCHAR(10) NOT NULL , `fecha_cons_presc` DATE NOT NULL , `curso` INT NOT NULL , `resumen` TEXT NOT NULL , `localizacion` VARCHAR(50) NOT NULL , `t` VARCHAR(10) NOT NULL , `n` VARCHAR(10) NOT NULL , `m` VARCHAR(10) NOT NULL , `estadio` TEXT NOT NULL , `comentario` TEXT NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

################################## crear tabla dosis #########################################
try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "oncologico"    
        )
    cursor = conn.cursor()

    sql = """ CREATE TABLE `oncologico`.`dosis` (`id` INT NOT NULL, `fecha` DATE NOT NULL , `ci` VARCHAR(50) NOT NULL , `curso` INT NOT NULL , `volumen` VARCHAR(50) NOT NULL , `dosis_x_fraccion` DOUBLE NOT NULL , `fx` INT NOT NULL , `dosis` DOUBLE NOT NULL, `fx_vencidas` INT NOT NULL, `dosis_restante` DOUBLE NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
    
except:
    pass



#####################################################################################
################################### autenticacion ###################################
#####################################################################################
class Autenticacion(CTk):
    
    def __init__(self):
        super().__init__()        
        self.title("Login")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 600
        hventana = 300
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("600x300")
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico')) 

        ############################ usuario #########################
        self.label_usuario = CTkLabel(self, text="Usuario:",font=("Arial",18))  
        self.label_usuario.place(x=100,y=100) 

        string_usuarios = []                  

        self.entry_usuario = CTkComboBox(self, values=string_usuarios ,font=("Arial",18), width=200)
        self.entry_usuario.set("Escoger Usuario")
        self.entry_usuario.place(x=300,y=100)

        ############################## pass ############################
        self.label_pass = CTkLabel(self, text="Password:",font=("Arial",18))  
        self.label_pass.place(x=100,y=140)

        self.entry_pass = CTkEntry(self,font=("Arial",18), show="*", width=200)  
        self.entry_pass.place(x=300,y=140) 

        ################ area ####################################
        self.label_area = CTkLabel(self, text="Area:",font=("Arial",18))  
        self.label_area.place(x=100,y=50) 
        
        string_areas = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"    
            )
        cursor = conn.cursor()
        sql = """SELECT * FROM `areas`; """
        cursor.execute(sql)
        for index in cursor:
            string_areas.append(index[0])

        def asociar_usuario(event):            
            string_usuarios = []
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"    
                )
            cursor = conn.cursor()
            sql = f"""SELECT * FROM `usuarios` WHERE area = '{self.combo_area.get()}';"""
            cursor.execute(sql)
            for index in cursor:
                string_usuarios.append(index[0])
            self.entry_usuario.configure(values=string_usuarios)  

        self.combo_area = CTkComboBox(self, values=string_areas,font=("Arial",18), command=asociar_usuario, width=200) 
        self.combo_area.set("Escoger Area") 
        self.combo_area.place(x=300,y=60)        
        
        def iniciar_autenticacion():
            try:
                usuario_existe = False
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "oncologico"    
                    )
                cursor = conn.cursor()
                sql = """ SELECT * FROM `usuarios` """
                cursor.execute(sql)  
                for index in cursor:
                    ############ verificamos usuario y pass ######
                    if self.entry_usuario.get() == index[0] and self.entry_pass.get() == index[1]:
                        ########################## ahora vamos a trabajar con la licencia ###################
                        usuario_existe = True
                        lic = ""  
                        
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "oncologico"    
                            )
                        cursor = conn.cursor()
                        sql = """SELECT * FROM `licencia` """
                        cursor.execute(sql)
                        for index in cursor:
                            lic = index[0]

                        if lic == "":
                            autenticacion.withdraw()
                            licencia = Licencia()
                        
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

                            if fecha_vencimiento >= fecha_actual:
                                autenticacion.withdraw()                                
                                lobby = Lobby()                           
                            else:
                                autenticacion.withdraw()
                                licencia = Licencia()
                            
                if usuario_existe == False:
                    error = messagebox.showwarning("Error", "Usuario o Contraseña incorrecta")
            except:
                pass                              
                    
        
        self.btn = CTkButton(self,text="Iniciar",command=iniciar_autenticacion,width=200,height=50)
        self.btn.place(x=200,y=220)




#######################################################################################################
################################## licencia ###########################################################
#######################################################################################################

class Licencia(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Licencia")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 600
        hventana = 300
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("600x300")
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.label = CTkLabel(self, text = "Introduzca una licencia nueva", font=("Arial",18))
        self.label.place(x = 180 , y = 20)        

        self.texto = CTkEntry(self, width = 300)
        self.texto.place(x = 150 , y = 80) 

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
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = """SELECT codigo FROM `licencia` """
                    cursor.execute(sql)
                    conn.commit

                    licencia_vacia = True

                    for index in cursor:
                        if index == None:
                            licencia_vacia = True
                        else:
                            licencia_vacia = False

                    

                    if licencia_vacia:
                        sql = f""" INSERT INTO `licencia`(`codigo`) VALUES ('{texto_encriptado}')"""
                        cursor.execute(sql)
                        conn.commit()

                    else:
                                    
                        sql = f""" UPDATE `licencia` SET `codigo` = '{texto_encriptado}'"""
                        cursor.execute(sql)
                        conn.commit()


                    if fecha_vencimiento < fecha_actual:
                        error = messagebox.showinfo("Error", "Licencia Inservible") 
                        
                    else:
                        self.destroy()
                        # pendiente poner todas las opciones de lobby que habran al final dependiendo del area escogida
                        lobby = Lobby()            
                        
                        
                else:
                    error = messagebox.showinfo("Error", "Licencia Inservible. Estas en una pc incorrecta") 
                
            except:
                error = messagebox.showinfo("Error", "Licencia Inservible")
        
        def cancelar_nueva_lic():            
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=codigo_btn_aceptar_nueva_licencia, width = 200 , height = 50)
        self.btn_aceptar.place(x = 80 , y = 160 )

        self.btn_aceptar = CTkButton(self,text="Cancelar",command=cancelar_nueva_lic, width = 200 , height = 50)
        self.btn_aceptar.place(x = 320 , y = 160 )


############################################################################################################
######################################## lobby #############################################################
############################################################################################################

class Lobby(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Lobby")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1300x700")
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))        

        firma = "Vence (" + str(fecha_vencimiento) + ")"
        self.label_ysos = CTkLabel(self, text = firma, font=("Times New Roman",16))
        self.label_ysos.place(x = 1150, y = 650)

        self.menu = Menu(self)
        self.config(menu=self.menu, width="200", height="100")

        def agregar_usuario():
            agus = UsuarioAgregar()

        def eliminar_usuario():
            elus = EliminarUsuario()
        
        usuario_menu = Menu(self.menu, tearoff = 0)
        usuario_menu.add_command(label="Agregar",command=agregar_usuario)
        usuario_menu.add_command(label="Eliminar",command=eliminar_usuario)

        def agregar_nueva_licencia():
            licencia = Licencia()

        licencia_menu = Menu(self.menu, tearoff = 0)
        licencia_menu.add_command(label="Nueva", command = agregar_nueva_licencia)

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

        salir_menu = Menu(self.menu, tearoff = 0)
        salir_menu.add_command(label="Cerrar Cesion", command = cerrar_cesion)
        salir_menu.add_command(label="Cerrar Programa", command = cerrar_programa)

        def registro_lobby():
            rl = Registro()  

        def presc_lobby():
            pr = Prescripcion()    

        def dos_lobby():
            pr = Dosimetria() 

        def trat_lobby():
            pr = Tratamiento()  

        def seg_lobby():
            pr = Seguimiento()  
        
        self.menu.add_cascade(label="Registro", command=registro_lobby) 
        self.menu.add_cascade(label="Prescripcion",command=presc_lobby)  
        self.menu.add_cascade(label="Dosimetria",command=dos_lobby)  
        self.menu.add_cascade(label="Tratamiento",command=trat_lobby) 
        self.menu.add_cascade(label="Seguimiento",command=seg_lobby)
        self.menu.add_cascade(label="Usuarios", menu = usuario_menu)
        self.menu.add_cascade(label="Licencia", menu = licencia_menu)
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
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open('D:/Oncologico/imagenes/image1.jpg'), size = (400,300))                            
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        # *********************** Label ****************************************

        self.label_nombre = CTkLabel(self,text = "Area:", font=("Times New Roman",14))
        self.label_nombre.place(x = 50 , y = 10)
        
        self.label_nombre = CTkLabel(self,text = "Usuario:", font=("Times New Roman",14))
        self.label_nombre.place(x = 50 , y = 50)        

        self.label_pass = CTkLabel(self,text = "Contraseña:", font=("Times New Roman",14))
        self.label_pass.place(x = 50 , y = 90)
        
        self.label_confirmar = CTkLabel(self,text = "Confirmar:", font=("Times New Roman",14))
        self.label_confirmar.place(x = 50 , y = 130)
        
        # *********************** Entry ***************************************
        string_areas_agregar_usuario = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"    
            )
        cursor = conn.cursor()
        sql = f"""SELECT * FROM `areas`;"""
        cursor.execute(sql)
        for index in cursor:
            string_areas_agregar_usuario.append(index[0])

        self.texto_area = CTkComboBox(self, values=string_areas_agregar_usuario)
        self.texto_area.place(x = 200 , y = 15)
        
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
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = f""" INSERT INTO `usuarios`(`nombre`, `pass`, `area`) VALUES ('{self.texto_nombre.get()}','{self.texto_pass.get()}','{self.texto_area.get()}') """
                    cursor.execute(sql)
                    conn.commit()                    
                    
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
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/imagen4.jpg"), size = (400,300))                            
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_nombre = CTkLabel(self,text = "Usuario:", font=("Times New Roman",14))
        self.label_nombre.place(x = 100 , y = 80)
        
        items_usuarios = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"
            )
        cursor = conn.cursor()

        sql = """SELECT `nombre` FROM `usuarios`;"""
        cursor.execute(sql)
        for index in cursor:
            items_usuarios.append(index[0])

        texto_nombre_usuario_eliminar = CTkComboBox(self, values=items_usuarios)
        texto_nombre_usuario_eliminar.place(x = 200 , y = 80)       


        def codigo_btn_eliminar_usuarios_eliminar():
            try:
                if texto_nombre_usuario_eliminar.get() == "ysos":
                        error = messagebox.showinfo("Error", "Ese usuario no puede eliminarse")
                else:
                    cuidado = messagebox.askquestion("Delete","Se borrara el Usuario")
                    if cuidado == "yes":
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "oncologico"
                            )
                        cursor = conn.cursor()
                        sql = f""" DELETE FROM `usuarios` WHERE nombre = '{texto_nombre_usuario_eliminar.get()}' """
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



#########################################################################################################################
###################################################### Registro #########################################################
#########################################################################################################################
class Registro(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Registro")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1200
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1200x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        #*********************************** Seccion buacador

        ############ agregar imagen #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Oncologico/imagenes/Funcionamiento/sin_rostro.jpg"), size = (250,250))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 680, y = 80)          

        ###################################################

        estilos_tablas()

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "HC", "Curso"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("HC", width = 100)
        self.tabla.column("Curso", width = 75)       

        self.tabla.place(x = 850, y = 420)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "CI")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("HC", text = "HC")
        self.tabla.heading("Curso", text = "Curso")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        global ci
        ci = 0

        def on_click(event):
            global ci
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                ci = self.tabla.item(item, "text")                

        self.tabla.bind("<ButtonRelease-1>", on_click)

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()

            if self.texto_buscador_fecha.get() == "":
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%' """

            else:
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `fecha_cons_presc` = "{self.texto_buscador_fecha.get()}" AND (`ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%') """

            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1] + " " + index[2] + " " +index[3], index[4],index[5],))  

        self.label_buscador = CTkLabel(self,text="----------------------- Buscador -----------------------", font=("Times New Roman",24))       
        self.label_buscador.place(x=680,y = 50)     
        
        self.texto_buscador_strig = CTkEntry(self, placeholder_text="Buscador...",width=200)
        self.texto_buscador_strig.place(x = 950, y = 200)
        self.texto_buscador_strig.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_fecha = CTkEntry(self, placeholder_text="Fecha...")
        self.texto_buscador_fecha.place(x = 950, y = 240)

        def fecha_buscador():
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
                self.texto_buscador_fecha.delete(0,END)
                fecha_select = cal.get_date()
                self.texto_buscador_fecha.insert(0,str(fecha_select)) 
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_buscador = CTkButton(self,text="...",command=fecha_buscador, width = 35)
        self.btn_fecha_buscador.place(x=1115 ,y=240 )

        llenar_tabla(True)

        def carpeta():
            if ci == 0:
                error = messagebox.showinfo("No existe","Selecciona un paciente en la tabla")
            else:
                ruta = f"D:/Oncologico/imagenes/Pacientes/{ci}"
                os.startfile(ruta)

        self.btn_carpeta = CTkButton(self,text="Carpeta",command=carpeta,width=100)
        self.btn_carpeta.place(x=1050,y=600)

        #***************************************************************************************

        #********************************** Seccion Pacientes
        self.label_pacientes = CTkLabel(self,text="------------------------- Pacientes -------------------------", font=("Times New Roman",24))       
        self.label_pacientes.place(x=50,y = 50)

        self.texto_ci = CTkEntry(self, placeholder_text="CI...")
        self.texto_ci.place(x = 50, y = 100)

        self.texto_hc = CTkEntry(self, placeholder_text="HC...")
        self.texto_hc.place(x = 50, y = 140)

        self.texto_nombre  = CTkEntry(self, placeholder_text="Nombre...")
        self.texto_nombre.place(x = 50, y = 180)

        self.texto_apellido1 = CTkEntry(self, placeholder_text="Apellido 1...")
        self.texto_apellido1.place(x = 50, y = 220)

        self.texto_apellido2 = CTkEntry(self, placeholder_text="Apellido 2...")
        self.texto_apellido2.place(x = 50, y = 260)

        self.texto_edad = CTkEntry(self, placeholder_text="Edad...")
        self.texto_edad.place(x = 50, y = 300)        

        self.texto_raza = CTkComboBox(self, values=raza)
        self.texto_raza.place(x = 50, y = 340)
        self.texto_raza.set("Raza...")        

        self.texto_sexo = CTkComboBox(self, values=sexo)
        self.texto_sexo.place(x = 50, y = 380)
        self.texto_sexo.set("Sexo...")

        self.texto_municipios = CTkComboBox(self, values=municipios)
        self.texto_municipios.place(x = 50, y = 420)
        self.texto_municipios.set("Municipios...")

        self.texto_curso = CTkEntry(self, placeholder_text="Curso...")
        self.texto_curso.place(x = 50, y = 460)         

        self.texto_presc = CTkEntry(self, placeholder_text="Fecha Presc...")
        self.texto_presc.place(x = 50, y = 500) 

        def fecha_presc():
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
                self.texto_presc.delete(0,END)
                fecha_select = cal.get_date()
                self.texto_presc.insert(0,str(fecha_select))                 
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_presc = CTkButton(self,text="...",command=fecha_presc, width = 35)
        self.btn_fecha_presc.place(x=200 ,y=500 )

        def crear():
            conf = messagebox.askokcancel("Confirmar","Se va a agregar el paciente")
            if conf:
                if self.texto_municipios.get() == "Municipios..." or self.texto_presc.get() == "" or self.texto_curso.get() == "" or self.texto_sexo.get() == "Sexo..." or self.texto_raza.get() == "Raza..." or self.texto_edad.get() == "" or self.texto_apellido2.get() == "" or self.texto_apellido1.get() == "" or self.texto_nombre.get() == "" or self.texto_hc.get() == "" or self.texto_ci.get() == "":
                    error = messagebox.showinfo("Error", "Debes escribir en todos los campos antes de agregar el paciente")

                else:
                    # veamos que no este repetido el ci
                    repetido = False
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT COUNT(`ci`) FROM `pacientes` WHERE `ci` = "{self.texto_ci.get()}" """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == 0:
                            pass

                        else:
                            repetido = True


                    if repetido:
                        error = messagebox.showerror("Error","Esta repetido el CI \n Ya debe haber agregado este paciente en otra ocasión")

                    else:
                        # si todo esta bien se agregara a la bd 
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "oncologico"
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `pacientes`(`fecha_registro`, `historia_clinica`, `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `edad`, `raza`, `municipio`, `sexo`, `fecha_cons_presc`, `curso`, `resumen`, `localizacion`, `t`, `n`, `m`, `estadio`, `comentario`, `estado`) VALUES ('{fecha_actual}','{self.texto_hc.get()}','{self.texto_ci.get()}','{self.texto_nombre.get()}','{self.texto_apellido1.get()}','{self.texto_apellido2.get()}','{self.texto_edad.get()}','{self.texto_raza.get()}','{self.texto_municipios.get()}','{self.texto_sexo.get()}','{self.texto_presc.get()}','{self.texto_curso.get()}','-','-','-','-','-','-','-','abierto') """
                        cursor.execute(sql)
                        conn.commit()

                        # crear la carpeta para la foto
                        ruta_completa = f"D:/Oncologico/imagenes/Pacientes/{self.texto_ci.get()}"
                        os.makedirs(ruta_completa, exist_ok=True)

                        #actualizar la tabla y campos
                        llenar_tabla(True)
                        self.texto_hc.delete(0,END)
                        self.texto_ci.delete(0,END)
                        self.texto_nombre.delete(0,END)
                        self.texto_apellido1.delete(0,END)
                        self.texto_apellido2.delete(0,END)
                        self.texto_edad.delete(0,END)
                        self.texto_raza.set("Raza...")
                        self.texto_municipios.set("Municipios...")
                        self.texto_sexo.set("Sexo...")
                        self.texto_presc.delete(0,END)
                        self.texto_curso.delete(0,END)

                        

        self.btn_crear = CTkButton(self, text="Crear",command=crear)
        self.btn_crear.place(x=50,y=600)

        # ahora vamos a mostrar la info del paciente al dar doble click
        def doble_click(event):
            # 1ro tomar el ci del paciente
            global ci
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                ci = self.tabla.item(item, "text")  

            # ahora borramos los campos
            self.texto_hc.delete(0,END)
            self.texto_ci.delete(0,END)
            self.texto_nombre.delete(0,END)
            self.texto_apellido1.delete(0,END)
            self.texto_apellido2.delete(0,END)
            self.texto_edad.delete(0,END)
            self.texto_raza.set("")
            self.texto_municipios.set("")
            self.texto_sexo.set("")
            self.texto_presc.delete(0,END)
            self.texto_curso.delete(0,END)

            # ahora mostramos la info 
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM `pacientes` WHERE `ci` = "{ci}" """
            cursor.execute(sql)
            for index in cursor:
                self.texto_hc.insert(0,index[1])
                self.texto_ci.insert(0,index[2])
                self.texto_nombre.insert(0,index[3])
                self.texto_apellido1.insert(0,index[4])
                self.texto_apellido2.insert(0,index[5])
                self.texto_edad.insert(0,index[6])
                self.texto_raza.set(index[7])
                self.texto_municipios.set(index[8])
                self.texto_sexo.set(index[9])
                self.texto_presc.insert(0,index[10])
                self.texto_curso.insert(0,index[11])

            # ahora mostremos la foto
            try:
                string = f"D:/Oncologico/imagenes/Pacientes/{ci}/foto.jpg"                    
                self.imagen = CTkImage(Image.open(string), size = (250,250))   

                self.label_image = CTkLabel(self, image = self.imagen, text = "")
                self.label_image.place(x = 680, y = 80) 
            except:
                string = f"D:/Oncologico/imagenes/Funcionamiento/sin_rostro.jpg"                    
                self.imagen = CTkImage(Image.open(string), size = (250,250))   

                self.label_image = CTkLabel(self, image = self.imagen, text = "")
                self.label_image.place(x = 680, y = 80) 

        self.tabla.bind("<Double-1>", doble_click)

        def modificar():
            conf = messagebox.askokcancel("Confirmar","Se va a modificar el paciente")
            if conf:
                if self.texto_municipios.get() == "Municipios..." or self.texto_presc.get() == "" or self.texto_curso.get() == "" or self.texto_sexo.get() == "Sexo..." or self.texto_raza.get() == "Raza..." or self.texto_edad.get() == "" or self.texto_apellido2.get() == "" or self.texto_apellido1.get() == "" or self.texto_nombre.get() == "" or self.texto_hc.get() == "" or self.texto_ci.get() == "":
                    error = messagebox.showinfo("Error", "Algun campo no esta correcto")

                else:                    
                    # si todo esta bien se agregara a la bd 
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()                    

                    sql = f""" UPDATE `pacientes` SET `historia_clinica`='{self.texto_hc.get()}',`ci`='{self.texto_ci.get()}',`nombre`='{self.texto_nombre.get()}',`1er_apellido`='{self.texto_apellido1.get()}',`2do_apellido`='{self.texto_apellido2.get()}',`edad`='{self.texto_edad.get()}',`raza`='{self.texto_raza.get()}',`municipio`='{self.texto_municipios.get()}',`sexo`='{self.texto_sexo.get()}',`fecha_cons_presc`='{self.texto_presc.get()}',`curso`='{self.texto_curso.get()}' WHERE `ci` = {ci} """
                    cursor.execute(sql)
                    conn.commit()

                    #actualizar la tabla y campos
                    llenar_tabla(True)
                    self.texto_hc.delete(0,END)
                    self.texto_ci.delete(0,END)
                    self.texto_nombre.delete(0,END)
                    self.texto_apellido1.delete(0,END)
                    self.texto_apellido2.delete(0,END)
                    self.texto_edad.delete(0,END)
                    self.texto_raza.set("Raza...")
                    self.texto_municipios.set("Municipios...")
                    self.texto_sexo.set("Sexo...")
                    self.texto_presc.delete(0,END)
                    self.texto_curso.delete(0,END)

        self.btn_modificar = CTkButton(self, text="Modificar",command=modificar)
        self.btn_modificar.place(x=400,y=600)





#########################################################################################################################
###################################################### Prescripcion #########################################################
#########################################################################################################################
class Prescripcion(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Prescripcion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1200
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1200x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        #*********************************** Seccion buacador

        ############ agregar imagen #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Oncologico/imagenes/Funcionamiento/sin_rostro.jpg"), size = (250,250))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 680, y = 80)          

        ###################################################

        estilos_tablas()

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "HC", "Curso"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("HC", width = 100)
        self.tabla.column("Curso", width = 75)       

        self.tabla.place(x = 850, y = 420)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "CI")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("HC", text = "HC")
        self.tabla.heading("Curso", text = "Curso")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        global ci
        ci = 0

        def on_click(event):
            global ci
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                ci = self.tabla.item(item, "text")                

        self.tabla.bind("<ButtonRelease-1>", on_click)

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()

            if self.texto_buscador_fecha.get() == "":
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%' """

            else:
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `fecha_cons_presc` = "{self.texto_buscador_fecha.get()}" AND (`ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%') """

            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1] + " " + index[2] + " " +index[3], index[4],index[5],))  

        self.label_buscador = CTkLabel(self,text="----------------------- Buscador -----------------------", font=("Times New Roman",24))       
        self.label_buscador.place(x=680,y = 50)     
        
        self.texto_buscador_strig = CTkEntry(self, placeholder_text="Buscador...",width=200)
        self.texto_buscador_strig.place(x = 950, y = 200)
        self.texto_buscador_strig.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_fecha = CTkEntry(self, placeholder_text="Fecha...")
        self.texto_buscador_fecha.place(x = 950, y = 240)

        def fecha_buscador():
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
                self.texto_buscador_fecha.delete(0,END)
                fecha_select = cal.get_date()
                self.texto_buscador_fecha.insert(0,str(fecha_select)) 
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_buscador = CTkButton(self,text="...",command=fecha_buscador, width = 35)
        self.btn_fecha_buscador.place(x=1115 ,y=240 )

        llenar_tabla(True)

        def carpeta():
            if ci == 0:
                error = messagebox.showinfo("No existe","Selecciona un paciente en la tabla")
            else:
                ruta = f"D:/Oncologico/imagenes/Pacientes/{ci}"
                os.startfile(ruta)

        self.btn_carpeta = CTkButton(self,text="Carpeta",command=carpeta,width=100)
        self.btn_carpeta.place(x=1050,y=600)

        #***************************************************************************************

        #********************************** Seccion Prescripcion
        self.label_pacientes = CTkLabel(self,text="------------------------- Prescripcion -------------------------", font=("Times New Roman",24))       
        self.label_pacientes.place(x=50,y = 50)

        self.texto_localizacion = CTkEntry(self, placeholder_text="Localizacion...")
        self.texto_localizacion.place(x = 50, y = 100)

        self.texto_t = CTkEntry(self, placeholder_text="T...",width=75)
        self.texto_t.place(x = 50, y = 140)

        self.texto_n = CTkEntry(self, placeholder_text="N...",width=75)
        self.texto_n.place(x = 130, y = 140)

        self.texto_m = CTkEntry(self, placeholder_text="M...",width=75)
        self.texto_m.place(x = 210, y = 140)

        self.texto_estadio  = CTkEntry(self, placeholder_text="Estadio...")
        self.texto_estadio.place(x = 50, y = 180)

        self.texto_resumen = CTkTextbox(self,width=400,height=150)
        self.texto_resumen.insert("0.0","Resumen...")
        self.texto_resumen.place(x = 50, y = 220)

        self.texto_comentario = CTkTextbox(self,width=400,height=150)
        self.texto_comentario.insert("0.0","Comentario...")
        self.texto_comentario.place(x = 50, y = 400)

        # ahora vamos a mostrar la info del paciente al dar doble click
        def doble_click(event):
            # 1ro tomar el ci del paciente
            global ci
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                ci = self.tabla.item(item, "text")             

            # ahora mostramos la info 
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()

            sql = f""" SELECT * FROM `pacientes` WHERE `ci` = "{ci}" """
            cursor.execute(sql)
            for index in cursor:
                if index[13] == "-" or index[14] == "-" or index[15] == "-" or index[16] == "-" or index[17] == "-" or index[12] == "-" or index[18] == "-":
                    pass
                else:
                    # ahora borramos los campos
                    self.texto_localizacion.delete(0,END)
                    self.texto_t.delete(0,END)
                    self.texto_n.delete(0,END)
                    self.texto_m.delete(0,END)
                    self.texto_estadio.delete(0,END)
                    self.texto_resumen.delete("0.0",END)
                    self.texto_comentario.delete("0.0",END)

                    self.texto_localizacion.insert(0,index[13])
                    self.texto_t.insert(0,index[14])
                    self.texto_n.insert(0,index[15])
                    self.texto_m.insert(0,index[16])
                    self.texto_estadio.insert(0,index[17])
                    self.texto_resumen.insert("0.0",index[12])
                    self.texto_comentario.insert("0.0",index[18])

            # ahora mostremos la foto
            try:
                string = f"D:/Oncologico/imagenes/Pacientes/{ci}/foto.jpg"                    
                self.imagen = CTkImage(Image.open(string), size = (250,250))   

                self.label_image = CTkLabel(self, image = self.imagen, text = "")
                self.label_image.place(x = 680, y = 80) 
            except:
                string = f"D:/Oncologico/imagenes/Funcionamiento/sin_rostro.jpg"                    
                self.imagen = CTkImage(Image.open(string), size = (250,250))   

                self.label_image = CTkLabel(self, image = self.imagen, text = "")
                self.label_image.place(x = 680, y = 80) 

        self.tabla.bind("<Double-1>", doble_click)

        def presc():
            pass

        self.btn_prescripcion = CTkButton(self,text="Prescribir")
        self.btn_prescripcion.place(x=50,y=600)

        
        

        

        

#########################################################################################################################
###################################################### Dosimetria #######################################################
#########################################################################################################################
class Dosimetria(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Dosimetria")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1200
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1200x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        #*********************************** Seccion buacador

        ############ agregar imagen #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Oncologico/imagenes/Funcionamiento/sin_rostro.jpg"), size = (250,250))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 680, y = 80)          

        ###################################################

        estilos_tablas()

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "HC", "Curso"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("HC", width = 100)
        self.tabla.column("Curso", width = 75)       

        self.tabla.place(x = 850, y = 420)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "CI")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("HC", text = "HC")
        self.tabla.heading("Curso", text = "Curso")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        global ci
        ci = 0

        def on_click(event):
            global ci
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                ci = self.tabla.item(item, "text")                

        self.tabla.bind("<ButtonRelease-1>", on_click)

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()

            if self.texto_buscador_fecha.get() == "":
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%' """

            else:
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `fecha_cons_presc` = "{self.texto_buscador_fecha.get()}" AND (`ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%') """

            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1] + " " + index[2] + " " +index[3], index[4],index[5],))  

        self.label_buscador = CTkLabel(self,text="----------------------- Buscador -----------------------", font=("Times New Roman",24))       
        self.label_buscador.place(x=680,y = 50)     
        
        self.texto_buscador_strig = CTkEntry(self, placeholder_text="Buscador...",width=200)
        self.texto_buscador_strig.place(x = 950, y = 200)
        self.texto_buscador_strig.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_fecha = CTkEntry(self, placeholder_text="Fecha...")
        self.texto_buscador_fecha.place(x = 950, y = 240)

        def fecha_buscador():
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
                self.texto_buscador_fecha.delete(0,END)
                fecha_select = cal.get_date()
                self.texto_buscador_fecha.insert(0,str(fecha_select)) 
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_buscador = CTkButton(self,text="...",command=fecha_buscador, width = 35)
        self.btn_fecha_buscador.place(x=1115 ,y=240 )

        llenar_tabla(True)

        def carpeta():
            if ci == 0:
                error = messagebox.showinfo("No existe","Selecciona un paciente en la tabla")
            else:
                ruta = f"D:/Oncologico/imagenes/Pacientes/{ci}"
                os.startfile(ruta)

        self.btn_carpeta = CTkButton(self,text="Carpeta",command=carpeta,width=100)
        self.btn_carpeta.place(x=1050,y=600)

        #***************************************************************************************

        












#########################################################################################################################
###################################################### Tratamiento ######################################################
#########################################################################################################################
class Tratamiento(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Tratamiento")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1200
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1200x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        #*********************************** Seccion buacador

        ############ agregar imagen #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Oncologico/imagenes/Funcionamiento/sin_rostro.jpg"), size = (250,250))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 680, y = 80)          

        ###################################################

        estilos_tablas()

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "HC", "Curso"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("HC", width = 100)
        self.tabla.column("Curso", width = 75)       

        self.tabla.place(x = 850, y = 420)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "CI")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("HC", text = "HC")
        self.tabla.heading("Curso", text = "Curso")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        global ci
        ci = 0

        def on_click(event):
            global ci
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                ci = self.tabla.item(item, "text")                

        self.tabla.bind("<ButtonRelease-1>", on_click)

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()

            if self.texto_buscador_fecha.get() == "":
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%' """

            else:
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `fecha_cons_presc` = "{self.texto_buscador_fecha.get()}" AND (`ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%') """

            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1] + " " + index[2] + " " +index[3], index[4],index[5],))  

        self.label_buscador = CTkLabel(self,text="----------------------- Buscador -----------------------", font=("Times New Roman",24))       
        self.label_buscador.place(x=680,y = 50)     
        
        self.texto_buscador_strig = CTkEntry(self, placeholder_text="Buscador...",width=200)
        self.texto_buscador_strig.place(x = 950, y = 200)
        self.texto_buscador_strig.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_fecha = CTkEntry(self, placeholder_text="Fecha...")
        self.texto_buscador_fecha.place(x = 950, y = 240)

        def fecha_buscador():
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
                self.texto_buscador_fecha.delete(0,END)
                fecha_select = cal.get_date()
                self.texto_buscador_fecha.insert(0,str(fecha_select)) 
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_buscador = CTkButton(self,text="...",command=fecha_buscador, width = 35)
        self.btn_fecha_buscador.place(x=1115 ,y=240 )

        llenar_tabla(True)

        def carpeta():
            if ci == 0:
                error = messagebox.showinfo("No existe","Selecciona un paciente en la tabla")
            else:
                ruta = f"D:/Oncologico/imagenes/Pacientes/{ci}"
                os.startfile(ruta)

        self.btn_carpeta = CTkButton(self,text="Carpeta",command=carpeta,width=100)
        self.btn_carpeta.place(x=1050,y=600)

        #***************************************************************************************














#########################################################################################################################
###################################################### Seguimiento ######################################################
#########################################################################################################################
class Seguimiento(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Seguimiento")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1200
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1200x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        #*********************************** Seccion buacador

        ############ agregar imagen #########
      
        self.imagen = CTkImage (light_image = Image.open("D:/Oncologico/imagenes/Funcionamiento/sin_rostro.jpg"), size = (250,250))  

        self.label_image = CTkLabel(self, image = self.imagen, text = "")  
        self.label_image.place(x = 680, y = 80)          

        ###################################################

        estilos_tablas()

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "HC", "Curso"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("HC", width = 100)
        self.tabla.column("Curso", width = 75)       

        self.tabla.place(x = 850, y = 420)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "CI")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("HC", text = "HC")
        self.tabla.heading("Curso", text = "Curso")        

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        global ci
        ci = 0

        def on_click(event):
            global ci
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                ci = self.tabla.item(item, "text")                

        self.tabla.bind("<ButtonRelease-1>", on_click)

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()

            if self.texto_buscador_fecha.get() == "":
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%' """

            else:
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `fecha_cons_presc` = "{self.texto_buscador_fecha.get()}" AND (`ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%') """

            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1] + " " + index[2] + " " +index[3], index[4],index[5],))  

        self.label_buscador = CTkLabel(self,text="----------------------- Buscador -----------------------", font=("Times New Roman",24))       
        self.label_buscador.place(x=680,y = 50)     
        
        self.texto_buscador_strig = CTkEntry(self, placeholder_text="Buscador...",width=200)
        self.texto_buscador_strig.place(x = 950, y = 200)
        self.texto_buscador_strig.bind("<KeyRelease>", llenar_tabla) 

        self.texto_buscador_fecha = CTkEntry(self, placeholder_text="Fecha...")
        self.texto_buscador_fecha.place(x = 950, y = 240)

        def fecha_buscador():
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
                self.texto_buscador_fecha.delete(0,END)
                fecha_select = cal.get_date()
                self.texto_buscador_fecha.insert(0,str(fecha_select)) 
                llenar_tabla(True)
                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 


        self.btn_fecha_buscador = CTkButton(self,text="...",command=fecha_buscador, width = 35)
        self.btn_fecha_buscador.place(x=1115 ,y=240 )

        llenar_tabla(True)

        def carpeta():
            if ci == 0:
                error = messagebox.showinfo("No existe","Selecciona un paciente en la tabla")
            else:
                ruta = f"D:/Oncologico/imagenes/Pacientes/{ci}"
                os.startfile(ruta)

        self.btn_carpeta = CTkButton(self,text="Carpeta",command=carpeta,width=100)
        self.btn_carpeta.place(x=1050,y=600)

        #***************************************************************************************




















conn.close()

autenticacion = Autenticacion()
autenticacion.mainloop()