import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.UsuarioDAO import UsuarioDAO

class VentanaLogin:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("WavePlay - Login")
        self.ventana.geometry("420x620")
        self.ventana.configure(bg=BG_DARK)
        self.setup_ui()

    def setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK)
        root.pack(fill="both", expand=True)

        # Fondo decorativo
        c = tk.Canvas(root, width=420, height=620, bg=BG_DARK, highlightthickness=0)
        c.place(x=0, y=0)
        c.create_oval(-60, -60, 200, 200, fill="#1A0A2E", outline="")
        c.create_oval(250, 400, 500, 650, fill="#0A1A2E", outline="")
        c.create_oval(300, -40, 480, 140, fill="#1A102E", outline="")

        frame = tk.Frame(root, bg=BG_DARK)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        logo_c = tk.Canvas(frame, width=64, height=64, bg=BG_DARK, highlightthickness=0)
        logo_c.pack(pady=(0, 8))
        logo_c.create_oval(4, 4, 60, 60, fill=ACCENT, outline="")
        logo_c.create_oval(16, 16, 48, 48, fill=BG_DARK, outline="")
        logo_c.create_oval(24, 24, 40, 40, fill=ACCENT2, outline="")

        Componentes.label(frame, "WavePlay", font=("Helvetica", 28, "bold"),
                         fg=TEXT_PRI, bg=BG_DARK, anchor="center").pack()
        Componentes.label(frame, "Tu música, sin límites", font=FONT_SMALL,
                         fg=TEXT_SEC, bg=BG_DARK, anchor="center").pack(pady=(2, 20))

        # ── Campo Nombre ───────────────────────────────────
        def campo(placeholder):
            wrap = tk.Frame(frame, bg=BG_CARD)
            wrap.pack(fill="x", pady=4)
            inner = tk.Frame(wrap, bg=BG_CARD, padx=14, pady=8)
            inner.pack(fill="x")
            e = Componentes.entry(inner, placeholder, width=28)
            e.pack(fill="x")
            e.configure(bg=BG_CARD)
            return e

        self.entry_nombre    = campo("Nombre")
        self.entry_ap        = campo("Apellido Paterno")
        self.entry_am        = campo("Apellido Materno (opcional)")
        self.entry_fecha     = campo("Fecha de nacimiento  YYYY-MM-DD")

        # ── Botón continuar ────────────────────────────────
        btn_continuar = Componentes.btn(
            frame, "CONTINUAR", self._continuar,
            bg=ACCENT, fg="white", font=("Helvetica", 11, "bold"))
        btn_continuar.pack(fill="x", pady=(16, 6))

        # ── Botones de registro ────────────────────────────
        btn_reg = Componentes.btn(
            frame, "CREAR CUENTA", self._abrir_registro_usuario,
            bg=BG_CARD, fg=TEXT_SEC, font=FONT_SMALL)
        btn_reg.pack(fill="x", pady=4)

        btn_art = Componentes.btn(
            frame, "🎤  SOY ARTISTA — CREAR CUENTA", self._abrir_registro_artista,
            bg=BG_DARK, fg=ACCENT, font=("Helvetica", 10, "bold"))
        btn_art.pack(fill="x", pady=(0, 4))

    # ──────────────────────────────────────────────────────
    def _continuar(self):
        nombre = self.entry_nombre.get().strip()
        ap     = self.entry_ap.get().strip()
        am     = self.entry_am.get().strip()
        fecha  = self.entry_fecha.get().strip()

        # Limpiar placeholder del apellido materno
        if am == "Apellido Materno (opcional)":
            am = ""
        if fecha == "Fecha de nacimiento  YYYY-MM-DD":
            fecha = ""

        if not nombre or nombre == "Nombre":
            messagebox.showerror("Error", "Ingresa tu nombre", parent=self.ventana)
            return
        if not ap or ap == "Apellido Paterno":
            messagebox.showerror("Error", "Ingresa tu apellido paterno", parent=self.ventana)
            return
        if not fecha:
            messagebox.showerror("Error", "Ingresa tu fecha de nacimiento", parent=self.ventana)
            return

        # Validar formato de fecha
        if not self._fecha_valida(fecha):
            messagebox.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD",
                                 parent=self.ventana)
            return

        # Buscar en Persona
        persona = UsuarioDAO.buscar_persona(nombre, ap, am, fecha)

        if not persona:
            messagebox.showerror("Error",
                                 "No encontramos ninguna cuenta con esos datos.\n"
                                 "Verifica la información o crea una cuenta nueva.",
                                 parent=self.ventana)
            return

        # Ir a selección de rol
        self.ventana.destroy()
        from views.ventana_seleccion_rol import VentanaSeleccionRol
        VentanaSeleccionRol(persona).ejecutar()

    def _fecha_valida(self, fecha):
        from datetime import datetime
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _abrir_registro_usuario(self):
        self.ventana.destroy()
        from views.ventana_registro import VentanaRegistro
        VentanaRegistro().ejecutar()

    def _abrir_registro_artista(self):
        self.ventana.destroy()
        from views.ventana_registro_artista import VentanaRegistroArtista
        VentanaRegistroArtista().ejecutar()

    def ejecutar(self):
        self.ventana.mainloop()