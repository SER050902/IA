import tkinter as tk
from tkinter import messagebox
import sqlite3
import spacy
from dateutil.parser import parse
from datetime import datetime
import os
import openai

# Configurar spaCy y OpenAI
nlp = spacy.load("es_core_news_sm")
openai.api_key = os.getenv("OPENAI_API_KEY")  # Configura tu clave API en una variable de entorno

# Ruta de la base de datos SQLite
DATABASE_PATH = 'students.db'


# Función para conectar a la base de datos
def connect_to_db():
    try:
        return sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
        return None


# Función para extraer entidades y fechas de una pregunta
def extract_entities_and_dates(question):
    """
    Extrae el nombre del estudiante y las fechas de una pregunta usando spaCy.
    """
    doc = nlp(question)
    student_name = None
    dates = []

    for ent in doc.ents:
        if ent.label_ == "PER":
            student_name = ent.text.strip()
        elif ent.label_ == "DATE":
            try:
                date = parse(ent.text, fuzzy=True)
                dates.append(date)
            except ValueError:
                pass  # Ignorar fechas no válidas

    return student_name, dates


# Función para consultar la base de datos
def query_database(student_name):
    """
    Consulta múltiples tablas de la base de datos SQLite para obtener información sobre un estudiante.
    """
    if not student_name:
        return "Por favor, proporciona el nombre del estudiante."

    conn = connect_to_db()
    if not conn:
        return "No se pudo establecer conexión con la base de datos."

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

        conn.close()
        return " ".join(context)

    except sqlite3.Error as e:
        return f"Error al consultar la base de datos: {e}"


# Función para realizar consultas a OpenAI
def ask_openai(question, context):
    """
    Realiza una consulta a la API de OpenAI con el contexto y la pregunta del usuario.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente académico que responde preguntas de forma detallada y clara. Utiliza el contexto disponible para enriquecer tus respuestas, pero sé flexible y natural."},
                {"role": "user", "content": f"Contexto: {context}\nPregunta: {question}"}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error al conectar con OpenAI: {e}"



# Función principal para manejar preguntas
def handle_question(question):
    """
    Maneja la pregunta del usuario: extrae entidades, verifica fechas y utiliza OpenAI si es necesario.
    """
    student_name, dates = extract_entities_and_dates(question)

    if student_name:
        context = query_database(student_name)  # Consultar base de datos para construir un contexto
        # Aquí llamamos a OpenAI incluso si hay contexto disponible
        return ask_openai(question, context)
    else:
        return "No pude identificar el nombre del estudiante en tu pregunta. Por favor, especifica mejor."


# Función de la interfaz para manejar consultas
def consultar_ia():
    pregunta = text_pregunta.get("1.0", tk.END).strip()
    if pregunta:
        respuesta = handle_question(pregunta)
        text_respuesta.delete("1.0", tk.END)
        text_respuesta.insert(tk.END, respuesta)
    else:
        messagebox.showerror("Error", "Por favor, ingresa una pregunta.")


# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Sistema Académico con IA")
root.geometry("800x600")

# Etiqueta y área de texto para la pregunta
label_chat = tk.Label(root, text="Escribe tu pregunta:")
label_chat.pack()
text_pregunta = tk.Text(root, height=3, width=80)
text_pregunta.pack()

# Botón para enviar la pregunta
btn_chat = tk.Button(root, text="Consultar", command=consultar_ia)
btn_chat.pack()

# Área de texto para mostrar la respuesta
label_respuesta = tk.Label(root, text="Respuesta:")
label_respuesta.pack()
text_respuesta = tk.Text(root, height=5, width=80)
text_respuesta.pack()

# Iniciar la aplicación
root.mainloop()