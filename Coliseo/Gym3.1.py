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



# ***************************************************************************************
# **************** Creando Usuario, Base de Datos y Tablas de Admin necesarias **********
# ***************************************************************************************



ususario_ysos_is_created = False
base_data_is_created = False
table_usuarios_is_created = False
usuario_ysos_is_created = False
table_licencias_is_created = False

# ********************** creando usuario admin ******************************

try:
    sql = """CREATE USER 'ysos'@'localhost' IDENTIFIED BY '123456';"""
    cursor.execute(sql)
    conn.commit()
except:
    ususario_ysos_is_created = True

sql = """GRANT ALL PRIVILEGES ON *.* TO 'ysos'@'localhost' REQUIRE NONE WITH GRANT OPTION MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0; """
cursor.execute(sql)
conn.commit()

conn.close()

conn = mysql.connector.connect(
    host = "localhost",
    user = "ysos",
    password = "123456",
    )
cursor = conn.cursor()

# ******* creando la base de datos ysos ***********
try:
    sql = """CREATE DATABASE ysos CHARACTER SET = utf8mb4 COLLATE utf8mb4_spanish_ci;"""
    cursor.execute(sql)
    conn.commit()
    base_data_is_created = True
except:
    base_data_is_created = True

conn = mysql.connector.connect(
    host = "localhost",
    user = "ysos",
    password = "123456",
    database = "ysos"
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
    user = "ysos",
    password = "123456",
    database = "ysos"
    )
cursor = conn.cursor()

usuario_inicial = []
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
        
        usuario_ysos_is_created = True
    except:
        usuario_ysos_is_created = True


# ************** creando tabla licencias ***************

conn = mysql.connector.connect(
    host = "localhost",
    user = "ysos",
    password = "123456",
    database = "ysos"
    )
cursor = conn.cursor()

