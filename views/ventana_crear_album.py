import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes

class VentanaCrearAlbum:
    """
    Popup para crear un álbum y armarle el tracklist.
    Patrón igual a VentanaSubirCancion (Toplevel).

    Requiere en AlbumDAO:
        AlbumDAO.crear_album(album_obj) -> id_album | None
        AlbumDAO.agregar_cancion_a_album(id_album, id_cancion) -> bool
    Requiere en CancionDAO:
        CancionDAO.obtener_canciones_por_artista(id_artista) -> list[Cancion]
        CancionDAO.listar_todas_canciones() -> list[Cancion]
    """

    def __init__(self, usuario_actual, app_principal, on_creado_callback=None):
        self.usuario_actual = usuario_actual
        self.app = app_principal
        self.on_creado = on_creado_callback
        # Canciones seleccionadas para el tracklist: lista de dicts
        self.tracklist: list[dict] = []
        self.ventana = tk.Toplevel(app_principal.ventana)
        self.ventana.title("Crear álbum")
        self.ventana.geometry("880x660")
        self.ventana.configure(bg=BG_DARK)
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        self._setup_ui()

    # ──────────────────────────────────────────────────────────
    def _setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK, padx=28, pady=20)
        root.pack(fill="both", expand=True)

        # Título
        back = tk.Frame(root, bg=BG_DARK, cursor="hand2")
        back.pack(anchor="w")
        back_l = tk.Label(back, text="← Cancelar", font=FONT_BODY, fg=ACCENT2, bg=BG_DARK)
        back_l.pack()
        for w in (back, back_l):
            w.bind("<Button-1>", lambda e: self.ventana.destroy())

        tk.Label(root, text="Crear nuevo álbum", font=FONT_TITLE,
                 fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 20))

        body = tk.Frame(root, bg=BG_DARK)
        body.pack(fill="both", expand=True)

        # ── Columna izquierda ──────────────────────────────────
        left = tk.Frame(body, bg=BG_DARK)
        left.pack(side="left", padx=(0, 30))

        # Portada
        cover = tk.Canvas(left, width=200, height=200, bg=BG_CARD,
                          highlightthickness=2, highlightbackground=ACCENT, cursor="hand2")
        cover.pack()
        cover.create_text(100, 80,  text="🖼", font=("Helvetica", 42), fill=ACCENT)
        cover.create_text(100, 135, text="Portada del álbum", font=FONT_SMALL, fill=TEXT_SEC)
        cover.create_text(100, 155, text="JPG · PNG · máx 5 MB", font=FONT_TINY, fill=TEXT_MUT)
        cover.bind("<Button-1>", lambda e: messagebox.showinfo(
            "Info", "Selección de imagen — conecta con tkinter.filedialog",
            parent=self.ventana))

        # Tipo de lanzamiento
        tk.Label(left, text="Tipo de lanzamiento", font=FONT_H3, fg=TEXT_SEC,
                 bg=BG_DARK, anchor="w").pack(fill="x", pady=(18, 6))
        self.tipo_var = tk.StringVar(value="Álbum")
        for opt in ["Álbum", "EP", "Single"]:
            tk.Radiobutton(left, text=opt, variable=self.tipo_var, value=opt,
                           bg=BG_DARK, fg=TEXT_PRI, selectcolor=BG_DARK,
                           activebackground=BG_DARK, font=FONT_BODY,
                           borderwidth=0, highlightthickness=0).pack(anchor="w")

        # Visibilidad
        tk.Label(left, text="Visibilidad", font=FONT_H3, fg=TEXT_SEC,
                 bg=BG_DARK, anchor="w").pack(fill="x", pady=(14, 6))
        self.vis_var = tk.StringVar(value="Pública")
        for opt in ["Pública", "Privada"]:
            tk.Radiobutton(left, text=opt, variable=self.vis_var, value=opt,
                           bg=BG_DARK, fg=TEXT_PRI, selectcolor=BG_DARK,
                           activebackground=BG_DARK, font=FONT_BODY,
                           borderwidth=0, highlightthickness=0).pack(anchor="w")

        # ── Columna derecha ────────────────────────────────────
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)

        self.entries = {}
        for key, label, ph in [
            ("nombre", "Nombre del álbum *", "Ej: Neon Horizons"),
            ("fechaLanzamiento",   "Fecha de lanzamiento",              "Ej: 2024-08-15"),
            ("genero", "Género",             "Ej: Synthwave, Electrónica"),
        ]:
            tk.Label(right, text=label, font=FONT_H3, fg=TEXT_SEC,
                     bg=BG_DARK, anchor="w").pack(fill="x", pady=(8, 3))
            e = tk.Entry(right, font=FONT_BODY, bg=BG_CARD, fg=TEXT_SEC,
                         insertbackground=ACCENT2, relief="flat", bd=0)
            e.insert(0, ph)
            e.pack(fill="x", ipady=8, ipadx=10)
            self.entries[key] = e

        # Tracklist header
        tl_header = tk.Frame(right, bg=BG_DARK)
        tl_header.pack(fill="x", pady=(16, 6))
        tk.Label(tl_header, text="Tracklist", font=FONT_H2,
                 fg=TEXT_PRI, bg=BG_DARK).pack(side="left")
        add_btn = tk.Frame(tl_header, bg=BG_CARD, cursor="hand2")
        add_btn.pack(side="right")
        add_l = tk.Label(add_btn, text="＋ Agregar pista", font=FONT_SMALL,
                         fg=ACCENT2, bg=BG_CARD, padx=10, pady=4)
        add_l.pack()
        for w in (add_btn, add_l):
            w.bind("<Button-1>", lambda e: self._abrir_selector_cancion())

        # Contenedor del tracklist (scrollable con canvas)
        self.tracklist_frame = tk.Frame(right, bg=BG_DARK)
        self.tracklist_frame.pack(fill="both", expand=True)
        self._refrescar_tracklist()

        # Botón publicar
        pub_f = tk.Frame(right, bg=ACCENT, cursor="hand2")
        pub_f.pack(fill="x", pady=14)
        pub_l = tk.Label(pub_f, text="PUBLICAR ÁLBUM", fg=BG_DARK, bg=ACCENT,
                         font=("Helvetica", 11, "bold"), pady=10)
        pub_l.pack(fill="x")
        for w in (pub_f, pub_l):
            w.bind("<Button-1>", lambda e: self._publicar())
            w.bind("<Enter>", lambda e: pub_f.configure(bg=ACCENT2) or pub_l.configure(bg=ACCENT2))
            w.bind("<Leave>", lambda e: pub_f.configure(bg=ACCENT) or pub_l.configure(bg=ACCENT))

    # ──────────────────────────────────────────────────────────
    def _refrescar_tracklist(self):
        for w in self.tracklist_frame.winfo_children():
            w.destroy()

        if not self.tracklist:
            tk.Label(self.tracklist_frame,
                     text="Aún no hay pistas. Usa '＋ Agregar pista'.",
                     font=FONT_SMALL, fg=TEXT_MUT, bg=BG_DARK).pack(pady=10)
            return

        for i, cancion in enumerate(self.tracklist, 1):
            tr = tk.Frame(self.tracklist_frame, bg=BG_CARD)
            tr.pack(fill="x", pady=2, ipadx=6, ipady=4)

            tk.Label(tr, text=str(i), font=FONT_SMALL, fg=TEXT_MUT,
                     bg=BG_CARD, width=3).pack(side="left")
            tk.Label(tr, text="≡", fg=TEXT_MUT, bg=BG_CARD,
                     font=FONT_H3, padx=4).pack(side="left")
            tk.Label(tr, text=cancion.get("nombre", "—"), font=FONT_BODY,
                     fg=TEXT_PRI, bg=BG_CARD, width=26, anchor="w").pack(side="left")

            dur = cancion.get("duracion", 0)
            if isinstance(dur, (int, float)) and dur > 0:
                dur_txt = f"{int(dur // 60)}:{int(dur % 60):02d}"
            else:
                dur_txt = "—"
            tk.Label(tr, text=dur_txt, font=FONT_TINY, fg=TEXT_MUT,
                     bg=BG_CARD).pack(side="left", padx=6)

            rm = tk.Label(tr, text="✕", fg="#EF4444", bg=BG_CARD,
                          font=FONT_SMALL, cursor="hand2")
            rm.pack(side="right", padx=8)
            rm.bind("<Button-1>", lambda e, idx=i-1: self._quitar_pista(idx))

    def _quitar_pista(self, idx):
        del self.tracklist[idx]
        self._refrescar_tracklist()

    # ──────────────────────────────────────────────────────────
    def _es_fecha_valida(self, fecha_str):
        """Valida si la fecha está en formato YYYY-MM-DD."""
        from datetime import datetime
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # ──────────────────────────────────────────────────────────
    def _abrir_selector_cancion(self):
        """Abre un popup para buscar y seleccionar canciones del artista."""
        sel = _SelectorCancionParaAlbum(
            parent_ventana=self.ventana,
            id_artista=self.usuario_actual.id_persona,
            ya_en_tracklist=[c["id"] for c in self.tracklist],
            on_seleccionada=self._agregar_al_tracklist,
        )

    def _agregar_al_tracklist(self, cancion_dict):
        """Recibe un dict con id, nombre, duracion."""
        if any(c["id"] == cancion_dict["id"] for c in self.tracklist):
            messagebox.showwarning("Aviso", "Esa canción ya está en el tracklist.",
                                   parent=self.ventana)
            return
        self.tracklist.append(cancion_dict)
        self._refrescar_tracklist()

    # ──────────────────────────────────────────────────────────
    def _publicar(self):
        nombre = self.entries["nombre"].get().strip()
        fechaLanzamiento = self.entries["fechaLanzamiento"].get().strip()

        if not nombre or nombre.startswith("Ej:"):
            messagebox.showerror("Error", "El nombre del álbum es obligatorio.",
                                 parent=self.ventana)
            return
        if not fechaLanzamiento or not self._es_fecha_valida(fechaLanzamiento):
            messagebox.showerror("Error", "La fecha de lanzamiento no es válida.",
                                 parent=self.ventana)
            return

        # ── CONECTAR CON DAO ──────────────────────────────────
        from models.Album import Album
        from controller.AlbumDAO import AlbumDAO
        from datetime import datetime
        
        try:
            # Convertir string de fecha a objeto date
            fecha_obj = datetime.strptime(fechaLanzamiento, "%Y-%m-%d").date()
            album = Album(nombre=nombre, id_persona=self.usuario_actual.id_persona, fecha_lanzamiento=fecha_obj)
            id_album = AlbumDAO.crear_album(album)
            if id_album:
                for c in self.tracklist:
                    AlbumDAO.agregar_cancion_a_album(id_album, c["id"])
                messagebox.showinfo("Éxito", f"Álbum '{nombre}' publicado.", parent=self.ventana)
                if self.on_creado:
                    self.on_creado()
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", 
                    "No se pudo crear el álbum.\nRevisa la consola para más detalles.", 
                    parent=self.ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el álbum: {str(e)}", parent=self.ventana)


