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


fecha_actual = datetime.now().date()

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

###################################### creando tabla municipios #############################

try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "oncologico"    
        )
    cursor = conn.cursor()

    sql = """ CREATE TABLE `oncologico`.`municipios` (`municipio` VARCHAR(50) NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    pass

################################### agregando datos a la tabla municipios ###########################

municipios = ["Pinar del Río","Consolación del Sur","Viñales","Guane","Sandino","La Palma","San Luis","Los Palacios","San Juan y Martínez","Mantua","Minas de Matahambre","Ajeno"]
try:
    for index in municipios:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"    
            )
        cursor = conn.cursor()
        sql = f"""INSERT INTO `municipios`(`municipio`) VALUES ('{index}')"""
        cursor.execute(sql)
        conn.commit()
except:
    pass

######################################## crear tabla pacientes #################################
try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "oncologico"    
        )
    cursor = conn.cursor()

    sql = """ CREATE TABLE `oncologico`.`pacientes` (`fecha_registro` DATE NOT NULL , `historia_clinica` INT NOT NULL , `ci` VARCHAR(50) NOT NULL , `nombre` VARCHAR(50) NOT NULL , `1er_apellido` VARCHAR(50) NOT NULL , `2do_apellido` VARCHAR(50) NOT NULL , `edad` INT NOT NULL , `raza` VARCHAR(50) NOT NULL , `municipio` VARCHAR(50) NOT NULL , `sexo` VARCHAR(10) NOT NULL , `fecha_cons_presc` DATE NOT NULL , `curso` INT NOT NULL , `resumen` TEXT NOT NULL , `localizacion` VARCHAR(50) NOT NULL , `t` VARCHAR(10) NOT NULL , `n` VARCHAR(10) NOT NULL , `m` VARCHAR(10) NOT NULL , `estadio` TEXT NOT NULL , `comentario` TEXT NOT NULL ) ENGINE = InnoDB;"""
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

        self.combo_area = ttk.Combobox(self, values=string_areas,font=("Arial",18), width=17) 
        self.combo_area.set("Escoger Area") 
        self.combo_area.place(x=300,y=60)
        

        ############################ usuario #########################
        self.label_usuario = CTkLabel(self, text="Usuario:",font=("Arial",18))  
        self.label_usuario.place(x=100,y=100) 

        string_usuarios = []       

        def asociar_usuario(event):
            self.entry_usuario.delete(0,END)
            self.entry_usuario.insert(0,"Escoger Usuario")
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

        self.combo_area.bind("<<ComboboxSelected>>",asociar_usuario) # esto lo hago para que me salgan los usuarios que le tocan al area seleccionada

        self.entry_usuario = ttk.Combobox(self, values=string_usuarios ,font=("Arial",18), width=17)
        self.entry_usuario.insert(0,"Escoger Usuario")
        self.entry_usuario.place(x=300,y=123)

        ############################## pass ############################
        self.label_pass = CTkLabel(self, text="Password:",font=("Arial",18))  
        self.label_pass.place(x=100,y=150)

        self.entry_pass = Entry(self,font=("Arial",18), width=17, show="*")  
        self.entry_pass.place(x=300,y=190) 
        
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
                                if self.combo_area.get() == "admin":
                                    lobbyadmin = LobbyAdmin()
                                elif self.combo_area.get() == "Recepcion":
                                    print("lobby recepcion")
                                elif self.combo_area.get() == "Medico":
                                    print("lobby medico")
                                elif self.combo_area.get() == "Fisico-Medico":
                                    print("lobby fisico-medico")
                                elif self.combo_area.get() == "Tecnologo":
                                    print("lobby tecnologo")                            
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
                        lobbyadmin = LobbyAdmin()            
                        
                        
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
######################################## lobbyadmin #############################################################
############################################################################################################

class LobbyAdmin(CTkToplevel):
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

        # **************************** fondo *****************************************************
        try:            
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/image2.jpg"), size = (1300,700))                  
            
            label_imagen_lobby = CTkLabel(self, image = self.imagen, text = "")
            label_imagen_lobby.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error","No se encontro foto")

        firma = "Vence (" + str(fecha_vencimiento) + ")"
        self.label_ysos = CTkLabel(self, text = firma, font=("Times New Roman",16))
        self.label_ysos.place(x = 1150, y = 650)

        self.menu = Menu(self)
        self.config(menu=self.menu, width="200", height="100")

        def nuevo_menu_lobby_registro():
            nuevo_paciente = NuevoPaciente()

        def modificar_menu_lobby_registro():
            modificar_paciente = BuscarPacienteModificar()

        def eliminar_menu_lobby_registro():
            eliminar_paciente = BuscarPacienteEliminar()       
        
        registro_menu = Menu(self.menu, tearoff = 0)
        registro_menu.add_command(label="Nuevo", command = nuevo_menu_lobby_registro)
        registro_menu.add_command(label="Modificar", command = modificar_menu_lobby_registro)
        registro_menu.add_command(label="Eliminar", command = eliminar_menu_lobby_registro)

        def nuevo_menu_lobby_prescripcion():
            buscar_paciente_nuevo_prescripcion = BuscarPacienteNuevoPrescripcion()

        def modificar_menu_lobby_prescripcion():
            buscar_paciente_modificar_prescripcion = BuscarPacienteModificarPrescripcion()

        def eliminar_menu_lobby_prescripcion():
            buscar_paciente_eliminar_prescripcion = BuscarPacienteEliminarPrescripcion()
        
        prescripcion_menu = Menu(self.menu, tearoff = 0)
        prescripcion_menu.add_command(label="Nuevo", command = nuevo_menu_lobby_prescripcion)
        prescripcion_menu.add_command(label="Modificar", command = modificar_menu_lobby_prescripcion)
        prescripcion_menu.add_command(label="Eliminar", command = eliminar_menu_lobby_prescripcion)



        def nuevo_menu_lobby_dosimetria():
            pass
        def modificar_menu_lobby_dosimetria():
            pass
        def eliminar_menu_lobby_dosimetria():
            pass

        dosimetria_menu = Menu(self.menu, tearoff = 0)
        dosimetria_menu.add_command(label="Nuevo", command = nuevo_menu_lobby_dosimetria)
        dosimetria_menu.add_command(label="Modificar", command = modificar_menu_lobby_dosimetria)
        dosimetria_menu.add_command(label="Eliminar", command = eliminar_menu_lobby_dosimetria)


        def nuevo_menu_lobby_tratamiento():
            pass
        def modificar_menu_lobby_tratamiento():
            pass
        def eliminar_menu_lobby_tratamiento():
            pass

        tratamiento_menu = Menu(self.menu, tearoff = 0)
        tratamiento_menu.add_command(label="Nuevo", command = nuevo_menu_lobby_tratamiento)
        tratamiento_menu.add_command(label="Modificar", command = modificar_menu_lobby_tratamiento)
        tratamiento_menu.add_command(label="Eliminar", command = eliminar_menu_lobby_tratamiento)

        def nuevo_menu_lobby_seguimiento():
            pass
        def modificar_menu_lobby_seguimiento():
            pass
        def eliminar_menu_lobby_seguimiento():
            pass

        seguimiento_menu = Menu(self.menu, tearoff = 0)
        seguimiento_menu.add_command(label="Nuevo", command = nuevo_menu_lobby_seguimiento)
        seguimiento_menu.add_command(label="Modificar", command = modificar_menu_lobby_seguimiento)
        seguimiento_menu.add_command(label="Eliminar", command = eliminar_menu_lobby_seguimiento)

        def agregar_usuario():
            usuario_agregar = UsuarioAgregar()
        def eliminar_usuario():
            usuario_eliminar = EliminarUsuario()
        
        usuario_menu = Menu(self.menu, tearoff = 0)
        usuario_menu.add_command(label="Agregar", command = agregar_usuario)
        usuario_menu.add_command(label="Eliminar", command = eliminar_usuario)

        def agregar_nueva_licencia():
            licencia = Licencia()

        licencia_menu = Menu(self.menu, tearoff = 0)
        licencia_menu.add_command(label="Nueva", command = agregar_nueva_licencia)

        def cerrar_cesion():
            self.destroy()
            autenticacion.deiconify() 

        def cerrar_programa():
            autenticacion.quit()
            

        salir_menu = Menu(self.menu, tearoff = 0)
        salir_menu.add_command(label="Cerrar Cesion", command = cerrar_cesion)
        salir_menu.add_command(label="Cerrar Programa", command = cerrar_programa)
        
        
        self.menu.add_cascade(label="Registro", menu = registro_menu) 
        self.menu.add_cascade(label="Prescripcion", menu = prescripcion_menu)  
        self.menu.add_cascade(label="Dosimetria", menu = dosimetria_menu)  
        self.menu.add_cascade(label="Tratamiento", menu = tratamiento_menu) 
        self.menu.add_cascade(label="Seguimiento", menu = seguimiento_menu)
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


        texto_nombre_usuario_eliminar = ttk.Combobox(self)
        texto_nombre_usuario_eliminar.place(x = 200 , y = 105)
        texto_nombre_usuario_eliminar['values'] = items_usuarios


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

# **********************************************************************************
# *********************** trabajo con nuevo paciente  ******************************
# **********************************************************************************

class NuevoPaciente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Nuevo Paciente")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/imagen6.jpg"), size = (800,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        # ************************** Labels y Texts *************************        

        self.label_Historia = CTkLabel(self,text="No. Historia Clinica:", font=("Times New Roman",16))
        self.label_Historia.place(x = 50, y = 50)

        self.texto_Historia = CTkEntry(self)
        self.texto_Historia.place(x = 300, y = 50)

        self.label_CI = CTkLabel(self,text="CI:", font=("Times New Roman",16))
        self.label_CI.place(x = 50, y = 90)

        self.texto_CI = CTkEntry(self)
        self.texto_CI.place(x = 300, y = 90)

        self.label_Nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_Nombre.place(x = 50, y = 130)

        self.texto_Nombre = CTkEntry(self)
        self.texto_Nombre.place(x = 300, y = 130)

        self.label_1er = CTkLabel(self,text="1er Apellido:", font=("Times New Roman",16))
        self.label_1er.place(x = 50, y = 170)

        self.texto_1er = CTkEntry(self)
        self.texto_1er.place(x = 300, y = 170)

        self.label_2do = CTkLabel(self,text="2do Apellido", font=("Times New Roman",16))
        self.label_2do.place(x = 50, y = 210)

        self.texto_2do = CTkEntry(self)
        self.texto_2do.place(x = 300, y = 210)

        self.label_Edad = CTkLabel(self,text="Edad", font=("Times New Roman",16))
        self.label_Edad.place(x = 50, y = 250)

        self.texto_Edad = CTkEntry(self)
        self.texto_Edad.place(x = 300, y = 250)

        self.label_Raza = CTkLabel(self,text="Raza:", font=("Times New Roman",16))
        self.label_Raza.place(x = 50, y = 290)
        
        self.string_razas = ["Blanca","Mestiza","Negra"]
        self.texto_Raza = CTkComboBox(self, values=self.string_razas)
        self.texto_Raza.set("")
        self.texto_Raza.place(x = 300, y = 290)
        
        self.label_Municipio = CTkLabel(self,text="Municipio:", font=("Times New Roman",16))
        self.label_Municipio.place(x = 50, y = 330)

        self.string_municipios = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"
            )
        cursor = conn.cursor()
        sql = f""" SELECT * FROM `municipios` """
        cursor.execute(sql)
        for index in cursor:
            self.string_municipios.append(index[0])

        self.texto_Municipio = CTkComboBox(self, values=self.string_municipios)
        self.texto_Municipio.set("")
        self.texto_Municipio.place(x = 300, y = 330)

        self.label_Sexo = CTkLabel(self,text="Sexo:", font=("Times New Roman",16))
        self.label_Sexo.place(x = 50, y = 370)

        self.string_sexo = ["M","F"]
        self.texto_Sexo = CTkComboBox(self,values=self.string_sexo)
        self.texto_Sexo.set("")
        self.texto_Sexo.place(x = 300, y = 370)

        self.label_Prescripcion = CTkLabel(self,text="Fecha Consulta Prescripcion:", font=("Times New Roman",16))
        self.label_Prescripcion.place(x = 50, y = 410)

        # crear boton calendario para agregar la fecha al text        
        def btn_fecha_agregar_paciente():
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
                self.texto_Prescripcion.delete(0,END)                
                fecha_select = cal.get_date()
                self.texto_Prescripcion.insert(0,str(fecha_select))
                calendario.destroy()
            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 

        self.btn_fecha = CTkButton(self,text="...",command=btn_fecha_agregar_paciente, width = 27, height = 27)
        self.btn_fecha.place(x=450 ,y=410 )

        self.texto_Prescripcion = CTkEntry(self)
        self.texto_Prescripcion.place(x = 300, y = 410)

        self.label_Curso = CTkLabel(self,text="No. Curso:", font=("Times New Roman",16))
        self.label_Curso.place(x = 50, y = 450)

        self.texto_Curso = CTkEntry(self)
        self.texto_Curso.place(x = 300, y = 450)


        # **************** botones ********************
        def agregar_paciente_agregar():
            if len(self.texto_CI.get()) != 11:
                error = messagebox.showinfo("error","El carnet esta incorrecto")
            else:
                error = messagebox.askquestion("Agregar","Se agregara el Paciente")
                if error == "yes":
                    # verificar que no esta repetido el CI o que sean cursos diferentes                   
                    existe_ci = False 
                    existe_curso = False

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT * FROM `pacientes` """
                    cursor.execute(sql)
                    for index in cursor:                        
                        if index[2] == self.texto_CI.get():
                            existe_ci = True                                        
                    
                    if existe_ci:
                        error = messagebox.askquestion("Atencion", "Ese CI ya existe, quieres crear un nuevo curso \n para esta persona?")
                        if error == "yes":                            
                            #### necesito comprobar que el curso no es el mismo, solo puede repetirse el carnet si son cursos diferentes
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password = "",
                                database = "oncologico"
                                )
                            cursor = conn.cursor()
                            sql = f""" SELECT `curso` FROM `pacientes` WHERE `ci` = "{self.texto_CI.get()}"; """
                            cursor.execute(sql)
                            for index in cursor:                                
                                if index[0] == int(self.texto_Curso.get()):
                                    existe_curso = True                                

                            if existe_curso:
                                error = messagebox.showinfo("Error","Debes cambiar el Curso de este paciente para poder agregarlo")
                            else:
                                try:
                                    # entramos los datos a la bd
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "root",
                                        password = "",
                                        database = "oncologico"
                                        )
                                    cursor = conn.cursor()
                                    sql = f""" INSERT INTO `pacientes`(`fecha_registro`, `historia_clinica`, `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `edad`, `raza`, `municipio`, `sexo`, `fecha_cons_presc`, `curso`, `resumen`, `localizacion`, `t`, `n`, `m`, `estadio`, `comentario`) 
                                                            VALUES ('{fecha_actual}','{self.texto_Historia.get()}','{self.texto_CI.get()}','{self.texto_Nombre.get()}','{self.texto_1er.get()}','{self.texto_2do.get()}','{int(self.texto_Edad.get())}','{self.texto_Raza.get()}','{self.texto_Municipio.get()}','{self.texto_Sexo.get()}','{self.texto_Prescripcion.get()}','{self.texto_Curso.get()}','-','-','-','-','-','-','-') """
                                    cursor.execute(sql)
                                    conn.commit()
                                    self.destroy()
                                except:
                                    messagebox.showinfo("Error","No se pudieron agregar los datos, agreguelos correctamente")
                                                    
                        
                        else:
                            pass

                    if  not existe_ci:
                        try:
                            # entramos los datos a la bd
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password = "",
                                database = "oncologico"
                                )
                            cursor = conn.cursor()
                            sql = f""" INSERT INTO `pacientes`(`fecha_registro`, `historia_clinica`, `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `edad`, `raza`, `municipio`, `sexo`, `fecha_cons_presc`, `curso`, `resumen`, `localizacion`, `t`, `n`, `m`, `estadio`, `comentario`) 
                                                    VALUES ('{fecha_actual}','{self.texto_Historia.get()}','{self.texto_CI.get()}','{self.texto_Nombre.get()}','{self.texto_1er.get()}','{self.texto_2do.get()}','{int(self.texto_Edad.get())}','{self.texto_Raza.get()}','{self.texto_Municipio.get()}','{self.texto_Sexo.get()}','{self.texto_Prescripcion.get()}','{self.texto_Curso.get()}','-','-','-','-','-','-','-') """
                            cursor.execute(sql)
                            conn.commit()
                            self.destroy()
                        except:
                            messagebox.showinfo("Error","No se pudieron agregar los datos, agreguelos correctamente")

        def cancelar_paciente_agregar():
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=agregar_paciente_agregar, width = 150, height = 40)
        self.btn_aceptar.place(x=100 ,y=600 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_paciente_agregar, width = 150, height = 40)
        self.btn_cancelar.place(x=300 ,y=600 )

