import aiomysql #Librería async para MySQL

#configuracion de conexion

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "db": "citas_medicas"
}

#función de conexión

async def get_connection():
    """
    Crea una conexión async con la base de datos
    """
    return await aiomysql.connect(**DB_CONFIG)