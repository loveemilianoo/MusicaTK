import tkinter as tk
from views.colores import *
from views.componentes import Componentes
from views.ventana_home import VentanaHome
from views.ventana_search import VentanaSearch
from views.ventana_library import VentanaLibrary
from controller.PlaylistDAO import PlaylistDAO

class VentanaPrincipal:
    def __init__(self, usuario_actual):
        self.usuario_actual = usuario_actual
        self.ventana = tk.Tk()
        self.ventana.title("WavePlay")
        self.ventana.geometry("980x650")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg=BG_DARK)
        
        # Variables de estado
        self.current_screen = None
        self.now_playing = tk.StringVar(value="Selecciona una canción")
        self.progress_val = tk.DoubleVar(value=0)
        self.is_playing = tk.BooleanVar(value=False)
        self.current_cancion = None
        
        self.setup_ui()
    
    def setup_ui(self):
        outer = tk.Frame(self.ventana, bg=BG_DARK)
        outer.pack(fill="both", expand=True)
        
        # Sidebar
        self.sidebar = self._crear_sidebar(outer)
        
        # Área de contenido
        content_wrap = tk.Frame(outer, bg=BG_DARK)
        content_wrap.pack(side="left", fill="both", expand=True)
        
        self.content = tk.Frame(content_wrap, bg=BG_DARK)
        self.content.pack(fill="both", expand=True, padx=28, pady=20)
        
        # Mostrar inicio por defecto
        self.mostrar_home()
        
        # Player inferior
        self._crear_player(outer)
    
    def _crear_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=BG_SIDEBAR, width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo
        logo_f = tk.Frame(sidebar, bg=BG_SIDEBAR, pady=20, padx=18)
        logo_f.pack(fill="x")
        tk.Label(logo_f, text="◉ WavePlay", font=("Helvetica", 14, "bold"),
                fg=ACCENT2, bg=BG_SIDEBAR).pack(anchor="w")
        
        # Navegación
        nav_items = [
            ("🏠  Inicio", self.mostrar_home),
            ("🔍  Buscar", self.mostrar_search),
            ("📚  Biblioteca", self.mostrar_library),
        ]
        
        for label, cmd in nav_items:
            f = tk.Frame(sidebar, bg=BG_SIDEBAR, cursor="hand2")
            f.pack(fill="x")
            lbl = tk.Label(f, text=label, font=("Helvetica", 10, "bold"),
                          fg=TEXT_SEC, bg=BG_SIDEBAR, anchor="w", padx=20, pady=10)
            lbl.pack(fill="x")
            
            for w in (f, lbl):
                w.bind("<Button-1>", lambda e, c=cmd: c())
                w.bind("<Enter>", lambda e, f=f, l=lbl: f.configure(bg=BG_HOVER) or l.configure(bg=BG_HOVER))
                w.bind("<Leave>", lambda e, f=f, l=lbl: f.configure(bg=BG_SIDEBAR) or l.configure(bg=BG_SIDEBAR))
        
        Componentes.divider(sidebar)
        
        # Playlists del usuario
        tk.Label(sidebar, text="TUS PLAYLISTS", font=FONT_TINY,
                fg=TEXT_MUT, bg=BG_SIDEBAR, anchor="w", padx=20).pack(fill="x", pady=(8, 4))
        
        self.playlists_frame = tk.Frame(sidebar, bg=BG_SIDEBAR)
        self.playlists_frame.pack(fill="both", expand=True)
        
        self._cargar_playlists_sidebar()
        
        return sidebar
    
    def _cargar_playlists_sidebar(self):
        """Cargar playlists del usuario en el sidebar"""
        for w in self.playlists_frame.winfo_children():
            w.destroy()
        
        playlists = PlaylistDAO.obtener_playlists_por_usuario(self.usuario_actual.id_persona)
        
        for p in playlists:
            playlist_id = p[0]
            nombre = p[1]
            
            f = tk.Frame(self.playlists_frame, bg=BG_SIDEBAR, cursor="hand2")
            f.pack(fill="x")
            lbl = tk.Label(f, text=f"♪ {nombre}", font=FONT_SMALL, fg=TEXT_SEC,
                          bg=BG_SIDEBAR, anchor="w", padx=20, pady=6)
            lbl.pack(fill="x")
            
            for w in (f, lbl):
                w.bind("<Button-1>", lambda e, pid=playlist_id: self.mostrar_playlist(pid))
                w.bind("<Enter>", lambda e, f=f, l=lbl: f.configure(bg=BG_HOVER) or l.configure(bg=BG_HOVER))
                w.bind("<Leave>", lambda e, f=f, l=lbl: f.configure(bg=BG_SIDEBAR) or l.configure(bg=BG_SIDEBAR))
    
    def mostrar_home(self):
        self._limpiar_content()
        home = VentanaHome(self.content, self.usuario_actual, self)
        home.mostrar()
        self.current_screen = "home"
    
    def mostrar_search(self):
        self._limpiar_content()
        search = VentanaSearch(self.content, self.usuario_actual, self)
        search.mostrar()
        self.current_screen = "search"
    
    def mostrar_library(self):
        self._limpiar_content()
        library = VentanaLibrary(self.content, self.usuario_actual, self, self._cargar_playlists_sidebar)
        library.mostrar()
        self.current_screen = "library"
    
    def mostrar_playlist(self, playlist_id):
        self._limpiar_content()
        from views.ventana_playlist_detalle import VentanaPlaylistDetalle
        playlist_view = VentanaPlaylistDetalle(self.content, self.usuario_actual, self, playlist_id)
        playlist_view.mostrar()
    
    def _limpiar_content(self):
        for w in self.content.winfo_children():
            w.destroy()
    
    def _crear_player(self, parent):
        """Player inferior"""
        player = tk.Frame(parent, bg=BG_CARD, height=80)
        player.pack(side="bottom", fill="x")
        player.pack_propagate(False)
        
        inner = tk.Frame(player, bg=BG_CARD)
        inner.pack(fill="both", expand=True, padx=20)
        
        # Canción actual
        left = tk.Frame(inner, bg=BG_CARD)
        left.pack(side="left", fill="y")
        
        cv = tk.Canvas(left, width=48, height=48, bg=ACCENT,
                      highlightthickness=0, cursor="hand2")
        cv.pack(side="left", pady=16, padx=(0, 12))
        cv.create_text(24, 24, text="♫", font=("Helvetica", 18), fill=ACCENT2)
        
        song_info = tk.Frame(left, bg=BG_CARD)
        song_info.pack(side="left", pady=22)
        tk.Label(song_info, textvariable=self.now_playing,
                font=("Helvetica", 10, "bold"), fg=TEXT_PRI, bg=BG_CARD).pack(anchor="w")
        
        # Controles centrales
        center = tk.Frame(inner, bg=BG_CARD)
        center.pack(side="left", expand=True, fill="both")
        
        ctrl_row = tk.Frame(center, bg=BG_CARD)
        ctrl_row.pack(pady=10)
        
        # Botón play/pausa
        self.play_btn = tk.Canvas(ctrl_row, width=32, height=32, bg=BG_CARD,
                                  highlightthickness=0, cursor="hand2")
        self.play_btn.pack(side="left", padx=4)
        self._actualizar_boton_play()
        self.play_btn.bind("<Button-1>", lambda e: self.toggle_play())
        
        # Barra de progreso
        prog_f = tk.Frame(center, bg=BG_CARD)
        prog_f.pack(fill="x", padx=30)
        tk.Label(prog_f, text="0:00", font=FONT_TINY, fg=TEXT_MUT, bg=BG_CARD).pack(side="left")
        
        self.progress_bar = tk.Scale(prog_f, from_=0, to=100, orient="horizontal",
                                     variable=self.progress_val, bg=BG_CARD, fg=TEXT_SEC,
                                     troughcolor=BG_DARK, activebackground=ACCENT2,
                                     highlightthickness=0, length=340, showvalue=False)
        self.progress_bar.pack(side="left", padx=8)
        
        self.time_label = tk.Label(prog_f, text="0:00", font=FONT_TINY, fg=TEXT_MUT, bg=BG_CARD)
        self.time_label.pack(side="left")
        
        # Volumen
        right = tk.Frame(inner, bg=BG_CARD)
        right.pack(side="right", pady=22)
        tk.Label(right, text="🔊", fg=TEXT_SEC, bg=BG_CARD, font=FONT_BODY).pack(side="left")
        tk.Scale(right, from_=0, to=100, orient="horizontal",
                bg=BG_CARD, fg=TEXT_SEC, troughcolor=BG_DARK,
                activebackground=ACCENT2, highlightthickness=0,
                length=90, showvalue=False).pack(side="left")
    
    def _actualizar_boton_play(self):
        self.play_btn.delete("all")
        icon = "⏸" if self.is_playing.get() else "▶"
        self.play_btn.create_text(16, 16, text=icon, font=("Helvetica", 13), fill=GREEN)
    
    def toggle_play(self):
        self.is_playing.set(not self.is_playing.get())
        self._actualizar_boton_play()
    
    def reproducir_cancion(self, cancion_data):
        """Reproducir una canción"""
        nombre = cancion_data.get('nombre', '')
        artista = cancion_data.get('artista', '')
        duracion = cancion_data.get('duracion', 0)
        
        self.now_playing.set(f"{nombre} — {artista}")
        self.current_cancion = cancion_data
        
        if isinstance(duracion, (int, float)) and duracion > 0:
            minutos = int(duracion // 60)
            segundos = int(duracion % 60)
            self.time_label.config(text=f"{minutos}:{segundos:02d}")
        
        self.is_playing.set(True)
        self._actualizar_boton_play()
    
    def ejecutar(self):
        self.ventana.mainloop()