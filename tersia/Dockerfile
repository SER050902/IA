# Usa una imagen base de Python más ligera
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto y el requirements.txt
COPY . .
COPY requirements.txt .

# Establecer la clave API de OpenAI
ENV OPENAI_API_KEY="Tu llave api"

# Instalar dependencias mínimas y eliminar los archivos temporales
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-dev \
    tk-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -r requirements.txt --use-deprecated=legacy-resolver \
    && python -m spacy download es_core_news_sm

# Comando para ejecutar la aplicación
CMD ["python", "ia.py"]
