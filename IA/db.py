import sqlite3

# Ruta de la base de datos
DATABASE_PATH = 'students.db'


def insert_sample_data():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Insertar estudiantes
    cursor.execute("INSERT INTO students (name, email, date_of_birth) VALUES (?, ?, ?)",
                   ("Juan Pérez", "juanperez@email.com", "2000-05-15"))
    cursor.execute("INSERT INTO students (name, email, date_of_birth) VALUES (?, ?, ?)",
                   ("Ana García", "anagarcia@email.com", "1999-10-10"))

    # Insertar exámenes
    cursor.execute("INSERT INTO exams (student_name, exam_date, grade) VALUES (?, ?, ?)",
                   ("Juan Pérez", "2024-06-15", 8.5))
    cursor.execute("INSERT INTO exams (student_name, exam_date, grade) VALUES (?, ?, ?)",
                   ("Ana García", "2024-06-16", 9.0))

    # Insertar notas
    cursor.execute("INSERT INTO notas (alumno_id, modulo, nota) VALUES (?, ?, ?)", (1, "Matemáticas", 7.5))
    cursor.execute("INSERT INTO notas (alumno_id, modulo, nota) VALUES (?, ?, ?)", (1, "Física", 8.0))
    cursor.execute("INSERT INTO notas (alumno_id, modulo, nota) VALUES (?, ?, ?)", (2, "Matemáticas", 9.5))
    cursor.execute("INSERT INTO notas (alumno_id, modulo, nota) VALUES (?, ?, ?)", (2, "Física", 9.0))

    conn.commit()
    conn.close()


# Llamar a la función para insertar datos de ejemplo
insert_sample_data()

