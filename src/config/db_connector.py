import os
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class MoviesDatabase:
    # ============================================
    # Métodos de conexión
    # ============================================
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', 'root')
        self.database = os.getenv('DB_NAME', 'movies')

        # Crear engine de SQLAlchemy para pandas
        self.connection_string = (
            f"mysql+pymysql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )
        self.engine = create_engine(self.connection_string)

    def test_connection(self) -> bool:
        try:
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            connection.close()
            print("😎 Conectado a la base de datos")
            return True
        except Exception as exception:
            print(f"📛 Error al conectar a la base de datos: {exception}")
            return False

    def execute_query(self, query: str) -> pd.DataFrame:
        try:
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as exception:
            print(f"Error al ejecutar la consulta: {exception}")
            return pd.DataFrame()

    # ============================================
    # Métodos para consultas compuestas
    # ============================================
    def get_complete_movie_info(self) -> pd.DataFrame:
        query = """
        SELECT
            m.mov_id,
            m.mov_title,
            m.mov_year,
            m.mov_time,
            m.mov_lang,
            m.mov_rel_country,
            CONCAT(d.dir_fname, ' ', d.dir_lname) as director_name,
            g.gen_title as genre,
            AVG(r.rev_stars) as avg_rating,
            AVG(r.num_o_ratings) as avg_num_ratings
        FROM movie m
        LEFT JOIN movie_direction md ON m.mov_id = md.mov_id
        LEFT JOIN director d ON md.dir_id = d.dir_id
        LEFT JOIN movie_genres mg ON m.mov_id = mg.mov_id
        LEFT JOIN genres g ON mg.gen_id = g.gen_id
        LEFT JOIN rating r ON m.mov_id = r.mov_id
        GROUP BY m.mov_id, m.mov_title, m.mov_year, m.mov_time, 
                 m.mov_lang, m.mov_rel_country, director_name, g.gen_title
        """

        return self.execute_query(query)

    def close_connection(self):
        self.engine.dispose()
        print("🥸 Desconectado de la base de datos")