try:
    sql = """CREATE TABLE `ysos`.`licencias` (`codigo_lic` VARCHAR(50) NOT NULL , `pass_economia` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    table_licencias_is_created = True
    
    
fecha_actual = datetime.now().date()


# ******************** Creando Tabla Clientes *******************


try:
    sql = """CREATE TABLE `ysos`.`clientes` (`ID` INT NOT NULL , `Nombre` VARCHAR(50) NOT NULL , `Apellido 1` VARCHAR(50) NOT NULL , `Apellido 2` VARCHAR(50) NOT NULL , `Modalidad` VARCHAR(50) NOT NULL , `Entrenador` VARCHAR(50) NOT NULL , `Telefono` VARCHAR(50) NOT NULL , `Ultima_Asistencia` DATE NOT NULL , `Fecha_Pago` DATE NOT NULL ) ENGINE = InnoDB; """
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# ********************** creando tabla pagos ***************************************
try:
    sql = """CREATE TABLE `ysos`.`pagos` (`fecha` DATE NOT NULL , `id` INT NOT NULL , `nombre_completo` VARCHAR(50) NOT NULL , `modalidad` VARCHAR(50) NOT NULL , `Entrenador` VARCHAR(50) NOT NULL, `pagar_activacion` VARCHAR(50) NOT NULL , `importe` INT NOT NULL, `pago_entrenador` INT NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# ********************** creando tabla modalidad ***********************************
try:
    sql = """CREATE TABLE `ysos`.`modalidad` (`modalidad` VARCHAR(50) NOT NULL , `precio` INT NOT NULL , `pago_entrenador` INT NOT NULL) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# *************************** creando tabla entrenadores ****************************
try:
    sql = """CREATE TABLE `ysos`.`entrenadores` (`nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# *************************** creando tabla agrego **********************************
try:
    sql = """CREATE TABLE `ysos`.`agrego` (`agrego` VARCHAR(50) NOT NULL , `precio` INT(11) NOT NULL , `pago entrenador` INT(11) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    temp = True

# ************************** creando tabla cliente_agrego ****************************
try:
    sql = """CREATE TABLE `ysos`.`cliente_agrego` (`id` INT(11) NOT NULL , `agrego` VARCHAR(50) NOT NULL , `entrenador` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;  """
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
            user = "ysos",
            password = "123456",
            database = "ysos"
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
                        user = "ysos",
                        password = "123456",
                        database = "ysos"
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
        self.title("Coliseo")
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
        self.label_ysos = CTkLabel(self, text = firma, font=("Times New Roman",16))
        self.label_ysos.place(x = 1150, y = 650)

        self.menu = Menu(self)
        self.config(menu=self.menu, width="200", height="100")
                
        def balance_lobby():
            seguridad_balance = SeguridadBalance()                                  

        def entrenadores_lobby():
            entrenadores = Entrenadores()

        def modalidad_lobby():
            seguridad_modalidad = SeguridadModalidad()

        def clientes_atrasados_lobby():
            clientes_atrasados = ClientesAtrasados()

        
        items_modalidad = []

        def incertar_cliente():           
            agregar_cliente = AgregarCliente()
                                    
        def modificar_cliente_lobby():
            modificar_cliente = ModificarCliente()

        def eliminar_cliente_lobby():
            eliminar_cliente = EliminarCliente()

        def asistencia_pago_cliente_lobby():
            asistemcia_pago = AsistenciaYPago()

        def agregar_usuario():
            usuario_agregar = UsuarioAgregar()
            
        def eliminar_usuario():                        
            eliminar_usuario = EliminarUsuario()          

        def cerrar_cesion():
            self.destroy()
            autenticacion.deiconify()            
            
        def cerrar_programa(): 
                self.quit()         

        def agregar_nueva_licencia():                         
            nueva_licencia = NuevaLicencia()

        def pago_entrenadores_lobby():            
            pago_entrenadores = PagoEntrenadores()

        def agregos_lobby():
            agrego = Agrego()

        def contratar_agrego_lobby():
            contratar_agrego = ContratarAgrego()

        def modificar_agrego_lobby():
            modificar_agrego = ModificarAgrego()

        def despedir_agrego_lobby():
            despedir_agrego = DespedirAgrego()
                                        
            

        economia_menu = Menu(self.menu, tearoff = 0)   
        economia_menu.add_command(label="Balance ", command = balance_lobby)
        economia_menu.add_command(label="Modalidad ", command = modalidad_lobby)
        economia_menu.add_command(label="Agregos", command = agregos_lobby)
        economia_menu.add_command(label="Pago Entrenadores ", command = pago_entrenadores_lobby)
        economia_menu.add_command(label="Pagos Atrasados", command = clientes_atrasados_lobby)
        
        entrenadores_menu = Menu(self.menu, tearoff = 0)
        entrenadores_menu.add_command(label="Listado ", command = entrenadores_lobby)

        clientes_menu = Menu(self.menu, tearoff = 0)
        clientes_menu.add_command(label="Agregar", command = incertar_cliente)
        clientes_menu.add_command(label="Modificar", command = modificar_cliente_lobby)
        clientes_menu.add_command(label="Eliminar", command = eliminar_cliente_lobby)        
        clientes_menu.add_command(label="Asistencia y Pago", command = asistencia_pago_cliente_lobby)

        agregos_menu = Menu(self.menu, tearoff = 0)
        agregos_menu.add_command(label="Contratar", command = contratar_agrego_lobby)
        agregos_menu.add_command(label="Modificar", command = modificar_agrego_lobby)
        agregos_menu.add_command(label="Despedir", command = despedir_agrego_lobby)        
        

        usuario_menu = Menu(self.menu, tearoff = 0)
        usuario_menu.add_command(label="Agregar", command = agregar_usuario)
        usuario_menu.add_command(label="Eliminar", command = eliminar_usuario)

        licencia_menu = Menu(self.menu, tearoff = 0)
        licencia_menu.add_command(label="Nueva", command = agregar_nueva_licencia)

        salir_menu = Menu(self.menu, tearoff = 0)
        salir_menu.add_command(label="Cerrar Cesion", command = cerrar_cesion)
        salir_menu.add_command(label="Cerrar Programa", command = cerrar_programa)

        self.menu.add_cascade (label="Economia", menu = economia_menu)
        self.menu.add_cascade (label="Entrenadores", menu = entrenadores_menu)
        self.menu.add_cascade (label="Clientes", menu = clientes_menu)
        self.menu.add_cascade (label="Agregos", menu = agregos_menu)
        self.menu.add_cascade(label="Usuarios", menu = usuario_menu)
        self.menu.add_cascade(label = "Licencia", menu = licencia_menu)
        self.menu.add_cascade(label="Salir", menu = salir_menu)


# **********************************************************************************
# ************************** seguridad_balance ************************************
# **********************************************************************************

class SeguridadBalance(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Seguridad Economia")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 400
        hventana = 200
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("400x200") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/logo3.jpg"), size = (400,200))  
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_seguridad = CTkLabel(self,text="Insertar contraseña:", font=("Times New Roman",16))
        self.label_seguridad.place(x = 10, y = 10)        

        self.texto_contraseña = CTkEntry(self, width = 200)
        self.texto_contraseña.place(x = 100, y = 80)
        

        def aceptar_seguridad_balance():
            
            conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
            cursor = conn.cursor()

            sql = """SELECT `pass_economia` FROM `licencias`;"""
            cursor.execute(sql)
            
            for index in cursor:
                
                if self.texto_contraseña.get() == index[0]:                     
                    self.destroy()
                    balance = Balance()
                    
                    

                else:
                    error = messagebox.showinfo("Error", "Contraseña incorrecta")


        def cambiar_seguridad_balance():
            cambiar_contraseña_economia = CambiarContraseña()

        def cancelar_seguridad_balance():
            self.destroy()

        self.btn_aceptar = CTkButton(self, command = aceptar_seguridad_balance,text = "Aceptar", width = 100, height = 2)
        self.btn_aceptar.place(x = 20, y = 160)
        
        self.btn_cambiar = CTkButton(self, command = cambiar_seguridad_balance, text = "Cambiar", width = 100, height = 2)
        self.btn_cambiar.place(x = 140, y = 160)
        
        self.btn_cancelar = CTkButton(self, command = cancelar_seguridad_balance, text = "Cancelar", width = 100, height = 2)
        self.btn_cancelar.place(x = 260, y = 160)


# **********************************************************************************
# ****************** confirmar_cambiar_contraseña **********************************
# **********************************************************************************

class CambiarContraseña(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Cambiar Contraseña")    
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
        
        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/logo3.jpg"), size = (400,300))                       
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_contraseña_actual = CTkLabel(self,text="Contraseña Actual:", font=("Times New Roman",16), fg_color = "black")
        self.label_contraseña_actual.place(x = 50, y = 50)

        self.texto_contraseña_actual = CTkEntry(self, width = 100)
        self.texto_contraseña_actual.place(x = 250, y = 50)
        
        
        self.label_new_contraseña = CTkLabel(self,text="Contraseña Nueva:", font=("Times New Roman",16), fg_color = "black")
        self.label_new_contraseña.place(x = 50, y = 90)

        self.texto_new_contraseña = CTkEntry(self, width = 100)
        self.texto_new_contraseña.place(x = 250, y = 90)
        
        
        self.label_confirmar_contraseña = CTkLabel(self,text="Confirmar:", font=("Times New Roman",16), fg_color = "black")
        self.label_confirmar_contraseña.place(x = 50, y = 130) 

        self.texto_confirmar_contraseña = CTkEntry(self, width = 100)
        self.texto_confirmar_contraseña.place(x = 250, y = 130)
        

        def ejecutar_cambiar_contraseña_economia():
            conn = mysql.connector.connect(
                host = "localhost",
                user = "ysos",
                password = "123456",
                database = "ysos"
                )
            cursor = conn.cursor()
            sql = """SELECT `pass_economia` FROM `licencias`;"""
            cursor.execute(sql)
            for index in cursor:
                if self.texto_contraseña_actual.get() == index[0]:

                    if self.texto_new_contraseña.get() == self.texto_confirmar_contraseña.get():
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "ysos",
                        password = "123456",
                        database = "ysos"
                        )
                        cursor = conn.cursor()

                        sql = f"""UPDATE `licencias` SET `pass_economia`='{self.texto_confirmar_contraseña.get()}' """
                        cursor.execute(sql)
                        conn.commit()

                        self.destroy()
                        

                    else:
                        error = messagebox.showinfo("Error", "No es igual la contraseña y su confirmacion")
                else:
                    error = messagebox.showinfo("Error", "Escriba correctamente la contraseña actual")

            
                

        def cancelar_cambiar_contraseña_economia():
            self.destroy()

        btn_cambiar_confirmar_contraseña_economia = CTkButton(self, command = ejecutar_cambiar_contraseña_economia, text = "Cambiar", width = 100, height = 2)
        btn_cambiar_confirmar_contraseña_economia.place(x = 80, y = 250)
        
        btn_cancelar_confirmar_contraseña_economia = CTkButton(self, command = cancelar_cambiar_contraseña_economia, text = "Cancelar", width = 100, height = 2)
        btn_cancelar_confirmar_contraseña_economia.place(x = 220, y = 250)
        
# **********************************************************************************
# ************************ balance *************************************************
# **********************************************************************************

class Balance(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Balance ")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1300x700") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))  

        
        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (1300,700))                        
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)


        self.label_fecha_completa = CTkLabel(self, text = "Fecha (Año-Mes-Dia):", font=("Times New Roman",16))
        self.label_fecha_completa.place(x = 50, y = 10)  

        self.texto_fecha_completa = CTkEntry(self)
        self.texto_fecha_completa.place(x = 220, y = 10)


        self.label_fecha_mes = CTkLabel(self, text = "Fecha Mes(#):", font=("Times New Roman",16))
        self.label_fecha_mes.place(x = 700, y = 10)

        self.texto_fecha_mes = CTkEntry(self)
        self.texto_fecha_mes.place(x = 800, y = 10)

        
        self.label_fecha_año = CTkLabel(self, text = "Fecha Año(#):", font=("Times New Roman",16))
        self.label_fecha_año.place(x = 980, y = 10)  

        self.texto_fecha_anio = CTkEntry(self)
        self.texto_fecha_anio.place(x = 1090, y = 10)         

        opcion_radio_btn_balance = IntVar()

        self. radio_btn_diario = CTkRadioButton(self, variable = opcion_radio_btn_balance, value = 1, text="Por dia")
        self. radio_btn_diario.place(x = 100, y = 50)

        self.radio_btn_mensual = CTkRadioButton(self, variable = opcion_radio_btn_balance, value = 2, text="Por mes")
        self.radio_btn_mensual.place(x = 1000, y = 50)

        # ********************* para escoger la fecha ********************
        def seleccionar_fecha_balance():
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
                self.texto_fecha_completa.delete(0,END)
                self.texto_fecha_anio.delete(0,END)
                self.texto_fecha_mes.delete(0,END)
                
                fecha_select = cal.get_date()
                anio = fecha_select[0:4]
                mes = fecha_select[5:7]

                self.texto_fecha_completa.insert(0,str(fecha_select)) 
                self.texto_fecha_anio.insert(0,anio)
                self.texto_fecha_mes.insert(0,mes)  

                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()

        self.btn_seleccionar_fecha = CTkButton(self, text="Fecha",command=seleccionar_fecha_balance, width = 40, height = 27)
        self.btn_seleccionar_fecha.place(x = 500, y = 10)

        # ***************************************************************************************************


        self.label_importe_independiente = CTkLabel(self, text = "Importe Independientes:", font=("Times New Roman",16))
        self.label_importe_independiente.place(x = 1060, y = 100)        

        string_resultado_importe_independiente_balance = StringVar()
        string_resultado_importe_independiente_balance.set("")

        self.label_resultado_importe_independiente = CTkLabel(self, textvariable = string_resultado_importe_independiente_balance, font=("Times New Roman",16))
        self.label_resultado_importe_independiente.place(x = 1060, y = 140)
        

        self.label_importe_dirigido = CTkLabel(self, text = "Importe Dirigido:", font=("Times New Roman",16))
        self.label_importe_dirigido.place(x = 1060, y = 180)        

        string_resultado_importe_dirigido_balance = StringVar()
        string_resultado_importe_dirigido_balance.set("")

        self.label_resultado_importe_dirigido = CTkLabel(self, textvariable = string_resultado_importe_dirigido_balance, font=("Times New Roman",16))
        self.label_resultado_importe_dirigido.place(x = 1060, y = 220)
        

        self.label_importe_personalizado = CTkLabel(self, text = "Importe Personalizado:", font=("Times New Roman",16))
        self.label_importe_personalizado.place(x = 1060, y = 260)        

        string_resultado_importe_personalizado_balance = StringVar()
        string_resultado_importe_personalizado_balance.set("")

        self.label_resultado_importe_personalizado = CTkLabel(self, textvariable = string_resultado_importe_personalizado_balance, font=("Times New Roman",16))
        self.label_resultado_importe_personalizado.place(x = 1060, y = 300)


        self.label_importe_agrego = CTkLabel(self, text = "Importe Agrego:", font=("Times New Roman",16))
        self.label_importe_agrego.place(x = 1060, y = 340)        

        string_resultado_importe_agrego_balance = StringVar()
        string_resultado_importe_agrego_balance.set("")

        self.label_resultado_importe_agrego = CTkLabel(self, textvariable = string_resultado_importe_agrego_balance, font=("Times New Roman",16))
        self.label_resultado_importe_agrego.place(x = 1060, y = 380)
       

        self.label_importe_activaciones = CTkLabel(self, text = "Importe Activaciones:", font=("Times New Roman",16))
        self.label_importe_activaciones.place(x = 1060, y = 420)        

        string_resultado_importe_activaciones_balance = StringVar()
        string_resultado_importe_activaciones_balance.set("")

        self.label_resultado_importe_activaciones = CTkLabel(self, textvariable = string_resultado_importe_activaciones_balance, font=("Times New Roman",16))
        self.label_resultado_importe_activaciones.place(x = 1060, y = 460)


        self.label__importe_extra = CTkLabel(self, text = "Extra:", font=("Times New Roman",16))
        self.label__importe_extra.place(x = 1060, y = 520)        

        string_resultado_importe_extra_balance = StringVar()
        string_resultado_importe_extra_balance.set("")

        self.label_resultado_importe_extra = CTkLabel(self, textvariable = string_resultado_importe_extra_balance, font=("Times New Roman",16))
        self.label_resultado_importe_extra.place(x = 1060, y = 570)


        self.label__importe_total = CTkLabel(self, text = "Total Importe:", font=("Times New Roman",16))
        self.label__importe_total.place(x = 1060, y = 620)        

        string_resultado_importe_total_balance = StringVar()
        string_resultado_importe_total_balance.set("")

        self.label_resultado_importe_total = CTkLabel(self, textvariable = string_resultado_importe_total_balance, font=("Times New Roman",16))
        self.label_resultado_importe_total.place(x = 1060, y = 670)      

        
        tabla_balance = ttk.Treeview(self, columns = ("Fecha","Id","nombre_completo","Modalidad", "Entrenador", "Activacion", "Importe"))
        tabla_balance.column("#0", width = 40)
        tabla_balance.column("Fecha", width = 120)
        tabla_balance.column("Id", width = 80)
        tabla_balance.column("nombre_completo", width = 200)
        tabla_balance.column("Modalidad", width = 120)
        tabla_balance.column("Entrenador", width = 120)
        tabla_balance.column("Activacion", width = 100)
        tabla_balance.column("Importe", width = 100)
        tabla_balance.place(x = 50, y = 150)
        tabla_balance.config(height = 15)
        tabla_balance.heading("#0", text = "No.")
        tabla_balance.heading("Fecha", text = "Fecha")
        tabla_balance.heading("Id", text = "Id")
        tabla_balance.heading("nombre_completo", text = "Nombre Completo")
        tabla_balance.heading("Modalidad", text = "Modalidad")
        tabla_balance.heading("Entrenador", text = "Entrenador")
        tabla_balance.heading("Activacion", text = "Pagar Activacion")
        tabla_balance.heading("Importe", text = "Importe")

        scrollbar_balance = CTkScrollbar(self, command = tabla_balance.yview, width = 18)
        scrollbar_balance.place(in_ = tabla_balance, relheigh = 1, relx = 1)

        tabla_balance.config(yscrollcommand = scrollbar_balance.set)

        

        def generar_balance():
            try:
                tabla_balance.delete(*tabla_balance.get_children())
                int_resultado_importe_independiente_balance = 0
                int_resultado_importe_dirigido_balance = 0
                int_resultado_importe_personalizado_balance = 0
                int_resultado_importe_agrego_balance = 0
                int_resultado_importe_activaciones_balance = 0
                int_resultado_importe_extra_balance = 0
                int_resultado_importe_total_balance = 0

                if opcion_radio_btn_balance.get() == 1:       

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "ysos",
                        password = "123456",
                        database = "ysos"
                        )
                    cursor = conn.cursor()


                    sql = f"""SELECT * FROM `pagos` WHERE fecha = '{date(int(self.texto_fecha_completa.get()[0:4]),int(self.texto_fecha_completa.get()[5:7]),int(self.texto_fecha_completa.get()[8:10]))}';"""
                    cursor.execute(sql)

                    contador = 0
                    for index in cursor:
                        contador += 1
                        tabla_balance.insert("", END , text = contador, values = (f"{index[0]}",f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}"))
                        if index[3] == "Personalizado":
                            int_resultado_importe_personalizado_balance += index[6]

                        elif index[3] == "Independiente":
                            int_resultado_importe_independiente_balance += index[6]

                        elif index[3] == "Dirigido":
                            int_resultado_importe_dirigido_balance += index[6]
                        
                        elif index[3] == "Agrego":
                            int_resultado_importe_agrego_balance += index[6]

                        else:
                            int_resultado_importe_extra_balance += index[6]

                        if index[5] == "SI":
                            int_resultado_importe_activaciones_balance += 200
                        
                        
                    
                    int_resultado_importe_total_balance = int_resultado_importe_personalizado_balance + int_resultado_importe_independiente_balance + int_resultado_importe_dirigido_balance + int_resultado_importe_activaciones_balance + int_resultado_importe_agrego_balance + int_resultado_importe_extra_balance

                    string_resultado_importe_independiente_balance.set(str(int_resultado_importe_independiente_balance))
                    string_resultado_importe_dirigido_balance.set(str(int_resultado_importe_dirigido_balance))
                    string_resultado_importe_personalizado_balance.set(str(int_resultado_importe_personalizado_balance))
                    string_resultado_importe_agrego_balance.set(str(int_resultado_importe_agrego_balance))
                    string_resultado_importe_activaciones_balance.set(str(int_resultado_importe_activaciones_balance))
                    string_resultado_importe_extra_balance.set(str(int_resultado_importe_extra_balance))
                    string_resultado_importe_total_balance.set(str(int_resultado_importe_total_balance))


                elif opcion_radio_btn_balance.get() == 2:

                    anio = int(self.texto_fecha_anio.get())
                    mes = int(self.texto_fecha_mes.get())
                    fecha_inicio = date(anio,mes,1)
                    fecha_final = date(anio,mes,1)

                    ############## ahora hay que hallar la fecha final ##################
                    if mes == 12:
                        fecha_final = date(anio + 1, 1, 1)
                    else:
                        fecha_final = date(anio,mes + 1,1)
                        
                    contador = 0
                    while fecha_inicio < fecha_final:            
                        
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "ysos",
                            password = "123456",
                            database = "ysos"
                            )
                        cursor = conn.cursor()

                        sql = f"""SELECT * FROM `pagos` WHERE fecha = '{fecha_inicio}';"""
                        cursor.execute(sql)
                        
                        for index in cursor:
                            contador += 1
                            tabla_balance.insert("", END , text = contador, values = (str(fecha_inicio), f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}"))
                            if index[3] == "Personalizado":
                                int_resultado_importe_personalizado_balance += index[6]

                            elif index[3] == "Independiente":
                                int_resultado_importe_independiente_balance += index[6]

                            elif index[3] == "Dirigido":
                                int_resultado_importe_dirigido_balance += index[6]

                            elif index[3] == "Agrego":
                                int_resultado_importe_agrego_balance += index[6]

                            else:
                                int_resultado_importe_extra_balance += index[6]

                            if index[5] == "SI":
                                int_resultado_importe_activaciones_balance += index[6]   
                            
                                


                        fecha_inicio = fecha_inicio + timedelta(days = 1)

                    int_resultado_importe_total_balance = int_resultado_importe_personalizado_balance + int_resultado_importe_independiente_balance + int_resultado_importe_dirigido_balance + int_resultado_importe_activaciones_balance + int_resultado_importe_agrego_balance + int_resultado_importe_extra_balance

                    string_resultado_importe_independiente_balance.set(str(int_resultado_importe_independiente_balance))
                    string_resultado_importe_dirigido_balance.set(str(int_resultado_importe_dirigido_balance))
                    string_resultado_importe_personalizado_balance.set(str(int_resultado_importe_personalizado_balance))
                    string_resultado_importe_agrego_balance.set(str(int_resultado_importe_agrego_balance))
                    string_resultado_importe_activaciones_balance.set(str(int_resultado_importe_activaciones_balance))
                    string_resultado_importe_extra_balance.set(str(int_resultado_importe_extra_balance))
                    string_resultado_importe_total_balance.set(str(int_resultado_importe_total_balance))

                else:
                    error = messagebox.showinfo("Error", "Escoge un tipo de balance")
            except:
                error = messagebox.showinfo("Error","Escribe bien los datos para poder generar el balance")


        def exportar_excel():
            try:
                rows = []
                for item in tabla_balance.get_children():
                    rows.append(tabla_balance.item(item)['values'])
                
                df = pd.DataFrame(rows, columns=["Fecha", "ID", "Nombre Completo", "Modalidad", "Pagar Activacion", "Importe"])
                
                if opcion_radio_btn_balance.get() == 1:
                    df.to_excel(f"D:/gym_Coliseo/ Balance Diario {fecha_actual}.xlsx", index=False)
                    error = messagebox.showinfo("Exportar", "Exportado a Excel")
                else:
                    df.to_excel(f"D:/gym_Coliseo/Balance Mensual {self.texto_fecha_anio.get()} - {self.texto_fecha_mes.get()}.xlsx", index=False)
                    error = messagebox.showinfo("Exportar", "Exportado a Excel")

            except:
                error = messagebox.showinfo("Error","Algun dato introducido no esta bien y no se puede exportar")

            

        def cerrar_balance():     
            self.destroy()

        self.btn_generar = CTkButton(self, command = generar_balance, text = "Generar Balance", width = 350, height = 50)
        self.btn_generar.place(x = 400, y = 500)
        
        self.btn_cerrar = CTkButton(self, command = cerrar_balance, text = "Cerrar", width = 200, height = 40)
        self.btn_cerrar.place(x = 800, y = 600)
        
        self.btn_exportar_excel = CTkButton(self, command = exportar_excel, text = "Exportar a Excel", width = 30, height = 40)
        self.btn_exportar_excel.place(x = 150, y = 600)


# **********************************************************************************
# **************************** pago entrenadores ***********************************
# **********************************************************************************

class PagoEntrenadores(CTkToplevel):
    def __init__(self):        
        self = CTkToplevel() 
        self.title("Pago Entrenadores")       
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1300
        hventana = 700
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1300x700") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

    
        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (1300,700))                          
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        items_entrenador_pago_entrenador = []
        conn = mysql.connector.connect(
        host = "localhost",
        user = "ysos",
        password = "123456",
        database = "ysos"
        )
        cursor = conn.cursor()
        sql = """SELECT `nombre` FROM `entrenadores` """
        cursor.execute(sql)

        for index in cursor:
            items_entrenador_pago_entrenador.append(index[0])

        self.texto_entrenador = ttk.Combobox(self)
        self.texto_entrenador.place(x = 450, y = 15)
        self.texto_entrenador['values'] = items_entrenador_pago_entrenador

        self.label_entrenador = CTkLabel(self, text = "Entrenador:", font=("Times New Roman",16))
        self.label_entrenador.place(x = 370, y = 10)
        

        self.label_fecha_completa = CTkLabel(self, text = "Fecha (Año-Mes-Dia):", font=("Times New Roman",16))
        self.label_fecha_completa.place(x = 10, y = 10)  

        self.texto_fecha_completa = CTkEntry(self)
        self.texto_fecha_completa.place(x = 160, y = 10)
        

        self.label_fecha_mes = CTkLabel(self, text = "Fecha Mes(#):", font=("Times New Roman",16))
        self.label_fecha_mes.place(x = 700, y = 10)

        self.texto_fecha_mes = CTkEntry(self)
        self.texto_fecha_mes.place(x = 800, y = 10)
        

        self.label_fecha_año = CTkLabel(self, text = "Fecha Año(#):", font=("Times New Roman",16))
        self.label_fecha_año.place(x = 980, y = 10)
        
        self.texto_fecha_anio = CTkEntry(self)
        self.texto_fecha_anio.place(x = 1090, y = 10)        

        opcion_radio_btn_pago_entrenador = IntVar()

        self.radio_btn_diario = CTkRadioButton(self, variable = opcion_radio_btn_pago_entrenador, value = 1, text="Por dia")
        self.radio_btn_diario.place(x = 100 , y = 50)

        self.radio_btn_mensual = CTkRadioButton(self, variable = opcion_radio_btn_pago_entrenador, value = 2, text="Por mes")
        self.radio_btn_mensual.place(x = 1000 , y = 50)

        # ********************* para escoger la fecha ********************
        def seleccionar_fecha_entrenadores():
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
                self.texto_fecha_completa.delete(0,END)
                self.texto_fecha_anio.delete(0,END)
                self.texto_fecha_mes.delete(0,END)
                
                fecha_select = cal.get_date()
                anio = fecha_select[0:4]
                mes = fecha_select[5:7]

                self.texto_fecha_completa.insert(0,str(fecha_select)) 
                self.texto_fecha_anio.insert(0,anio)
                self.texto_fecha_mes.insert(0,mes)  

                calendario.destroy()                 
                

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()

        self.btn_seleccionar_fecha = CTkButton(self, text="Fecha",command=seleccionar_fecha_entrenadores, width = 40, height = 27)
        self.btn_seleccionar_fecha.place(x = 500, y = 50)

        # ***************************************************************************************************

        

        self.label_importe_personalizado = CTkLabel(self, text = "Importe Personalizado:", font=("Times New Roman",16))
        self.label_importe_personalizado.place(x = 1060, y = 120)        

        string_resultado_importe_personalizado_pago_entrenadores = StringVar()
        string_resultado_importe_personalizado_pago_entrenadores.set("")

        self.label_resultado_importe_personalizado = CTkLabel(self, textvariable = string_resultado_importe_personalizado_pago_entrenadores, font=("Times New Roman",16))
        self.label_resultado_importe_personalizado.place(x = 1060, y = 170)
        

        self.label_importe_dirigido = CTkLabel(self, text = "Importe Dirigido:", font=("Times New Roman",16))
        self.label_importe_dirigido.place(x = 1060, y = 220)        

        string_resultado_importe_dirigido_pago_entrenadores = StringVar()
        string_resultado_importe_dirigido_pago_entrenadores.set("")

        self.label_resultado_importe_dirigido = CTkLabel(self, textvariable = string_resultado_importe_dirigido_pago_entrenadores, font=("Times New Roman",16))
        self.label_resultado_importe_dirigido.place(x = 1060, y = 270)


        self.label_importe_agrego = CTkLabel(self, text = "Importe Agregados:", font=("Times New Roman",16))
        self.label_importe_agrego.place(x = 1060, y = 320)        

        string_resultado_importe_agrego_pago_entrenadores = StringVar()
        string_resultado_importe_agrego_pago_entrenadores.set("")

        self.label_resultado_importe_agrego = CTkLabel(self, textvariable = string_resultado_importe_agrego_pago_entrenadores, font=("Times New Roman",16))
        self.label_resultado_importe_agrego.place(x = 1060, y = 370)
        

        self.label_importe_total = CTkLabel(self, text = "Total Importe:", font=("Times New Roman",16))
        self.label_importe_total.place(x = 1060, y = 520)        

        string_resultado_importe_total_pago_entrenadores = StringVar()
        string_resultado_importe_total_pago_entrenadores.set("")

        self.label_resultado_importe_total = CTkLabel(self, textvariable = string_resultado_importe_total_pago_entrenadores, font=("Times New Roman",16))
        self.label_resultado_importe_total.place(x = 1060, y = 570)


        self.label_importe_extra = CTkLabel(self, text = "Extra:", font=("Times New Roman",16))
        self.label_importe_extra.place(x = 1060, y = 420)        

        string_resultado_importe_extra_pago_entrenadores = StringVar()
        string_resultado_importe_extra_pago_entrenadores.set("")

        self.label_resultado_importe_extra = CTkLabel(self, textvariable = string_resultado_importe_extra_pago_entrenadores, font=("Times New Roman",16))
        self.label_resultado_importe_extra.place(x = 1060, y = 470)
                

        self.tabla_pago = ttk.Treeview(self, columns = ("Fecha","Id","nombre_completo","Modalidad", "Entrenador", "Activacion", "Importe", "Pago_Entrenador"))
        self.tabla_pago.column("#0", width = 40)
        self.tabla_pago.column("Fecha", width = 120)
        self.tabla_pago.column("Id", width = 80)
        self.tabla_pago.column("nombre_completo", width = 200)
        self.tabla_pago.column("Modalidad", width = 120)
        self.tabla_pago.column("Entrenador", width = 120)
        self.tabla_pago.column("Activacion", width = 100)
        self.tabla_pago.column("Importe", width = 100)
        self.tabla_pago.column("Pago_Entrenador", width = 100)
        self.tabla_pago.place(x = 25, y = 150)
        self.tabla_pago.config(height = 15)
        self.tabla_pago.heading("#0", text = "No.")
        self.tabla_pago.heading("Fecha", text = "Fecha")
        self.tabla_pago.heading("Id", text = "Id")
        self.tabla_pago.heading("nombre_completo", text = "Nombre Completo")
        self.tabla_pago.heading("Modalidad", text = "Modalidad")
        self.tabla_pago.heading("Entrenador", text = "Entrenador")
        self.tabla_pago.heading("Activacion", text = "Pagar Activacion")
        self.tabla_pago.heading("Importe", text = "Importe")
        self.tabla_pago.heading("Pago_Entrenador", text = "Pago Entrenador")

        self.scrollbar = CTkScrollbar(self, command = self.tabla_pago.yview, width = 18)
        self.scrollbar.place(in_ = self.tabla_pago, relheigh = 1, relx = 1)

        self.tabla_pago.config(yscrollcommand = self.scrollbar.set)

        

        def generar_pago_entrenadores():
            try:
                self.tabla_pago.delete(*self.tabla_pago.get_children())                
                string_resultado_importe_dirigido_pago_entrenadores.set("")
                string_resultado_importe_personalizado_pago_entrenadores.set("")
                string_resultado_importe_total_pago_entrenadores.set("") 
                string_resultado_importe_extra_pago_entrenadores.set("") 
                string_resultado_importe_agrego_pago_entrenadores.set("")
                
                int_resultado_importe_personalizado_pago_trabajadores = 0                
                int_resultado_importe_dirigido_pago_trabajadores = 0
                int_resultado_importe_agrego_pago_trabajadores = 0
                int_resultado_importe_total_pago_trabajadores = 0
                int_resultado_importe_extra_pago_trabajadores = 0

                if opcion_radio_btn_pago_entrenador.get() == 1:  
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "ysos",
                        password = "123456",
                        database = "ysos"
                        )
                    cursor = conn.cursor()


                    sql = f"""SELECT * FROM `pagos` WHERE fecha = '{date(int(self.texto_fecha_completa.get()[0:4]),int(self.texto_fecha_completa.get()[5:7]),int(self.texto_fecha_completa.get()[8:10]))}';"""
                    cursor.execute(sql)

                    contador = 0
                    for index in cursor:
                        contador += 1
                        if index[4] == self.texto_entrenador.get():
                            self.tabla_pago.insert("", END , text = contador, values = (f"{index[0]}",f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}"))
                        
                        if index[3] == "Personalizado": 
                            if index[4] == self.texto_entrenador.get():
                                int_resultado_importe_personalizado_pago_trabajadores += int(index[7])                

                        elif index[3] == "Dirigido":
                            if index[4] == self.texto_entrenador.get():
                                int_resultado_importe_dirigido_pago_trabajadores += int(index[7])

                        elif index[3] == "Agrego":
                            if index[4] == self.texto_entrenador.get():
                                int_resultado_importe_agrego_pago_trabajadores += int(index[7]) 
                                                                           
                        else:
                            if index[4] == self.texto_entrenador.get():
                                int_resultado_importe_extra_pago_trabajadores += int(index[7])                       
                        
                    
                    int_resultado_importe_total_pago_trabajadores = int_resultado_importe_personalizado_pago_trabajadores  + int_resultado_importe_dirigido_pago_trabajadores + int_resultado_importe_agrego_pago_trabajadores + int_resultado_importe_extra_pago_trabajadores

                    string_resultado_importe_dirigido_pago_entrenadores.set(str(int_resultado_importe_dirigido_pago_trabajadores))
                    string_resultado_importe_personalizado_pago_entrenadores.set(str(int_resultado_importe_personalizado_pago_trabajadores))
                    string_resultado_importe_agrego_pago_entrenadores.set(str(int_resultado_importe_agrego_pago_trabajadores))            
                    string_resultado_importe_total_pago_entrenadores.set(str(int_resultado_importe_total_pago_trabajadores))
                    string_resultado_importe_extra_pago_entrenadores.set(str(int_resultado_importe_extra_pago_trabajadores))

                elif opcion_radio_btn_pago_entrenador.get() == 2:
                    
                    anio = int(self.texto_fecha_anio.get())
                    mes = int(self.texto_fecha_mes.get())
                    fecha_inicio = date(anio,mes,1)
                    fecha_final = date(anio,mes,1)

                    ############## ahora hay que hallar la fecha final ##################
                    if mes == 12:
                        fecha_final = date(anio + 1, 1, 1)
                    else:
                        fecha_final = date(anio,mes + 1,1)
                        
                    contador = 0

                    while fecha_inicio < fecha_final:            
                        
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "ysos",
                            password = "123456",
                            database = "ysos"
                            )
                        cursor = conn.cursor()

                        sql = f"""SELECT * FROM `pagos` WHERE fecha = '{fecha_inicio}';"""
                        cursor.execute(sql)
                        
                        for index in cursor:
                            contador += 1                            
                            if index[4] == self.texto_entrenador.get():
                                self.tabla_pago.insert("", END , text = contador, values = (f"{index[0]}",f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}"))
                            
                            if index[3] == "Personalizado": 
                                if index[4] == self.texto_entrenador.get():
                                    int_resultado_importe_personalizado_pago_trabajadores += int(index[7])                

                            elif index[3] == "Dirigido":
                                if index[4] == self.texto_entrenador.get():
                                    int_resultado_importe_dirigido_pago_trabajadores += int(index[7])

                            elif index[3] == "Agrego":
                                if index[4] == self.texto_entrenador.get():
                                    int_resultado_importe_agrego_pago_trabajadores += int(index[7]) 
                                                                            
                            else:
                                if index[4] == self.texto_entrenador.get():
                                    int_resultado_importe_extra_pago_trabajadores += int(index[7]) 

                        fecha_inicio = fecha_inicio + timedelta(days = 1)

                    int_resultado_importe_total_pago_entrenadores = int_resultado_importe_dirigido_pago_trabajadores + int_resultado_importe_personalizado_pago_trabajadores + int_resultado_importe_agrego_pago_trabajadores + int_resultado_importe_extra_pago_trabajadores

                    string_resultado_importe_dirigido_pago_entrenadores.set(str(int_resultado_importe_dirigido_pago_trabajadores))
                    string_resultado_importe_personalizado_pago_entrenadores.set(str(int_resultado_importe_personalizado_pago_trabajadores))
                    string_resultado_importe_agrego_pago_entrenadores.set(str(int_resultado_importe_agrego_pago_trabajadores))
                    string_resultado_importe_total_pago_entrenadores.set(str(int_resultado_importe_total_pago_entrenadores))
                    string_resultado_importe_extra_pago_entrenadores.set(str(int_resultado_importe_extra_pago_trabajadores))
                    
            except:
                error = messagebox.showinfo("Error","Escribe bien los datos para poder generar el balance")

        def cerrar_pago_entrenadores(): 
            self.destroy()  
    


        self.btn_cerrar = CTkButton(self, command = cerrar_pago_entrenadores, text = "Cerrar", width = 200, height = 30)
        self.btn_cerrar.place(x = 800, y = 600)        

        self.btn_generar_balance = CTkButton(self, command = generar_pago_entrenadores, text = "Ver Pago", width = 200, height = 30)
        self.btn_generar_balance.place(x = 150, y = 600)


# **********************************************************************************
# ***************************** entrenadores ***************************************
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
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False)) 


        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/entrenadores.jpg"), size = (800,600))      
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        global tabla_entrenadores
        tabla_entrenadores = ttk.Treeview(self, columns = ())
        tabla_entrenadores.column("#0", width = 500)


        tabla_entrenadores.place(x = 150, y = 100)
        tabla_entrenadores.config(height = 10)
        tabla_entrenadores.heading("#0", text = "Nombre")


        scrollbar_entrenadores = CTkScrollbar(self, command = tabla_entrenadores.yview, width = 18)
        scrollbar_entrenadores.place(in_ = tabla_entrenadores, relheigh = 1, relx = 1)

        tabla_entrenadores.config(yscrollcommand = scrollbar_entrenadores.set)

        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `entrenadores`;"""
        cursor.execute(sql)

        for index in cursor:
            tabla_entrenadores.insert("",END, text = index[0])

        def agregar_entrenador():
            agregar_entrenador = AgregarEntrenador()

        def eliminar_entrenador():
            eliminar_entrenador = EliminarEntrenador()

        def cerrar_entrenador():
            self.destroy()

        self.btn_agregar = CTkButton(self, text = "Agregar", command = agregar_entrenador, width = 200, height = 30)
        self.btn_agregar.place(x = 100, y = 400)        

        self.btn_eliminar = CTkButton(self , text = "Eliminar", command = eliminar_entrenador, width = 200, height = 30)
        self.btn_eliminar.place(x = 500, y = 400)        

        self.btn_cerrar = CTkButton(self, text = "Cerrar", command = cerrar_entrenador, width = 300, height = 50)
        self.btn_cerrar.place(x = 250, y = 500)

# **********************************************************************************
# ******************************* agregar entrenador *******************************
# **********************************************************************************

class AgregarEntrenador(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agregar Entrenador")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False)  
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
       

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/entrenadores.jpg"), size = (800,400))               
        
        self.label_imagen = CTkLabel(self, image = self.imagen)
        self.label_imagen.place(x = 0 , y = 0)

        self.label_nuevo_entrenador = CTkLabel(self, text = "Nuevo Entrenador", font=("Times New Roman",16))
        self.label_nuevo_entrenador.place(x = 100, y = 70)        

        self.text_nuevo_entrenador = CTkEntry(self, width = 200, height = 30)
        self.text_nuevo_entrenador.place(x = 100, y = 140)

        def confirmar_agregar_entrenador():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                cursor = conn.cursor()

                sql = f"""INSERT INTO `entrenadores` (`nombre`) VALUES ('{self.text_nuevo_entrenador.get()}');"""
                cursor.execute(sql)
                conn.commit()

                tabla_entrenadores.insert("", END, text = f'{self.text_nuevo_entrenador.get()}')
                self.destroy()
            except:
                error = messagebox.showinfo("Error","Hay problemas para agregar este entrenador")


        def cancelar_agregar_entrenador():
            self.destroy()

        self.btn_confirmar = CTkButton(self, text = "Agregar", command = confirmar_agregar_entrenador, width = 200, height = 30)
        self.btn_confirmar.place(x = 100, y = 300)        

        self.btn_cancelar = CTkButton(self, text = "Cancelar", command = cancelar_agregar_entrenador, width = 200, height = 30)
        self.btn_cancelar.place(x = 400, y = 300)

# **********************************************************************************
# ******************************** eliminar entrenador *****************************
# **********************************************************************************

class EliminarEntrenador(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Elimminar Entrenador")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))         

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/entrenadores.jpg"), size = (800,400))                           
        
        self.label_imagen = CTkLabel(self, image = self.imagen)
        self.label_imagen.place(x = 0 , y = 0)

        self.label_eliminar_entrenador = CTkLabel(self, text = "Eliminar Entrenador", font=("Times New Roman",16))
        self.label_eliminar_entrenador.place(x = 250, y = 70)

        items_entrenador = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()
        sql = """SELECT `nombre` FROM `entrenadores` """
        cursor.execute(sql)

        for index in cursor:
            items_entrenador.append(index[0])        
        
        self.text_eliminar_entrenador = ttk.Combobox(self, width = 50)
        self.text_eliminar_entrenador.place(x = 250, y = 160)
        self.text_eliminar_entrenador['values'] = items_entrenador
                   

        def confirmar_eliminar_entrenador():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                cursor = conn.cursor()
                sql = f"""DELETE FROM `entrenadores` WHERE nombre = '{self.text_eliminar_entrenador.get()}'"""
                cursor.execute(sql)
                conn.commit()
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar el entrenador")

        # ****************** actualizar tabla entrenador ***************************
            tabla_entrenadores.delete(*tabla_entrenadores.get_children())

            sql = """SELECT * FROM `entrenadores`;"""
            cursor.execute(sql)

            for index in cursor:
                tabla_entrenadores.insert("",END, text = index[0])
            
            self.destroy()

            
        def cancelar_confirmar_eliminar_entrenadores():
            self.destroy()

        self.btn_confirmar = CTkButton(self, text = "Eliminar", command = confirmar_eliminar_entrenador, width = 200, height = 30)
        self.btn_confirmar.place(x = 100, y = 300)
        
        self.btn_cancelar = CTkButton(self, text = "Cancelar", command = cancelar_confirmar_eliminar_entrenadores, width = 200, height = 30)
        self.btn_cancelar.place(x = 400, y = 300)


# **********************************************************************************
# **************************** seguridad_modalidad *********************************
# **********************************************************************************

class SeguridadModalidad(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Seguridad Modalidad")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 400
        hventana = 200
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("400x200") 
        self.resizable(False,False)
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))       

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/logo3.jpg"), size = (400,200))                  
        
        self. label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self. label_imagen.place(x = 0 , y = 0)

        self.label_seguridad = CTkLabel(self,text="Insertar contraseña:", font=("Times New Roman",16))
        self.label_seguridad.place(x = 10, y = 10)        

        self.texto_contraseña = CTkEntry(self, width = 200)
        self.texto_contraseña.place(x = 100, y = 80)        

        def aceptar_seguridad_modalidad():
            conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
            cursor = conn.cursor()

            sql = f"""SELECT `pass_economia` FROM `licencias`;"""
            cursor.execute(sql)

            for index in cursor:
                if self.texto_contraseña.get() == index[0]:                    
                    self.destroy()                    
                    modalidad = Modalidad()
                                        

                else:
                    error = messagebox.showinfo("Error", "Contraseña incorrecta")


        def cambiar_seguridad_modalidad():
            cambiar_contraseña = CambiarContraseña()

        def cancelar_seguridad_modalidad():
            self.destroy()

        btn_aceptar_seguridad_economia = CTkButton(self, command = aceptar_seguridad_modalidad, text = "Aceptar", width = 100, height = 30)
        btn_aceptar_seguridad_economia.place(x = 20, y = 130)        

        btn_cambiar_seguridad_economia = CTkButton(self, command = cambiar_seguridad_modalidad, text = "Cambiar", width = 100, height = 30)
        btn_cambiar_seguridad_economia.place(x = 140, y = 130)        

        btn_cancelar_seguridad_economia = CTkButton(self, command = cancelar_seguridad_modalidad, text = "Cancelar", width = 100, height = 30)
        btn_cancelar_seguridad_economia.place(x = 260, y = 130)


# **********************************************************************************
# **************************** modalidad *******************************************
# **********************************************************************************

class Modalidad(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Modalidad")    
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

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (800,600))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        global tabla_modalidad
        tabla_modalidad = ttk.Treeview(self, columns = ("Precio","Pago Entrenador"))
        tabla_modalidad.column("#0", width = 200)
        tabla_modalidad.column("Precio", width = 200)
        tabla_modalidad.column("Pago Entrenador", width = 200)

        tabla_modalidad.place(x = 100, y = 100)
        tabla_modalidad.config(height = 10)
        tabla_modalidad.heading("#0", text = "Modalidad")
        tabla_modalidad.heading("Precio", text = "Precio")
        tabla_modalidad.heading("Pago Entrenador", text = "Pago Entrenador")

        scrollbar_modalidad = CTkScrollbar(self, command = tabla_modalidad.yview, width = 18)
        scrollbar_modalidad.place(in_ = tabla_modalidad, relheigh = 1, relx = 1)

        tabla_modalidad.config(yscrollcommand = scrollbar_modalidad.set)


        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `modalidad`;"""
        cursor.execute(sql)

        for index in cursor:
            tabla_modalidad.insert("",END, text = index[0], values = (index[1], index[2]))
            

        def agregar_modalidad():
            agregar_modalidad_economia = AgregarModalidad()
            

        def eliminar_modalidad():
            eliminar_modalidad_economia = EliminarModalidad()


        def cerrar_modalidad():
            self.destroy()

        btn_agregar_modalidad = CTkButton(self, text = "Agregar", command = agregar_modalidad, width = 100, height = 30)
        btn_agregar_modalidad.place(x = 150, y = 400)        

        btn_eliminar_modalidad = CTkButton(self , text = "Eliminar", command = eliminar_modalidad, width = 100, height = 30)
        btn_eliminar_modalidad.place(x = 550, y = 400)        

        btn_cerrar_modalidad = CTkButton(self, text = "Cerrar", command = cerrar_modalidad, width = 200, height = 30)
        btn_cerrar_modalidad.place(x = 300, y = 500)

# **********************************************************************************
# ************************* agregar_modalidad **************************************
# **********************************************************************************

class AgregarModalidad(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agegar Modalidad")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))       

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (800,400))                    
        
        self.label_imagen_agregar_modalidad_economia = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen_agregar_modalidad_economia.place(x = 0 , y = 0)

        self.label_nueva_modalidad = CTkLabel(self, text = "Nueva Modalidad", font=("Times New Roman",16))
        self.label_nueva_modalidad.place(x = 100, y = 70)        

        self.label_nuevo_precio = CTkLabel(self, text = "Precio", font=("Times New Roman",16))
        self.label_nuevo_precio.place(x = 300, y = 70)

        self.label_nuevo_pago_entrenadores = CTkLabel(self, text = "Pago Entrenador", font=("Times New Roman",16))
        self.label_nuevo_pago_entrenadores.place(x = 500, y = 70)        

        self.text_nueva_modalidad = CTkEntry(self)
        self.text_nueva_modalidad.place(x = 100, y = 160)

        self.text_nuevo_precio = CTkEntry(self)
        self.text_nuevo_precio.place(x = 300, y = 160)

        self.text_nuevo_pago_entrenador = CTkEntry(self)
        self.text_nuevo_pago_entrenador.place(x = 500, y = 160)

        def confirmar_agregar_modalidad():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                cursor = conn.cursor()

                sql = f"""INSERT INTO `modalidad` (`modalidad`, `precio`, `pago_entrenador`) VALUES ('{self.text_nueva_modalidad.get()}', '{self.text_nuevo_precio.get()}', '{self.text_nuevo_pago_entrenador.get()}');"""
                cursor.execute(sql)
                conn.commit()

                tabla_modalidad.insert("", END, text = f'{self.text_nueva_modalidad.get()}', values = (f'{self.text_nuevo_precio.get()}', f'{self.text_nuevo_pago_entrenador.get()}'))
                self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo agregar la modalidad")


        def cancelar_agregar_modalidad():
            self.destroy()

        btn_confirmar_agregar_modalidad = CTkButton(self, text = "Agregar", command = confirmar_agregar_modalidad, width = 200, height = 30)
        btn_confirmar_agregar_modalidad.place(x = 100, y = 300)        

        btn_cancelar_agregar_modalidad = CTkButton(self, text = "Cancelar", command = cancelar_agregar_modalidad, width = 200, height = 30)
        btn_cancelar_agregar_modalidad.place(x = 400, y = 300)
        

# **********************************************************************************
# *************************** eliminar_modalidad ***********************************
# **********************************************************************************

class EliminarModalidad(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Eliminar Modalidad")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (800,400))                       
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label = CTkLabel(self, text = "Eliminar Modalidad", font=("Times New Roman",16))
        self.label.place(x = 250, y = 70)
        

        items_modalidad = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()
        sql = """SELECT `modalidad` FROM `modalidad`;"""
        cursor.execute(sql)

        for index in cursor:
            items_modalidad.append(index[0])            
        
        self.text = ttk.Combobox(self, width = 30)
        self.text.place(x = 250, y = 160)        
        self.text['values'] = items_modalidad    
        

        def eliminar_modalidad():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                cursor = conn.cursor()

                sql = f"""DELETE FROM `modalidad` WHERE modalidad = '{self.text.get()}'"""
                cursor.execute(sql)
                conn.commit()
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar la modalidad")

        # ****************** actualizar tabla modalidad ***************************
            tabla_modalidad.delete(*tabla_modalidad.get_children())  # esto borra toda la tabla 

            sql = """SELECT * FROM `modalidad`;"""
            cursor.execute(sql)

            for index in cursor:
                tabla_modalidad.insert("",END, text = index[0])

            self.destroy()

            
        def cancelar_eliminar_modalidad():
            self.destroy()

        self.btn_confirmar = CTkButton(self, text = "Eliminar", command = eliminar_modalidad, width = 200, height = 30)
        self.btn_confirmar.place(x = 100, y = 300)        

        self.btn_cancelar = CTkButton(self, text = "Cancelar", command = cancelar_eliminar_modalidad, width = 200, height = 30)
        self.btn_cancelar.place(x = 400, y = 300)

# **********************************************************************************
# **************************** agrego *******************************************
# **********************************************************************************

class Agrego(CTkToplevel):     
    def __init__(self):                               
        self = CTkToplevel()        
        self.title("Agrego")    
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

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (800,600))                         
    
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        global tabla_agregos
        tabla_agregos = ttk.Treeview(self, columns = ("Precio","Pago Entrenador"))
        tabla_agregos.column("#0", width = 200)
        tabla_agregos.column("Precio", width = 200)
        tabla_agregos.column("Pago Entrenador", width = 200)

        tabla_agregos.place(x = 100, y = 100)
        tabla_agregos.config(height = 10)
        tabla_agregos.heading("#0", text = "Agrego")
        tabla_agregos.heading("Precio", text = "Precio")
        tabla_agregos.heading("Pago Entrenador", text = "Pago Entrenador")

        scrollbar_agregos = CTkScrollbar(self, command = tabla_agregos.yview, width = 18)
        scrollbar_agregos.place(in_ = tabla_agregos, relheigh = 1, relx = 1)

        tabla_agregos.config(yscrollcommand = scrollbar_agregos.set)


        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()

        sql = """SELECT * FROM `agrego`;"""
        cursor.execute(sql)

        for index in cursor:
            tabla_agregos.insert("",END, text = index[0], values = (index[1], index[2]))

        global listado_agregos   # para controlar los agregos 
        listado_agregos = []
            

        def agregar_agrego():
            agregar_modalidad_economia = AgregarAgrego()
            

        def eliminar_agrego():
            eliminar_modalidad_economia = EliminarAgrego()


        def cerrar_agrego():
            self.destroy()

        btn_agregar_agrego = CTkButton(self, text = "Agregar", command = agregar_agrego, width = 100, height = 30)
        btn_agregar_agrego.place(x = 150, y = 400)        

        btn_eliminar_agrego = CTkButton(self , text = "Eliminar", command = eliminar_agrego, width = 100, height = 30)
        btn_eliminar_agrego.place(x = 550, y = 400)        

        btn_cerrar_agrego = CTkButton(self, text = "Cerrar", command = cerrar_agrego, width = 200, height = 30)
        btn_cerrar_agrego.place(x = 300, y = 500)

# **********************************************************************************
# ************************* agregar_agrego **************************************
# **********************************************************************************

class AgregarAgrego(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agegar Agrego")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico')) 
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))       

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (800,400))                    
        
        self.label_imagen_agregar_agrego_economia = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen_agregar_agrego_economia.place(x = 0 , y = 0)

        self.label_nuevo_agrego = CTkLabel(self, text = "Nuevo Agrego", font=("Times New Roman",16))
        self.label_nuevo_agrego.place(x = 100, y = 70)        

        self.label_nuevo_precio = CTkLabel(self, text = "Precio", font=("Times New Roman",16))
        self.label_nuevo_precio.place(x = 300, y = 70)

        self.label_nuevo_pago_entrenadores = CTkLabel(self, text = "Pago Entrenador", font=("Times New Roman",16))
        self.label_nuevo_pago_entrenadores.place(x = 500, y = 70)        

        self.text_nuevo_agrego = CTkEntry(self)
        self.text_nuevo_agrego.place(x = 100, y = 160)

        self.text_nuevo_precio = CTkEntry(self)
        self.text_nuevo_precio.place(x = 300, y = 160)

        self.text_nuevo_pago_entrenador = CTkEntry(self)
        self.text_nuevo_pago_entrenador.place(x = 500, y = 160)

        def confirmar_agregar_agrego():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                cursor = conn.cursor()

                sql = f"""INSERT INTO `agrego` (`agrego`, `precio`, `pago entrenador`) VALUES ('{self.text_nuevo_agrego.get()}', '{self.text_nuevo_precio.get()}', '{self.text_nuevo_pago_entrenador.get()}');"""
                cursor.execute(sql)
                conn.commit()

                tabla_agregos.insert("", END, text = f'{self.text_nuevo_agrego.get()}', values = (f'{self.text_nuevo_precio.get()}', f'{self.text_nuevo_pago_entrenador.get()}'))
                self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo agregar la modalidad")


        def cancelar_agregar_agrego():
            self.destroy()

        btn_confirmar_agregar_agrego = CTkButton(self, text = "Agregar", command = confirmar_agregar_agrego, width = 200, height = 30)
        btn_confirmar_agregar_agrego.place(x = 100, y = 300)        

        btn_cancelar_agregar_agrego = CTkButton(self, text = "Cancelar", command = cancelar_agregar_agrego, width = 200, height = 30)
        btn_cancelar_agregar_agrego.place(x = 400, y = 300)

# **********************************************************************************
# *************************** eliminar_agrego ***********************************
# **********************************************************************************

class EliminarAgrego(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()        
        self.title("Eliminar Agrego")    
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 800
        hventana = 400
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry("800x400") 
        self.resizable(False,False) 
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (800,400))                       
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label = CTkLabel(self, text = "Eliminar Agrego", font=("Times New Roman",16))
        self.label.place(x = 250, y = 70)
        

        items_agregos = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()
        sql = """SELECT `agrego` FROM `agrego`;"""
        cursor.execute(sql)

        for index in cursor:
            items_agregos.append(index[0])            
        
        self.text = ttk.Combobox(self, width = 30)
        self.text.place(x = 250, y = 160)        
        self.text['values'] = items_agregos    
        

        def eliminar_agrego():
            try:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                cursor = conn.cursor()

                sql = f"""DELETE FROM `agrego` WHERE agrego = '{self.text.get()}'"""
                cursor.execute(sql)
                conn.commit()
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar el agrego")

        # ****************** actualizar tabla agrego ***************************
            tabla_agregos.delete(*tabla_agregos.get_children())  # esto borra toda la tabla 

            sql = """SELECT * FROM `agrego`;"""
            cursor.execute(sql)

            for index in cursor:
                tabla_agregos.insert("",END, text = index[0])

            self.destroy()

            
        def cancelar_eliminar_agrego():
            self.destroy()

        self.btn_confirmar = CTkButton(self, text = "Eliminar", command = eliminar_agrego, width = 200, height = 30)
        self.btn_confirmar.place(x = 100, y = 300)        

        self.btn_cancelar = CTkButton(self, text = "Cancelar", command = cancelar_eliminar_agrego, width = 200, height = 30)
        self.btn_cancelar.place(x = 400, y = 300)


# *********************************************************************************
# *************************** pagos atrasados *************************************
# *********************************************************************************

class ClientesAtrasados(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Pagos Atrasados")    
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

        try:                        
            self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_agregar_cliente.jpg"), size = (1000,600))      

            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 600)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No hay foto")

        listado = Listbox(self)
        listado.config(selectmode = SINGLE , width = 118 , height = 20)
        listado.place(x = 150 , y = 100)

        self.scrollbar = CTkScrollbar(self, command = listado.yview, width = 18)
        self.scrollbar.place(in_ = listado, relheigh = 1, relx = 1)

        listado.config(yscrollcommand = self.scrollbar.set)

        
        def buscar_atrasados():            

            listado.delete(0,END) 

            conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
            cursor = conn.cursor() 

            sql = """SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2`, `Telefono`, `Fecha_Pago` FROM `clientes`"""
            cursor.execute(sql)

            for index in cursor:
                if index[5] < fecha_actual:
                    string_atrasados  = ""
                    string_atrasados += str(index[0]) +  "  " + index[1] + "  " + index[2] + "  " + index[3] + "  " + index[4] + "  " + str(index[5])
                    listado.insert(END, string_atrasados)

        def cerrar_atrasados():
            self.destroy()

        self.btn =  CTkButton(self, text = "Buscar", command = buscar_atrasados, width = 300, height = 50)
        self.btn.place(x = 150, y = 500)
        self.btn =  CTkButton(self, text = "Salir", command = cerrar_atrasados, width = 300, height = 50)
        self.btn.place(x = 550, y = 500)

                

        


# **********************************************************************************
# *********************** trabajo con agregar_cliente ******************************
# **********************************************************************************

class AgregarCliente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Agregar Cliente")    
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

        global ultimo_id 
        ultimo_id = StringVar()
        ultimo_id.set("")

        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()

        sql = """SELECT MAX(ID) FROM `clientes`;"""
        cursor.execute(sql)
        
        for index in cursor:                
            ultimo_id.set(index[0])

        label_ultimo_id = CTkLabel(self, textvariable = ultimo_id)
        label_ultimo_id.place(x = 650, y = 70) 
        


        # ************************** Labels *************************        

        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 738, y = 70)        

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 110)        

        self.label_apellido1 = CTkLabel(self,text="Apellido1:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 692, y = 150)        

        self.label_apellido2 = CTkLabel(self,text="Apellido2:", font=("Times New Roman",16))
        self.label_apellido2.place(x = 692, y = 190)        

        self.label_modalidad = CTkLabel(self,text="Modalidad:", font=("Times New Roman",16))
        self.label_modalidad.place(x = 684, y = 230)  

        items_modalidad = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()

        sql = """SELECT `modalidad` FROM `modalidad`"""
        cursor.execute(sql)
        for index in cursor:
            items_modalidad.append(index[0])

        global texto_modalidad_agregar_cliente
        texto_modalidad_agregar_cliente = ttk.Combobox(self)
        texto_modalidad_agregar_cliente.place(x = 800, y = 233)  
        texto_modalidad_agregar_cliente['values'] = items_modalidad       

        self.label_entrenador = CTkLabel(self,text="Entrenador:", font=("Times New Roman",16))
        self.label_entrenador.place(x = 681, y = 270) 

        items_entrenador = []
        sql = """SELECT * FROM `entrenadores`"""
        cursor.execute(sql)
        for index in cursor:
            items_entrenador.append(index[0])
        global texto_entrenador_agregar_cliente
        texto_entrenador_agregar_cliente = ttk.Combobox(self)
        texto_entrenador_agregar_cliente.place(x = 800, y = 275)
        texto_entrenador_agregar_cliente['values'] = items_entrenador       

        self.label_ultima_asistencia = CTkLabel(self,text="Ultima Asistencia:", font=("Times New Roman",16))
        self.label_ultima_asistencia.place(x = 650, y = 310)        

        self.label_fecha_pago = CTkLabel(self,text="Pago:", font=("Times New Roman",16))
        self.label_fecha_pago.place(x = 725, y = 350)        

        self.label_estado = CTkLabel(self,text="Estado:", font=("Times New Roman",16))
        self.label_estado.place(x = 716, y = 390) 
                
        items_estado = ["Activo", "Inactivo"]
        global texto_estado_agregar_cliente
        texto_estado_agregar_cliente = ttk.Combobox(self)
        texto_estado_agregar_cliente.place(x = 800, y = 395)
        texto_estado_agregar_cliente['values'] = items_estado       

        self.label_telefono = CTkLabel(self,text="Telefono:", font=("Times New Roman",16))
        self.label_telefono.place(x = 700, y = 430)
        

        # ******************** Text ***************************

        global texto_id_agregar_cliente
        texto_id_agregar_cliente = CTkEntry(self)
        texto_id_agregar_cliente.place(x = 800, y = 70)

        global texto_nombre_agregar_cliente
        texto_nombre_agregar_cliente = CTkEntry(self)
        texto_nombre_agregar_cliente.place(x = 800, y = 110)
        
        global texto_apellido1_agregar_cliente
        texto_apellido1_agregar_cliente = CTkEntry(self)
        texto_apellido1_agregar_cliente.place(x = 800, y = 150)
        
        global texto_apellido2_agregar_cliente
        texto_apellido2_agregar_cliente = CTkEntry(self)
        texto_apellido2_agregar_cliente.place(x = 800, y = 190)
        
        global texto_asistencia_agregar_cliente
        texto_asistencia_agregar_cliente = CTkEntry(self)
        texto_asistencia_agregar_cliente.place(x = 800, y = 310)
        
        global texto_fecha_pago_agregar_cliente
        texto_fecha_pago_agregar_cliente = CTkEntry(self)
        texto_fecha_pago_agregar_cliente.place(x = 800, y = 350)        
        
        global texto_telefono_agregar_cliente
        texto_telefono_agregar_cliente = CTkEntry(self)
        texto_telefono_agregar_cliente.place(x = 800, y = 430)


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
                texto_asistencia_agregar_cliente.delete(0,END)
                texto_fecha_pago_agregar_cliente.delete(0,END)

                fecha_select = cal.get_date()

                anio = int(fecha_select[0:4])
                mes = int(fecha_select[5:7])
                dia = int(fecha_select[8:10])
                            
                nuevo_anio = anio
                nuevo_mes = mes + 1
                nuevo_dia = dia

                if dia == 31 and mes != 7 and mes != 12:
                    nuevo_dia = 1
                    nuevo_mes = mes + 2
                
                elif mes == 12:
                    nuevo_anio = anio + 1 
                    nuevo_mes = 1

                elif mes == 1:
                    if dia > 28:
                        nuevo_dia = 1
                        nuevo_mes = mes + 2

                nueva_fecha_pago = date(nuevo_anio,nuevo_mes,nuevo_dia)

                texto_asistencia_agregar_cliente.insert(0,str(fecha_select))
                texto_fecha_pago_agregar_cliente.insert(0,str(nueva_fecha_pago))

                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()       
            
        
        self.btn_fecha = CTkButton(self,text="...",command=btn_fecha_agregar_cliente, width = 27, height = 27)
        self.btn_fecha.place(x=950 ,y=310 )

        def confirmar_agregar_cliente():
            try:
                conn = mysql.connector.connect(
                host = "localhost",
                user = "ysos",
                password = "123456",
                database = "ysos"
                )
                cursor = conn.cursor()

                sql = """SELECT ID FROM clientes;"""
                cursor.execute(sql)


                id_repetido = False
                

                for index in cursor:        
            
                    if int(texto_id_agregar_cliente.get()) == index[0]:
                        id_repetido = True

                if id_repetido == False:   
                    confirmar_cliente = ConfirmarCliente()

                else:
                    error = messagebox.showinfo("Error", "Ese ID ya existe")
            except:
                error = messagebox.showinfo("Error","Escribe bien los datos")
            
                
            
        def cancelar_agregar_cliente():            
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=confirmar_agregar_cliente, width = 150, height = 40)
        self.btn_aceptar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_agregar_cliente, width = 150, height = 40)
        self.btn_cancelar.place(x=820 ,y=500 )

        

# **********************************************************************************
# *************************** trabajo confirmar_cliente ****************************
# **********************************************************************************

class ConfirmarCliente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Confirmar Cliente")    
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

        id_buscado = texto_id_agregar_cliente.get()
        
        # ****************** Labels *********************************

        # **** aqui tengo que escribir el label de confirmar donde saldran lo datos de agregar_clientes ********
        self.label2_id = CTkLabel(self, text = texto_id_agregar_cliente.get())
        self.label2_id.place(x = 800, y = 75)
                
        self.label2_nombre = CTkLabel(self , text = texto_nombre_agregar_cliente.get())
        self.label2_nombre.place(x = 800, y = 115)
                
        self.label2_apellido1 = CTkLabel(self , text = texto_apellido1_agregar_cliente.get())
        self.label2_apellido1.place(x = 800, y = 155)
        
        self.label2_apellido2 = CTkLabel(self , text = texto_apellido2_agregar_cliente.get())
        self.label2_apellido2.place(x = 800, y = 195)
                
        self.label2_modalidad = CTkLabel(self , text = texto_modalidad_agregar_cliente.get())
        self.label2_modalidad.place(x = 800, y = 235)
                
        self.label2_entrenador = CTkLabel(self , text = texto_entrenador_agregar_cliente.get())
        self.label2_entrenador.place(x = 800, y = 275)
                
        self.label2_ultima_asistencia = CTkLabel(self , text = texto_asistencia_agregar_cliente.get())
        self.label2_ultima_asistencia.place(x = 800, y = 315)
                
        self.label2_fecha_pago = CTkLabel(self , text = texto_fecha_pago_agregar_cliente.get())
        self.label2_fecha_pago.place(x = 800, y = 355)        
        
        self.label2_estado = CTkLabel(self , text = texto_estado_agregar_cliente.get())
        self.label2_estado.place(x = 800, y = 395)        
        
        self.label2_telefono = CTkLabel(self , text = texto_telefono_agregar_cliente.get())
        self.label2_telefono.place(x = 800, y = 435)                                                        
        

        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 745, y = 70)        

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 710, y = 110)        

        self.label_apellido1 = CTkLabel(self,text="Apellido1:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 700, y = 150)        

        self.label_apellido2 = CTkLabel(self,text="Apellido2:", font=("Times New Roman",16))
        self.label_apellido2.place(x = 700, y = 190)
        
        self.label_modalidad = CTkLabel(self,text="Modalidad:", font=("Times New Roman",16))
        self.label_modalidad.place(x = 694, y = 230)
        
        self.label_entrenador = CTkLabel(self,text="Entrenador:", font=("Times New Roman",16))
        self.label_entrenador.place(x = 690, y = 270)
        
        self.label_ultima_asistencia = CTkLabel(self,text="Ultima Asistencia:", font=("Times New Roman",16))
        self.label_ultima_asistencia.place(x = 650, y = 310)
        
        self.label_fecha_pago = CTkLabel(self,text="Pago:", font=("Times New Roman",16))
        self.label_fecha_pago.place(x = 730, y = 350)
        
        self.label_estado = CTkLabel(self,text="Estado:", font=("Times New Roman",16))
        self.label_estado.place(x = 716, y = 390)
        
        self.label_telefono = CTkLabel(self,text="Telefono:", font=("Times New Roman",16))
        self.label_telefono.place(x = 700, y = 430)

        # **************** botones *******************

        def confirmar_confirmar_cliente():   

            conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
            cursor = conn.cursor()
            
            
            sql = f"""INSERT INTO `clientes` (`ID`, `Nombre`, `Apellido 1`, `Apellido 2`, `Modalidad`, `Entrenador`, `Telefono`, `Ultima_Asistencia`, `Fecha_Pago`) VALUES ('{texto_id_agregar_cliente.get()}', '{texto_nombre_agregar_cliente.get()}', '{texto_apellido1_agregar_cliente.get()}', '{texto_apellido2_agregar_cliente.get()}', '{texto_modalidad_agregar_cliente.get()}', '{texto_entrenador_agregar_cliente.get()}', '{texto_telefono_agregar_cliente.get()}', '{texto_asistencia_agregar_cliente.get()}', '{texto_fecha_pago_agregar_cliente.get()}') """
            cursor.execute(sql)
            conn.commit()

            
            conn = mysql.connector.connect(
                host = "localhost",
                user = "ysos",
                password = "123456",
                database = "ysos"
                )
            cursor = conn.cursor()

            sql = """SELECT MAX(ID) FROM `clientes`;"""
            cursor.execute(sql)
            
            for index in cursor:                
                ultimo_id.set(index[0]) 

            ########### crear el pago por la entrada del cliente nuevo #############
        
            nombre_completo = texto_nombre_agregar_cliente.get() + " " + texto_apellido1_agregar_cliente.get() + " " + texto_apellido2_agregar_cliente.get()
            
            ################# buscar el importe  de entrada ##############
            importe_agregar_cliente = 0
            pago_entrenador_agregar_cliente = 0
            sql = """SELECT * FROM `modalidad`"""
            cursor.execute(sql)
                
            for index in cursor:
                if texto_modalidad_agregar_cliente.get() == index[0]:
                    importe_agregar_cliente = index[1]
                    pago_entrenador_agregar_cliente = index[2]

            
            sql = f""" INSERT INTO `pagos`(`fecha`, `id`, `nombre_completo`, `modalidad`, `Entrenador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{fecha_actual}','{texto_id_agregar_cliente.get()}','{nombre_completo}','{texto_modalidad_agregar_cliente.get()}', '{texto_entrenador_agregar_cliente.get()}', 'SI','{importe_agregar_cliente}','{pago_entrenador_agregar_cliente}')"""
            cursor.execute(sql)
            conn.commit()           

            self.destroy()

        def rotar_confirmar_cliente():
            self.imagen = CTkImage(Image.open(f"D:/gym_Coliseo/fotos_gym/gym_Clientes/{int(texto_id_agregar_cliente.get())}.jpg"), size = (600,600))                                
            
            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 600)
            self.label_imagen.place(x = 0 , y = 0)

        def cancelar_confirmar_cliente():    
            self.destroy()

        self.btn_rotar = CTkButton(self,text="Rotar",command=rotar_confirmar_cliente, width = 150, height = 30)
        self.btn_rotar.place(x=650 ,y=10 )
        
        self.btn_confirmar = CTkButton(self,text="Confirmar",command=confirmar_confirmar_cliente, width = 150, height = 30)
        self.btn_confirmar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_confirmar_cliente, width = 150, height = 30)
        self.btn_cancelar.place(x=820 ,y=500 )

        ################# imagen ########################
        try:
            self.imagen = CTkImage(Image.open(f"D:/gym_Coliseo/fotos_gym/gym_Clientes/{id_buscado}.jpg").rotate(270), size = (600,600))                                
            
            self.label_imagen = CTkLabel(self, image = self.imagen, text = "", width = 600, height = 600)
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")

# *************************************************************************************
# ******************* trabajo con modificar_cliente ***********************************
# *************************************************************************************

class ModificarCliente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Modificar Cliente")    
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
        

        # **************** Imagenes *********************
        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/modificar cliente.jpg"), size = (1000,600))                            
        
        self.label_imagen = CTkLabel(self, image = self.imagen)
        self.label_imagen.place(x = 0 , y = 0)


        #  *************** Labels ***********************

        self.label_buscar_por_id = CTkLabel(self,text="Buscar por ID:", font=("Times New Roman",16))
        self.label_buscar_por_id.place(x = 100, y = 20)        

        self.label__buscar_por_nombre = CTkLabel(self,text="Buscar por Nombre:", font=("Times New Roman",16))
        self.label__buscar_por_nombre.place(x = 650, y = 20)

        self.label__buscar_por_apellido = CTkLabel(self,text="Buscar por Apellido:", font=("Times New Roman",16))
        self.label__buscar_por_apellido.place(x = 650, y = 55)
        

        # ***************** Entrys *****************
        
        global texto_buscar_por_id_modificar_cliente
        texto_buscar_por_id_modificar_cliente = CTkEntry(self)
        texto_buscar_por_id_modificar_cliente.place(x = 200, y = 20)

        self.texto_buscar_por_nombre = CTkEntry(self)
        self.texto_buscar_por_nombre.place(x = 800, y = 20)

        self.texto_buscar_por_apellido = CTkEntry(self)
        self.texto_buscar_por_apellido.place(x = 800, y = 55)
        
        global listado_modificar_cliente
        listado_modificar_cliente = Listbox(self)
        listado_modificar_cliente.config(selectmode = SINGLE , width = 118 , height = 15)
        listado_modificar_cliente.place(x = 150 , y = 200)

        self.scrollbar = CTkScrollbar(self, command = listado_modificar_cliente.yview, width = 18)
        self.scrollbar.place(in_ = listado_modificar_cliente, relheigh = 1, relx = 1)

        listado_modificar_cliente.config(yscrollcommand = self.scrollbar.set)

        id_buscado = ''
        # ******************* boton ******************        

        def buscar_modificar_cliente(): 

            try: 
                # ****************** si me dan el id ******************************

                if texto_buscar_por_id_modificar_cliente.get() != "":

                    id_buscado = texto_buscar_por_id_modificar_cliente.get()
                    
                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()

                    sql = f"""SELECT ID FROM `clientes` WHERE ID = {id_buscado}; """
                    cursor.execute(sql)
                    
                    cursor_vacio = True

                    for index in cursor:
                        if index[0] != None:
                            cursor_vacio = False
                    
                    if cursor_vacio == False:                  

                        confirmar_modificacion_cliente = ConfirmarModificarCliente()

                    else:
                        error = messagebox.showinfo("Error", "No hay ningun ID con ese numero")

                # ******************** si me dan el nombre **********************************
                elif self.texto_buscar_por_nombre.get() != "":
                    listado_modificar_cliente.delete(0,END)
                    string_lista = ""

                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()
                            
                    sql = f"""SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE Nombre = '{self.texto_buscar_por_nombre.get()}' """
                    cursor.execute(sql)
                    

                    for index in cursor:
                        string_lista = ""
                        string_lista += str(index[0])+ '  ' + index[1] + '  ' + index[2] + '  ' + index[3]
                        listado_modificar_cliente.insert(END , string_lista)

                # ****************** si me dan el 1er apellido ****************************
                elif self.texto_buscar_por_apellido.get() != "":

                    listado_modificar_cliente.delete(0,END)

                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()
                            
                    sql = f"""SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE `Apellido 1` = '{self.texto_buscar_por_apellido.get()}' """
                    cursor.execute(sql)

                    for index in cursor:
                        string_lista = ""
                        string_lista += str(index[0])+ '  ' + index[1] + '  ' + index[2] + '  ' + index[3]
                        listado_modificar_cliente.insert(END , string_lista)
                    
                else:
                    error = messagebox.showwarning("Error","Debe escribir algun parametro para buscar")
            except:
                error = messagebox.showinfo("Error","Escribe bien los datos")
            
        def cerrar_modificar_cliente():
            self.destroy()

        self.btn_buscar = CTkButton(self,text="Buscar",command=buscar_modificar_cliente, width = 500, height = 50)
        self.btn_buscar.place(x=230 ,y=100 )        

        self.btn_cerrar = CTkButton(self,text="Cerrar",command=cerrar_modificar_cliente, width = 500, height = 50)
        self.btn_cerrar.place(x=230 ,y=500 ) 
        

#  ***************************************************************************************
#  ******************************** confirmar_modificacion_cliente ***********************
#  ***************************************************************************************

class ConfirmarModificarCliente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Confirmar Modificacion del Cliente")    
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

        id_buscado = texto_buscar_por_id_modificar_cliente.get()
        
        
        
        ############################ labels fijos ################################

        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 740, y = 70)        

        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 110)        

        self.label_apellido1 = CTkLabel(self,text="Apellido1:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 690, y = 150)        

        self.label_apellido2 = CTkLabel(self,text="Apellido2:", font=("Times New Roman",16))
        self.label_apellido2.place(x = 690, y = 190)        

        self.label_modalidad = CTkLabel(self,text="Modalidad:", font=("Times New Roman",16))
        self.label_modalidad.place(x = 684, y = 230)        

        self.label_entrenador = CTkLabel(self,text="Entrenador:", font=("Times New Roman",16))
        self.label_entrenador.place(x = 681, y = 270)        

        self.label_ultima_asistencia = CTkLabel(self,text="Ultima Asistencia:", font=("Times New Roman",16))
        self.label_ultima_asistencia.place(x = 640, y = 310)        

        self.label_fecha_pago = CTkLabel(self,text="Pago:", font=("Times New Roman",16))
        self.label_fecha_pago.place(x = 722, y = 350)        

        self.label_estado = CTkLabel(self,text="Estado:", font=("Times New Roman",16))
        self.label_estado.place(x = 716, y = 390)        

        self.label_telefono = CTkLabel(self,text="Telefono:", font=("Times New Roman",16))
        self.label_telefono.place(x = 700, y = 430)     
        

        ############################ labels dependientes #########################
        ##################### para que funcione el combobox de lamodalidad ###################
        items_modalidad = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()

        sql = """SELECT `modalidad` FROM `modalidad`"""
        cursor.execute(sql)
        for index in cursor:
            items_modalidad.append(index[0])
        ############################## hasta aqui ###########################################
        ############################## ahora el combobox de entrenadores ####################
        items_entrenador = []
        sql = """SELECT `nombre` FROM `entrenadores`"""
        cursor.execute(sql)
        for index in cursor:
            items_entrenador.append(index[0])
        ################################## hasta aqui #######################################
        # ***** aqui debo configurar para que salga la info que tenia antes *******
        sql = f"""SELECT * FROM `clientes` WHERE ID = {id_buscado}; """
        cursor.execute(sql) 
        for index in cursor:
            string_texto_id_confirmar_modificacion_cliente = StringVar()
            string_texto_id_confirmar_modificacion_cliente.set(str(index[0]))            
            global texto_id_confirmar_modificacion_cliente
            texto_id_confirmar_modificacion_cliente = CTkEntry(self, textvariable = string_texto_id_confirmar_modificacion_cliente)                
            texto_id_confirmar_modificacion_cliente.place(x = 800, y = 70)
            
            string_texto_nombre_confirmar_modificacion_cliente = StringVar()
            string_texto_nombre_confirmar_modificacion_cliente.set(str(index[1]))
            global texto_nombre_confirmar_modificacion_cliente
            texto_nombre_confirmar_modificacion_cliente = CTkEntry(self, textvariable = string_texto_nombre_confirmar_modificacion_cliente)
            texto_nombre_confirmar_modificacion_cliente.place(x = 800, y = 110)
            
            string_texto_apellido1_confirmar_modificacion_cliente = StringVar()
            string_texto_apellido1_confirmar_modificacion_cliente.set(str(index[2]))
            global texto_apellido1_confirmar_modificacion_cliente
            texto_apellido1_confirmar_modificacion_cliente = CTkEntry(self, textvariable = string_texto_apellido1_confirmar_modificacion_cliente)
            texto_apellido1_confirmar_modificacion_cliente.place(x = 800, y = 150)
            
            string_texto_apellido2_confirmar_modificacion_cliente = StringVar()
            string_texto_apellido2_confirmar_modificacion_cliente.set(str(index[3]))
            global texto_apellido2_confirmar_modificacion_cliente
            texto_apellido2_confirmar_modificacion_cliente = CTkEntry(self, textvariable = string_texto_apellido2_confirmar_modificacion_cliente)
            texto_apellido2_confirmar_modificacion_cliente.place(x = 800, y = 190)
            
            string_texto_modalidad_confirmar_modificacion_cliente = StringVar()
            string_texto_modalidad_confirmar_modificacion_cliente.set(str(index[4]))
            global texto_modalidad_confirmar_modificacion_cliente
            texto_modalidad_confirmar_modificacion_cliente = ttk.Combobox(self, textvariable = string_texto_modalidad_confirmar_modificacion_cliente)
            texto_modalidad_confirmar_modificacion_cliente.place(x = 800, y = 233)
            texto_modalidad_confirmar_modificacion_cliente['values'] = items_modalidad
            
            string_texto_entrenador_confirmar_modificacion_cliente = StringVar()
            string_texto_entrenador_confirmar_modificacion_cliente.set(str(index[5]))
            global texto_entrenador_confirmar_modificacion_cliente
            texto_entrenador_confirmar_modificacion_cliente = ttk.Combobox(self, textvariable = string_texto_entrenador_confirmar_modificacion_cliente)
            texto_entrenador_confirmar_modificacion_cliente.place(x = 800, y = 275)
            texto_entrenador_confirmar_modificacion_cliente['values'] = items_entrenador
            
            string_texto_asistencia_confirmar_modificacion_cliente = StringVar()
            string_texto_asistencia_confirmar_modificacion_cliente.set(str(index[7]))
            global texto_asistencia_confirmar_modificacion_cliente
            texto_asistencia_confirmar_modificacion_cliente = CTkEntry(self, textvariable = string_texto_asistencia_confirmar_modificacion_cliente)
            texto_asistencia_confirmar_modificacion_cliente.place(x = 800, y = 310)
            
            string_texto_fecha_pago_confirmar_modificacion_cliente = StringVar()
            string_texto_fecha_pago_confirmar_modificacion_cliente.set(str(index[8]))
            global texto_fecha_pago_confirmar_modificacion_cliente
            texto_fecha_pago_confirmar_modificacion_cliente = CTkEntry(self, textvariable = string_texto_fecha_pago_confirmar_modificacion_cliente)
            texto_fecha_pago_confirmar_modificacion_cliente.place(x = 800, y = 350)
            
            items_estado = ["Activo", "Inactivo"]
            global texto_estado_confirmar_modificacion_cliente
            texto_estado_confirmar_modificacion_cliente = ttk.Combobox(self)
            texto_estado_confirmar_modificacion_cliente.place(x = 800, y = 395)
            texto_estado_confirmar_modificacion_cliente['values'] = items_estado
            
            string_texto_telefono_confirmar_modificacion_cliente = StringVar()
            string_texto_telefono_confirmar_modificacion_cliente.set(str(index[6]))
            global texto_telefono_confirmar_modificacion_cliente
            texto_telefono_confirmar_modificacion_cliente = CTkEntry(self, textvariable = string_texto_telefono_confirmar_modificacion_cliente)
            texto_telefono_confirmar_modificacion_cliente.place(x = 800, y = 430)          
        
        # *********************** seleccionar fecha ****************************

        def btn_fecha_modificar_cliente_asistencia(): 

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
                fecha_select = cal.get_date()                
                string_texto_asistencia_confirmar_modificacion_cliente.set(str(fecha_select))
                

                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()            
            
        
        self.btn_fecha_asistencia = CTkButton(self,text="...",command=btn_fecha_modificar_cliente_asistencia, width = 27, height = 27)
        self.btn_fecha_asistencia.place(x=950 ,y=310 )

        def btn_fecha_modificar_cliente_pago(): 

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
                fecha_select = cal.get_date()                
                string_texto_fecha_pago_confirmar_modificacion_cliente.set(str(fecha_select))
                

                calendario.destroy()

            btn = CTkButton(calendario, text="Insertar Fecha", command=fecha)
            btn.pack()            
            
        
        self.btn_fecha_pago = CTkButton(self,text="...",command=btn_fecha_modificar_cliente_pago, width = 27, height = 27)
        self.btn_fecha_pago.place(x=950 ,y=350 )
        # ************************************************************************************

        def confirmar_modificar_cliente(): 
            try:  
                conn = mysql.connector.connect(
                host = "localhost",
                user = "ysos",
                password = "123456",
                database = "ysos"
                )
                cursor = conn.cursor()
                    
                sql = f""" UPDATE `clientes` SET `Nombre`='{texto_nombre_confirmar_modificacion_cliente.get()}',`Apellido 1`='{texto_apellido1_confirmar_modificacion_cliente.get()}',`Apellido 2`='{texto_apellido2_confirmar_modificacion_cliente.get()}',`Modalidad`='{texto_modalidad_confirmar_modificacion_cliente.get()}',`Entrenador`='{texto_entrenador_confirmar_modificacion_cliente.get()}',`Telefono`='{texto_telefono_confirmar_modificacion_cliente.get()}',`Ultima_Asistencia`='{texto_asistencia_confirmar_modificacion_cliente.get()}',`Fecha_Pago`='{texto_fecha_pago_confirmar_modificacion_cliente.get()}' WHERE ID = {texto_buscar_por_id_modificar_cliente.get()} """
                cursor.execute(sql)
                conn.commit()

                self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo modificar el cliente")          

        def rotar_confirmar_modificar_cliente():
            self.imagen = CTkImage(Image.open(f"D:/gym_Coliseo/fotos_gym/gym_Clientes/{id_buscado}.jpg"), size = (600,600))                           
            
            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)

        def cancelar_modificar_cliente():
            self.destroy()

        self.btn_rotar = CTkButton(self,text="Rotar",command=rotar_confirmar_modificar_cliente, width = 100, height = 30)
        self.btn_rotar.place(x=650 ,y=10 )        

        self.btn_modificar = CTkButton(self,text="Modificar",command=confirmar_modificar_cliente, width = 100, height = 30)
        self.btn_modificar.place(x=650 ,y=500 )        

        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_modificar_cliente, width = 100, height = 30)
        self.btn_cancelar.place(x=820 ,y=500 )

        try:
            self.imagen = CTkImage(Image.open(f"D:/gym_Coliseo/fotos_gym/gym_Clientes/{id_buscado}.jpg").rotate(270), size = (600,600))                           
            
            self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
            self.label_imagen.place(x = 0 , y = 0)

        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")
        
# ******************************************************************************************
# ******************************** eliminar_cliente ****************************************
# ******************************************************************************************

class EliminarCliente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Eliminar Cliente")    
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

        self.imagen = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/eliminar cliente.jpg"), size = (1000,600))                           
        
        self.label_imagen = CTkLabel(self, image = self.imagen, text = "")
        self.label_imagen.place(x = 0 , y = 0)

        self.label_buscar_por_id = CTkLabel(self,text="Buscar por ID:", font=("Times New Roman",16))
        self.label_buscar_por_id.place(x = 50, y = 20)        

        self.label__buscar_por_nombre = CTkLabel(self,text="Buscar por Nombre:", font=("Times New Roman",16))
        self.label__buscar_por_nombre.place(x = 650, y = 20)

        self.label__buscar_por_apellido = CTkLabel(self,text="Buscar por Apellido:", font=("Times New Roman",16))
        self.label__buscar_por_apellido.place(x = 650, y = 55)

        self.texto_buscar_por_id = CTkEntry(self)
        self.texto_buscar_por_id.place(x = 150, y = 20)

        self.texto_buscar_por_nombre = CTkEntry(self)
        self.texto_buscar_por_nombre.place(x = 800, y = 20)

        self.texto_buscar_por_apellido = CTkEntry(self)
        self.texto_buscar_por_apellido.place(x = 800, y = 55)

        listado_eliminar_cliente = Listbox(self)
        listado_eliminar_cliente.config(selectmode = SINGLE , width = 118 , height = 15)
        listado_eliminar_cliente.place(x = 150 , y = 200)

        self.scrollbar = CTkScrollbar(self, command = listado_eliminar_cliente.yview, width = 18)
        self.scrollbar.place(in_ = listado_eliminar_cliente, relheigh = 1, relx = 1)

        listado_eliminar_cliente.config(yscrollcommand = self.scrollbar.set)

        def buscar_eliminar_cliente():
            try: 
                # ****************** si me dan el id ******************************

                if self.texto_buscar_por_id.get() != "":

                    global id_buscado
                    id_buscado = self.texto_buscar_por_id.get()           
                    

                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()

                    sql = f"""SELECT ID FROM `clientes` WHERE ID = {id_buscado}; """
                    cursor.execute(sql)
                    
                    cursor_vacio = True

                    for index in cursor:
                        if index[0] != None:
                            cursor_vacio = False
                    
                    if cursor_vacio == False: 
                        confirmar_eliminacion_cliente = ConfirmarEliminarCliente()

                    else:
                        error = messagebox.showinfo("Error", "No hay ningun ID con ese numero")

                # ******************** si me dan el nombre **********************************
                elif self.texto_buscar_por_nombre.get() != "":
                    listado_eliminar_cliente.delete(0,END)
                    string_lista = ""

                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()
                            
                    sql = f"""SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE Nombre = '{self.texto_buscar_por_nombre.get()}' """
                    cursor.execute(sql)
                    

                    for index in cursor:
                        string_lista = ""
                        string_lista += str(index[0])+ '  ' + index[1] + '  ' + index[2] + '  ' + index[3]
                        listado_eliminar_cliente.insert(END , string_lista)

                # ******************** si me dan el 1er apellido *****************************
                elif self.texto_buscar_por_apellido.get() != "":
                    listado_eliminar_cliente.delete(0,END)
                    string_lista = ""

                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()
                            
                    sql = f"""SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE `Apellido 1` = '{self.texto_buscar_por_apellido.get()}' """
                    cursor.execute(sql)
                    

                    for index in cursor:
                        string_lista = ""
                        string_lista += str(index[0])+ '  ' + index[1] + '  ' + index[2] + '  ' + index[3]
                        listado_eliminar_cliente.insert(END , string_lista)

                else:
                    error = messagebox.showwarning("Error","Debe escribir algun parametro para buscar")
            except:
                error = messagebox.showinfo("Error","Escribe bien los datos")

        def cerrar_eliminar_cliente(): 
            self.destroy()


        self.btn_buscar = CTkButton(self,text="Buscar",command=buscar_eliminar_cliente, width = 500, height = 40)
        self.btn_buscar.place(x=250 ,y=100 )        

        self.btn_cerrar = CTkButton(self,text="Cerrar",command=cerrar_eliminar_cliente, width = 500, height = 40)
        self.btn_cerrar.place(x=250 ,y=500 )
        

# *****************************************************************************************
# ******************************* confirmar_eliminar_cliente ******************************
# *****************************************************************************************

class ConfirmarEliminarCliente(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Confirmar Eliminacion de Cliente")    
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
        
        ################## labels fijos #######################

        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 735, y = 70)
        
        self.label_nombre = CTkLabel(self,text="Nombre:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 110)
        
        self.label_apellido1 = CTkLabel(self,text="Apellido1:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 690, y = 150)        

        self.label_apellido2 = CTkLabel(self,text="Apellido2:", font=("Times New Roman",16))
        self.label_apellido2.place(x = 690, y = 190)
        
        self.label_modalidad = CTkLabel(self,text="Modalidad:", font=("Times New Roman",16))
        self.label_modalidad.place(x = 684, y = 230)
        
        self.label_entrenador = CTkLabel(self,text="Entrenador:", font=("Times New Roman",16))
        self.label_entrenador.place(x = 681, y = 270)
        
        self.label_ultima_asistencia = CTkLabel(self,text="Ultima Asistencia:", font=("Times New Roman",16))
        self.label_ultima_asistencia.place(x = 650, y = 310)
        
        self.label_fecha_pago = CTkLabel(self,text="Pago:", font=("Times New Roman",16))
        self.label_fecha_pago.place(x = 730, y = 350)        

        self.label_estado = CTkLabel(self,text="Estado:", font=("Times New Roman",16))
        self.label_estado.place(x = 716, y = 390)
        
        self.label_telefono = CTkLabel(self,text="Telefono:", font=("Times New Roman",16))
        self.label_telefono.place(x = 700, y = 430)
        
        sql = f"""SELECT * FROM `clientes` WHERE ID = {id_buscado}; """
        cursor.execute(sql) 
        for index in cursor:
            string_texto_id_confirmar_eliminacion_cliente = StringVar()
            string_texto_id_confirmar_eliminacion_cliente.set(str(index[0]))
            global texto_id_confirmar_eliminacion_cliente
            texto_id_confirmar_eliminacion_cliente = CTkEntry(self, textvariable = string_texto_id_confirmar_eliminacion_cliente)                
            texto_id_confirmar_eliminacion_cliente.place(x = 800, y = 75)
            
            string_texto_nombre_confirmar_eliminacion_cliente = StringVar()
            string_texto_nombre_confirmar_eliminacion_cliente.set(str(index[1]))
            global texto_nombre_confirmar_eliminacion_cliente
            texto_nombre_confirmar_eliminacion_cliente = CTkEntry(self, textvariable = string_texto_nombre_confirmar_eliminacion_cliente)
            texto_nombre_confirmar_eliminacion_cliente.place(x = 800, y = 115)
            
            string_texto_apellido1_confirmar_eliminacion_cliente = StringVar()
            string_texto_apellido1_confirmar_eliminacion_cliente.set(str(index[2]))
            global texto_apellido1_confirmar_eliminacion_cliente
            texto_apellido1_confirmar_eliminacion_cliente = CTkEntry(self, textvariable = string_texto_apellido1_confirmar_eliminacion_cliente)
            texto_apellido1_confirmar_eliminacion_cliente.place(x = 800, y = 155)
            
            string_texto_apellido2_confirmar_eliminacion_cliente = StringVar()
            string_texto_apellido2_confirmar_eliminacion_cliente.set(str(index[3]))
            global texto_apellido2_confirmar_eliminacion_cliente
            texto_apellido2_confirmar_eliminacion_cliente = CTkEntry(self, textvariable = string_texto_apellido2_confirmar_eliminacion_cliente)
            texto_apellido2_confirmar_eliminacion_cliente.place(x = 800, y = 195)
            
            string_texto_modalidad_confirmar_eliminacion_cliente = StringVar()
            string_texto_modalidad_confirmar_eliminacion_cliente.set(str(index[4]))
            global texto_modalidad_confirmar_eliminacion_cliente
            texto_modalidad_confirmar_eliminacion_cliente = CTkEntry(self, textvariable = string_texto_modalidad_confirmar_eliminacion_cliente)
            texto_modalidad_confirmar_eliminacion_cliente.place(x = 800, y = 235)
            
            string_texto_entrenador_confirmar_eliminacion_cliente = StringVar()
            string_texto_entrenador_confirmar_eliminacion_cliente.set(str(index[5]))
            global texto_entrenador_confirmar_eliminacion_cliente
            texto_entrenador_confirmar_eliminacion_cliente = CTkEntry(self, textvariable = string_texto_entrenador_confirmar_eliminacion_cliente)
            texto_entrenador_confirmar_eliminacion_cliente.place(x = 800, y = 275)
            
            string_texto_asistencia_confirmar_eliminacion_cliente = StringVar()
            string_texto_asistencia_confirmar_eliminacion_cliente.set(str(index[8]))
            global texto_asistencia_confirmar_eliminacion_cliente
            texto_asistencia_confirmar_eliminacion_cliente = CTkEntry(self, textvariable = string_texto_asistencia_confirmar_eliminacion_cliente)
            texto_asistencia_confirmar_eliminacion_cliente.place(x = 800, y = 315)
            
            string_texto_fecha_pago_confirmar_eliminacion_cliente = StringVar()
            string_texto_fecha_pago_confirmar_eliminacion_cliente.set(str(index[7]))
            global texto_fecha_pago_confirmar_eliminacion_cliente
            texto_fecha_pago_confirmar_eliminacion_cliente = CTkEntry(self, textvariable = string_texto_fecha_pago_confirmar_eliminacion_cliente)
            texto_fecha_pago_confirmar_eliminacion_cliente.place(x = 800, y = 355)
            
            
            global texto_estado_confirmar_eliminacion_cliente
            texto_estado_confirmar_eliminacion_cliente = CTkEntry(self)
            texto_estado_confirmar_eliminacion_cliente.place(x = 800, y = 395)
            
            string_texto_telefono_confirmar_eliminacion_cliente = StringVar()
            string_texto_telefono_confirmar_eliminacion_cliente.set(str(index[6]))
            global texto_telefono_confirmar_eliminacion_cliente
            texto_telefono_confirmar_eliminacion_cliente = CTkEntry(self, textvariable = string_texto_telefono_confirmar_eliminacion_cliente)
            texto_telefono_confirmar_eliminacion_cliente.place(x = 800, y = 435)

        def confirmar_eliminar_cliente():
            try:   
                conn = mysql.connector.connect(
                host = "localhost",
                user = "ysos",
                password = "123456",
                database = "ysos"
                )
                cursor = conn.cursor()
                    
                sql = f""" DELETE FROM `clientes` WHERE ID = {id_buscado} """
                cursor.execute(sql)
                conn.commit()

                self.destroy()
            except:
                error = messagebox.showinfo("Error","No se pudo eliminar el cliente")

        def rotar_confirmar_eliminar_cliente():
            try:
                global imagen_confirmar_eliminacion_cliente
                imagen_confirmar_eliminacion_cliente = CTkImage(Image.open(f"D:/gym_Coliseo/fotos_gym/gym_Clientes/{id_buscado}.jpg"), size = (600,600))                                
                
                self.label_imagen = CTkLabel(self, image = imagen_confirmar_eliminacion_cliente, width = 600, height = 600, text = "")
                self.label_imagen.place(x = 0 , y = 0)
            except:
                error = messagebox.showinfo("Error", "No se pudo cargar la imagen")


        def cancelar_eliminar_cliente():
            self.destroy()

        self.btn_rotar = CTkButton(self,text="Rotar",command=rotar_confirmar_eliminar_cliente, width = 300, height = 30)
        self.btn_rotar.place(x=630 ,y=10 )
        
        self.btn_confirmar = CTkButton(self,text="Eliminar",command=confirmar_eliminar_cliente, width = 150, height = 30)
        self.btn_confirmar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_eliminar_cliente, width = 150, height = 30)
        self.btn_cancelar.place(x=820 ,y=500 )
        
        try:
            global imagen_confirmar_eliminacion_cliente
            imagen_confirmar_eliminacion_cliente = CTkImage(Image.open(f"D:/gym_Coliseo/fotos_gym/gym_Clientes/{id_buscado}.jpg").rotate(270), size = (600,600))                                
            
            self.label_imagen = CTkLabel(self, image = imagen_confirmar_eliminacion_cliente, width = 600, height = 600, text = "")
            self.label_imagen.place(x = 0 , y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")

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
        self.after(250, lambda: self.iconbitmap('D:/gym_Coliseo/fotos_gym/gym_fondos/logo1.ico'))  
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        try:
            global imagen_asistencia_cliente
            imagen_asistencia_cliente = CTkImage(Image.open("D:/gym_Coliseo/fotos_gym/gym_fondos/fondo_asistencia.jpg"), size = (600,600))
            
            self.label_imagen = CTkLabel(self, image = imagen_asistencia_cliente, width = 600, height = 600, text = "")
            self.label_imagen.place(x = 0 , y = 100)

        except:
            error = messagebox.showinfo("Error","No se encontro foto")

        self.label_buscar_por_id = CTkLabel(self,text="Buscar por ID:", font=("Times New Roman",16))
        self.label_buscar_por_id.place(x = 50, y = 20)
        
        self.label__buscar_por_nombre = CTkLabel(self,text="Buscar por Nombre:", font=("Times New Roman",16))
        self.label__buscar_por_nombre.place(x = 970, y = 20)

        self.label__buscar_por_apellido = CTkLabel(self,text="Buscar por Apellido:", font=("Times New Roman",16))
        self.label__buscar_por_apellido.place(x = 970, y = 55)
        
        string_nombre_asistencia_cliente = StringVar()
        string_nombre_asistencia_cliente.set("")

        self.label_nombre = CTkLabel(self,textvariable = string_nombre_asistencia_cliente, font=("Times New Roman",18))
        self.label_nombre.place(x = 650, y = 350)

        string_modalidad_pago_cliente = StringVar()
        string_modalidad_pago_cliente.set("") 

        self.label_modalidad = CTkLabel(self,textvariable = string_modalidad_pago_cliente, font=("Times New Roman",18))
        self.label_modalidad.place(x = 650, y = 400)

        string_entrenador_pago_cliente = StringVar()
        string_entrenador_pago_cliente.set("") 

        self.label_entrenador = CTkLabel(self,textvariable = string_entrenador_pago_cliente, font=("Times New Roman",18))
        self.label_entrenador.place(x = 650, y = 450)
        
        string_pago_asistencia_cliente = StringVar()
        string_pago_asistencia_cliente.set("")

        self.label_pago = CTkLabel(self,textvariable = string_pago_asistencia_cliente, font=("Times New Roman",18))
        self.label_pago.place(x = 650, y = 500)
        
        string_ultima_asistencia_asistencia_cliente = StringVar()
        string_ultima_asistencia_asistencia_cliente.set("")

        self.label_ultima_asistencia = CTkLabel(self,textvariable = string_ultima_asistencia_asistencia_cliente, font=("Times New Roman",18))
        self.label_ultima_asistencia.place(x = 650, y = 550)       
        
        self.texto_buscar_por_id = CTkEntry(self)
        self.texto_buscar_por_id.place(x = 200, y = 20)

        self.texto_buscar_por_nombre = CTkEntry(self)
        self.texto_buscar_por_nombre.place(x = 1120, y = 20)

        self.texto_buscar_por_apellido = CTkEntry(self)
        self.texto_buscar_por_apellido.place(x = 1120, y = 55)

        self.listado = Listbox(self)
        self.listado.config(selectmode = SINGLE , width = 60 , height = 15)
        self.listado.place(x = 900 , y = 200)

        self.scrollbar = CTkScrollbar(self, command = self.listado.yview, width = 18)
        self.scrollbar.place(in_ = self.listado, relheigh = 1, relx = 1)

        self.listado.config(yscrollcommand = self.scrollbar.set)
        
        def buscar_asistencia_cliente(): 
            self.listado.delete(0,END)
            try:
                # ****************** si me dan el id ******************************
                

                if self.texto_buscar_por_id.get() != "":
                    
                    global id_buscado
                    id_buscado = self.texto_buscar_por_id.get()  

                    # escribir los agregos que tiene en la tabla de asistencia y pago 
                    self.listado.delete(0,END)
                    self.listado.insert(END , "Agregos:")

                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()

                    sql = f""" SELECT * FROM `cliente_agrego` WHERE id = {id_buscado}; """
                    cursor.execute(sql)                    

                    for index in cursor:
                        self.listado.insert(END , index[1])
                    # ****************************************************************                  

                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "ysos",
                        password = "123456",
                        database = "ysos"
                        )
                    cursor = conn.cursor()

                    sql = f"""SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2`, `Fecha_Pago`, `Ultima_Asistencia`, `Entrenador`, `Modalidad` FROM `clientes` WHERE ID = {id_buscado}; """
                    cursor.execute(sql)
                    
                    cursor_vacio = True

                    for index in cursor:
                        if index[0] != "":
                            string_nombre_asistencia_cliente.set(index[1] + " " + index[2] + " " + index[3]) 
                            string_ultima_asistencia_asistencia_cliente.set(f"Ultima Asistencia ({index[5]})")
                            string_entrenador_pago_cliente.set(f"Entrenador: {index[6]}")
                            string_modalidad_pago_cliente.set(f"{index[7]}")
                            
                            if fecha_actual > index[4]:
                                string_pago_asistencia_cliente.set(f"Pago Atrasado ({index[4]})")
                                self.label_pago.configure(fg_color="red")           
                                
                                
                            else:
                                string_pago_asistencia_cliente.set(f"Pago En Orden ({index[4]})") 
                                self.label_pago = CTkLabel(self,textvariable = string_pago_asistencia_cliente, font=("Times New Roman",18))
                                self.label_pago.place(x = 650, y = 500)
                                
                            cursor_vacio = False
                            
                    
                    if cursor_vacio == False:
                        
                        try:
                            global imagen_persona_asistencia_cliente
                            imagen_persona_asistencia_cliente = CTkImage(Image.open(f"D:/gym_Coliseo/fotos_gym/gym_Clientes/{id_buscado}.jpg").rotate(270), size = (600,600)) 
                            
                            self.label_imagen = CTkLabel(self, image = imagen_persona_asistencia_cliente, width = 600, height = 600, text = "")
                            self.label_imagen.place(x = 0 , y = 200) 
                        except:
                              error = messagebox.showinfo("Error", "No se pudo cargar la imagen")                       

                    else:
                        error = messagebox.showinfo("Error", "No hay ningun ID con ese numero")



                # ******************** si me dan el nombre **********************************
                elif self.texto_buscar_por_nombre.get() != "":
                    self.listado.delete(0,END)
                    string_lista = ""

                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()
                            
                    sql = f"""SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE Nombre = '{self.texto_buscar_por_nombre.get()}' """
                    cursor.execute(sql)
                    

                    for index in cursor:
                        string_lista = ""
                        string_lista += str(index[0])+ '  ' + index[1] + '  ' + index[2] + '  ' + index[3]
                        self.listado.insert(END , string_lista)

                # ******************** si me dan el 1er apellido **********************************
                elif self.texto_buscar_por_apellido.get() != "":
                    self.listado.delete(0,END)
                    string_lista = ""

                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()
                            
                    sql = f"""SELECT `ID`, `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE `Apellido 1` = '{self.texto_buscar_por_apellido.get()}' """
                    cursor.execute(sql)
                    

                    for index in cursor:
                        string_lista = ""
                        string_lista += str(index[0])+ '  ' + index[1] + '  ' + index[2] + '  ' + index[3]
                        self.listado.insert(END , string_lista)
                    
                    

                else:
                    error = messagebox.showwarning("Error","Debe escribir algun parametro para buscar")
            except:
                error = messagebox.showinfo("Error","Escribe bien los datos")

        def pago_asistencia_cliente():
            try:    
                error = messagebox.askokcancel("Confirmar Pago", "Ejecutar el pago")
                if error == True:
                    ################# ajustar la nueva fecha de pago ############################################
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "ysos",
                        password = "123456",
                        database = "ysos"
                        )
                    cursor = conn.cursor()  
                    sql = f"""SELECT `Ultima_Asistencia` FROM `clientes` WHERE ID = {int(self.texto_buscar_por_id.get())};"""
                    cursor.execute(sql)
                    for index in cursor:  
                        if index[0] + timedelta(days = 90) < fecha_actual:     
                            ############ los que deben pagar activacion ############
                            error = messagebox.askyesno("Pagar Activacion","Esta persona debe pagar la activacion")

                            if error == True:          ################ los que si deben pagar activacion ###################
                                try:                       

                                    ################ hallar nueva fecha de pago en base de datos ################
                                    string_pagar_activacion = "SI"    #### en el balance le saldra 200 pesos mas por reactivacion #####
                                    fecha_pago_actual = str(fecha_actual)
                                    string_nombre_completo_pago = ""
                                    importe_pago = 0 
                                    importe_pago_entrenador = 0                                                    
                                    
                                    anio = int(fecha_pago_actual[0:4])
                                    mes = int(fecha_pago_actual[5:7])
                                    dia = int(fecha_pago_actual[8:10])
                                                
                                    nuevo_anio = anio
                                    nuevo_mes = mes + 1
                                    nuevo_dia = dia

                                    if dia == 31 and mes != 7 and mes != 12:
                                        nuevo_dia = 1
                                        nuevo_mes = mes + 2
                                    
                                    elif mes == 12:
                                        nuevo_anio = anio + 1 
                                        nuevo_mes = 1

                                    elif mes == 1:
                                        if dia > 28:
                                            nuevo_dia = 1
                                            nuevo_mes = mes + 2

                                    nueva_fecha_pago = date(nuevo_anio,nuevo_mes,nuevo_dia)

                                    ############# buscar nombre completo para que salga en el balance #############
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "ysos",
                                        password = "123456",
                                        database = "ysos"
                                        )
                                    cursor = conn.cursor()  

                                    sql = f"""SELECT `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE ID = {self.texto_buscar_por_id.get()};"""
                                    cursor.execute(sql)

                                    for index in cursor:
                                        string_nombre_completo_pago += index[0] + ' ' +  index[1] + ' ' + index[2]

                                    ########### vamos a trabajar con el pago ##################
                                    ########## ver cuanto es el importe ####################
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "ysos",
                                        password = "123456",
                                        database = "ysos"
                                        )
                                    cursor = conn.cursor()

                                    sql = """SELECT * FROM `modalidad`"""
                                    cursor.execute(sql)
                                    for index in cursor:
                                        
                                        if string_modalidad_pago_cliente.get() == index[0]:
                                            importe_pago = index[1]
                                            importe_pago_entrenador = index[2]
                                    
                                    ############ llevar el pago a la base de datos ############  
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "ysos",
                                        password = "123456",
                                        database = "ysos"
                                        )
                                    cursor = conn.cursor() 

                                    sql = f"""SELECT `Entrenador` FROM `clientes` WHERE id = {int(self.texto_buscar_por_id.get())}""" 
                                    cursor.execute(sql)  
                                    for index in cursor:
                                        global string_entrenador_pago_asistencia
                                        string_entrenador_pago_asistencia = str(index[0])
                                    
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "ysos",
                                        password = "123456",
                                        database = "ysos"
                                        )
                                    cursor = conn.cursor()
                                                                                            
                                    sql = f"""INSERT INTO `pagos` (`fecha`, `id`, `nombre_completo`, `modalidad`, `Entrenador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{fecha_actual}', '{int(self.texto_buscar_por_id.get())}', '{string_nombre_completo_pago}', '{string_modalidad_pago_cliente.get()}', '{string_entrenador_pago_asistencia}', '{string_pagar_activacion}', '{importe_pago}', '{importe_pago_entrenador}');"""   
                                    cursor.execute(sql)
                                    conn.commit()   

                                    ################## pagar los agregos contratados #######################
                                    # *************** voy a trabajarlos por listas *******************
                                    lista1 = []
                                    lista2 = []
                                        
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "ysos",
                                        password = "123456",
                                        database = "ysos"
                                        )
                                    cursor = conn.cursor()
                                    sql = f""" SELECT * FROM `cliente_agrego` WHERE id = {int(self.texto_buscar_por_id.get())} """ 
                                    cursor.execute(sql) 
                                    for index in cursor:
                                        lista1.append(index) # aqui tengo los clientes con sus agregos y entrenador
                                    
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "ysos",
                                        password = "123456",
                                        database = "ysos"
                                        )
                                    cursor = conn.cursor()
                                    sql = f""" SELECT * FROM `agrego` """ 
                                    cursor.execute(sql) 
                                    for index in cursor:
                                        lista2.append(index)                               
                                    
                                    for i in lista1:
                                        for y in lista2:
                                            if i[1] == y[0]:
                                                conn = mysql.connector.connect(
                                                    host = "localhost",
                                                    user = "ysos",
                                                    password = "123456",
                                                    database = "ysos"
                                                    )
                                                cursor = conn.cursor()
                                                sql = f""" INSERT INTO `pagos`(`fecha`, `id`, `nombre_completo`, `modalidad`, `Entrenador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{fecha_actual}','{i[0]}','{string_nombre_completo_pago}','Agrego','{i[2]}','NO','{y[1]}','{y[2]}') """
                                                cursor.execute(sql)
                                                conn.commit()                               


                                    ############# cambiar de fecha de pago y ultima asistencia al cliente despues de pagar ################
                                    conn = mysql.connector.connect(
                                        host = "localhost",
                                        user = "ysos",
                                        password = "123456",
                                        database = "ysos"
                                        )
                                    cursor = conn.cursor() 

                                    sql = f"""UPDATE `clientes` SET `Ultima_Asistencia`='{fecha_actual}',`Fecha_Pago`='{nueva_fecha_pago}' WHERE Id = {self.texto_buscar_por_id.get()} """
                                    cursor.execute(sql)
                                    conn.commit() 

                                    ################ actualizar el string del pago y el de la asistencia de asistencia ########################

                                    string_pago_asistencia_cliente.set(f"Pago En Orden ({str(nueva_fecha_pago)})")
                                    self.label_pago = CTkLabel(self,textvariable = string_pago_asistencia_cliente, font=("Times New Roman",18))
                                    self.label_pago.place(x = 650, y = 500)
                                    string_ultima_asistencia_asistencia_cliente.set(f"Ultima Asistencia ({fecha_actual})")

                                except:
                                    error = messagebox.showinfo("Error","No se pudo ejecutar el pago") 
                                                            

                            else:
                                error = messagebox.showinfo("Pagar Autenticacion","Si no paga activacion no ejecuta el pago") 
                                    

                        
                        else:              ################ los que no deben pagar activacion ###################
                            try:
                                
                                ################ hallar nueva fecha de pago en base de datos ################
                                string_pagar_activacion = "NO"
                                fecha_pago_actual = ""
                                string_nombre_completo_pago = ""
                                importe_pago = 0
                                importe_pago_entrenador = 0

                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "ysos",
                                    password = "123456",
                                    database = "ysos"
                                    )
                                cursor = conn.cursor()

                                sql = f""" SELECT `Fecha_Pago` FROM `clientes` WHERE Id = {self.texto_buscar_por_id.get()};"""
                                cursor.execute(sql)
                                
                                for index in cursor:
                                    fecha_pago_actual = str(index[0])            
                                
                                anio = int(fecha_pago_actual[0:4])
                                mes = int(fecha_pago_actual[5:7])
                                dia = int(fecha_pago_actual[8:10])
                                            
                                nuevo_anio = anio
                                nuevo_mes = mes + 1
                                nuevo_dia = dia

                                if dia == 31 and mes != 7 and mes != 12:
                                    nuevo_dia = 1
                                    nuevo_mes = mes + 2
                                
                                elif mes == 12:
                                    nuevo_anio = anio + 1 
                                    nuevo_mes = 1

                                elif mes == 1:
                                    if dia > 28:
                                        nuevo_dia = 1
                                        nuevo_mes = mes + 2

                                nueva_fecha_pago = date(nuevo_anio,nuevo_mes,nuevo_dia)

                                ############# buscar nombre completo para que salga en el balance #############
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "ysos",
                                    password = "123456",
                                    database = "ysos"
                                    )
                                cursor = conn.cursor()

                                sql = f"""SELECT `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE ID = {self.texto_buscar_por_id.get()};"""
                                cursor.execute(sql)

                                for index in cursor:
                                    string_nombre_completo_pago += index[0] + ' ' +  index[1] + ' ' + index[2]

                                
                                ########### vamos a trabajar con el pago ##################
                                ########## ver cuanto es el importe ####################
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "ysos",
                                    password = "123456",
                                    database = "ysos"
                                    )
                                cursor = conn.cursor()

                                sql = """SELECT * FROM `modalidad`"""
                                cursor.execute(sql)                                

                                for index in cursor:
                                    if string_modalidad_pago_cliente.get() == index[0]:
                                        importe_pago = index[1]
                                        importe_pago_entrenador = index[2] 
                                                                     
                                
                                ############ llevar el pago a la base de datos ############
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "ysos",
                                    password = "123456",
                                    database = "ysos"
                                    )
                                cursor = conn.cursor()
                                
                                sql = f"""SELECT `Entrenador` FROM `clientes` WHERE id = {int(self.texto_buscar_por_id.get())}""" 
                                cursor.execute(sql)  
                                for index in cursor:                            
                                    string_entrenador_pago_asistencia = str(index[0])

                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "ysos",
                                    password = "123456",
                                    database = "ysos"
                                    )
                                cursor = conn.cursor()
                                                                                        
                                sql = f"""INSERT INTO `pagos` (`fecha`, `id`, `nombre_completo`, `modalidad`, `Entrenador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{fecha_actual}', '{int(self.texto_buscar_por_id.get())}', '{string_nombre_completo_pago}', '{string_modalidad_pago_cliente.get()}', '{string_entrenador_pago_asistencia}', '{string_pagar_activacion}', '{importe_pago}', '{importe_pago_entrenador}');"""   
                                cursor.execute(sql)
                                conn.commit() 

                                ################## pagar los agregos contratados #######################
                                # *************** voy a trabajarlos por listas *******************
                                lista1 = []
                                lista2 = []
                                    
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "ysos",
                                    password = "123456",
                                    database = "ysos"
                                    )
                                cursor = conn.cursor()
                                sql = f""" SELECT * FROM `cliente_agrego` WHERE id = {int(self.texto_buscar_por_id.get())} """ 
                                cursor.execute(sql) 
                                for index in cursor:
                                    lista1.append(index) # aqui tengo los clientes con sus agregos y entrenador
                                
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "ysos",
                                    password = "123456",
                                    database = "ysos"
                                    )
                                cursor = conn.cursor()
                                sql = f""" SELECT * FROM `agrego` """ 
                                cursor.execute(sql) 
                                for index in cursor:
                                    lista2.append(index)                               
                                
                                for i in lista1:
                                    for y in lista2:
                                        if i[1] == y[0]:
                                            conn = mysql.connector.connect(
                                                host = "localhost",
                                                user = "ysos",
                                                password = "123456",
                                                database = "ysos"
                                                )
                                            cursor = conn.cursor()                                            
                                            sql = f""" INSERT INTO `pagos`(`fecha`, `id`, `nombre_completo`, `modalidad`, `Entrenador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{fecha_actual}','{i[0]}','{string_nombre_completo_pago}','Agrego','{i[2]}','NO','{y[1]}','{y[2]}') """
                                            cursor.execute(sql)
                                            conn.commit()


                                ################### atualizar fecha de pago en la base de datos ####################
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "ysos",
                                    password = "123456",
                                    database = "ysos"
                                    )
                                cursor = conn.cursor()

                                sql = f"""UPDATE `clientes` SET `Ultima_Asistencia`='{fecha_actual}',`Fecha_Pago`='{nueva_fecha_pago}' WHERE Id = {self.texto_buscar_por_id.get()} """
                                cursor.execute(sql)
                                conn.commit() 

                                ################ actualizar el string del pago de asistencia ########################

                                string_pago_asistencia_cliente.set(f"Pago En Orden ({str(nueva_fecha_pago)})")
                                self.label_pago = CTkLabel(self,textvariable = string_pago_asistencia_cliente, font=("Times New Roman",18))
                                self.label_pago.place(x = 650, y = 500)
                                string_ultima_asistencia_asistencia_cliente.set(f"Ultima Asistencia ({fecha_actual})")
                            except:
                                temp = True
                else:
                    error = messagebox.askokcancel("Pago","Pago Cancelado")
                                
            except:
                temp = True        

                
            

        def asistio_asistencia_cliente():
            try:
                error = messagebox.askokcancel("Asistio","Confirmar Asistencia")
                if error == True:
                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()

                    sql = f"""UPDATE `clientes` SET `Ultima_Asistencia`='{fecha_actual}' WHERE ID = {int(self.texto_buscar_por_id.get())} """
                    cursor.execute(sql)
                    conn.commit()

                    ################ actualizar el strin de la asistencia en asistencia ###################
                    conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                    cursor = conn.cursor()

                    sql = f"""SELECT `Ultima_Asistencia` FROM `clientes` WHERE ID = {int(self.texto_buscar_por_id.get())};"""
                    cursor.execute(sql)
                    for index in cursor:
                        string_ultima_asistencia_asistencia_cliente.set(f"Ultima Asistencia ({index[0]})")
            except:
                error = messagebox.showinfo("Error","No se pudo actualizar la asistencia")


        def rotar_asistencia_cliente(): 
            try:
                imagen_persona_asistencia_cliente = CTkImage(Image.open(f"D:/gym_Coliseo/fotos_gym/gym_Clientes/{id_buscado}.jpg"), size = (600,600)) 
                
                self.label_imagen = CTkLabel(self, image = imagen_persona_asistencia_cliente, width = 600, height = 600, text = "")
                self.label_imagen.place(x = 0 , y = 200) 
            except:
                error = messagebox.showinfo("Error", "No se pudo cargar la imagen")            


        def salir_asistencia_cliente():
            self.destroy()

        self.btn_buscar = CTkButton(self,text="Buscar",command=buscar_asistencia_cliente, width = 600, height = 30)
        self.btn_buscar.place(x=350 ,y=68 )
        
        self.btn_rotar = CTkButton(self,text="Rotar",command=rotar_asistencia_cliente, width = 300, height = 30)
        self.btn_rotar.place(x=995 ,y=550 )
        
        self.btn_pago = CTkButton(self,text="Pagar",command=pago_asistencia_cliente, width = 300, height = 30)
        self.btn_pago.place(x=995 ,y=600 )
        
        self.btn_asistio = CTkButton(self,text="Asistio Hoy",command=asistio_asistencia_cliente, width = 300, height = 30)
        self.btn_asistio.place(x=650 ,y=650 )
        
        self.btn_cancelar = CTkButton(self,text="Salir de Asistencia",command=salir_asistencia_cliente, width = 300, height = 30)
        self.btn_cancelar.place(x=995 ,y=650 )


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
                        user = "ysos",
                        password = "123456",
                        database = "ysos"
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

        self.label_nombre = CTkLabel(self,text = "Usuario:", font=("Times New Roman",14))
        self.label_nombre.place(x = 100 , y = 100)
        
        items_usuarios = []

        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
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
                                    user = "ysos",
                                    password = "123456",
                                    database = "ysos"
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
# ********************************** contratar agrego ******************************
# **********************************************************************************
class ContratarAgrego(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Contratar Agrego")    
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
        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 738, y = 70)  

        self.label_nombre = CTkLabel(self,text="Agrego:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 110)

        self.label_apellido1 = CTkLabel(self,text="Entrenador:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 692, y = 150) 

        items_agregos = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()

        sql = """SELECT `agrego` FROM `agrego`"""
        cursor.execute(sql)
        for index in cursor:
            items_agregos.append(index[0])
                        
        global texto_agrego_contratar_agrego
        texto_agrego_contratar_agrego = ttk.Combobox(self)
        texto_agrego_contratar_agrego.place(x = 800, y = 115)  
        texto_agrego_contratar_agrego['values'] = items_agregos 

        items_entrenador = []
        sql = """SELECT * FROM `entrenadores`"""
        cursor.execute(sql)
        for index in cursor:
            items_entrenador.append(index[0])
        global texto_entrenador_contratar_agrego
        texto_entrenador_contratar_agrego = ttk.Combobox(self)
        texto_entrenador_contratar_agrego.place(x = 800, y = 155)
        texto_entrenador_contratar_agrego['values'] = items_entrenador       
        
        global texto_id_contratar_agrego
        texto_id_contratar_agrego = CTkEntry(self)
        texto_id_contratar_agrego.place(x = 800, y = 70)

        def confirmar_contratar_agrego():

            # verificar que el id exista:
            conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
            cursor = conn.cursor()

            sql = """SELECT ID FROM clientes;"""
            cursor.execute(sql)

            existe_id = False

            for index in cursor:
                if int(texto_id_contratar_agrego.get()) == index[0]:
                        existe_id = True
                        break
            
            if existe_id == True:

                # verificar que no se repita el id y el agrego para no contratar por gusto
                conn = mysql.connector.connect(
                host = "localhost",
                user = "ysos",
                password = "123456",
                database = "ysos"
                )
                cursor = conn.cursor()

                sql = """SELECT * FROM cliente_agrego;"""
                cursor.execute(sql)

                repetido_id = False

                for index in cursor:
                    if index[0] == int(texto_id_contratar_agrego.get()) and index[1] == texto_agrego_contratar_agrego.get():
                        repetido_id = True
                        break
                        
                if repetido_id == False:
                    error = messagebox.askyesno("Confirmar","Confirmar Contrato")
                    if error == True:
                        conn = mysql.connector.connect(
                        host = "localhost",
                        user = "ysos",
                        password = "123456",
                        database = "ysos"
                        )
                        cursor = conn.cursor()
                        
                        
                        sql = f""" INSERT INTO `cliente_agrego`(`id`, `agrego`, `entrenador`) VALUES ('{texto_id_contratar_agrego.get()}','{texto_agrego_contratar_agrego.get()}','{texto_entrenador_contratar_agrego.get()}')"""
                        cursor.execute(sql)
                        conn.commit()  

                        error = messagebox.askyesno("Pagar Agrego","Quieres ejecutar un pago automatico ahora?")
                        if error == "yes":                                                

                            ###################### generar el pago por el contrato del agrego ##############  
                            ################## pagar los agregos contratados #######################
                            # *************** voy a trabajarlos por listas *******************
                            lista1 = []                        
                            string_nombre_completo_pago = ""

                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "ysos",
                                password = "123456",
                                database = "ysos"
                                )
                            cursor = conn.cursor()
                            sql = f""" SELECT * FROM `agrego` WHERE agrego = "{texto_agrego_contratar_agrego.get()}"; """
                            cursor.execute(sql)
                            for index in cursor:
                                print(index)
                                lista1.append(index)       
                                


                            # ahora voy a buscar el nombre completo para agregarlo en la bd despues 

                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "ysos",
                                password = "123456",
                                database = "ysos"
                                )
                            cursor = conn.cursor()
                            sql = f"""SELECT `Nombre`, `Apellido 1`, `Apellido 2` FROM `clientes` WHERE ID = {texto_id_contratar_agrego.get()};"""
                            cursor.execute(sql)

                            for index in cursor:
                                string_nombre_completo_pago += index[0] + ' ' +  index[1] + ' ' + index[2]
                            # ******************************************************************************
                            conn = mysql.connector.connect(
                                host = "localhost",
                                user = "ysos",
                                password = "123456",
                                database = "ysos"
                                )
                            cursor = conn.cursor()                                            
                            sql = f""" INSERT INTO `pagos`(`fecha`, `id`, `nombre_completo`, `modalidad`, `Entrenador`, `pagar_activacion`, `importe`, `pago_entrenador`) VALUES ('{fecha_actual}','{texto_id_contratar_agrego.get()}','{string_nombre_completo_pago}','Agrego','{texto_entrenador_contratar_agrego.get()}','NO','{lista1[0][1]}','{lista1[0][2]}') """
                            cursor.execute(sql)
                            conn.commit()                       

                            self.destroy()
                        else:
                            self.destroy()
                else:
                    error = messagebox.showinfo("Error", "Ya esta contratado ese agrego")

            else:
                error = messagebox.showinfo("Error", "ID no existente")


        def cancelar_contratar_agrego():            
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Aceptar",command=confirmar_contratar_agrego, width = 150, height = 40)
        self.btn_aceptar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_contratar_agrego, width = 150, height = 40)
        self.btn_cancelar.place(x=820 ,y=500 )