class _SelectorCancionParaAlbum:
    """
    Popup interno: busca canciones del artista y devuelve la seleccionada.
    Se instancia desde VentanaCrearAlbum, no se usa directamente.
    """

    def __init__(self, parent_ventana, id_artista, ya_en_tracklist, on_seleccionada):
        self.id_artista = id_artista
        self.ya_en = ya_en_tracklist
        self.on_seleccionada = on_seleccionada

        self.ventana = tk.Toplevel(parent_ventana)
        self.ventana.title("Seleccionar pista")
        self.ventana.geometry("480x460")
        self.ventana.configure(bg=BG_DARK)
        self.ventana.grab_set()
        self._setup_ui()

    def _setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK, padx=20, pady=16)
        root.pack(fill="both", expand=True)

        tk.Label(root, text="Agregar pista al álbum", font=FONT_H2,
                 fg=TEXT_PRI, bg=BG_DARK).pack(anchor="w", pady=(0, 10))

        # Búsqueda
        sw = tk.Frame(root, bg=BG_CARD)
        sw.pack(fill="x", pady=(0, 10))
        tk.Label(sw, text="🔍", fg=TEXT_MUT, bg=BG_CARD, padx=8).pack(side="left")
        self.search_entry = tk.Entry(sw, font=FONT_BODY, bg=BG_CARD, fg=TEXT_PRI,
                                     insertbackground=ACCENT2, relief="flat", bd=0, width=36)
        self.search_entry.pack(side="left", pady=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self._filtrar())

        Componentes.divider(root)

        # Lista
        self.lista_frame = tk.Frame(root, bg=BG_DARK)
        self.lista_frame.pack(fill="both", expand=True)
        self._cargar_canciones()

        # Botón cancelar
        cancel = tk.Frame(root, bg=BG_CARD, cursor="hand2")
        cancel.pack(fill="x", pady=(10, 0))
        cl = tk.Label(cancel, text="Cancelar", fg=TEXT_SEC, bg=BG_CARD,
                      font=FONT_BODY, pady=8)
        cl.pack(fill="x")
        for w in (cancel, cl):
            w.bind("<Button-1>", lambda e: self.ventana.destroy())

    def _cargar_canciones(self, filtro=""):
        for w in self.lista_frame.winfo_children():
            w.destroy()

        # ── CONECTAR CON DAO ──────────────────────────────────
        from controller.CancionDAO import CancionDAO
        if filtro:
            canciones_raw = CancionDAO.buscar_cancion_por_nombre(filtro)
        else:
            canciones_raw = CancionDAO.obtener_canciones_por_artista(self.id_artista)
        canciones = [{"id": c.id_cancion, "nombre": c.nombre, "duracion": c.duracion}
                     for c in canciones_raw]

        if not canciones:
            tk.Label(self.lista_frame, text="Sin resultados",
                     font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=20)
            return

        for c in canciones:
            already = c["id"] in self.ya_en
            bg = BG_HOVER if already else BG_DARK
            row = tk.Frame(self.lista_frame, bg=bg,
                           cursor="arrow" if already else "hand2")
            row.pack(fill="x", pady=2)

            ic = tk.Canvas(row, width=34, height=34, bg=ACCENT, highlightthickness=0)
            ic.pack(side="left", padx=(0, 10))
            ic.create_text(17, 17, text="♫", font=("Helvetica", 11), fill=ACCENT2)

            info = tk.Frame(row, bg=bg)
            info.pack(side="left", expand=True, fill="x")
            tk.Label(info, text=c["nombre"], font=FONT_H3, fg=TEXT_PRI, bg=bg).pack(anchor="w")

            dur = c.get("duracion", 0)
            dur_txt = f"{int(dur // 60)}:{int(dur % 60):02d}" if dur else "—"
            tk.Label(row, text=dur_txt, font=FONT_TINY, fg=TEXT_MUT, bg=bg).pack(side="right", padx=8)

            if already:
                tk.Label(row, text="✔ ya incluida", font=FONT_TINY,
                         fg=GREEN, bg=bg).pack(side="right", padx=6)
            else:
                add_l = tk.Label(row, text="＋", fg=ACCENT2, bg=bg,
                                 font=("Helvetica", 14, "bold"), cursor="hand2", padx=8)
                add_l.pack(side="right")
                add_l.bind("<Button-1>", lambda e, cancion=c: self._seleccionar(cancion))
                row.bind("<Button-1>",   lambda e, cancion=c: self._seleccionar(cancion))
                row.bind("<Enter>", lambda e, r=row, inf=info: (
                    r.configure(bg=BG_HOVER), inf.configure(bg=BG_HOVER)))
                row.bind("<Leave>", lambda e, r=row, inf=info: (
                    r.configure(bg=BG_DARK), inf.configure(bg=BG_DARK)))

    def _filtrar(self):
        self._cargar_canciones(self.search_entry.get())

    def _seleccionar(self, cancion):
        self.on_seleccionada(cancion)
        self.ventana.destroy()