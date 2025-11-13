# Análisis de Películas con Pandas

## Herramientas Usadas

[Python 3.12](https://www.python.org/)

[Pandas](https://pandas.pydata.org/)

[MySQL](https://www.mysql.com/)

[Tkinter](https://docs.python.org/es/3/library/tkinter.html)

[Docker](https://www.docker.com/)

---

## Instalación y Ejecución del Proyecto

1. **Clonar el repositorio**

    ```bash
      git clone https://github.com/Nisanech/pandas_movie_database
    ```
       
    ```bash
      cd pandas_movie_database
    ```
   
2. **Crear un entorno virtual en Windows**

    ```bash
      python -m venv venv
    ```

    ```bash
      .\venv\Scripts\activate
    ```

3. **Instalar las dependencias**

    ```bash
      pip install -r requirements.txt
    ```
    
4. Crear en la raiz del proyecto el archivo `.env` con las siguientes variables de entorno:
   
    ```
        DB_HOST=localhost
        DB_PORT=3307
        DB_PORT_EXTERNAL=3307
        DB_USER=movieuser
        DB_PASSWORD=moviepassword
        DB_NAME=movies
        
        MYSQL_ROOT_PASSWORD=rootpassword
        MYSQL_DATABASE=movies
        MYSQL_USER=movieuser
        MYSQL_PASSWORD=moviepassword
   ```

5. **Construir la imagen de Docker**

    Iniciar la aplicación de Docker Desktop y ejecutar el siguiente comando en la terminal:

    ```bash
      docker-compose build --no-cache
    ```
   
    Una vez se construya la imagen, iniciar el contenedor de la base de datos:

    ```bash
      docker-compose up -d
    ```
   
## Ejecutar el Proyecto

Para ejecutar el proyecto, ejecutar el siguiente comando:

```bash
    python .\src\main.py
```
