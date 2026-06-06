import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes

class VentanaConvertirArtista:
    """
    Formulario que aparece cuando un Usuario quiere
    convertirse en Artista. Los datos de Persona ya
    vienen cargados y solo se piden Banda y Disquera.
    """

    def __init__(self, persona):
        self.persona = persona
        self.ventana = tk.Tk()
        self.ventana.title("WavePlay — Convertirse en Artista")
        self.ventana.geometry("440x520")
        self.ventana.configure(bg=BG_DARK)
        self.ventana.resizable(False, False)
        self._setup_ui()

    def _setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK, padx=36, pady=24)
        root.pack(fill="both", expand=True)

        # Título
        tk.Label(root, text="🎤  Crear perfil de artista",
                 font=FONT_TITLE, fg=TEXT_PRI, bg=BG_DARK,
                 anchor="w").pack(fill="x", pady=(0, 6))
        tk.Label(root, text="Completa los datos de tu perfil artístico",
                 font=FONT_SMALL, fg=TEXT_SEC, bg=BG_DARK,
                 anchor="w").pack(fill="x", pady=(0, 20))

        # ── Datos de Persona (solo lectura) ───────────────
        info_f = tk.Frame(root, bg=BG_CARD, padx=16, pady=12)
        info_f.pack(fill="x", pady=(0, 20))

        tk.Label(info_f, text="Datos de tu cuenta",
                 font=FONT_H3, fg=TEXT_SEC, bg=BG_CARD).pack(anchor="w")

        nombre_completo = f"{self.persona.nombre} {self.persona.apellido_paterno}"
        if self.persona.apellido_materno:
            nombre_completo += f" {self.persona.apellido_materno}"

        tk.Label(info_f, text=nombre_completo,
                 font=("Helvetica", 11, "bold"), fg=TEXT_PRI,
                 bg=BG_CARD).pack(anchor="w", pady=(6, 0))

        fecha = self.persona.fecha_nacimiento
        fecha_str = fecha.strftime("%d/%m/%Y") if fecha else "—"
        tk.Label(info_f, text=f"Nacimiento: {fecha_str}",
                 font=FONT_TINY, fg=TEXT_MUT, bg=BG_CARD).pack(anchor="w")

        Componentes.divider(root)

        # ── Tipo de artista ────────────────────────────────
        tk.Label(root, text="Tipo de artista",
                 font=FONT_H3, fg=TEXT_SEC, bg=BG_DARK,
                 anchor="w").pack(fill="x", pady=(12, 6))

        self.banda_var = tk.StringVar(value="0")
        tipo_row = tk.Frame(root, bg=BG_DARK)
        tipo_row.pack(fill="x")
        for texto, val in [("Solista", "0"), ("Banda", "1")]:
            tk.Radiobutton(tipo_row, text=texto, variable=self.banda_var,
                          value=val, bg=BG_DARK, fg=TEXT_PRI,
                          selectcolor=BG_DARK, activebackground=BG_DARK,
                          font=FONT_BODY, borderwidth=0,
                          highlightthickness=0).pack(side="left", padx=(0, 20))

        # ── Disquera ───────────────────────────────────────
        tk.Label(root, text="Disquera / Sello (opcional)",
                 font=FONT_H3, fg=TEXT_SEC, bg=BG_DARK,
                 anchor="w").pack(fill="x", pady=(16, 4))
        self.entry_disquera = tk.Entry(root, font=FONT_BODY, bg=BG_CARD,
                                       fg=TEXT_PRI, insertbackground=ACCENT2,
                                       relief="flat", bd=0)
        self.entry_disquera.pack(fill="x", ipady=8, ipadx=10)

        # ── Botones ────────────────────────────────────────
        btn_row = tk.Frame(root, bg=BG_DARK)
        btn_row.pack(fill="x", pady=(28, 0))

        # Confirmar
        ok_f = tk.Frame(btn_row, bg=ACCENT, cursor="hand2")
        ok_f.pack(side="left", expand=True, fill="x", padx=(0, 8))
        ok_l = tk.Label(ok_f, text="CONFIRMAR Y ENTRAR",
                        fg="white", bg=ACCENT,
                        font=("Helvetica", 10, "bold"), pady=10)
        ok_l.pack(fill="x")
        for w in (ok_f, ok_l):
            w.bind("<Button-1>", lambda e: self._confirmar())
            w.bind("<Enter>", lambda e: ok_f.configure(bg=ACCENT2) or ok_l.configure(bg=ACCENT2))
            w.bind("<Leave>", lambda e: ok_f.configure(bg=ACCENT) or ok_l.configure(bg=ACCENT))

        # Cancelar
        can_f = tk.Frame(btn_row, bg=BG_CARD, cursor="hand2")
        can_f.pack(side="left", expand=True, fill="x")
        can_l = tk.Label(can_f, text="Cancelar", fg=TEXT_SEC,
                         bg=BG_CARD, font=FONT_BODY, pady=10)
        can_l.pack(fill="x")
        for w in (can_f, can_l):
            w.bind("<Button-1>", lambda e: self._cancelar())

    # ──────────────────────────────────────────────────────
    def _confirmar(self):
        banda    = int(self.banda_var.get())
        disquera = self.entry_disquera.get().strip() or None

        from controller.ArtistaDAO import ArtistaDAO
        ok = ArtistaDAO.convertir_usuario_a_artista(
            self.persona.id_persona, banda, disquera
        )

        if ok:
            # Recargar como objeto Artista completo
            artista = ArtistaDAO.obtener_artista_por_id(self.persona.id_persona)
            messagebox.showinfo(
                "¡Listo!",
                f"Ya eres artista, {artista.nombre}.\n"
                "Ahora puedes subir música desde tu portal.",
                parent=self.ventana
            )
            self.ventana.destroy()
            from views.ventana_principal import VentanaPrincipal
            VentanaPrincipal(artista).ejecutar()
        else:
            messagebox.showerror(
                "Error",
                "No se pudo crear el perfil de artista.\n"
                "Intenta de nuevo.",
                parent=self.ventana
            )

    def _cancelar(self):
        self.ventana.destroy()
        from views.ventana_seleccion_rol import VentanaSeleccionRol
        VentanaSeleccionRol(self.persona).ejecutar()

    def ejecutar(self):
        self.ventana.mainloop()