#########################################################################################################################
############################################### buscar_paciente #########################################################
#########################################################################################################################
class BuscarPacienteModificar(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Buscar Paciente")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/image2.jpg"), size = (800,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        self.opcion_radio = IntVar()
        
        self.radio_Historia = CTkRadioButton(self,text="Buscar por Historia Clinica:", font=("Times New Roman",16),variable = self.opcion_radio, value = 1)
        self.radio_Historia.place(x = 50, y = 50)

        self.texto_Historia = CTkEntry(self)
        self.texto_Historia.place(x = 280, y = 50)

        self.radio_CI = CTkRadioButton(self,text="Buscar por CI:", font=("Times New Roman",16),variable = self.opcion_radio, value = 2)
        self.radio_CI.place(x = 50, y = 90)

        self.texto_CI = CTkEntry(self)
        self.texto_CI.place(x = 280, y = 90)

        self.radio_Nombre = CTkRadioButton(self,text="Buscar por Nombre:", font=("Times New Roman",16),variable = self.opcion_radio, value = 3)
        self.radio_Nombre.place(x = 50, y = 130)

        self.texto_Nombre = CTkEntry(self)
        self.texto_Nombre.place(x = 280, y = 130)

        self.radio_1er = CTkRadioButton(self,text="Buscar por 1er Apellido:", font=("Times New Roman",16),variable = self.opcion_radio, value = 4)
        self.radio_1er.place(x = 50, y = 170)

        self.texto_1er = CTkEntry(self)
        self.texto_1er.place(x = 280, y = 170)

        self.radio_2do = CTkRadioButton(self,text="Buscar por 2do Apellido:", font=("Times New Roman",16),variable = self.opcion_radio, value = 5)
        self.radio_2do.place(x = 50, y = 210)

        self.texto_2do = CTkEntry(self)
        self.texto_2do.place(x = 280, y = 210)

        self.listado = Listbox(self)
        self.listado.config(selectmode = SINGLE , width = 100 , height = 20)
        self.listado.place(x = 200 , y = 350)

        self.scrollbar = CTkScrollbar(self, command = self.listado.yview, width = 18)
        self.scrollbar.place(in_ = self.listado, relheigh = 1, relx = 1)

        self.listado.config(yscrollcommand = self.scrollbar.set)

        def buscar_ver_paciente():
            try:
                self.listado.delete(0,END)
                lista = ""

                if self.opcion_radio.get() == 1: # esta es la opcion buscar por historia clinica

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `historia_clinica` = {self.texto_Historia.get()}; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4]) 
                        self.listado.insert(END , lista)


                elif self.opcion_radio.get() == 2: # esta es la opcion buscar por CI
                                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `ci` = '{self.texto_CI.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 3: # esta es la opcion buscar por Nombre
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `Nombre` = '{self.texto_Nombre.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 4: # esta es la opcion buscar por 1er apellido
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `1er_apellido` = '{self.texto_1er.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 5: # esta es la opcion buscar por 2do apellido
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `2do_apellido` = '{self.texto_2do.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                else:
                    error = messagebox.showinfo("Error", "Escoja una opcion")
            except:
                pass


        self.btn_buscar = CTkButton(self,text="Buscar",command=buscar_ver_paciente, width = 300, height = 100)
        self.btn_buscar.place(x=450, y = 90)
        
        ## ahora vamos a extraer el ci de la opcion escogida con un click en el listado ##
        def extraer_ci_y_curso_de_seleccion(event):
            try:
                index = self.listado.curselection()
                selected_string = self.listado.get(index)
                global ci_extraido_modificar_registro
                ci_extraido_modificar_registro = selected_string[12:23] # aqui se guardara el carnet de id cuando seleccione una persona en el listbox
                global curso_extraido_modificar_registro
                curso_extraido_modificar_registro = selected_string[7] # aqui  se guarda el curso que esta ejecutando 
                
            except:
                pass
                      

        self.listado.bind("<<ListboxSelect>>", extraer_ci_y_curso_de_seleccion)

        # modificar paciente con doble click en la busqueda 
        def abrir_ventana_vista_paciente(event):
            index = self.listado.curselection()
            selected_string = self.listado.get(index)
            ci_extraido_modificar_registro = selected_string[12:23]
            curso_extraido_modificar_registro = selected_string[7]
            modificar_paciente = ModificarPaciente()


        self.listado.bind("<Double-1>", abrir_ventana_vista_paciente)

        
        def modificar_ver_paciente():
            modificar_paciente = ModificarPaciente()


        self.btn_modificar = CTkButton(self,text="Modificar",command=modificar_ver_paciente, width = 500, height = 60)
        self.btn_modificar.place(x=150, y = 600)

        


