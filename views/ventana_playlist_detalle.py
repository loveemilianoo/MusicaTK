import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.PlaylistDAO import PlaylistDAO
from controller.CancionDAO import CancionDAO

class VentanaPlaylistDetalle:
    def __init__(self, parent, usuario_actual, app_principal, playlist_id):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.app = app_principal
        self.playlist_id = playlist_id
        self.playlist_info = None
    
    def mostrar(self):
        # Obtener información de la playlist
        self.playlist_info = PlaylistDAO.obtener_playlist_por_id(self.playlist_id)
        
        if not self.playlist_info:
            tk.Label(self.parent, text="Playlist no encontrada",
                    font=FONT_TITLE, fg=TEXT_MUT, bg=BG_DARK).pack(pady=50)
            return
        
        # Header
        header = tk.Frame(self.parent, bg=BG_DARK)
        header.pack(fill="x", pady=(0, 20))
        
        # Botón volver
        back = Componentes.btn(header, "← Volver", self._volver, bg=BG_CARD, fg=ACCENT2)
        back.pack(side="left")
        
        # Título
        tk.Label(header, text=self.playlist_info.nombre, font=FONT_TITLE,
                fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(side="left", padx=20)
        
        # Info de la playlist
        info_frame = tk.Frame(self.parent, bg=BG_CARD, padx=20, pady=15)
        info_frame.pack(fill="x", pady=(0, 20))
        
        total = 0  # Se calcularía en una consulta separada
        duracion = 0  # Se calcularía en una consulta separada
        minutos = duracion // 60 if isinstance(duracion, (int, float)) else 0
        
        tk.Label(info_frame, text=f"📊 {total} canciones", font=FONT_BODY,
                fg=TEXT_SEC, bg=BG_CARD).pack(side="left", padx=10)
        tk.Label(info_frame, text=f"⏱ {minutos} minutos", font=FONT_BODY,
                fg=TEXT_SEC, bg=BG_CARD).pack(side="left", padx=10)
        
        # Botón eliminar playlist
        btn_eliminar = Componentes.btn(info_frame, "🗑 Eliminar playlist", 
                                       self._eliminar_playlist, bg="#dc3545", fg="white")
        btn_eliminar.pack(side="right", padx=10)
        
        # Botón agregar canción
        btn_agregar = Componentes.btn(info_frame, "+ Agregar canción",
                                      self._agregar_cancion, bg=ACCENT, fg="white")
        btn_agregar.pack(side="right", padx=10)
        
        # Lista de canciones
        tk.Label(self.parent, text="Canciones", font=FONT_H2,
                fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 10))
        
        self.canciones_frame = tk.Frame(self.parent, bg=BG_DARK)
        self.canciones_frame.pack(fill="both", expand=True)
        
        self._cargar_canciones()
    
    def _cargar_canciones(self):
        # Limpiar
        for w in self.canciones_frame.winfo_children():
            w.destroy()
        
        canciones = PlaylistDAO.obtener_canciones_playlist(self.playlist_id)
        
        if not canciones:
            tk.Label(self.canciones_frame, text="Esta playlist está vacía. Agrega canciones.",
                    font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=30)
            return
        
        for cancion in canciones:
            cancion_data = {
                'id': cancion[0],
                'nombre': cancion[1],
                'duracion': cancion[2],
                'artista': cancion[3]
            }
            
            row = Componentes.cancion_row(
                self.canciones_frame,
                cancion_data,
                on_double_click=self._reproducir_cancion
            )
            
            # Botón quitar en cada fila
            btn_quitar = tk.Button(row, text="✖", font=FONT_SMALL,
                                   bg=BG_DARK, fg=TEXT_MUT, bd=0,
                                   cursor="hand2", command=lambda cid=cancion[0]: self._quitar_cancion(cid))
            btn_quitar.pack(side="right", padx=10)
    
    def _reproducir_cancion(self, cancion_data):
        self.app.reproducir_cancion(cancion_data)
    
    def _quitar_cancion(self, id_cancion):
        if messagebox.askyesno("Confirmar", "¿Quitar esta canción de la playlist?"):
            PlaylistDAO.quitar_cancion_de_playlist(self.playlist_id, id_cancion)
            self._cargar_canciones()
            
            # Actualizar información
            self.playlist_info = PlaylistDAO.obtener_playlist_por_id(self.playlist_id)
    
    def _agregar_cancion(self):
        from views.ventana_seleccionar_cancion import VentanaSeleccionarCancion
        
        def on_agregada():
            self._cargar_canciones()
            self.playlist_info = PlaylistDAO.obtener_playlist_por_id(self.playlist_id)
        
        VentanaSeleccionarCancion(self.usuario_actual, self.playlist_id, on_agregada, self.app.ventana)
    
    def _eliminar_playlist(self):
        if messagebox.askyesno("Confirmar", f"¿Eliminar la playlist '{self.playlist_info['nombre']}'?"):
            PlaylistDAO.eliminar_playlist(self.playlist_id)
            messagebox.showinfo("Éxito", "Playlist eliminada")
            self._volver()
    
    def _volver(self):
        self.app.mostrar_library()