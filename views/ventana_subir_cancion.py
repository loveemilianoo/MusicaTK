import tkinter as tk
from tkinter import messagebox, filedialog
from views.colores import *
from views.componentes import Componentes
from controller.CancionDAO import CancionDAO
from models.Cancion import Cancion
import os
import shutil

CARPETA_AUDIO = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio"
)

class VentanaSubirCancion:

    def __init__(self, usuario_actual, app_principal):
        self.usuario_actual = usuario_actual
        self.app = app_principal
        self.ruta_archivo_seleccionada = None  # ── NUEVO
        self.ventana = tk.Toplevel(app_principal.ventana)
        self.ventana.title("Subir nueva canción")
        self.ventana.geometry("800x700")
        self.ventana.configure(bg=BG_DARK)
        self.ventana.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK, padx=28, pady=20)
        root.pack(fill="both", expand=True)

        # Botón volver
        back = tk.Frame(root, bg=BG_DARK, cursor="hand2")
        back.pack(anchor="w", pady=(0, 20))
        back_lbl = tk.Label(back, text="← Volver", font=FONT_BODY, fg=ACCENT2, bg=BG_DARK)
        back_lbl.pack()
        for w in (back, back_lbl):
            w.bind("<Button-1>", lambda e: self.ventana.destroy())

        tk.Label(root, text="Subir nueva canción", font=FONT_TITLE,
                fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x", pady=(0, 20))

        body = tk.Frame(root, bg=BG_DARK)
        body.pack(fill="both", expand=True)

        # ── Columna izquierda ──────────────────────────────
        left = tk.Frame(body, bg=BG_DARK)
        left.pack(side="left", padx=(0, 30))

        # Drop zone
        self.drop_zone = tk.Canvas(left, width=180, height=180, bg=BG_CARD,
                                   highlightthickness=2,
                                   highlightbackground=ACCENT, cursor="hand2")
        self.drop_zone.pack()
        self.icono_id  = self.drop_zone.create_text(
            90, 60, text="🎵", font=("Helvetica", 48), fill=ACCENT)
        self.texto_id  = self.drop_zone.create_text(
            90, 110, text="Arrastra archivo", font=FONT_H3, fill=TEXT_SEC)
        self.drop_zone.create_text(
            90, 135, text="MP3, WAV, FLAC", font=FONT_TINY, fill=TEXT_MUT)

        # Botón examinar — ahora funcional
        btn_f = tk.Frame(left, bg=ACCENT, cursor="hand2")
        btn_f.pack(fill="x", pady=12)
        btn_lbl = tk.Label(btn_f, text="Examinar archivo", fg="white",
                           bg=ACCENT, font=FONT_BODY, pady=8)
        btn_lbl.pack(fill="x")
        for w in (btn_f, btn_lbl):
            w.bind("<Button-1>", lambda e: self._seleccionar_archivo())

        # Label que muestra el archivo elegido
        self.lbl_archivo = tk.Label(left, text="Ningún archivo seleccionado",
                                    font=FONT_TINY, fg=TEXT_MUT, bg=BG_DARK,
                                    wraplength=180)
        self.lbl_archivo.pack(pady=4)

        # ── Columna derecha ────────────────────────────────
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)

        self.entries = {}
        campos = [
            ("titulo",           "Título de la canción *", "Mi Canción"),
            ("fechaLanzamiento", "Fecha de lanzamiento *", "2026-12-01"),
        ]

        for key, label, placeholder in campos:
            tk.Label(right, text=label, font=FONT_H3, fg=TEXT_SEC,
                    bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 3))
            entry = tk.Entry(right, font=FONT_BODY, bg=BG_CARD, fg=TEXT_SEC,
                           insertbackground=ACCENT2, relief="flat", bd=0)
            entry.insert(0, placeholder)
            entry.pack(fill="x", ipady=8, ipadx=10)
            self.entries[key] = entry

        tk.Label(right, text="Duración (segundos) *", font=FONT_H3, fg=TEXT_SEC,
                bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 3))
        self.entries["duracion"] = tk.Entry(right, font=FONT_BODY, bg=BG_CARD,
                                            fg=TEXT_SEC, insertbackground=ACCENT2,
                                            relief="flat", bd=0)
        self.entries["duracion"].insert(0, "180")
        self.entries["duracion"].pack(fill="x", ipady=8, ipadx=10)

        tk.Label(right, text="Género", font=FONT_H3, fg=TEXT_SEC,
                bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 3))
        # Cargar géneros de la BD
        from controller.GeneroDAO import GeneroDAO
        generos = GeneroDAO.listar_todos_generos()

        self.genero_var = tk.StringVar()
        self.genero_ids = {} 

        genero_nombres = []
        for g in generos:
            genero_nombres.append(g.nombre)
            self.genero_ids[g.nombre] = g.id_genero

        if not genero_nombres:
            genero_nombres = ["Sin género"]
            self.genero_ids["Sin género"] = None
        self.genero_var.set(genero_nombres[0])
        combo_genero = tk.OptionMenu(right, self.genero_var, *genero_nombres)
        combo_genero.config(bg=BG_CARD, fg=TEXT_PRI, font=FONT_BODY,
                            activebackground=BG_HOVER, relief="flat",
                            highlightthickness=0)
        combo_genero.pack(fill="x", ipady=4)

        # Visibilidad
        tk.Label(right, text="Visibilidad", font=FONT_H3, fg=TEXT_SEC,
                bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 4))
        self.visibilidad = tk.StringVar(value="Pública")
        vis_row = tk.Frame(right, bg=BG_DARK)
        vis_row.pack(fill="x")
        for opt in ["Pública", "Privada"]:
            tk.Radiobutton(vis_row, text=opt, variable=self.visibilidad, value=opt,
                          bg=BG_DARK, fg=TEXT_PRI, selectcolor=BG_CARD,
                          activebackground=BG_DARK, font=FONT_SMALL,
                          borderwidth=0, highlightthickness=0).pack(side="left", padx=(0, 14))

        # Botón publicar
        pub_f = tk.Frame(right, bg=GREEN, cursor="hand2")
        pub_f.pack(fill="x", pady=(20, 0), ipadx=14, ipady=10)
        pub_lbl = tk.Label(pub_f, text="PUBLICAR CANCIÓN", fg=BG_DARK,
                          bg=GREEN, font=("Helvetica", 11, "bold"))
        pub_lbl.pack(fill="x")
        for w in (pub_f, pub_lbl):
            w.bind("<Button-1>", lambda e: self._publicar_cancion())
            w.bind("<Enter>", lambda e: pub_f.configure(bg="#22C55E") or pub_lbl.configure(bg="#22C55E"))
            w.bind("<Leave>", lambda e: pub_f.configure(bg=GREEN) or pub_lbl.configure(bg=GREEN))

    # ── NUEVO ──────────────────────────────────────────────
    def _seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar canción",
            filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg *.flac")]
        )
        if ruta:
            self.ruta_archivo_seleccionada = ruta
            nombre = os.path.basename(ruta)
            self.lbl_archivo.config(text=nombre, fg=ACCENT2)
            self.drop_zone.itemconfig(self.texto_id, text=nombre)

    # ──────────────────────────────────────────────────────
    def _publicar_cancion(self):
        titulo          = self.entries["titulo"].get().strip()
        duracion_str    = self.entries["duracion"].get().strip()
        fechaLanzamiento = self.entries["fechaLanzamiento"].get().strip()

        if not titulo or titulo == "Mi Canción":
            messagebox.showerror("Error", "Debes ingresar un título", parent=self.ventana)
            return

        # ── NUEVO: validar que se eligió archivo ──
        if not self.ruta_archivo_seleccionada:
            messagebox.showerror("Error", "Selecciona un archivo de audio",
                                 parent=self.ventana)
            return

        try:
            duracion = int(duracion_str)
        except ValueError:
            messagebox.showerror("Error", "La duración debe ser un número", parent=self.ventana)
            return

        if not self._es_fecha_valida(fechaLanzamiento):
            messagebox.showerror("Error", "Fecha inválida (usa YYYY-MM-DD)", parent=self.ventana)
            return

        try:
            from datetime import datetime
            fecha_obj = datetime.strptime(fechaLanzamiento, "%Y-%m-%d").date()

            # Guardar sin ruta primero para obtener el ID
            cancion = Cancion(
                nombre=titulo,
                duracion=duracion,
                id_artista=self.usuario_actual.id_persona,
                fecha_lanzamiento=fecha_obj,
                ruta_de_archivo=None
            )
            id_resultado = CancionDAO.crear_cancion(cancion)

            if not id_resultado:
                messagebox.showerror("Error", "No se pudo guardar la canción",
                                     parent=self.ventana)
                return

            # ── NUEVO: copiar archivo a carpeta local ──────
            os.makedirs(CARPETA_AUDIO, exist_ok=True)
            extension = os.path.splitext(self.ruta_archivo_seleccionada)[1]
            nombre_destino = f"{int(id_resultado)}_{titulo.replace(' ', '_')}{extension}"
            ruta_destino   = os.path.join(CARPETA_AUDIO, nombre_destino)
            shutil.copy2(self.ruta_archivo_seleccionada, ruta_destino)

            # Guardar ruta relativa en BD
            ruta_relativa = f"audio/{nombre_destino}"
            CancionDAO.actualizar_ruta(id_resultado, ruta_relativa)

            # Asociar el género seleccionado a la canción
            id_genero = self.genero_ids.get(self.genero_var.get())
            if id_genero is not None:
                from controller.GeneroDAO import GeneroDAO
                GeneroDAO.agregar_genero_a_cancion(id_resultado, id_genero)
            # ───────────────────────────────────────────────

            messagebox.showinfo("Éxito",
                                f"¡Canción publicada!\nID: {int(id_resultado)}",
                                parent=self.ventana)
            self.ventana.destroy()
            if hasattr(self.app, 'mostrar_portal_artista'):
                self.app.mostrar_portal_artista()

        except Exception as e:
            messagebox.showerror("Error", f"Error al publicar: {e}", parent=self.ventana)

    def _es_fecha_valida(self, fecha_str):
        from datetime import datetime
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False