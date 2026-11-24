"""
Facilitador Legal
-----------------
Fase 1: extracción de datos de la Escritura Pública (PDF digital).
Funciona sin internet. Requiere:  pip install pdfplumber

Al seleccionar el PDF se genera, en la misma carpeta, el archivo
"escritura_extraccion.txt" con los datos extraídos.
"""

import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

import pdfplumber

NO_ENCONTRADO = "No encontrado"
ARCHIVO_SALIDA = "escritura_extraccion.txt"

# Cualquier tipo de guion usado como relleno en las escrituras
G = r"\-–—"


# ======================================================================
#  LECTURA Y LIMPIEZA
# ======================================================================
def leer_pdf(ruta):
    """Devuelve todo el texto del PDF (sin OCR, solo PDF digital)."""
    paginas = []
    with pdfplumber.open(ruta) as pdf:
        for pagina in pdf.pages:
            paginas.append(pagina.extract_text() or "")
    return "\n".join(paginas)


def limpiar(texto):
    """Une renglones y quita espacios sobrantes."""
    return " ".join(texto.split()).strip()


def normalizar_comillas(texto):
    """Pasa todas las variantes de comillas a comillas rectas."""
    return re.sub(r"[“”„‟«»¨´`‘’'\"]", '"', texto)


def buscar(patron, texto):
    """Busca el patrón y devuelve el grupo 1 limpio, o 'No encontrado'."""
    m = re.search(patron, texto, re.IGNORECASE)
    if not m:
        return NO_ENCONTRADO
    valor = limpiar(m.group(1))
    return valor if valor else NO_ENCONTRADO


# ======================================================================
#  REGLAS DE EXTRACCIÓN DE LA ESCRITURA PÚBLICA
# ======================================================================
def extraer_nombre(texto):
    # Inicio: después de "ESCRITURA PÚBLICA DE CONSTITUCIÓN DE"
    # Fin: primer guion (no se incluye)
    valor = buscar(
        r"ESCRITURA\s+P[ÚU]BLICA\s+DE\s+CONSTITUCI[ÓO]N\s+DE\s+([^" + G + r"]+)",
        texto,
    )
    if valor == NO_ENCONTRADO:
        return valor
    valor = normalizar_comillas(valor)
    valor = re.sub(r'(?<=")\s*\.\s*$', "", valor)  # quita el punto tras la comilla final
    return valor.strip()


def extraer_numero(texto):
    # Inicio: después de "NÚMERO:" (saltando guiones)
    # Fin: primer punto o guion (no se incluye)
    return buscar(
        r"N[ÚU]MERO\s*:\s*[" + G + r"\s]*([^." + G + r"]+)",
        texto,
    )


def extraer_fecha(texto):
    # Inicio: después de "a los" en la línea "En <ciudad>, a los ..."
    # Fin: primer punto o guion (no se incluye)
    return buscar(
        r"\bEn\s+[^,]{1,60},\s*a\s+los\s+(.+?)\s*[." + G + r"]",
        texto,
    )


def extraer_notario(texto):
    # Inicio: después de "ANTE MI:" (saltando guiones)
    # Fin: primer guion (no se incluye); el punto final sí queda
    return buscar(
        r"ANTE\s+M[IÍ]\s*:\s*[" + G + r"\s]*([^" + G + r"]+)",
        texto,
    )


def extraer_representante(texto):
    # Inicio: después de "DECISIÓN NÚMERO 1: Designar a"
    # Fin: primer guion (no se incluye); el punto final sí queda
    return buscar(
        r"DECISI[ÓO]N\s+N[ÚU]MERO\s+1\s*:\s*Designar\s+a\s+([^" + G + r"]+)",
        texto,
    )


def extraer_domicilio(texto):
    # Inicio: en "El domicilio Social se establece" (se incluye)
    # Fin: primer guion (no se incluye); el punto final sí queda
    return buscar(
        r"(El\s+domicilio\s+Social\s+se\s+establece[^" + G + r"]*)",
        texto,
    )


def extraer_objeto(texto):
    # Inicio: después de "TERCERA:" (la palabra no se incluye)
    # Fin: primer guion (no se incluye); el punto final sí queda
    return buscar(
        r"TERCERA\s*:\s*([^" + G + r"]+)",
        texto,
    )


def extraer_escritura(ruta_pdf):
    """Lee el PDF y devuelve un diccionario con los datos de la Fase 1."""
    texto = limpiar(leer_pdf(ruta_pdf))
    if not texto:
        raise ValueError(
            "No se pudo leer texto del PDF. Puede ser un PDF escaneado "
            "(requeriría OCR)."
        )
    return {
        "nombre": extraer_nombre(texto),
        "numero": extraer_numero(texto),
        "fecha": extraer_fecha(texto),
        "notario": extraer_notario(texto),
        "representante": extraer_representante(texto),
        "domicilio": extraer_domicilio(texto),
        "objeto": extraer_objeto(texto),
    }


