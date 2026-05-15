import tkinter as tk
from views.colores import *
from views.componentes import Componentes
from controller.CancionDAO import CancionDAO

class VentanaSearch:
    def __init__(self, parent, usuario_actual, app_principal):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.app = app_principal
        self.resultados_frame = None
    
    def mostrar(self):
        tk.Label(self.parent, text="Buscar", font=FONT_TITLE,
                fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x")
        
        # Barra de búsqueda
        search_wrap = tk.Frame(self.parent, bg=BG_CARD, padx=14, pady=10)
        search_wrap.pack(fill="x", pady=10)
        
        tk.Label(search_wrap, text="🔍", fg=TEXT_SEC, bg=BG_CARD,
                font=FONT_BODY).pack(side="left")
        
        self.search_entry = tk.Entry(search_wrap, font=FONT_BODY, bg=BG_CARD, fg=TEXT_PRI,
                                     insertbackground=ACCENT2, relief="flat", bd=0, width=50)
        self.search_entry.pack(side="left", padx=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self._buscar())
        
        # Géneros populares
        tk.Label(self.parent, text="Géneros populares", font=FONT_H2,
                fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x", pady=(12, 8))
        
        self._cargar_generos()
        
        # Resultados
        tk.Label(self.parent, text="Resultados", font=FONT_H2,
                fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x", pady=(16, 8))
        
        self.resultados_frame = tk.Frame(self.parent, bg=BG_DARK)
        self.resultados_frame.pack(fill="both", expand=True)
    
    def _cargar_generos(self):
        generos = [
            ("Synthwave", "#4A1080"), ("Lo-Fi", "#0A4A80"),
            ("Electrónica", "#804A00"), ("Ambient", "#004A40"),
            ("Hip-Hop", "#6A0A0A"), ("Jazz", "#2A4A00")
        ]
        
        row1 = tk.Frame(self.parent, bg=BG_DARK)
        row1.pack(fill="x")
        row2 = tk.Frame(self.parent, bg=BG_DARK)
        row2.pack(fill="x", pady=8)
        
        for i, (genero, color) in enumerate(generos):
            row = row1 if i < 3 else row2
            gc = tk.Frame(row, bg=color, cursor="hand2")
            gc.pack(side="left", padx=(0, 10), ipadx=20, ipady=20)
            tk.Label(gc, text=genero, font=("Helvetica", 11, "bold"),
                    fg=TEXT_PRI, bg=color, padx=24, pady=18).pack()
            gc.bind("<Button-1>", lambda e, g=genero: self._buscar_por_genero(g))
    
    def _buscar_por_genero(self, genero):
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, genero)
        self._buscar()
    
    def _buscar(self):
        texto = self.search_entry.get()
        
        for w in self.resultados_frame.winfo_children():
            w.destroy()
        
        if not texto or texto == "Buscar":
            return
        
        canciones = CancionDAO.buscar_cancion_por_nombre(texto)
        
        if not canciones:
            tk.Label(self.resultados_frame, text="No se encontraron resultados",
                    font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=20)
            return
        
        for cancion in canciones:
            cancion_data = {
                'id': cancion[0],
                'nombre': cancion[1],
                'artista': cancion[2],
                'album': cancion[3],
                'duracion': cancion[4]
            }
            
            Componentes.cancion_row(
                self.resultados_frame,
                cancion_data,
                on_double_click=self._reproducir_cancion
            )
    
    def _reproducir_cancion(self, cancion_data):
        self.app.reproducir_cancion(cancion_data)