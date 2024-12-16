# Se importa la libreria para PostgreSQL
import psycopg2

# ***** Conexion *****
def connection_postgresql():
    # Se genera la conexión con la base de datos
    try:
        credenciales = {
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
            # Producción
            "password": "123456",
            "dbname": "spei"
        }
    
        conexion = psycopg2.connect(**credenciales)
        conexion.autocommit = True
        
    except psycopg2.Error as e:
        print("ERROR:", e)

    # *** Validación de usuarios ***

    # Se abre un cursor para realizar las operaciones en la base de datos
    cursor = conexion.cursor()

    return cursor

        
