# Manual de Ejecución de la TerSIA

## Descripción de la App

La aplicación **TerSIA** automatiza y centraliza la búsqueda de información académica para estudiantes, ofreciendo una experiencia intuitiva, rápida y eficiente que optimiza el acceso a recursos educativos y fomenta un aprendizaje dinámico e interactivo.

Está implementada con **python-tkinter** conectado al modelo **GPT** con la **API** de OpenAI. Requiere una clave API propia y una conexión a Internet.

## Herramientas de Desarrollo

  - **Lenguaje:** Python
  - **Interfaz gráfica:** tkinter
  - **Modelo IA:** GPT
  - **Base de datos:** SQLite
  - **Contenedor:** Docker

### Librerías Python Utilizadas

| Librería        | Descripción                                                                                                                               |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `tkinter`       | Crear interfaces gráficas de usuario (GUI).                                                                                             |
| `ttk`           | Submódulo de tkinter con componentes gráficos mejorados.                                                                                   |
| `scrolledtext` | Crear cuadros de texto con barras de desplazamiento.                                                                                     |
| `messagebox`   | Mostrar cuadros de mensajes, como alertas o notificaciones.                                                                               |
| `sqlite3`       | Interactuar con bases de datos SQLite.                                                                                                   |
| `spacy`         | Procesamiento de lenguaje natural (NLP), optimizando la interacción con GPT.                                                            |
| `os`            | Realizar operaciones con archivos y directorios del sistema operativo.                                                                   |
| `openai`        | Interactuar con la API de OpenAI para integrar la inteligencia artificial.                                                                |

## Ejecución

1.  **Clonar el repositorio:**  

    ```bash
    git clone https://github.com/SER050902/IA.git
    ```

2.  **Construir la imagen de Docker:**  

    ```bash
    sudo docker build -t tersia .
    ```

3.  **Permitir acceso servidor x11 a la pantalla (solo Linux):**  

    ```bash
    xhost +local:docker
    ```

    Si estás en **Windows**, consulta la sección de [**Instale el servidor X11**](#instale-el-servidor-x11) y:
     ```bash
    $env:DISPLAY="host.docker.internal:0"
    ```

5.  **Ejecutar el contenedor:**  

    ```bash
    sudo docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix tersia
    ```

## Configuración de la API Key

Asegúrate de tener tu propia clave API de OpenAI. Configura la variable de entorno del api (llamado `OPENAI_API_KEY`) en el archivo Dockerfile con tu clave.

## Ejemplos de Consultas

**Sobre alumnos:**

  - "Dime sobre el alumno Sergio"
  - "Dime qué módulo cursa Sergio"

**Sobre profesores:**

  - "¿Es Jose Pedro un profesor?"
  - "Dime sobre el profesor Gines"
  - "¿El profesor Gines imparte el módulo Base de datos?"

**Sobre horarios:**

  - "Dime el horario de los módulos"
  - "¿Qué horario hay en el módulo de Hardware?"

## Instale el servidor X11
Windows no es compatible con X11 de forma nativa, por lo que se requiere un servidor X11 para manejar la representación de la GUI.  
Para poder permitir el acceso a la pantalla Docker, descarga el software [**VcXsrv**](./Instalación%20VcXsrv.md).

## Consideraciones

  - **Especificar roles:** Si la consulta no produce resultados, intenta agregar el rol de la persona (alumno o profesor).
      - Ejemplo: En lugar de "Dime sobre Jose Pedro", usa "Dime sobre el profesor Jose Pedro".
  - **Una clave por consulta:** La IA solo puede procesar una clave a la vez.
      - Ejemplo: En "Dime sobre el profesor Gines y profesor Alejandro", solo se buscará información sobre Alejandro.
