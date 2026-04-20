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
    texto.insert(0,str(fecha_select))
    

btn = CTkButton(self, text="Insertar Fecha", command=fecha)
btn.pack()

self.mainloop()
            

            

                







                     

                        

                        

                        

                        
                        
                    
            
            

            
            

            