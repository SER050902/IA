import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3
import spacy
import os
import openai

# Configuración de spaCy y OpenAI
nlp = spacy.load("es_core_news_sm")
openai.api_key = os.getenv("OPENAI_API_KEY")  # Configura tu clave API en una variable de entorno

# Ruta de la base de datos SQLite
DATABASE_PATH = 'students.db'

# Funciones relacionadas con la base de datos
def connect_to_db():
    try:
        return sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
        return None

def query_database(student_name=None, professor_name=None, module_name=None):
    conn = connect_to_db()
    if not conn:
        return "No se pudo establecer conexión con la base de datos."

    try:
        cursor = conn.cursor()
        context = []

        # Consultar información sobre estudiantes
        if student_name:
            cursor.execute("""
                SELECT a.nombre AS estudiante, 
                       m.modulo AS modulo, 
                       c.aula AS aula, 
                       c.piso AS piso, 
                       h.horario AS horario, 
                       p.nombre AS profesor
                FROM alumnos a
                JOIN clase c ON a.clase = c.id
                JOIN modulo m ON a.modulo = m.id
                JOIN profesor p ON m.profesor = p.id
                LEFT JOIN horario h ON m.id = h.modulo
                WHERE LOWER(a.nombre) LIKE LOWER(?)
            """, (f'%{student_name}%',))
            students = cursor.fetchall()

            if students:
                for student in students:
                    context.append(
                        f"Estudiante: {student[0]}, Módulo: {student[1]}, "
                        f"Aula: {student[2]}, Piso: {student[3]}, "
                        f"Horario: {student[4] or 'No asignado'}, Profesor: {student[5]}."
                    )
            else:
                context.append(f"No se encontró al estudiante {student_name}.")

        # Consultar información sobre profesores
        if professor_name:
            cursor.execute("""
                SELECT p.nombre AS profesor, 
                       m.modulo AS modulo, 
                       h.horario AS horario
                FROM profesor p
                JOIN modulo m ON p.id = m.profesor
                LEFT JOIN horario h ON m.id = h.modulo
                WHERE LOWER(p.nombre) LIKE LOWER(?)
            """, (f'%{professor_name}%',))
            professors = cursor.fetchall()

            if professors:
                for prof in professors:
                    context.append(
                        f"Profesor: {prof[0]}, Módulo: {prof[1]}, Horario: {prof[2] or 'No asignado'}."
                    )
            else:
                context.append(f"No se encontró al profesor {professor_name}.")

        # Consultar información sobre módulos
        if module_name:
            cursor.execute("""
                SELECT m.modulo AS nombre_modulo, 
                       h.horario AS horario, 
                       c.aula AS aula, 
                       c.piso AS piso, 
                       p.nombre AS profesor
                FROM modulo m
                JOIN clase c ON m.id = c.id
                LEFT JOIN horario h ON m.id = h.modulo
                LEFT JOIN profesor p ON m.profesor = p.id
                WHERE LOWER(m.modulo) LIKE LOWER(?)
            """, (f'%{module_name}%',))
            modules = cursor.fetchall()

            if modules:
                for module in modules:
                    context.append(
                        f"Módulo: {module[0]}, Horario: {module[1] or 'No asignado'}, "
                        f"Aula: {module[2]}, Piso: {module[3]}, Profesor: {module[4]}."
                    )
            else:
                context.append(f"No se encontró información sobre el módulo '{module_name}'.")

        # Consultar todos los horarios
        if not student_name and not professor_name and not module_name:
            cursor.execute("""
                SELECT m.modulo AS nombre_modulo, 
                       h.horario AS horario, 
                       c.aula AS aula, 
                       c.piso AS piso, 
                       p.nombre AS profesor
                FROM horario h
                JOIN modulo m ON h.modulo = m.id
                JOIN clase c ON m.id = c.id
                LEFT JOIN profesor p ON m.profesor = p.id
            """)
            all_schedules = cursor.fetchall()

            if all_schedules:
                for schedule in all_schedules:
                    context.append(
                        f"Módulo: {schedule[0]}, Horario: {schedule[1]}, "
                        f"Aula: {schedule[2]}, Piso: {schedule[3]}, Profesor: {schedule[4]}."
                    )
            else:
                context.append("No se encontraron horarios registrados en la base de datos.")

        conn.close()
        return " ".join(context) if context else "No se encontró información."

    except sqlite3.Error as e:
        return f"Error al consultar la base de datos: {e}"