#################################################################################################################################
################################################ modificar paciente  ############################################################
#################################################################################################################################
class ModificarPaciente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Modificar Paciente para Modificar")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/imagen6.jpg"), size = (800,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        # ************************** Labels y Texts *************************        

        self.label_Registro = CTkLabel(self,text="Fecha Registro:", font=("Times New Roman",16))
        self.label_Registro.place(x = 50, y = 50)

        def btn_fecha_registro_modificar_paciente():
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
                self.texto_Registro_modificar.delete(0,END)                
                fecha_select = cal.get_date()
                self.texto_Registro_modificar.insert(0,str(fecha_select))
                calendario.destroy()
            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 

        self.btn_fecha_registro = CTkButton(self,text="...",command=btn_fecha_registro_modificar_paciente, width = 27, height = 27)
        self.btn_fecha_registro.place(x=450 ,y=50 )

        self.texto_Registro_modificar = CTkEntry(self)
        self.texto_Registro_modificar.place(x = 300, y = 50)
        
        self.label_Historia = CTkLabel(self,text="No. Historia Clinica:", font=("Times New Roman",16))
        self.label_Historia.place(x = 50, y = 90)

        self.texto_Historia_modificar = CTkEntry(self)
        self.texto_Historia_modificar.place(x = 300, y = 90)

        self.label_CI = CTkLabel(self,text="CI:", font=("Times New Roman",16))
        self.label_CI.place(x = 50, y = 130)

        self.texto_CI_modificar = CTkEntry(self)
        self.texto_CI_modificar.place(x = 300, y = 130)

        self.label_Nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_Nombre.place(x = 50, y = 170)

        self.texto_Nombre_modificar = CTkEntry(self)
        self.texto_Nombre_modificar.place(x = 300, y = 170)

        self.label_1er = CTkLabel(self,text="1er Apellido:", font=("Times New Roman",16))
        self.label_1er.place(x = 50, y = 210)

        self.texto_1er_modificar = CTkEntry(self)
        self.texto_1er_modificar.place(x = 300, y = 210)

        self.label_2do = CTkLabel(self,text="2do Apellido", font=("Times New Roman",16))
        self.label_2do.place(x = 50, y = 250)

        self.texto_2do_modificar = CTkEntry(self)
        self.texto_2do_modificar.place(x = 300, y = 250)

        self.label_Edad = CTkLabel(self,text="Edad", font=("Times New Roman",16))
        self.label_Edad.place(x = 50, y = 290)

        self.texto_Edad_modificar = CTkEntry(self)
        self.texto_Edad_modificar.place(x = 300, y = 290)

        self.label_Raza = CTkLabel(self,text="Raza:", font=("Times New Roman",16))
        self.label_Raza.place(x = 50, y = 330)
        
        self.string_razas = ["Blanco","Mestizo","Negro"]
        self.texto_Raza_modificar = CTkComboBox(self, values=self.string_razas)
        self.texto_Raza_modificar.place(x = 300, y = 330)
        
        self.label_Municipio = CTkLabel(self,text="Municipio:", font=("Times New Roman",16))
        self.label_Municipio.place(x = 50, y = 370)

        self.string_municipios = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"
            )
        cursor = conn.cursor()
        sql = f""" SELECT * FROM `municipios` """
        cursor.execute(sql)
        for index in cursor:
            self.string_municipios.append(index[0])

        self.texto_Municipio_modificar = CTkComboBox(self, values=self.string_municipios)
        self.texto_Municipio_modificar.place(x = 300, y = 370)

        self.label_Sexo = CTkLabel(self,text="Sexo:", font=("Times New Roman",16))
        self.label_Sexo.place(x = 50, y = 410)

        self.string_sexo = ["M","F"]
        self.texto_Sexo_modificar = CTkComboBox(self,values=self.string_sexo)
        self.texto_Sexo_modificar.place(x = 300, y = 410)

        self.label_Prescripcion = CTkLabel(self,text="Fecha Consulta Prescripcion:", font=("Times New Roman",16))
        self.label_Prescripcion.place(x = 50, y = 450)

        # crear boton calendario para agregar la fecha al text        
        def btn_fecha_modificar_paciente():
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
                self.texto_Prescripcion_modificar.delete(0,END)                
                fecha_select = cal.get_date()
                self.texto_Prescripcion_modificar.insert(0,str(fecha_select))
                calendario.destroy()
            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 

        self.btn_fecha_prescripcion = CTkButton(self,text="...",command=btn_fecha_modificar_paciente, width = 27, height = 27)
        self.btn_fecha_prescripcion.place(x=450 ,y=450 )

        self.texto_Prescripcion_modificar = CTkEntry(self)
        self.texto_Prescripcion_modificar.place(x = 300, y = 450)

        self.label_Curso = CTkLabel(self,text="No. Curso:", font=("Times New Roman",16))
        self.label_Curso.place(x = 50, y = 490)

        self.texto_Curso_modificar = CTkEntry(self)
        self.texto_Curso_modificar.place(x = 300, y = 490) 

        ################ vamos a mostrar en los text lo que esta actualmente, antes del cambio ###############
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"
            )
        cursor = conn.cursor()
        sql = f""" SELECT * FROM `pacientes` WHERE `ci` = '{ci_extraido_modificar_registro}' and `curso` = {curso_extraido_modificar_registro}; """
        cursor.execute(sql)
        for index in cursor:
            self.texto_Registro_modificar.insert(0,str(index[0]))
            self.texto_Historia_modificar.insert(0,str(index[1]))
            self.texto_CI_modificar.insert(0,index[2])
            self.texto_Nombre_modificar.insert(0,index[3])
            self.texto_1er_modificar.insert(0,index[4])
            self.texto_2do_modificar.insert(0,index[5])
            self.texto_Edad_modificar.insert(0,index[6])
            self.texto_Raza_modificar.set(index[7])
            self.texto_Municipio_modificar.set(index[8])
            self.texto_Sexo_modificar.set(index[9])
            self.texto_Prescripcion_modificar.insert(0,str(index[10]))
            self.texto_Curso_modificar.insert(0,index[11])
        
        # **************** botones ********************
        def modificar_paciente_modificar1():
            if len(self.texto_CI_modificar.get()) != 11:
                error = messagebox.showinfo("error","El carnet esta incorrecto")
            else:
                error = messagebox.askquestion("Modificar","Se modificara el Paciente")
                if error == "yes":
                    try:
                        # actualizamos los datos de la bd
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "",
                            database = "oncologico"
                            )
                        cursor = conn.cursor()
                        sql = f""" UPDATE `pacientes` SET `fecha_registro`='{self.texto_Registro_modificar.get()}',`historia_clinica`='{self.texto_Historia_modificar.get()}',`ci`='{self.texto_CI_modificar.get()}',
                                   `nombre`='{self.texto_Nombre_modificar.get()}',`1er_apellido`='{self.texto_1er_modificar.get()}',`2do_apellido`='{self.texto_2do_modificar.get()}',`edad`='{self.texto_Edad_modificar.get()}',`raza`='{self.texto_Raza_modificar.get()}',
                                   `municipio`='{self.texto_Municipio_modificar.get()}',`sexo`='{self.texto_Sexo_modificar.get()}',`fecha_cons_presc`='{self.texto_Prescripcion_modificar.get()}',`curso`='{self.texto_Curso_modificar.get()}',`resumen`='-',
                                   `localizacion`='-',`t`='-',`n`='-',`m`='-',`estadio`='-',`comentario`='-' 
                                   WHERE `ci`='{ci_extraido_modificar_registro}' and `curso` = {curso_extraido_modificar_registro} """
                        cursor.execute(sql)
                        conn.commit()
                        self.destroy()
                    except:
                        messagebox.showinfo("Error","No se pudieron modificar los datos, agreguelos correctamente en los campos correspondientes")

        def cancelar_paciente_modificar1():
            self.destroy()        

        self.btn_aceptar = CTkButton(self,text="Modificar",command=modificar_paciente_modificar1, width = 150, height = 40)
        self.btn_aceptar.place(x=150 ,y=600 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_paciente_modificar1, width = 150, height = 40)
        self.btn_cancelar.place(x=400 ,y=600 )

#########################################################################################################################
############################################### buscar_paciente_eliminar ################################################
#########################################################################################################################
class BuscarPacienteEliminar(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Buscar Paciente para Eliminar")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/image2.jpg"), size = (800,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        self.opcion_radio = IntVar()
        
        self.radio_Historia = CTkRadioButton(self,text="Buscar por Historia Clinica:", font=("Times New Roman",16),variable = self.opcion_radio, value = 1)
        self.radio_Historia.place(x = 50, y = 50)

        self.texto_Historia = CTkEntry(self)
        self.texto_Historia.place(x = 280, y = 50)

        self.radio_CI = CTkRadioButton(self,text="Buscar por CI:", font=("Times New Roman",16),variable = self.opcion_radio, value = 2)
        self.radio_CI.place(x = 50, y = 90)

        self.texto_CI = CTkEntry(self)
        self.texto_CI.place(x = 280, y = 90)

        self.radio_Nombre = CTkRadioButton(self,text="Buscar por Nombre:", font=("Times New Roman",16),variable = self.opcion_radio, value = 3)
        self.radio_Nombre.place(x = 50, y = 130)

        self.texto_Nombre = CTkEntry(self)
        self.texto_Nombre.place(x = 280, y = 130)

        self.radio_1er = CTkRadioButton(self,text="Buscar por 1er Apellido:", font=("Times New Roman",16),variable = self.opcion_radio, value = 4)
        self.radio_1er.place(x = 50, y = 170)

        self.texto_1er = CTkEntry(self)
        self.texto_1er.place(x = 280, y = 170)

        self.radio_2do = CTkRadioButton(self,text="Buscar por 2do Apellido:", font=("Times New Roman",16),variable = self.opcion_radio, value = 5)
        self.radio_2do.place(x = 50, y = 210)

        self.texto_2do = CTkEntry(self)
        self.texto_2do.place(x = 280, y = 210)

        self.listado = Listbox(self)
        self.listado.config(selectmode = SINGLE , width = 100 , height = 20)
        self.listado.place(x = 200 , y = 350)

        self.scrollbar = CTkScrollbar(self, command = self.listado.yview, width = 18)
        self.scrollbar.place(in_ = self.listado, relheigh = 1, relx = 1)

        self.listado.config(yscrollcommand = self.scrollbar.set)

        def buscar_ver_paciente():
            try:
                self.listado.delete(0,END)
                lista = ""

                if self.opcion_radio.get() == 1: # esta es la opcion buscar por historia clinica

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `historia_clinica` = {self.texto_Historia.get()}; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4]) 
                        self.listado.insert(END , lista)


                elif self.opcion_radio.get() == 2: # esta es la opcion buscar por CI
                                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `ci` = '{self.texto_CI.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 3: # esta es la opcion buscar por Nombre
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `Nombre` = '{self.texto_Nombre.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 4: # esta es la opcion buscar por 1er apellido
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `1er_apellido` = '{self.texto_1er.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 5: # esta es la opcion buscar por 2do apellido
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `2do_apellido` = '{self.texto_2do.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                else:
                    error = messagebox.showinfo("Error", "Escoja una opcion")
            except:
                pass


        self.btn_buscar = CTkButton(self,text="Buscar",command=buscar_ver_paciente, width = 300, height = 100)
        self.btn_buscar.place(x=450, y = 90)
        
        ## ahora vamos a extraer el ci de la opcion escogida con un click en el listado ##
        def extraer_ci_de_seleccion(event):
            try:
                index = self.listado.curselection()
                selected_string = self.listado.get(index)
                global ci_extraido_eliminar_registro
                ci_extraido_eliminar_registro = selected_string[12:23] # aqui se guardara el carnet de id cuando seleccione una persona en el listbox
                global curso_extraido_eliminar_registro
                curso_extraido_eliminar_registro = selected_string[7] # aqui  se guarda el curso que esta ejecutando 
            except:
                pass
                      

        self.listado.bind("<<ListboxSelect>>", extraer_ci_de_seleccion)

        ## eliminamos con el 2ble click
        def abrir_ventana_vista_paciente(event):
            index = self.listado.curselection()
            selected_string = self.listado.get(index)
            ci_extraido_eliminar_registro = selected_string[12:23]
            curso_extraido_eliminar_registro = selected_string[7]
            cuidado = messagebox.askquestion("Delete","Se borraran los datos del Paciente")
            if cuidado == "yes":                
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "oncologico"
                    )
                cursor = conn.cursor()
                sql = f""" DELETE FROM `pacientes` WHERE `ci` = '{ci_extraido_eliminar_registro}' and `curso` = {curso_extraido_eliminar_registro};"""
                cursor.execute(sql) 
                conn.commit()    


        self.listado.bind("<Double-1>", abrir_ventana_vista_paciente)

        

        def eliminar_ver_paciente():
            cuidado = messagebox.askquestion("Delete","Se borraran los datos del Paciente")
            if cuidado == "yes":                
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "oncologico"
                    )
                cursor = conn.cursor()
                sql = f""" DELETE FROM `pacientes` WHERE `ci` = '{ci_extraido_eliminar_registro}' and `curso` = {curso_extraido_eliminar_registro};"""
                cursor.execute(sql) 
                conn.commit()

        self.btn_eliminar = CTkButton(self,text="Eliminar",command=eliminar_ver_paciente, width = 500, height = 60)
        self.btn_eliminar.place(x=150, y = 600)

