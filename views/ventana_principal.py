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
        self.current_screen   = None
        self.now_playing      = tk.StringVar(value="Selecciona una canción")
        self.progress_val     = tk.DoubleVar(value=0)
        self.is_playing       = tk.BooleanVar(value=False)
        self.current_cancion  = None
        self.timer_id         = None
        self._duracion_actual = 0
        self._siguiente_callback = None

        self.player = MusicPlayer()  

        self.setup_ui()

    def setup_ui(self):
        outer = tk.Frame(self.ventana, bg=BG_DARK)
        outer.pack(fill="both", expand=True)

        # El player va PRIMERO: pack side="bottom" debe reservar espacio
        # antes de que sidebar y content tomen todo con side="left"
        self._crear_player(outer)

        self.sidebar = self._crear_sidebar(outer)

        content_wrap = tk.Frame(outer, bg=BG_DARK)
        content_wrap.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(content_wrap, bg=BG_DARK)
        self.content.pack(fill="both", expand=True, padx=28, pady=20)

        self.mostrar_home()

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

        self.prog_canvas = tk.Canvas(
            prog_row, height=16, bg=BG_CARD,
            highlightthickness=0, cursor="hand2"
        )
        self.prog_canvas.pack(side="left", fill="x", expand=True, padx=6)
        self.prog_canvas.bind("<Button-1>",   self._click_progreso)
        self.prog_canvas.bind("<B1-Motion>",  self._click_progreso)

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
    
    def _dibujar_progreso(self, pos=None):
        c = self.prog_canvas
        c.update_idletasks()
        w = c.winfo_width()
        if w <= 1:
            return
        c.delete("all")
        if pos is None:
            pos = self.progress_val.get()
        total = self._duracion_actual
        ratio = (pos / total) if total > 0 else 0
        cx = int(ratio * w)

        # Track de fondo
        c.create_rectangle(0, 6, w, 10, fill=BG_HOVER, outline="")
        # Parte completada
        if cx > 0:
            c.create_rectangle(0, 6, cx, 10, fill=ACCENT, outline="")
        # Bolita de posición
        c.create_oval(cx - 6, 2, cx + 6, 14, fill=ACCENT2, outline="")

    def _click_progreso(self, event):
        if self._duracion_actual <= 0:
            return
        w = self.prog_canvas.winfo_width()
        ratio = max(0.0, min(1.0, event.x / w))
        pos = ratio * self._duracion_actual
        self.progress_val.set(pos)
        m, s = divmod(int(pos), 60)
        self.lbl_tiempo_actual.config(text=f"{m}:{s:02d}")
        self._dibujar_progreso(pos)
        self.player.seek(pos)

    def _iniciar_loop_progreso(self):
        if self.timer_id:
            self.ventana.after_cancel(self.timer_id)

        def tick():
            if self.player.esta_reproduciendo():
                pos = self.player.get_posicion_segundos()
                self.progress_val.set(pos)
                m, s = divmod(int(pos), 60)
                self.lbl_tiempo_actual.config(text=f"{m}:{s:02d}")
                self._dibujar_progreso(pos)
                self.timer_id = self.ventana.after(500, tick)
            elif self.player.pausado:
                # Mantener el loop sin actualizar posición
                self.timer_id = self.ventana.after(500, tick)
            else:
                # Canción terminó naturalmente
                self.is_playing.set(False)
                self._actualizar_boton_play()
                self.progress_val.set(0)
                self.lbl_tiempo_actual.config(text="0:00")
                self._dibujar_progreso(0)
                if self._siguiente_callback:
                    self.ventana.after(300, self._siguiente_callback)

        self.timer_id = self.ventana.after(500, tick)

    def _resetear_player(self):
        self.player.detener()
        self.is_playing.set(False)
        self._actualizar_boton_play()
        self.progress_val.set(0)
        self.lbl_tiempo_actual.config(text="0:00")
        self._dibujar_progreso(0)

    def set_siguiente_callback(self, fn):
        self._siguiente_callback = fn

    def _cancion_anterior(self):
        self._resetear_player()

    def _cancion_siguiente(self):
        if self._siguiente_callback:
            self._resetear_player()
            self.ventana.after(100, self._siguiente_callback)
        else:
            self._resetear_player()

    def reproducir_cancion(self, cancion_data):
        self._siguiente_callback = None  # se reestablece desde ventana_playlist si aplica
        nombre   = cancion_data.get('nombre', '')
        artista  = cancion_data.get('artista', '')
        duracion = cancion_data.get('duracion', 0)
        ruta     = cancion_data.get('ruta_archivo')

        self.now_playing.set(f"{nombre} — {artista}")
        self.current_cancion = cancion_data

        if isinstance(duracion, (int, float)) and duracion > 0:
            self._duracion_actual = duracion
            m, s = divmod(int(duracion), 60)
            self.time_label.config(text=f"{m}:{s:02d}")
        else:
            self._duracion_actual = 0
            self.time_label.config(text="0:00")

        if ruta:
            ok = self.player.reproducir(ruta)
            if ok:
                self.progress_val.set(0)
                self.is_playing.set(True)
                self._actualizar_boton_play()
                self.ventana.after(50, lambda: self._dibujar_progreso(0))
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