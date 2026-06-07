import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.PlaylistDAO import PlaylistDAO
from controller.AlbumDAO import AlbumDAO
from controller.ArtistaDAO import ArtistaDAO

class VentanaLibrary:
    def __init__(self, parent, usuario_actual, app_principal, recargar_sidebar_callback):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.app = app_principal
        self.recargar_sidebar = recargar_sidebar_callback
        self.current_tab = "playlists"
        # Cola de reproducción del álbum en curso
        self._album_cola = []
        self._album_index = -1
    
    def mostrar(self):
        header = tk.Frame(self.parent, bg=BG_DARK)
        header.pack(fill="x")
        
        tk.Label(header, text="Tu biblioteca", font=FONT_TITLE,
                fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(side="left")
        
        # Botón nueva playlist
        btn_nueva = Componentes.btn(header, "+ Nueva playlist", self._crear_playlist,
                                    bg=ACCENT, fg="white", pad=(14, 6))
        btn_nueva.pack(side="right", pady=10)
        
        # Tabs
        tabs = tk.Frame(self.parent, bg=BG_DARK)
        tabs.pack(fill="x", pady=8)
        
        for tab in ["Playlists", "Álbumes", "Artistas"]:
            tb = tk.Frame(tabs, bg=BG_CARD, cursor="hand2")
            tb.pack(side="left", padx=(0, 6), ipadx=10, ipady=4)
            label = tk.Label(tb, text=tab, font=FONT_SMALL, fg=TEXT_SEC,
                           bg=BG_CARD, padx=8, pady=4)
            label.pack()
            
            tb.bind("<Button-1>", lambda e, t=tab.lower(): self._cambiar_tab(t))
            label.bind("<Button-1>", lambda e, t=tab.lower(): self._cambiar_tab(t))
        
        Componentes.divider(self.parent)
        
        # Contenedor de contenido
        self.content_frame = tk.Frame(self.parent, bg=BG_DARK)
        self.content_frame.pack(fill="both", expand=True)
        
        self._cambiar_tab("playlists")
    
    def _cambiar_tab(self, tab):
        self.current_tab = tab
        
        for w in self.content_frame.winfo_children():
            w.destroy()
        
        if tab == "playlists":
            self._mostrar_playlists()
        elif tab == "álbumes" or tab == "albumes":
            self._mostrar_albumes()
        elif tab == "artistas":
            self._mostrar_artistas()
    
    def _mostrar_playlists(self):
        # Mostrar TODAS las playlists que existan
        playlists = PlaylistDAO.obtener_playlists_con_detalle()
        
        if not playlists:
            tk.Label(self.content_frame, text="No hay playlists disponibles. ¡Crea una!",
                    font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=20)
            return
        
        for p in playlists:
            # p es una tupla: (id, nombre, fecha_creacion, usuario, total_canciones)
            row = tk.Frame(self.content_frame, bg=BG_DARK, cursor="hand2")
            row.pack(fill="x", pady=8)
            row.bind("<Button-1>", lambda e, pid=p[0]: self.app.mostrar_playlist(pid))
            
            # Canvas con icono
            canvas = tk.Canvas(row, width=50, height=50, bg="#1A1A2E", highlightthickness=0)
            canvas.pack(side="left", padx=(0, 12), pady=4)
            canvas.create_rectangle(5, 5, 45, 45, fill=ACCENT, outline="")
            canvas.create_text(25, 25, text="♫", font=("Helvetica", 20), fill="white")
            canvas.bind("<Button-1>", lambda e, pid=p[0]: self.app.mostrar_playlist(pid))
            
            # Información
            info = tk.Frame(row, bg=BG_DARK)
            info.pack(side="left", fill="both", expand=True)
            info.bind("<Button-1>", lambda e, pid=p[0]: self.app.mostrar_playlist(pid))
            
            nombre_label = tk.Label(info, text=p[1], font=FONT_H3, fg=TEXT_PRI, bg=BG_DARK)
            nombre_label.pack(anchor="w")
            nombre_label.bind("<Button-1>", lambda e, pid=p[0]: self.app.mostrar_playlist(pid))
            
            detalles = f"{p[3]} • {p[4]} canciones"
            detalles_label = tk.Label(info, text=detalles, font=FONT_SMALL, fg=TEXT_SEC, bg=BG_DARK)
            detalles_label.pack(anchor="w")
            detalles_label.bind("<Button-1>", lambda e, pid=p[0]: self.app.mostrar_playlist(pid))
    
    def _mostrar_albumes(self):
        albumes = AlbumDAO.listar_todos_albumes()
        
        if not albumes:
            tk.Label(self.content_frame, text="No hay álbumes disponibles",
                    font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=20)
            return
        
        for album in albumes:
            row = tk.Frame(self.content_frame, bg=BG_DARK, cursor="hand2")
            row.pack(fill="x", pady=3)

            canvas = tk.Canvas(row, width=44, height=44, bg="#1A1A2E", highlightthickness=0)
            canvas.pack(side="left", padx=(0, 10))
            canvas.create_text(22, 22, text="▶", font=("Helvetica", 14), fill=ACCENT)

            info = tk.Frame(row, bg=BG_DARK)
            info.pack(side="left")
            nombre_lbl = tk.Label(info, text=album.nombre, font=FONT_H3, fg=TEXT_PRI, bg=BG_DARK)
            nombre_lbl.pack(anchor="w")
            detalle_lbl = tk.Label(info, text=f"{album.fecha_lanzamiento}  •  {album.num_canciones} canciones",
                    font=FONT_SMALL, fg=TEXT_SEC, bg=BG_DARK)
            detalle_lbl.pack(anchor="w")

            # Click en cualquier parte de la fila → reproducir el álbum en orden
            for w in (row, canvas, info, nombre_lbl, detalle_lbl):
                w.bind("<Button-1>", lambda e, aid=album.id_album: self._reproducir_album(aid))
    
    def _reproducir_album(self, id_album):
        """Reproduce todas las canciones del álbum en orden de track."""
        canciones = AlbumDAO.obtener_canciones_del_album(id_album)
        # Solo las que tienen archivo de audio, conservando el orden
        self._album_cola = [c for c in canciones if c.get('ruta_de_archivo')]

        if not self._album_cola:
            messagebox.showinfo("Álbum",
                                "Este álbum no tiene canciones reproducibles.",
                                parent=self.app.ventana)
            return

        self._reproducir_album_indice(0)

    def _reproducir_album_indice(self, index):
        if 0 <= index < len(self._album_cola):
            self._album_index = index
            self.app.reproducir_cancion(self._album_cola[index])
            self.app.set_siguiente_callback(self._album_siguiente)

    def _album_siguiente(self):
        siguiente = self._album_index + 1
        if siguiente < len(self._album_cola):
            self._reproducir_album_indice(siguiente)

    def _mostrar_artistas(self):
        artistas = ArtistaDAO.listar_todos_artistas()
        
        if not artistas:
            tk.Label(self.content_frame, text="No hay artistas disponibles",
                    font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=20)
            return
        
        for artista in artistas:
            row = tk.Frame(self.content_frame, bg=BG_DARK, cursor="hand2")
            row.pack(fill="x", pady=3)
            
            canvas = tk.Canvas(row, width=44, height=44, bg=ACCENT, highlightthickness=0)
            canvas.pack(side="left", padx=(0, 10))
            canvas.create_text(22, 22, text="🎤", font=("Helvetica", 14), fill=ACCENT2)
            
            info = tk.Frame(row, bg=BG_DARK)
            info.pack(side="left")
            nombre_completo = artista.nombre_completo
            tk.Label(info, text=nombre_completo, font=FONT_H3, fg=TEXT_PRI, bg=BG_DARK).pack(anchor="w")
            tipo = "Banda" if artista.banda == 1 else "Solista"
            tk.Label(info, text=f"{tipo} • {artista.disquera or 'Sin disquera'}",
                    font=FONT_SMALL, fg=TEXT_SEC, bg=BG_DARK).pack(anchor="w")
    
    def _crear_playlist(self):
        from views.ventana_crear_playlist import VentanaCrearPlaylist
        
        def on_creada():
            self._mostrar_playlists()
            self.recargar_sidebar()
        
        VentanaCrearPlaylist(self.usuario_actual, on_creada, self.app.ventana)