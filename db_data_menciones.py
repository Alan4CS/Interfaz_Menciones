import mysql.connector
import pandas as pd

def menciones_database():

    # Configura tu conexión a la base de datos MySQL
    conexion = mysql.connector.connect(
        host="laclicsa.online",
        user="Admin1",
        password="admin_123!",
        database="twitter_database"
    )

    # Crea un cursor para ejecutar consultas SQL
    cursor = conexion.cursor()

    # Ejecuta una consulta SQL para obtener el usuario a buscar
    consulta = "SELECT * FROM menciones_users;"
    cursor.execute(consulta)

    # Recupera el resultado de la consulta
    resultado = cursor.fetchall()


# Obtiene los nombres de las columnas de la tabla
    columnas = [i[0] for i in cursor.description]

    # Crea un DataFrame de Pandas a partir de los resultados y las columnas
    df_menciones = pd.DataFrame(resultado, columns=columnas).set_index(columnas[0])

    # Cierra el cursor y la conexión
    cursor.close()
    conexion.close()

    opciones_usuario = [{'label': usuario, 'value': usuario} for usuario in df_menciones['usuario_twitter'].unique()]
    #print(opciones_usuario)

    return df_menciones,opciones_usuario

