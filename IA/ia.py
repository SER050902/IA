import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox
import sqlite3
import spacy
from dateutil.parser import parse
import os
import openai

# Configuración de spaCy y OpenAI
nlp = spacy.load("es_core_news_sm")
openai.api_key = os.getenv("OPENAI_API_KEY")  # Configura tu clave API en una variable de entorno

# Ruta de la base de datos SQLite
DATABASE_PATH = 'students.db'


# Funciones relacionadas con la base de datos
def connect_to_db():
    """Conecta a la base de datos SQLite."""
    try:
        return sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
        return None


def query_database(student_name=None, class_name=None, module_name=None):
    """Consulta la base de datos según los parámetros proporcionados."""
    conn = connect_to_db()
    if not conn:
        return "No se pudo establecer conexión con la base de datos."

    try:
        cursor = conn.cursor()
        context = []

        if student_name:
            cursor.execute("""
                SELECT clase_id, nombre FROM alumnos WHERE LOWER(nombre) LIKE LOWER(?) 
            """, (f'%{student_name}%',))
            students = cursor.fetchall()

            if students:
                for student in students:
                    class_id = student[0]
                    cursor.execute("SELECT nombre, aula, piso FROM clases WHERE id=?", (class_id,))
                    class_info = cursor.fetchone()
                    if class_info:
                        context.append(
                            f"Estudiante: {student[1]}, Clase: {class_info[0]} (Aula: {class_info[1]}, Piso: {class_info[2]})."
                        )
                    else:
                        context.append(f"No se encontró información de clase para el estudiante {student[1]}.")
            else:
                context.append(f"No se encontró al estudiante {student_name}.")

        if class_name:
            cursor.execute("SELECT id, aula, piso FROM clases WHERE LOWER(nombre) LIKE LOWER(?)", (f'%{class_name}%',))
            class_info = cursor.fetchone()
            if class_info:
                context.append(f"La clase {class_name} está en el Aula {class_info[1]}, Piso {class_info[2]}.")
                cursor.execute("SELECT nombre, horario FROM modulos WHERE clase_id=?", (class_info[0],))
                modules = cursor.fetchall()
                if modules:
                    mod_info = ", ".join([f"{module[0]} (Horario: {module[1]})" for module in modules])
                    context.append(f"Módulos asignados: {mod_info}.")
                else:
                    context.append(f"No hay módulos asignados para la clase {class_name}.")
            else:
                context.append(f"No se encontró la clase {class_name}.")

        if module_name:
            cursor.execute("""
                SELECT nombre, horario FROM modulos WHERE LOWER(nombre) LIKE LOWER(?) 
            """, (f'%{module_name}%',))
            module_info = cursor.fetchall()
            if module_info:
                for module in module_info:
                    context.append(f"Módulo: {module[0]}, Horario: {module[1]}.")
            else:
                context.append(f"No se encontró el módulo {module_name}.")

        conn.close()
        return " ".join(context) if context else "No se encontró información."

    except sqlite3.Error as e:
        return f"Error al consultar la base de datos: {e}"


# Funciones relacionadas con OpenAI
def ask_openai(question, context):
    """Consulta la API de OpenAI con el contexto y la pregunta."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "Eres un asistente académico que responde preguntas de forma clara y detallada."},
                {"role": "user", "content": f"Contexto: {context}\nPregunta: {question}"}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error al conectar con OpenAI: {e}"


# Función principal
def handle_question(question):
    """Procesa la pregunta del usuario, extrae entidades y consulta base de datos o OpenAI."""
    doc = nlp(question)
    student_name = None
    class_name = None
    module_name = None
    date = None

    for ent in doc.ents:
        if ent.label_ == "PER":
            student_name = ent.text.strip()
        elif ent.label_ == "ORG":
            class_name = ent.text.strip()
        elif ent.label_ == "MISC":
            module_name = ent.text.strip()
        elif ent.label_ == "DATE":
            try:
                date = parse(ent.text).date()
            except ValueError:
                pass

    if student_name or class_name or module_name or date:
        context = query_database(student_name, class_name, module_name)
        return ask_openai(question, context)
    else:
        return "No pude identificar información suficiente en tu pregunta. Por favor, especifica mejor."


# Función de la interfaz para manejar consultas
def consultar_ia():
    pregunta = text_pregunta.get("1.0", tk.END).strip()
    if pregunta:
        respuesta = handle_question(pregunta)
        text_respuesta.delete("1.0", tk.END)
        text_respuesta.insert(tk.END, respuesta)
    else:
        messagebox.showerror("Error", "Por favor, ingresa una pregunta.")


# Interfaz gráfica mejorada con ttk
root = tk.Tk()
root.title("Sistema Académico con IA")
root.geometry("800x600")
root.configure(bg="#f5f5f5")  # Fondo claro

# Estilo general
style = ttk.Style()
style.theme_use("clam")  # Tema moderno
style.configure("TLabel", font=("Helvetica", 12), background="#f5f5f5")
style.configure("TButton", font=("Helvetica", 12), background="#0078d7", foreground="white", padding=6)
style.configure("TFrame", background="#f5f5f5")

# Marco principal
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Etiqueta y área de texto para la pregunta
label_pregunta = ttk.Label(main_frame, text="Escribe tu pregunta:")
label_pregunta.pack(anchor="w", pady=5)
text_pregunta = tk.Text(main_frame, height=5, font=("Helvetica", 12), wrap=tk.WORD)
text_pregunta.pack(fill=tk.X, pady=5)

# Botón para enviar la pregunta
btn_chat = ttk.Button(main_frame, text="Consultar", command=consultar_ia)
btn_chat.pack(pady=10)

# Área de texto para mostrar la respuesta con barra de desplazamiento
label_respuesta = ttk.Label(main_frame, text="Respuesta:")
label_respuesta.pack(anchor="w", pady=5)
text_respuesta = scrolledtext.ScrolledText(main_frame, height=15, font=("Helvetica", 12), wrap=tk.WORD)
text_respuesta.pack(fill=tk.BOTH, expand=True, pady=5)

# Ejecutar la aplicación
root.mainloop()
