"""
Eliminador de Virus - Fase 1: Eliminación del virus EACoreServer
==================================================================

Aplicación de escritorio (customtkinter) que detecta y elimina el virus
"EACoreServer", alojado dentro de la carpeta:

    C:\\ProgramData\\EACoreService

Funcionamiento de la Fase 1:
    1. Busca si la carpeta "EACoreService" existe dentro de C:\\ProgramData.
    2. Si existe, verifica si dentro de ella está el archivo del virus
       "EACoreServer".
    3. Si el virus está presente:
         - Notifica al usuario con el detalle de la ubicación.
         - Habilita el botón "Eliminar virus" para que el usuario acepte.
         - Al aceptar, elimina la carpeta completa "EACoreService".
    4. Si no hay virus, informa que no se detectó ninguna amenaza.

Uso:
    Requiere Python 3.8+ y la librería customtkinter:
        pip install customtkinter

    El usuario debe ejecutar el programa como Administrador
    (clic derecho -> Ejecutar como administrador) para que pueda borrar
    archivos de C:\\ProgramData:
        python eliminador_virus.py
"""

import os
import shutil
import ctypes
import sys
import threading
import time

import customtkinter as ctk


# ---------------------------------------------------------------------------
# Atributos de archivo en Windows (oculto / sistema / solo lectura)
# ---------------------------------------------------------------------------
# La carpeta del virus tiene los atributos Oculto + Sistema, por eso no se
# ve con la casilla normal de "mostrar archivos ocultos" y solo aparece
# cuando se desmarca "ocultar archivos protegidos del sistema operativo".
#
# Windows protege los archivos con atributo "sistema" frente al borrado, así
# que antes de eliminar la carpeta hay que quitarle esos atributos con
# SetFileAttributesW (equivalente a `attrib -h -s /S /D`).

FILE_ATTRIBUTE_READONLY = 0x00000001
FILE_ATTRIBUTE_HIDDEN = 0x00000002
FILE_ATTRIBUTE_SYSTEM = 0x00000004
INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF


def get_file_attributes(path):
    """Devuelve los atributos (int) de un archivo/carpeta, o None si no aplica."""
    try:
        return ctypes.windll.kernel32.GetFileAttributesW(path)
    except (AttributeError, OSError):
        return None


def describe_attributes(attrs):
    """Convierte la máscara de atributos en un texto legible."""
    if attrs is None or attrs == INVALID_FILE_ATTRIBUTES:
        return "desconocido"
    flags = []
    if attrs & FILE_ATTRIBUTE_READONLY:
        flags.append("solo lectura")
    if attrs & FILE_ATTRIBUTE_HIDDEN:
        flags.append("oculto")
    if attrs & FILE_ATTRIBUTE_SYSTEM:
        flags.append("sistema")
    return ", ".join(flags) if flags else "normal"


def clear_hidden_system_attrs(path):
    """
    Quita los atributos oculto, sistema y solo lectura de un archivo/carpeta.

    Devuelve True si se pudo modificar (o si no aplicaba), False si falló.
    """
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(path)
        if attrs == INVALID_FILE_ATTRIBUTES or attrs is None:
            return False
        # Limpiar los bits HIDDEN, SYSTEM y READONLY (máscara 0x7).
        new_attrs = attrs & ~0x7
        if new_attrs == attrs:
            return True  # Ya no tenía esos atributos, nada que hacer.
        ok = ctypes.windll.kernel32.SetFileAttributesW(path, new_attrs)
        return ok != 0
    except (AttributeError, OSError):
        return False


# ---------------------------------------------------------------------------
# Configuración de la amenaza
# ---------------------------------------------------------------------------

# Carpeta raíz donde vive el virus.
PROGRAM_DATA_PATH = os.environ.get("PROGRAMDATA", r"C:\ProgramData")

