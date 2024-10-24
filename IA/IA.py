import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests

# Conectar a la base de datos SQLite
def connect_to_db():
    return sqlite3.connect('students.db')

# Función para obtener horarios desde la base de datos
def obtener_horarios():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM horarios")  # Consulta de ejemplo
        horarios = cursor.fetchall()
        text_horarios.delete("1.0", tk.END)
        for horario in horarios:
            text_horarios.insert(tk.END, f"Curso: {horario[1]}, Hora: {horario[2]}-{horario[3]}, Días: {horario[4]}\n")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los horarios: {e}")

# Función para consultar notas de un estudiante
def consultar_notas():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        alumno_id = entry_alumno.get()
        cursor.execute("SELECT modulo, nota FROM notas WHERE alumno_id = ?", (alumno_id,))
        notas = cursor.fetchall()
        text_notas.delete("1.0", tk.END)
        for nota in notas:
            text_notas.insert(tk.END, f"Módulo: {nota[0]}, Nota: {nota[1]}\n")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener las notas: {e}")

# Función para hacer consultas a la IA
def consultar_ia(pregunta):
    try:
        url = "https://api.openai.com/v1/chat/completions"  # URL de la API de OpenAI
        headers = {
            "Authorization": "sk-l7asCE9b4lKbPe0FLSGBS7V6WggZoG0P94Fi_gP6hIT3BlbkFJWmEWTORlIdvTw6VcgBH6byDffCPQ2zQ_iT7I2QwqAA",  # Tu token de AP
        }
        payload = {
            "model": "gpt-3.5-turbo",  # O "gpt-4" si tienes acceso
            "messages": [{"role": "user", "content": pregunta}],
            "max_tokens": 100  # Ajusta según lo que necesites
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta de la IA")
        else:
            return "Error al contactar la IA"
    except Exception as e:
        return f"Error: {e}"

# Función para manejar las consultas al chat con IA
def chat_ia():
    pregunta = text_pregunta.get("1.0", tk.END).strip()
    if pregunta:
        respuesta = consultar_ia(pregunta)
        text_respuesta.delete("1.0", tk.END)
        text_respuesta.insert(tk.END, respuesta)
    else:
        messagebox.showerror("Error", "Por favor, ingrese una pregunta.")

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Sistema Académico con IA")
root.geometry("800x600")

# Sección de horarios
label_horarios = tk.Label(root, text="Horarios de Cursos:")
label_horarios.pack()
btn_horarios = tk.Button(root, text="Consultar Horarios", command=obtener_horarios)
btn_horarios.pack()
text_horarios = tk.Text(root, height=5, width=80)
text_horarios.pack()

# Sección de notas
label_alumno = tk.Label(root, text="ID del Alumno:")
label_alumno.pack()
entry_alumno = tk.Entry(root)
entry_alumno.pack()
btn_notas = tk.Button(root, text="Consultar Notas", command=consultar_notas)
btn_notas.pack()
text_notas = tk.Text(root, height=5, width=80)
text_notas.pack()

# Sección del chat con IA
label_chat = tk.Label(root, text="Chat con IA:")
label_chat.pack()
text_pregunta = tk.Text(root, height=3, width=80)
text_pregunta.pack()
btn_chat = tk.Button(root, text="Consultar IA", command=chat_ia)
btn_chat.pack()
text_respuesta = tk.Text(root, height=5, width=80)
text_respuesta.pack()

# Iniciar la aplicación
root.mainloop()
