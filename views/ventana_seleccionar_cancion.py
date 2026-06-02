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
        self.ventana.title("Agregar canciones")
        self.ventana.geometry("520x580")
        self.ventana.configure(bg=BG_DARK)
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        # IDs que ya están en la playlist (antes de abrir esta ventana)
        try:
            rows = PlaylistDAO.obtener_canciones_playlist(self.playlist_id)
            self._ya_en_playlist = {row[0] for row in rows}
        except Exception:
            self._ya_en_playlist = set()

        self._setup_ui()

    def _setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK, padx=20, pady=16)
        root.pack(fill="both", expand=True)

        tk.Label(root, text="Agregar canciones", font=FONT_H2,
                 fg=TEXT_PRI, bg=BG_DARK).pack(anchor="w", pady=(0, 10))

        # Barra de búsqueda
        sw = tk.Frame(root, bg=BG_CARD)
        sw.pack(fill="x", pady=(0, 10))
        tk.Label(sw, text="🔍", fg=TEXT_MUT, bg=BG_CARD, padx=8).pack(side="left")
        self.search_entry = tk.Entry(sw, font=FONT_BODY, bg=BG_CARD, fg=TEXT_PRI,
                                     insertbackground=ACCENT2, relief="flat", bd=0, width=36)
        self.search_entry.pack(side="left", pady=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self._filtrar())

        Componentes.divider(root)

        # Lista de canciones
        self.lista_frame = tk.Frame(root, bg=BG_DARK)
        self.lista_frame.pack(fill="both", expand=True)
        self._cargar_canciones()

        # Botón listo
        done_f = tk.Frame(root, bg=ACCENT, cursor="hand2")
        done_f.pack(fill="x", pady=(10, 0))
        done_l = tk.Label(done_f, text="Listo", fg=BG_DARK, bg=ACCENT,
                          font=("Helvetica", 11, "bold"), pady=10)
        done_l.pack(fill="x")
        for w in (done_f, done_l):
            w.bind("<Button-1>", lambda e: self.ventana.destroy())
            w.bind("<Enter>", lambda e: done_f.configure(bg=ACCENT2) or done_l.configure(bg=ACCENT2))
            w.bind("<Leave>", lambda e: done_f.configure(bg=ACCENT) or done_l.configure(bg=ACCENT))

    def _cargar_canciones(self, filtro=""):
        for w in self.lista_frame.winfo_children():
            w.destroy()

        if filtro:
            canciones = CancionDAO.buscar_cancion_por_nombre(filtro)
        else:
            canciones = CancionDAO.obtener_todas_canciones()

        if not canciones:
            tk.Label(self.lista_frame, text="Sin resultados",
                     font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=20)
            return

        for c in canciones:
            ya_en = c.id_cancion in self._ya_en_playlist
            bg = BG_HOVER if ya_en else BG_DARK

            row = tk.Frame(self.lista_frame, bg=bg,
                           cursor="arrow" if ya_en else "hand2")
            row.pack(fill="x", pady=2)

            ic = tk.Canvas(row, width=34, height=34, bg=ACCENT, highlightthickness=0)
            ic.pack(side="left", padx=(0, 10))
            ic.create_text(17, 17, text="♫", font=("Helvetica", 11), fill=ACCENT2)

            info = tk.Frame(row, bg=bg)
            info.pack(side="left", expand=True, fill="x")
            tk.Label(info, text=c.nombre, font=FONT_H3,
                     fg=TEXT_PRI, bg=bg).pack(anchor="w")
            artista = getattr(c, "nombre_artista", "") or ""
            if artista:
                tk.Label(info, text=artista, font=FONT_TINY,
                         fg=TEXT_MUT, bg=bg).pack(anchor="w")

            dur = c.duracion
            dur_txt = f"{int(dur // 60)}:{int(dur % 60):02d}" if dur else "—"
            tk.Label(row, text=dur_txt, font=FONT_TINY,
                     fg=TEXT_MUT, bg=bg).pack(side="right", padx=8)

            if ya_en:
                tk.Label(row, text="✔ ya en playlist", font=FONT_TINY,
                         fg=GREEN, bg=bg).pack(side="right", padx=6)
            else:
                add_l = tk.Label(row, text="＋", fg=ACCENT2, bg=bg,
                                 font=("Helvetica", 14, "bold"), cursor="hand2", padx=8)
                add_l.pack(side="right")
                add_l.bind("<Button-1>", lambda e, cancion=c: self._agregar(cancion))
                row.bind("<Button-1>",   lambda e, cancion=c: self._agregar(cancion))
                row.bind("<Enter>", lambda e, r=row, inf=info: (
                    r.configure(bg=BG_HOVER), inf.configure(bg=BG_HOVER)))
                row.bind("<Leave>", lambda e, r=row, inf=info: (
                    r.configure(bg=BG_DARK), inf.configure(bg=BG_DARK)))

    def _filtrar(self):
        self._cargar_canciones(self.search_entry.get())

    def _agregar(self, cancion):
        ok = PlaylistDAO.agregar_cancion_a_playlist(cancion.id_cancion, self.playlist_id)
        if ok:
            self._ya_en_playlist.add(cancion.id_cancion)
            self.on_agregada()
            # Refresca la lista para marcar la canción como ya añadida
            self._cargar_canciones(self.search_entry.get())
        else:
            messagebox.showwarning("Advertencia",
                                   "No se pudo agregar la canción.\n"
                                   "Es posible que ya esté en la playlist.",
                                   parent=self.ventana)