# Funciones relacionadas con OpenAI
def ask_openai(question, context):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente académico que responde preguntas."},
                {"role": "user", "content": f"He consultado una base de datos académica y obtuve esta información: {context}. Con base en esto, responde la pregunta: {question}"}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error al conectar con OpenAI: {e}"

def handle_question(question):
    doc = nlp(question)
    student_name = None
    professor_name = None
    module_name = None

    # Identificar entidades reconocidas por spaCy
    for ent in doc.ents:
        if ent.label_ == "PER":  # Persona
            if "profesor" in question.lower() or "maestro" in question.lower():
                professor_name = ent.text.strip()
            elif "alumno" in question.lower() or "estudiante" in question.lower():
                student_name = ent.text.strip()

    # Método de respaldo: buscar nombres manualmente si spaCy falla
    if not student_name and not professor_name and not module_name:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()

            # Consultar nombres de estudiantes
            cursor.execute("SELECT nombre FROM alumnos;")
            all_students = [row[0].lower() for row in cursor.fetchall()]

            # Consultar nombres de profesores
            cursor.execute("SELECT nombre FROM profesor;")
            all_professors = [row[0].lower() for row in cursor.fetchall()]

            # Consultar nombres de módulos
            cursor.execute("SELECT modulo FROM modulo;")
            all_modules = [row[0].lower() for row in cursor.fetchall()]

            # Comparar palabras de la pregunta con los nombres en la base de datos
            tokens = question.lower().split()
            for token in tokens:
                if token in all_students:
                    student_name = token.capitalize()
                    break
                elif token in all_professors:
                    professor_name = token.capitalize()
                    break
                elif token in all_modules:
                    module_name = token.capitalize()
                    break

            conn.close()

    # Consultar la base de datos según las entidades detectadas
    if student_name:
        context = query_database(student_name=student_name)
        return ask_openai(question, context)
    elif professor_name:
        context = query_database(professor_name=professor_name)
        return ask_openai(question, context)
    elif module_name:
        context = query_database(module_name=module_name)
        return ask_openai(question, context)
    elif "horario" in question.lower():
        context = query_database()
        return ask_openai(question, context)
    else:
        return "No pude identificar suficiente información en tu pregunta. Por favor, sé más específico."


# Función de la interfaz para manejar consultas
def consultar_ia():
    pregunta = text_pregunta.get("1.0", tk.END).strip()
    if pregunta:
        respuesta = handle_question(pregunta)
        text_respuesta.delete("1.0", tk.END)
        text_respuesta.insert(tk.END, respuesta)
    else:
        messagebox.showerror("Error", "Por favor, ingresa una pregunta.")


# Interfaz gráfica
root = tk.Tk()
root.title("Sistema Académico con IA")
root.geometry("900x600")
root.configure(bg="#2b2b2b")
root.resizable(False, False)

# Estilo oscuro
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Arial", 12), background="#2b2b2b", foreground="#e1e1e1")
style.configure("BoldLabel.TLabel", font=("Arial", 14, "bold"), background="#2b2b2b", foreground="#ffffff")
style.configure("TButton", font=("Arial", 12), background="#0078d7", foreground="#ffffff", padding=8)
style.configure("Header.TLabel", font=("Arial", 20, "bold"), foreground="#ffffff")
style.configure("TText", font=("Arial", 12), foreground="#e1e1e1", background="#1e1e1e")

# Etiquetas
lbl_titulo = ttk.Label(root, text="Sistema Académico con IA", style="Header.TLabel")
lbl_titulo.pack(pady=20)

lbl_pregunta = ttk.Label(root, text="Ingresa tu pregunta:", style="BoldLabel.TLabel")
lbl_pregunta.pack(anchor="w", padx=20, pady=(10, 0))

# Cuadro de texto para la pregunta
text_pregunta = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=5, font=("Arial", 12), bg="#1e1e1e", fg="#e1e1e1", insertbackground="white")
text_pregunta.pack(padx=20, pady=10)

# Botón para enviar la consulta
btn_consultar = ttk.Button(root, text="Consultar", command=consultar_ia)
btn_consultar.pack(pady=10)

# Cuadro de texto para la respuesta
lbl_respuesta = ttk.Label(root, text="Respuesta:", style="BoldLabel.TLabel")
lbl_respuesta.pack(anchor="w", padx=20, pady=(20, 0))

text_respuesta = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15, font=("Arial", 12), bg="#1e1e1e", fg="#e1e1e1", insertbackground="white")
text_respuesta.pack(padx=20, pady=10)

# Ejecutar la interfaz
root.mainloop()