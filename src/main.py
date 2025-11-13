"""
Menú Principal - Análisis de Películas con Pandas
=================================================
"""


import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

sys.path.append('/app')

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Películas con Pandas")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')

        # Centrar ventana
        self.center_window()

        self.setup_ui()

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Encabezado
        header_frame = tk.Frame(self.root, bg='#1976D2', height=120)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(
            header_frame,
            text="ANÁLISIS DE PELÍCULAS CON PANDAS",
            font=("Arial", 20, "bold"),
            bg='#1976D2',
            fg='white',
            pady=20
        )
        title_label.pack()

        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Descripción
        desc_frame = tk.LabelFrame(
            main_frame,
            text="Descripción del Proyecto",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333'
        )
        desc_frame.pack(fill=tk.X, pady=10)

        desc_text = tk.Label(
            desc_frame,
            text="Proyecto: Fundamentos de pandas para manejo de bases de datos\n"
                 "Introducción a pandas: dataframes y series.\n"
                 "Importación y exportación de datos.\n"
                 "Indexación básica y avanzada\n"
                 "Métodos para eliminar o reemplazar valores faltantes\n",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#555',
            justify=tk.LEFT,
            pady=10
        )
        desc_text.pack(padx=10)

        # Temas
        temas_frame = tk.LabelFrame(
            main_frame,
            text="Selecciona un Tema",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333'
        )
        temas_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Botones de temas
        temas = [
            {
                'numero': '1',
                'titulo': 'DataFrames y Series',
                'descripcion': 'Exploración inicial de datos',
                'color': '#4CAF50',
                'archivo': 'themes/theme1_dataframes_series.py'
            },
            {
                'numero': '2',
                'titulo': 'Importación y Exportación',
                'descripcion': 'Manejo de archivos Excel',
                'color': '#2196F3',
                'archivo': 'themes/theme2_import_export.py'
            },
            {
                'numero': '3',
                'titulo': 'Indexación Básica y Avanzada',
                'descripcion': 'Filtrado y selección de datos',
                'color': '#FF9800',
                'archivo': 'themes/theme3_indexing.py'
            },
            {
                'numero': '4',
                'titulo': 'Manejo de Valores Faltantes',
                'descripcion': 'Limpieza e imputación de datos',
                'color': '#9C27B0',
                'archivo': 'themes/theme4_missing_values.py'
            },
            {
                'numero': '5',
                'titulo': 'Análisis y Visualización',
                'descripcion': 'Gráficos y análisis estadístico',
                'color': '#00BCD4',
                'archivo': 'themes/theme5_analysis_visualization.py'
            }
        ]

        for i, tema in enumerate(temas):
            self.crear_boton_tema(temas_frame, tema, i)

        # Footer
        footer_frame = tk.Frame(self.root, bg='#333', height=60)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        footer_label = tk.Label(
            footer_frame,
            text="Cada módulo es independiente y puede ejecutarse por separado\n"
                 "Desarrollado con Python, Pandas, Tkinter y MySQL",
            font=("Arial", 9),
            bg='#333',
            fg='white',
            pady=10
        )
        footer_label.pack()

    def crear_boton_tema(self, parent, tema, row):
        """Crea un botón estilizado para cada tema"""
        # Frame del botón
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        # Botón principal
        btn = tk.Button(
            button_frame,
            text=f"  TEMA {tema['numero']}  ",
            font=("Arial", 11, "bold"),
            bg=tema['color'],
            fg='white',
            width=12,
            height=2,
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.abrir_tema(tema['archivo'])
        )
        btn.pack(side=tk.LEFT, padx=(0, 10))

        # Información del tema
        info_frame = tk.Frame(button_frame, bg='#f0f0f0')
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        titulo_label = tk.Label(
            info_frame,
            text=tema['titulo'],
            font=("Arial", 11, "bold"),
            bg='#f0f0f0',
            fg='#333',
            anchor='w'
        )
        titulo_label.pack(anchor='w')

        desc_label = tk.Label(
            info_frame,
            text=tema['descripcion'],
            font=("Arial", 9),
            bg='#f0f0f0',
            fg='#666',
            anchor='w'
        )
        desc_label.pack(anchor='w')

        # Efectos hover
        btn.bind('<Enter>', lambda e: btn.config(bg=self.lighten_color(tema['color'])))
        btn.bind('<Leave>', lambda e: btn.config(bg=tema['color']))


    def lighten_color(self, color):
        """Aclara un color hexadecimal"""
        # Conversión simple para efecto hover
        color_map = {
            '#4CAF50': '#66BB6A',
            '#2196F3': '#42A5F5',
            '#FF9800': '#FFA726',
            '#9C27B0': '#AB47BC',
            '#00BCD4': '#26C6DA'
        }
        return color_map.get(color, color)

    def abrir_tema(self, archivo):
        """Abre un módulo de tema específico"""
        try:
            # Construir la ruta del archivo
            script_dir = os.path.dirname(os.path.abspath(__file__))
            archivo_path = os.path.join(script_dir, archivo)

            if not os.path.exists(archivo_path):
                messagebox.showerror(
                    "Error",
                    f"No se encontró el archivo: {archivo}"
                )
                return

            # Ejecutar el script en un nuevo proceso
            subprocess.Popen([sys.executable, archivo_path])

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al abrir el módulo:\n{str(e)}"
            )

def main():
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()