# **********************************************************************************
# ********************************** modificar agrego ******************************
# **********************************************************************************

class ModificarAgrego(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Modificar Agrego")    
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
        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 738, y = 70)  

        self.label_nombre = CTkLabel(self,text="Agrego:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 110)

        self.label_apellido1 = CTkLabel(self,text="Entrenador:", font=("Times New Roman",16))
        self.label_apellido1.place(x = 692, y = 150) 

        items_agregos = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()

        sql = """SELECT `agrego` FROM `agrego`"""
        cursor.execute(sql)
        for index in cursor:
            items_agregos.append(index[0])
                        
        global texto_agrego_modificar_agrego
        texto_agrego_modificar_agrego = ttk.Combobox(self)
        texto_agrego_modificar_agrego.place(x = 800, y = 115)  
        texto_agrego_modificar_agrego['values'] = items_agregos 

        items_entrenador = []
        sql = """SELECT * FROM `entrenadores`"""
        cursor.execute(sql)
        for index in cursor:
            items_entrenador.append(index[0])
        global texto_entrenador_modificar_agrego
        texto_entrenador_modificar_agrego = ttk.Combobox(self)
        texto_entrenador_modificar_agrego.place(x = 800, y = 155)
        texto_entrenador_modificar_agrego['values'] = items_entrenador       
        
        global texto_id_modificar_agrego
        texto_id_modificar_agrego = CTkEntry(self)
        texto_id_modificar_agrego.place(x = 800, y = 70)

        def confirmar_modificar_agrego():
            # verificar que el id tenga contratado agrego
            conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
            cursor = conn.cursor()
            sql = """SELECT * FROM cliente_agrego;"""
            cursor.execute(sql)

            existe_id = False
            agrego_contratado = False

            for index in cursor:
                if int(texto_id_modificar_agrego.get()) == index[0]:
                        existe_id = True
                        break
                
            if existe_id == True:
                # verificar que tiene ese agrego especifico contratado
                for index in cursor:
                    if texto_agrego_modificar_agrego.get() == index[1]:
                        agrego_contratado = True
                        break
                
                if agrego_contratado == True:
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "ysos",
                        password = "123456",
                        database = "ysos"
                        )
                    cursor = conn.cursor()
                    sql = f""" UPDATE `cliente_agrego` SET `entrenador`='{texto_entrenador_modificar_agrego.get()}' WHERE id = {int(texto_id_modificar_agrego.get())} """
                    cursor.execute(sql)
                    conn.commit()
                    self.destroy()

                else:
                    error = messagebox.showinfo("Error", "Este Id no tiene ese agrego contratado")

            else:
                error = messagebox.showinfo("Error", "Este Id no tiene agregos contratados")


        def cancelar_modificar_agrego():            
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Modificar",command=confirmar_modificar_agrego, width = 150, height = 40)
        self.btn_aceptar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_modificar_agrego, width = 150, height = 40)
        self.btn_cancelar.place(x=820 ,y=500 )

