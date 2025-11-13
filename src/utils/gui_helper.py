import tkinter as tk
from tkinter import scrolledtext
from src.config.db_connector import MoviesDatabase


class GUIHelper:
    def __init__(self, text_area: scrolledtext.ScrolledText):
        self.text_area = text_area
        self.db = MoviesDatabase()
        self.df = None

    def log(self, message: str):
        """Escribe texto en el área de resultados"""
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    def limpiar_log(self):
        """Limpia el área de resultados"""
        self.text_area.delete(1.0, tk.END)

    def datos_no_cargados(self):
        """Verifica si hay datos cargados"""
        if self.df is None:
            self.limpiar_log()
            self.log("No hay datos cargados.\n")
            return True
        return False

    def cargar_datos(self):
        """Carga datos desde la base de datos y los almacena en self.df"""
        self.limpiar_log()
        self.log("=" * 70)
        self.log("CARGANDO DATOS DE LA BASE DE DATOS...")
        self.log("=" * 70)

        if not self.db.test_connection():
            self.log("Error: No se pudo conectar a la base de datos.")
            return None

        self.df = self.db.get_complete_movie_info()

        if self.df is not None and len(self.df) > 0:
            self.log("\nDatos cargados correctamente")
            self.log(f"Total de registros: {len(self.df)}")
            self.log(f"Columnas: {list(self.df.columns)}")
        else:
            self.log("Error: No se pudieron cargar los datos.")

        return self.df
