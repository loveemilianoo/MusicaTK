import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from views.colores import *
from views.componentes import Componentes
from controller.CancionDAO import CancionDAO
import os
import shutil

CARPETA_AUDIO = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio"
)


class VentanaEditarCancion:
    """
    Popup para editar una canción existente.
    Usa el patrón Toplevel igual que VentanaEditarPerfilArtista.
    """

    def __init__(self, id_cancion, usuario_actual, app_principal,
                 on_guardado_callback=None):
        self.usuario_actual = usuario_actual
        self.app = app_principal
        self.on_guardado = on_guardado_callback
        self.nueva_ruta_audio = None  # ruta del archivo nuevo si se reemplaza

        # Cargar la canción desde la BD
        self.cancion = CancionDAO.obtener_cancion_por_id(id_cancion)
        if not self.cancion:
            messagebox.showerror("Error", "No se pudo cargar la canción")
            return

        self.ventana = tk.Toplevel(app_principal.ventana)
        self.ventana.title("Editar canción")
        self.ventana.geometry("520x560")
        self.ventana.configure(bg=BG_DARK)
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        self._setup_ui()

    # ──────────────────────────────────────────────────────────
    def _setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK, padx=30, pady=20)
        root.pack(fill="both", expand=True)

        tk.Label(root, text="Editar canción", font=FONT_TITLE,
                 fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x", pady=(0, 20))

        Componentes.divider(root)

        # ── Formulario ─────────────────────────────────────────
        form = tk.Frame(root, bg=BG_DARK)
        form.pack(fill="both", expand=True)

        self.entries = {}

        # Valores actuales formateados
        fecha_actual = ""
        if self.cancion.fecha_lanzamiento:
            try:
                fecha_actual = self.cancion.fecha_lanzamiento.strftime("%Y-%m-%d")
            except AttributeError:
                fecha_actual = str(self.cancion.fecha_lanzamiento)

        campos = [
            ("titulo",           "Título de la canción *", self.cancion.nombre or ""),
            ("fechaLanzamiento", "Fecha de lanzamiento *", fecha_actual),
            ("duracion",         "Duración (segundos) *",
             str(self.cancion.duracion) if self.cancion.duracion is not None else ""),
        ]

        for key, label, valor in campos:
            tk.Label(form, text=label, font=FONT_H3, fg=TEXT_SEC,
                     bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 3))
            e = tk.Entry(form, font=FONT_BODY, bg=BG_CARD, fg=TEXT_SEC,
                         insertbackground=ACCENT2, relief="flat", bd=0)
            e.insert(0, valor)
            e.pack(fill="x", ipady=8, ipadx=10)
            self.entries[key] = e

        # ── Archivo de audio (opcional reemplazar) ─────────────
        tk.Label(form, text="Archivo de audio", font=FONT_H3, fg=TEXT_SEC,
                 bg=BG_DARK, anchor="w").pack(fill="x", pady=(14, 3))

        btn_f = tk.Frame(form, bg=BG_CARD, cursor="hand2")
        btn_f.pack(fill="x")
        btn_lbl = tk.Label(btn_f, text="Cambiar archivo de audio", fg=ACCENT2,
                           bg=BG_CARD, font=FONT_BODY, pady=8)
        btn_lbl.pack(fill="x")
        for w in (btn_f, btn_lbl):
            w.bind("<Button-1>", lambda e: self._seleccionar_archivo())

        actual = self.cancion.ruta_de_archivo or "Sin archivo"
        self.lbl_archivo = tk.Label(form, text=f"Actual: {os.path.basename(actual)}",
                                    font=FONT_TINY, fg=TEXT_MUT, bg=BG_DARK,
                                    wraplength=440, anchor="w")
        self.lbl_archivo.pack(fill="x", pady=4)

        # ── Botones ────────────────────────────────────────────
        btn_row = tk.Frame(root, bg=BG_DARK)
        btn_row.pack(fill="x", pady=20)

        # Guardar
        save_f = tk.Frame(btn_row, bg=ACCENT, cursor="hand2")
        save_f.pack(side="left", expand=True, fill="x", padx=(0, 8))
        save_l = tk.Label(save_f, text="GUARDAR CAMBIOS", fg=BG_DARK, bg=ACCENT,
                          font=("Helvetica", 10, "bold"), pady=10)
        save_l.pack(fill="x")
        for w in (save_f, save_l):
            w.bind("<Button-1>", lambda e: self._guardar())
            w.bind("<Enter>", lambda e: save_f.configure(bg=ACCENT2) or save_l.configure(bg=ACCENT2))
            w.bind("<Leave>", lambda e: save_f.configure(bg=ACCENT) or save_l.configure(bg=ACCENT))

        # Cancelar
        cancel_f = tk.Frame(btn_row, bg=BG_CARD, cursor="hand2")
        cancel_f.pack(side="left", expand=True, fill="x")
        cancel_l = tk.Label(cancel_f, text="Cancelar", fg=TEXT_SEC, bg=BG_CARD,
                            font=FONT_BODY, pady=10)
        cancel_l.pack(fill="x")
        for w in (cancel_f, cancel_l):
            w.bind("<Button-1>", lambda e: self.ventana.destroy())

    # ──────────────────────────────────────────────────────────
    def _seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar canción",
            filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg *.flac")]
        )
        if ruta:
            self.nueva_ruta_audio = ruta
            self.lbl_archivo.config(text=f"Nuevo: {os.path.basename(ruta)}", fg=ACCENT2)

    # ──────────────────────────────────────────────────────────
    def _guardar(self):
        titulo = self.entries["titulo"].get().strip()
        fecha_str = self.entries["fechaLanzamiento"].get().strip()
        duracion_str = self.entries["duracion"].get().strip()

        if not titulo:
            messagebox.showerror("Error", "El título es obligatorio",
                                 parent=self.ventana)
            return

        try:
            duracion = int(duracion_str)
        except ValueError:
            messagebox.showerror("Error", "La duración debe ser un número",
                                 parent=self.ventana)
            return

        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida (usa YYYY-MM-DD)",
                                 parent=self.ventana)
            return

        try:
            # Actualizar campos editables, preservando el resto
            self.cancion.nombre = titulo
            self.cancion.duracion = duracion
            self.cancion.fecha_lanzamiento = fecha_obj

            # Si se eligió un archivo nuevo, copiarlo y actualizar la ruta
            if self.nueva_ruta_audio:
                os.makedirs(CARPETA_AUDIO, exist_ok=True)
                extension = os.path.splitext(self.nueva_ruta_audio)[1]
                nombre_destino = f"{int(self.cancion.id_cancion)}_{titulo.replace(' ', '_')}{extension}"
                ruta_destino = os.path.join(CARPETA_AUDIO, nombre_destino)
                shutil.copy2(self.nueva_ruta_audio, ruta_destino)
                self.cancion.ruta_de_archivo = f"audio/{nombre_destino}"

            if CancionDAO.actualizar_cancion(self.cancion):
                messagebox.showinfo("Éxito", "Canción actualizada",
                                    parent=self.ventana)
                if self.on_guardado:
                    self.on_guardado()
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la canción",
                                     parent=self.ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {e}",
                                 parent=self.ventana)