# **********************************************************************************
# ********************************** eliminar agrego ******************************
# **********************************************************************************
class DespedirAgrego(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Despedir Agrego")    
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
        self.label_id = CTkLabel(self,text="ID:", font=("Times New Roman",16))
        self.label_id.place(x = 738, y = 70)  

        self.label_nombre = CTkLabel(self,text="Agrego:", font=("Times New Roman",16))
        self.label_nombre.place(x = 704, y = 110)

        items_agregos = []
        conn = mysql.connector.connect(
            host = "localhost",
            user = "ysos",
            password = "123456",
            database = "ysos"
            )
        cursor = conn.cursor()

        sql = """SELECT `agrego` FROM `agrego`"""
        cursor.execute(sql)
        for index in cursor:
            items_agregos.append(index[0])
                        
        global texto_agrego_despedir_agrego
        texto_agrego_despedir_agrego = ttk.Combobox(self)
        texto_agrego_despedir_agrego.place(x = 800, y = 115)  
        texto_agrego_despedir_agrego['values'] = items_agregos 

        global texto_id_despedir_agrego
        texto_id_despedir_agrego = CTkEntry(self)
        texto_id_despedir_agrego.place(x = 800, y = 70)

        def confirmar_despedir_agrego():
            # verificar que tenga contratado el agrego
            conn = mysql.connector.connect(
                host = "localhost",
                user = "ysos",
                password = "123456",
                database = "ysos"
                )
            cursor = conn.cursor()

            sql = """SELECT * FROM `cliente_agrego`"""
            cursor.execute(sql)

            agrego_contratado = False

            for index in cursor:
                if index[0] == int(texto_id_despedir_agrego.get()) and index[1] == texto_agrego_despedir_agrego.get():
                    agrego_contratado = True
                    break

            if agrego_contratado:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "ysos",
                    password = "123456",
                    database = "ysos"
                    )
                cursor = conn.cursor()

                sql = f""" DELETE FROM `cliente_agrego` WHERE id = {int(texto_id_despedir_agrego.get())} AND agrego = "{texto_agrego_despedir_agrego.get()}" """
                cursor.execute(sql)
                conn.commit()
                self.destroy()

            else:
                error = messagebox.showinfo("Error", "Ese Id no tiene contratado ese agrego")


        def cancelar_despedir_agrego():
            self.destroy()

        self.btn_aceptar = CTkButton(self,text="Despedir",command=confirmar_despedir_agrego, width = 150, height = 40)
        self.btn_aceptar.place(x=650 ,y=500 )
        
        self.btn_cancelar = CTkButton(self,text="Cancelar",command=cancelar_despedir_agrego, width = 150, height = 40)
        self.btn_cancelar.place(x=820 ,y=500 )


autenticacion = Autenticacion()
autenticacion.mainloop()
