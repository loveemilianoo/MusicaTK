import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes

class VentanaAgregarAPlaylist:
    """
    Popup que muestra las playlists del usuario y permite
    marcar / desmarcar en cuál añadir una canción.
    
    Úsalo así (desde cualquier ventana que tenga app.ventana):
    
        VentanaAgregarAPlaylist(
            usuario_actual  = self.usuario_actual,
            cancion_data    = {"id": 3, "nombre": "Neon Pulse", "artista": "Riders"},
            app_principal   = self.app,
            on_guardado     = lambda: self._recargar(),   # opcional
        )

    Requiere en PlaylistDAO:
        PlaylistDAO.obtener_playlists_por_usuario(id_persona) -> list[Playlist]
            Playlist tiene: .id_playlist, .nombre
        PlaylistDAO.cancion_en_playlist(id_cancion, id_playlist) -> bool
        PlaylistDAO.agregar_cancion_a_playlist(id_cancion, id_playlist) -> bool
        PlaylistDAO.quitar_cancion_de_playlist(id_playlist, id_cancion) -> bool
    """

    def __init__(self, usuario_actual, cancion_data: dict,
                 app_principal, on_guardado=None):
        self.usuario_actual = usuario_actual
        self.cancion = cancion_data      # {"id", "nombre", "artista"}
        self.app = app_principal
        self.on_guardado = on_guardado

        # {id_playlist: BooleanVar}  → estado checkbox
        self.checks: dict[int, tk.BooleanVar] = {}
        # Estado inicial (antes de tocar nada)
        self.estado_inicial: dict[int, bool] = {}

        self.ventana = tk.Toplevel(app_principal.ventana)
        self.ventana.title("Agregar a playlist")
        self.ventana.geometry("380x500")
        self.ventana.configure(bg=BG_DARK)
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        self._setup_ui()

    # ──────────────────────────────────────────────────────────
    def _setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK, padx=24, pady=20)
        root.pack(fill="both", expand=True)

        # Título + nombre de la canción
        tk.Label(root, text="Agregar a playlist", font=FONT_H2,
                 fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x")
        nombre = self.cancion.get("nombre", "—")
        artista = self.cancion.get("artista", "")
        subtitulo = f"«{nombre}»" + (f"  —  {artista}" if artista else "")
        tk.Label(root, text=subtitulo, font=FONT_SMALL,
                 fg=ACCENT2, bg=BG_DARK, anchor="w").pack(fill="x", pady=(2, 12))

        # Búsqueda de playlist
        sw = tk.Frame(root, bg=BG_CARD)
        sw.pack(fill="x", pady=(0, 8))
        tk.Label(sw, text="🔍", fg=TEXT_MUT, bg=BG_CARD, padx=8).pack(side="left")
        self.search_entry = tk.Entry(sw, font=FONT_BODY, bg=BG_CARD, fg=TEXT_PRI,
                                     insertbackground=ACCENT2, relief="flat", bd=0, width=28)
        self.search_entry.pack(side="left", pady=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self._filtrar())

        Componentes.divider(root)

        # Lista de playlists (scrollable frame manual)
        self.lista_frame = tk.Frame(root, bg=BG_DARK)
        self.lista_frame.pack(fill="both", expand=True)
        self._cargar_playlists()

        Componentes.divider(root)

        # Botón crear nueva playlist rápida
        nueva_row = tk.Frame(root, bg=BG_DARK, cursor="hand2")
        nueva_row.pack(fill="x", pady=(4, 10))
        tk.Label(nueva_row, text="＋", fg=GREEN, bg=BG_DARK,
                 font=("Helvetica", 14, "bold"), padx=4).pack(side="left")
        nueva_l = tk.Label(nueva_row, text="Crear nueva playlist", font=FONT_BODY,
                           fg=GREEN, bg=BG_DARK, cursor="hand2")
        nueva_l.pack(side="left")
        for w in (nueva_row, nueva_l):
            w.bind("<Button-1>", lambda e: self._crear_nueva_playlist())

        # Botones guardar / cancelar
        btn_row = tk.Frame(root, bg=BG_DARK)
        btn_row.pack(fill="x")

        cancel_f = tk.Frame(btn_row, bg=BG_CARD, cursor="hand2")
        cancel_f.pack(side="left", expand=True, fill="x", padx=(0, 8))
        cl = tk.Label(cancel_f, text="Cancelar", fg=TEXT_SEC, bg=BG_CARD,
                      font=FONT_BODY, pady=9)
        cl.pack(fill="x")
        for w in (cancel_f, cl):
            w.bind("<Button-1>", lambda e: self.ventana.destroy())

        save_f = tk.Frame(btn_row, bg=ACCENT, cursor="hand2")
        save_f.pack(side="left", expand=True, fill="x")
        sl = tk.Label(save_f, text="Guardar", fg=BG_DARK, bg=ACCENT,
                      font=("Helvetica", 10, "bold"), pady=9)
        sl.pack(fill="x")
        for w in (save_f, sl):
            w.bind("<Button-1>", lambda e: self._guardar())
            w.bind("<Enter>", lambda e: save_f.configure(bg=ACCENT2) or sl.configure(bg=ACCENT2))
            w.bind("<Leave>", lambda e: save_f.configure(bg=ACCENT) or sl.configure(bg=ACCENT))

    # ──────────────────────────────────────────────────────────
    def _cargar_playlists(self, filtro=""):
        for w in self.lista_frame.winfo_children():
            w.destroy()

        # ── CONECTAR CON DAO ──────────────────────────────────
        from controller.PlaylistDAO import PlaylistDAO
        playlists = PlaylistDAO.obtener_playlists_por_usuario(self.usuario_actual.id_persona)
        for p in playlists:
            ya = PlaylistDAO.cancion_en_playlist(self.cancion["id"], p.id_playlist)
            self.estado_inicial[p.id_playlist] = ya
            if p.id_playlist not in self.checks:
                self.checks[p.id_playlist] = tk.BooleanVar(value=ya)
        
        playlists_a_mostrar = [
            p for p in playlists
            if filtro.lower() in p.nombre.lower()
        ] if filtro else playlists
        
        if not playlists_a_mostrar:
            tk.Label(self.lista_frame, text="Sin resultados",
                     font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=16)
            return

        for p in playlists_a_mostrar:
            pid = p.id_playlist
            var = self.checks[pid]
            already = self.estado_inicial[pid]

            row = tk.Frame(self.lista_frame, bg=BG_DARK, cursor="hand2")
            row.pack(fill="x", pady=4)

            # Ícono
            ic = tk.Canvas(row, width=40, height=40, bg=ACCENT, highlightthickness=0)
            ic.pack(side="left", padx=(0, 10))
            ic.create_text(20, 20, text="♪", font=("Helvetica", 14), fill=ACCENT2)

            # Info
            info = tk.Frame(row, bg=BG_DARK)
            info.pack(side="left", expand=True, fill="x")
            tk.Label(info, text=p.nombre, font=FONT_H3,
                     fg=TEXT_PRI, bg=BG_DARK).pack(anchor="w")
            meta = "0 canciones"  # Se puede agregar método en Playlist para contar canciones
            if already:
                meta += "  ·  ✔ ya incluida"
            tk.Label(info, text=meta, font=FONT_TINY, fg=TEXT_MUT, bg=BG_DARK).pack(anchor="w")

            # Checkbox
            chk = tk.Checkbutton(row, variable=var, bg=BG_DARK,
                                  activebackground=BG_DARK, selectcolor=BG_DARK,
                                  fg=GREEN, cursor="hand2",
                                  highlightthickness=0, borderwidth=0)
            chk.pack(side="right", padx=6)

            # Click en la fila también toggle
            for w in (row, info):
                w.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))
            row.bind("<Enter>", lambda e, r=row: r.configure(bg=BG_HOVER))
            row.bind("<Leave>", lambda e, r=row: r.configure(bg=BG_DARK))

    def _filtrar(self):
        self._cargar_playlists(self.search_entry.get())

    # ──────────────────────────────────────────────────────────
    def _guardar(self):
        id_cancion = self.cancion.get("id")
        cambios = 0
        errores = 0

        from controller.PlaylistDAO import PlaylistDAO

        for pid, var in self.checks.items():
            estado_nuevo = var.get()
            estado_previo = self.estado_inicial.get(pid, False)

            try:
                if estado_nuevo and not estado_previo:
                    PlaylistDAO.agregar_cancion_a_playlist(id_cancion, pid)
                    cambios += 1
                elif not estado_nuevo and estado_previo:
                    PlaylistDAO.quitar_cancion_de_playlist(id_cancion, pid)
                    cambios += 1
            except Exception as e:
                print(f"Error al actualizar playlist {pid}: {e}")
                errores += 1

        if cambios or errores:
            msg = f"Cambios guardados ({cambios} playlist(s) actualizadas)."
            if errores:
                msg += f"\n⚠ {errores} playlist(s) con error."
            messagebox.showinfo("Resultado", msg, parent=self.ventana)
        
        if self.on_guardado:
            self.on_guardado()
        self.ventana.destroy()

    # ──────────────────────────────────────────────────────────
    def _crear_nueva_playlist(self):
        """Abre VentanaCrearPlaylist y, al cerrar, recarga la lista."""
        from views.ventana_crear_playlist import VentanaCrearPlaylist

        def on_creada():
            # Reinicia checks y recarga
            self.checks.clear()
            self.estado_inicial.clear()
            self._cargar_playlists()

        VentanaCrearPlaylist(
            usuario_actual=self.usuario_actual,
            on_creada_callback=on_creada,
            parent_ventana=self.ventana,
        )