# Carpeta que contiene al virus (se elimina por completo en la Fase 1).
VIRUS_FOLDER_NAME = "EACoreService"
VIRUS_FOLDER_PATH = os.path.join(PROGRAM_DATA_PATH, VIRUS_FOLDER_NAME)

# Archivo del virus dentro de la carpeta anterior.
VIRUS_FILE_NAME = "EACoreServer"
VIRUS_FILE_PATH = os.path.join(VIRUS_FOLDER_PATH, VIRUS_FILE_NAME)


# ---------------------------------------------------------------------------
# Apariencia de la ventana
# ---------------------------------------------------------------------------

ctk.set_appearance_mode("dark")        # dark / light / system
ctk.set_default_color_theme("blue")    # blue / green / dark-blue

WINDOW_TITLE = "Eliminador de Virus - EACoreServer"
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 520


class EliminadorVirusApp(ctk.CTk):
    """Ventana principal del eliminador de virus (Fase 1)."""

    def __init__(self):
        super().__init__()

        # --- Configuración básica de la ventana -----------------------------
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.center_window()

        # --- Estado interno -------------------------------------------------
        self.virus_found = False
        self.folder_exists = False

        # --- Construcción de la interfaz ------------------------------------
        self._build_ui()

        # --- Lanzar la verificación apenas se abre la ventana --------------
        # Se hace en un hilo para no congelar la interfaz mientras se revisa
        # el disco.
        self.after(200, self._start_scan_async)

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def _build_ui(self):
        # Título principal
        self.title_label = ctk.CTkLabel(
            self,
            text="Eliminador de Virus",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        self.title_label.pack(pady=(30, 4))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Detección y eliminación de EACoreServer",
            font=ctk.CTkFont(size=14),
            text_color="#9aa4b2",
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Tarjeta de estado
        self.status_frame = ctk.CTkFrame(self, corner_radius=12)
        self.status_frame.pack(fill="x", padx=40, pady=(0, 16))

        self.status_title = ctk.CTkLabel(
            self.status_frame,
            text="Estado:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )
        self.status_title.pack(anchor="w", padx=16, pady=(14, 2))

        self.status_value = ctk.CTkLabel(
            self.status_frame,
            text="Buscando el virus...",
            font=ctk.CTkFont(size=14),
            anchor="w",
            wraplength=520,
            justify="left",
        )
        self.status_value.pack(anchor="w", padx=16, pady=(0, 14))

        # Detalle de la ubicación detectada
        self.detail_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#7d8794",
            wraplength=540,
            justify="left",
            anchor="w",
        )
        self.detail_label.pack(fill="x", padx=40, pady=(0, 16))

        # Botón para eliminar (deshabilitado hasta detectar el virus)
        self.delete_button = ctk.CTkButton(
            self,
            text="Eliminar virus",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=44,
            state="disabled",
            command=self._on_delete_clicked,
        )
        self.delete_button.pack(pady=(4, 12))

        # Botón para volver a analizar
        self.rescan_button = ctk.CTkButton(
            self,
            text="Volver a analizar",
            font=ctk.CTkFont(size=13),
            height=36,
            fg_color="transparent",
            border_width=1,
            command=self._on_rescan_clicked,
        )
        self.rescan_button.pack(pady=(0, 18))

        # Consola / registro de acciones (parte inferior)
        self.log_label = ctk.CTkLabel(
            self,
            text="Registro:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
            text_color="#9aa4b2",
        )
        self.log_label.pack(fill="x", padx=40, pady=(0, 2))

        self.log_textbox = ctk.CTkTextbox(
            self,
            height=110,
            font=ctk.CTkFont(size=12),
            state="disabled",
            wrap="word",
        )
        self.log_textbox.pack(fill="both", expand=True, padx=40, pady=(0, 24))

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def center_window(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - WINDOW_WIDTH) // 2
        y = (sh - WINDOW_HEIGHT) // 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def log(self, message):
        """Agrega una línea al registro de acciones con marca de tiempo."""
        timestamp = time.strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", line)
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def set_status(self, value, color=None):
        self.status_value.configure(text=value)
        if color is not None:
            self.status_value.configure(text_color=color)

    # ------------------------------------------------------------------
    # Verificación (Fase 1 - detección)
    # ------------------------------------------------------------------
    def _start_scan_async(self):
        """Lanza el escaneo en un hilo para no bloquear la interfaz."""
        threading.Thread(target=self._scan, daemon=True).start()

    def _scan(self):
        """Busca la carpeta del virus y el archivo del virus dentro de ella."""
        # Limpieza visual de un escaneo anterior
        self.folder_exists = False
        self.virus_found = False
        self.delete_button.configure(state="disabled")
        self.set_status("Buscando el virus...", color="#9aa4b2")
        self.detail_label.configure(text="")
        self.log("Iniciando análisis del sistema...")

        # Pequeña pausa para que la UI muestre el estado "buscando"
        time.sleep(0.4)

        self.log(f"Carpeta raíz de búsqueda: {PROGRAM_DATA_PATH}")
        self.log(f"Carpeta objetivo: {VIRUS_FOLDER_PATH}")

        # 1) ¿Existe la carpeta EACoreService?
        if os.path.isdir(VIRUS_FOLDER_PATH):
            self.folder_exists = True
            self.log("✔ Carpeta 'EACoreService' encontrada en C:\\ProgramData.")

            # Comprobar y reportar atributos oculto/sistema.
            attrs = get_file_attributes(VIRUS_FOLDER_PATH)
            attr_desc = describe_attributes(attrs)
            self.log(f"Atributos de la carpeta: {attr_desc}")
            if attrs is not None and attrs != INVALID_FILE_ATTRIBUTES:
                if attrs & FILE_ATTRIBUTE_SYSTEM:
                    self.log("La carpeta está marcada como 'protegida del "
                             "sistema' (por eso no se ve con la casilla "
                             "normal de ocultos). Se quitarán los atributos "
                             "antes de borrar.")

            # 2) ¿Está el archivo del virus dentro de ella?
            if os.path.exists(VIRUS_FILE_PATH):
                self.virus_found = True
                size = self._human_size(self._path_size(VIRUS_FILE_PATH))
                self.log(f"⚠ Virus 'EACoreServer' detectado ({size}).")
                self._notify_virus_found(size, attr_desc)
            else:
                # La carpeta existe pero el archivo del virus no está.
                self.log("La carpeta existe pero el archivo 'EACoreServer' no "
                         "se encontró dentro de ella.")
                self._notify_no_virus(
                    detalle=("Se encontró la carpeta 'EACoreService', pero el "
                             "archivo del virus 'EACoreServer' no está dentro "
                             "de ella. No hay nada que eliminar.")
                )
        else:
            self.log("La carpeta 'EACoreService' no existe en C:\\ProgramData.")
            self._notify_no_virus()

    def _notify_virus_found(self, size_str, attr_desc="normal"):
        """Muestra la notificación al usuario y habilita la eliminación."""
        mensaje = (
            f"¡Virus detectado!\n\n"
            f"Se encontró el archivo '{VIRUS_FILE_NAME}' dentro de la carpeta:\n"
            f"{VIRUS_FOLDER_PATH}\n\n"
            f"Tamaño aproximado: {size_str}\n"
            f"Atributos de la carpeta: {attr_desc}\n\n"
            f"Pulsa «Eliminar virus» para borrar la carpeta completa y "
            f"eliminar la amenaza. (Si la carpeta está protegida como "
            f"'sistema', se le quitarán esos atributos automáticamente "
            f"antes de borrarla.)"
        )
        self.set_status("⚠ Virus detectado", color="#ff5c5c")
        self.detail_label.configure(text=mensaje, text_color="#ff8c8c")
        self.delete_button.configure(state="normal")

    def _notify_no_virus(self, detalle=None):
        """Informa que no se detectó el virus."""
        self.set_status("✔ No hay virus detectado", color="#3ddc84")
        if detalle:
            self.detail_label.configure(text=detalle, text_color="#9aa4b2")
        else:
            self.detail_label.configure(
                text=("No se encontró la carpeta 'EACoreService' ni el "
                      "archivo del virus 'EACoreServer' en C:\\ProgramData. "
                      "El equipo no presenta la amenaza."),
                text_color="#9aa4b2",
            )

    # ------------------------------------------------------------------
    # Eliminación (Fase 1 - limpieza)
    # ------------------------------------------------------------------
    def _on_delete_clicked(self):
        """Pide confirmación y, si se acepta, elimina la carpeta del virus."""
        if not self.virus_found:
            return

        # Ventana de confirmación modal.
        confirm = ctk.CTkInputDialog  # noqa: F841  (solo para recordar que
        # existe; abajo usamos un CTkToplevel propio para una mejor UX).
        confirm_dialog = _ConfirmDialog(
            self,
            title="Confirmar eliminación",
            message=(
                "Estás a punto de eliminar la carpeta completa:\n\n"
                f"{VIRUS_FOLDER_PATH}\n\n"
                "Esto borrará el virus 'EACoreServer' y cualquier otro "
                "archivo dentro de esa carpeta.\n\n"
                "¿Deseas continuar?"
            ),
        )
        aceptado = confirm_dialog.get_result()

        if not aceptado:
            self.log("Eliminación cancelada por el usuario.")
            return

        # Ejecutar la eliminación en un hilo para no congelar la UI.
        self.delete_button.configure(state="disabled")
        threading.Thread(target=self._delete_virus, daemon=True).start()

    def _delete_virus(self):
        """Elimina la carpeta del virus y reporta el resultado."""
        try:
            self.log("Eliminando carpeta del virus...")

            # 1) Quitar atributos oculto/sistema/readonly de la carpeta y de
            #    TODO su contenido. Windows protege los archivos con
            #    atributo "sistema" frente al borrado, por lo que hay que
            #    limpiarlos primero (equivalente a `attrib -h -s /S /D`).
            self._clear_all_attributes(VIRUS_FOLDER_PATH)

            # 2) Borrar la carpeta completa con todo su contenido.
            shutil.rmtree(VIRUS_FOLDER_PATH, ignore_errors=False)
            self.log("✔ Carpeta eliminada correctamente.")

            # 3) Verificar que realmente se haya borrado.
            if os.path.exists(VIRUS_FOLDER_PATH):
                self.log("⚠ La carpeta sigue presente tras el intento de "
                         "borrado. Puede que falten permisos de "
                         "administrador.")
                self.set_status("⚠ No se pudo eliminar", color="#ffb454")
                self.detail_label.configure(
                    text=("No fue posible eliminar por completo la carpeta "
                          "'EACoreService'. Cierra el programa, ejecútalo "
                          "como Administrador e inténtalo de nuevo."),
                    text_color="#ffb454",
                )
                self.delete_button.configure(state="normal")
                return

            # Éxito: el virus ya no está.
            self.virus_found = False
            self.folder_exists = False
            self.set_status("✔ Virus eliminado con éxito", color="#3ddc84")
            self.detail_label.configure(
                text=("La carpeta 'EACoreService' y el virus 'EACoreServer' "
                      "fueron eliminados correctamente. El equipo está "
                      "limpio."),
                text_color="#3ddc84",
            )
            self.delete_button.configure(state="disabled")
            self.log("Análisis final: el virus ya no está presente.")

        except PermissionError as exc:
            self.log(f"Error de permisos: {exc}")
            self.set_status("⚠ Permiso denegado", color="#ffb454")
            self.detail_label.configure(
                text=("No se tienen permisos suficientes para borrar la "
                      "carpeta. Ejecuta el programa como Administrador e "
                      "inténtalo de nuevo."),
                text_color="#ffb454",
            )
            self.delete_button.configure(state="normal")
        except Exception as exc:  # noqa: BLE001
            self.log(f"Error inesperado: {exc}")
            self.set_status("⚠ Error al eliminar", color="#ff5c5c")
            self.detail_label.configure(
                text=f"Ocurrió un error al eliminar el virus:\n{exc}",
                text_color="#ff8c8c",
            )
            self.delete_button.configure(state="normal")

    def _clear_all_attributes(self, root_path):
        """
        Quita los atributos oculto/sistema/readonly de una carpeta y de
        todo su contenido (archivos y subcarpetas), recursivamente.

        Es necesario porque Windows protege del borrado a los archivos con
        atributo "sistema".
        """
        # Primero la carpeta raíz.
        if not clear_hidden_system_attrs(root_path):
            self.log(f"No se pudieron limpiar atributos de: {root_path}")
        else:
            self.log(f"Atributos limpiados: {root_path}")

        # Luego todo el contenido, recursivamente.
        for dirpath, dirnames, filenames in os.walk(root_path):
            for name in dirnames + filenames:
                full = os.path.join(dirpath, name)
                try:
                    clear_hidden_system_attrs(full)
                except Exception as exc:  # noqa: BLE001
                    self.log(f"Aviso: no se limpiaron atributos de "
                             f"{name}: {exc}")

    # ------------------------------------------------------------------
    # Re-análisis
    # ------------------------------------------------------------------
    def _on_rescan_clicked(self):
        self.log("Reiniciando análisis...")
        self._start_scan_async()

    # ------------------------------------------------------------------
    # Helpers de tamaño de archivo/carpeta
    # ------------------------------------------------------------------
    @staticmethod
    def _path_size(path):
        """Devuelve el tamaño en bytes de un archivo o de una carpeta."""
        if os.path.isfile(path):
            return os.path.getsize(path)
        total = 0
        for root, _dirs, files in os.walk(path):
            for name in files:
                fp = os.path.join(root, name)
                try:
                    total += os.path.getsize(fp)
                except OSError:
                    pass
        return total

    @staticmethod
    def _human_size(num_bytes):
        """Convierte bytes a una cadena legible (KB, MB, ...)."""
        size = float(num_bytes)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"


# ---------------------------------------------------------------------------
# Diálogo de confirmación
# ---------------------------------------------------------------------------
class _ConfirmDialog(ctk.CTkToplevel):
    """Diálogo modal de confirmación con botones Aceptar / Cancelar."""

    def __init__(self, master, title, message):
        super().__init__(master)
        self.title(title)
        self.geometry("440x300")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()  # modal

        self._result = False

        # Centrar respecto al padre
        master.update_idletasks()
        mx = master.winfo_x() + (master.winfo_width() - 440) // 2
        my = master.winfo_y() + (master.winfo_height() - 300) // 2
        self.geometry(f"+{max(mx, 0)}+{max(my, 0)}")

        ctk.CTkLabel(
            self,
            text="Confirmar eliminación",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(24, 10))

        ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=13),
            wraplength=400,
            justify="left",
        ).pack(padx=20, pady=(0, 20))

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(0, 24))

        ctk.CTkButton(
            button_frame,
            text="Cancelar",
            width=120,
            fg_color="transparent",
            border_width=1,
            command=self._on_cancel,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            button_frame,
            text="Aceptar y eliminar",
            width=160,
            command=self._on_accept,
        ).pack(side="left", padx=8)

        # Cerrar con la X también cuenta como cancelar.
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

        self.wait_window()
        self.grab_release()

    def _on_accept(self):
        self._result = True
        self.destroy()

    def _on_cancel(self):
        self._result = False
        self.destroy()

    def get_result(self):
        return self._result


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------
def main():
    app = EliminadorVirusApp()
    app.mainloop()


if __name__ == "__main__":
    main()
