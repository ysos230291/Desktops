import customtkinter as ctk
import calendar

# Configuración inicial
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Lista de nombres
nombres = [
    "María González López",
    "Carlos Pérez Ramírez",
    "Ana Martínez Sánchez",
    "José Fernández Gómez",
    "Laura Rodríguez Díaz"
]

# Función para cambiar color del día
def cambiar_color_dia(label, evento):
    color_actual = label.cget("fg_color")
    if color_actual == "green":
        label.configure(fg_color="transparent", text_color="white")
    else:
        label.configure(fg_color="green", text_color="white")

# Función para resetear colores
def resetear_colores(labels):
    for label in labels:
        if label.cget("text") != "":  # Solo días con número
            label.configure(fg_color="transparent", text_color="white")

# Función para mostrar el almanaque
def mostrar_almanaque(nombre):
    # Crear ventana emergente
    ventana_almanaque = ctk.CTkToplevel()
    ventana_almanaque.title(f"Almanaque - {nombre}")
    ventana_almanaque.geometry("500x480")
    
    # Obtener año y mes actual
    año = 2026
    mes = 7  # Julio
    
    # Generar calendario
    cal = calendar.monthcalendar(año, mes)
    
    # Título con mes y año
    titulo = ctk.CTkLabel(
        ventana_almanaque,
        text=f"{calendar.month_name[mes]} {año}",
        font=("Arial", 20, "bold")
    )
    titulo.pack(pady=15)
    
    # Frame para los días de la semana
    frame_dias = ctk.CTkFrame(ventana_almanaque)
    frame_dias.pack(pady=5)
    
    # Días de la semana
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    for i, dia in enumerate(dias_semana):
        label = ctk.CTkLabel(frame_dias, text=dia, width=50, font=("Arial", 13, "bold"))
        label.grid(row=0, column=i, padx=3, pady=3)
    
    # Frame para el calendario
    frame_calendario = ctk.CTkFrame(ventana_almanaque)
    frame_calendario.pack(pady=10)
    
    # Mostrar los días del mes
    labels_dias = []  # Lista para guardar referencias
    for semana in cal:
        for i, dia in enumerate(semana):
            if dia == 0:
                label = ctk.CTkLabel(frame_calendario, text="", width=50, height=40)
            else:
                label = ctk.CTkLabel(
                    frame_calendario, 
                    text=str(dia), 
                    width=50, 
                    height=40,
                    font=("Arial", 14),
                    fg_color="transparent"
                )
                # Hacer clic en el día para cambiar color
                label.bind("<Button-1>", lambda e, lbl=label: cambiar_color_dia(lbl, e))
            label.grid(row=len(labels_dias)//7 + 1, column=i, padx=3, pady=3)
            labels_dias.append(label)
    
    # Frame para botones
    frame_botones = ctk.CTkFrame(ventana_almanaque)
    frame_botones.pack(pady=15)
    
    # Botón para resetear colores
    btn_resetear = ctk.CTkButton(
        frame_botones,
        text="Resetear colores",
        command=lambda: resetear_colores(labels_dias),
        width=150,
        height=40
    )
    btn_resetear.pack(side="left", padx=10)
    
    # Botón para aceptar y cerrar ventana
    btn_aceptar = ctk.CTkButton(
        frame_botones,
        text="Aceptar",
        command=ventana_almanaque.destroy,
        width=150,
        height=40
    )
    btn_aceptar.pack(side="left", padx=10)

# Crear ventana principal
ventana = ctk.CTk()
ventana.title("Lista de Nombres")
ventana.geometry("400x400")

# Frame para contener los botones
frame = ctk.CTkFrame(ventana)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Crear un botón por cada nombre
for nombre in nombres:
    boton = ctk.CTkButton(
        frame,
        text=nombre,
        width=300,
        height=40,
        corner_radius=10,
        command=lambda n=nombre: mostrar_almanaque(n)
    )
    boton.pack(pady=5)

# Ejecutar ventana
ventana.mainloop()