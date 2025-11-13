"""
Tema 1: Introducción a pandas - DataFrames y Series
====================================================
- Cargar datos desde una base de datos
- Explorar DataFrames
- Trabajar con Series
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.gui_helper import GUIHelper


class DataFramesSeries:
    def __init__(self, root):
        self.root = root
        self.root.title("Tema 1: DataFrames y Series")
        self.root.geometry("1000x600")

        self.text_area = None
        self.helpers = None
        self.df = None
        self.setup_ui()

        self.helpers = GUIHelper(self.text_area)

    def setup_ui(self):
        """ Configurar interfaz de usuario """
        # Titulo
        title = tk.Label(
            self.root,
            text="Tema 1: DataFrames y Series",
            font=("Arial", 20, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=10
        )
        title.pack(fill=tk.X)

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Botones
        buttons_frame = ttk.LabelFrame(main_frame, text="DataFrames", padding="10")
        buttons_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            buttons_frame,
            text="1. Cargar datos",
            command=self.cargar_datos,
            width=40
        ).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(
            buttons_frame,
            text="2. Mostrar todos los registros",
            command=self.mostrar_registros,
            width=40
        ).grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(
            buttons_frame,
            text="3. Extraer títulos como Series",
            command=self.extraer_titulos,
            width=40
        ).grid(row=0, column=1, pady=5, padx=5)

        ttk.Button(
            buttons_frame,
            text="4. Películas por década",
            command=self.peliculas_por_decada,
            width=40
        ).grid(row=1, column=1, pady=5, padx=5)

        ttk.Button(
            buttons_frame,
            text="5. Limpiar datos",
            command=lambda: self.helpers.limpiar_log() if self.helpers else None,
            width=40
        ).grid(row=0, column=2, pady=5, padx=5)

        # Area de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.text_area = scrolledtext.ScrolledText(
            results_frame,
            width=100,
            height=20,
            wrap=tk.WORD,
            font=("Arial", 12)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def cargar_datos(self):
        self.df = self.helpers.cargar_datos()

    def mostrar_registros(self):
        """Mostrar todos los registros"""
        if self.helpers.datos_no_cargados():
            return

        # Crear una nueva ventana
        ventana = tk.Toplevel(self.root)
        ventana.title("Todos los registros")
        ventana.geometry("1000x600")

        # Frame con scroll
        frame = tk.Frame(ventana)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear Treeview
        tree = ttk.Treeview(frame, columns=list(self.helpers.df.columns), show='headings')

        # Scroll
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Posicionar
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Configurar columnas
        for col in self.helpers.df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Insertar datos
        for idx, row in self.helpers.df.iterrows():
            tree.insert("", tk.END, values=list(row))

    def extraer_titulos(self):
        """Series"""
        if self.helpers.datos_no_cargados():
            return

        titulos = self.helpers.df['mov_title']

        self.helpers.log("=" * 70)
        self.helpers.log("SERIE DE TÍTULOS DE PELÍCULAS")
        self.helpers.log("=" * 70)
        self.helpers.log(f"Tipo de objeto: {type(titulos)}")
        self.helpers.log(f"Nombre de la serie: {titulos.name}")
        self.helpers.log(f"Total de elementos: {len(titulos)}")

        for i, titulo in enumerate(titulos.head(10), 1):
            self.helpers.log(f"  {i:2}. {titulo}")

    def peliculas_por_decada(self):
        """DataFrame"""
        if self.helpers.datos_no_cargados():
            return

        self.helpers.log("=" * 50)
        self.helpers.log("PELÍCULAS POR DÉCADA")
        self.helpers.log("=" * 50)

        # Crear década
        df_temp = self.helpers.df.copy()
        df_temp['decada'] = (df_temp['mov_year'] // 10) * 10

        por_decada = df_temp['decada'].value_counts().sort_index()

        for decada, count in por_decada.items():
            self.helpers.log(f"{int(decada)}s: {count} películas")


def main():
    root = tk.Tk()
    app = DataFramesSeries(root)
    root.mainloop()


if __name__ == "__main__":
    main()
