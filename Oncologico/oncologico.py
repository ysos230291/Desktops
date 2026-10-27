<<<<<<< HEAD
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

    sql = """ CREATE TABLE `oncologico`.`pacientes` (`fecha_registro` DATE NOT NULL , `historia_clinica` VARCHAR(50) NOT NULL , `ci` VARCHAR(50) NOT NULL , `nombre` VARCHAR(50) NOT NULL , `1er_apellido` VARCHAR(50) NOT NULL , `2do_apellido` VARCHAR(50) NOT NULL , `edad` INT NOT NULL , `raza` VARCHAR(50) NOT NULL , `municipio` VARCHAR(50) NOT NULL , `sexo` VARCHAR(10) NOT NULL , `fecha_cons_presc` DATE NOT NULL, `resumen` TEXT NOT NULL , `localizacion` VARCHAR(50) NOT NULL , `t` VARCHAR(10) NOT NULL , `n` VARCHAR(10) NOT NULL , `m` VARCHAR(10) NOT NULL , `estadio` TEXT NOT NULL , `comentario` TEXT NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

######################################## crear tabla volumenes #################################
try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "oncologico"    
        )
    cursor = conn.cursor()

    sql = """ CREATE TABLE `oncologico`.`volumenes` ( `volumen` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

######################################## crear tabla localizaciones #################################
try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "oncologico"    
        )
    cursor = conn.cursor()

    sql = """ CREATE TABLE `oncologico`.`localizaciones` ( `localizacion` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
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

    sql = """ CREATE TABLE `oncologico`.`dosis` (`id` INT NOT NULL, `fecha_presc` DATE NOT NULL, `fecha_ultima` DATE NOT NULL , `ci` VARCHAR(50) NOT NULL, `volumen` VARCHAR(50) NOT NULL , `dosis_x_fraccion` DOUBLE NOT NULL , `fx` INT NOT NULL , `dosis` DOUBLE NOT NULL, `fx_vencidas` INT NOT NULL, `dosis_restante` DOUBLE NOT NULL, `arreglo` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
    
except:
    pass


################################## crear tabla arreglos #########################################
try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "oncologico"    
        )
    cursor = conn.cursor()

    sql = """ CREATE TABLE `oncologico`.`arreglos` (`Id` INT NOT NULL, `CI` VARCHAR(50) NOT NULL, `Nombre` VARCHAR(50) NOT NULL, `D/Campos` FLOAT NOT NULL , `Campo` VARCHAR(50) NOT NULL , `X(cm)` FLOAT NOT NULL , `Y(cm)` FLOAT NOT NULL, `SSD` FLOAT NOT NULL, `Camilla` INT NOT NULL, `Gantry` INT NOT NULL, `Colim` INT NOT NULL, `Filtro` VARCHAR(50) NOT NULL, `Bandeja` VARCHAR(50) NOT NULL, `Tiempo` FLOAT NOT NULL ) ENGINE = InnoDB; """
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

        def volumenes_lobby():
            vol = Volumenes()

        def localizaciones_lobby():
            loc = Localizaciones()
        
        administrativo_menu = Menu(self.menu, tearoff = 0)
        administrativo_menu.add_command(label="Volumenes",command=volumenes_lobby)
        administrativo_menu.add_command(label="Localizaciones",command=localizaciones_lobby)

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
        self.menu.add_cascade(label="Administrativo",menu=administrativo_menu)
        self.menu.add_cascade(label="Usuarios", menu = usuario_menu)
        self.menu.add_cascade(label="Licencia", menu = licencia_menu)
        self.menu.add_cascade(label="Salir", menu = salir_menu)


# **********************************************************************************
# ****************************** Volumenes *****************************************
# **********************************************************************************

class Volumenes(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Volumenes")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))   

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ())
        self.tabla.column("#0", width = 500)

        self.tabla.place(x = 100, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Volumen")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)   

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"    
                )
            cursor = conn.cursor()
            sql = f""" SELECT * FROM `volumenes` """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0])                        

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
            temp.after(250, lambda: temp.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))  

            temp.texto_nombre = CTkEntry(temp, placeholder_text="Volumen ...")
            temp.texto_nombre.pack(pady = 10)

            def aceptar():
                if temp.texto_nombre.get() == "":
                    error = messagebox.showerror("Error","Debes escribir algun nombre para el volumen que quieres agregar")
                else:
                    # vemos que no se repita la categoria
                    repetido = False
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"    
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT * FROM `volumenes` """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == temp.texto_nombre.get():
                            repetido = True
                            error = messagebox.showerror("Error","Esa categoria ya existe")

                    if not repetido:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "oncologico"    
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `volumenes`(`volumen`) VALUES ('{temp.texto_nombre.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla(True)

                        term = messagebox.showinfo("Terminado","Se ha creado la Categoria")
                        temp.destroy()

            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 30)
        self.btn_agregar.place(x = 100, y = 400)                            
             

        def on_click(event):            
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                volumen = self.tabla.item(item, "text")  

            try:
                string = f"Vas a eliminar a {volumen} de las categorias"
                conf = messagebox.askokcancel("Confirmar",string)    
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"    
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `volumenes` WHERE `Volumen` = "{volumen}" """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla(True)

                    term = messagebox.showinfo("Terminado","Se ha eliminado la Categoria")                    

            except:
                error = messagebox.showerror("Error","Selecciona una categoria para eliminar")               

        self.tabla.bind("<Double-1>", on_click)




# **********************************************************************************
# ****************************** Localizaciones ************************************
# **********************************************************************************

