import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes

class VentanaEditarPerfilArtista:
    """
    Popup para editar el perfil del artista.
    Usa el patrón Toplevel igual que VentanaSubirCancion.
    
    Requiere en ArtistaDAO:
        ArtistaDAO.obtener_artista_por_id(id_persona) -> objeto/tupla con campos:
            nombre, apellido, es_banda (bool/int), disquera, bio, pais
        ArtistaDAO.actualizar_artista(id_persona, datos_dict) -> bool
    """

    def __init__(self, usuario_actual, app_principal, on_guardado_callback=None):
        self.usuario_actual = usuario_actual
        self.app = app_principal
        self.on_guardado = on_guardado_callback
        self.ventana = tk.Toplevel(app_principal.ventana)
        self.ventana.title("Editar perfil de artista")
        self.ventana.geometry("520x600")
        self.ventana.configure(bg=BG_DARK)
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        self._setup_ui()

    # ──────────────────────────────────────────────────────────
    def _setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK, padx=30, pady=20)
        root.pack(fill="both", expand=True)

        # Título
        tk.Label(root, text="Editar perfil de artista", font=FONT_TITLE,
                 fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x", pady=(0, 20))

        # ── Avatar simulado ────────────────────────────────────
        avatar_row = tk.Frame(root, bg=BG_DARK)
        avatar_row.pack(fill="x", pady=(0, 20))

        av = tk.Canvas(avatar_row, width=80, height=80, bg=ACCENT,
                       highlightthickness=0, cursor="hand2")
        av.pack(side="left")
        av.create_text(40, 40, text="🎤", font=("Helvetica", 32), fill=TEXT_PRI)

        av_info = tk.Frame(avatar_row, bg=BG_DARK)
        av_info.pack(side="left", padx=16)
        tk.Label(av_info, text="Foto de perfil", font=FONT_H3,
                 fg=TEXT_PRI, bg=BG_DARK).pack(anchor="w")
        tk.Label(av_info, text="JPG · PNG · máx 2 MB", font=FONT_TINY,
                 fg=TEXT_MUT, bg=BG_DARK).pack(anchor="w")
        change_btn = tk.Frame(av_info, bg=BG_CARD, cursor="hand2")
        change_btn.pack(anchor="w", pady=6)
        change_lbl = tk.Label(change_btn, text="Cambiar imagen", font=FONT_SMALL,
                              fg=ACCENT2, bg=BG_CARD, padx=10, pady=4)
        change_lbl.pack()
        for w in (change_btn, change_lbl):
            w.bind("<Button-1>", lambda e: messagebox.showinfo(
                "Info", "Selección de imagen — conecta con tkinter.filedialog"))

        Componentes.divider(root)

        # ── Formulario ─────────────────────────────────────────
        form = tk.Frame(root, bg=BG_DARK)
        form.pack(fill="both", expand=True)

        self.entries = {}

        campos = [
            ("nombre",   "Nombre artístico / Nombre *", "Ej: Synthwave Riders"),
            ("apellido", "Apellido (si aplica)",         "Ej: García"),
            ("disquera", "Disquera / Sello",             "Ej: Indie Records"),
        ]

        for key, label, ph in campos:
            tk.Label(form, text=label, font=FONT_H3, fg=TEXT_SEC,
                     bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 3))
            e = tk.Entry(form, font=FONT_BODY, bg=BG_CARD, fg=TEXT_SEC,
                         insertbackground=ACCENT2, relief="flat", bd=0)
            e.insert(0, ph)
            e.pack(fill="x", ipady=8, ipadx=10)
            self.entries[key] = e

        # Tipo (solista / banda)
        tk.Label(form, text="Tipo", font=FONT_H3, fg=TEXT_SEC,
                 bg=BG_DARK, anchor="w").pack(fill="x", pady=(12, 4))
        self.tipo_var = tk.StringVar(value="Solista")
        tipo_row = tk.Frame(form, bg=BG_DARK)
        tipo_row.pack(fill="x")
        for opt in ["Solista", "Banda"]:
            tk.Radiobutton(tipo_row, text=opt, variable=self.tipo_var, value=opt,
                           bg=BG_DARK, fg=TEXT_PRI, selectcolor=BG_DARK,
                           activebackground=BG_DARK, font=FONT_BODY,
                           borderwidth=0, highlightthickness=0).pack(side="left", padx=(0, 20))

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
    def _guardar(self):
        nombre = self.entries["nombre"].get().strip()
        if not nombre or nombre.startswith("Ej:"):
            messagebox.showerror("Error", "El nombre artístico es obligatorio",
                                 parent=self.ventana)
            return

        datos = {
            "nombre":   nombre,
            "apellido": self.entries["apellido"].get().strip(),
            "disquera": self.entries["disquera"].get().strip(),
            "es_banda": 1 if self.tipo_var.get() == "Banda" else 0,
        }

        # ── CONECTAR CON DAO ──────────────────────────────────
        from controller.ArtistaDAO import ArtistaDAO
        try:
            resultado = ArtistaDAO.actualizar_artista(self.usuario_actual.id_persona, datos)
            if resultado:
                messagebox.showinfo("Éxito", "Perfil actualizado", parent=self.ventana)
                if self.on_guardado:
                    self.on_guardado()
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el perfil", 
                                   parent=self.ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {e}", 
                               parent=self.ventana)