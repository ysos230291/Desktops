import os
import shutil
import subprocess
import threading
import ctypes
import string
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- Utilidades del sistema ----------------
def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def obtener_unidades_extraibles():
    """Devuelve lista de (letra, etiqueta) de unidades removibles."""
    unidades = []
    for letra in string.ascii_uppercase:
        ruta = f"{letra}:\\"
        if os.path.exists(ruta):
            tipo = ctypes.windll.kernel32.GetDriveTypeW(ruta)
            if tipo == 2:  # DRIVE_REMOVABLE
                etiqueta = ""
                try:
                    buffer = ctypes.create_unicode_buffer(261)
                    ctypes.windll.kernel32.GetVolumeInformationW(
                        ruta, buffer, 261, None, None, None, None, 0
                    )
                    etiqueta = buffer.value
                except Exception:
                    pass
                unidades.append((letra, etiqueta or "Sin etiqueta"))
    return unidades


def quitar_atributos_ocultos(ruta):
    """Quita atributos oculto/sistema/lectura a un archivo o carpeta."""
    try:
        # -h oculto, -s sistema, -r solo lectura
        subprocess.run(
            ["attrib", "-h", "-s", "-r", ruta],
            capture_output=True, shell=False
        )
    except Exception:
        pass


# ---------------- Aplicación ----------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Limpiador de Virus + Reparador USB")
        self.geometry("680x700")
        self.resizable(False, False)

        # Título
        ctk.CTkLabel(
            self, text="🧹 Limpiador de Virus y Reparador de USB",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(15, 5))

        if not es_admin():
            ctk.CTkLabel(
                self, text="⚠️ Ejecuta como Administrador para poder borrar archivos protegidos",
                text_color="#FF6B6B"
            ).pack(pady=(0, 5))
        else:
            ctk.CTkLabel(
                self, text="✅ Ejecutando con permisos de Administrador",
                text_color="#6BCB77"
            ).pack(pady=(0, 5))

        # Pestañas
        self.tabs = ctk.CTkTabview(self, width=640, height=560)
        self.tabs.pack(padx=15, pady=10, fill="both", expand=True)

        self.tab_pc = self.tabs.add("🖥️ Eliminar virus de la PC")
        self.tab_usb = self.tabs.add("💾 Reparar memoria USB")

        self._construir_tab_pc()
        self._construir_tab_usb()

        # Log común
        ctk.CTkLabel(self, text="Registro de acciones:",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=20)

        self.texto_log = ctk.CTkTextbox(self, width=640, height=150,
                                        font=ctk.CTkFont(size=12))
        self.texto_log.pack(padx=15, pady=(5, 15))
        self.texto_log.configure(state="disabled")

        self.log("Listo. Selecciona una pestaña para empezar.")

    # ---------------- Pestaña PC ----------------
    def _construir_tab_pc(self):
        ctk.CTkLabel(
            self.tab_pc,
            text="Introduce los datos del virus que viste en el Administrador de tareas:",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", padx=10, pady=(10, 10))

        # Nombre del proceso
        ctk.CTkLabel(self.tab_pc, text="Nombre del proceso (ej. eacoreservices.exe):").pack(anchor="w", padx=10)
        self.entry_proceso = ctk.CTkEntry(self.tab_pc, width=580,
                                          placeholder_text="eacoreservices.exe")
        self.entry_proceso.pack(padx=10, pady=(0, 10))

        # Ruta del archivo
        ctk.CTkLabel(self.tab_pc, text="Ruta del archivo (opcional, clic derecho > Abrir ubicación):").pack(anchor="w", padx=10)
        self.entry_ruta = ctk.CTkEntry(self.tab_pc, width=580,
                                       placeholder_text=r"C:\Users\Public\eacoreservices.exe")
        self.entry_ruta.pack(padx=10, pady=(0, 10))

        # Segundo par opcional (por si hay otro proceso)
        ctk.CTkLabel(self.tab_pc, text="Segundo proceso (opcional):").pack(anchor="w", padx=10)
        self.entry_proceso2 = ctk.CTkEntry(self.tab_pc, width=580,
                                           placeholder_text="(déjalo vacío si no aplica)")
        self.entry_proceso2.pack(padx=10, pady=(0, 10))

        ctk.CTkLabel(self.tab_pc, text="Segunda ruta (opcional):").pack(anchor="w", padx=10)
        self.entry_ruta2 = ctk.CTkEntry(self.tab_pc, width=580,
                                        placeholder_text="(déjalo vacío si no aplica)")
        self.entry_ruta2.pack(padx=10, pady=(0, 15))

        self.btn_eliminar = ctk.CTkButton(
            self.tab_pc, text="🛑 Detener y eliminar proceso(s) y archivo(s)",
            command=self.iniciar_eliminar_pc,
            height=45, fg_color="#8B0000", hover_color="#B22222",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_eliminar.pack(padx=10, pady=5, fill="x")

        # Pista útil
        ctk.CTkLabel(
            self.tab_pc,
            text="💡 Si no sabes la ruta exacta, deja ese campo vacío: se intentará\n"
                 "matar el proceso por nombre. Si el archivo está en una ruta protegida\n"
                 "quizás necesites ejecutar como Administrador.",
            font=ctk.CTkFont(size=11), text_color="gray"
        ).pack(padx=10, pady=(10, 5), anchor="w")

    # ---------------- Pestaña USB ----------------
    def _construir_tab_usb(self):
        ctk.CTkLabel(
            self.tab_usb,
            text="Selecciona la memoria y el nombre de la carpeta oculta del virus:",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", padx=10, pady=(10, 10))

        # Selector de unidad
        ctk.CTkLabel(self.tab_usb, text="Memorias conectadas:").pack(anchor="w", padx=10)
        self.combo_unidades = ctk.CTkComboBox(
            self.tab_usb, values=["(Sin memorias detectadas)"],
            width=580, command=self.seleccionar_unidad
        )
        self.combo_unidades.pack(padx=10, pady=(0, 5))

        self.btn_refrescar = ctk.CTkButton(
            self.tab_usb, text="🔄 Refrescar unidades",
            command=self.refrescar_unidades, width=200
        )
        self.btn_refrescar.pack(pady=(0, 15), padx=10, anchor="w")

        # Nombre de la carpeta del virus
        ctk.CTkLabel(self.tab_usb,
                     text="Nombre de la carpeta oculta del virus:").pack(anchor="w", padx=10)
        self.entry_carpeta = ctk.CTkEntry(self.tab_usb, width=580,
                                          placeholder_text="karspesky")
        self.entry_carpeta.insert(0, "karspesky")
        self.entry_carpeta.pack(padx=10, pady=(0, 15))

        # Checkbox para quitar atributos ocultos
        self.var_quitar_oculto = ctk.BooleanVar(value=True)
        chk = ctk.CTkCheckBox(
            self.tab_usb,
            text="Quitar atributos de oculto/sistema a los archivos recuperados",
            variable=self.var_quitar_oculto
        )
        chk.pack(anchor="w", padx=10, pady=(0, 15))

        # Botón reparar
        self.btn_reparar = ctk.CTkButton(
            self.tab_usb, text="🔧 Reparar memoria seleccionada",
            command=self.iniciar_reparacion,
            height=45, font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_reparar.pack(padx=10, pady=5, fill="x")

        self.unidad_seleccionada = None
        self.refrescar_unidades()

    # ---------------- Log ----------------
    def log(self, mensaje):
        self.texto_log.configure(state="normal")
        self.texto_log.insert("end", mensaje + "\n")
        self.texto_log.see("end")
        self.texto_log.configure(state="disabled")

    # ---------------- Gestión de unidades ----------------
    def refrescar_unidades(self):
        unidades = obtener_unidades_extraibles()
        if not unidades:
            self.combo_unidades.configure(values=["(Sin memorias detectadas)"])
            self.combo_unidades.set("(Sin memorias detectadas)")
            self.unidad_seleccionada = None
            return
        valores = [f"{letra}:  ({etiqueta})" for letra, etiqueta in unidades]
        self.combo_unidades.configure(values=valores)
        self.combo_unidades.set(valores[0])
        self.unidad_seleccionada = unidades[0][0] + ":\\"
        self.log(f"Detectadas {len(unidades)} memoria(s). Seleccionada: {self.unidad_seleccionada}")

    def seleccionar_unidad(self, valor):
        if valor and not valor.startswith("("):
            letra = valor.split(":")[0]
            self.unidad_seleccionada = letra + ":\\"
            self.log(f"Memoria seleccionada: {self.unidad_seleccionada}")

    # ---------------- Acción PC ----------------
    def iniciar_eliminar_pc(self):
        nombre1 = self.entry_proceso.get().strip()
        ruta1 = self.entry_ruta.get().strip()
        nombre2 = self.entry_proceso2.get().strip()
        ruta2 = self.entry_ruta2.get().strip()

        if not nombre1 and not ruta1 and not nombre2 and not ruta2:
            self.log("❌ Introduce al menos un nombre de proceso o una ruta.")
            return

        procesos = [(n, r) for n, r in [(nombre1, ruta1), (nombre2, ruta2)] if n or r]
        self.btn_eliminar.configure(state="disabled", text="Procesando...")
        threading.Thread(target=self._eliminar_pc, args=(procesos,), daemon=True).start()

    def _eliminar_pc(self, procesos):
        self.log("\n--- Eliminando virus de la PC ---")
        for nombre, ruta in procesos:
            if nombre:
                self.log(f"🛑 Deteniendo proceso: {nombre}")
                try:
                    resultado = subprocess.run(
                        ["taskkill", "/F", "/IM", nombre],
                        capture_output=True, text=True
                    )
                    if resultado.returncode == 0:
                        self.log(f"   Proceso '{nombre}' terminado.")
                    else:
                        self.log(f"   '{nombre}' no estaba en ejecución o no existe.")
                except Exception as e:
                    self.log(f"   Error al matar proceso: {e}")
            if ruta:
                self.log(f"🗑️ Borrando archivo: {ruta}")
                if not os.path.exists(ruta):
                    self.log("   La ruta no existe.")
                    continue
                try:
                    # Primero quitar atributos ocultos/sistema, si los tiene
                    quitar_atributos_ocultos(ruta)
                    os.remove(ruta)
                    self.log("   Archivo eliminado correctamente.")
                except PermissionError:
                    self.log("   ERROR: Sin permisos. Ejecuta como Administrador.")
                except Exception as e:
                    self.log(f"   Error: {e}")
        self.log("--- Eliminación finalizada ---\n")
        self.btn_eliminar.configure(
            state="normal", text="🛑 Detener y eliminar proceso(s) y archivo(s)"
        )

    # ---------------- Acción USB ----------------
    def iniciar_reparacion(self):
        if not self.unidad_seleccionada:
            self.log("❌ Primero selecciona una memoria.")
            return
        carpeta = self.entry_carpeta.get().strip()
        if not carpeta:
            self.log("❌ Indica el nombre de la carpeta oculta del virus.")
            return
        self.btn_reparar.configure(state="disabled", text="Reparando...")
        threading.Thread(
            target=self._reparar_usb,
            args=(self.unidad_seleccionada, carpeta, self.var_quitar_oculto.get()),
            daemon=True
        ).start()

    def _reparar_usb(self, letra_usb, nombre_carpeta, quitar_ocultos):
        carpeta_virus = os.path.join(letra_usb, nombre_carpeta)
        self.log(f"\n--- Reparando {letra_usb} (carpeta: '{nombre_carpeta}') ---")

        # 1. Borrar autorun.inf si existe
        autorun = os.path.join(letra_usb, "autorun.inf")
        if os.path.exists(autorun):
            try:
                quitar_atributos_ocultos(autorun)
                os.remove(autorun)
                self.log("🗑️ autorun.inf eliminado.")
            except Exception as e:
                self.log(f"No se pudo borrar autorun.inf: {e}")

        # 2. Comprobar que existe la carpeta del virus
        if not os.path.exists(carpeta_virus):
            self.log(f"✅ No se encontró la carpeta '{nombre_carpeta}'. Nada que mover.")
            self.finalizar_reparacion()
            return

        # 3. Mover archivos de vuelta a la raíz, uno por uno
        self.log("📂 Moviendo archivos de vuelta a la raíz de la memoria...")
        movidos, errores = 0, 0
        for root, dirs, files in os.walk(carpeta_virus):
            for file in files:
                origen = os.path.join(root, file)
                ruta_rel = os.path.relpath(origen, carpeta_virus)
                destino = os.path.join(letra_usb, ruta_rel)
                try:
                    os.makedirs(os.path.dirname(destino) or letra_usb, exist_ok=True)
                    if os.path.exists(destino):
                        base, ext = os.path.splitext(destino)
                        destino = f"{base}_recuperado{ext}"
                    # Quitar atributos ocultos al origen antes de moverlo
                    if quitar_ocultos:
                        quitar_atributos_ocultos(origen)
                    shutil.move(origen, destino)
                    # Y también al destino final
                    if quitar_ocultos:
                        quitar_atributos_ocultos(destino)
                    movidos += 1
                except Exception as e:
                    errores += 1
                    self.log(f"Error con {file}: {e}")

        self.log(f"✅ Archivos recuperados: {movidos}. Errores: {errores}.")

        # 4. Borrar la carpeta del virus
        try:
            shutil.rmtree(carpeta_virus)
            self.log(f"🗑️ Carpeta '{nombre_carpeta}' eliminada.")
        except Exception as e:
            self.log(f"No se pudo eliminar la carpeta: {e}")

        # 5. Restaurar atributos a TODO el contenido de la raíz
        if quitar_ocultos:
            try:
                subprocess.run(
                    ["attrib", "-h", "-s", "-r", "/s", "/d", f"{letra_usb}*.*"],
                    capture_output=True, shell=False
                )
                self.log("👁️ Atributos oculto/sistema/lectura restaurados en la memoria.")
            except Exception as e:
                self.log(f"No se pudieron restaurar atributos: {e}")

        self.finalizar_reparacion()

    def finalizar_reparacion(self):
        self.log("--- Reparación completada ---\n")
        self.btn_reparar.configure(state="normal", text="🔧 Reparar memoria seleccionada")


if __name__ == "__main__":
    app = App()
    app.mainloop()