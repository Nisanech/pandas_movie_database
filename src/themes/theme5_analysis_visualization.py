"""
Tema 5: Análisis Integrado y Visualización
==========================================
- Crear gráficos de línea
- Analizar tendencias temporales
- Crear gráficos de barras
- Análisis por categorías
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.gui_helper import GUIHelper

class AnalysisVisualization:
    def __init__(self, root):
        self.root = root
        self.root.title("Tema 5: Análisis y Visualización")
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
            text="Tema 5: Análisis Integrado y Visualización",
            font=("Arial", 20, "bold"),
            bg="#00BCD4",
            fg="white",
            pady=10
        )
        title.pack(fill=tk.X)

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Análisis Temporal
        temporal_frame = ttk.LabelFrame(main_frame, text="Análisis Temporal", padding="10")
        temporal_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            temporal_frame,
            text="1. Cargar datos",
            command=self.cargar_datos,
            width=45
        ).grid(row=0, column=0, pady=5, padx=5)

        ttk.Button(
            temporal_frame,
            text="2. Gráfico: Películas por año",
            command=self.grafico_peliculas_por_anio,
            width=45
        ).grid(row=1, column=0, pady=5, padx=5)

        ttk.Button(
            temporal_frame,
            text="3. Gráfico: Duración promedio por año",
            command=self.grafico_duracion_por_anio,
            width=45
        ).grid(row=2, column=0, pady=5, padx=5)

        # Análisis por Categorías
        category_frame = ttk.LabelFrame(main_frame, text="Análisis por Categorías", padding="10")
        category_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            category_frame,
            text="4. Gráfico: Rating promedio por género",
            command=self.grafico_rating_por_genero,
            width=45
        ).grid(row=0, column=0, pady=5, padx=5)

        ttk.Button(
            category_frame,
            text="5. Tabla: Estadísticas por género",
            command=self.tabla_estadisticas_genero,
            width=45
        ).grid(row=1, column=0, pady=5, padx=5)

        ttk.Button(
            category_frame,
            text="6. Gráfico: Top 10 directores",
            command=self.grafico_top_directores,
            width=45
        ).grid(row=2, column=0, pady=5, padx=5)

        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.text_area = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=100,
            height=18,
            font=("Courier", 10)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def cargar_datos(self):
        self.df = self.helpers.cargar_datos()

    def grafico_peliculas_por_anio(self):
        """Crea gráfico de línea de películas producidas por año"""
        if self.helpers.datos_no_cargados():
            return

        # Contar películas por año
        peliculas_por_anio = self.df['mov_year'].value_counts().sort_index()

        # Crear ventana
        ventana = tk.Toplevel(self.root)
        ventana.title("Películas Producidas por Año")
        ventana.geometry("1000x600")

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(peliculas_por_anio.index, peliculas_por_anio.values,
                marker='o', linewidth=2, color='#2196F3', markersize=6)

        ax.set_xlabel('Año', fontsize=12, fontweight='bold')
        ax.set_ylabel('Número de Películas', fontsize=12, fontweight='bold')
        ax.set_title('Número de Películas Producidas por Año',
                     fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')

        # Rotar etiquetas del eje x
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Incrustar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Guardar gráfico
        os.makedirs('output/charts', exist_ok=True)
        fig.savefig('output/charts/peliculas_por_anio.png', dpi=300, bbox_inches='tight')

        self.helpers.log("\nGráfico de películas por año generado")
        self.helpers.log(f"Guardado en: output/charts/peliculas_por_anio.png")

    def grafico_duracion_por_anio(self):
        """Analiza cómo ha cambiado la duración promedio con el tiempo"""
        if self.helpers.datos_no_cargados():
            return

        # Calcular duración promedio por año
        duracion_por_anio = self.df.groupby('mov_year')['mov_time'].mean().sort_index()

        # Crear ventana
        ventana = tk.Toplevel(self.root)
        ventana.title("Duración Promedio de Películas por Año")
        ventana.geometry("1000x600")

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(duracion_por_anio.index, duracion_por_anio.values,
                marker='s', linewidth=2, color='#4CAF50', markersize=6)

        ax.set_xlabel('Año', fontsize=12, fontweight='bold')
        ax.set_ylabel('Duración Promedio (minutos)', fontsize=12, fontweight='bold')
        ax.set_title('Evolución de la Duración Promedio de Películas',
                     fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')

        # Añadir línea de tendencia
        z = np.polyfit(duracion_por_anio.index, duracion_por_anio.values, 1)
        p = np.poly1d(z)
        ax.plot(duracion_por_anio.index, p(duracion_por_anio.index),
                "--", color='red', alpha=0.6, label='Tendencia')
        ax.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Incrustar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Guardar
        os.makedirs('output/charts', exist_ok=True)
        fig.savefig('output/charts/duracion_por_anio.png', dpi=300, bbox_inches='tight')

        self.helpers.log("\nGráfico de duración promedio por año generado")
        self.helpers.log(f"Guardado en: output/charts/duracion_por_anio.png")

    def grafico_rating_por_genero(self):
        """Crea gráfico de barras horizontales con rating promedio por género"""
        if self.helpers.datos_no_cargados():
            return

        # Calcular rating promedio por género (excluir nulos)
        df_con_rating = self.df[self.df['avg_rating'].notna() & self.df['genre'].notna()].copy()

        if len(df_con_rating) == 0:
            self.helpers.log("No hay datos de rating por género")
            return

        rating_por_genero = df_con_rating.groupby('genre')['avg_rating'].mean().sort_values(ascending=True)

        # Crear ventana
        ventana = tk.Toplevel(self.root)
        ventana.title("Rating Promedio por Género")
        ventana.geometry("1000x600")

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 8))

        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(rating_por_genero)))
        ax.barh(range(len(rating_por_genero)), rating_por_genero.values, color=colors)
        ax.set_yticks(range(len(rating_por_genero)))
        ax.set_yticklabels(rating_por_genero.index)

        ax.set_xlabel('Rating Promedio', fontsize=12, fontweight='bold')
        ax.set_ylabel('Género', fontsize=12, fontweight='bold')
        ax.set_title('Rating Promedio por Género de Película',
                     fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        # Añadir valores en las barras
        for i, v in enumerate(rating_por_genero.values):
            ax.text(v + 0.1, i, f'{v:.2f}', va='center', fontsize=10)

        plt.tight_layout()

        # Incrustar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Guardar
        os.makedirs('output/charts', exist_ok=True)
        fig.savefig('output/charts/rating_por_genero.png', dpi=300, bbox_inches='tight')

        self.helpers.log(f"Guardado en: output/charts/rating_por_genero.png")
        self.helpers.log("\nGráfico de rating por género generado")

    def tabla_estadisticas_genero(self):
        """Muestra tabla con estadísticas por género"""
        if self.helpers.datos_no_cargados():
            return

        # Filtrar datos válidos
        df_valido = self.df[self.df['genre'].notna()].copy()

        # Calcular estadísticas por género
        estadisticas = df_valido.groupby('genre').agg({
            'mov_title': 'count',
            'avg_rating': 'mean',
            'mov_time': 'mean',
            'mov_year': ['min', 'max']
        }).round(2)

        # Renombrar columnas
        estadisticas.columns = ['Num_Películas', 'Rating_Promedio',
                                'Duración_Promedio', 'Año_Min', 'Año_Max']
        estadisticas = estadisticas.reset_index()

        # Mostrar en ventana
        self.mostrar_dataframe(estadisticas, "Estadísticas por Género")

        self.helpers.log("\nTabla de estadísticas por género generada")

    def grafico_top_directores(self):
        """Crea gráfico con los directores con más películas"""
        if self.helpers.datos_no_cargados():
            return

        # Contar películas por director (excluir nulos)
        df_directores = self.df[self.df['director_name'].notna()].copy()
        top_directores = df_directores['director_name'].value_counts().head(10)

        # Crear ventana
        ventana = tk.Toplevel(self.root)
        ventana.title("Top 10 Directores")
        ventana.geometry("1000x600")

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6))

        colors = plt.cm.Paired(range(len(top_directores)))
        ax.bar(range(len(top_directores)), top_directores.values, color=colors)
        ax.set_xticks(range(len(top_directores)))
        ax.set_xticklabels(top_directores.index, rotation=45, ha='right')

        ax.set_xlabel('Director', fontsize=12, fontweight='bold')
        ax.set_ylabel('Número de Películas', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Directores con Más Películas',
                     fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        # Añadir valores
        for i, v in enumerate(top_directores.values):
            ax.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()

        # Incrustar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Guardar
        os.makedirs('output/charts', exist_ok=True)
        fig.savefig('output/charts/top_directores.png', dpi=300, bbox_inches='tight')

        self.helpers.log("\nGráfico de top directores generado")
        self.helpers.log(f"Guardado en: output/charts/top_directores.png")

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
    app = AnalysisVisualization(root)
    root.mainloop()


if __name__ == "__main__":
    main()