class Localizaciones(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Localizaciones")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x600") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))   

        estilos_tablas()        
        
        self.tabla = ttk.Treeview(self, columns = ())
        self.tabla.column("#0", width = 500)

        self.tabla.place(x = 100, y = 50)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "Localizaciones")

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)   

        def llenar_tabla(event):
            self.tabla.delete(*self.tabla.get_children())
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"    
                )
            cursor = conn.cursor()
            sql = f""" SELECT * FROM `localizaciones` """
            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0])                        

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
            temp.after(250, lambda: temp.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))  

            temp.texto_nombre = CTkEntry(temp, placeholder_text="Volumen ...")
            temp.texto_nombre.pack(pady = 10)

            def aceptar():
                if temp.texto_nombre.get() == "":
                    error = messagebox.showerror("Error","Debes escribir algun nombre para la localizacion que quieres agregar")
                else:
                    # vemos que no se repita la localizacion
                    repetido = False
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"    
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT * FROM `localizaciones` """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] == temp.texto_nombre.get():
                            repetido = True
                            error = messagebox.showerror("Error","Esa categoria ya existe")

                    if not repetido:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "oncologico"    
                            )
                        cursor = conn.cursor()

                        sql = f""" INSERT INTO `localizaciones`(`localizacion`) VALUES ('{temp.texto_nombre.get()}') """
                        cursor.execute(sql)
                        conn.commit()

                        llenar_tabla(True)

                        term = messagebox.showinfo("Terminado","Se ha creado la Localizacion")
                        temp.destroy()

            temp.btn = CTkButton(temp, text="Aceptar", command=aceptar)
            temp.btn.pack(pady = 10)

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar, width = 200, height = 30)
        self.btn_agregar.place(x = 100, y = 400)                            
             

        def on_click(event):            
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                localizacion = self.tabla.item(item, "text")  

            try:
                string = f"Vas a eliminar a {localizacion} de las localizaciones"
                conf = messagebox.askokcancel("Confirmar",string)    
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"    
                        )
                    cursor = conn.cursor()

                    sql = f""" DELETE FROM `localizaciones` WHERE `Localizacion` = "{localizacion}" """
                    cursor.execute(sql)
                    conn.commit()

                    llenar_tabla(True)

                    term = messagebox.showinfo("Terminado","Se ha eliminado la Localizacion")                    

            except:
                error = messagebox.showerror("Error","Selecciona una localizacion para eliminar")               

        self.tabla.bind("<Double-1>", on_click)



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

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "HC"))
        self.tabla.column("#0", width = 140)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("HC", width = 140)               

        self.tabla.place(x = 850, y = 420)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "CI")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("HC", text = "HC")
                

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
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica` FROM `pacientes` WHERE `ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%' """

            else:
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica` FROM `pacientes` WHERE `fecha_cons_presc` = "{self.texto_buscador_fecha.get()}" AND (`ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%') """

            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1] + " " + index[2] + " " +index[3], index[4],))  

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

        self.texto_presc = CTkEntry(self, placeholder_text="Fecha Presc...")
        self.texto_presc.place(x = 50, y = 460) 

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
        self.btn_fecha_presc.place(x=200 ,y=460 )

        def crear():
            conf = messagebox.askokcancel("Confirmar","Se va a agregar el paciente")
            if conf:
                if self.texto_municipios.get() == "Municipios..." or self.texto_presc.get() == "" or self.texto_sexo.get() == "Sexo..." or self.texto_raza.get() == "Raza..." or self.texto_edad.get() == "" or self.texto_apellido2.get() == "" or self.texto_apellido1.get() == "" or self.texto_nombre.get() == "" or self.texto_hc.get() == "" or self.texto_ci.get() == "":
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

                        sql = f""" INSERT INTO `pacientes`(`fecha_registro`, `historia_clinica`, `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `edad`, `raza`, `municipio`, `sexo`, `fecha_cons_presc`, `resumen`, `localizacion`, `t`, `n`, `m`, `estadio`, `comentario`, `estado`) VALUES ('{fecha_actual}','{self.texto_hc.get()}','{self.texto_ci.get()}','{self.texto_nombre.get()}','{self.texto_apellido1.get()}','{self.texto_apellido2.get()}','{self.texto_edad.get()}','{self.texto_raza.get()}','{self.texto_municipios.get()}','{self.texto_sexo.get()}','{self.texto_presc.get()}','-','-','-','-','-','-','-','abierto') """
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
                if self.texto_municipios.get() == "Municipios..." or self.texto_presc.get() == "" or self.texto_sexo.get() == "Sexo..." or self.texto_raza.get() == "Raza..." or self.texto_edad.get() == "" or self.texto_apellido2.get() == "" or self.texto_apellido1.get() == "" or self.texto_nombre.get() == "" or self.texto_hc.get() == "" or self.texto_ci.get() == "":
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

                    sql = f""" UPDATE `pacientes` SET `historia_clinica`='{self.texto_hc.get()}',`ci`='{self.texto_ci.get()}',`nombre`='{self.texto_nombre.get()}',`1er_apellido`='{self.texto_apellido1.get()}',`2do_apellido`='{self.texto_apellido2.get()}',`edad`='{self.texto_edad.get()}',`raza`='{self.texto_raza.get()}',`municipio`='{self.texto_municipios.get()}',`sexo`='{self.texto_sexo.get()}',`fecha_cons_presc`='{self.texto_presc.get()}' WHERE `ci` = {ci} """
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

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "HC"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("HC", width = 100)              

        self.tabla.place(x = 850, y = 420)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "CI")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("HC", text = "HC")              

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
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica` FROM `pacientes` WHERE `ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%' """

            else:
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica` FROM `pacientes` WHERE `fecha_cons_presc` = "{self.texto_buscador_fecha.get()}" AND (`ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%') """

            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1] + " " + index[2] + " " +index[3], index[4],))  

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
            global nombre
            global hc

            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                ci = self.tabla.item(item, "text")                                          
                nombre = self.tabla.item(item, "values")[0]                          
                hc = self.tabla.item(item, "values")[1]                          

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
                    # lo ponemos como estaba originalmente
                    self.texto_localizacion.delete(0,END)
                    self.texto_t.delete(0,END)
                    self.texto_n.delete(0,END)
                    self.texto_m.delete(0,END)
                    self.texto_estadio.delete(0,END)
                    self.texto_resumen.delete("0.0",END)
                    self.texto_comentario.delete("0.0",END)

                    self.texto_comentario.insert("0.0","Comentario...")
                    self.texto_resumen.insert("0.0","Resumen...")
                    
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

        def aceptar():
            if self.texto_localizacion.get() == "" or self.texto_t.get() == "" or self.texto_n.get() == "" or self.texto_m.get() == "" or self.texto_estadio.get() == "" or self.texto_resumen.get("0.0",END) == "Resumen..." or self.texto_comentario.get("0.0",END) == "Comentario...":
                error = messagebox.showerror("Error","Llena todos los campos")

            else:
                conf = messagebox.askokcancel("Confirmar","Se va a prescribir el paciente")
                if conf:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = f""" UPDATE `pacientes` SET `resumen`='{self.texto_resumen.get("0.0",END)}',`localizacion`='{self.texto_localizacion.get()}',`t`='{self.texto_t.get()}',`n`='{self.texto_n.get()}',`m`='{self.texto_m.get()}',`estadio`='{self.texto_estadio.get()}',`comentario`='{self.texto_comentario.get("0.0",END)}' WHERE `ci` = "{ci}" """
                    cursor.execute(sql)
                    conn.commit()

        self.btn_aceptar = CTkButton(self,text="Aceptar", command=aceptar)
        self.btn_aceptar.place(x=50,y=600)

        def prescribir():
            if ci and nombre and hc:
                temp = CTkToplevel()
                temp.title("Prescripcion") 
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
                temp.after(250, lambda: temp.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   

                # ahora vamos a mostrar la cinta con la info del paciente que vamos a trabajar  
                string = f"     ci: {ci}    HC: {hc}    Nombre: {nombre}"  
                temp.label_cinta = CTkLabel(temp,text=string)   
                temp.label_cinta.place(x=0,y=0)

                temp.tabla_volumen = ttk.Treeview(temp)
                temp.tabla_volumen.column("#0", width = 200)               

                temp.tabla_volumen.place(x = 50, y = 100)        
                temp.tabla_volumen.config(height = 10)

                temp.tabla_volumen.heading("#0", text = "Volumen")                                      

                scrollbar1 = CTkScrollbar(temp, command = temp.tabla_volumen.yview, width = 18)
                scrollbar1.place(in_ = temp.tabla_volumen, relheigh = 1, relx = 1)

                temp.tabla_volumen.config(yscrollcommand = scrollbar1.set)

                def llenar_tabla_volumen():
                    temp.tabla_volumen.delete(*temp.tabla_volumen.get_children())
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT DISTINCT `volumen` FROM `dosis` WHERE `ci` = "{ci}" """
                    cursor.execute(sql)
                    for index in cursor:
                        temp.tabla_volumen.insert("",END, text = index[0],) 

                llenar_tabla_volumen()

                # ahora vamos a seleccionar el volumen dando un click
                def sel_vol(event):
                    global volumen
                    seleccion = temp.tabla_volumen.selection()
                    if seleccion:
                        item = seleccion[0]                
                        volumen = temp.tabla_volumen.item(item, "text")                     

                    llenar_tabla_presc()                                 
        
                temp.tabla_volumen.bind("<ButtonRelease-1>", sel_vol)

                def agregar_volumen():
                    root = CTkToplevel()
                    root.title("Agregar Volumen") 
                    htotal = root.winfo_screenheight()
                    wtotal = root.winfo_screenwidth()               
                    posx = round(wtotal/2-wventana/2)
                    posy = round(htotal/2-hventana/2)
                    root.geometry(f"300x300+{posx}+{posy}")
                    root.lift()
                    root.attributes('-topmost', True)
                    root.after(200, lambda: temp.attributes('-topmost', False)) 
                    root.after(250, lambda: temp.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))  

                    root.texto_volumen = CTkEntry(root,placeholder_text="Volumen ...")
                    root.texto_volumen.pack(pady = 10)

                    def aceptar():
                        conf = messagebox.askokcancel("Confirmar","Se va a agregar el volumen")
                        if conf:
                            # 1ro revisar que el volumen que voy a agregar no este ya 
                            repetido = False
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password = "",
                                database = "oncologico"
                                )
                            cursor = conn.cursor()
        
                            sql = f""" SELECT `volumen` FROM `dosis` WHERE `ci` = "{ci}" """
                            cursor.execute(sql)
                            for index in cursor:
                                if index[0] == root.texto_volumen.get():
                                    repetido = True
                                    break

                            if not repetido:
                                # 2do encontrar el id de la dosis                                                 
                                id_dosis = 1
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "",
                                    database = "oncologico"
                                    )
                                cursor = conn.cursor()

                                sql = """ SELECT MAX(id) FROM `dosis`; """
                                cursor.execute(sql)
                                for index in cursor:
                                    if index[0] == None:
                                        pass
                                    else:
                                        id_dosis = index[0] + 1 

                                # 3ro llevar el volumen a la base de datos
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "",
                                    database = "oncologico"
                                    )
                                cursor = conn.cursor()
            
                                sql = f""" INSERT INTO `dosis`(`id`, `fecha_presc`, `fecha_ultima`, `ci`, `volumen`, `dosis_x_fraccion`, `fx`, `dosis`, `fx_vencidas`, `dosis_restante`) VALUES ('{id_dosis}','{fecha_actual}','{fecha_actual}','{ci}','{root.texto_volumen.get()}','0','0','0','0','0') """
                                cursor.execute(sql)
                                conn.commit()

                                llenar_tabla_volumen()
                                root.destroy()


                    root.btn_aceptar = CTkButton(root,text="Aceptar",command=aceptar)
                    root.btn_aceptar.pack(pady = 10)

                temp.btn_agregar = CTkButton(temp,text="Agregar",command=agregar_volumen)
                temp.btn_agregar.place(x=50,y=400)

                temp.tabla_presc = ttk.Treeview(temp, columns = ("D/fx", "No.fx", "Dosis", "Impartida", "F_Presc", "Ult_Act"), show="headings")
                temp.tabla_presc.column("#0", width = 50)               
                temp.tabla_presc.column("D/fx", width = 150)
                temp.tabla_presc.column("No.fx", width = 150)
                temp.tabla_presc.column("Dosis", width = 100)       
                temp.tabla_presc.column("Impartida", width = 100)       
                temp.tabla_presc.column("F_Presc", width = 100)       
                temp.tabla_presc.column("Ult_Act", width = 100)       

                temp.tabla_presc.place(x = 480, y = 100)        
                temp.tabla_presc.config(height = 10)

                temp.tabla_presc.heading("#0", text = "id")                
                temp.tabla_presc.heading("D/fx", text = "D/fx[cGy]")
                temp.tabla_presc.heading("No.fx", text = "No.fx")
                temp.tabla_presc.heading("Dosis", text = "Dosis[cGy]")        
                temp.tabla_presc.heading("Impartida", text = "Impartida")        
                temp.tabla_presc.heading("F_Presc", text = "F_Presc")        
                temp.tabla_presc.heading("Ult_Act", text = "Ult_Act")        

                scrollbar = CTkScrollbar(temp, command = temp.tabla_presc.yview, width = 18)
                scrollbar.place(in_ = temp.tabla_presc, relheigh = 1, relx = 1)

                temp.tabla_presc.config(yscrollcommand = scrollbar.set)

                def llenar_tabla_presc():
                    temp.tabla_presc.delete(*temp.tabla_presc.get_children())
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `dosis` WHERE `ci` = "{ci}" AND `volumen` = "{volumen}" """
                    cursor.execute(sql)
                    for index in cursor:
                        temp.tabla_presc.insert("",END, text = index[0], values = (index[5],index[6],index[7],index[8],index[1],index[2],)) 

                # ahora vamos a hacer la ventana modal para poder agregar prescripciones cuando demos al boton
                def agregar_prescripcion():
                    vent1 = CTkToplevel()
                    vent1.title("Agregar Prescricion")                     
                    vent1.geometry(f"+{posx}+{posy}")
                    vent1.lift()
                    vent1.attributes('-topmost', True)
                    vent1.after(200, lambda: vent1.attributes('-topmost', False)) 
                    vent1.after(250, lambda: vent1.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico')) 

                    vent1.texto_d_f = CTkEntry(vent1,placeholder_text="D/fx[cGy] ...")
                    vent1.texto_d_f.pack(pady = 10)

                    vent1.texto_f = CTkEntry(vent1,placeholder_text="No.fx ...")
                    vent1.texto_f.pack(pady = 10)

                    def agregar():
                        if volumen == None:
                            messagebox.showerror("Error","Selecciona un volumen dando click sobre el") 
                        else:
                            string_volumen = f"Se va a agregar la prescripcion al {volumen}"
                            conf = messagebox.askokcancel("Confirmar",string_volumen)
                            if conf:
                                modificar = False
                                id_dosis = 0
                                try:
                                    # verifiquemos si el volumen esta en 0 (para modificarlo entonces, si no hay que insertar)
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "root",
                                        password = "",
                                        database = "oncologico"
                                        )
                                    cursor = conn.cursor()
                
                                    sql = f""" SELECT `id`, `dosis_x_fraccion` FROM `dosis` WHERE `ci` = "{ci}" AND `volumen` = "{volumen}" """
                                    cursor.execute(sql)
                                    for index in cursor:
                                        if index[1] == 0:
                                            modificar = True
                                            id_dosis = index[0]

                                    if modificar:
                                        # ahora agregamos la dosis respectiva a ese volumen
                                        conn = mysql.connector.connect(
                                            host = "localhost",
                                            user = "root",
                                            password = "",
                                            database = "oncologico"
                                            )
                                        cursor = conn.cursor()
                    
                                        sql = f""" UPDATE `dosis` SET `fecha_ultima`='{fecha_actual}',`dosis_x_fraccion`='{vent1.texto_d_f.get()}',`fx`='{vent1.texto_f.get()}',`dosis`='{int(vent1.texto_d_f.get())*int(vent1.texto_f.get())}',`fx_vencidas`='0',`dosis_restante`='{int(vent1.texto_d_f.get())*int(vent1.texto_f.get())}' WHERE `id` = {id_dosis} """
                                        cursor.execute(sql)
                                        conn.commit()

                                        llenar_tabla_presc()
                                        vent1.destroy()

                                    else:
                                        # significa que ay que insertar la dosis
                                        # hallemos el id de la dosis
                                        id_dosis = 1
                                        conn = mysql.connector.connect(
                                            host = "localhost",
                                            user = "root",
                                            password = "",
                                            database = "oncologico"
                                            )
                                        cursor = conn.cursor()
        
                                        sql = """ SELECT MAX(id) FROM `dosis`; """
                                        cursor.execute(sql)
                                        for index in cursor:
                                            if index[0] == None:
                                                pass
                                            else:
                                                id_dosis = index[0] + 1 

                                        # ahora insertamos la dosis a la bd 
                                        conn = mysql.connector.connect(
                                            host = "localhost",
                                            user = "root",
                                            password = "",
                                            database = "oncologico"
                                            )
                                        cursor = conn.cursor()
                    
                                        sql = f""" INSERT INTO `dosis`(`id`, `fecha_presc`, `fecha_ultima`, `ci`, `volumen`, `dosis_x_fraccion`, `fx`, `dosis`, `fx_vencidas`, `dosis_restante`) VALUES ('{id_dosis}','{fecha_actual}','{fecha_actual}','{ci}','{volumen}','{vent1.texto_d_f.get()}','{vent1.texto_f.get()}','{int(vent1.texto_d_f.get())*int(vent1.texto_f.get())}','0','{int(vent1.texto_d_f.get())*int(vent1.texto_f.get())}') """
                                        cursor.execute(sql)
                                        conn.commit()

                                        llenar_tabla_presc()
                                        vent1.destroy()

                                except:
                                    messagebox.showerror("Error","No se pudo agregar correctamente la prescripcion al volumen") 

                    vent1.btn_agregar = CTkButton(vent1,text="Agregar", command=agregar)
                    vent1.btn_agregar.pack(pady = 10)

                temp.btn_agregar_presccripcion = CTkButton(temp,text="Agregar Prescripcion", command=agregar_prescripcion)
                temp.btn_agregar_presccripcion.place(x=230,y=200)

                # ya podemos agregar volumenes y prescripciones, ahora hay que poder eliminarlos o modificarlos
                # primero vamos a eliminar los volumenes de su tabla si es posible 

                def eliminar_volumen():
                    conf = messagebox.askokcancel("Confirmar","Se va a eliminar el volumen")
                    if conf:
                        # primero debemos revisar que ninguna de las dosis este inicializada, si no no se puede eliminar el volumen
                        permiso_eliminar = True
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "oncologico"
                            )
                        cursor = conn.cursor()

                        sql = f""" SELECT `fx_vencidas` FROM `dosis` WHERE `ci` = "{ci}" AND `volumen` = "{volumen}" """
                        cursor.execute(sql)
                        for index in cursor:
                            if index[0] == 0:
                                pass
                            else:
                                permiso_eliminar = False
                                messagebox.showerror("Error", "No puedes eliminar un volumen que tiene dosis inicializadas")

                        if permiso_eliminar:
                            # ahora podemos eliminar el volumen
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password = "",
                                database = "oncologico"
                                )
                            cursor = conn.cursor()
        
                            sql = f""" DELETE FROM `dosis` WHERE `ci` = "{ci}" AND `volumen` = "{volumen}" """
                            cursor.execute(sql)
                            conn.commit()

                            llenar_tabla_presc()
                            llenar_tabla_volumen()


                temp.menu = Menu(temp,tearoff=0)
                temp.menu.add_command(label="Eliminar",command=eliminar_volumen)

                def mostrar_menu_volumen(event):
                    global volumen_eliminar
                    item = temp.tabla_volumen.identify_row(event.y)
                    if item:
                        temp.tabla_volumen.selection_set(item)
                        item_seleccionado = item
                        temp.menu.post(event.x_root,event.y_root)
                        volumen_eliminar = temp.tabla_volumen.item(item, "text") 

                temp.tabla_volumen.bind("<Button-3>",mostrar_menu_volumen)

                # ahora el menu de click derecho de la tabla presc
                def modificar_presc():
                    vent1 = CTkToplevel()
                    vent1.title("Modificar Prescricion")                     
                    vent1.geometry(f"+{posx}+{posy}")
                    vent1.lift()
                    vent1.attributes('-topmost', True)
                    vent1.after(200, lambda: vent1.attributes('-topmost', False)) 
                    vent1.after(250, lambda: vent1.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico')) 

                    vent1.label = CTkLabel(vent1,text="Se sustituira el numero de fracciones")
                    vent1.label.pack(pady = 10)

                    vent1.texto_f = CTkEntry(vent1,placeholder_text="No.fx ...")
                    vent1.texto_f.pack(pady = 10)

                    def modificar():
                        # 1ro verificar que el numero de fracciones nuevo es mayor que las impartidas
                        if impartidas > int(vent1.texto_f.get()):
                            messagebox.showerror("Error","No puedes hacer esta modificacion \n Las dosis impartidas serian mayor que el numero de dosis")

                        else:
                            conf = messagebox.askokcancel("Confirmar","Se va a modificar la prescripcion")
                            if conf:
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "",
                                    database = "oncologico"
                                    )
                                cursor = conn.cursor()
            
                                sql = f""" UPDATE `dosis` SET `fecha_ultima`='{fecha_actual}',`fx`='{vent1.texto_f.get()}',`dosis`=`dosis_x_fraccion`*'{int(vent1.texto_f.get())}',`dosis_restante`='{int(vent1.texto_f.get())}'-`fx_vencidas` WHERE `id` = {presc} """
                                cursor.execute(sql)
                                conn.commit()
    
                                llenar_tabla_presc()
                                llenar_tabla_volumen()
                                vent1.destroy()

                    vent1.btn = CTkButton(vent1,text="Modificar", command=modificar)
                    vent1.btn.pack(pady = 10)

                def eliminar_presc():
                    # 1ro es que no tenga impartidas
                    if impartidas > 0:
                        messagebox.showerror("Error","No puedes eliminar una prescripcion que tenga fracciones impartidas")
                    else:
                        conf = messagebox.askokcancel("Confirmar","Se va a eliminar la prescripcion")
                        if conf:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password = "",
                                database = "oncologico"
                                )
                            cursor = conn.cursor()
        
                            sql = f""" DELETE FROM `dosis` WHERE `id` = {presc} """
                            cursor.execute(sql)
                            conn.commit()

                            llenar_tabla_presc()
                            llenar_tabla_volumen()

                temp.menu_presc = Menu(temp,tearoff=0)
                temp.menu_presc.add_command(label="Modificar",command=modificar_presc)
                temp.menu_presc.add_command(label="Eliminar",command=eliminar_presc)

                def mostrar_menu_volumen(event):
                    global presc
                    global impartidas
                    item = temp.tabla_presc.identify_row(event.y)
                    if item:
                        temp.tabla_presc.selection_set(item)                        
                        temp.menu_presc.post(event.x_root,event.y_root)
                        presc = temp.tabla_presc.item(item, "text") 
                        impartidas = int(temp.tabla_presc.item(item, "values")[3])

                temp.tabla_presc.bind("<Button-3>",mostrar_menu_volumen)



            else:
                error = messagebox.showerror("Error","Selecciona algun paciente dando doble click")

        self.btn_prescripcion = CTkButton(self,text="Prescribir", command=prescribir)
        self.btn_prescripcion.place(x=310,y=600)



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

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "HC"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("HC", width = 100)              

        self.tabla.place(x = 850, y = 420)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "CI")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("HC", text = "HC")              

        scrollbar = CTkScrollbar(self, command = self.tabla.yview, width = 18)
        scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = scrollbar.set)

        global ci
        ci = 0

        def on_click(event):
            global ci
            global nombre
            global hc
            seleccion = self.tabla.selection()
            if seleccion:
                item = seleccion[0]                
                ci = self.tabla.item(item, "text") 
                nombre = self.tabla.item(item, "values")[0] 
                hc = self.tabla.item(item, "values")[1] 

            llenar_tabla_volumen()  
            llenar_comentario()             

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
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica` FROM `pacientes` WHERE `ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%' """

            else:
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica` FROM `pacientes` WHERE `fecha_cons_presc` = "{self.texto_buscador_fecha.get()}" AND (`ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%') """

            cursor.execute(sql)
            for index in cursor:
                self.tabla.insert("",END, text = index[0], values = (index[1] + " " + index[2] + " " +index[3], index[4],))  

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

        # ahora trabajaremos con el lado izquierdo de la ventana 
        # 1ro la tabla volumenes

        self.tabla_volumen = ttk.Treeview(self)
        self.tabla_volumen.column("#0", width = 200)               

        self.tabla_volumen.place(x = 60, y = 90)        
        self.tabla_volumen.config(height = 10)

        self.tabla_volumen.heading("#0", text = "Volumen")                                      

        scrollbar1 = CTkScrollbar(self, command = self.tabla_volumen.yview, width = 18)
        scrollbar1.place(in_ = self.tabla_volumen, relheigh = 1, relx = 1)

        self.tabla_volumen.config(yscrollcommand = scrollbar1.set)

        def llenar_tabla_volumen():
            try:
                self.tabla_volumen.delete(*self.tabla_volumen.get_children())
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "oncologico"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT DISTINCT `volumen` FROM `dosis` WHERE `ci` = "{ci}" """
                cursor.execute(sql)
                for index in cursor:
                    self.tabla_volumen.insert("",END, text = index[0],) 
            except:
                messagebox.showerror("Error","Hubo algun error al agregar los volumenes")

        # 2do el campo del comentario
        self.texto_comentario = CTkTextbox(self,width=400,height=150)
        self.texto_comentario.insert("0.0","Comentario...")
        self.texto_comentario.place(x = 50, y = 400)

        def llenar_comentario():
            try:
                self.texto_comentario.delete("0.0",END)
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "oncologico"
                    )
                cursor = conn.cursor()

                sql = f""" SELECT `comentario` FROM `pacientes` WHERE `ci` = "{ci}" """
                cursor.execute(sql)
                for index in cursor:
                    self.texto_comentario.insert("0.0",index[0])

            except:
                messagebox.showerror("Error","Hubo problemas al mostrar el comentario")

        def arreglos(): 
            try:                    
                # aqui vamos a agregar los arreglos ya sea manual o importado
                string = f"     ci: {ci}    HC: {hc}    Nombre: {nombre}"             
            
                vent1 = CTkToplevel()
                vent1.title("Arreglos") 
                htotal = vent1.winfo_screenheight()
                wtotal = vent1.winfo_screenwidth()
                wventana = 1000
                hventana = 600
                posx = round(wtotal/2-wventana/2)
                posy = round(htotal/2-hventana/2)
                vent1.geometry(f"1000x600+{posx}+{posy}")
                vent1.lift()
                vent1.attributes('-topmost', True)
                vent1.after(200, lambda: vent1.attributes('-topmost', False)) 
                vent1.after(250, lambda: vent1.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico')) 

                # ahora vamos a mostrar la cinta con la info del paciente que vamos a trabajar                   
                vent1.label_cinta = CTkLabel(vent1,text=string)   
                vent1.label_cinta.place(x=0,y=0)

                # ahora vamos a hacer la tabla donde se muestran solo los nombres de los arreglos 
                vent1.tabla_nombre = ttk.Treeview(vent1,columns=("Nombre"), show="headings")
                vent1.tabla_nombre.column("#0", width = 50)               
                vent1.tabla_nombre.column("Nombre", width = 200)               

                vent1.tabla_nombre.place(x = 50, y = 50)        
                vent1.tabla_nombre.config(height = 10)

                vent1.tabla_nombre.heading("#0", text = "Id")                                      
                vent1.tabla_nombre.heading("Nombre", text = "Nombre")                                      

                scrollbar1 = CTkScrollbar(vent1, command = vent1.tabla_nombre.yview, width = 18)
                scrollbar1.place(in_ = vent1.tabla_nombre, relheigh = 1, relx = 1)

                vent1.tabla_nombre.config(yscrollcommand = scrollbar1.set)                 

                def llenar_tabla_nombre():
                    vent1.tabla_nombre.delete(*vent1.tabla_nombre.get_children())
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT DISTINCT `Id`, `Nombre` FROM `arreglos` WHERE `CI` = "{ci}" """
                    cursor.execute(sql)
                    for index in cursor:
                        vent1.tabla_nombre.insert("",END, text = index[0], values = (index[1],)) 

                llenar_tabla_nombre()                              

                # ahora los eventos de la tabla nombre 
                def on_click(event):
                    global id_arreglo
                    seleccion = vent1.tabla_nombre.selection()
                    if seleccion:
                        item = seleccion[0]                
                        id_arreglo = vent1.tabla_nombre.item(item, "text")  

                    llenar_tabla_arreglos()              
        
                vent1.tabla_nombre.bind("<ButtonRelease-1>", on_click)

                def doble_click(event):
                    seleccion = vent1.tabla_nombre.selection()
                    if seleccion:
                        item = seleccion[0]                
                        id_arreglo = vent1.tabla_nombre.item(item, "text") 

                    def eliminar_arreglo():
                        conf = messagebox.askokcancel("Confirmar","Se va a eliminar el arreglo")
                        if conf:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password = "",
                                database = "oncologico"
                                )
                            cursor = conn.cursor()
            
                            sql = f""" DELETE FROM `arreglos` WHERE `Id` = {id_arreglo} """
                            cursor.execute(sql)
                            conn.commit()
        
                            llenar_tabla_nombre() 
                            vaciar_tabla_arreglos() 

                    eliminar_arreglo()

                vent1.tabla_nombre.bind("<Double-1>", doble_click)

                # ahora vamos a hacer la tabla de los arreglos
                vent1.tabla_arreglos = ttk.Treeview(vent1, columns = ("D/Campos","Campo", "X(cm)", "Y(cm)", "SSD", "Camilla","Gantry","Colim","Filtro","Bandeja","Tiempo"), show="headings")
                vent1.tabla_arreglos.column("#0", width = 50,anchor="center")               
                vent1.tabla_arreglos.column("D/Campos", width = 100,anchor="center")
                vent1.tabla_arreglos.column("Campo", width = 100,anchor="center")
                vent1.tabla_arreglos.column("X(cm)", width = 100,anchor="center")       
                vent1.tabla_arreglos.column("Y(cm)", width = 100,anchor="center")       
                vent1.tabla_arreglos.column("SSD", width = 100,anchor="center")       
                vent1.tabla_arreglos.column("Camilla", width = 100,anchor="center")       
                vent1.tabla_arreglos.column("Gantry", width = 100,anchor="center")       
                vent1.tabla_arreglos.column("Colim", width = 100,anchor="center")       
                vent1.tabla_arreglos.column("Filtro", width = 100,anchor="center")       
                vent1.tabla_arreglos.column("Bandeja", width = 100,anchor="center")       
                vent1.tabla_arreglos.column("Tiempo", width = 100,anchor="center")       

                vent1.tabla_arreglos.place(x = 50, y = 400)        
                vent1.tabla_arreglos.config(height = 5)

                vent1.tabla_arreglos.heading("#0", text = "id")                
                vent1.tabla_arreglos.heading("D/Campos", text = "D/Campos")
                vent1.tabla_arreglos.heading("Campo", text = "Campo")
                vent1.tabla_arreglos.heading("X(cm)", text = "X(cm)")        
                vent1.tabla_arreglos.heading("Y(cm)", text = "Y(cm)")        
                vent1.tabla_arreglos.heading("SSD", text = "SSD")        
                vent1.tabla_arreglos.heading("Camilla", text = "Camilla")        
                vent1.tabla_arreglos.heading("Gantry", text = "Gantry")        
                vent1.tabla_arreglos.heading("Colim", text = "Colim")        
                vent1.tabla_arreglos.heading("Filtro", text = "Filtro")        
                vent1.tabla_arreglos.heading("Bandeja", text = "Bandeja")        
                vent1.tabla_arreglos.heading("Tiempo", text = "Tiempo")        

                scrollbar2 = CTkScrollbar(vent1, command = vent1.tabla_arreglos.yview, width = 18)
                scrollbar2.place(in_ = vent1.tabla_arreglos, relheigh = 1, relx = 1)

                vent1.tabla_arreglos.config(yscrollcommand = scrollbar2.set)

                # ahora vamos a llenar la tabla
                def llenar_tabla_arreglos():
                    vent1.tabla_arreglos.delete(*vent1.tabla_arreglos.get_children())
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `arreglos` WHERE `Id` = {id_arreglo} """
                    cursor.execute(sql)
                    for index in cursor:
                        vent1.tabla_arreglos.insert("",END, text = index[0], values = (index[3],index[4],index[5],index[6],index[7],index[8],index[9],index[10],index[11],index[12],index[13],)) 

                def vaciar_tabla_arreglos():
                    vent1.tabla_arreglos.delete(*vent1.tabla_arreglos.get_children())

                # ahora boton de insertar manual 
                def insertar_manual():
                    vent2 = CTkToplevel()
                    vent2.title("Arreglos") 
                    htotal = vent2.winfo_screenheight()
                    wtotal = vent2.winfo_screenwidth()
                    wventana = 1000
                    hventana = 600
                    posx = round(wtotal/2-wventana/2)
                    posy = round(htotal/2-hventana/2)
                    vent2.geometry(f"1000x600+{posx}+{posy}")
                    vent2.lift()
                    vent2.attributes('-topmost', True)
                    vent2.after(200, lambda: vent2.attributes('-topmost', False)) 
                    vent2.after(250, lambda: vent2.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico')) 

                    # ahora vamos a hacer la tabla de los arreglos
                    vent2.tabla_arreglos = ttk.Treeview(vent2, columns = ("Nombre","D/Campos","Campo", "X(cm)", "Y(cm)", "SSD", "Camilla","Gantry","Colim","Filtro","Bandeja","Tiempo"), show="headings")
                    vent2.tabla_arreglos.column("#0", width = 50,anchor="center")               
                    vent2.tabla_arreglos.column("Nombre", width = 100,anchor="center")
                    vent2.tabla_arreglos.column("D/Campos", width = 100,anchor="center")
                    vent2.tabla_arreglos.column("Campo", width = 100,anchor="center")
                    vent2.tabla_arreglos.column("X(cm)", width = 75,anchor="center")       
                    vent2.tabla_arreglos.column("Y(cm)", width = 75,anchor="center")       
                    vent2.tabla_arreglos.column("SSD", width = 100,anchor="center")       
                    vent2.tabla_arreglos.column("Camilla", width = 75,anchor="center")       
                    vent2.tabla_arreglos.column("Gantry", width = 75,anchor="center")       
                    vent2.tabla_arreglos.column("Colim", width = 100,anchor="center")       
                    vent2.tabla_arreglos.column("Filtro", width = 100,anchor="center")       
                    vent2.tabla_arreglos.column("Bandeja", width = 100,anchor="center")       
                    vent2.tabla_arreglos.column("Tiempo", width = 100,anchor="center")       
        
                    vent2.tabla_arreglos.place(x = 50, y = 50)        
                    vent2.tabla_arreglos.config(height = 5)
        
                    vent2.tabla_arreglos.heading("#0", text = "id")                
                    vent2.tabla_arreglos.heading("Nombre", text = "Nombre")
                    vent2.tabla_arreglos.heading("D/Campos", text = "D/Campos")
                    vent2.tabla_arreglos.heading("Campo", text = "Campo")
                    vent2.tabla_arreglos.heading("X(cm)", text = "X(cm)")        
                    vent2.tabla_arreglos.heading("Y(cm)", text = "Y(cm)")        
                    vent2.tabla_arreglos.heading("SSD", text = "SSD")        
                    vent2.tabla_arreglos.heading("Camilla", text = "Camilla")        
                    vent2.tabla_arreglos.heading("Gantry", text = "Gantry")        
                    vent2.tabla_arreglos.heading("Colim", text = "Colim")        
                    vent2.tabla_arreglos.heading("Filtro", text = "Filtro")        
                    vent2.tabla_arreglos.heading("Bandeja", text = "Bandeja")        
                    vent2.tabla_arreglos.heading("Tiempo", text = "Tiempo")        
        
                    scrollbar3 = CTkScrollbar(vent2, command = vent2.tabla_arreglos.yview, width = 18)
                    scrollbar3.place(in_ = vent2.tabla_arreglos, relheigh = 1, relx = 1)
        
                    vent2.tabla_arreglos.config(yscrollcommand = scrollbar3.set)

                    # ahora vamos a llenar la tabla 
                    def llenar_tabla_arreglos():
                        vent2.tabla_arreglos.delete(*vent2.tabla_arreglos.get_children())
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "oncologico"
                            )
                        cursor = conn.cursor()

                        sql = f""" SELECT * FROM `arreglos` WHERE `CI` = "{ci}" ORDER BY `Id` DESC """
                        cursor.execute(sql)
                        for index in cursor:
                            vent2.tabla_arreglos.insert("",END, text = index[0], values = (index[2],index[3],index[4],index[5],index[6],index[7],index[8],index[9],index[10],index[11],index[12],index[13],)) 

                    llenar_tabla_arreglos()


                    # ahora vamos a empezar a poner los campos de entrada 
                    vent2.nombre = CTkEntry(vent2, placeholder_text="Nombre")
                    vent2.nombre.place(x=40,y=200)

                    vent2.d_campos = CTkEntry(vent2,width=75, placeholder_text="D/Campos")
                    vent2.d_campos.place(x=40,y=240)

                    vent2.campo = CTkEntry(vent2,width=75, placeholder_text="Campo")
                    vent2.campo.place(x=120,y=240)

                    vent2.x = CTkEntry(vent2,width=75, placeholder_text="X(cm)")
                    vent2.x.place(x=200,y=240)

                    vent2.y = CTkEntry(vent2,width=75, placeholder_text="Y(cm)")
                    vent2.y.place(x=280,y=240)

                    vent2.ssd = CTkEntry(vent2,width=75, placeholder_text="SSD")
                    vent2.ssd.place(x=360,y=240)

                    vent2.camilla = CTkEntry(vent2,width=75, placeholder_text="Camilla")
                    vent2.camilla.place(x=440,y=240)

                    vent2.gantry = CTkEntry(vent2,width=75, placeholder_text="Gantry")
                    vent2.gantry.place(x=520,y=240)

                    vent2.colim = CTkEntry(vent2,width=75, placeholder_text="Colim")
                    vent2.colim.place(x=600,y=240)

                    vent2.filtro = CTkEntry(vent2,width=75, placeholder_text="Filtro")
                    vent2.filtro.place(x=680,y=240)

                    vent2.bandeja = CTkEntry(vent2,width=75, placeholder_text="Bandeja")
                    vent2.bandeja.place(x=760,y=240)

                    vent2.tiempo = CTkEntry(vent2,width=75, placeholder_text="Tiempo")
                    vent2.tiempo.place(x=840,y=240)

                    global mantener_id
                    mantener_id = False

                    # ahora el boton agregar registro 
                    def agregar_registro():  
                        conf=messagebox.askokcancel("Confirmar","Se va a agregar el arreglo")   
                        if conf: 
                            def buscar_id_arreglo():
                                global id_arreglo
                                # primero encontrar el id del arreglo
                                id_arreglo = 1
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "",
                                    database = "oncologico"
                                    )
                                cursor = conn.cursor()

                                sql = """ SELECT MAX(Id) FROM `arreglos`; """
                                cursor.execute(sql)
                                for index in cursor:
                                    if index[0] == None:
                                        pass
                                    else:
                                        id_arreglo = index[0] + 1 

                            def dar_entrada_arreglo():
                                global mantener_id
                                try:
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "root",
                                        password = "",
                                        database = "oncologico"
                                        )
                                    cursor = conn.cursor()
                
                                    sql = f""" INSERT INTO `arreglos`(`Id`, `CI`, `Nombre`, `D/Campos`, `Campo`, `X(cm)`, `Y(cm)`, `SSD`, `Camilla`, `Gantry`, `Colim`, `Filtro`, `Bandeja`, `Tiempo`) VALUES ('{id_arreglo}','{ci}','{vent2.nombre.get()}','{vent2.d_campos.get()}','{vent2.campo.get()}','{vent2.x.get()}','{vent2.y.get()}','{vent2.ssd.get()}','{vent2.camilla.get()}','{vent2.gantry.get()}','{vent2.colim.get()}','{vent2.filtro.get()}','{vent2.bandeja.get()}','{vent2.tiempo.get()}') """
                                    cursor.execute(sql)
                                    conn.commit()

                                    llenar_tabla_arreglos()

                                    # ahora vamos a verificar si agregamos otro registro o no 
                                    verificar = messagebox.askquestion("Coclusion","¿Se ha concluido la entrada de registros a este arreglo?")
                                    if verificar == "yes":
                                        # hay que actualizar la tabla de los nombres de los arreglos para que se vean 
                                        llenar_tabla_nombre()
                                        vent2.destroy()
                                    else:
                                        mantener_id = True
                                        # borramos los campos para volver a agregar info a la tabla arreglos
                                        vent2.d_campos.delete(0,END)
                                        vent2.campo.delete(0,END)
                                        vent2.x.delete(0,END)
                                        vent2.y.delete(0,END)
                                        vent2.ssd.delete(0,END)
                                        vent2.camilla.delete(0,END)
                                        vent2.gantry.delete(0,END)
                                        vent2.colim.delete(0,END)
                                        vent2.filtro.delete(0,END)
                                        vent2.bandeja.delete(0,END)
                                        vent2.tiempo.delete(0,END)

                                except:
                                    messagebox.showerror("Error","Ha habido error al agregar la informacion a la base de datos")

                            if mantener_id == False:
                                buscar_id_arreglo()
                                dar_entrada_arreglo()
                            else:
                                dar_entrada_arreglo()
                                

                    vent2.btn = CTkButton(vent2,text="Agregar Registro",command=agregar_registro)
                    vent2.btn.place(x=40,y=300)

                vent1.btn_manual = CTkButton(vent1,text="Manual",command=insertar_manual)
                vent1.btn_manual.place(x=50,y=500)

                # ahora boton de importar 
                def importar():
                    pass

                vent1.btn_importar = CTkButton(vent1,text="Importar",command=importar)
                vent1.btn_importar.place(x=200,y=500)     
            except:
                messagebox.showerror("Error","Debes seleccionar un paciente")       

        self.btn_arreglos = CTkButton(self,text="Arreglos",command=arreglos,width=100)
        self.btn_arreglos.place(x=50,y=600)

        

        def ventana_dosimetria():            
            try:
                string = f"     ci: {ci}    HC: {hc}    Nombre: {nombre}" 

                temp = CTkToplevel()
                temp.title("Dosimetria") 
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
                temp.after(250, lambda: temp.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico')) 

                # ahora vamos a mostrar la cinta con la info del paciente que vamos a trabajar                   
                temp.label_cinta = CTkLabel(temp,text=string)   
                temp.label_cinta.place(x=0,y=0)

                temp.tabla_volumen = ttk.Treeview(temp)
                temp.tabla_volumen.column("#0", width = 200)               

                temp.tabla_volumen.place(x = 50, y = 50)        
                temp.tabla_volumen.config(height = 10)

                temp.tabla_volumen.heading("#0", text = "Volumen")                                      

                scrollbar1 = CTkScrollbar(temp, command = temp.tabla_volumen.yview, width = 18)
                scrollbar1.place(in_ = temp.tabla_volumen, relheigh = 1, relx = 1)

                temp.tabla_volumen.config(yscrollcommand = scrollbar1.set)  

                def llenar_tabla_volumen():
                    temp.tabla_volumen.delete(*temp.tabla_volumen.get_children())
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT DISTINCT `volumen` FROM `dosis` WHERE `ci` = "{ci}" """
                    cursor.execute(sql)
                    for index in cursor:
                        temp.tabla_volumen.insert("",END, text = index[0],) 

                llenar_tabla_volumen()

                def sel_vol(event):
                    global volumen
                    seleccion = temp.tabla_volumen.selection()
                    if seleccion:
                        item = seleccion[0]                
                        volumen = temp.tabla_volumen.item(item, "text")                     

                    llenar_tabla_presc()                                 
        
                temp.tabla_volumen.bind("<ButtonRelease-1>", sel_vol)

                temp.tabla_presc = ttk.Treeview(temp, columns = ("D/fx", "No.fx", "Dosis", "Impartida", "F_Presc", "Ult_Act", "Arreglo"), show="headings")
                temp.tabla_presc.column("#0", width = 50)               
                temp.tabla_presc.column("D/fx", width = 100)
                temp.tabla_presc.column("No.fx", width = 100)
                temp.tabla_presc.column("Dosis", width = 100)       
                temp.tabla_presc.column("Impartida", width = 100)       
                temp.tabla_presc.column("F_Presc", width = 100)       
                temp.tabla_presc.column("Ult_Act", width = 100)       
                temp.tabla_presc.column("Arreglo", width = 100)       

                temp.tabla_presc.place(x = 480, y = 50)        
                temp.tabla_presc.config(height = 10)

                temp.tabla_presc.heading("#0", text = "id")                
                temp.tabla_presc.heading("D/fx", text = "D/fx[cGy]")
                temp.tabla_presc.heading("No.fx", text = "No.fx")
                temp.tabla_presc.heading("Dosis", text = "Dosis[cGy]")        
                temp.tabla_presc.heading("Impartida", text = "Impartida")        
                temp.tabla_presc.heading("F_Presc", text = "F_Presc")        
                temp.tabla_presc.heading("Ult_Act", text = "Ult_Act")        
                temp.tabla_presc.heading("Arreglo", text = "Arreglo")        

                scrollbar = CTkScrollbar(temp, command = temp.tabla_presc.yview, width = 18)
                scrollbar.place(in_ = temp.tabla_presc, relheigh = 1, relx = 1)

                temp.tabla_presc.config(yscrollcommand = scrollbar.set)

                def llenar_tabla_presc():
                    temp.tabla_presc.delete(*temp.tabla_presc.get_children())
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `dosis` WHERE `ci` = "{ci}" AND `volumen` = "{volumen}" """
                    cursor.execute(sql)
                    for index in cursor:
                        temp.tabla_presc.insert("",END, text = index[0], values = (index[5],index[6],index[7],index[8],index[1],index[2],))                  

                # ahora la tabla de los arreglos 
                temp.tabla_arreglos = ttk.Treeview(temp, columns = ("D/Campos","Campo", "X(cm)", "Y(cm)", "SSD", "Camilla","Gantry","Colim","Filtro","Bandeja","Tiempo"), show="headings")
                temp.tabla_arreglos.column("#0", width = 50)               
                temp.tabla_arreglos.column("D/Campos", width = 100)
                temp.tabla_arreglos.column("Campo", width = 100)
                temp.tabla_arreglos.column("X(cm)", width = 100)       
                temp.tabla_arreglos.column("Y(cm)", width = 100)       
                temp.tabla_arreglos.column("SSD", width = 100)       
                temp.tabla_arreglos.column("Camilla", width = 100)       
                temp.tabla_arreglos.column("Gantry", width = 100)       
                temp.tabla_arreglos.column("Colim", width = 100)       
                temp.tabla_arreglos.column("Filtro", width = 100)       
                temp.tabla_arreglos.column("Bandeja", width = 100)       
                temp.tabla_arreglos.column("Tiempo", width = 100)       

                temp.tabla_arreglos.place(x = 60, y = 450)        
                temp.tabla_arreglos.config(height = 5)

                temp.tabla_arreglos.heading("#0", text = "id")                
                temp.tabla_arreglos.heading("D/Campos", text = "D/Campos")
                temp.tabla_arreglos.heading("Campo", text = "Campo")
                temp.tabla_arreglos.heading("X(cm)", text = "X(cm)")        
                temp.tabla_arreglos.heading("Y(cm)", text = "Y(cm)")        
                temp.tabla_arreglos.heading("SSD", text = "SSD")        
                temp.tabla_arreglos.heading("Camilla", text = "Camilla")        
                temp.tabla_arreglos.heading("Gantry", text = "Gantry")        
                temp.tabla_arreglos.heading("Colim", text = "Colim")        
                temp.tabla_arreglos.heading("Filtro", text = "Filtro")        
                temp.tabla_arreglos.heading("Bandeja", text = "Bandeja")        
                temp.tabla_arreglos.heading("Tiempo", text = "Tiempo")        

                scrollbar2 = CTkScrollbar(temp, command = temp.tabla_arreglos.yview, width = 18)
                scrollbar2.place(in_ = temp.tabla_arreglos, relheigh = 1, relx = 1)

                temp.tabla_arreglos.config(yscrollcommand = scrollbar2.set)

                def llenar_tabla_arreglo_dos(event):
                    temp.tabla_arreglos.delete(*temp.tabla_arreglos.get_children())
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `arreglos` WHERE `Nombre` = "{temp.texto_escoger_arreglo.get()}" AND `CI` = "{ci}" """
                    cursor.execute(sql)
                    for index in cursor:
                        temp.tabla_arreglos.insert("",END, text = index[0], values = (index[3],index[4],index[5],index[6],index[7],index[8],index[9],index[10],index[11],index[12],index[13],))  

                # necesitamos un combo para escoger el arreglo
                nombres_arreglos = []                
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "oncologico"
                    )
                cursor = conn.cursor()
        
                sql = f""" SELECT DISTINCT `Nombre` FROM `arreglos` WHERE `CI` = "{ci}" """
                cursor.execute(sql)
                for index in cursor:
                    nombres_arreglos.append(index[0])

                temp.texto_escoger_arreglo=CTkComboBox(temp,values=nombres_arreglos,command=llenar_tabla_arreglo_dos)
                temp.texto_escoger_arreglo.set("...")
                temp.texto_escoger_arreglo.place(x=50,y=320)

            except:
                messagebox.showerror("Error","Seleccione algun paciente")
            
        self.btn_dosimetria = CTkButton(self,text="Dosimetria",command=ventana_dosimetria,width=100)
        self.btn_dosimetria.place(x=300,y=600)
                
                    


        








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

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "HC"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("HC", width = 100)             

        self.tabla.place(x = 850, y = 420)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "CI")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("HC", text = "HC")              

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
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica` FROM `pacientes` WHERE `ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%' """

            else:
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica` FROM `pacientes` WHERE `fecha_cons_presc` = "{self.texto_buscador_fecha.get()}" AND (`ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%') """

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

        self.tabla = ttk.Treeview(self, columns = ("Nombre Completo", "HC"))
        self.tabla.column("#0", width = 100)
        self.tabla.column("Nombre Completo", width = 300)
        self.tabla.column("HC", width = 100)           

        self.tabla.place(x = 850, y = 420)        
        self.tabla.config(height = 10)

        self.tabla.heading("#0", text = "CI")
        self.tabla.heading("Nombre Completo", text = "Nombre Completo")
        self.tabla.heading("HC", text = "HC")              

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
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica` FROM `pacientes` WHERE `ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%' """

            else:
                sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica` FROM `pacientes` WHERE `fecha_cons_presc` = "{self.texto_buscador_fecha.get()}" AND (`ci` LIKE '%{self.texto_buscador_strig.get()}%' OR `historia_clinica` LIKE '%{self.texto_buscador_strig.get()}%' OR `nombre` LIKE '%{self.texto_buscador_strig.get()}%' OR `1er_apellido` LIKE '%{self.texto_buscador_strig.get()}%' OR `2do_apellido` LIKE '%{self.texto_buscador_strig.get()}%') """

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
=======
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
>>>>>>> dac44e66a94edec1fd4f995e92c68c258b5f8f39
autenticacion.mainloop()