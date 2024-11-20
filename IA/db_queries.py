import sqlite3
from config import DATABASE_PATH

def connect_to_db():
    """
    Establece conexión con la base de datos SQLite.
    """
    try:
        return sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        raise Exception(f"Error al conectar con la base de datos: {e}")


def query_database(student_name):
    """
    Consulta múltiples tablas de la base de datos SQLite para obtener información sobre un estudiante.
    """
    if not student_name:
        return "Por favor, proporciona el nombre del estudiante."

    conn = connect_to_db()

    try:
        cursor = conn.cursor()

        # Consultar exámenes
        cursor.execute("SELECT exam_date, grade FROM exams WHERE student_name=?", (student_name,))
        exams = cursor.fetchall()

        # Consultar notas
        cursor.execute("""
            SELECT n.modulo, n.nota 
            FROM notas n
            INNER JOIN students s ON s.id = n.alumno_id
            WHERE s.name=?
        """, (student_name,))
        grades = cursor.fetchall()

        # Crear el mensaje contextual
        context = []
        if exams:
            exam_info = ", ".join([f"{date} (nota: {grade})" for date, grade in exams])
            context.append(f"Exámenes: {exam_info}.")
        else:
            context.append("No hay exámenes registrados.")

        if grades:
            grade_info = ", ".join([f"{modulo}: {nota}" for modulo, nota in grades])
            context.append(f"Notas: {grade_info}.")
        else:
            context.append("No hay notas registradas.")

        return " ".join(context)

    except sqlite3.Error as e:
        return f"Error al consultar la base de datos: {e}"

    finally:
        conn.close()
