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

self = CTk()
self.title("Calendario") 
htotal = self.winfo_screenheight()
wtotal = self.winfo_screenwidth()
wventana = 300
hventana = 300
posx = round(wtotal/2-wventana/2)
posy = round(htotal/2-hventana/2)
self.geometry(f"+{posx}+{posy}")
self.lift()
self.attributes('-topmost', True)
self.after(200, lambda: self.attributes('-topmost', False))

cal = Calendar(self, selectmode = "day", date_pattern="yyyy-mm-dd")
cal.pack()

texto = CTkEntry(self)
texto.pack()


def fecha():
    texto.delete(0,END)
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
    texto.insert(0,str(nueva_fecha_pago))
    

btn = CTkButton(self, text="Insertar Fecha", command=fecha)
btn.pack()

self.mainloop()