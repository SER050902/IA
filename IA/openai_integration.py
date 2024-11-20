import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY



def ask_openai(question, context):
    """
    Realiza una consulta a la API de OpenAI con el contexto y la pregunta del usuario.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente que responde preguntas académicas de manera precisa."},
                {"role": "user", "content": f"Contexto: {context}\nPregunta: {question}"}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error al conectar con OpenAI: {e}"
