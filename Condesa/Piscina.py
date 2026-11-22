from customtkinter import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, date
import mysql.connector
import subprocess
from PIL import Image
import pandas as pd
from tkcalendar import Calendar
import os


# ***************************************************************************************
# ********************************** Constantes y utilidades ****************************
# ***************************************************************************************

RUTA_IMG = "D:/condesa/imagenes funcionamiento/"
ICONO = RUTA_IMG + "condesa_icono.ico"

fecha_actual = datetime.now().date()
fecha_vencimiento = None
autorizacion = []
estado = {"etiqueta_vencimiento": None}

# columnas Insumo1, Cantidad1, ... Insumo10, Cantidad10 (en ese orden)
COLUMNAS_INSUMOS = ", ".join(f"`Insumo{i}`, `Cantidad{i}`" for i in range(1, 11))

SQL_INSERT_PRODUCTO = (
    "INSERT INTO `productos` (`Codigo`, `Nombre`, `Costo`, `PrecioUsd`, `Precio`, `Categoria`, "
    + COLUMNAS_INSUMOS + ") VALUES (" + ", ".join(["%s"] * 26) + ")"
)
SQL_UPDATE_PRODUCTO = (
    "UPDATE `productos` SET `Nombre`=%s, `Costo`=%s, `PrecioUsd`=%s, `Precio`=%s, `Categoria`=%s, "
    + ", ".join(f"`Insumo{i}`=%s, `Cantidad{i}`=%s" for i in range(1, 11))
    + " WHERE `Codigo`=%s"
)


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="condesa",
        password="123456",
        database="condesa"
    )


def db_select(sql, params=()):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        conn.close()


def db_exec(sql, params=()):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
    finally:
        conn.close()


def obtener_tarifa():
    filas = db_select("SELECT `Usd` FROM `Tarifa` LIMIT 1")
    if filas and filas[0][0] is not None:
        return float(filas[0][0])
    return 0.0


def a_decimal(texto):
    texto = texto.strip().replace(",", ".")
    if texto == "":
        return 0.0
    return float(texto)


def a_entero(texto):
    valor = a_decimal(texto)
    if valor != int(valor):
        raise ValueError("no es entero")
    return int(valor)


def fmt(valor):
    texto = format(round(float(valor), 4), "f").rstrip("0").rstrip(".")
    return texto if texto not in ("", "-0") else "0"


def fecha_valida(texto):
    try:
        datetime.strptime(texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ---------------------- encriptado de licencias ----------------------
ABECEDARIO_NORMAL = "qwertyuiopasdfghjklñzxcvbnm0123456789"
ABECEDARIO_ENC = "qwyu678iopamghj012ñ3sdfertklzxcvbn459"


def desencriptar(texto_encriptado):
    resultado = ""
    for caracter in texto_encriptado:
        for j in range(len(ABECEDARIO_ENC)):
            if caracter == ABECEDARIO_ENC[j]:
                resultado += ABECEDARIO_NORMAL[j]
    return resultado


def obtener_serial():
    # primero wmic (como siempre); si no existe en este Windows, PowerShell
    try:
        x = subprocess.run("wmic bios get serialnumber", shell=True, capture_output=True, text=True)
        lineas = [l.strip() for l in x.stdout.splitlines() if l.strip()]
        if len(lineas) >= 2:
            return lineas[1].lower()
    except Exception:
        pass
    try:
        x = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_BIOS).SerialNumber"],
            capture_output=True, text=True)
        serial = x.stdout.strip()
        if serial:
            return serial.lower()
    except Exception:
        pass
    return ""


# ---------------------- ventanas: frente, icono, instancia unica ----------------------
ventanas_abiertas = {}


def poner_icono(ventana):
    def _icono():
        try:
            ventana.iconbitmap(ICONO)
        except Exception:
            pass
    ventana.after(250, _icono)


def traer_al_frente(ventana):
    def _quitar_topmost():
        try:
            ventana.attributes('-topmost', False)
        except Exception:
            pass

    def _frente():
        try:
            ventana.lift()
            ventana.attributes('-topmost', True)
            ventana.focus_force()
        except Exception:
            return
        ventana.after(300, _quitar_topmost)

    ventana.after(100, _frente)


def crear_ventana(clave, titulo, ancho, alto, redimensionable=False):
    """Crea una ventana. Si ya habia una abierta con la misma clave, la cierra
    (descartando lo que tuviera sin guardar) y abre una nueva."""
    anterior = ventanas_abiertas.get(clave)
    if anterior is not None:
        try:
            if anterior.winfo_exists():
                anterior.destroy()
        except Exception:
            pass
        ventanas_abiertas.pop(clave, None)

    ventana = CTkToplevel()
    ventana.title(titulo)
    posx = round(ventana.winfo_screenwidth() / 2 - ancho / 2)
    posy = round(ventana.winfo_screenheight() / 2 - alto / 2)
    ventana.geometry(f"{ancho}x{alto}+{posx}+{posy}")
    if not redimensionable:
        ventana.resizable(False, False)
    poner_icono(ventana)
    traer_al_frente(ventana)
    ventanas_abiertas[clave] = ventana
    return ventana


def cerrar_ventanas_abiertas(excepto=None):
    for clave in list(ventanas_abiertas.keys()):
        if clave == excepto:
            continue
        try:
            if ventanas_abiertas[clave].winfo_exists():
                ventanas_abiertas[clave].destroy()
        except Exception:
            pass
        ventanas_abiertas.pop(clave, None)


def lobby_abierto():
    ventana = ventanas_abiertas.get("Lobby")
    try:
        return ventana is not None and bool(ventana.winfo_exists())
    except Exception:
        return False


def poner_fondo(ventana, archivo, ancho, alto):
    ventana.imagen = CTkImage(light_image=Image.open(RUTA_IMG + archivo), size=(ancho, alto))
    ventana.label_image = CTkLabel(ventana, image=ventana.imagen, text="")
    ventana.label_image.place(x=0, y=0)


