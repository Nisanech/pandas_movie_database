"""
Tema 2: Importación y Exportación de Datos
==========================================
- Exportar subconjuntos de datos a Excel
- Crear resúmenes personalizados
- Guardar datos en diferentes formatos
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.gui_helper import GUIHelper


class ImportExport:
    def __init__(self, root):
        self.root = root
        self.root.title("Tema 2: Importación y Exportación")
        self.root.geometry("1000x600")

        self.text_area = None
        self.helpers = None
        self.df = None
        self.setup_ui()

        self.helpers = GUIHelper(self.text_area)

    def setup_ui(self):
        """ Configurar interfaz de usuario """
        # Título
        title = tk.Label(
            self.root,
            text="Tema 2: Importación y Exportación de Datos",
            font=("Arial", 16, "bold"),
            bg="#2196F3",
            fg="white",
            pady=10
        )
        title.pack(fill=tk.X)

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Botones
        buttons_frame = ttk.LabelFrame(main_frame, text="Exportación de Datos", padding="10")
        buttons_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            buttons_frame,
            text="1. Cargar datos",
            command=self.cargar_datos,
            width=45
        ).grid(row=0, column=0, pady=5, padx=5)

        ttk.Button(
            buttons_frame,
            text="2. Exportar películas posteriores al 2000",
            command=self.exportar_post_2000,
            width=45
        ).grid(row=1, column=0, pady=5, padx=5)

        ttk.Button(
            buttons_frame,
            text="3. Exportar resumen (título, año, director, rating)",
            command=self.exportar_resumen,
            width=45
        ).grid(row=0, column=1, pady=5, padx=5)

        ttk.Button(
            buttons_frame,
            text="4. Limpiar datos",
            command=lambda: self.helpers.limpiar_log() if self.helpers else None,
            width=40
        ).grid(row=1, column=1, pady=5, padx=5)

        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.text_area = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=100,
            height=25,
            font=("Arial", 10)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def cargar_datos(self):
        self.df = self.helpers.cargar_datos()

    def exportar_post_2000(self):
        """Exporta películas posteriores al 2000"""
        if self.helpers.datos_no_cargados():
            return

        # Filtrar películas posteriores a 2000
        df_filtrado = self.df[self.df['mov_year'] > 2000].copy()

        self.helpers.log("=" * 70)
        self.helpers.log("PELÍCULAS POSTERIORES AL AÑO 2000")
        self.helpers.log("=" * 70)
        self.helpers.log(f"\nTotal de películas filtradas: {len(df_filtrado)}")

        # Crear directorio si no existe
        os.makedirs('output/exports', exist_ok=True)

        # Exportar a Excel
        filename = 'output/exports/peliculas_post_2000.xlsx'
        df_filtrado.to_excel(filename, index=False, engine='openpyxl')

        self.helpers.log(f"\nArchivo exportado: {filename}")
        self.helpers.log(f"\nPrimeras 5 películas exportadas:\n")

        for idx, row in df_filtrado.head(5).iterrows():
            self.helpers.log(f"  • {row['mov_title']} ({row['mov_year']})")

        self.helpers.log(f"Se exportaron {len(df_filtrado)} películas a:\n{filename}")

    def exportar_resumen(self):
        """Exporta resumen con título, año, director y rating"""
        if self.helpers.datos_no_cargados():
            return

        # Seleccionar columnas específicas
        columnas = ['mov_title', 'mov_year', 'director_name', 'avg_rating']
        df_resumen = self.df[columnas].copy()

        # Renombrar columnas
        df_resumen.columns = ['Título', 'Año', 'Director', 'Rating Promedio']

        self.helpers.log("=" * 70)
        self.helpers.log("RESUMEN DE PELÍCULAS")
        self.helpers.log("=" * 70)
        self.helpers.log(f"\nColumnas incluidas: {list(df_resumen.columns)}")
        self.helpers.log(f"Total de registros: {len(df_resumen)}")

        # Exportar
        os.makedirs('output/exports', exist_ok=True)
        filename = 'output/exports/resumen_peliculas.xlsx'

        # Crear Excel con formato
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df_resumen.to_excel(writer, sheet_name='Resumen', index=False)

            # Obtener workbook y worksheet
            workbook = writer.book
            worksheet = writer.sheets['Resumen']

            # Formato para encabezados
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4CAF50',
                'font_color': 'white',
                'border': 1
            })

            # Aplicar formato a encabezados
            for col_num, value in enumerate(df_resumen.columns):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 20)

        self.helpers.log(f"\nArchivo exportado: {filename}")

        self.helpers.log(f"Resumen exportado a:\n{filename}")


def main():
    root = tk.Tk()
    app = ImportExport(root)
    root.mainloop()


if __name__ == "__main__":
    main()
