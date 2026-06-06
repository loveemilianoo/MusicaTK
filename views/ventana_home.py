import tkinter as tk
from views.colores import *
from views.componentes import Componentes
from controller.CancionDAO import CancionDAO

class VentanaHome:
    def __init__(self, parent, usuario_actual, app_principal):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.app = app_principal
    
    def mostrar(self):
        # Saludo
        hora = self._obtener_saludo()
        tk.Label(self.parent, text=f"{hora} 🌙", font=FONT_TITLE,
                fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x")
        tk.Label(self.parent, text="Continúa escuchando", font=FONT_H3,
                fg=TEXT_SEC, bg=BG_DARK, anchor="w").pack(fill="x", pady=(4, 12))
        
        # Canciones recientes
        self._cargar_canciones_recientes()
    
    def _obtener_saludo(self):
        from datetime import datetime
        hora = datetime.now().hour
        if hora < 12:
            return "Buenos días"
        elif hora < 18:
            return "Buenas tardes"
        else:
            return "Buenas noches"
    
    def _cargar_canciones_recientes(self):
        canciones = CancionDAO.obtener_todas_canciones()

        if not canciones:
            tk.Label(self.parent, text="No hay canciones disponibles",
                    font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=20)
            return

        # Contenedor con scroll
        container = tk.Frame(self.parent, bg=BG_DARK)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_DARK)

        scroll_frame.bind(
            "<Configure>",
            lambda _: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        def _on_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Enter>", lambda _: canvas.bind_all("<MouseWheel>", _on_wheel))
        canvas.bind("<Leave>", lambda _: canvas.unbind_all("<MouseWheel>"))

        for cancion in canciones:
            cancion_data = {
                'id': cancion.id_cancion,
                'nombre': cancion.nombre,
                'artista': cancion.id_artista,
                'album': cancion.id_album,
                'duracion': cancion.duracion,
                'ruta_archivo': cancion.ruta_de_archivo
            }

            Componentes.cancion_row(
                scroll_frame,
                cancion_data,
                on_double_click=self._reproducir_cancion
            )
    
    def _reproducir_cancion(self, cancion_data):
        self.app.reproducir_cancion(cancion_data)