##############################################################################################################################
####################################### buscar para prescripcion #############################################################
##############################################################################################################################

class BuscarPacienteNuevoPrescripcion(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Buscar para Prescripcion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/image2.jpg"), size = (800,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        self.opcion_radio = IntVar()
        
        self.radio_Historia = CTkRadioButton(self,text="Buscar por Historia Clinica:", font=("Times New Roman",16),variable = self.opcion_radio, value = 1)
        self.radio_Historia.place(x = 50, y = 50)

        self.texto_Historia = CTkEntry(self)
        self.texto_Historia.place(x = 280, y = 50)

        self.radio_CI = CTkRadioButton(self,text="Buscar por CI:", font=("Times New Roman",16),variable = self.opcion_radio, value = 2)
        self.radio_CI.place(x = 50, y = 90)

        self.texto_CI = CTkEntry(self)
        self.texto_CI.place(x = 280, y = 90)

        self.radio_Nombre = CTkRadioButton(self,text="Buscar por Nombre:", font=("Times New Roman",16),variable = self.opcion_radio, value = 3)
        self.radio_Nombre.place(x = 50, y = 130)

        self.texto_Nombre = CTkEntry(self)
        self.texto_Nombre.place(x = 280, y = 130)

        self.radio_1er = CTkRadioButton(self,text="Buscar por 1er Apellido:", font=("Times New Roman",16),variable = self.opcion_radio, value = 4)
        self.radio_1er.place(x = 50, y = 170)

        self.texto_1er = CTkEntry(self)
        self.texto_1er.place(x = 280, y = 170)

        self.radio_2do = CTkRadioButton(self,text="Buscar por 2do Apellido:", font=("Times New Roman",16),variable = self.opcion_radio, value = 5)
        self.radio_2do.place(x = 50, y = 210)

        self.texto_2do = CTkEntry(self)
        self.texto_2do.place(x = 280, y = 210)

        self.listado = Listbox(self)
        self.listado.config(selectmode = SINGLE , width = 100 , height = 20)
        self.listado.place(x = 200 , y = 350)

        self.scrollbar = CTkScrollbar(self, command = self.listado.yview, width = 18)
        self.scrollbar.place(in_ = self.listado, relheigh = 1, relx = 1)

        self.listado.config(yscrollcommand = self.scrollbar.set)

        def buscar_ver_paciente():
            try:
                self.listado.delete(0,END)
                lista = ""

                if self.opcion_radio.get() == 1: # esta es la opcion buscar por historia clinica

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `historia_clinica` = {self.texto_Historia.get()}; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4]) 
                        self.listado.insert(END , lista)


                elif self.opcion_radio.get() == 2: # esta es la opcion buscar por CI
                                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `ci` = '{self.texto_CI.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 3: # esta es la opcion buscar por Nombre
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `Nombre` = '{self.texto_Nombre.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 4: # esta es la opcion buscar por 1er apellido
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `1er_apellido` = '{self.texto_1er.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 5: # esta es la opcion buscar por 2do apellido
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `2do_apellido` = '{self.texto_2do.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                else:
                    error = messagebox.showinfo("Error", "Escoja una opcion")
            except:
                pass


        self.btn_buscar = CTkButton(self,text="Buscar",command=buscar_ver_paciente, width = 300, height = 100)
        self.btn_buscar.place(x=450, y = 90)
        
        ## abrimos la prescripcion dando 2ble click

        def abrir_ventana_nuevo_prescripcion_paciente(event):
            index = self.listado.curselection()
            selected_string = self.listado.get(index)
            global ci_extraido_nueva_prescripcion
            ci_extraido_nueva_prescripcion = selected_string[12:23]
            global curso_extraido_nueva_prescripcion
            curso_extraido_nueva_prescripcion = selected_string[7]

            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()
            sql = f""" SELECT * FROM `pacientes` WHERE `ci` = '{ci_extraido_nueva_prescripcion}' and `curso` = {curso_extraido_nueva_prescripcion}; """
            cursor.execute(sql) 
            for index in cursor:

                global string_label_registro_vista_paciente
                string_label_registro_vista_paciente = StringVar()           
                string_label_registro_vista_paciente.set(f"Fecha Registro: {str(index[0])}")

                global string_label_historia_vista_paciente      
                string_label_historia_vista_paciente = StringVar()           
                string_label_historia_vista_paciente.set(f"Historia Clinica: {index[1]}")

                global string_label_ci_vista_paciente
                string_label_ci_vista_paciente = StringVar()
                string_label_ci_vista_paciente.set(f"CI: {index[2]}")

                global string_label_Nombre_vista_paciente
                string_label_Nombre_vista_paciente = StringVar()
                string_label_Nombre_vista_paciente.set(f"Nombre: {index[3]}")

                global string_label_1er_vista_paciente
                string_label_1er_vista_paciente = StringVar()
                string_label_1er_vista_paciente.set(f"1er Apellido: {index[4]}")

                global string_label_2do_vista_paciente
                string_label_2do_vista_paciente = StringVar()
                string_label_2do_vista_paciente.set(f"2do Apellido: {index[5]}")

                global string_label_Edad_vista_paciente
                string_label_Edad_vista_paciente = StringVar()
                string_label_Edad_vista_paciente.set(f"Edad: {index[6]}")

                global string_label_Raza_vista_paciente
                string_label_Raza_vista_paciente = StringVar()
                string_label_Raza_vista_paciente.set(f"Raza: {index[7]}")

                global string_label_Municipio_vista_paciente
                string_label_Municipio_vista_paciente = StringVar() 
                string_label_Municipio_vista_paciente.set(f"Municipio: {index[8]}")

                global string_label_Sexo_vista_paciente
                string_label_Sexo_vista_paciente = StringVar()
                string_label_Sexo_vista_paciente.set(f"Sexo: {index[9]}")

                global string_label_Prescripcion_vista_paciente
                string_label_Prescripcion_vista_paciente = StringVar()
                string_label_Prescripcion_vista_paciente.set(f"Fecha Prescripcion: {index[10]}")

                global string_label_Curso_vista_paciente
                string_label_Curso_vista_paciente = StringVar()
                string_label_Curso_vista_paciente.set(f"Curso: {index[11]}")                
                
                try:
                    global imagen_foto_nueva_prescripcion
                    imagen_foto_nueva_prescripcion = CTkImage(Image.open(f"D:/Oncologico/imagenes/Pacientes/{ci_extraido_nueva_prescripcion}.jpg"), size = (300,300))
                except:
                    error = messagebox.showinfo("Error", "No hay foto")

            nuevoprescripcion_paciente = NuevoPrescripcionPaciente()

        self.listado.bind("<Double-1>", abrir_ventana_nuevo_prescripcion_paciente)


#########################################################################################################################
######################################## nuevo_prescripcion_paciente ####################################################
#########################################################################################################################

