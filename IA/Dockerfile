# Usa una imagen base de Python
FROM python:3.10-slim

# Instala dependencias del sistema para Tkinter, SQLite y xvfb
RUN apt-get update && apt-get install -y \
    python3-tk sqlite3

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de código a /app
COPY .. /app

# Instala las dependencias de Python necesarias
RUN pip install requests

# Ejecuta el script principal usando xvfb
CMD ["python", "IA.py"]
