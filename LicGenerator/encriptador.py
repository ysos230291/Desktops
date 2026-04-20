from tkinter import *

enc = Tk()
enc.title("Encriptador")    
posx = enc.winfo_screenheight()//3
posy = enc.winfo_screenwidth()//10
enc.geometry(f"+{posx}+{posy}")
enc.geometry("500x400") 
enc.resizable(False,False)    

frame_enc = Frame(enc)
frame_enc.pack(fill="both" ,expand=True) 

label_serial = Label(frame_enc,text="Serie de la Pc:")
label_serial.place(x = 50, y = 70)
label_serial.config(font=("Times New Roman",16))

label_fecha = Label(frame_enc,text="Vence (año-mes-dia):")
label_fecha.place(x = 250, y = 70)
label_fecha.config(font=("Times New Roman",16))

label_lic = Label(frame_enc,text="Licencia:")
label_lic.place(x = 190, y = 150)
label_lic.config(font=("Times New Roman",16))

text_serial = Entry(frame_enc)
text_serial.place(x = 50, y = 100)

text_fecha = Entry(frame_enc)
text_fecha.place(x = 275, y = 100)


string_lic = StringVar()

text_lic = Entry(frame_enc, textvariable = string_lic)
text_lic.place(x = 100, y = 200)
text_lic.config(width = '50')

def generar_lic():
    year = text_fecha.get()[0:4]
    month = text_fecha.get()[5:7]
    day = text_fecha.get()[8:10]

    string_list = ["nuevalicenciaaño","mes","dia","serial"]
    string = string_list[0] + year + string_list[1] + month + string_list[2] + day + string_list[3] + text_serial.get()

        
    abecedario_normal = "qwertyuiopasdfghjklñzxcvbnm0123456789"
    abecedario_enc = "qwyu678iopamghj012ñ3sdfertklzxcvbn459"

    lista_abe_normal = list(abecedario_normal)
    lista_abe_enc = list(abecedario_enc)

    texto_encriptado = ""
    texto_normal = string

    lista_normal = list(texto_normal)
    lista_enc = []


    for i in range(len(lista_normal)):
        for j in range(len(lista_abe_normal)):
            if lista_normal[i] == lista_abe_normal[j]:
                lista_enc.append(lista_abe_enc[j])

    for index in range(len(lista_enc)):
        texto_encriptado += lista_enc[index]

    
    string_lic.set(texto_encriptado)
    
    

btn = Button(frame_enc,text="Generar",command=generar_lic)
btn.place(x=75 ,y=300 )
btn.config(width = '50', height = '3')




enc.mainloop()