class NuevoPrescripcionPaciente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Nueva Prescripcion Paciente")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/imagen6.jpg"), size = (1000,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        # ************************** Labels  ************************* 
                
        self.label_registro = CTkLabel(self,textvariable = string_label_registro_vista_paciente, font=("Times New Roman",16))
        self.label_registro.place(x = 50, y = 50)
        
        self.label_Historia = CTkLabel(self,textvariable = string_label_historia_vista_paciente, font=("Times New Roman",16))
        self.label_Historia.place(x = 50, y = 90)
                
        self.label_CI = CTkLabel(self,textvariable = string_label_ci_vista_paciente, font=("Times New Roman",16))
        self.label_CI.place(x = 50, y = 130)
                
        self.label_Nombre = CTkLabel(self,textvariable = string_label_Nombre_vista_paciente, font=("Times New Roman",16))
        self.label_Nombre.place(x = 50, y = 170)
                
        self.label_1er = CTkLabel(self,textvariable = string_label_1er_vista_paciente, font=("Times New Roman",16))
        self.label_1er.place(x = 50, y = 210)
                
        self.label_2do = CTkLabel(self,textvariable = string_label_2do_vista_paciente, font=("Times New Roman",16))
        self.label_2do.place(x = 50, y = 250)
                
        self.label_Edad = CTkLabel(self,textvariable = string_label_Edad_vista_paciente, font=("Times New Roman",16))
        self.label_Edad.place(x = 50, y = 290)
                
        self.label_Raza = CTkLabel(self,textvariable = string_label_Raza_vista_paciente, font=("Times New Roman",16))
        self.label_Raza.place(x = 50, y = 330)
                       
        self.label_Municipio = CTkLabel(self,textvariable = string_label_Municipio_vista_paciente, font=("Times New Roman",16))
        self.label_Municipio.place(x = 50, y = 370)
        
        self.label_Sexo = CTkLabel(self,textvariable = string_label_Sexo_vista_paciente, font=("Times New Roman",16))
        self.label_Sexo.place(x = 50, y = 410)
                
        self.label_Prescripcion = CTkLabel(self,textvariable = string_label_Prescripcion_vista_paciente, font=("Times New Roman",16))
        self.label_Prescripcion.place(x = 50, y = 450)
                
        self.label_Curso = CTkLabel(self,textvariable = string_label_Curso_vista_paciente, font=("Times New Roman",16))
        self.label_Curso.place(x = 50, y = 490)

        ########################################## text #################################################

        self.label_Resumen = CTkLabel(self,text= "Resumen:", font=("Times New Roman",16))
        self.label_Resumen.place(x = 300, y = 310)

        self.text_Resumen = CTkTextbox(self,width=500,height=150)
        self.text_Resumen.place(x = 450, y = 310)

        self.label_Localizacion = CTkLabel(self,text="Localizacion:", font=("Times New Roman",16))
        self.label_Localizacion.place(x = 300, y = 50)

        self.text_Localizacion = CTkEntry(self)
        self.text_Localizacion.place(x = 450, y = 50)

        self.label_T = CTkLabel(self,text="T:", font=("Times New Roman",16))
        self.label_T.place(x = 300, y = 90)

        self.text_T = CTkEntry(self,width=30)
        self.text_T.place(x = 320, y = 90)

        self.label_N = CTkLabel(self,text="N:", font=("Times New Roman",16))
        self.label_N.place(x = 350, y = 90)

        self.text_N = CTkEntry(self,width=30)
        self.text_N.place(x = 370, y = 90)

        self.label_M = CTkLabel(self,text="M:", font=("Times New Roman",16))
        self.label_M.place(x = 400, y = 90)

        self.text_M = CTkEntry(self,width=30)
        self.text_M.place(x = 420, y = 90)

        self.label_Estadio = CTkLabel(self,text="Estadio:", font=("Times New Roman",16))
        self.label_Estadio.place(x = 300, y = 130)

        self.text_Estadio = CTkEntry(self)
        self.text_Estadio.place(x = 450, y = 130)

        self.label_Comentario = CTkLabel(self,text="Comentario:", font=("Times New Roman",16))
        self.label_Comentario.place(x = 300, y = 500)

        self.text_Comentario = CTkTextbox(self,width=500,height=150)
        self.text_Comentario.place(x = 450, y = 500) 

        try:           
            self.label_imagen_foto = CTkLabel(self, image = imagen_foto_nueva_prescripcion, text = "")
            self.label_imagen_foto.place(x = 700 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        def tabla_dosis_vista_paciente():
            tabla_dosis_vista = TablaDosisNuevoPrescripcion()

        self.btn = CTkButton(self,text="Tabla Dosis", font=("Times New Roman",16),width=200,height=50, command=tabla_dosis_vista_paciente)
        self.btn.place(x=50,y=550)

        def agregar_info_nueva_prescripcion():
            error = messagebox.askquestion("Prescribir","Se va a prescribir el Paciente")
            if error == "yes":
                try:
                    # actualizamos los datos de la bd
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" UPDATE `pacientes` SET `resumen`='{self.text_Resumen.get("1.0","end")}', `localizacion`='{self.text_Localizacion.get()}',
                                `t`='{self.text_T.get()}',`n`='{self.text_N.get()}',`m`='{self.text_M.get()}',`estadio`='{self.text_Estadio.get()}',
                                `comentario`='{self.text_Comentario.get("1.0","end")}' WHERE `ci`='{ci_extraido_nueva_prescripcion}' and `curso` = {curso_extraido_nueva_prescripcion} """
                    cursor.execute(sql)
                    conn.commit()
                    self.destroy()
                except:
                    messagebox.showinfo("Error","No se pudo prescribir el paciente, revise que la informacion se halla agregado correctamente")


        self.btn2 = CTkButton(self,text="Prescribir", font=("Times New Roman",16),width=200,height=50, command=agregar_info_nueva_prescripcion)
        self.btn2.place(x=50,y=610)


###########################################################################################################################
######################################### tabla dosis nuevo prescripcion ##################################################
###########################################################################################################################
class TablaDosisNuevoPrescripcion(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Tabla Dosis Nueva Prescripcion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/image2.jpg"), size = (1000,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        # hagamos la tabla de las dosis

        self.tabla_dosis = ttk.Treeview(self, columns = ("volumen", "dosis_fraccion", "fraccion", "dosis"))
        self.tabla_dosis.column("#0", width = 120)
        self.tabla_dosis.column("volumen", width = 200)
        self.tabla_dosis.column("dosis_fraccion", width = 200)
        self.tabla_dosis.column("fraccion", width = 200)
        self.tabla_dosis.column("dosis", width = 200)
        
        self.tabla_dosis.place(x = 150, y = 150)
        self.tabla_dosis.config(height = 15)

        self.tabla_dosis.heading("#0", text = "Fecha")
        self.tabla_dosis.heading("volumen", text = "Volumen a Tratar")
        self.tabla_dosis.heading("dosis_fraccion", text = "Dosis x Fraccion [cGy]")
        self.tabla_dosis.heading("fraccion", text = "Fraccion")
        self.tabla_dosis.heading("dosis", text = "Dosis [cGy]")   

        # vamos a llenar la tabla con los elementos de la bd 
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"
            )
        cursor = conn.cursor()
        sql = f""" SELECT * FROM `dosis` WHERE `ci` = "{ci_extraido_nueva_prescripcion}" and `curso` = {curso_extraido_nueva_prescripcion} """
        cursor.execute(sql)
        for index in cursor:
            self.tabla_dosis.insert("", END , text =f"{index[1]}", values = (f"{index[4]}",f"{index[5]}", f"{index[6]}", f"{index[7]}"))

        self.scrollbar_dosis = CTkScrollbar(self, command = self.tabla_dosis.yview, width = 18)
        self.scrollbar_dosis.place(in_ = self.tabla_dosis, relheigh = 1, relx = 1)

        self.tabla_dosis.config(yscrollcommand = self.scrollbar_dosis.set)

        self.label_agregar = CTkLabel(self, text="Agregar", font=("Times New Roman",16))
        self.label_agregar.place(x=50,y=400)

        self.label_volumen = CTkLabel(self, text="Volumen", font=("Times New Roman",16))
        self.label_volumen.place(x=150,y=450)

        self.text_volumen = CTkEntry(self)
        self.text_volumen.place(x=150,y=490)

        self.label_d_f = CTkLabel(self, text="Dosis x Fraccion", font=("Times New Roman",16))
        self.label_d_f.place(x=350,y=450)

        self.text_d_f = CTkEntry(self)
        self.text_d_f.place(x=350,y=490)

        self.label_f = CTkLabel(self, text="Fraccion", font=("Times New Roman",16))
        self.label_f.place(x=550,y=450)

        self.text_f = CTkEntry(self)
        self.text_f.place(x=550,y=490)

        
        def agregar_dosis_nuevo():
            #primero veamis cual es el id de la dosis que insertaremos
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()
            sql = f""" SELECT MAX(`id`) FROM `dosis` """
            cursor.execute(sql)
            for index in cursor:
                if index[0] == None:
                    id_dosis = 1 
                else:
                    id_dosis = index[0] + 1           

            # segundo hay que agregar la info a la bd
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()
            sql = f""" INSERT INTO `dosis`(`id`, `fecha`, `ci`, `curso`, `volumen`, `dosis_x_fraccion`, `fx`, `dosis`, `fx_vencidas`, `dosis_restante`) 
                      VALUES ('{id_dosis}','{fecha_actual}','{ci_extraido_nueva_prescripcion}','{curso_extraido_nueva_prescripcion}','{self.text_volumen.get()}','{float(self.text_d_f.get())}','{int(self.text_f.get())}','{float(self.text_d_f.get())*int(self.text_f.get())}','0','{float(self.text_d_f.get())*int(self.text_f.get())}') """
            cursor.execute(sql)
            conn.commit()

            # ahora hay que agregarlo a la tabla de la ventana
            self.tabla_dosis.insert("", END , text = fecha_actual, values = (f"{self.text_volumen.get()}",f"{float(self.text_d_f.get())}", f"{int(self.text_f.get())}", f"{float(self.text_d_f.get())*int(self.text_f.get())}"))

        self.btn_agregar = CTkButton(self,text="Agregar",command=agregar_dosis_nuevo,height=60,width=200)
        self.btn_agregar.place(x=325,y=550)




###########################################################################################################################
################################# buscar para modificar prescripcion ######################################################
###########################################################################################################################

class BuscarPacienteModificarPrescripcion(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Buscar para Modificar Prescripcion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/image2.jpg"), size = (800,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        self.opcion_radio = IntVar()
        
        self.radio_Historia = CTkRadioButton(self,text="Buscar por Historia Clinica:", font=("Times New Roman",16),variable = self.opcion_radio, value = 1)
        self.radio_Historia.place(x = 50, y = 50)

        self.texto_Historia = CTkEntry(self)
        self.texto_Historia.place(x = 280, y = 50)

        self.radio_CI = CTkRadioButton(self,text="Buscar por CI:", font=("Times New Roman",16),variable = self.opcion_radio, value = 2)
        self.radio_CI.place(x = 50, y = 90)

        self.texto_CI = CTkEntry(self)
        self.texto_CI.place(x = 280, y = 90)

        self.radio_Nombre = CTkRadioButton(self,text="Buscar por Nombre:", font=("Times New Roman",16),variable = self.opcion_radio, value = 3)
        self.radio_Nombre.place(x = 50, y = 130)

        self.texto_Nombre = CTkEntry(self)
        self.texto_Nombre.place(x = 280, y = 130)

        self.radio_1er = CTkRadioButton(self,text="Buscar por 1er Apellido:", font=("Times New Roman",16),variable = self.opcion_radio, value = 4)
        self.radio_1er.place(x = 50, y = 170)

        self.texto_1er = CTkEntry(self)
        self.texto_1er.place(x = 280, y = 170)

        self.radio_2do = CTkRadioButton(self,text="Buscar por 2do Apellido:", font=("Times New Roman",16),variable = self.opcion_radio, value = 5)
        self.radio_2do.place(x = 50, y = 210)

        self.texto_2do = CTkEntry(self)
        self.texto_2do.place(x = 280, y = 210)

        self.listado = Listbox(self)
        self.listado.config(selectmode = SINGLE , width = 100 , height = 20)
        self.listado.place(x = 200 , y = 350)

        self.scrollbar = CTkScrollbar(self, command = self.listado.yview, width = 18)
        self.scrollbar.place(in_ = self.listado, relheigh = 1, relx = 1)

        self.listado.config(yscrollcommand = self.scrollbar.set)

        def buscar_ver_paciente():
            try:
                self.listado.delete(0,END)
                lista = ""

                if self.opcion_radio.get() == 1: # esta es la opcion buscar por historia clinica

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `historia_clinica` = {self.texto_Historia.get()}; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4]) 
                        self.listado.insert(END , lista)


                elif self.opcion_radio.get() == 2: # esta es la opcion buscar por CI
                                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `ci` = '{self.texto_CI.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 3: # esta es la opcion buscar por Nombre
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `Nombre` = '{self.texto_Nombre.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 4: # esta es la opcion buscar por 1er apellido
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `1er_apellido` = '{self.texto_1er.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 5: # esta es la opcion buscar por 2do apellido
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `2do_apellido` = '{self.texto_2do.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                else:
                    error = messagebox.showinfo("Error", "Escoja una opcion")
            except:
                pass


        self.btn_buscar = CTkButton(self,text="Buscar",command=buscar_ver_paciente, width = 300, height = 100)
        self.btn_buscar.place(x=450, y = 90)
        
        ## abrimos la prescripcion dando 2ble click

        def abrir_ventana_modificar_prescripcion_paciente(event):
            index = self.listado.curselection()
            selected_string = self.listado.get(index)
            global ci_extraido_modificar_prescripcion
            ci_extraido_modificar_prescripcion = selected_string[12:23]
            global curso_extraido_modificar_prescripcion
            curso_extraido_modificar_prescripcion = selected_string[7]
            

            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()
            sql = f""" SELECT * FROM `pacientes` WHERE `ci` = '{ci_extraido_modificar_prescripcion}' and `curso` = {curso_extraido_modificar_prescripcion}; """
            cursor.execute(sql) 
            for index in cursor:

                global string_label_registro_vista_paciente
                string_label_registro_vista_paciente = StringVar()           
                string_label_registro_vista_paciente.set(f"Fecha Registro: {str(index[0])}")

                global string_label_historia_vista_paciente      
                string_label_historia_vista_paciente = StringVar()           
                string_label_historia_vista_paciente.set(f"Historia Clinica: {index[1]}")

                global string_label_ci_vista_paciente
                string_label_ci_vista_paciente = StringVar()
                string_label_ci_vista_paciente.set(f"CI: {index[2]}")

                global string_label_Nombre_vista_paciente
                string_label_Nombre_vista_paciente = StringVar()
                string_label_Nombre_vista_paciente.set(f"Nombre: {index[3]}")

                global string_label_1er_vista_paciente
                string_label_1er_vista_paciente = StringVar()
                string_label_1er_vista_paciente.set(f"1er Apellido: {index[4]}")

                global string_label_2do_vista_paciente
                string_label_2do_vista_paciente = StringVar()
                string_label_2do_vista_paciente.set(f"2do Apellido: {index[5]}")

                global string_label_Edad_vista_paciente
                string_label_Edad_vista_paciente = StringVar()
                string_label_Edad_vista_paciente.set(f"Edad: {index[6]}")

                global string_label_Raza_vista_paciente
                string_label_Raza_vista_paciente = StringVar()
                string_label_Raza_vista_paciente.set(f"Raza: {index[7]}")

                global string_label_Municipio_vista_paciente
                string_label_Municipio_vista_paciente = StringVar() 
                string_label_Municipio_vista_paciente.set(f"Municipio: {index[8]}")

                global string_label_Sexo_vista_paciente
                string_label_Sexo_vista_paciente = StringVar()
                string_label_Sexo_vista_paciente.set(f"Sexo: {index[9]}")

                global string_label_Prescripcion_vista_paciente
                string_label_Prescripcion_vista_paciente = StringVar()
                string_label_Prescripcion_vista_paciente.set(f"Fecha Prescripcion: {index[10]}")

                global string_label_Curso_vista_paciente
                string_label_Curso_vista_paciente = StringVar()
                string_label_Curso_vista_paciente.set(f"Curso: {index[11]}")                
                
                try:
                    global imagen_foto_nueva_prescripcion
                    imagen_foto_nueva_prescripcion = CTkImage(Image.open(f"D:/Oncologico/imagenes/Pacientes/{ci_extraido_modificar_prescripcion}.jpg"), size = (300,300))
                except:
                    error = messagebox.showinfo("Error", "No hay foto")

            modificar_prescripcion_paciente = ModificarPrescripcionPaciente()

        self.listado.bind("<Double-1>", abrir_ventana_modificar_prescripcion_paciente)
        

#########################################################################################################################
######################################## modificar_prescripcion_paciente ####################################################
#########################################################################################################################

class ModificarPrescripcionPaciente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Modificar Prescripcion Paciente")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/imagen6.jpg"), size = (1000,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        # ************************** Labels  ************************* 
                
        self.label_registro = CTkLabel(self,textvariable = string_label_registro_vista_paciente, font=("Times New Roman",16))
        self.label_registro.place(x = 50, y = 50)
        
        self.label_Historia = CTkLabel(self,textvariable = string_label_historia_vista_paciente, font=("Times New Roman",16))
        self.label_Historia.place(x = 50, y = 90)
                
        self.label_CI = CTkLabel(self,textvariable = string_label_ci_vista_paciente, font=("Times New Roman",16))
        self.label_CI.place(x = 50, y = 130)
                
        self.label_Nombre = CTkLabel(self,textvariable = string_label_Nombre_vista_paciente, font=("Times New Roman",16))
        self.label_Nombre.place(x = 50, y = 170)
                
        self.label_1er = CTkLabel(self,textvariable = string_label_1er_vista_paciente, font=("Times New Roman",16))
        self.label_1er.place(x = 50, y = 210)
                
        self.label_2do = CTkLabel(self,textvariable = string_label_2do_vista_paciente, font=("Times New Roman",16))
        self.label_2do.place(x = 50, y = 250)
                
        self.label_Edad = CTkLabel(self,textvariable = string_label_Edad_vista_paciente, font=("Times New Roman",16))
        self.label_Edad.place(x = 50, y = 290)
                
        self.label_Raza = CTkLabel(self,textvariable = string_label_Raza_vista_paciente, font=("Times New Roman",16))
        self.label_Raza.place(x = 50, y = 330)
                       
        self.label_Municipio = CTkLabel(self,textvariable = string_label_Municipio_vista_paciente, font=("Times New Roman",16))
        self.label_Municipio.place(x = 50, y = 370)
        
        self.label_Sexo = CTkLabel(self,textvariable = string_label_Sexo_vista_paciente, font=("Times New Roman",16))
        self.label_Sexo.place(x = 50, y = 410)
                
        self.label_Prescripcion = CTkLabel(self,textvariable = string_label_Prescripcion_vista_paciente, font=("Times New Roman",16))
        self.label_Prescripcion.place(x = 50, y = 450)
                
        self.label_Curso = CTkLabel(self,textvariable = string_label_Curso_vista_paciente, font=("Times New Roman",16))
        self.label_Curso.place(x = 50, y = 490)

        ########################################## text #################################################

        self.label_Resumen = CTkLabel(self,text= "Resumen:", font=("Times New Roman",16))
        self.label_Resumen.place(x = 300, y = 310)

        self.text_Resumen = CTkTextbox(self,width=500,height=150)
        self.text_Resumen.place(x = 450, y = 310)

        self.label_Localizacion = CTkLabel(self,text="Localizacion:", font=("Times New Roman",16))
        self.label_Localizacion.place(x = 300, y = 50)

        self.text_Localizacion = CTkEntry(self)
        self.text_Localizacion.place(x = 450, y = 50)

        self.label_T = CTkLabel(self,text="T:", font=("Times New Roman",16))
        self.label_T.place(x = 300, y = 90)

        self.text_T = CTkEntry(self,width=30)
        self.text_T.place(x = 320, y = 90)

        self.label_N = CTkLabel(self,text="N:", font=("Times New Roman",16))
        self.label_N.place(x = 350, y = 90)

        self.text_N = CTkEntry(self,width=30)
        self.text_N.place(x = 370, y = 90)

        self.label_M = CTkLabel(self,text="M:", font=("Times New Roman",16))
        self.label_M.place(x = 400, y = 90)

        self.text_M = CTkEntry(self,width=30)
        self.text_M.place(x = 420, y = 90)

        self.label_Estadio = CTkLabel(self,text="Estadio:", font=("Times New Roman",16))
        self.label_Estadio.place(x = 300, y = 130)

        self.text_Estadio = CTkEntry(self)
        self.text_Estadio.place(x = 450, y = 130)

        self.label_Comentario = CTkLabel(self,text="Comentario:", font=("Times New Roman",16))
        self.label_Comentario.place(x = 300, y = 500)

        self.text_Comentario = CTkTextbox(self,width=500,height=150)
        self.text_Comentario.place(x = 450, y = 500) 

        try:           
            self.label_imagen_foto = CTkLabel(self, image = imagen_foto_nueva_prescripcion, text = "")
            self.label_imagen_foto.place(x = 700 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        ##### ahora queremos que se muestren los datos anteriores
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"
            )
        cursor = conn.cursor()
        sql = f""" SELECT * FROM `pacientes` WHERE `ci` = '{ci_extraido_modificar_prescripcion}' and `curso` = {curso_extraido_modificar_prescripcion}; """
        cursor.execute(sql)
        for index in cursor:
            self.text_Resumen.insert(1.0,str(index[12]))
            self.text_Localizacion.insert(0,str(index[13]))
            self.text_T.insert(0,index[14])
            self.text_N.insert(0,index[15])
            self.text_M.insert(0,index[16])
            self.text_Estadio.insert(0,index[17])
            self.text_Comentario.insert(1.0,index[18])

        def tabla_dosis_modificar_prescripcion_paciente():
            tabla_dosis_modificar = TablaDosisModificarPrescripcion()

        self.btn = CTkButton(self,text="Tabla Dosis", font=("Times New Roman",16),width=200,height=50, command=tabla_dosis_modificar_prescripcion_paciente)
        self.btn.place(x=50,y=550)

        def agregar_info_modificar_prescripcion():
            error = messagebox.askquestion("Prescribir","Se va a modificar la prescripcion del Paciente")
            if error == "yes":
                try:
                    # actualizamos los datos de la bd
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" UPDATE `pacientes` SET `resumen`='{self.text_Resumen.get("1.0","end")}', `localizacion`='{self.text_Localizacion.get()}',
                                `t`='{self.text_T.get()}',`n`='{self.text_N.get()}',`m`='{self.text_M.get()}',`estadio`='{self.text_Estadio.get()}',
                                `comentario`='{self.text_Comentario.get("1.0","end")}' WHERE `ci`='{ci_extraido_modificar_prescripcion}' and `curso` = {curso_extraido_modificar_prescripcion} """
                    cursor.execute(sql)
                    conn.commit()
                    self.destroy()
                except:
                    messagebox.showinfo("Error","No se modifico la prescripcion del paciente, revise que la informacion se halla agregado correctamente")


        self.btn2 = CTkButton(self,text="Modificar", font=("Times New Roman",16),width=200,height=50, command=agregar_info_modificar_prescripcion)
        self.btn2.place(x=50,y=610)

###########################################################################################################################
######################################### tabla dosis modificar prescripcion ##################################################
###########################################################################################################################
class TablaDosisModificarPrescripcion(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Tabla Dosis Modificar Prescripcion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/image2.jpg"), size = (1000,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        # hagamos la tabla de las dosis

        self.tabla_dosis = ttk.Treeview(self, columns = ("fecha", "volumen", "dosis_fraccion", "fraccion", "dosis", "fracciones_vencidas", "dosis_restantes"))
        self.tabla_dosis.column("#0", width = 60)
        self.tabla_dosis.column("fecha", width = 120)
        self.tabla_dosis.column("volumen", width = 200)
        self.tabla_dosis.column("dosis_fraccion", width = 200)
        self.tabla_dosis.column("fraccion", width = 100)
        self.tabla_dosis.column("dosis", width = 100)
        self.tabla_dosis.column("fracciones_vencidas", width = 200)
        self.tabla_dosis.column("dosis_restantes", width = 200)
        
        self.tabla_dosis.place(x = 25, y = 150)
        self.tabla_dosis.config(height = 15)

        self.tabla_dosis.heading("#0", text = "Id")
        self.tabla_dosis.heading("fecha", text = "Fecha")
        self.tabla_dosis.heading("volumen", text = "Volumen a Tratar")
        self.tabla_dosis.heading("dosis_fraccion", text = "Dosis x Fraccion [cGy]")
        self.tabla_dosis.heading("fraccion", text = "Fraccion")
        self.tabla_dosis.heading("dosis", text = "Dosis [cGy]") 
        self.tabla_dosis.heading("fracciones_vencidas", text = "Fracciones Vencidas")
        self.tabla_dosis.heading("dosis_restantes", text = "Dosis Restantes [cGy]")    

        # vamos a llenar la tabla con los elementos de la bd 
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"
            )
        cursor = conn.cursor()
        sql = f""" SELECT * FROM `dosis` WHERE `ci` = "{ci_extraido_modificar_prescripcion}" and `curso` = {curso_extraido_modificar_prescripcion} """
        cursor.execute(sql)
        for index in cursor:
            self.tabla_dosis.insert("", END , text =f"{index[0]}", values = (f"{index[1]}",f"{index[4]}",f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}", f"{index[9]}"))

        self.scrollbar_dosis = CTkScrollbar(self, command = self.tabla_dosis.yview, width = 18)
        self.scrollbar_dosis.place(in_ = self.tabla_dosis, relheigh = 1, relx = 1)

        self.tabla_dosis.config(yscrollcommand = self.scrollbar_dosis.set)

        # labels y entrys para modificar la dosis
        self.label1 = CTkLabel(self,text="Fecha")
        self.label1.place(x=25,y=400)

        self.entry1 = CTkEntry(self, width=80)
        self.entry1.place(x=25,y=440)

        # para agregarle la fecha
        # crear boton calendario para agregar la fecha al text        
        def btn_fecha_tabla_dosis_modificar():
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
                self.entry1.delete(0,END)                
                fecha_select = cal.get_date()
                self.entry1.insert(0,str(fecha_select))
                calendario.destroy()
            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack() 

        self.btn_fecha = CTkButton(self,text="...",command=btn_fecha_tabla_dosis_modificar, width = 27, height = 27)
        self.btn_fecha.place(x=70 ,y=400 )


        self.label2 = CTkLabel(self,text="D x Fx")
        self.label2.place(x=135,y=400)

        self.entry2 = CTkEntry(self, width=100)
        self.entry2.place(x=120,y=440)

        self.label3 = CTkLabel(self,text="Fx")
        self.label3.place(x=260,y=400)

        self.entry3 = CTkEntry(self, width=100)
        self.entry3.place(x=240,y=440)

        self.label4 = CTkLabel(self,text="Fx Vencidas")
        self.label4.place(x=370,y=400)

        self.entry4 = CTkEntry(self, width=100)
        self.entry4.place(x=360,y=440)   
          

        # vamos a recoger el id de la dosis que señalemos 
        def seleccionar_id_de_la_dosis_seleccionada(event):
            selected_item = self.tabla_dosis.focus()
            global item_id
            item_id = self.tabla_dosis.item(selected_item,'text')[0] 
            item_id = int(item_id) 
            print(type(item_id)) 
            print(item_id)                             

        self.tabla_dosis.bind("<<TreeviewSelect>>",seleccionar_id_de_la_dosis_seleccionada)

        def modificar_dosis_modificar():
            try:

                # primero asegurarnos de que hay algo escrito en todos los entrys
                if self.entry1.get() == "" or self.entry2.get() == "" or self.entry3.get() == "" or self.entry4.get() == "":
                    error = messagebox.showinfo("Error", "Escribe en todos los campos")                

                else:
                    # 3ro asegurarnos que la nueva cantidad de fracciones no es menor que las que ya se han dado
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `fx_vencidas` FROM `dosis` WHERE `id` = {item_id}; """
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] > int(self.entry3.get()):
                            error = messagebox.showinfo("Error", "Ya has ejecutado mas dosis que la cantidad que deseas escribir")
                        else:
                            error = messagebox.askyesno("Actualizar", "Se va a modificar la dosisimetria")
                            if error:
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "",
                                    database = "oncologico"
                                    )
                                cursor = conn.cursor() 
                                sql = f""" UPDATE `dosis` SET `fecha`='{self.entry1.get()}',`dosis_x_fraccion`='{float(self.entry2.get())}',`fx`='{int(self.entry3.get())}',`dosis`='{float(self.entry2.get())}',`fx_vencidas`= '{int(self.entry3.get())}', `dosis_restante`='{float(self.entry2.get())}' WHERE `id` = {item_id}; """
                                cursor.execute(sql)
                                conn.commit()
                                self.destroy()
            except:
                error = messagebox.showinfo("Error", "Asegurate de haber seleccionado en la tabla para modificar")
        


            
        self.btn_agregar = CTkButton(self,text="Modificar",command=modificar_dosis_modificar,height=60,width=200)
        self.btn_agregar.place(x=325,y=550)

###########################################################################################################################
################################# buscar para eliminar prescripcion ######################################################
###########################################################################################################################

class BuscarPacienteEliminarPrescripcion(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Buscar para Eliminar Prescripcion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/image2.jpg"), size = (800,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        self.opcion_radio = IntVar()
        
        self.radio_Historia = CTkRadioButton(self,text="Buscar por Historia Clinica:", font=("Times New Roman",16),variable = self.opcion_radio, value = 1)
        self.radio_Historia.place(x = 50, y = 50)

        self.texto_Historia = CTkEntry(self)
        self.texto_Historia.place(x = 280, y = 50)

        self.radio_CI = CTkRadioButton(self,text="Buscar por CI:", font=("Times New Roman",16),variable = self.opcion_radio, value = 2)
        self.radio_CI.place(x = 50, y = 90)

        self.texto_CI = CTkEntry(self)
        self.texto_CI.place(x = 280, y = 90)

        self.radio_Nombre = CTkRadioButton(self,text="Buscar por Nombre:", font=("Times New Roman",16),variable = self.opcion_radio, value = 3)
        self.radio_Nombre.place(x = 50, y = 130)

        self.texto_Nombre = CTkEntry(self)
        self.texto_Nombre.place(x = 280, y = 130)

        self.radio_1er = CTkRadioButton(self,text="Buscar por 1er Apellido:", font=("Times New Roman",16),variable = self.opcion_radio, value = 4)
        self.radio_1er.place(x = 50, y = 170)

        self.texto_1er = CTkEntry(self)
        self.texto_1er.place(x = 280, y = 170)

        self.radio_2do = CTkRadioButton(self,text="Buscar por 2do Apellido:", font=("Times New Roman",16),variable = self.opcion_radio, value = 5)
        self.radio_2do.place(x = 50, y = 210)

        self.texto_2do = CTkEntry(self)
        self.texto_2do.place(x = 280, y = 210)

        self.listado = Listbox(self)
        self.listado.config(selectmode = SINGLE , width = 100 , height = 20)
        self.listado.place(x = 200 , y = 350)

        self.scrollbar = CTkScrollbar(self, command = self.listado.yview, width = 18)
        self.scrollbar.place(in_ = self.listado, relheigh = 1, relx = 1)

        self.listado.config(yscrollcommand = self.scrollbar.set)

        def buscar_ver_paciente():
            try:
                self.listado.delete(0,END)
                lista = ""

                if self.opcion_radio.get() == 1: # esta es la opcion buscar por historia clinica

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `historia_clinica` = {self.texto_Historia.get()}; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4]) 
                        self.listado.insert(END , lista)


                elif self.opcion_radio.get() == 2: # esta es la opcion buscar por CI
                                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `ci` = '{self.texto_CI.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 3: # esta es la opcion buscar por Nombre
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `Nombre` = '{self.texto_Nombre.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 4: # esta es la opcion buscar por 1er apellido
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `1er_apellido` = '{self.texto_1er.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                elif self.opcion_radio.get() == 5: # esta es la opcion buscar por 2do apellido
                    
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" SELECT `ci`, `nombre`, `1er_apellido`, `2do_apellido`, `historia_clinica`, `curso` FROM `pacientes` WHERE `2do_apellido` = '{self.texto_2do.get()}'; """
                    cursor.execute(sql)
                    for index in cursor:
                        lista = ""
                        lista = "Curso: " + str(index[5]) + "    " + index[0] + "    " + index[1] + "    " + index[2] + "    " + index[3] + "    " + "No. de Historia Clinica:" + "    " + str(index[4])
                        self.listado.insert(END , lista)

                else:
                    error = messagebox.showinfo("Error", "Escoja una opcion")
            except:
                pass


        self.btn_buscar = CTkButton(self,text="Buscar",command=buscar_ver_paciente, width = 300, height = 100)
        self.btn_buscar.place(x=450, y = 90)
        
        ## abrimos la prescripcion dando 2ble click

        def abrir_ventana_eliminar_prescripcion_paciente(event):
            index = self.listado.curselection()
            selected_string = self.listado.get(index)
            global ci_extraido_eliminar_prescripcion
            ci_extraido_eliminar_prescripcion = selected_string[12:23]
            global curso_extraido_eliminar_prescripcion
            curso_extraido_eliminar_prescripcion = selected_string[7]

            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "oncologico"
                )
            cursor = conn.cursor()
            sql = f""" SELECT * FROM `pacientes` WHERE `ci` = '{ci_extraido_eliminar_prescripcion}' and `curso` = {curso_extraido_eliminar_prescripcion}; """
            cursor.execute(sql) 
            for index in cursor:

                global string_label_registro_vista_paciente
                string_label_registro_vista_paciente = StringVar()           
                string_label_registro_vista_paciente.set(f"Fecha Registro: {str(index[0])}")

                global string_label_historia_vista_paciente      
                string_label_historia_vista_paciente = StringVar()           
                string_label_historia_vista_paciente.set(f"Historia Clinica: {index[1]}")

                global string_label_ci_vista_paciente
                string_label_ci_vista_paciente = StringVar()
                string_label_ci_vista_paciente.set(f"CI: {index[2]}")

                global string_label_Nombre_vista_paciente
                string_label_Nombre_vista_paciente = StringVar()
                string_label_Nombre_vista_paciente.set(f"Nombre: {index[3]}")

                global string_label_1er_vista_paciente
                string_label_1er_vista_paciente = StringVar()
                string_label_1er_vista_paciente.set(f"1er Apellido: {index[4]}")

                global string_label_2do_vista_paciente
                string_label_2do_vista_paciente = StringVar()
                string_label_2do_vista_paciente.set(f"2do Apellido: {index[5]}")

                global string_label_Edad_vista_paciente
                string_label_Edad_vista_paciente = StringVar()
                string_label_Edad_vista_paciente.set(f"Edad: {index[6]}")

                global string_label_Raza_vista_paciente
                string_label_Raza_vista_paciente = StringVar()
                string_label_Raza_vista_paciente.set(f"Raza: {index[7]}")

                global string_label_Municipio_vista_paciente
                string_label_Municipio_vista_paciente = StringVar() 
                string_label_Municipio_vista_paciente.set(f"Municipio: {index[8]}")

                global string_label_Sexo_vista_paciente
                string_label_Sexo_vista_paciente = StringVar()
                string_label_Sexo_vista_paciente.set(f"Sexo: {index[9]}")

                global string_label_Prescripcion_vista_paciente
                string_label_Prescripcion_vista_paciente = StringVar()
                string_label_Prescripcion_vista_paciente.set(f"Fecha Prescripcion: {index[10]}")

                global string_label_Curso_vista_paciente
                string_label_Curso_vista_paciente = StringVar()
                string_label_Curso_vista_paciente.set(f"Curso: {index[11]}")                
                
                try:
                    global imagen_foto_nueva_prescripcion
                    imagen_foto_nueva_prescripcion = CTkImage(Image.open(f"D:/Oncologico/imagenes/Pacientes/{ci_extraido_eliminar_prescripcion}.jpg"), size = (300,300))
                except:
                    error = messagebox.showinfo("Error", "No hay foto")

            eliminar_prescripcion_paciente = EliminarPrescripcionPaciente()

        self.listado.bind("<Double-1>", abrir_ventana_eliminar_prescripcion_paciente)
        

#########################################################################################################################
######################################## eliminar_prescripcion_paciente ####################################################
#########################################################################################################################

class EliminarPrescripcionPaciente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Eliminar Prescripcion Paciente")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/imagen6.jpg"), size = (1000,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        # ************************** Labels  ************************* 
                
        self.label_registro = CTkLabel(self,textvariable = string_label_registro_vista_paciente, font=("Times New Roman",16))
        self.label_registro.place(x = 50, y = 50)
        
        self.label_Historia = CTkLabel(self,textvariable = string_label_historia_vista_paciente, font=("Times New Roman",16))
        self.label_Historia.place(x = 50, y = 90)
                
        self.label_CI = CTkLabel(self,textvariable = string_label_ci_vista_paciente, font=("Times New Roman",16))
        self.label_CI.place(x = 50, y = 130)
                
        self.label_Nombre = CTkLabel(self,textvariable = string_label_Nombre_vista_paciente, font=("Times New Roman",16))
        self.label_Nombre.place(x = 50, y = 170)
                
        self.label_1er = CTkLabel(self,textvariable = string_label_1er_vista_paciente, font=("Times New Roman",16))
        self.label_1er.place(x = 50, y = 210)
                
        self.label_2do = CTkLabel(self,textvariable = string_label_2do_vista_paciente, font=("Times New Roman",16))
        self.label_2do.place(x = 50, y = 250)
                
        self.label_Edad = CTkLabel(self,textvariable = string_label_Edad_vista_paciente, font=("Times New Roman",16))
        self.label_Edad.place(x = 50, y = 290)
                
        self.label_Raza = CTkLabel(self,textvariable = string_label_Raza_vista_paciente, font=("Times New Roman",16))
        self.label_Raza.place(x = 50, y = 330)
                       
        self.label_Municipio = CTkLabel(self,textvariable = string_label_Municipio_vista_paciente, font=("Times New Roman",16))
        self.label_Municipio.place(x = 50, y = 370)
        
        self.label_Sexo = CTkLabel(self,textvariable = string_label_Sexo_vista_paciente, font=("Times New Roman",16))
        self.label_Sexo.place(x = 50, y = 410)
                
        self.label_Prescripcion = CTkLabel(self,textvariable = string_label_Prescripcion_vista_paciente, font=("Times New Roman",16))
        self.label_Prescripcion.place(x = 50, y = 450)
                
        self.label_Curso = CTkLabel(self,textvariable = string_label_Curso_vista_paciente, font=("Times New Roman",16))
        self.label_Curso.place(x = 50, y = 490)

        ########################################## text #################################################

        self.label_Resumen = CTkLabel(self,text= "Resumen:", font=("Times New Roman",16))
        self.label_Resumen.place(x = 300, y = 310)

        self.text_Resumen = CTkTextbox(self,width=500,height=150)
        self.text_Resumen.place(x = 450, y = 310)

        self.label_Localizacion = CTkLabel(self,text="Localizacion:", font=("Times New Roman",16))
        self.label_Localizacion.place(x = 300, y = 50)

        self.text_Localizacion = CTkEntry(self)
        self.text_Localizacion.place(x = 450, y = 50)

        self.label_T = CTkLabel(self,text="T:", font=("Times New Roman",16))
        self.label_T.place(x = 300, y = 90)

        self.text_T = CTkEntry(self,width=30)
        self.text_T.place(x = 320, y = 90)

        self.label_N = CTkLabel(self,text="N:", font=("Times New Roman",16))
        self.label_N.place(x = 350, y = 90)

        self.text_N = CTkEntry(self,width=30)
        self.text_N.place(x = 370, y = 90)

        self.label_M = CTkLabel(self,text="M:", font=("Times New Roman",16))
        self.label_M.place(x = 400, y = 90)

        self.text_M = CTkEntry(self,width=30)
        self.text_M.place(x = 420, y = 90)

        self.label_Estadio = CTkLabel(self,text="Estadio:", font=("Times New Roman",16))
        self.label_Estadio.place(x = 300, y = 130)

        self.text_Estadio = CTkEntry(self)
        self.text_Estadio.place(x = 450, y = 130)

        self.label_Comentario = CTkLabel(self,text="Comentario:", font=("Times New Roman",16))
        self.label_Comentario.place(x = 300, y = 500)

        self.text_Comentario = CTkTextbox(self,width=500,height=150)
        self.text_Comentario.place(x = 450, y = 500) 

        try:           
            self.label_imagen_foto = CTkLabel(self, image = imagen_foto_nueva_prescripcion, text = "")
            self.label_imagen_foto.place(x = 700 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        ##### ahora queremos que se muestren los datos anteriores
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"
            )
        cursor = conn.cursor()
        sql = f""" SELECT * FROM `pacientes` WHERE `ci` = '{ci_extraido_eliminar_prescripcion}' and `curso` = {curso_extraido_eliminar_prescripcion}; """
        cursor.execute(sql)
        for index in cursor:
            self.text_Resumen.insert(1.0,str(index[12]))
            self.text_Localizacion.insert(0,str(index[13]))
            self.text_T.insert(0,index[14])
            self.text_N.insert(0,index[15])
            self.text_M.insert(0,index[16])
            self.text_Estadio.insert(0,index[17])
            self.text_Comentario.insert(1.0,index[18])

        def tabla_dosis_eliminar_prescripcion_paciente():            
            tabla_dosis_eliminar = TablaDosisEliminarPrescripcion()

        self.btn = CTkButton(self,text="Tabla Dosis", font=("Times New Roman",16),width=200,height=50, command=tabla_dosis_eliminar_prescripcion_paciente)
        self.btn.place(x=50,y=550)

        def agregar_info_eliminar_prescripcion():
            error = messagebox.askquestion("Prescribir","Se va a eliminar la prescripcion del Paciente")
            if error == "yes":
                try:
                    # actualizamos los datos de la bd
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "",
                        database = "oncologico"
                        )
                    cursor = conn.cursor()
                    sql = f""" UPDATE `pacientes` SET `resumen`='-', `localizacion`='-',
                                `t`='-',`n`='-',`m`='-',`estadio`='-',
                                `comentario`='-' WHERE `ci`='{ci_extraido_eliminar_prescripcion}' and `curso` = {curso_extraido_eliminar_prescripcion}"""
                    cursor.execute(sql)
                    conn.commit()
                    self.destroy()
                except:
                    messagebox.showinfo("Error","No se elimino la prescripcion del paciente")


        self.btn2 = CTkButton(self,text="Eliminar", font=("Times New Roman",16),width=200,height=50, command=agregar_info_eliminar_prescripcion)
        self.btn2.place(x=50,y=610)

###########################################################################################################################
######################################### tabla dosis eliminar prescripcion ##################################################
###########################################################################################################################
class TablaDosisEliminarPrescripcion(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Tabla Dosis Eliminar Prescripcion")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x700") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))   
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 

        # ****************** Imagen *********************
                            
        try:                        
            self.imagen = CTkImage(Image.open("D:/Oncologico/imagenes/image2.jpg"), size = (1000,700))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        # hagamos la tabla de las dosis

        self.tabla_dosis = ttk.Treeview(self, columns = ("fecha", "volumen", "dosis_fraccion", "fraccion", "dosis", "fracciones_vencidas", "dosis_restantes"))
        self.tabla_dosis.column("#0", width = 60)
        self.tabla_dosis.column("fecha", width = 120)
        self.tabla_dosis.column("volumen", width = 200)
        self.tabla_dosis.column("dosis_fraccion", width = 200)
        self.tabla_dosis.column("fraccion", width = 100)
        self.tabla_dosis.column("dosis", width = 100)
        self.tabla_dosis.column("fracciones_vencidas", width = 200)
        self.tabla_dosis.column("dosis_restantes", width = 200)
        
        self.tabla_dosis.place(x = 25, y = 150)
        self.tabla_dosis.config(height = 15)

        self.tabla_dosis.heading("#0", text = "Id")
        self.tabla_dosis.heading("fecha", text = "Fecha")
        self.tabla_dosis.heading("volumen", text = "Volumen a Tratar")
        self.tabla_dosis.heading("dosis_fraccion", text = "Dosis x Fraccion [cGy]")
        self.tabla_dosis.heading("fraccion", text = "Fraccion")
        self.tabla_dosis.heading("dosis", text = "Dosis [cGy]") 
        self.tabla_dosis.heading("fracciones_vencidas", text = "Fracciones Vencidas")
        self.tabla_dosis.heading("dosis_restantes", text = "Dosis Restantes [cGy]")   

        # vamos a llenar la tabla con los elementos de la bd 
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "oncologico"
            )
        cursor = conn.cursor()
        sql = f""" SELECT * FROM `dosis` WHERE `ci` = "{ci_extraido_eliminar_prescripcion}" and `curso` = {curso_extraido_eliminar_prescripcion} """
        cursor.execute(sql)
        for index in cursor:
            self.tabla_dosis.insert("", END , text =f"{index[0]}", values = (f"{index[1]}",f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}", f"{index[9]}"))

        self.scrollbar_dosis = CTkScrollbar(self, command = self.tabla_dosis.yview, width = 18)
        self.scrollbar_dosis.place(in_ = self.tabla_dosis, relheigh = 1, relx = 1)

        self.tabla_dosis.config(yscrollcommand = self.scrollbar_dosis.set)
        
        # vamos a recoger el id de la dosis que señalemos 
        def seleccionar_id_de_la_fila_seleccionada(event):
            selected_item = self.tabla_dosis.focus()
            global item_id
            item_id = self.tabla_dosis.item(selected_item,'text')[0]                               

        self.tabla_dosis.bind("<<TreeviewSelect>>",seleccionar_id_de_la_fila_seleccionada)


        def eliminar_dosis_eliminar():
            try:
                #primero verificar que la dosis no esta comenzada, si no no se puede eliminar
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "oncologico"
                    )
                cursor = conn.cursor()
                sql = f""" SELECT * FROM `dosis` WHERE `id` = {item_id}"""
                cursor.execute(sql)
                for index in cursor:
                    if index[8] != 0:
                        global dosis_comenzada
                        dosis_comenzada = True
                        error = messagebox.showerror("Error","No se puede eliminar la dosis porque ya comenzo a ejecutarla \n pruebe modificarla mejor")

                    else:
                        error = messagebox.askokcancel("Alerta","Se va a eliminar la dosis")
                        if error == True:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password = "",
                                database = "oncologico"
                                )
                            cursor = conn.cursor()
                            sql = f""" DELETE FROM `dosis` WHERE `id` = {item_id}"""
                            cursor.execute(sql)
                            conn.commit()
                            self.destroy()
            except:
                pass

        def eliminar_dosis_eliminar2(event):
            try:
                #primero verificar que la dosis no esta comenzada, si no no se puede eliminar
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "oncologico"
                    )
                cursor = conn.cursor()
                sql = f""" SELECT * FROM `dosis` WHERE `id` = {item_id}"""
                cursor.execute(sql)
                for index in cursor:
                    if index[8] != 0:
                        global dosis_comenzada
                        dosis_comenzada = True
                        error = messagebox.showerror("Error","No se puede eliminar la dosis porque ya comenzo a ejecutarla \n pruebe modificarla mejor")

                    else:
                        error = messagebox.askokcancel("Alerta","Se va a eliminar la dosis")
                        if error == True:
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password = "",
                                database = "oncologico"
                                )
                            cursor = conn.cursor()
                            sql = f""" DELETE FROM `dosis` WHERE `id` = {item_id}"""
                            cursor.execute(sql)
                            conn.commit()
                            self.destroy()
            except:
                pass

        self.tabla_dosis.bind("<Double-1>",eliminar_dosis_eliminar2)
            
        self.btn_eliminar = CTkButton(self,text="Eliminar",command=eliminar_dosis_eliminar,height=60,width=200)
        self.btn_eliminar.place(x=325,y=550)




        
        









































conn.close()

autenticacion = Autenticacion()
autenticacion.mainloop()