def generar_txt(datos, ruta_pdf):
    """Escribe el .txt con los datos extraídos en la carpeta del PDF."""
    carpeta = os.path.dirname(os.path.abspath(ruta_pdf))
    ruta_txt = os.path.join(carpeta, ARCHIVO_SALIDA)
    lineas = [
        "Nombre y denominación:",
        datos["nombre"],
        "",
        "Número de escritura notarial y fecha de emisión:",
        f"Número: {datos['numero']}",
        f"Fecha: {datos['fecha']}",
        "",
        "Notario que autoriza, su competencia y sede notarial:",
        datos["notario"],
        "",
        "Quién representa:",
        datos["representante"],
        "",
        "Domicilio social:",
        datos["domicilio"],
        "",
        "Objeto:",
        datos["objeto"],
        "",
    ]
    with open(ruta_txt, "w", encoding="utf-8-sig") as f:
        f.write("\n".join(lineas))
    return ruta_txt


# ======================================================================
#  INTERFAZ
# ======================================================================
class FacilitadorLegal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Facilitador Legal")
        self.geometry("900x820")
        self.minsize(700, 450)
        self._crear_menu_superior()
        self._crear_area_principal()

    def _crear_menu_superior(self):
        barra = tk.Frame(self, bg="#1f2a44", height=50)
        barra.pack(side="top", fill="x")
        tk.Button(
            barra,
            text="Escritura Pública",
            font=("Segoe UI", 11, "bold"),
            bg="#34508c",
            fg="white",
            activebackground="#4a68a8",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.abrir_escritura_publica,
        ).pack(side="left", padx=10, pady=8)

    def _crear_area_principal(self):
        self.area = tk.Frame(self, bg="#f4f6fa")
        self.area.pack(fill="both", expand=True)
        self._pantalla_inicio()

    def _limpiar_area(self):
        for w in self.area.winfo_children():
            w.destroy()

    def _pantalla_inicio(self):
        self._limpiar_area()
        tk.Label(
            self.area, text="Facilitador Legal",
            font=("Segoe UI", 24, "bold"), bg="#f4f6fa", fg="#1f2a44",
        ).pack(pady=(60, 10))
        tk.Label(
            self.area,
            text="Selecciona una opción del menú superior para comenzar.",
            font=("Segoe UI", 12), bg="#f4f6fa", fg="#555555",
        ).pack()

    # ---------- Fase 1: Escritura Pública ----------
    def abrir_escritura_publica(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar Escritura Pública",
            filetypes=[("Archivos PDF", "*.pdf")],
        )
        if not ruta:
            return
        try:
            datos = extraer_escritura(ruta)
            ruta_txt = generar_txt(datos, ruta)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el documento:\n{e}")
            return
        self._mostrar_resultado(ruta, datos, ruta_txt)

    def _mostrar_resultado(self, ruta, datos, ruta_txt):
        self._limpiar_area()
        tk.Label(
            self.area, text="Escritura Pública",
            font=("Segoe UI", 18, "bold"), bg="#f4f6fa", fg="#1f2a44",
        ).pack(anchor="w", padx=30, pady=(20, 2))
        tk.Label(
            self.area,
            text=f"Archivo: {os.path.basename(ruta)}    |    TXT generado: {ruta_txt}",
            font=("Segoe UI", 9), bg="#f4f6fa", fg="#555555",
            wraplength=820, justify="left",
        ).pack(anchor="w", padx=30, pady=(0, 12))

        campos = [
            ("Nombre y denominación", datos["nombre"], 2),
            ("Número de escritura notarial", datos["numero"], 1),
            ("Fecha de emisión", datos["fecha"], 1),
            ("Notario que autoriza, su competencia y sede notarial", datos["notario"], 3),
            ("Quién representa", datos["representante"], 3),
            ("Domicilio social", datos["domicilio"], 3),
            ("Objeto", datos["objeto"], 5),
        ]
        for etiqueta, valor, alto in campos:
            tk.Label(
                self.area, text=etiqueta,
                font=("Segoe UI", 10, "bold"), bg="#f4f6fa", fg="#1f2a44",
            ).pack(anchor="w", padx=30)
            caja = tk.Text(self.area, height=alto, font=("Segoe UI", 10), wrap="word")
            caja.insert("1.0", valor)
            caja.config(state="disabled")
            caja.pack(fill="x", padx=30, pady=(2, 10))


if __name__ == "__main__":
    FacilitadorLegal().mainloop()