def abrir_calendario(entry, despues=None):
    cal_win = crear_ventana("calendario", "Calendario", 300, 300)
    cal = Calendar(cal_win, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack()

    def insertar():
        entry.delete(0, END)
        entry.insert(0, str(cal.get_date()))
        cal_win.destroy()
        if despues:
            despues()

    CTkButton(cal_win, text="Insertar Fecha", command=insertar).pack()


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

    for orientacion in ("Vertical", "Horizontal"):
        style.configure(f"{orientacion}.TScrollbar",
            background="#2a2a2a",
            troughcolor="#1e1e1e",
            arrowcolor="#888888",
            bordercolor="#1e1e1e",
            lightcolor="#2a2a2a",
            darkcolor="#2a2a2a",
        )
        style.map(f"{orientacion}.TScrollbar",
            background=[("active", "#3a3a3a"), ("pressed", "#444444")],
            arrowcolor=[("active", "#ffffff")],
        )


def crear_tabla(ventana, columnas, anchos, x=0, y=0, alto=10, solo_headings=False,
                texto0="Codigo", ancho0=100, empaquetar=False):
    estilos_tablas()
    if solo_headings:
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
    else:
        tabla = ttk.Treeview(ventana, columns=columnas)
    tabla.column("#0", width=ancho0, anchor="center")
    tabla.heading("#0", text=texto0, anchor="center")
    for columna, ancho in zip(columnas, anchos):
        tabla.column(columna, width=ancho, anchor="center")
        tabla.heading(columna, text=columna, anchor="center")
    if empaquetar:
        tabla.pack(pady=10)
    else:
        tabla.place(x=x, y=y)
    tabla.config(height=alto)
    barra = CTkScrollbar(ventana, command=tabla.yview, width=18)
    barra.place(in_=tabla, relheight=1, relx=1)
    tabla.config(yscrollcommand=barra.set)
    return tabla


# ---------------------- insumos de un producto (para ventas, regalos y devoluciones) ----------------------
def insumos_de_producto(cursor, codigo_producto):
    cursor.execute(f"SELECT {COLUMNAS_INSUMOS} FROM `productos` WHERE `Codigo` = %s", (codigo_producto,))
    fila = cursor.fetchone()
    if fila is None:
        return []
    return [(fila[i], fila[i + 1]) for i in range(0, 20, 2) if fila[i] != 0]


def registrar_salida(es_venta, codigo, cantidad, fecha, concepto=""):
    """Vende o regala un producto. Todo en una sola transaccion: o se descuentan los
    insumos Y se guarda la salida, o no se hace nada. Devuelve None si salio bien o
    un texto con el motivo si no se pudo."""
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT `Nombre`, `Costo`, `Precio`, `Categoria` FROM `productos` WHERE `Codigo` = %s", (codigo,))
        producto = cursor.fetchone()
        if producto is None:
            return "El producto ya no existe"
        nombre, costo, precio, categoria = producto

        necesarios = {}
        for insumo, cant in insumos_de_producto(cursor, codigo):
            necesarios[insumo] = necesarios.get(insumo, 0) + cantidad * float(cant)

        for insumo, necesario in necesarios.items():
            cursor.execute("SELECT `Cantidad` FROM `insumos` WHERE `Codigo` = %s", (insumo,))
            fila = cursor.fetchone()
            if fila is not None and float(fila[0]) < necesario - 1e-6:
                accion = "vender" if es_venta else "regalar"
                return f"No alcanzan los insumos para {accion} el producto"

        for insumo, necesario in necesarios.items():
            cursor.execute("UPDATE `insumos` SET `Cantidad` = `Cantidad` - %s WHERE `Codigo` = %s", (necesario, insumo))

        tabla = "salidas" if es_venta else "regalos"
        ultima = "Categoria" if es_venta else "Concepto"
        cursor.execute(f"SELECT MAX(`Id`) FROM `{tabla}`")
        maximo = cursor.fetchone()[0]
        id_nuevo = 1 if maximo is None else maximo + 1

        cursor.execute(
            f"INSERT INTO `{tabla}` (`Id`, `Fecha`, `Codigo`, `Nombre`, `Costo`, `Precio`, `Cantidad`, `{ultima}`) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (id_nuevo, fecha, codigo, nombre, costo, precio, cantidad, categoria if es_venta else concepto))
        conn.commit()
        return None
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ***************************************************************************************
# **************** Creando Usuario, Base de Datos y Tablas de Admin necesarias **********
# ***************************************************************************************

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = conn.cursor()

# ********************** creando usuario admin ******************************
try:
    cursor.execute("""CREATE USER 'condesa'@'localhost' IDENTIFIED BY '123456';""")
    conn.commit()
except Exception:
    pass

sql = """GRANT ALL PRIVILEGES ON *.* TO 'condesa'@'localhost' REQUIRE NONE WITH GRANT OPTION MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0; """
cursor.execute(sql)
conn.commit()
conn.close()

conn = mysql.connector.connect(
    host="localhost",
    user="condesa",
    password="123456",
)
cursor = conn.cursor()

# ******* creando la base de datos condesa ***********
try:
    cursor.execute("""CREATE DATABASE condesa CHARACTER SET = utf8mb4 COLLATE utf8mb4_spanish_ci;""")
    conn.commit()
except Exception:
    pass
conn.close()

conn = conectar()
cursor = conn.cursor()

# *********** creando tabla usuarios **********
try:
    cursor.execute("""CREATE TABLE  usuarios (Usuario VARCHAR(50), Password VARCHAR(50))""")
    conn.commit()
except Exception:
    pass

cursor.execute("""SELECT Usuario FROM usuarios""")
usuarios_iniciales = [fila[0] for fila in cursor.fetchall()]

if "condesa" not in usuarios_iniciales:
    try:
        cursor.execute("""INSERT INTO usuarios (Usuario,Password) VALUES ("condesa","123456")""")
        conn.commit()
    except Exception:
        pass

# ************** creando el resto de las tablas ***************
_columnas_insumos_sql = ", ".join(f"`Insumo{i}` INT(11) NOT NULL, `Cantidad{i}` FLOAT NOT NULL" for i in range(1, 11))

SQL_TABLAS = [
    # licencias
    """CREATE TABLE `condesa`.`licencias` (`codigo_lic` VARCHAR(50) NOT NULL , `pass_economia` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;""",
    # categorias
    """CREATE TABLE `condesa`.`categorias` (`Nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;""",
    # categorias_productos
    """CREATE TABLE `condesa`.`categorias_productos` (`Nombre` VARCHAR(50) NOT NULL ) ENGINE = InnoDB;""",
    # insumos
    """CREATE TABLE `condesa`.`insumos` (`Codigo` INT(11) NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `Costo` FLOAT NOT NULL, `Cantidad` FLOAT NOT NULL, `U/M` VARCHAR(50) NOT NULL, `Categoria` VARCHAR(50) NOT NULL) ENGINE = InnoDB; """,
    # entradas
    """CREATE TABLE `condesa`.`entradas` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL,`Codigo` INT NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `Costo` FLOAT NOT NULL, `Cantidad` FLOAT NOT NULL,`Categoria` VARCHAR(50) NOT NULL) ENGINE = InnoDB;""",
    # productos (PrecioUsd va entre Costo y Precio)
    "CREATE TABLE `condesa`.`productos` (`Codigo` INT(11) NOT NULL, `Nombre` VARCHAR(50) NOT NULL, "
    "`Costo` FLOAT NOT NULL, `PrecioUsd` FLOAT NOT NULL, `Precio` FLOAT NOT NULL, `Categoria` VARCHAR(50) NOT NULL, "
    + _columnas_insumos_sql + ") ENGINE = InnoDB;",
    # salidas
    """CREATE TABLE `condesa`.`salidas` (`Id` INT(11) NOT NULL, `Fecha` DATE NOT NULL,`Codigo` INT(11) NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `Costo` FLOAT NOT NULL, `Precio` FLOAT NOT NULL, `Cantidad` INT NOT NULL, `Categoria` VARCHAR(50) NOT NULL) ENGINE = InnoDB;""",
    # regalos
    """CREATE TABLE `condesa`.`regalos` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL,`Codigo` VARCHAR(50) NOT NULL, `Nombre` VARCHAR(100) NOT NULL, `Costo` FLOAT NOT NULL, `Precio` FLOAT NOT NULL, `Cantidad` INT NOT NULL, `Concepto` VARCHAR(50) NOT NULL) ENGINE = InnoDB;""",
    # gastos asociados
    """CREATE TABLE `condesa`.`asociados` (`Id` INT NOT NULL, `Fecha` DATE NOT NULL, `Concepto` VARCHAR(100) NOT NULL, `Monto` FLOAT NOT NULL) ENGINE = InnoDB;""",
    # tarifa (una sola columna)
    """CREATE TABLE `condesa`.`Tarifa` (`Usd` FLOAT NOT NULL) ENGINE = InnoDB;""",
]

for sql in SQL_TABLAS:
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception:
        pass

# ******* la tarifa siempre tiene exactamente una fila; si esta vacia se inicializa en 0 *******
try:
    cursor.execute("SELECT COUNT(*) FROM `Tarifa`")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO `Tarifa` (`Usd`) VALUES (0)")
        conn.commit()
except Exception:
    pass

conn.close()


# *************************************************************************************
# ************************trabajo con ventana Autenticacion ***************************
# *************************************************************************************

class Autenticacion(CTk):
    def __init__(self):
        super().__init__()
        self.title("Autenticacion")
        wventana = 400
        hventana = 200
        posx = round(self.winfo_screenwidth() / 2 - wventana / 2)
        posy = round(self.winfo_screenheight() / 2 - hventana / 2)
        self.geometry(f"{wventana}x{hventana}+{posx}+{posy}")
        self.resizable(False, False)
        try:
            self.iconbitmap(ICONO)
        except Exception:
            pass

        poner_fondo(self, "fondo1.jpg", 400, 200)

        ################# textos y entradas ##################
        self.label_usuario = CTkLabel(self, text="Usuario:", font=("Times New Roman", 16), fg_color="black")
        self.label_usuario.place(x=63, y=20)

        self.texto_usuario = CTkEntry(self)
        self.texto_usuario.place(x=200, y=20)

        self.label_usuariolabel_pass = CTkLabel(self, text="Contraseña:", font=("Times New Roman", 16), fg_color="black")
        self.label_usuariolabel_pass.place(x=40, y=70)

        self.texto_pass = CTkEntry(self, show="*")
        self.texto_pass.place(x=200, y=70)

        global autorizacion
        autorizacion = [tuple(fila) for fila in db_select("SELECT Usuario, Password FROM usuarios")]

        def codigo_btn_iniciar():
            global fecha_vencimiento

            # ******************** control de vencimiento *****************
            filas = db_select("SELECT codigo_lic FROM licencias")
            lic = filas[-1][0] if filas else ""

            if lic == "":
                self.withdraw()
                NuevaLicencia()
                return

            texto_normal = desencriptar(lic)
            try:
                fecha_vencimiento = date(int(texto_normal[16:20]), int(texto_normal[23:25]), int(texto_normal[28:30]))
            except Exception:
                messagebox.showinfo("Error", "La lic no es correcta")
                return

            autenticar_usuario = False
            autenticar_pass = False

            for usuario, clave in autorizacion:
                if self.texto_usuario.get() == usuario:
                    autenticar_usuario = True
                    if self.texto_pass.get() == clave:
                        autenticar_pass = True
                        break

            if autenticar_pass:
                self.withdraw()
                self.texto_usuario.delete(0, END)
                self.texto_pass.delete(0, END)
                if fecha_vencimiento < fecha_actual:
                    NuevaLicencia()
                else:
                    Lobby()
            elif not autenticar_usuario:
                messagebox.showwarning("Error", "Usuario incorrecto")
            else:
                messagebox.showwarning("Error", "Contraseña incorrecta")

        self.btn_iniciar = CTkButton(self, text="Iniciar", command=codigo_btn_iniciar, width=200)
        self.btn_iniciar.place(x=100, y=160)

        traer_al_frente(self)


# ****************************************************************************************
# ********************************** nueva_licencia **************************************
# ****************************************************************************************

class NuevaLicencia:
    def __init__(self):
        self = crear_ventana("Licencia", "Licencia", 300, 200)
        poner_fondo(self, "fondo1.jpg", 300, 200)

        CTkLabel(self, text="Introduzca la licencia nueva", font=("Times New Roman", 14)).place(x=60, y=20)

        texto = CTkEntry(self, width=200)
        texto.place(x=60, y=80)

        def cancelar_nueva_lic():
            self.destroy()
            # si no hay Lobby abierto (licencia pedida al iniciar) volvemos a la pantalla de acceso
            if not lobby_abierto():
                autenticacion.deiconify()

        def codigo_btn_aceptar_nueva_licencia():
            global fecha_vencimiento
            # el codigo debe tener un formato como el del siguiente ejemplo:
            # nuevalicenciaaño2025-mes01-dia01serial5cd028cgmk
            # solo cambiamos los numeros de año , mes , dia y serial lo demas se mantiene igual
            texto_encriptado = texto.get().strip()
            try:
                texto_normal = desencriptar(texto_encriptado)
                nueva_fecha = date(int(texto_normal[16:20]), int(texto_normal[23:25]), int(texto_normal[28:30]))
                serial_txt = texto_normal[36:]
            except Exception:
                messagebox.showinfo("Error", "Licencia Inservible")
                return

            if obtener_serial() != serial_txt:
                messagebox.showinfo("Error", "Licencia Inservible. Estas en una pc incorrecta")
                return

            try:
                if db_select("SELECT codigo_lic FROM `licencias`"):
                    db_exec("UPDATE `licencias` SET `codigo_lic` = %s", (texto_encriptado,))
                else:
                    db_exec("INSERT INTO `licencias`(`codigo_lic`, `pass_economia`) VALUES (%s, '')", (texto_encriptado,))
            except Exception:
                messagebox.showerror("Error", "No se pudo guardar la licencia")
                return

            fecha_vencimiento = nueva_fecha

            if fecha_vencimiento < fecha_actual:
                messagebox.showinfo("Error", "Licencia Inservible")
                return

            self.destroy()
            if lobby_abierto():
                try:
                    estado["etiqueta_vencimiento"].configure(text="Vence (" + str(fecha_vencimiento) + ")")
                except Exception:
                    pass
                messagebox.showinfo("Licencia", "Licencia actualizada")
            else:
                Lobby()

        self.protocol("WM_DELETE_WINDOW", cancelar_nueva_lic)

        CTkButton(self, text="Aceptar", command=codigo_btn_aceptar_nueva_licencia, width=100, height=30).place(x=30, y=160)
        CTkButton(self, text="Cancelar", command=cancelar_nueva_lic, width=100, height=30).place(x=170, y=160)


# *******************************************************************************************
# ********************************* Trabajo con Lobby ***************************************
# *******************************************************************************************

class Lobby:
    def __init__(self):
        self = crear_ventana("Lobby", "Condesa", 1300, 700)
        poner_fondo(self, "fondo3.jpg", 1300, 700)

        firma = "Vence (" + str(fecha_vencimiento) + ")"
        estado["etiqueta_vencimiento"] = CTkLabel(self, text=firma, font=("Times New Roman", 16))
        estado["etiqueta_vencimiento"].place(x=1150, y=650)

        self.menu = Menu(self)
        self.config(menu=self.menu)

        def salva_lobby():
            # Crear carpeta de respaldos si no existe
            carpeta_respaldo = "D:/condesa/respaldos"
            if not os.path.exists(carpeta_respaldo):
                os.makedirs(carpeta_respaldo)

            nombre_archivo = f"condesa_{fecha_actual}.sql"
            ruta_completa = os.path.join(carpeta_respaldo, nombre_archivo)

            # Ruta de mysqldump en XAMPP
            ruta_mysqldump = "C:/xampp/mysql/bin/mysqldump.exe"

            try:
                comando = f'"{ruta_mysqldump}" -u condesa -p123456 condesa > "{ruta_completa}"'
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)

                if os.path.exists(ruta_completa) and os.path.getsize(ruta_completa) > 0:
                    messagebox.showinfo("Éxito", f"Respaldo creado exitosamente:\n{ruta_completa}\nTamaño: {os.path.getsize(ruta_completa)} bytes")
                else:
                    error_msg = resultado.stderr if resultado.stderr else "No se pudo crear el respaldo"
                    messagebox.showerror("Error", f"Error al crear respaldo:\n{error_msg}")

            except Exception as e:
                messagebox.showerror("Error", f"Error al crear respaldo:\n{str(e)}")

        def cerrar_cesion():
            cerrar_ventanas_abiertas(excepto="Lobby")
            self.destroy()
            autenticacion.deiconify()
            traer_al_frente(autenticacion)

        def cerrar_programa():
            self.quit()
            self.destroy()
            autenticacion.destroy()
            quit()

        # para que se cierre todo el programa si cerramos esta ventana
        self.protocol("WM_DELETE_WINDOW", cerrar_programa)

        def submenu(opciones):
            menu = Menu(self.menu, tearoff=0)
            for etiqueta, comando in opciones:
                menu.add_command(label=etiqueta, command=comando)
            return menu

        devoluciones_menu = submenu([("Devolver Regalo", ControlRegalos), ("Devolver Venta", ControlVentas)])
        productos_menu = submenu([("Ver y Modificar", ModificarProducto), ("Nuevo Producto", NuevoProducto)])
        gastos_menu = submenu([("Asociados", Asociados)])
        consultas_menu = submenu([("Totales", ConsultaTotales)])
        entradas_menu = submenu([("Ver y Modificar", Insumos), ("Nuevo Insumo", NuevoInsumo), ("Reabastecer", Reabastecer)])
        administrativo_menu = submenu([("Categorias Insumos", Categorias), ("Categorias Productos", CategoriasProductos)])
        usuario_menu = submenu([("Agregar", UsuarioAgregar), ("Eliminar", EliminarUsuario)])
        licencia_menu = submenu([("Nueva", NuevaLicencia)])
        salir_menu = submenu([("Cerrar Cesion", cerrar_cesion), ("Cerrar Programa", cerrar_programa)])

        self.menu.add_cascade(label="Ventas", command=Ventas)
        self.menu.add_cascade(label="Devoluciones", menu=devoluciones_menu)
        self.menu.add_cascade(label="Consultas", menu=consultas_menu)
        self.menu.add_cascade(label="Gastos", menu=gastos_menu)
        self.menu.add_cascade(label="Productos", menu=productos_menu)
        self.menu.add_cascade(label="Tarifa", command=Tarifa)
        self.menu.add_cascade(label="Insumos", menu=entradas_menu)
        self.menu.add_cascade(label="Administrativo", menu=administrativo_menu)
        self.menu.add_cascade(label="Salva", command=salva_lobby)
        self.menu.add_cascade(label="Usuarios", menu=usuario_menu)
        self.menu.add_cascade(label="Licencia", menu=licencia_menu)
        self.menu.add_cascade(label="Salir", menu=salir_menu)


# ******************************************************************************************
# ********************************* usuarios_agregar **************************************
# ******************************************************************************************

class UsuarioAgregar:
    def __init__(self):
        self = crear_ventana("UsuarioAgregar", "Agregar Usuario", 400, 300)
        poner_fondo(self, "fondo5.jpg", 400, 300)

        fuente = ("Times New Roman", 14)
        CTkLabel(self, text="Usuario:", font=fuente).place(x=50, y=50)
        CTkLabel(self, text="Contraseña:", font=fuente).place(x=50, y=90)
        CTkLabel(self, text="Confirmar:", font=fuente).place(x=50, y=130)

        texto_nombre = CTkEntry(self)
        texto_nombre.place(x=200, y=55)
        texto_pass = CTkEntry(self, show="*")
        texto_pass.place(x=200, y=95)
        texto_confirmar = CTkEntry(self, show="*")
        texto_confirmar.place(x=200, y=135)

        def aceptar():
            nombre = texto_nombre.get()
            clave = texto_pass.get()
            if nombre.strip() == "":
                messagebox.showwarning("Error", "Escribe el nombre del usuario")
                return
            if clave != texto_confirmar.get():
                messagebox.showwarning("Error", "Confirmacion incorrecta")
                return
            if any(nombre == u for u, _ in autorizacion):
                messagebox.showwarning("Error", "Ese usuario ya existe")
                return
            try:
                db_exec("INSERT INTO usuarios (Usuario, Password) VALUES (%s, %s)", (nombre, clave))
                autorizacion.append((nombre, clave))
                self.destroy()
            except Exception:
                messagebox.showinfo("Error", "No se pudo agregar el ususario")

        CTkButton(self, text="Aceptar", command=aceptar, width=150, height=30).place(x=30, y=200)
        CTkButton(self, text="Cancelar", command=self.destroy, width=150, height=30).place(x=220, y=200)


# ******************************************************************************************
# ******************************** usuarios_eliminar ***************************************
# ******************************************************************************************

class EliminarUsuario:
    def __init__(self):
        self = crear_ventana("EliminarUsuario", "Eliminar", 400, 300)
        poner_fondo(self, "fondo5.jpg", 400, 300)

        items_usuarios = [fila[0] for fila in db_select("SELECT `Usuario` FROM `usuarios`;")]

        combo = CTkComboBox(self, values=items_usuarios)
        combo.set("Usuario...")
        combo.place(x=150, y=100)

        def eliminar():
            usuario = combo.get()
            try:
                if usuario == "condesa":
                    messagebox.showinfo("Error", "Ese usuario no puede eliminarse")
                    return
                if not any(usuario == u for u, _ in autorizacion):
                    return
                if not messagebox.askokcancel("Delete", "Se borrara el Usuario"):
                    return
                db_exec("DELETE FROM `usuarios` WHERE Usuario = %s", (usuario,))
                for indice in range(len(autorizacion) - 1, -1, -1):
                    if autorizacion[indice][0] == usuario:
                        autorizacion.pop(indice)
                self.destroy()
            except Exception:
                messagebox.showinfo("Error", "No se pudo eliminar el usuario")

        CTkButton(self, text="Eliminar", command=eliminar, width=150, height=30).place(x=50, y=200)
        CTkButton(self, text="Cancelar", command=self.destroy, width=150, height=30).place(x=220, y=200)


# **********************************************************************************
# ******************** Categorias (insumos y productos) ****************************
# **********************************************************************************

def ventana_categorias(clave, titulo, tabla_sql):
    v = crear_ventana(clave, titulo, 800, 600)
    poner_fondo(v, "fondo.jpg", 800, 600)

    tabla = crear_tabla(v, (), (), 100, 50, 10, texto0="Categorias", ancho0=500)
    seleccion = {"nombre": None}

    def on_click(event):
        sel = tabla.selection()
        if sel:
            seleccion["nombre"] = tabla.item(sel[0], "text")

    tabla.bind("<ButtonRelease-1>", on_click)

    def llenar_tabla():
        tabla.delete(*tabla.get_children())
        for fila in db_select(f"SELECT `Nombre` FROM `{tabla_sql}`;"):
            tabla.insert("", END, text=fila[0])

    llenar_tabla()

    def agregar():
        temp = crear_ventana(clave + "_agregar", "Agregar", 300, 300)
        entry = CTkEntry(temp, placeholder_text="Categoria ...")
        entry.pack(pady=10)

        def aceptar():
            nombre = entry.get()
            if nombre == "":
                messagebox.showerror("Error", "Debes escribir algun nombre para la categoria que quieres agregar")
                return
            if db_select(f"SELECT 1 FROM `{tabla_sql}` WHERE `Nombre` = %s", (nombre,)):
                messagebox.showerror("Error", "Esa categoria ya existe")
                return
            db_exec(f"INSERT INTO `{tabla_sql}`(`Nombre`) VALUES (%s)", (nombre,))
            llenar_tabla()
            messagebox.showinfo("Terminado", "Se ha creado la Categoria")
            temp.destroy()

        CTkButton(temp, text="Aceptar", command=aceptar).pack(pady=10)

    def eliminar():
        nombre = seleccion["nombre"]
        if not nombre:
            messagebox.showerror("Error", "Selecciona una categoria para eliminar")
            return
        if messagebox.askokcancel("Confirmar", f"Vas a eliminar a {nombre} de las categorias"):
            db_exec(f"DELETE FROM `{tabla_sql}` WHERE `Nombre` = %s", (nombre,))
            llenar_tabla()
            messagebox.showinfo("Terminado", "Se ha eliminado la Categoria")
            seleccion["nombre"] = None

    CTkButton(v, text="Agregar", command=agregar, width=200, height=30).place(x=100, y=400)
    CTkButton(v, text="Eliminar", command=eliminar, width=200, height=30).place(x=500, y=400)


class Categorias:
    def __init__(self):
        ventana_categorias("Categorias", "Categorias Insumos", "categorias")


class CategoriasProductos:
    def __init__(self):
        ventana_categorias("CategoriasProductos", "Categorias Productos", "categorias_productos")


# **********************************************************************************
# ******************************** Campos de insumo ********************************
# **********************************************************************************

def campos_insumo(v, con_fecha=False):
    fuente = ("Times New Roman", 16)
    for texto, atributo, y in (("Nombre:", "texto_nombre", 70), ("Costo:", "texto_costo", 110),
                               ("U/M:", "texto_um", 150), ("Cantidad:", "texto_cantidad", 190)):
        CTkLabel(v, text=texto, font=fuente).place(x=630, y=y)
        entry = CTkEntry(v)
        entry.place(x=750, y=y)
        setattr(v, atributo, entry)

    CTkLabel(v, text="Categoria:", font=fuente).place(x=630, y=230)
    categorias = [fila[0] for fila in db_select("SELECT `Nombre` FROM `categorias`;")]
    v.texto_categoria = CTkComboBox(v, values=categorias)
    v.texto_categoria.set("...")
    v.texto_categoria.place(x=750, y=230)

    if con_fecha:
        v.texto_fecha = CTkEntry(v, placeholder_text="Fecha ...")
        v.texto_fecha.place(x=750, y=30)
        v.texto_fecha.bind("<ButtonRelease-1>", lambda e: abrir_calendario(v.texto_fecha))


# **********************************************************************************
# ******************************** Nuevo Insumo **********************************
# **********************************************************************************

class NuevoInsumo:
    def __init__(self):
        self = crear_ventana("NuevoInsumo", "Nuevo Insumo", 1000, 600)
        poner_fondo(self, "fondo2.jpg", 600, 600)

        # ************************ para saber por donde voy
        ultimo_id = StringVar()
        CTkLabel(self, textvariable=ultimo_id).place(x=630, y=30)

        def actualizar_id():
            fila = db_select("SELECT MAX(Codigo) FROM `insumos`;")
            ultimo_id.set("" if not fila or fila[0][0] is None else fila[0][0])

        actualizar_id()
        campos_insumo(self, con_fecha=True)

        def agregar_insumo():
            nombre = self.texto_nombre.get().strip()
            fecha = self.texto_fecha.get().strip()
            if nombre == "":
                messagebox.showerror("Error", "Debes escribir el nombre del insumo")
                return
            if not fecha_valida(fecha):
                messagebox.showerror("Error", "Selecciona una fecha valida")
                return
            try:
                costo = a_decimal(self.texto_costo.get())
                cantidad = a_decimal(self.texto_cantidad.get())
            except ValueError:
                messagebox.showerror("Error", "El costo y la cantidad deben ser numeros")
                return
            if not messagebox.askokcancel("Confirmar", "Vamos a agregar el producto a la base de datos"):
                return

            um = self.texto_um.get()
            categoria = self.texto_categoria.get()

            # el insumo y su entrada se guardan juntos o no se guarda nada
            conn = conectar()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(Codigo) FROM `insumos`;")
                maximo = cursor.fetchone()[0]
                id_insumo = 1 if maximo is None else maximo + 1

                cursor.execute(
                    "INSERT INTO `insumos`(`Codigo`, `Nombre`, `Costo`, `Cantidad`, `U/M`, `Categoria`) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id_insumo, nombre, costo, cantidad, um, categoria))

                cursor.execute("SELECT MAX(Id) FROM `entradas`;")
                maximo = cursor.fetchone()[0]
                id_entrada = 1 if maximo is None else maximo + 1

                cursor.execute(
                    "INSERT INTO `entradas`(`Id`, `Fecha`, `Codigo`, `Nombre`, `Costo`, `Cantidad`, `Categoria`) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (id_entrada, fecha, id_insumo, nombre, costo, cantidad, categoria))
                conn.commit()
            except Exception:
                conn.rollback()
                messagebox.showerror("Error", "Hubo problemas para agregar el producto")
                return
            finally:
                conn.close()

            # limpiar los campos
            self.texto_nombre.delete(0, END)
            self.texto_fecha.delete(0, END)
            self.texto_costo.delete(0, END)
            self.texto_um.delete(0, END)
            self.texto_cantidad.delete(0, END)
            self.texto_categoria.set("...")
            actualizar_id()

        CTkButton(self, text="Aceptar", command=agregar_insumo, width=300, height=40).place(x=650, y=500)


# **********************************************************************************
# ************************** Reabastecer Producto **********************************
# **********************************************************************************

class Reabastecer:
    def __init__(self):
        self = crear_ventana("Reabastecer", "Reabastecer Insumo", 1000, 600)
        poner_fondo(self, "fondo4.jpg", 1000, 600)

        tabla = crear_tabla(self, ("Nombre", "Costo", "Cantidad", "U/M", "Categoria"),
                            (200, 100, 100, 100, 100), 50, 200, 10)

        def llenar_reabastecer(event=None):
            tabla.delete(*tabla.get_children())
            filas = db_select(
                "SELECT `Codigo`, `Nombre`, ROUND(`Costo`, 4), ROUND(`Cantidad`, 4), `U/M`, `Categoria` FROM insumos "
                "WHERE `Codigo` LIKE %s and `Nombre` LIKE %s;",
                (f"%{texto_buscador_codigo.get()}%", f"%{texto_buscador_nombre.get()}%"))
            for fila in filas:
                tabla.insert("", END, text=fila[0], values=fila[1:])

        # vamos a hacer un buscador
        CTkLabel(self, text="------------------------------ Buscador ------------------------------", bg_color="black").place(x=50, y=50)

        texto_buscador_codigo = CTkEntry(self, placeholder_text="Buscar por codigo ...")
        texto_buscador_codigo.place(x=50, y=90)
        texto_buscador_codigo.bind("<KeyRelease>", llenar_reabastecer)

        texto_buscador_nombre = CTkEntry(self, placeholder_text="Buscar por nombre ...")
        texto_buscador_nombre.place(x=200, y=90)
        texto_buscador_nombre.bind("<KeyRelease>", llenar_reabastecer)

        llenar_reabastecer()

        # cuando demos 2ble click abriremos una ventana para hacer el reabastecimiento a ese producto seleccionado
        def reabastecer(event):
            seleccion = tabla.selection()
            if not seleccion:
                return
            codigo = tabla.item(seleccion[0], "text")

            temp = crear_ventana("ReabastecerPopup", "Reabastecer", 200, 200)

            texto_fecha = CTkEntry(temp, placeholder_text="Fecha ...")
            texto_fecha.pack(pady=5)
            texto_fecha.bind("<ButtonRelease-1>", lambda e: abrir_calendario(texto_fecha))

            texto_cantidad = CTkEntry(temp, placeholder_text="Cantidad ...")
            texto_cantidad.pack(pady=5)

            def reabastecer_insumo():
                # validamos ANTES de tocar la base de datos
                fecha = texto_fecha.get().strip()
                if not fecha_valida(fecha):
                    messagebox.showerror("Error", "Selecciona una fecha valida")
                    return
                try:
                    cantidad = a_decimal(texto_cantidad.get())
                except ValueError:
                    messagebox.showerror("Error", "La cantidad debe ser un numero")
                    return
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser mayor que cero")
                    return
                if not messagebox.askokcancel("Confirmar", f"Vamos a reabastecer el producto de codigo {codigo}"):
                    return

                # el aumento del stock y la entrada se guardan juntos o no se guarda nada
                conn = conectar()
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT `Nombre`, `Costo`, `Categoria` FROM `insumos` WHERE `Codigo` = %s", (codigo,))
                    insumo = cursor.fetchone()
                    if insumo is None:
                        raise ValueError("El insumo no existe")
                    nombre, costo, categoria = insumo

                    cursor.execute("UPDATE `insumos` SET `Cantidad` = `Cantidad` + %s WHERE `Codigo` = %s", (cantidad, codigo))

                    cursor.execute("SELECT MAX(Id) FROM `entradas`;")
                    maximo = cursor.fetchone()[0]
                    id_entrada = 1 if maximo is None else maximo + 1

                    cursor.execute(
                        "INSERT INTO `entradas`(`Id`, `Fecha`, `Codigo`, `Nombre`, `Costo`, `Cantidad`, `Categoria`) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (id_entrada, fecha, codigo, nombre, costo, cantidad, categoria))
                    conn.commit()
                except Exception:
                    conn.rollback()
                    messagebox.showerror("Error", "No se pudo reabastecer el producto")
                    return
                finally:
                    conn.close()

                temp.destroy()
                llenar_reabastecer()

            CTkButton(temp, text="Reabastecer", command=reabastecer_insumo).pack(pady=10)

        tabla.bind("<Double-1>", reabastecer)


# **********************************************************************************
# ************************************* Insumos ************************************
# **********************************************************************************

class Insumos:
    def __init__(self):
        self = crear_ventana("Insumos", "Insumos", 1000, 600)
        poner_fondo(self, "fondo.jpg", 1000, 600)

        tabla = crear_tabla(self, ("Nombre", "Costo", "U/M", "Cantidad", "Categoria"),
                            (200, 100, 75, 75, 200), 50, 200, 10, ancho0=75)

        # vamos a mostrar el equivalente en dinero a los productos que hay en almacen
        string = StringVar()
        string.set("En Almacen:")

        def actualizar_equivalencia():
            fila = db_select("SELECT ROUND(SUM(`Costo` * `Cantidad`), 2) FROM `insumos`;")
            valor = 0 if not fila or fila[0][0] is None else fila[0][0]
            string.set("En Almacen: " + f"{valor} ")

        actualizar_equivalencia()
        CTkLabel(self, textvariable=string).place(x=700, y=50)

        def llenar_tabla(event=None):
            tabla.delete(*tabla.get_children())
            filas = db_select(
                "SELECT `Codigo`, `Nombre`, ROUND(`Costo`, 4), `U/M`, ROUND(`Cantidad`, 4), `Categoria` FROM insumos "
                "WHERE `Codigo` LIKE %s and `Nombre` LIKE %s ORDER BY `Codigo`;",
                (f"%{texto_buscador_codigo.get()}%", f"%{texto_buscador_nombre.get()}%"))
            for fila in filas:
                tabla.insert("", END, text=fila[0], values=fila[1:])

        # vamos a hacer un buscador
        CTkLabel(self, text="------------------------------ Buscador ------------------------------").place(x=50, y=50)

        texto_buscador_codigo = CTkEntry(self, placeholder_text="Buscar por codigo ...")
        texto_buscador_codigo.place(x=50, y=90)
        texto_buscador_codigo.bind("<KeyRelease>", llenar_tabla)

        texto_buscador_nombre = CTkEntry(self, placeholder_text="Buscar por nombre ...")
        texto_buscador_nombre.place(x=200, y=90)
        texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla)

        def doble_click(event):
            seleccion = tabla.selection()
            if not seleccion:
                return
            codigo_almacen = tabla.item(seleccion[0], "text")
            nombre_almacen = tabla.item(seleccion[0], "values")[0]

            temp = crear_ventana("InsumosPopup", "Selección", 200, 200)

            def modificar():
                root = crear_ventana("ModificarInsumo", "Modificar", 1000, 600)
                poner_fondo(root, "fondo.jpg", 600, 600)
                campos_insumo(root)

                # vamos a llenar los campos con la info que ya existe en la base de datos
                filas = db_select(
                    "SELECT `Nombre`, `Costo`, `U/M`, `Cantidad`, `Categoria` FROM `insumos` WHERE `Codigo` = %s", (codigo_almacen,))
                if filas:
                    nombre, costo, um, cantidad, categoria = filas[0]
                    root.texto_nombre.insert(0, nombre)
                    root.texto_costo.insert(0, fmt(costo))
                    root.texto_um.insert(0, um)
                    root.texto_cantidad.insert(0, fmt(cantidad))
                    root.texto_categoria.set(categoria)

                def modificar_insumo():
                    try:
                        costo = a_decimal(root.texto_costo.get())
                        cantidad = a_decimal(root.texto_cantidad.get())
                    except ValueError:
                        messagebox.showerror("Error", "El costo y la cantidad deben ser numeros")
                        return
                    if not messagebox.askokcancel("Confirmar", "Vamos a modificar el producto en la base de datos"):
                        return
                    try:
                        db_exec(
                            "UPDATE `insumos` SET `Nombre`=%s, `Costo`=%s, `U/M`=%s, `Cantidad`=%s, `Categoria`=%s WHERE `Codigo` = %s;",
                            (root.texto_nombre.get(), costo, root.texto_um.get(), cantidad, root.texto_categoria.get(), codigo_almacen))
                    except Exception:
                        messagebox.showerror("Error", "No se ha podido modificar el producto")
                        return
                    messagebox.showinfo("Completado", "Se modifico el producto")
                    try:
                        llenar_tabla()
                        actualizar_equivalencia()
                    except Exception:
                        pass
                    root.destroy()
                    temp.destroy()

                CTkButton(root, text="Modificar", command=modificar_insumo, width=150, height=40).place(x=650, y=500)

            CTkButton(temp, text="Modificar", command=modificar).pack(pady=20)

            def eliminar():
                if messagebox.askokcancel("Confirmar", f"Vamos a eliminar el producto: {nombre_almacen}"):
                    try:
                        db_exec("DELETE FROM `insumos` WHERE `Codigo` = %s", (codigo_almacen,))
                    except Exception:
                        messagebox.showerror("Error", "No se pudo eliminar el producto")
                        return
                    actualizar_equivalencia()
                    llenar_tabla()
                    temp.destroy()

            CTkButton(temp, text="Eliminar", command=eliminar).pack(pady=20)

        tabla.bind("<Double-1>", doble_click)

        llenar_tabla()


# **********************************************************************************
# ******************** Formulario de producto (nuevo y modificar) ******************
# **********************************************************************************

def crear_formulario_producto(v):
    """Dibuja los campos de un producto en la ventana v. El precio se escribe en USD;
    el Precio final se calcula como Tarifa.Usd x PrecioUsd al guardar."""
    fuente = ("Times New Roman", 16)

    CTkLabel(v, text="Nombre:", font=fuente).place(x=630, y=20)
    v.texto_nombre = CTkEntry(v)
    v.texto_nombre.place(x=750, y=20)

    CTkLabel(v, text="Costo:", font=fuente).place(x=630, y=60)
    v.string_costo = StringVar(value="0")
    CTkLabel(v, textvariable=v.string_costo, font=fuente).place(x=750, y=60)

    CTkLabel(v, text="Precio Usd:", font=fuente).place(x=630, y=100)
    v.texto_precio = CTkEntry(v)
    v.texto_precio.place(x=750, y=100)

    CTkLabel(v, text="C / P:", font=fuente).place(x=630, y=140)
    v.string_cp = StringVar(value="0")
    CTkLabel(v, textvariable=v.string_cp, font=fuente).place(x=750, y=140)

    CTkLabel(v, text="Categoria:", font=fuente).place(x=630, y=180)
    categorias = [fila[0] for fila in db_select("SELECT * FROM `categorias_productos`;")]
    v.texto_categoria = CTkComboBox(v, values=categorias)
    v.texto_categoria.set("...")
    v.texto_categoria.place(x=750, y=180)

    CTkLabel(v, text="**************************************** Seccion Insumos ****************************************",
             font=fuente).place(x=150, y=220)

    # C / P = costo / (tarifa x precio usd); si el precio es 0 se muestra 0
    def actualizar_cp(event=None):
        try:
            costo = float(v.string_costo.get())
            precio = obtener_tarifa() * a_decimal(v.texto_precio.get())
            v.string_cp.set(str(round(costo / precio, 4)) if precio > 0 else "0")
        except Exception:
            v.string_cp.set("0")

    # costo total del producto segun sus insumos
    def calcular_costo(event=None):
        total = 0.0
        conn = conectar()
        try:
            cursor = conn.cursor()
            for i in range(10):
                codigo_txt = v.ins[i].get().strip()
                cantidad_txt = v.cant[i].get().strip()
                if codigo_txt == "" or cantidad_txt == "":
                    continue
                try:
                    codigo = a_entero(codigo_txt)
                    cantidad = a_decimal(cantidad_txt)
                except ValueError:
                    continue
                cursor.execute("SELECT `Costo` FROM `insumos` WHERE `Codigo` = %s", (codigo,))
                fila = cursor.fetchone()
                if fila is not None:
                    total += cantidad * float(fila[0])
        finally:
            conn.close()
        v.string_costo.set(str(round(total, 4)))
        actualizar_cp()

    v.calcular_costo = calcular_costo
    v.actualizar_cp = actualizar_cp
    v.texto_precio.bind("<KeyRelease>", actualizar_cp)

    # --------------- seleccion de insumos
    def seleccionar_insumo(n):
        sel = crear_ventana("SelectorInsumo", "Seleccionar Insumo", 720, 420)

        buscador = CTkEntry(sel, placeholder_text="Buscar por Nombre ...")
        buscador.pack(pady=10)

        tabla = crear_tabla(sel, ("Nombre", "Costo", "Cantidad", "U/M", "Categoria"),
                            (200, 100, 75, 75, 200), solo_headings=True, empaquetar=True)

        def llenar(event=None):
            tabla.delete(*tabla.get_children())
            filas = db_select(
                "SELECT `Codigo`, `Nombre`, ROUND(`Costo`, 4), ROUND(`Cantidad`, 4), `U/M`, `Categoria` FROM insumos WHERE `Nombre` LIKE %s;",
                (f"%{buscador.get()}%",))
            for fila in filas:
                tabla.insert("", END, text=fila[0], values=fila[1:])

        buscador.bind("<KeyRelease>", llenar)
        llenar()

        # ahora hay que seleccionar el insumo con 2ble click
        def escoger(event):
            seleccion = tabla.selection()
            if not seleccion:
                return
            codigo = tabla.item(seleccion[0], "text")
            medida = tabla.item(seleccion[0], "values")[3]

            v.ins[n].delete(0, END)
            v.ins[n].insert(0, codigo)
            v.um[n].set(medida)
            calcular_costo()
            sel.destroy()

        tabla.bind("<Double-1>", escoger)

    # --------------- los 10 insumos
    v.ins = []
    v.cant = []
    v.um = []
    for i in range(10):
        y = 260 + 40 * (i % 5)
        if i < 5:
            xb, xi, xc, xu = 100, 190, 260, 340
        else:
            xb, xi, xc, xu = 650, 740, 810, 890

        um_var = StringVar()

        CTkButton(v, text=f"Insumo{i + 1}", command=lambda n=i: seleccionar_insumo(n), width=75).place(x=xb, y=y)

        entry_codigo = CTkEntry(v, placeholder_text="codigo...", width=60)
        entry_codigo.place(x=xi, y=y)
        entry_codigo.bind("<KeyRelease>", calcular_costo)

        entry_cantidad = CTkEntry(v, placeholder_text="cantidad...", width=70)
        entry_cantidad.place(x=xc, y=y)
        entry_cantidad.bind("<KeyRelease>", calcular_costo)

        CTkLabel(v, textvariable=um_var, font=fuente).place(x=xu, y=y)

        v.ins.append(entry_codigo)
        v.cant.append(entry_cantidad)
        v.um.append(um_var)


def leer_formulario_producto(v):
    """Valida el formulario. Devuelve un diccionario con los datos listos para guardar, o None."""
    nombre = v.texto_nombre.get().strip()
    precio_txt = v.texto_precio.get().strip()
    categoria = v.texto_categoria.get().strip()

    if nombre == "" or precio_txt == "" or categoria == "":
        messagebox.showerror("Error", "Debes llenar los campor de arriba")
        return None

    try:
        precio_usd = a_decimal(precio_txt)
        insumos = []
        for i in range(10):
            insumos.append(a_entero(v.ins[i].get()))
            insumos.append(a_decimal(v.cant[i].get()))
    except ValueError:
        messagebox.showerror("Error", "Verifica los datos que escribiste")
        return None

    if precio_usd < 0:
        messagebox.showerror("Error", "El precio en Usd no puede ser negativo")
        return None

    v.calcular_costo()
    costo = float(v.string_costo.get())
    precio = round(obtener_tarifa() * precio_usd, 2)

    return {"nombre": nombre, "costo": costo, "precio_usd": precio_usd,
            "precio": precio, "categoria": categoria, "insumos": insumos}


def cargar_producto(v, codigo):
    filas = db_select(
        f"SELECT `Nombre`, `Costo`, `PrecioUsd`, `Categoria`, {COLUMNAS_INSUMOS} FROM `productos` WHERE `Codigo` = %s", (codigo,))
    if not filas:
        return
    fila = filas[0]
    v.texto_nombre.insert(0, fila[0])
    v.string_costo.set(fmt(fila[1]))
    v.texto_precio.insert(0, fmt(fila[2]))
    v.texto_categoria.set(fila[3])

    for i in range(10):
        codigo_insumo = fila[4 + 2 * i]
        cantidad = fila[5 + 2 * i]
        if codigo_insumo != 0:
            v.ins[i].insert(0, codigo_insumo)
            um = db_select("SELECT `U/M` FROM `insumos` WHERE `Codigo` = %s", (codigo_insumo,))
            if um:
                v.um[i].set(um[0][0])
        if cantidad != 0:
            v.cant[i].insert(0, fmt(cantidad))

    v.actualizar_cp()


# **********************************************************************************
# ******************************** Nuevo Producto **********************************
# **********************************************************************************

class NuevoProducto:
    def __init__(self):
        self = crear_ventana("NuevoProducto", "Nuevo Producto", 1000, 600)
        poner_fondo(self, "fondo2.jpg", 600, 200)
        crear_formulario_producto(self)

        def agregar_producto():
            datos = leer_formulario_producto(self)
            if datos is None:
                return
            if not messagebox.askokcancel("Confirmar", "Se va a agregar el producto"):
                return
            try:
                fila = db_select("SELECT MAX(Codigo) FROM `productos`;")
                maximo = fila[0][0]
                id_producto = 1 if maximo is None else maximo + 1

                db_exec(SQL_INSERT_PRODUCTO,
                        (id_producto, datos["nombre"], datos["costo"], datos["precio_usd"],
                         datos["precio"], datos["categoria"], *datos["insumos"]))
                self.destroy()
            except Exception:
                messagebox.showerror("Error", "No se pudo agregar el producto")

        CTkButton(self, text="Agregar Producto", command=agregar_producto, width=300, height=50).place(x=350, y=500)


# **********************************************************************************
# ****************************** Modificar Producto ********************************
# **********************************************************************************

class ModificarProducto:
    def __init__(self):
        self = crear_ventana("ModificarProducto", "Productos", 600, 600)

        buscador = CTkEntry(self, placeholder_text="Buscar por Nombre ...")
        buscador.pack(pady=10)

        tabla = crear_tabla(self, ("Nombre", "Costo", "Precio", "Categoria"), (200, 100, 100, 200),
                            alto=20, solo_headings=True, ancho0=75, empaquetar=True)

        def llenar(event=None):
            tabla.delete(*tabla.get_children())
            filas = db_select(
                "SELECT `Codigo`, `Nombre`, ROUND(`Costo`, 4), ROUND(`Precio`, 2), `Categoria` FROM productos WHERE `Nombre` LIKE %s;",
                (f"%{buscador.get()}%",))
            for fila in filas:
                tabla.insert("", END, text=fila[0], values=fila[1:])

        buscador.bind("<KeyRelease>", llenar)
        llenar()

        def doble_click(event):
            seleccion = tabla.selection()
            if not seleccion:
                return
            codigo_producto = tabla.item(seleccion[0], "text")

            temp = crear_ventana("ProductoPopup", "Selección", 200, 200)

            def eliminar():
                if messagebox.askokcancel("Confirmar", "Vamos a eliminar el producto"):
                    try:
                        db_exec("DELETE FROM `productos` WHERE `Codigo` = %s", (codigo_producto,))
                    except Exception:
                        messagebox.showerror("Error", "No se pudo eliminar el producto")
                        return
                    llenar()
                    temp.destroy()

            CTkButton(temp, text="Eliminar", command=eliminar).pack(pady=20)

            def modificar():
                temp.destroy()
                vent1 = crear_ventana("FormModificarProducto", "Modificar Producto", 1000, 600)
                poner_fondo(vent1, "fondo2.jpg", 600, 200)
                crear_formulario_producto(vent1)
                cargar_producto(vent1, codigo_producto)

                def guardar():
                    datos = leer_formulario_producto(vent1)
                    if datos is None:
                        return
                    if not messagebox.askokcancel("Confirmar", "Se va a modificar el producto"):
                        return
                    try:
                        db_exec(SQL_UPDATE_PRODUCTO,
                                (datos["nombre"], datos["costo"], datos["precio_usd"], datos["precio"],
                                 datos["categoria"], *datos["insumos"], codigo_producto))
                    except Exception:
                        messagebox.showerror("Error", "No se pudo modificar el producto")
                        return
                    try:
                        llenar()
                    except Exception:
                        pass
                    vent1.destroy()

                CTkButton(vent1, text="Modificar Producto", command=guardar, width=300, height=50).place(x=350, y=500)

            CTkButton(temp, text="Modificar", command=modificar).pack(pady=20)

        tabla.bind("<Double-1>", doble_click)


# **********************************************************************************
# ************************************ Tarifa **************************************
# **********************************************************************************

class Tarifa:
    def __init__(self):
        self = crear_ventana("Tarifa", "Tarifa", 300, 200)
        poner_fondo(self, "fondo1.jpg", 300, 200)

        CTkLabel(self, text="Precio del Usd en este momento", font=("Times New Roman", 14)).place(x=40, y=20)

        texto_usd = CTkEntry(self, placeholder_text="Precio del Usd ...", width=200)
        texto_usd.place(x=50, y=80)
        try:
            texto_usd.insert(0, fmt(obtener_tarifa()))
        except Exception:
            pass

        def aceptar():
            try:
                valor = a_decimal(texto_usd.get())
                if texto_usd.get().strip() == "" or valor < 0 or valor != valor or valor == float("inf"):
                    raise ValueError("invalido")
            except ValueError:
                messagebox.showerror("Error", "Escribe un precio valido para el Usd (un numero no negativo)")
                return

            if not messagebox.askokcancel(
                    "Confirmar",
                    f"La tarifa pasara a {fmt(valor)} y se recalcularan los precios de TODOS los productos.\n"
                    "Las ventas ya registradas no cambian."):
                return

            # la tarifa y los precios se actualizan juntos o no se actualiza nada
            conn = conectar()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM `Tarifa`")
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO `Tarifa` (`Usd`) VALUES (%s)", (valor,))
                else:
                    cursor.execute("UPDATE `Tarifa` SET `Usd` = %s", (valor,))
                cursor.execute("UPDATE `productos` SET `Precio` = ROUND(`PrecioUsd` * %s, 2)", (valor,))
                conn.commit()
            except Exception:
                conn.rollback()
                messagebox.showerror("Error", "No se pudo actualizar la tarifa")
                return
            finally:
                conn.close()

            messagebox.showinfo("Terminado", "Tarifa actualizada y precios recalculados")
            self.destroy()

        CTkButton(self, text="Aceptar", command=aceptar, width=200, height=30).place(x=50, y=140)


# **********************************************************************************
# ***********************************  Ventas **************************************
# **********************************************************************************

class Ventas:
    def __init__(self):
        self = crear_ventana("Ventas", "Ventas", 1000, 600)
        poner_fondo(self, "fondo.jpg", 1000, 600)

        CTkLabel(self, text="Productos").place(x=80, y=40)

        tabla = crear_tabla(self, ("Nombre", "Costo", "Precio", "Categoria"), (200, 100, 100, 200),
                            20, 100, 10, solo_headings=True)

        # solo se muestra Precio (ya calculado con la tarifa); PrecioUsd no aparece
        def llenar_ventas(event=None):
            tabla.delete(*tabla.get_children())
            filas = db_select(
                "SELECT `Codigo`, `Nombre`, ROUND(`Costo`, 4), ROUND(`Precio`, 2), `Categoria` FROM productos "
                "WHERE `Codigo` LIKE %s and `Nombre` LIKE %s;",
                (f"%{texto_buscador_codigo.get()}%", f"%{texto_buscador_nombre.get()}%"))
            for fila in filas:
                tabla.insert("", END, text=fila[0], values=fila[1:])

        CTkLabel(self, text="------------------------------ Buscador ------------------------------").place(x=650, y=80)

        texto_buscador_codigo = CTkEntry(self, placeholder_text="Buscar por codigo ...", width=250)
        texto_buscador_codigo.place(x=650, y=120)
        texto_buscador_codigo.bind("<KeyRelease>", llenar_ventas)

        texto_buscador_nombre = CTkEntry(self, placeholder_text="Buscar por nombre ...", width=250)
        texto_buscador_nombre.place(x=650, y=160)
        texto_buscador_nombre.bind("<KeyRelease>", llenar_ventas)

        llenar_ventas()

        # cuando demos 2ble click abriremos una ventana para hacer la venta o regalo
        def venta(event):
            seleccion = tabla.selection()
            if not seleccion:
                return
            codigo = tabla.item(seleccion[0], "text")
            nombre = tabla.item(seleccion[0], "values")[0]

            temp = crear_ventana("VentaPopup", "Vender", 200, 400)

            texto_concepto = CTkEntry(temp, placeholder_text="Concepto del Regalo ...")

            opcion = IntVar(value=1)

            def radio_select():
                if opcion.get() == 1:
                    texto_concepto.pack_forget()
                elif opcion.get() == 2:
                    texto_concepto.pack(pady=5)

            CTkRadioButton(temp, text="Vender", command=radio_select, variable=opcion, value=1).pack(pady=10)
            CTkRadioButton(temp, text="Regalar", command=radio_select, variable=opcion, value=2).pack(pady=10)

            texto_cantidad = CTkEntry(temp, placeholder_text="Cantidad ...")
            texto_cantidad.pack(pady=5)

            texto_fecha = CTkEntry(temp, placeholder_text="Fecha ...")
            texto_fecha.pack(pady=5)
            texto_fecha.bind("<ButtonRelease-1>", lambda e: abrir_calendario(texto_fecha))

            def salida():
                try:
                    cantidad = int(texto_cantidad.get().strip())
                except ValueError:
                    cantidad = 0
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser un numero entero mayor que cero")
                    return

                fecha = texto_fecha.get().strip()
                if not fecha_valida(fecha):
                    messagebox.showerror("Error", "Selecciona una fecha valida")
                    return

                es_venta = opcion.get() == 1
                accion = "vender" if es_venta else "regalar"
                if not messagebox.askokcancel("Confirmar", f"Vas a {accion} {cantidad} {nombre}"):
                    return

                try:
                    motivo = registrar_salida(es_venta, codigo, cantidad, fecha, texto_concepto.get())
                except Exception:
                    mensaje = "No se completo la venta" if es_venta else "No se completo el regalo"
                    messagebox.showerror("Error", mensaje + " \n Revise los datos introducidos")
                    return

                if motivo:
                    messagebox.showerror("Error", motivo)
                    return

                llenar_ventas()
                temp.destroy()

            CTkButton(temp, text="Aceptar", command=salida).pack(pady=20, side="bottom")

        tabla.bind("<Double-1>", venta)


# **********************************************************************************
# ************************* Devoluciones (regalos y ventas) ************************
# **********************************************************************************

def ventana_devoluciones(clave, titulo, tabla_sql, ultima_col, x_tabla, x_fechas, x_buscador, texto_cancelar):
    v = crear_ventana(clave, titulo, 1000, 600)
    poner_fondo(v, "fondo4.jpg", 1000, 600)

    tabla = crear_tabla(v, ("Fecha", "Codigo", "Nombre", "Costo", "Precio", "Cantidad", ultima_col),
                        (100, 75, 200, 100, 100, 75, 200), x_tabla, 200, 11, solo_headings=True, texto0="Id")

    def llenar_tabla(event=None):
        try:
            tabla.delete(*tabla.get_children())
            filtros = ["`Codigo` LIKE %s", "`Nombre` LIKE %s"]
            params = [f"%{texto_buscador_codigo.get()}%", f"%{texto_buscador_nombre.get()}%"]
            if texto_fecha_inicial.get() != "" and texto_fecha_final.get() != "":
                filtros += ["`Fecha` >= %s", "`Fecha` < %s"]
                params += [texto_fecha_inicial.get(), texto_fecha_final.get()]
            sql = (f"SELECT `Id`, `Fecha`, `Codigo`, `Nombre`, ROUND(`Costo`, 4), ROUND(`Precio`, 2), `Cantidad`, `{ultima_col}` "
                   f"FROM `{tabla_sql}` WHERE " + " AND ".join(filtros) + " ORDER BY `Fecha` DESC")
            for fila in db_select(sql, tuple(params)):
                tabla.insert("", END, text=fila[0], values=fila[1:])
        except Exception:
            messagebox.showerror("Error", "No se pudo actualizar la tabla")

    CTkLabel(v, text="---------- Control de fechas ----------").place(x=x_fechas, y=50)

    texto_fecha_inicial = CTkEntry(v, placeholder_text="Fecha inicial ...")
    texto_fecha_inicial.place(x=x_fechas, y=90)
    CTkButton(v, text="...", command=lambda: abrir_calendario(texto_fecha_inicial, llenar_tabla),
              width=27, height=27).place(x=x_fechas + 150, y=90)

    texto_fecha_final = CTkEntry(v, placeholder_text="Fecha final ...")
    texto_fecha_final.place(x=x_fechas, y=130)
    CTkButton(v, text="...", command=lambda: abrir_calendario(texto_fecha_final, llenar_tabla),
              width=27, height=27).place(x=x_fechas + 150, y=130)

    CTkLabel(v, text="---------- Buscador ----------").place(x=x_buscador, y=50)

    texto_buscador_codigo = CTkEntry(v, placeholder_text="Buscar por codigo ...")
    texto_buscador_codigo.place(x=x_buscador, y=90)
    texto_buscador_codigo.bind("<KeyRelease>", llenar_tabla)

    texto_buscador_nombre = CTkEntry(v, placeholder_text="Buscar por nombre ...")
    texto_buscador_nombre.place(x=x_buscador, y=130)
    texto_buscador_nombre.bind("<KeyRelease>", llenar_tabla)

    llenar_tabla()

    # doble click: se devuelven los insumos al almacen y se borra el registro
    def devolver(event):
        seleccion = tabla.selection()
        if not seleccion:
            return
        id_registro = tabla.item(seleccion[0], "text")
        valores = tabla.item(seleccion[0], "values")

        if not messagebox.askokcancel("Confirmar", texto_cancelar):
            return

        conn = conectar()
        try:
            cursor = conn.cursor()
            cantidad = float(valores[5])
            for insumo, cant in insumos_de_producto(cursor, valores[1]):
                cursor.execute("UPDATE `insumos` SET `Cantidad` = `Cantidad` + %s WHERE `Codigo` = %s",
                               (cantidad * float(cant), insumo))
            cursor.execute(f"DELETE FROM `{tabla_sql}` WHERE `Id` = %s", (id_registro,))
            conn.commit()
        except Exception:
            conn.rollback()
            messagebox.showerror("Error", "Hubo problemas al eliminar el registro")
            return
        finally:
            conn.close()

        llenar_tabla()

    tabla.bind("<Double-1>", devolver)
    return v, tabla


class ControlRegalos:
    def __init__(self):
        ventana_devoluciones("ControlRegalos", "Devolucion Regalos", "regalos", "Concepto",
                             50, 50, 300, "Se va a cancelar este regalo")


class ControlVentas:
    def __init__(self):
        v, tabla = ventana_devoluciones("ControlVentas", "Devolucion Ventas", "salidas", "Categoria",
                                        100, 200, 600, "Se va a cancelar esta venta")

        def exportar_devolucion_excel():
            filas = tabla.get_children()
            if len(filas) == 0:
                messagebox.showwarning("Aviso", "No hay datos en la tabla para exportar")
                return

            # leemos los datos directamente del Treeview (lo que se ve en ese momento)
            datos = []
            for item in filas:
                valores = tabla.item(item, "values")
                datos.append({
                    "Id": tabla.item(item, "text"),
                    "Fecha": valores[0],
                    "Codigo": valores[1],
                    "Nombre": valores[2],
                    "Costo": valores[3],
                    "Precio": valores[4],
                    "Cantidad": valores[5],
                    "Categoria": valores[6],
                })

            try:
                df = pd.DataFrame(datos)

                carpeta = "D:/Condesa/respaldos"
                if not os.path.exists(carpeta):
                    os.makedirs(carpeta)

                nombre_archivo = f"informe_ventas_{fecha_actual}.xlsx"
                ruta_completa = os.path.join(carpeta, nombre_archivo)

                df.to_excel(ruta_completa, index=False)

                messagebox.showinfo("Éxito", f"Archivo creado exitosamente:\n{ruta_completa}")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el archivo:\n{str(e)}")

        CTkButton(v, text="Exportar", command=exportar_devolucion_excel).place(x=80, y=450)


# **********************************************************************************
# **********************************  Asociados ************************************
# **********************************************************************************

class Asociados:
    def __init__(self):
        self = crear_ventana("Asociados", "Gastos Asociados", 1000, 600)
        poner_fondo(self, "fondo3.jpg", 1000, 600)

        tabla = crear_tabla(self, ("Fecha", "Concepto", "Monto"), (100, 500, 100), 150, 60, 10,
                            solo_headings=True, texto0="Id")

        def llenar_tabla():
            tabla.delete(*tabla.get_children())
            for fila in db_select("SELECT `Id`, `Fecha`, `Concepto`, ROUND(`Monto`, 2) FROM `asociados` ORDER BY `Fecha` DESC LIMIT 50"):
                tabla.insert("", END, text=fila[0], values=fila[1:])

        llenar_tabla()

        def eliminar(event):
            seleccion = tabla.selection()
            if not seleccion:
                return
            id_asociado = tabla.item(seleccion[0], "text")
            if messagebox.askokcancel("Confirmar", "Se va a eliminar el gasto asociado"):
                db_exec("DELETE FROM `asociados` WHERE `Id` = %s", (id_asociado,))
                llenar_tabla()

        tabla.bind("<Double-1>", eliminar)

        def agregar():
            temp = crear_ventana("AsociadoPopup", "Agregar", 300, 300)

            texto_fecha = CTkEntry(temp, placeholder_text="Fecha ...")
            texto_fecha.pack(pady=5)
            texto_fecha.bind("<ButtonRelease-1>", lambda e: abrir_calendario(texto_fecha))

            texto_concepto = CTkEntry(temp, placeholder_text="Concepto ...", width=300)
            texto_concepto.pack(pady=5)

            texto_monto = CTkEntry(temp, placeholder_text="Monto ...", width=300)
            texto_monto.pack(pady=5)

            def aceptar_asociado():
                fecha = texto_fecha.get().strip()
                if not fecha_valida(fecha):
                    messagebox.showerror("Error", "Selecciona una fecha valida")
                    return
                try:
                    monto = a_decimal(texto_monto.get())
                except ValueError:
                    messagebox.showerror("Error", "El monto debe ser un numero")
                    return
                if not messagebox.askokcancel("Confirmar", "Se va a agregar el gasto"):
                    return
                try:
                    fila = db_select("SELECT MAX(Id) FROM `asociados`;")
                    maximo = fila[0][0]
                    id_asociado = 1 if maximo is None else maximo + 1
                    db_exec("INSERT INTO `asociados`(`Id`, `Fecha`, `Concepto`, `Monto`) VALUES (%s, %s, %s, %s)",
                            (id_asociado, fecha, texto_concepto.get(), monto))
                except Exception:
                    messagebox.showerror("Error", "No se pudo agregar el gasto asociado")
                    return
                try:
                    llenar_tabla()
                except Exception:
                    pass
                temp.destroy()

            CTkButton(temp, text="Aceptar Asociado", command=aceptar_asociado).pack(pady=10)

        CTkButton(self, text="Agregar", command=agregar, width=500, height=50).place(x=270, y=400)


# **********************************************************************************
# ****************************  Consulta Totales ***********************************
# **********************************************************************************

class ConsultaTotales:
    def __init__(self):
        self = crear_ventana("ConsultaTotales", "Consulta Totales", 1000, 600)
        poner_fondo(self, "fondo.jpg", 1000, 600)

        CTkLabel(self, text="---------- Informaciones ----------").place(x=500, y=60)

        etiquetas = ["Total Ingresos: ", "Total Gastos Asociados: ", "Total Costos: ", "Total Ganancias: ",
                     "Producto Mas Vendido: ", "Producto Menos Vendido: ",
                     "Producto Mas Ganancia: ", "Producto Menos Ganancia: "]
        variables = []
        for i, texto in enumerate(etiquetas):
            y = 100 + 40 * i
            CTkLabel(self, text=texto).place(x=500, y=y)
            variable = StringVar(value="0")
            CTkLabel(self, textvariable=variable).place(x=700, y=y)
            variables.append(variable)
        v_ingresos, v_gastos, v_costos, v_ganancia, v_mas, v_menos, v_mas_gan, v_menos_gan = variables

        def producto_extremo(expresion, orden, fi, ff):
            filas = db_select(
                f"SELECT Codigo, Nombre, {expresion} AS total FROM salidas WHERE Fecha BETWEEN %s AND %s "
                f"GROUP BY Codigo, Nombre ORDER BY total {orden} LIMIT 1;", (fi, ff))
            if filas:
                return f"{filas[0][1]} ({round(float(filas[0][2]), 2)})"
            return " (0)"

        # ahora vamos a generar la funcion para mostrar los datos
        def consulta():
            fi = texto_fecha_inicial.get()
            ff = texto_fecha_final.get()
            if fi == "" or ff == "":
                return

            fila = db_select(
                "SELECT SUM(`Precio` * `Cantidad`), SUM(`Costo` * `Cantidad`) FROM `salidas` WHERE `Fecha` >= %s and `Fecha` < %s",
                (fi, ff))[0]
            ingresos = float(fila[0] or 0)
            costos = float(fila[1] or 0)

            fila = db_select("SELECT SUM(`Monto`) FROM `asociados` WHERE `Fecha` >= %s and `Fecha` < %s", (fi, ff))[0]
            asociados = float(fila[0] or 0)

            v_ingresos.set(round(ingresos, 2))
            v_gastos.set(round(asociados, 2))
            v_costos.set(round(costos, 2))
            v_ganancia.set(round(ingresos - asociados - costos, 2))

            v_mas.set(producto_extremo("SUM(Cantidad)", "DESC", fi, ff))
            v_menos.set(producto_extremo("SUM(Cantidad)", "ASC", fi, ff))
            v_mas_gan.set(producto_extremo("SUM((Precio - Costo) * Cantidad)", "DESC", fi, ff))
            v_menos_gan.set(producto_extremo("SUM((Precio - Costo) * Cantidad)", "ASC", fi, ff))

        CTkLabel(self, text="---------- Control de fechas ----------").place(x=50, y=50)

        texto_fecha_inicial = CTkEntry(self, placeholder_text="Fecha inicial ...")
        texto_fecha_inicial.place(x=50, y=90)
        CTkButton(self, text="...", command=lambda: abrir_calendario(texto_fecha_inicial, consulta),
                  width=27, height=27).place(x=200, y=90)

        texto_fecha_final = CTkEntry(self, placeholder_text="Fecha final ...")
        texto_fecha_final.place(x=50, y=130)
        CTkButton(self, text="...", command=lambda: abrir_calendario(texto_fecha_final, consulta),
                  width=27, height=27).place(x=200, y=130)

        def trayectoria_insumos():
            fi = texto_fecha_inicial.get()
            ff = texto_fecha_final.get()
            if fi == "" or ff == "":
                messagebox.showerror("Error", "Debes seleccionar la fecha inicial y la fecha final")
                return

            try:
                # ********** todos los insumos **********
                insumos = [{"codigo": f[0], "nombre": f[1], "costo": f[2], "cant_final": float(f[3]), "um": f[4]}
                           for f in db_select("SELECT `Codigo`, `Nombre`, `Costo`, `Cantidad`, `U/M` FROM `insumos` ORDER BY `Codigo`;")]

                # ********** entradas del periodo, por insumo **********
                entradas = {}
                for codigo, total in db_select(
                        "SELECT `Codigo`, SUM(`Cantidad`) FROM `entradas` WHERE `Fecha` >= %s AND `Fecha` < %s GROUP BY `Codigo`", (fi, ff)):
                    entradas[int(codigo)] = float(total or 0)

                # ********** productos vendidos o regalados en el periodo (las salidas guardan el codigo del PRODUCTO) **********
                productos_salidos = {}
                for tabla_origen in ("salidas", "regalos"):
                    for codigo, total in db_select(
                            f"SELECT `Codigo`, SUM(`Cantidad`) FROM `{tabla_origen}` WHERE `Fecha` >= %s AND `Fecha` < %s GROUP BY `Codigo`", (fi, ff)):
                        try:
                            clave = int(codigo)
                        except (TypeError, ValueError):
                            continue
                        productos_salidos[clave] = productos_salidos.get(clave, 0) + float(total or 0)

                # ********** cuanto de cada insumo se uso en esos productos **********
                insumos_usados = {}
                conn = conectar()
                try:
                    cursor = conn.cursor()
                    for codigo_producto, cantidad_salida in productos_salidos.items():
                        for insumo, cant in insumos_de_producto(cursor, codigo_producto):
                            insumos_usados[insumo] = insumos_usados.get(insumo, 0) + cantidad_salida * float(cant)
                finally:
                    conn.close()

                for insumo in insumos:
                    cant_entro = entradas.get(insumo["codigo"], 0)
                    cant_salio = insumos_usados.get(insumo["codigo"], 0)
                    # cant final real - entro + salio  = cant inicial
                    insumo["cant_entro"] = cant_entro
                    insumo["cant_salio"] = cant_salio
                    insumo["cant_inicial"] = insumo["cant_final"] - cant_entro + cant_salio

                # primero los que tienen movimiento, al final los que estan en cero
                insumos.sort(key=lambda x: (x["cant_entro"] == 0 and x["cant_salio"] == 0))

                datos = []
                for insumo in insumos:
                    datos.append({
                        "Codigo": insumo["codigo"],
                        "Nombre": insumo["nombre"],
                        "Costo": insumo["costo"],
                        "U/M": insumo["um"],
                        "Cant Inicial": insumo["cant_inicial"],
                        "Cant Entro": insumo["cant_entro"],
                        "Cant Salió": insumo["cant_salio"],
                        "Cant Final": insumo["cant_final"]
                    })

                df = pd.DataFrame(datos)

                carpeta_respaldo = "D:/condesa/respaldos"
                if not os.path.exists(carpeta_respaldo):
                    os.makedirs(carpeta_respaldo)

                nombre_archivo = f"TI {fi}-{ff}.xlsx"
                ruta_completa = os.path.join(carpeta_respaldo, nombre_archivo)

                df.to_excel(ruta_completa, index=False)

                messagebox.showinfo("Éxito", f"Archivo creado exitosamente:\n{ruta_completa}")

            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema al generar la trayectoria:\n{str(e)}")

        CTkButton(self, text="Trayectoria Insumos", command=trayectoria_insumos).place(x=50, y=200)


if __name__ == "__main__":
    autenticacion = Autenticacion()
    autenticacion.mainloop()
