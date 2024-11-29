import sqlite3

# Ruta del archivo de base de datos
db_path = "students.db"

# Conectar a la base de datos
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Consultar las tablas disponibles
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

if tables:
    print("Tablas encontradas en la base de datos:")
    for table in tables:
        print(f"- {table[0]}")

    # Mostrar columnas y datos de cada tabla
    for table in tables:
        table_name = table[0]
        print(f"\nTabla: '{table_name}'")

        # Obtener las columnas de la tabla
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        print("Columnas:", ", ".join(column_names))

        # Mostrar los datos de la tabla
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        print("Datos:")
        if rows:
            for row in rows:
                print(dict(zip(column_names, row)))
        else:
            print("La tabla está vacía.")
else:
    print("No se encontraron tablas en la base de datos.")

# Cerrar la conexión
connection.close()
