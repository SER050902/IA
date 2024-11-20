import tkinter as tk
from tkinter import messagebox
from db_queries import query_database
from nlp_utils import extract_entities_and_dates
from openai_integration import ask_openai

def handle_question(question):
    """
    Maneja la pregunta del usuario: extrae entidades, verifica fechas y utiliza OpenAI si es necesario.
    """
    student_name, dates = extract_entities_and_dates(question)

    if student_name:
        context = query_database(student_name)
        if "No hay" in context or "Error" in context:
            return ask_openai(question, context)

        return context
    else:
        return "No pude identificar el nombre del estudiante en tu pregunta. Por favor, especifica mejor."


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

