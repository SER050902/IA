import sqlite3

# Ruta de la base de datos SQLite
DATABASE_PATH = 'students.db'

# Función para conectar a la base de datos
def connect_to_db():
    try:
        return sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Función para borrar la tabla 'ufs'
def drop_ufs_table():
    conn = connect_to_db()
    if not conn:
        return "No se pudo establecer conexión con la base de datos."

    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS ufs")  # Borrar la tabla 'ufs' si existe
        conn.commit()
        conn.close()
        return "La tabla 'ufs' ha sido eliminada con éxito."
    except sqlite3.Error as e:
        return f"Error al eliminar la tabla 'ufs': {e}"

# Llamar a la función para eliminar la tabla
print(drop_ufs_table())
