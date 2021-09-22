# Como la base de datos que se eligio para almacenar los datos es sqlite3, procedemos a importarla
import sqlite3
# Se agrega también Error para capturar los posibles errores durante la connexion
from sqlite3 import Error


# Se crea la connexion, como parameter se le pasa el nombre de la base de datos
def crear_conexión(db_file):
    conn = None

    # Se utiliza un try except para mandar un mensaje a consola si la connexion fue exitosa o no
    try:
        conn = sqlite3.connect(db_file)
        print("Connexion Exitosa")
    except Error as e:
        print(e)
    return conn


# Se retorna la connexion para ser utiliza posteriormente ingresando los datos

# Creation de la tabla
def crear_tabla(conn):
    # Creo un cursor para ejecutar código SQL
    cursorObj = conn.cursor()
    cursorObj.execute("DROP TABLE IF EXISTS tiempos")
    # Creo dos execute uno para eliminar una posible duplicidad de mi tabla y la otra para
    # establecer sus parameters
    cursorObj.execute("CREATE TABLE tiempos(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                      "tiempo_total REAL NOT NULL,tiempo_promedio REAL NOT NULL,"
                      "tiempo_minimo REAL NOT NULL,tiempo_maximo REAL NOT NULL)")
    # Un commit para guardar los cambios en la base de datos
    conn.commit()


# Por buenas practicas cierro la base datos para evitar fuga de information
def cerrar_db(conn):
    if conn is not None:
        conn.close()