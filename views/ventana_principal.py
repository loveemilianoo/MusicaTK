import tkinter as tk
from models.Artista import Artista
from views.colores import *
from views.componentes import Componentes
from views.ventana_home import VentanaHome
from views.ventana_search import VentanaSearch
from views.ventana_library import VentanaLibrary
from views.ventana_portal_artista import VentanaPortalArtista
from controller.PlaylistDAO import PlaylistDAO
from controller.MusicPlayer import MusicPlayer  # ── NUEVO

class VentanaPrincipal:
    def __init__(self, usuario_actual):
        self.usuario_actual = usuario_actual
        self.ventana = tk.Tk()
        self.ventana.title("WavePlay")
        self.ventana.geometry("980x650")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg=BG_DARK)

        # Estado de reproducción
        self.current_screen  = None
        self.now_playing     = tk.StringVar(value="Selecciona una canción")
        self.progress_val    = tk.DoubleVar(value=0)
        self.is_playing      = tk.BooleanVar(value=False)
        self.current_cancion = None
        self.timer_id        = None  

        self.player = MusicPlayer()  

        self.setup_ui()

    def setup_ui(self):
        outer = tk.Frame(self.ventana, bg=BG_DARK)
        outer.pack(fill="both", expand=True)

        self.sidebar = self._crear_sidebar(outer)

        content_wrap = tk.Frame(outer, bg=BG_DARK)
        content_wrap.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(content_wrap, bg=BG_DARK)
        self.content.pack(fill="both", expand=True, padx=28, pady=20)

        self.mostrar_home()
        self._crear_player(outer)

    def _crear_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=BG_SIDEBAR, width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_f = tk.Frame(sidebar, bg=BG_SIDEBAR, pady=20, padx=18)
        logo_f.pack(fill="x")
        tk.Label(logo_f, text="◉ WavePlay", font=("Helvetica", 14, "bold"),
                fg=ACCENT2, bg=BG_SIDEBAR).pack(anchor="w")

        # Navegación base
        nav_items = [
            ("🏠  Inicio",     self.mostrar_home),
            ("🔍  Buscar",     self.mostrar_search),
            ("📚  Biblioteca", self.mostrar_library),
        ]

        # Mi Portal solo para artistas  ── CAMBIA
        if isinstance(self.usuario_actual, Artista):
            nav_items.append(("🎤  Mi Portal", self.mostrar_portal_artista))

        for label, cmd in nav_items:
            f = tk.Frame(sidebar, bg=BG_SIDEBAR, cursor="hand2")
            f.pack(fill="x")
            lbl = tk.Label(f, text=label, font=("Helvetica", 10, "bold"),
                          fg=TEXT_SEC, bg=BG_SIDEBAR, anchor="w", padx=20, pady=10)
            lbl.pack(fill="x")
            for w in (f, lbl):
                w.bind("<Button-1>", lambda e, c=cmd: c())
                w.bind("<Enter>",  lambda e, f=f, l=lbl: f.configure(bg=BG_HOVER)   or l.configure(bg=BG_HOVER))
                w.bind("<Leave>",  lambda e, f=f, l=lbl: f.configure(bg=BG_SIDEBAR) or l.configure(bg=BG_SIDEBAR))

        Componentes.divider(sidebar)

        tk.Label(sidebar, text="TUS PLAYLISTS", font=FONT_TINY,
                fg=TEXT_MUT, bg=BG_SIDEBAR, anchor="w", padx=20).pack(fill="x", pady=(8, 4))

        self.playlists_frame = tk.Frame(sidebar, bg=BG_SIDEBAR)
        self.playlists_frame.pack(fill="both", expand=True)

        try:
            self._cargar_playlists_sidebar()
        except Exception as e:
            print(f"Error al inicializar playlists: {e}")

        return sidebar

    def _cargar_playlists_sidebar(self):
        for w in self.playlists_frame.winfo_children():
            w.destroy()
        try:
            playlists = PlaylistDAO.obtener_playlists_por_usuario(
                self.usuario_actual.id_persona)
            for p in playlists:
                f = tk.Frame(self.playlists_frame, bg=BG_SIDEBAR, cursor="hand2")
                f.pack(fill="x")
                lbl = tk.Label(f, text=f"♪ {p.nombre}", font=FONT_SMALL,
                              fg=TEXT_SEC, bg=BG_SIDEBAR, anchor="w", padx=20, pady=6)
                lbl.pack(fill="x")
                for w in (f, lbl):
                    w.bind("<Button-1>", lambda e, pid=p.id_playlist: self.mostrar_playlist(pid))
                    w.bind("<Enter>",  lambda e, f=f, l=lbl: f.configure(bg=BG_HOVER)   or l.configure(bg=BG_HOVER))
                    w.bind("<Leave>",  lambda e, f=f, l=lbl: f.configure(bg=BG_SIDEBAR) or l.configure(bg=BG_SIDEBAR))
        except Exception as e:
            print(f"Error al cargar playlists: {e}")

    # ── Navegación ─────────────────────────────────────────
    def mostrar_home(self):
        self._limpiar_content()
        VentanaHome(self.content, self.usuario_actual, self).mostrar()
        self.current_screen = "home"

    def mostrar_search(self):
        self._limpiar_content()
        VentanaSearch(self.content, self.usuario_actual, self).mostrar()
        self.current_screen = "search"

    def mostrar_library(self):
        self._limpiar_content()
        VentanaLibrary(self.content, self.usuario_actual, self,
                       self._cargar_playlists_sidebar).mostrar()
        self.current_screen = "library"

    def mostrar_portal_artista(self):
        self._limpiar_content()
        VentanaPortalArtista(self.usuario_actual, self).mostrar(self.content)
        self.current_screen = "portal"

    def mostrar_playlist(self, playlist_id):
        self._limpiar_content()
        from views.ventana_playlist_detalle import VentanaPlaylistDetalle
        VentanaPlaylistDetalle(self.content, self.usuario_actual,
                               self, playlist_id).mostrar()

    def _limpiar_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ── Player ─────────────────────────────────────────────
    def _crear_player(self, parent):
        player_frame = tk.Frame(parent, bg=BG_CARD, height=90)
        player_frame.pack(side="bottom", fill="x")
        player_frame.pack_propagate(False)

        inner = tk.Frame(player_frame, bg=BG_CARD)
        inner.pack(fill="both", expand=True, padx=20, pady=8)

        # ── Info canción (izquierda) ───────────────────────────
        left = tk.Frame(inner, bg=BG_CARD)
        left.pack(side="left", fill="y", padx=(0, 20))

        cv = tk.Canvas(left, width=48, height=48, bg=ACCENT, highlightthickness=0)
        cv.pack(side="left", pady=4, padx=(0, 10))
        cv.create_text(24, 24, text="♫", font=("Helvetica", 18), fill=ACCENT2)

        song_info = tk.Frame(left, bg=BG_CARD)
        song_info.pack(side="left", fill="y")
        tk.Label(song_info, textvariable=self.now_playing,
                 font=("Helvetica", 10, "bold"), fg=TEXT_PRI, bg=BG_CARD,
                 anchor="w").pack(anchor="w", pady=(8, 2))
        tk.Label(song_info, text="WavePlay", font=FONT_TINY,
                 fg=TEXT_MUT, bg=BG_CARD, anchor="w").pack(anchor="w")

        # ── Controles centrales ────────────────────────────────
        center = tk.Frame(inner, bg=BG_CARD)
        center.pack(side="left", expand=True, fill="both")

        # Botones de control
        ctrl_row = tk.Frame(center, bg=BG_CARD)
        ctrl_row.pack(pady=(4, 2))

        # Botón anterior
        btn_prev = tk.Label(ctrl_row, text="⏮", font=("Helvetica", 14),
                            fg=TEXT_SEC, bg=BG_CARD, cursor="hand2")
        btn_prev.pack(side="left", padx=8)
        btn_prev.bind("<Button-1>", lambda e: self._cancion_anterior())

        # Botón play/pausa
        self.play_btn = tk.Canvas(ctrl_row, width=36, height=36,
                                   bg=ACCENT, highlightthickness=0, cursor="hand2")
        self.play_btn.pack(side="left", padx=8)
        self._actualizar_boton_play()
        self.play_btn.bind("<Button-1>", lambda e: self.toggle_play())

        # Botón siguiente
        btn_next = tk.Label(ctrl_row, text="⏭", font=("Helvetica", 14),
                            fg=TEXT_SEC, bg=BG_CARD, cursor="hand2")
        btn_next.pack(side="left", padx=8)
        btn_next.bind("<Button-1>", lambda e: self._cancion_siguiente())

        # Barra de progreso con tiempos
        prog_row = tk.Frame(center, bg=BG_CARD)
        prog_row.pack(fill="x", padx=20)

        self.lbl_tiempo_actual = tk.Label(prog_row, text="0:00", font=FONT_TINY,
                                           fg=TEXT_MUT, bg=BG_CARD, width=4)
        self.lbl_tiempo_actual.pack(side="left")

        self.progress_bar = tk.Scale(
            prog_row, from_=0, to=100, orient="horizontal",
            variable=self.progress_val,
            bg=BG_CARD, fg=TEXT_SEC, troughcolor=BG_HOVER,
            activebackground=ACCENT, highlightthickness=0,
            length=300, showvalue=False,
            command=self._al_mover_barra
        )
        self.progress_bar.pack(side="left", padx=6)

        self.time_label = tk.Label(prog_row, text="0:00", font=FONT_TINY,
                                    fg=TEXT_MUT, bg=BG_CARD, width=4)
        self.time_label.pack(side="left")

        # ── Volumen (derecha) ──────────────────────────────────
        right = tk.Frame(inner, bg=BG_CARD)
        right.pack(side="right", fill="y", pady=4)

        tk.Label(right, text="🔊", fg=TEXT_SEC, bg=BG_CARD,
                 font=FONT_BODY).pack(side="left", padx=(0, 4))

        self.vol_var = tk.IntVar(value=80)
        tk.Scale(
            right, from_=0, to=100, orient="horizontal",
            variable=self.vol_var,
            bg=BG_CARD, fg=TEXT_SEC, troughcolor=BG_HOVER,
            activebackground=ACCENT, highlightthickness=0,
            length=90, showvalue=False,
            command=lambda v: self.player.set_volumen(int(float(v)))
        ).pack(side="left")

    def _actualizar_boton_play(self):
        self.play_btn.delete("all")
        # Fondo circular
        self.play_btn.create_oval(2, 2, 34, 34, fill=ACCENT, outline="")
        icon = "⏸" if self.is_playing.get() else "▶"
        self.play_btn.create_text(18, 18, text=icon,
                                   font=("Helvetica", 13), fill="white")
    
    def toggle_play(self):
        if self.player.esta_reproduciendo():
            self.player.pausar()
            self.is_playing.set(False)
        elif self.player.pausado:
            self.player.reanudar()
            self.is_playing.set(True)
        self._actualizar_boton_play()
    
    def _al_mover_barra(self, valor):
        """Cuando el usuario arrastra la barra manualmente."""
        # pygame no soporta seek nativo en MP3, se ignora por ahora
        pass
    
    def _iniciar_loop_progreso(self):
        if self.timer_id:
            self.ventana.after_cancel(self.timer_id)
    
        def tick():
            if self.player.esta_reproduciendo():
                pos = self.player.get_posicion_segundos()
                self.progress_val.set(pos)
                # Actualizar label de tiempo actual
                m = int(pos // 60)
                s = int(pos % 60)
                self.lbl_tiempo_actual.config(text=f"{m}:{s:02d}")
                self.timer_id = self.ventana.after(500, tick)
            else:
                self.is_playing.set(False)
                self._actualizar_boton_play()
                self.progress_val.set(0)
                self.lbl_tiempo_actual.config(text="0:00")
    
        self.timer_id = self.ventana.after(500, tick)
    
    def _cancion_anterior(self):
        """Placeholder — se puede conectar a una cola después."""
        self.player.detener()
        self.is_playing.set(False)
        self._actualizar_boton_play()
        self.progress_val.set(0)
        self.lbl_tiempo_actual.config(text="0:00")
    
    def _cancion_siguiente(self):
        """Placeholder — se puede conectar a una cola después."""
        self.player.detener()
        self.is_playing.set(False)
        self._actualizar_boton_play()
        self.progress_val.set(0)
        self.lbl_tiempo_actual.config(text="0:00")

    def reproducir_cancion(self, cancion_data):  # ── CAMBIA
        nombre   = cancion_data.get('nombre', '')
        artista  = cancion_data.get('artista', '')
        duracion = cancion_data.get('duracion', 0)
        ruta     = cancion_data.get('ruta_archivo')

        self.now_playing.set(f"{nombre} — {artista}")
        self.current_cancion = cancion_data

        if isinstance(duracion, (int, float)) and duracion > 0:
            self.progress_bar.config(to=duracion)
            minutos  = int(duracion // 60)
            segundos = int(duracion % 60)
            self.time_label.config(text=f"{minutos}:{segundos:02d}")

        if ruta:
            ok = self.player.reproducir(ruta)
            if ok:
                self.is_playing.set(True)
                self._actualizar_boton_play()
                self._iniciar_loop_progreso()
            else:
                from tkinter import messagebox
                messagebox.showwarning("Aviso",
                    "No se encontró el archivo de audio.\n"
                    "Verifica que el archivo existe en la carpeta /audio.",
                    parent=self.ventana)
        else:
            from tkinter import messagebox
            messagebox.showwarning("Aviso",
                "Esta canción no tiene archivo de audio asociado.",
                parent=self.ventana)

    def ejecutar(self):
        self.ventana.mainloop()