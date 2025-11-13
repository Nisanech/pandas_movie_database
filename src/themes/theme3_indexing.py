"""
Tema 3: Indexación Básica y Avanzada
====================================
- Indexación básica (loc, iloc)
- Selección condicional
- Filtros múltiples
- Operaciones avanzadas
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.gui_helper import GUIHelper


class Indexing:
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
            text="Tema 3: Indexación Básica y Avanzada",
            font=("Arial", 20, "bold"),
            bg="#FF9800",
            fg="white",
            pady=10
        )
        title.pack(fill=tk.X)

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Botones - Indexación Básica
        basic_frame = ttk.LabelFrame(main_frame, text="Indexación Básica", padding="10")
        basic_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            basic_frame,
            text="1. Cargar datos",
            command=self.cargar_datos,
            width=40
        ).grid(row=0, column=0, pady=5, padx=5)

        ttk.Button(
            basic_frame,
            text='2. Películas género "Drama" de UK',
            command=self.drama_uk,
            width=40
        ).grid(row=1, column=0, pady=5, padx=5)

        # Indexación Avanzada
        advanced_frame = ttk.LabelFrame(main_frame, text="Indexación Avanzada", padding="10")
        advanced_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            advanced_frame,
            text="3. UK + después de 1995 + rating > 4",
            command=self.condiciones_multiples,
            width=40
        ).grid(row=0, column=0, pady=5, padx=5)

        ttk.Button(
            basic_frame,
            text="4. Limpiar datos",
            command=lambda: self.helpers.limpiar_log() if self.helpers else None,
            width=40
        ).grid(row=0, column=1, pady=5, padx=5)

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

    def drama_uk(self):
        """Obtiene películas de género Drama producidas en UK"""
        if self.helpers.datos_no_cargados():
            return

        resultado = self.df[(self.df['genre'] == 'Drama') & (self.df['mov_rel_country'] == 'UK')].copy()

        self.helpers.log("=" * 70)
        self.helpers.log('PELÍCULAS DE DRAMA PRODUCIDAS EN UK')
        self.helpers.log("=" * 70)
        self.helpers.log(f"\nTotal encontradas: {len(resultado)}\n")


        if len(resultado) > 0:
            self.mostrar_dataframe(resultado, "Drama - UK")
        else:
            self.helpers.log("No se encontraron películas con estos criterios")

    def condiciones_multiples(self):
        """Combina condiciones múltiples: UK, después de 1995, rating > 4"""
        if self.helpers.datos_no_cargados():
            return

        resultado = self.df[
            (self.df['mov_rel_country'] == 'UK') &
            (self.df['mov_year'] > 1995) &
            (self.df['avg_rating'] > 4)
            ].copy()

        self.helpers.log("=" * 70)
        self.helpers.log('CONDICIONES MÚLTIPLES')
        self.helpers.log("=" * 70)
        self.helpers.log("\nCriterios aplicados:")
        self.helpers.log("  ✓ País: UK")
        self.helpers.log("  ✓ Año: > 1995")
        self.helpers.log("  ✓ Rating: > 4")
        self.helpers.log(f"\nTotal encontradas: {len(resultado)}\n")

        if len(resultado) > 0:
            self.mostrar_dataframe(resultado, "Filtro Múltiple: UK + >1995 + Rating>4")
        else:
            self.helpers.log("No se encontraron películas con estos criterios")

    def mostrar_dataframe(self, df, titulo):
        """Muestra un DataFrame en una ventana emergente"""
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("1000x600")

        frame = ttk.Frame(ventana)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for idx, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))


def main():
    root = tk.Tk()
    app = Indexing(root)
    root.mainloop()


if __name__ == "__main__":
    main()
