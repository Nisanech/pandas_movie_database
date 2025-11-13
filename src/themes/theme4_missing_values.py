"""
Tema 4: Manejo de Valores Faltantes
===================================
- Identificar valores nulos
- Calcular porcentajes de datos faltantes
- Eliminar registros estratégicamente
- Imputar valores faltantes
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.gui_helper import GUIHelper

class MissingValues:
    def __init__(self, root):
        self.root = root
        self.root.title("Tema 4: Valores Faltantes")
        self.root.geometry("1000x600")

        self.text_area = None
        self.helpers = None
        self.df = None
        self.setup_ui()

        self.helpers = GUIHelper(self.text_area)

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Título
        title = tk.Label(
            self.root,
            text="Tema 4: Manejo de Valores Faltantes",
            font=("Arial", 20, "bold"),
            bg="#9C27B0",
            fg="white",
            pady=10
        )
        title.pack(fill=tk.X)

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Identificación
        identification_frame = ttk.LabelFrame(main_frame, text="Identificación de Valores Nulos", padding="10")
        identification_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            identification_frame,
            text="1. Cargar datos",
            command=self.cargar_datos,
            width=40
        ).grid(row=0, column=0, pady=5, padx=5)

        ttk.Button(
            identification_frame,
            text="2. Identificar columnas con valores faltantes",
            command=self.identificar_nulos,
            width=45
        ).grid(row=1, column=0, pady=5, padx=5)

        # Eliminación
        deletion_frame = ttk.LabelFrame(main_frame, text="Eliminación Estratégica", padding="10")
        deletion_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            deletion_frame,
            text="3. Conservar solo películas con info completa",
            command=self.conservar_completos,
            width=45
        ).grid(row=1, column=0, pady=5, padx=5)

        # Imputación
        imputation_frame = ttk.LabelFrame(main_frame, text="Reemplazo e Imputación", padding="10")
        imputation_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            imputation_frame,
            text="4. Reemplazar ratings con mediana por género",
            command=self.imputar_rating_por_genero,
            width=45
        ).grid(row=0, column=0, pady=5, padx=5)

        ttk.Button(
            identification_frame,
            text="5. Limpiar datos",
            command=lambda: self.helpers.limpiar_log() if self.helpers else None,
            width=40
        ).grid(row=0, column=2, pady=5, padx=5)

        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.text_area = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=100,
            height=20,
            font=("Courier", 10)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def cargar_datos(self):
        self.df = self.helpers.cargar_datos()

    def identificar_nulos(self):
        """Identifica qué columnas tienen valores faltantes"""
        if self.helpers.datos_no_cargados():
            return

        nulos = self.df.isnull().sum()
        nulos_filtrado = nulos[nulos > 0]

        self.text_area.delete(1.0, tk.END)
        self.helpers.log("=" * 70)
        self.helpers.log("IDENTIFICACIÓN DE VALORES FALTANTES")
        self.helpers.log("=" * 70)

        if len(nulos_filtrado) == 0:
            self.helpers.log("\n¡No hay valores faltantes en el dataset!")
        else:
            # self.helpers.log(f"\nColumnas con valores faltantes: {len(nulos_filtrado)}\n")

            for col, count in nulos_filtrado.items():
                self.helpers.log(f"  {col:25} → {count:3} valores nulos")

        # Mostrar en ventana
        self.mostrar_analisis_nulos()





    def conservar_completos(self):
        """Conserva solo películas con información completa"""
        if self.helpers.datos_no_cargados():
            return

        registros_iniciales = len(self.df)

        # Eliminar todas las filas con cualquier valor nulo
        self.df_clean = self.df.dropna().copy()

        registros_finales = len(self.df_clean)
        eliminados = registros_iniciales - registros_finales

        self.text_area.delete(1.0, tk.END)
        self.helpers.log("=" * 70)
        self.helpers.log("CONSERVAR SOLO INFORMACIÓN COMPLETA")
        self.helpers.log("=" * 70)
        self.helpers.log("\nCriterio: Eliminar cualquier fila con al menos un valor nulo\n")
        self.helpers.log(f"  Registros iniciales:  {registros_iniciales}")
        self.helpers.log(f"  Registros finales:    {registros_finales}")
        self.helpers.log(f"  Registros eliminados: {eliminados}")
        self.helpers.log(f"  Porcentaje retenido:  {(registros_finales / registros_iniciales * 100):.2f}%")

        if len(self.df_clean) > 0:
            self.mostrar_dataframe(self.df_clean.head(20), "Datos Completos (primeros 20)")

        self.helpers.log(
            f"Se conservaron {registros_finales} de {registros_iniciales} registros\n"
            f"({(registros_finales / registros_iniciales * 100):.1f}% de los datos)"
        )

    def imputar_rating_por_genero(self):
        """Reemplaza ratings nulos con la mediana del género correspondiente"""
        if self.helpers.datos_no_cargados():
            return

        self.df_clean = self.df.copy()

        # Contar nulos iniciales
        nulos_iniciales = self.df_clean['avg_rating'].isnull().sum()

        # Calcular mediana por género
        mediana_por_genero = self.df_clean.groupby('genre')['avg_rating'].median()

        # Función para imputar
        def imputar_rating(row):
            if pd.isnull(row['avg_rating']) and pd.notna(row['genre']):
                return mediana_por_genero.get(row['genre'], row['avg_rating'])
            return row['avg_rating']

        # Aplicar imputación
        self.df_clean['avg_rating'] = self.df_clean.apply(imputar_rating, axis=1)

        # Contar nulos finales
        nulos_finales = self.df_clean['avg_rating'].isnull().sum()
        imputados = nulos_iniciales - nulos_finales

        self.text_area.delete(1.0, tk.END)
        self.helpers.log("=" * 70)
        self.helpers.log("IMPUTACIÓN DE RATINGS POR GÉNERO")
        self.helpers.log("=" * 70)
        self.helpers.log("\nEstrategia: Reemplazar ratings nulos con la mediana de su género\n")
        self.helpers.log(f"  Valores nulos iniciales: {nulos_iniciales}")
        self.helpers.log(f"  Valores nulos finales:   {nulos_finales}")
        self.helpers.log(f"  Valores imputados:       {imputados}")
        self.helpers.log("\nMediana por género:\n")

        for genero, mediana in mediana_por_genero.items():
            if pd.notna(genero):
                self.helpers.log(f"  {genero:15} → {mediana:.2f}")

        if imputados > 0:
            self.helpers.log(f"Se imputaron {imputados} valores de rating usando la mediana por género")
        else:
            self.helpers.log("No había ratings nulos para imputar")



    def mostrar_analisis_nulos(self):
        """Muestra análisis visual de valores nulos"""
        if self.df is None:
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Análisis de Valores Nulos")
        ventana.geometry("600x500")

        text = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, font=("Courier", 11))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text.insert(tk.END, "ANÁLISIS DETALLADO DE VALORES NULOS\n")
        text.insert(tk.END, "=" * 60 + "\n\n")

        nulos = self.df.isnull().sum()
        total = len(self.df)

        text.insert(tk.END, f"Total de registros: {total}\n")
        text.insert(tk.END, f"Total de columnas:  {len(self.df.columns)}\n\n")

        text.insert(tk.END, "Columna                  Nulos    %\n")
        text.insert(tk.END, "-" * 60 + "\n")

        for col in self.df.columns:
            count = nulos[col]
            porcentaje = (count / total * 100)

            if count > 0:
                text.insert(tk.END, f"{col:25} {count:5}  {porcentaje:5.1f}%\n")
            else:
                text.insert(tk.END, f"{col:25} {count:5}  {porcentaje:5.1f}%\n")

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
    app = MissingValues(root)
    root.mainloop()


if __name__ == "__main__":
    main()