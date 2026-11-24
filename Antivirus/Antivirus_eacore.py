# -*- coding: utf-8 -*-
"""
Herramienta de desinfeccion: EACoreServer
Solo para Windows. Ejecutar como Administrador.

Boton 1 - Desinfeccion: detiene EACoreServer.exe y borra C:\\ProgramData\\EACoreService
Boton 2 - USB: en todas las memorias removibles, rescata el contenido oculto en
            <unidad>:\\Kaspersky\\Usb Drive, borra la carpeta "3.0" y elimina "Kaspersky".
"""

import ctypes
import os
import shutil
import stat
import subprocess
import sys
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

# ---------------- Configuracion ----------------
PROCESO = "EACoreServer.exe"
CARPETA_VIRUS = r"C:\ProgramData\EACoreService"
NOMBRE_KASPERSKY = "Kaspersky"
NOMBRE_USB_DRIVE = "usb drive"          # se compara sin mayusculas ni caracteres invisibles
CARPETA_A_BORRAR = "3.0"
CARPETA_RECUPERADOS = "Archivos recuperados"
SUFIJO_DUPLICADO = " (recuperado)"

DRIVE_REMOVABLE = 2
FILE_ATTRIBUTE_NORMAL = 0x80
# Caracteres invisibles que el virus puede usar al final de los nombres
INVISIBLES = "\u200e\u200f\u200b\u200c\u200d\u202a\u202b\u202c\u202d\u202e\u2060\ufeff"


# ---------------- Utilidades ----------------
def es_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def ext(path):
    """Ruta con prefijo \\\\?\\ para soportar nombres con caracteres raros."""
    path = os.path.abspath(path)
    if path.startswith("\\\\?\\"):
        return path
    return "\\\\?\\" + path


def limpiar_nombre(nombre):
    for c in INVISIBLES:
        nombre = nombre.replace(c, "")
    return nombre.strip().lower()


def buscar_hijo(carpeta, nombre_objetivo):
    """Devuelve el nombre real (con posibles caracteres ocultos) o None."""
    try:
        for entrada in os.scandir(ext(carpeta)):
            if limpiar_nombre(entrada.name) == nombre_objetivo.lower():
                return entrada.name
    except OSError:
        pass
    return None


def quitar_atributos(ruta):
    """Quita oculto/sistema/solo lectura de una ruta y de todo lo que contiene."""
    k32 = ctypes.windll.kernel32
    k32.SetFileAttributesW(ext(ruta), FILE_ATTRIBUTE_NORMAL)
    if os.path.isdir(ext(ruta)):
        for raiz, dirs, archivos in os.walk(ext(ruta)):
            for n in dirs + archivos:
                k32.SetFileAttributesW(os.path.join(raiz, n), FILE_ATTRIBUTE_NORMAL)


