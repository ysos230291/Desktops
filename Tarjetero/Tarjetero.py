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
    sql = """CREATE DATABASE tarjetero CHARACTER SET = utf8mb4 COLLATE utf8mb4_spanish_ci;"""
    cursor.execute(sql)
    conn.commit()    
except:
    pass

############################ creando tabla tarjeta ################################

try:
    sql = """CREATE TABLE `tarjetero`.`tarjeta` (`numero` VARCHAR(100) NOT NULL , `dueño` VARCHAR(100) NOT NULL , `banco` VARCHAR(50) NOT NULL , `limite_transferencia` INT NOT NULL , `limite_extraccion` INT NOT NULL , `gastado_transferencia` INT NOT NULL , `gastado_extraccion` INT NOT NULL , `pendiente_transferencia` INT NOT NULL , `pendiente_extraccion` INT NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

########################### creando tabla operaciones ############################
try:
    sql = """CREATE TABLE `tarjetero`.`operaciones` (`fecha` DATE NOT NULL , `numero` VARCHAR(100) NOT NULL , `dueño` VARCHAR(100) NOT NULL , `banco` VARCHAR(50) NOT NULL , `transferencia` INT NOT NULL , `extraccion` INT NOT NULL , `responsable` VARCHAR(100) NOT NULL, `concepto` VARCHAR(150) NOT NULL ) ENGINE = InnoDB;"""
    cursor.execute(sql)
    conn.commit()
except:
    pass

########################### reseteando los gastos de las tarjetas el dia 1ro de cada mes #####
reseteo = False
if datetime.now().date().day == 1:
    reseteo = True
else: 
    pass

if reseteo:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "", 
        database = "tarjetero"   
        )
    cursor = conn.cursor()
    sql = """ UPDATE `tarjeta` SET `gastado_transferencia`= 0,`gastado_extraccion`= 0"""
    cursor.execute(sql)
    conn.commit()

################################ definiciones ###################################
def listado_tarjeta():
    listado_tarjetas = ListadoTarjetas()

def deglose_tarjeta():
    balance_tarjetas = BalanceTarjetas()

def incertar_tarjeta():
    insertar_tarjetas = InsertarTarjetas()

def buscar_tarjeta():
    buscar_tarjetas = BuscarTarjetas()

def transferencias_operaciones():
    transferencias = Transferencias()

def extracciones_operaciones():
    extraciones = Extracciones()



#########################################################################################
######################################### lobby #########################################
#########################################################################################

class Lobby(CTk):
    def __init__(self):
        super().__init__()
        self.title("Tarjetero")
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
        
        self.menu = Menu(self)
        self.config(menu=self.menu, width = 200, height = 100)

        self.balance_menu = Menu(self.menu, tearoff = 0)
        self.balance_menu.add_command(label="Listado", command = listado_tarjeta)
        self.balance_menu.add_command(label="Deglose", command = deglose_tarjeta)        

        self.tarjetas_menu = Menu(self.menu, tearoff = 0)
        self.tarjetas_menu.add_command(label="Insertar ", command = incertar_tarjeta)
        self.tarjetas_menu.add_command(label="Buscar ", command = buscar_tarjeta)        

        self.operaciones_menu = Menu(self.menu, tearoff = 0)   
        self.operaciones_menu.add_command(label="Transferencias", command = transferencias_operaciones)
        self.operaciones_menu.add_command(label="Extracciones", command = extracciones_operaciones)
        
        self.menu.add_cascade (label="Balance", menu = self.balance_menu)
        self.menu.add_cascade (label="Tarjetas", menu = self.tarjetas_menu)
        self.menu.add_cascade (label="Operaciones", menu = self.operaciones_menu)
        
        try:
            self.image = CTkImage(Image.open("D:/Mis Softwares/Python/Tarjetero/lobby.jpg"), size = (1300,700))

            self.label_image = CTkLabel(self, image = self.image, text = "")
            self.label_image.place(x = 0, y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen") 


###############################################################################################
####################################### Listado tarjetas ######################################
###############################################################################################
class ListadoTarjetas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Listado Tarjetas")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600")
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))

        try:
            self.image = CTkImage(Image.open("D:/Mis Softwares/Python/Tarjetero/listado.jpg"), size = (1000,600))

            self.label_image = CTkLabel(self, image = self.image, text = "")
            self.label_image.place(x = 0, y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")

        ################################# labels #######################################
        self.duenio = CTkLabel(self, text = "Buscar por:", font=("Arial",18))
        self.duenio.place(x = 50, y = 20)

        self.filtros = CTkLabel(self, text = "Filtros:", font=("Arial",18))
        self.filtros.place(x = 500, y = 20)

        ################################# entradas #######################################
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "", 
            database = "tarjetero"   
            )
        cursor = conn.cursor()

        sql = f"""SELECT `dueño` FROM `tarjeta` """
        cursor.execute(sql)
        lista_duenios = []
        elim = []
        for index in cursor:
            lista_duenios.append(index[0]) 

        for i in range(len(lista_duenios)):
            for j in range(i+1,len(lista_duenios)):
                if lista_duenios[i] == lista_duenios[j]:
                    elim.append(j)

        for index in elim:
            lista_duenios.pop(index)
                    

        self.combo_duenio = CTkComboBox(self, values=lista_duenios)
        self.combo_duenio.place(x = 200, y = 60) 

        
        sql = f"""SELECT `banco` FROM `tarjeta` """
        cursor.execute(sql)
        lista_bancos = []
        elim = []
        for index in cursor:
            lista_bancos.append(index[0]) 

        for i in range(len(lista_bancos)):
            for j in range(i+1,len(lista_bancos)):
                if lista_bancos[i] == lista_bancos[j]:
                    elim.append(j)

        for index in elim:
            lista_bancos.pop(index)

        self.combo_bancos  = CTkComboBox(self, values=lista_bancos)
        self.combo_bancos.place(x = 200, y = 90)  

        ################################# tabla ##################################
        self.indice = CTkTabview(self, width=900, height = 300)
        self.indice.place(x = 50, y = 150)
        self.indice.add("Tabla")

        self.tabla = ttk.Treeview(self.indice.tab("Tabla"), columns = ("duenio","banco","lt", "le", "gt", "ge", "pt", "pe"), height=13)
        self.tabla.column("#0", width = 150)
        self.tabla.column("duenio", width = 200)
        self.tabla.column("banco", width = 100)
        self.tabla.column("lt", width = 100)
        self.tabla.column("le", width = 100)
        self.tabla.column("gt", width = 100)
        self.tabla.column("ge", width = 100)
        self.tabla.column("pt", width = 100)
        self.tabla.column("pe", width = 100)

        self.tabla.heading("#0", text = "Numero")
        self.tabla.heading("duenio", text = "Dueño")
        self.tabla.heading("banco", text = "Banco")
        self.tabla.heading("lt", text = "Limite T")
        self.tabla.heading("le", text = "Limite E")
        self.tabla.heading("gt", text = "Gastado T")
        self.tabla.heading("ge", text = "Gastado E")
        self.tabla.heading("pt", text = "Pendiente T")
        self.tabla.heading("pe", text = "Pendiente E")

        self.tabla.place(x=0,y=0)   

        self.scrollbar = CTkScrollbar(self.indice.tab("Tabla"), command = self.tabla.yview, width = 18)
        self.scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = self.scrollbar.set)


        ################################ botones ##########################################
        opcion_busqueda = IntVar()
        dispt = IntVar()
        dispe = IntVar() 
        
        self.radio_duenio = CTkRadioButton(self, variable = opcion_busqueda, text = "Por dueño", font=("Arial",24), value = 2)
        self.radio_duenio.place(x=50, y=60)        

        self.radio_banco = CTkRadioButton(self, variable = opcion_busqueda, text = "Por banco", font=("Arial",24), value = 1)
        self.radio_banco.place(x=50, y=90)

        self.radio_todas = CTkRadioButton(self, variable = opcion_busqueda, text = "Todas", font=("Arial",24), value = 3)
        self.radio_todas.place(x=50, y=120)

        self.check_dt = CTkCheckBox(self, variable = dispt, text = "Disponibilidad en Transferencia", font=("Arial",18))
        self.check_dt.place(x=500, y=60)

        self.check_de = CTkCheckBox(self, variable = dispe, text = "Disponibilidad en Extracción", font=("Arial",18))
        self.check_de.place(x=500, y=90)

        def buscar_listado():
            self.tabla.delete(*self.tabla.get_children())

            if opcion_busqueda.get() == 1:
                if dispt.get() == 1:
                    if dispe.get() == 1:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()
                        sql = f"""SELECT * FROM `tarjeta` WHERE `banco` = "{self.combo_bancos.get()}" AND limite_transferencia > gastado_transferencia AND limite_extraccion > gastado_extraccion"""
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))

                    elif dispe.get() == 0:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()
                        sql = f"""SELECT * FROM `tarjeta` WHERE `banco` = "{self.combo_bancos.get()}" AND limite_transferencia > gastado_transferencia """
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))


                elif dispt.get() == 0:
                    if dispe.get() == 1:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()
                        sql = f"""SELECT * FROM `tarjeta` WHERE `banco` = "{self.combo_bancos.get()}" AND limite_extraccion > gastado_extraccion"""
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))

                    elif dispe.get() == 0:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()
                        sql = f"""SELECT * FROM `tarjeta` WHERE `banco` = "{self.combo_bancos.get()}" """
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))
            
            elif opcion_busqueda.get() == 2:
                if dispt.get() == 1:
                    if dispe.get() == 1:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()
                        sql = f"""SELECT * FROM `tarjeta` WHERE `dueño` = "{self.combo_duenio.get()}" AND limite_transferencia > gastado_transferencia AND limite_extraccion > gastado_extraccion"""
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))

                    elif dispe.get() == 0:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()
                        sql = f"""SELECT * FROM `tarjeta` WHERE `dueño` = "{self.combo_duenio.get()}" AND limite_transferencia > gastado_transferencia """
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))


                elif dispt.get() == 0:
                    if dispe.get() == 1:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()
                        sql = f"""SELECT * FROM `tarjeta` WHERE `dueño` = "{self.combo_duenio.get()}" AND  limite_extraccion > gastado_extraccion"""
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))

                    elif dispe.get() == 0:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()
                        sql = f"""SELECT * FROM `tarjeta` WHERE `dueño` = "{self.combo_duenio.get()}" """
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))
    

            elif opcion_busqueda.get() == 3:  
                if dispt.get() == 1:          
                    if dispe.get() == 1: 
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()    
                        sql = """SELECT * FROM `tarjeta` WHERE limite_transferencia > gastado_transferencia AND limite_extraccion > gastado_extraccion ORDER BY dueño;"""
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))

                    elif dispe.get() == 0:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()   
                        sql = """SELECT * FROM `tarjeta` WHERE limite_transferencia > gastado_transferencia ORDER BY dueño"""
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))


                elif dispt.get() == 0:
                    if dispe.get() == 1:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()
                        sql = """SELECT * FROM `tarjeta` WHERE limite_extraccion > gastado_extraccion ORDER BY dueño;"""
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))

                    elif dispe.get() == 0:
                        conn = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "", 
                            database = "tarjetero"   
                            )
                        cursor = conn.cursor()
                        sql = """SELECT * FROM `tarjeta` ORDER BY dueño"""
                        cursor.execute(sql)
                        for index in cursor:
                            self.tabla.insert("", END, text = index[0] , values = (f"{index[1]}", f"{index[2]}", f"{index[3]}", f"{index[4]}", f"{index[5]}", f"{index[6]}", f"{index[7]}", f"{index[8]}"))
            
            else:
                error = messagebox.showinfo("Error", "Marque opciones de busqueda")
            
        self.btn_buscar = CTkButton(self, text = "Buscar", width=500, height=30, command=buscar_listado)
        self.btn_buscar.place(x=250, y=500)
        


###############################################################################################
######################################## deglose tarjetas #####################################
###############################################################################################

class BalanceTarjetas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Deglose Tarjetas")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600")
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))

        try:
            self.image = CTkImage(Image.open("D:/Mis Softwares/Python/Tarjetero/balance.jpg"), size = (1000,600))

            self.label_image = CTkLabel(self, image = self.image, text = "")
            self.label_image.place(x = 0, y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")

        ################################ label ##################################

        self.numero = CTkLabel(self, text="Tarjeta: ", font=("Arial",18))
        self.numero.place(x=50,y = 50)

        self.mes = CTkLabel(self, text="Mes: ", font=("Arial",18))
        self.mes.place(x=300,y = 50)

        self.duenio = CTkLabel(self,text="Dueño:", font=("Arial",18))
        self.duenio.place(x=600,y=50)

        ################################ entradas ###############################
        duenio = StringVar()

        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "", 
            database = "tarjetero"   
            )
        cursor = conn.cursor()

        lista_tarjetas = []
        sql = """SELECT `numero` FROM `tarjeta`;"""
        cursor.execute(sql)

        for index in cursor:
            lista_tarjetas.append(index[0])

        self.combo_numero = ttk.Combobox(self, values=lista_tarjetas, font=("Arial",18),width=13)
        self.combo_numero.place(x=150,y = 65)

        def buscar_duenio(event):
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "", 
                database = "tarjetero"   
                )
            cursor = conn.cursor()
            
            sql = f"""SELECT `dueño` FROM `tarjeta` WHERE `numero` = {self.combo_numero.get()} """
            cursor.execute(sql)
            for index in cursor:
                duenio.set(index[0])

            

        self.combo_numero.bind("<<ComboboxSelected>>",buscar_duenio)

        self.entry_mes = CTkEntry(self)
        self.entry_mes.place(x = 350, y = 50)

        def calendario_deglose():
            root = Toplevel()
            root.title("Calendario")
            root.geometry(f"+{posx + 1000}+{posy}")
                        
            cal2 = Calendar(root, select_mode = "day", date_pattern = "yyyy/mm/dd")
            cal2.pack()

            def escoger_fecha():
                global fecha
                fecha = cal2.selection_get() 
                mes = fecha.month
                name_mes = ""
                if mes == 1:
                    name_mes = "Enero"
                if mes == 2:
                    name_mes = "Febrero"
                if mes == 3:
                    name_mes = "Marzo"
                if mes == 4:
                    name_mes = "Abril"
                if mes == 5:
                    name_mes = "Mayo"
                if mes == 6:
                    name_mes = "Junio"
                if mes == 7:
                    name_mes = "Julio"
                if mes == 8:
                    name_mes = "Agosto"
                if mes == 9:
                    name_mes = "Septiembre"
                if mes == 10:
                    name_mes = "Octubre"
                if mes == 11:
                    name_mes = "Noviembre"
                if mes == 12:
                    name_mes = "Diciembre"
                anio = fecha.year 

                texto_fecha = name_mes + "-" + str(anio)   ######### para que salga esto en el entry                  

                self.entry_mes.delete(0,END)
                self.entry_mes.insert(0, texto_fecha)
                root.destroy()

            btn = Button(root, text = "Usar Fecha", command = escoger_fecha)
            btn.pack()

        self.btn_calendario = CTkButton(self, text="...", command=calendario_deglose, width=30)
        self.btn_calendario.place(x = 500, y = 50)

        self.entry_duenio = CTkEntry(self, textvariable=duenio, font=("Arial",18))
        self.entry_duenio.place(x=670,y=50)

        ################################# tabla ##################################
        self.indice = CTkTabview(self, width=900, height = 300)
        self.indice.place(x = 50, y = 150)
        self.indice.add("Deglose")

        self.tabla = ttk.Treeview(self.indice.tab("Deglose"), columns = ("numero","monto","responsable", "concepto"), height=13)
        self.tabla.column("#0", width = 150)
        self.tabla.column("numero", width = 200)
        self.tabla.column("monto", width = 200)
        self.tabla.column("responsable", width = 200)
        self.tabla.column("concepto", width = 300)
        

        self.tabla.heading("#0", text = "Fecha")
        self.tabla.heading("numero", text = "Numero")
        self.tabla.heading("monto", text = "Monto")
        self.tabla.heading("responsable", text = "Responsable")
        self.tabla.heading("concepto", text = "Concepto")
        

        self.tabla.place(x=0,y=0)   

        self.scrollbar = CTkScrollbar(self.indice.tab("Deglose"), command = self.tabla.yview, width = 18)
        self.scrollbar.place(in_ = self.tabla, relheigh = 1, relx = 1)

        self.tabla.config(yscrollcommand = self.scrollbar.set)

        ######################################## botones #############################################
        def generar_deglose():
            self.tabla.delete(*self.tabla.get_children())
            ############ buscar el periodo a analizar ###############
            fecha_inicial = date(fecha.year,fecha.month,1)
            if fecha.month == 12:
                fecha_final = date(fecha.year + 1,1,1)
            else:
                fecha_final = date(fecha.year,fecha.month + 1,1)

            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "", 
                database = "tarjetero"   
                )
            cursor = conn.cursor()

            sql = f"""SELECT `fecha`, `numero`, `transferencia`, `extraccion`, `responsable`, `concepto` FROM `operaciones` WHERE `numero` = "{self.combo_numero.get()}" AND fecha < "{str(fecha_final)}" AND fecha > "{str(fecha_inicial)}" ORDER BY fecha """
            cursor.execute(sql)
            for index in cursor:
                if index[2] == 0:
                    monto = index[3]
                else:
                    monto = index[2]
                
                self.tabla.insert("", END, text = index[0], values = (f"{index[1]}",monto,f"{index[4]}",f"{index[5]}"))
            

        self.btn_deglose = CTkButton(self,text="Generar Deglose", width=600,height=70,command=generar_deglose)
        self.btn_deglose.place(x=200,y=500)

###############################################################################################
######################################## insertar_tarjetas ####################################
###############################################################################################

class InsertarTarjetas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Insertar Tarjetas")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600")
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))

        ############################## labels ###############################

        self.numero = CTkLabel(self, text = "Numero:", font=("Arial",18))
        self.numero.place(x = 620, y = 30)

        self.duenio = CTkLabel(self, text = "Dueño:", font=("Arial",18))
        self.duenio.place(x = 620, y = 90)

        self.banco = CTkLabel(self, text = "Banco:", font=("Arial",18))
        self.banco.place(x = 620, y = 150)

        self.lt = CTkLabel(self, text = "Limite T:", font=("Arial",18))
        self.lt.place(x = 620, y = 210)

        self.le = CTkLabel(self, text = "Limite E:", font=("Arial",18))
        self.le.place(x = 620, y = 270)

        self.gt = CTkLabel(self, text = "Gastado T:", font=("Arial",18))
        self.gt.place(x = 620, y = 330)

        self.ge = CTkLabel(self, text = "Gastado E:", font=("Arial",18))
        self.ge.place(x = 620, y = 390)

        ############################## Entrys ################################

        self.text_numero = CTkEntry(self, width = 200) 
        self.text_numero.place(x = 750, y = 30)

        self.text_duenio = CTkEntry(self, width = 200) 
        self.text_duenio.place(x = 750, y = 90)

        self.text_banco = CTkEntry(self, width = 200) 
        self.text_banco.place(x = 750, y = 150)

        self.text_lt = CTkEntry(self, width = 200) 
        self.text_lt.place(x = 750, y = 210)

        self.text_le = CTkEntry(self, width = 200) 
        self.text_le.place(x = 750, y = 270)

        self.text_gt = CTkEntry(self, width = 200) 
        self.text_gt.place(x = 750, y = 330)

        self.text_ge = CTkEntry(self, width = 200) 
        self.text_ge.place(x = 750, y = 390)

        ####################### botones #######################
        def insertar_tarjeta():

            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "", 
                database = "tarjetero"   
                )
            cursor = conn.cursor()


            sql = f"""INSERT INTO `tarjeta`(`numero`, `dueño`, `banco`, `limite_transferencia`, `limite_extraccion`, `gastado_transferencia`, `gastado_extraccion`, `pendiente_transferencia`, `pendiente_extraccion`) VALUES ('{self.text_numero.get()}','{self.text_duenio.get()}','{self.text_banco.get()}','{self.text_lt.get()}','{self.text_le.get()}','{self.text_gt.get()}','{self.text_ge.get()}','{int(self.text_lt.get()) - int(self.text_gt.get())}','{int(self.text_le.get()) - int(self.text_ge.get())}')"""
            cursor.execute(sql)
            conn.commit()

            self.text_numero.delete(0,END) 
            self.text_duenio.delete(0,END) 
            self.text_banco.delete(0,END) 
            self.text_lt.delete(0,END) 
            self.text_le.delete(0,END) 
            self.text_gt.delete(0,END) 
            self.text_ge.delete(0,END) 

        def cancelar_insercion():
            self.destroy()

        self.btn_insertar = CTkButton(self, text = "Insertar", width = 150, height = 30, command= insertar_tarjeta)
        self.btn_insertar.place(x=650, y=500)

        self.btn_cancelar = CTkButton(self, text = "Cancelar", width = 150, height = 30, command= cancelar_insercion)
        self.btn_cancelar.place(x=830, y=500)

        try:
            self.image = CTkImage(Image.open("D:/Mis Softwares/Python/Tarjetero/insertar.jpg"), size = (600,600))

            self.label_image = CTkLabel(self, image = self.image, text = "")
            self.label_image.place(x = 0, y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")

################################################################################################
######################################## buscar tarjeta #######################################
################################################################################################

class BuscarTarjetas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Buscar Tarjeta")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 600
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry(f"+{posx}+{posy}")
        self.geometry("600x600")
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))

        try:
            self.image = CTkImage(Image.open("D:/Mis Softwares/Python/Tarjetero/buscar.jpg"), size = (600,600))

            self.label_image = CTkLabel(self, image = self.image, text = "")
            self.label_image.place(x = 0, y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")

        self.buscar_numero = CTkLabel(self, text = "Buscar por Numero:", font=("Arial",18))
        self.buscar_numero.place(x = 70, y = 50)

        self.buscar_nombre = CTkLabel(self, text = "Buscar por Nombre:", font=("Arial",18))
        self.buscar_nombre.place(x = 380, y = 50)

        self.radio_btn = IntVar()

        self. radio_btn_numero = Radiobutton(self, variable = self.radio_btn, value = 1)
        self. radio_btn_numero.place(x = 40 , y = 65)

        self.radio_btn_duenio = Radiobutton(self, variable = self.radio_btn, value = 2)
        self.radio_btn_duenio.place(x = 700 , y = 65)

        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "", 
            database = "tarjetero"   
            )
        cursor = conn.cursor()
        
        lista_tarjetas = []
        sql = """SELECT `numero` FROM `tarjeta`;"""
        cursor.execute(sql)

        for index in cursor:
            lista_tarjetas.append(index[0])
                        
        self.text_numero = AutocompleteEntry(self, width = 50, completevalues = lista_tarjetas) 
        self.text_numero.place(x = 40, y = 100)

        lista_duenios = []
        sql = """SELECT `dueño` FROM `tarjeta`;"""
        cursor.execute(sql)

        for index in cursor:
            lista_duenios.append(index[0])

        self.text_duenio = AutocompleteEntry(self, width = 50, completevalues = lista_duenios) 
        self.text_duenio.place(x = 430, y = 100)

        
        tabla_tarjetas = ttk.Treeview(self, columns = ("Numero","Dueño","Banco"))
        tabla_tarjetas.column("#0", width = 40)
        tabla_tarjetas.column("Numero", width = 200)
        tabla_tarjetas.column("Dueño", width = 300)
        tabla_tarjetas.column("Banco", width = 100)
        
        tabla_tarjetas.place(x = 50, y = 230)
        tabla_tarjetas.config(height = 15)

        tabla_tarjetas.heading("#0", text = "No.")
        tabla_tarjetas.heading("Numero", text = "Numero")
        tabla_tarjetas.heading("Dueño", text = "Dueño")
        tabla_tarjetas.heading("Banco", text = "Banco")

        scrollbar_tarjetas = CTkScrollbar(self, command = tabla_tarjetas.yview, width = 18)
        scrollbar_tarjetas.place(in_ = tabla_tarjetas, relheigh = 1, relx = 1)

        tabla_tarjetas.config(yscrollcommand = scrollbar_tarjetas.set)
        

        ############# nuevo para mi ###############
        ########### esto es para coger el numero de la tarjeta que seleccione en la tabla ############
                
        def seleccionar_numero_tarjeta(event):
            for item in tabla_tarjetas.selection():
                global num_tar
                num_tar = copy.deepcopy(str(tabla_tarjetas.item(item,"values")[0]))
                    
                
        tabla_tarjetas.bind("<<TreeviewSelect>>", seleccionar_numero_tarjeta)
        

        def buscar():
            tabla_tarjetas.delete(*tabla_tarjetas.get_children())
            ################## si busco por numero #######################
            if self.radio_btn.get() == 1:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "", 
                    database = "tarjetero"   
                    )
                cursor = conn.cursor()
                sql = f"""SELECT `numero`, `dueño`, `banco`FROM `tarjeta` WHERE numero = {self.text_numero.get()};"""
                cursor.execute(sql)
                cont = 1
                for index in cursor:
                    tabla_tarjetas.insert("",END,text=cont,values=(index[0],index[1],index[2]))
                    cont += 1 
            
            ################## si busco por dueño ########################

            elif self.radio_btn.get() == 2:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "", 
                    database = "tarjetero"   
                    )
                cursor = conn.cursor()
                sql = f"""SELECT `numero`, `dueño`, `banco`FROM `tarjeta` WHERE `dueño` = "{self.text_duenio.get()}";"""
                cursor.execute(sql)
                cont = 1
                for index in cursor:
                    tabla_tarjetas.insert("",END,text=cont,values=(index[0],index[1],index[2]))
                    cont += 1

            ######################## si no se ha marcado ninguno ################################# 
            else:
                error = messagebox.showinfo("Error","Debe escoger alguna opcion para buscar")

        

        self.btn_buscar = CTkButton(self, text = "Buscar", width = 500, height = 30, command= buscar)
        self.btn_buscar.place(x=50, y=120)
        

        def modificar_tarjetas():
            global text_numero,text_duenio,text_banco,text_lt,text_le,text_gt,text_ge,text_pt,text_pe
            text_numero = StringVar()
            text_duenio = StringVar()
            text_banco = StringVar()
            text_lt = StringVar()
            text_le = StringVar()
            text_gt = StringVar()
            text_ge = StringVar()
            text_pt = StringVar()
            text_pe = StringVar()

            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "", 
                database = "tarjetero"   
                )
            cursor = conn.cursor()
            sql = f"""SELECT * FROM `tarjeta` WHERE `numero` = "{num_tar}";"""
            cursor.execute(sql)

            for index in cursor:
                text_numero.set(index[0])
                text_duenio.set(index[1])
                text_banco.set(index[2])
                text_lt.set(index[3])
                text_le.set(index[4])
                text_gt.set(index[5])
                text_ge.set(index[6])
                text_pt.set(index[7])
                text_pe.set(index[8])

            modificar_tarjetas = ModificarTarjetas()

        self.btn_modificar = CTkButton(self, text = "Modificar", width = 200, height = 30, command= modificar_tarjetas)
        self.btn_modificar.place(x=50, y=500)

        def eliminar_tarjetas():
            eliminar_tarjetas = EliminarTarjetas()

        self.btn_eliminar = CTkButton(self, text = "Eliminar", width = 200, height = 30, command= eliminar_tarjetas)
        self.btn_eliminar.place(x=350, y=500)



        
################################################################################################
######################################## modificar_tarjetas ####################################
################################################################################################

class ModificarTarjetas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Modificar Tarjetas")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600")
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))

        ################# foto ##############################

        try:
            self.image = CTkImage(Image.open("D:/Mis Softwares/Python/Tarjetero/modificar.jpg"), size = (600,600))

            self.label_image = CTkLabel(self, image = self.image, text = "")
            self.label_image.place(x = 0, y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")

        ###################### labels ##########################

        self.numero = CTkLabel(self, text = "Numero:", font=("Arial",18))
        self.numero.place(x = 620, y = 30)

        self.duenio = CTkLabel(self, text = "Dueño:", font=("Arial",18))
        self.duenio.place(x = 620, y = 90)

        self.banco = CTkLabel(self, text = "Banco:", font=("Arial",18))
        self.banco.place(x = 620, y = 150)

        self.lt = CTkLabel(self, text = "Limite T:", font=("Arial",18))
        self.lt.place(x = 620, y = 210)

        self.le = CTkLabel(self, text = "Limite E:", font=("Arial",18))
        self.le.place(x = 620, y = 270)

        self.gt = CTkLabel(self, text = "Gastado T:", font=("Arial",18))
        self.gt.place(x = 620, y = 330)

        self.ge = CTkLabel(self, text = "Gastado E:", font=("Arial",18))
        self.ge.place(x = 620, y = 390)
        
        ############################## Entrys ################################
                
        self.text_numero = CTkEntry(self, width = 200, textvariable=text_numero) 
        self.text_numero.place(x = 750, y = 30)        
        
        self.text_duenio = CTkEntry(self, width = 200, textvariable=text_duenio) 
        self.text_duenio.place(x = 750, y = 90)        
        
        self.text_banco = CTkEntry(self, width = 200, textvariable=text_banco) 
        self.text_banco.place(x = 750, y = 150)
        
        self.text_lt = CTkEntry(self, width = 200, textvariable=text_lt) 
        self.text_lt.place(x = 750, y = 210)
        
        self.text_le = CTkEntry(self, width = 200, textvariable=text_le) 
        self.text_le.place(x = 750, y = 270)
        
        self.text_gt = CTkEntry(self, width = 200, textvariable=text_gt) 
        self.text_gt.place(x = 750, y = 330)
        
        self.text_ge = CTkEntry(self, width = 200, textvariable=text_ge) 
        self.text_ge.place(x = 750, y = 390)

        def modificar_tarjeta():
            error = messagebox.askyesno("Confirmar", "Confirma la modificacion ?")
            if error == True:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "", 
                    database = "tarjetero"   
                    )
                cursor = conn.cursor()
                sql = f"""UPDATE `tarjeta` SET `numero`='{self.text_numero.get()}',`dueño`='{self.text_duenio.get()}',`banco`='{self.text_banco.get()}',`limite_transferencia`= {int(self.text_lt.get())},`limite_extraccion`={int(self.text_le.get())},`gastado_transferencia`={int(self.text_gt.get())},`gastado_extraccion`={int(self.text_ge.get())},`pendiente_transferencia`={int(self.text_lt.get()) - int(self.text_gt.get())},`pendiente_extraccion`={int(self.text_le.get()) - int(self.text_ge.get())} WHERE `numero` = "{num_tar}" """
                cursor.execute(sql)
                conn.commit()

        def cancelar_modificacion():
            self.destroy()

        self.btn_modificar = CTkButton(self, text = "Modificar", width = 150, height = 30, command = modificar_tarjeta)
        self.btn_modificar.place(x=650, y=500)

        self.btn_cancelar = CTkButton(self, text = "Cancelar", width = 150, height = 30, command= cancelar_modificacion)
        self.btn_cancelar.place(x=830, y=500)

###############################################################################################
######################################## eliminar_tarjetas ####################################
###############################################################################################

class EliminarTarjetas(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Eliminar Tarjetas")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600")
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))

        try:
            self.image = CTkImage(Image.open("D:/Mis Softwares/Python/Tarjetero/eliminar.jpg"), size = (600,600))

            self.label_image = CTkLabel(self, image = self.image, text = "")
            self.label_image.place(x = 0, y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")

        ###################### labels ##########################

        self.numero = CTkLabel(self, text = "Numero:", font=("Arial",18))
        self.numero.place(x = 620, y = 30)

        self.duenio = CTkLabel(self, text = "Dueño:", font=("Arial",18))
        self.duenio.place(x = 620, y = 90)

        self.banco = CTkLabel(self, text = "Banco:", font=("Arial",18))
        self.banco.place(x = 620, y = 150)

        self.lt = CTkLabel(self, text = "Limite T:", font=("Arial",18))
        self.lt.place(x = 620, y = 210)

        self.le = CTkLabel(self, text = "Limite E:", font=("Arial",18))
        self.le.place(x = 620, y = 270)

        self.gt = CTkLabel(self, text = "Gastado T:", font=("Arial",18))
        self.gt.place(x = 620, y = 330)

        self.ge = CTkLabel(self, text = "Gastado E:", font=("Arial",18))
        self.ge.place(x = 620, y = 390)
        
        ############################## Entrys ################################
                
        self.text_numero = CTkLabel(self, width = 200, textvariable=text_numero) 
        self.text_numero.place(x = 750, y = 30)        
        
        self.text_duenio = CTkLabel(self, width = 200, textvariable=text_duenio) 
        self.text_duenio.place(x = 750, y = 90)        
        
        self.text_banco = CTkLabel(self, width = 200, textvariable=text_banco) 
        self.text_banco.place(x = 750, y = 150)
        
        self.text_lt = CTkLabel(self, width = 200, textvariable=text_lt) 
        self.text_lt.place(x = 750, y = 210)
        
        self.text_le = CTkLabel(self, width = 200, textvariable=text_le) 
        self.text_le.place(x = 750, y = 270)
        
        self.text_gt = CTkLabel(self, width = 200, textvariable=text_gt) 
        self.text_gt.place(x = 750, y = 330)
        
        self.text_ge = CTkLabel(self, width = 200, textvariable=text_ge) 
        self.text_ge.place(x = 750, y = 390)
        
        def eliminar_tarjeta():
            error = messagebox.askyesno("Confirmar", "Confirma la eliminacion ?")
            if error == True:
                conn = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "", 
                    database = "tarjetero"   
                    )
                cursor = conn.cursor()
                sql = f""" DELETE FROM `tarjeta` WHERE numero = "{num_tar}" """
                cursor.execute(sql)
                conn.commit()


        def cancelar_eliminacion():
            self.destroy()

        self.btn_eliminar = CTkButton(self, text = "Eliminar", width = 150, height = 30, command = eliminar_tarjeta)
        self.btn_eliminar.place(x=650, y=500)

        self.btn_cancelar = CTkButton(self, text = "Cancelar", width = 150, height = 30, command= cancelar_eliminacion)
        self.btn_cancelar.place(x=830, y=500)

############################################################################################
######################################## transferencias ####################################
############################################################################################

class Transferencias(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Transferencias")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600")
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))

        try:
            self.image = CTkImage(Image.open("D:/Mis Softwares/Python/Tarjetero/transferencias.jpg"), size = (600,600))

            self.label_image = CTkLabel(self, image = self.image, text = "")
            self.label_image.place(x = 0, y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")

        self.fecha = CTkLabel(self, text = "Fecha:", font=("Arial",18))
        self.fecha.place(x = 620, y = 30)

        self.tarjeta = CTkLabel(self, text = "Tarjeta:", font=("Arial",18))
        self.tarjeta.place(x = 620, y = 90)

        self.monto = CTkLabel(self, text = "Monto:", font=("Arial",18))
        self.monto.place(x = 620, y = 150)

        self.responsable = CTkLabel(self, text = "Responsable:", font=("Arial",18))
        self.responsable.place(x = 620, y = 210)

        self.concepto = CTkLabel(self, text = "Concepto:", font=("Arial",18))
        self.concepto.place(x = 620, y = 270)
        
        
        ############################## Entrys ################################
                
        self.text_fecha = CTkEntry(self, width = 200) 
        self.text_fecha.place(x = 750, y = 30) 
        self.text_fecha.insert(0,"yyyy/mm/dd") 
        
        ############################################################################################
        ############### nuevo para mi hacerle el boton de la fecha usando calendario ###############
        def calendario():
            root = Toplevel()
            root.title("Calendario")
            root.geometry(f"+{posx + 1000}+{posy}")
            
            global cal
            cal = Calendar(root, select_mode = "day", date_pattern = "yyyy/mm/dd")
            cal.pack()

            def escoger_fecha():
                self.text_fecha.delete(0,END)
                self.text_fecha.insert(0, cal.get_date())
                root.destroy()

            btn = Button(root, text = "Usar Fecha", command = escoger_fecha)
            btn.pack()

        self.btn_calendario = CTkButton(self, text = "...", command = calendario, width=30)  
        self.btn_calendario.place(x = 960, y = 30)
        ############################################################################################
        ############################################################################################ 
               
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "", 
            database = "tarjetero"   
            )
        cursor = conn.cursor()
        lista_tarjetas = []
        sql = """SELECT `numero` FROM `tarjeta`;"""
        cursor.execute(sql)

        for index in cursor:
            lista_tarjetas.append(index[0])
                        
        self.text_tarjeta = ttk.Combobox(self, width = "30", values = lista_tarjetas) 
        self.text_tarjeta.place(x = 940, y = 120)

        pendiente = StringVar()
        pendiente.set("")

        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "", 
            database = "tarjetero"   
            )
        cursor = conn.cursor()
        sql = f"""SELECT `pendiente_transferencia` FROM `tarjeta` WHERE `numero` = "{self.text_tarjeta.get()}" """
        cursor.execute(sql)

        for index in cursor:
            pendiente.set(str(index[0]))

        self.pediente = CTkEntry(self, textvariable = pendiente, font=("Arial",18))
        self.pediente.place(x = 620, y = 380)
        
        ################### nuevo para mi actuar al seleccionar elemento del combobox #######################################
        #####################################################################################################################
        def seleccionar_tarjeta_transferencia(event):
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "", 
                database = "tarjetero"   
                )
            cursor = conn.cursor()
            sql = f"""SELECT `pendiente_transferencia` FROM `tarjeta` WHERE `numero` = {self.text_tarjeta.get()} """
            cursor.execute(sql)

            for index in cursor:
                pendiente.set(str(index[0]))            

        self.text_tarjeta.bind("<<ComboboxSelected>>", seleccionar_tarjeta_transferencia) 
        ##################################################################################################################
        ##################################################################################################################       
       
        self.text_monto = CTkEntry(self, width = 200) 
        self.text_monto.place(x = 750, y = 150)
        
        self.text_responsable = CTkEntry(self, width = 200) 
        self.text_responsable.place(x = 750, y = 210)
        
        self.text_concepto = CTkEntry(self, width = 350) 
        self.text_concepto.place(x = 620, y = 300)

        self.pediente = CTkLabel(self, text = "Pendiente a Transferir:", font=("Arial",18))
        self.pediente.place(x = 620, y = 350)


        def transferir():
            try:
                if self.text_fecha.get() == "" or self.text_tarjeta.get() == "" or self.text_monto.get() == "" or self.text_responsable.get() == "" or self.text_concepto.get() == "":
                    error = messagebox.askyesno("Error", "Llena todos los campos de informacion")
                else:
                    ################# ahora hay que verificar que no se pase de limites #################
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "", 
                        database = "tarjetero"   
                        )
                    cursor = conn.cursor()

                    sql = f"""SELECT `gastado_transferencia`, `limite_transferencia` FROM `tarjeta` WHERE {self.text_tarjeta.get()};"""
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] + int(self.text_monto.get()) <= index[1]:
                            error = messagebox.askyesno("Confirmar", "Confirma la transferencia ?")            
                            if error == True:

                                ################ 1ro agregar la transferencia a la bd #################
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "", 
                                    database = "tarjetero"   
                                    )
                                cursor = conn.cursor()

                                sql = f"""SELECT `dueño`, `banco`, `gastado_transferencia`, `limite_transferencia` FROM `tarjeta` WHERE `numero` = {self.text_tarjeta.get()};"""
                                cursor.execute(sql)
                                duenio = ""
                                banco = ""
                                gt = 0
                                lt = 0
                                for index in cursor:
                                    duenio = index[0]
                                    banco = index[1]
                                    gt = index[2]
                                    lt = index[3]

                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "", 
                                    database = "tarjetero"   
                                    )
                                cursor = conn.cursor()

                                sql = f""" INSERT INTO `operaciones`(`fecha`, `numero`, `dueño`, `banco`, `transferencia`, `extraccion`, `responsable`, `concepto`) VALUES ('{self.text_fecha.get()}','{self.text_tarjeta.get()}','{duenio}','{banco}','{self.text_monto.get()}','{0}','{self.text_responsable.get()}','{self.text_concepto.get()}') """
                                cursor.execute(sql)
                                conn.commit()

                                ########################## actualizar la tarjeta de la que transferi ############################
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "", 
                                    database = "tarjetero"   
                                    )
                                cursor = conn.cursor()

                                sql = f"""UPDATE `tarjeta` SET `gastado_transferencia`='{gt + int(self.text_monto.get())}',`pendiente_transferencia`='{lt - gt - int(self.text_monto.get())}' WHERE `numero` = {self.text_tarjeta.get()}"""
                                cursor.execute(sql)
                                conn.commit()
                        else:
                            error = messagebox.askokcancel("Error", "No puedes hacer la transferencia por exceder el limite permitido")
                            if error == True:
                                 self.destroy()
            except:
                pass
                            

        def cancelar_transferencia():
            self.destroy()
        
        self.btn_transferir = CTkButton(self, text = "Transferir", width = 150, height = 30, command = transferir)
        self.btn_transferir.place(x=650, y=500)

        self.btn_cancelar = CTkButton(self, text = "Cancelar", width = 150, height = 30, command= cancelar_transferencia)
        self.btn_cancelar.place(x=830, y=500)
        

##########################################################################################
######################################## extracciones ####################################
##########################################################################################

class Extracciones(CTkToplevel):
    def __init__(self):
        self = CTkToplevel()
        self.title("Extracciones")
        htotal = self.winfo_screenheight()
        wtotal = self.winfo_screenwidth()
        wventana = 1000
        hventana = 600
        posx = round(wtotal/2-wventana/2)
        posy = round(htotal/2-hventana/2)
        self.geometry(f"+{posx}+{posy}")
        self.geometry(f"+{posx}+{posy}")
        self.geometry("1000x600")
        self.resizable(False,False)
        self.lift()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        self.after(250, lambda: self.iconbitmap('D:/Mis Softwares/Python/Tarjetero/tarjeteroicon.ico'))

        try:
            self.image = CTkImage(Image.open("D:/Mis Softwares/Python/Tarjetero/extraccion.jpg"), size = (600,600))

            self.label_image = CTkLabel(self, image = self.image, text = "")
            self.label_image.place(x = 0, y = 0)
        except:
            error = messagebox.showinfo("Error", "No se pudo cargar la imagen")

        self.fecha = CTkLabel(self, text = "Fecha:", font=("Arial",18))
        self.fecha.place(x = 620, y = 30)

        self.tarjeta = CTkLabel(self, text = "Tarjeta:", font=("Arial",18))
        self.tarjeta.place(x = 620, y = 90)

        self.monto = CTkLabel(self, text = "Monto:", font=("Arial",18))
        self.monto.place(x = 620, y = 150)

        self.responsable = CTkLabel(self, text = "Responsable:", font=("Arial",18))
        self.responsable.place(x = 620, y = 210)

        self.concepto = CTkLabel(self, text = "Concepto:", font=("Arial",18))
        self.concepto.place(x = 620, y = 270)
        
        
        ############################## Entrys ################################
                
        self.text_fecha = CTkEntry(self, width = 200) 
        self.text_fecha.place(x = 750, y = 30) 
        self.text_fecha.insert(0,"yyyy/mm/dd") 
        
        ############################################################################################
        ############### nuevo para mi hacerle el boton de la fecha usando calendario ###############
        def calendario():
            root = Toplevel()
            root.title("Calendario")
            root.geometry(f"+{posx + 1000}+{posy}")
            
            global cal
            cal = Calendar(root, select_mode = "day", date_pattern = "yyyy/mm/dd")
            cal.pack()

            def escoger_fecha():
                self.text_fecha.delete(0,END)
                self.text_fecha.insert(0, cal.get_date())
                root.destroy()

            btn = Button(root, text = "Usar Fecha", command = escoger_fecha)
            btn.pack()

        self.btn_calendario = CTkButton(self, text = "...", command = calendario, width=30)  
        self.btn_calendario.place(x = 960, y = 30)
        ############################################################################################
        ############################################################################################ 
               
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "", 
            database = "tarjetero"   
            )
        cursor = conn.cursor()
        lista_tarjetas = []
        sql = """SELECT `numero` FROM `tarjeta`;"""
        cursor.execute(sql)

        for index in cursor:
            lista_tarjetas.append(index[0])
                        
        self.text_tarjeta = ttk.Combobox(self, width = "30", values = lista_tarjetas) 
        self.text_tarjeta.place(x = 940, y = 120)

        pendiente = StringVar()
        pendiente.set("")

        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "", 
            database = "tarjetero"   
            )
        cursor = conn.cursor()
        sql = f"""SELECT `pendiente_extraccion` FROM `tarjeta` WHERE `numero` = "{self.text_tarjeta.get()}" """
        cursor.execute(sql)

        for index in cursor:
            pendiente.set(str(index[0]))

        self.pediente = CTkEntry(self, textvariable = pendiente, font=("Arial",18))
        self.pediente.place(x = 620, y = 380)
        
        ################### nuevo para mi actuar al seleccionar elemento del combobox #######################################
        #####################################################################################################################
        def seleccionar_tarjeta_extraccion(event):
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "", 
                database = "tarjetero"   
                )
            cursor = conn.cursor()
            sql = f"""SELECT `pendiente_extraccion` FROM `tarjeta` WHERE `numero` = {self.text_tarjeta.get()} """
            cursor.execute(sql)

            for index in cursor:
                pendiente.set(str(index[0]))            

        self.text_tarjeta.bind("<<ComboboxSelected>>", seleccionar_tarjeta_extraccion) 
        ##################################################################################################################
        ##################################################################################################################       
       
        self.text_monto = CTkEntry(self, width = 200) 
        self.text_monto.place(x = 750, y = 150)
        
        self.text_responsable = CTkEntry(self, width = 200) 
        self.text_responsable.place(x = 750, y = 210)
        
        self.text_concepto = CTkEntry(self, width = 350) 
        self.text_concepto.place(x = 620, y = 300)

        self.pediente = CTkLabel(self, text = "Pendiente a Transferir:", font=("Arial",18))
        self.pediente.place(x = 620, y = 350)


        def extraer():
            try:
                if self.text_fecha.get() == "" or self.text_tarjeta.get() == "" or self.text_monto.get() == "" or self.text_responsable.get() == "" or self.text_concepto.get() == "":
                    error = messagebox.askyesno("Error", "Llena todos los campos de informacion")
                else:
                    ################# ahora hay que verificar que no se pase de limites #################
                    conn = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "", 
                        database = "tarjetero"   
                        )
                    cursor = conn.cursor()

                    sql = f"""SELECT `gastado_extraccion`, `limite_extraccion` FROM `tarjeta` WHERE {self.text_tarjeta.get()};"""
                    cursor.execute(sql)
                    for index in cursor:
                        if index[0] + int(self.text_monto.get()) <= index[1]:
                            error = messagebox.askyesno("Confirmar", "Confirma la extraccion ?")            
                            if error == True:

                                ################ 1ro agregar la extraccion a la bd #################
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "", 
                                    database = "tarjetero"   
                                    )
                                cursor = conn.cursor()

                                sql = f"""SELECT `dueño`, `banco`, `gastado_extraccion`, `limite_extraccion` FROM `tarjeta` WHERE `numero` = {self.text_tarjeta.get()};"""
                                cursor.execute(sql)
                                duenio = ""
                                banco = ""
                                ge = 0
                                le = 0
                                for index in cursor:
                                    duenio = index[0]
                                    banco = index[1]
                                    ge = index[2]
                                    le = index[3]

                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "", 
                                    database = "tarjetero"   
                                    )
                                cursor = conn.cursor()

                                sql = f""" INSERT INTO `operaciones`(`fecha`, `numero`, `dueño`, `banco`, `transferencia`, `extraccion`, `responsable`, `concepto`) VALUES ('{self.text_fecha.get()}','{self.text_tarjeta.get()}','{duenio}','{banco}','{0}','{self.text_monto.get()}','{self.text_responsable.get()}','{self.text_concepto.get()}') """
                                cursor.execute(sql)
                                conn.commit()

                                ########################## actualizar la tarjeta de la que transferi ############################
                                conn = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    password = "", 
                                    database = "tarjetero"   
                                    )
                                cursor = conn.cursor()

                                sql = f"""UPDATE `tarjeta` SET `gastado_extraccion`='{ge + int(self.text_monto.get())}',`pendiente_extraccion`='{le - ge - int(self.text_monto.get())}' WHERE `numero` = {self.text_tarjeta.get()}"""
                                cursor.execute(sql)
                                conn.commit()
                        else:
                            error = messagebox.askokcancel("Error", "No puedes hacer la extraccion por exceder el limite permitido")
                            if error == True:
                                 self.destroy()
            except:
                pass
                            

        def cancelar_extraccion():
            self.destroy()
        
        self.btn_extraer = CTkButton(self, text = "Extraer", width = 150, height = 30, command = extraer)
        self.btn_extraer.place(x=650, y=500)

        self.btn_cancelar = CTkButton(self, text = "Cancelar", width = 150, height = 30, command= cancelar_extraccion)
        self.btn_cancelar.place(x=830, y=500)



conn.close()
lobby = Lobby()
lobby.mainloop()