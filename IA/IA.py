import tkinter as tk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ventana Pequeña")

# Configurar el tamaño de la ventana (ancho x alto)
ventana.geometry("200x100")

# Función para cerrar la ventana
def cerrar():
    ventana.destroy()

# Etiqueta de ejemplo
etiqueta = tk.Label(ventana, text="¡Hola!")
etiqueta.pack(pady=10)

# Botón para cerrar la ventana
boton_cerrar = tk.Button(ventana, text="Cerrar", command=cerrar)
boton_cerrar.pack(pady=5)

# Iniciar el bucle de la ventan
# a
ventana.mainloop()
