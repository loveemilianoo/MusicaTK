import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.CancionDAO import CancionDAO
from controller.PlaylistDAO import PlaylistDAO

class VentanaSeleccionarCancion:
    def __init__(self, usuario_actual, playlist_id, on_agregada_callback, parent_ventana):
        self.usuario_actual = usuario_actual
        self.playlist_id = playlist_id
        self.on_agregada = on_agregada_callback
        self.ventana = tk.Toplevel(parent_ventana)
        self.ventana.title("Agregar canción")
        self.ventana.geometry("500x500")
        self.ventana.configure(bg=BG_DARK)
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self.ventana, text="Seleccionar canción", font=FONT_TITLE,
                fg=TEXT_PRI, bg=BG_DARK).pack(pady=20)
        
        # Búsqueda
        search_wrap = tk.Frame(self.ventana, bg=BG_CARD, padx=14, pady=10)
        search_wrap.pack(fill="x", pady=10, padx=20)
        
        tk.Label(search_wrap, text="🔍", fg=TEXT_SEC, bg=BG_CARD,
                font=FONT_BODY).pack(side="left")
        
        self.search_entry = tk.Entry(search_wrap, font=FONT_BODY, bg=BG_CARD, fg=TEXT_PRI,
                                     insertbackground=ACCENT2, relief="flat", bd=0, width=40)
        self.search_entry.pack(side="left", padx=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self._buscar())
        
        # Lista de canciones
        self.canciones_frame = tk.Frame(self.ventana, bg=BG_DARK)
        self.canciones_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self._cargar_canciones()
    
    def _cargar_canciones(self, texto=""):
        for w in self.canciones_frame.winfo_children():
            w.destroy()
        
        if texto:
            canciones = CancionDAO.buscar_cancion_por_nombre(texto)
        else:
            canciones = CancionDAO.listar_todas_canciones()
        
        if not canciones:
            tk.Label(self.canciones_frame, text="No hay canciones disponibles",
                    font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=20)
            return
        
        for cancion in canciones[:20]:
            cancion_data = {
                'id': cancion[0],
                'nombre': cancion[1],
                'artista': cancion[2],
                'duracion': cancion[4]
            }
            
            row = Componentes.cancion_row(
                self.canciones_frame,
                cancion_data,
                on_click=lambda cd: self._agregar_cancion(cd)
            )
    
    def _buscar(self):
        texto = self.search_entry.get()
        self._cargar_canciones(texto)
    
    def _agregar_cancion(self, cancion_data):
        resultado = PlaylistDAO.agregar_cancion_a_playlist(
            cancion_data['id'], self.playlist_id
        )
        
        if resultado:
            messagebox.showinfo("Éxito", f"'{cancion_data['nombre']}' agregada a la playlist")
            self.on_agregada()
            self.ventana.destroy()
        else:
            messagebox.showwarning("Advertencia", "La canción ya está en esta playlist")