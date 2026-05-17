
import tkinter as tk
from views.colores import *

# Ventana de prueba simple
ventana = tk.Tk()
ventana.title("Prueba GUI")
ventana.geometry("400x300")
ventana.configure(bg=BG_DARK)

# Etiqueta para ver que funciona
tk.Label(ventana, text="¡Esto es una prueba!", font=("Helvetica", 16), fg=TEXT_PRI, bg=BG_DARK).pack(pady=50)
tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack()

ventana.mainloop()