def _onerror(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        raise


def borrar_carpeta(ruta):
    quitar_atributos(ruta)
    shutil.rmtree(ext(ruta), onerror=_onerror)


def nombre_libre(destino_dir, nombre):
    """Si el nombre ya existe en destino, agrega ' (recuperado)' (y un numero si hace falta)."""
    if not os.path.exists(os.path.join(destino_dir, nombre)):
        return nombre
    base, extension = os.path.splitext(nombre)
    candidato = f"{base}{SUFIJO_DUPLICADO}{extension}"
    n = 2
    while os.path.exists(os.path.join(destino_dir, candidato)):
        candidato = f"{base}{SUFIJO_DUPLICADO} {n}{extension}"
        n += 1
    return candidato


def etiqueta_volumen(raiz):
    """Nombre (etiqueta) que tiene la memoria, o '' si no tiene."""
    buf = ctypes.create_unicode_buffer(261)
    ok = ctypes.windll.kernel32.GetVolumeInformationW(raiz, buf, 261, None, None, None, None, 0)
    return buf.value if ok else ""


def unidades_removibles():
    unidades = []
    mascara = ctypes.windll.kernel32.GetLogicalDrives()
    for i in range(26):
        if mascara & (1 << i):
            raiz = f"{chr(65 + i)}:\\"
            if ctypes.windll.kernel32.GetDriveTypeW(raiz) == DRIVE_REMOVABLE:
                unidades.append(raiz)
    return unidades


# ---------------- Fase 1: Desinfeccion ----------------
def desinfeccion(log):
    log("=== DESINFECCION ===")

    log(f"Deteniendo el proceso {PROCESO}...")
    r = subprocess.run(
        ["taskkill", "/F", "/T", "/IM", PROCESO],
        capture_output=True, text=True, creationflags=0x08000000,
    )
    salida = (r.stdout + r.stderr).strip()
    if r.returncode == 0:
        log("  Proceso detenido.")
        time.sleep(1.5)
    else:
        log("  El proceso no estaba en ejecucion (o no se pudo detener): " + salida)

    if not os.path.exists(CARPETA_VIRUS):
        log(f"La carpeta {CARPETA_VIRUS} no existe. Nada que borrar.")
        log("=== FIN ===")
        return

    log(f"Borrando {CARPETA_VIRUS} ...")
    for intento in range(1, 4):
        try:
            borrar_carpeta(CARPETA_VIRUS)
            break
        except Exception as e:
            log(f"  Intento {intento} fallido: {e}")
            time.sleep(2)

    if os.path.exists(CARPETA_VIRUS):
        log("  NO se pudo borrar por completo. Reinicia el equipo en modo seguro y repite.")
    else:
        log("  Carpeta eliminada correctamente.")
    log("=== FIN ===")


# ---------------- Fase 2: USB ----------------
def limpiar_usb(raiz, log):
    log(f"--- Unidad {raiz} ---")
    etiqueta = etiqueta_volumen(raiz)
    kasp_nombre = buscar_hijo(raiz, NOMBRE_KASPERSKY)
    if not kasp_nombre:
        log("  No se encontro la carpeta Kaspersky. Unidad omitida.")
        return
    kasp = os.path.join(raiz, kasp_nombre)

    usb_nombre = buscar_hijo(kasp, NOMBRE_USB_DRIVE)
    if not usb_nombre:
        log("  No se encontro la subcarpeta 'Usb Drive'. Unidad omitida.")
        return
    usb = os.path.join(kasp, usb_nombre)

    # 1. Borrar la carpeta 3.0
    n30 = buscar_hijo(usb, CARPETA_A_BORRAR)
    if n30:
        try:
            borrar_carpeta(os.path.join(usb, n30))
            log(f"  Carpeta '{CARPETA_A_BORRAR}' eliminada.")
        except Exception as e:
            log(f"  No se pudo borrar '{CARPETA_A_BORRAR}': {e}")

    # 2. Crear carpeta de recuperados
    destino = os.path.join(raiz, CARPETA_RECUPERADOS)
    os.makedirs(ext(destino), exist_ok=True)

    # 3. Mover contenido y quitar atributos
    movidos, fallidos = 0, 0
    for entrada in list(os.scandir(ext(usb))):
        origen = os.path.join(usb, entrada.name)
        try:
            quitar_atributos(origen)
            nuevo = nombre_libre(ext(destino), entrada.name)
            shutil.move(ext(origen), os.path.join(ext(destino), nuevo))
            movidos += 1
        except Exception as e:
            fallidos += 1
            log(f"  Error moviendo '{entrada.name}': {e}")
    log(f"  Elementos recuperados: {movidos}" + (f" | con error: {fallidos}" if fallidos else ""))

    # 4. Borrar la carpeta Kaspersky completa (solo si todo se rescato sin errores)
    if fallidos == 0:
        try:
            borrar_carpeta(kasp)
            log("  Carpeta Kaspersky eliminada.")
        except Exception as e:
            log(f"  No se pudo eliminar Kaspersky: {e}")
        # 5. Dejar en la raiz solo 'Archivos recuperados'
        limpiar_raiz(raiz, etiqueta, destino, log)
    else:
        log("  Hubo errores: Kaspersky NO se elimino para no perder archivos.")


def limpiar_raiz(raiz, etiqueta, destino, log):
    """Borra TODO lo que haya en la raiz excepto 'Archivos recuperados' y las
    carpetas propias de Windows (incluye el archivo con el nombre de la memoria)."""
    ignorar = {"system volume information", "$recycle.bin",
               limpiar_nombre(CARPETA_RECUPERADOS)}
    for entrada in list(os.scandir(ext(raiz))):
        if limpiar_nombre(entrada.name) in ignorar:
            continue
        ruta = os.path.join(raiz, entrada.name)
        try:
            quitar_atributos(ruta)
            if entrada.is_dir(follow_symlinks=False):
                borrar_carpeta(ruta)
            else:
                os.remove(ext(ruta))
            log(f"  '{entrada.name}' eliminado de la raiz.")
        except Exception as e:
            log(f"  No se pudo borrar '{entrada.name}' de la raiz: {e}")


def usb(log):
    log("=== USB ===")
    unidades = unidades_removibles()
    if not unidades:
        log("No hay memorias removibles conectadas.")
        log("=== FIN ===")
        return
    log("Unidades detectadas: " + ", ".join(unidades))
    for raiz in unidades:
        try:
            limpiar_usb(raiz, log)
        except Exception as e:
            log(f"  Error inesperado en {raiz}: {e}")
    log("=== FIN ===")


# ---------------- Interfaz (lobby) ----------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Antivirus EACoreServer")
        root.geometry("620x440")
        root.resizable(False, False)

        tk.Label(root, text="Herramienta de limpieza EACoreServer",
                 font=("Segoe UI", 14, "bold")).pack(pady=(14, 8))

        marco = tk.Frame(root)
        marco.pack(pady=4)
        self.b1 = tk.Button(marco, text="Desinfección", width=22, height=2,
                            font=("Segoe UI", 11), command=self.on_desinfeccion)
        self.b1.grid(row=0, column=0, padx=10)
        self.b2 = tk.Button(marco, text="Usb", width=22, height=2,
                            font=("Segoe UI", 11), command=self.on_usb)
        self.b2.grid(row=0, column=1, padx=10)

        self.salida = scrolledtext.ScrolledText(root, height=15, state="disabled",
                                                font=("Consolas", 9))
        self.salida.pack(fill="both", expand=True, padx=12, pady=12)

        if not es_admin():
            self.log("AVISO: no estas ejecutando como Administrador. "
                     "La desinfeccion puede fallar. Cierra y abre como administrador.")

    def log(self, texto):
        self.salida.configure(state="normal")
        self.salida.insert("end", texto + "\n")
        self.salida.see("end")
        self.salida.configure(state="disabled")
        self.root.update()

    def _correr(self, funcion, pregunta):
        if not messagebox.askyesno("Confirmar", pregunta):
            return
        self.b1.configure(state="disabled")
        self.b2.configure(state="disabled")
        try:
            funcion(self.log)
        finally:
            self.b1.configure(state="normal")
            self.b2.configure(state="normal")

    def on_desinfeccion(self):
        self._correr(
            desinfeccion,
            f"Se detendra {PROCESO} y se borrara por completo:\n{CARPETA_VIRUS}\n\n¿Continuar?",
        )

    def on_usb(self):
        self._correr(
            usb,
            "Se limpiaran TODAS las memorias removibles conectadas.\n"
            "El contenido oculto se movera a 'Archivos recuperados'.\n\n¿Continuar?",
        )


if __name__ == "__main__":
    if os.name != "nt":
        print("Este programa solo funciona en Windows.")
        sys.exit(1)
    ventana = tk.Tk()
    App(ventana)
    ventana.mainloop()