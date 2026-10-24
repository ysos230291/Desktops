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
            l = Lobby()

        self.btn_iniciar = CTkButton(self,text="Iniciar",command=codigo_btn_iniciar, width = 200)
        self.btn_iniciar.place(x = 100 , y = 160)




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

        def agregar_usuario():
            usuario_agregar = UsuarioAgregar()
            
        def eliminar_usuario():                        
            eliminar_usuario = EliminarUsuario()        

        usuario_menu = Menu(self.menu, tearoff = 0)
        usuario_menu.add_command(label="Agregar", command=agregar_usuario)
        usuario_menu.add_command(label="Eliminar", command=eliminar_usuario)


        self.menu.add_cascade (label="Economia", menu = economia_menu)                 
        self.menu.add_cascade(label="Usuarios", menu = usuario_menu)        
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











autenticacion = Autenticacion()
autenticacion.mainloop()