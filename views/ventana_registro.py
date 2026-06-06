import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.UsuarioDAO import UsuarioDAO
from models.Usuario import Usuario

class VentanaRegistro:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("WavePlay - Registro")
        self.ventana.geometry("450x660")
        self.ventana.configure(bg=BG_DARK)
        self.setup_ui()

    def setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK)
        root.pack(fill="both", expand=True, padx=30, pady=20)

        Componentes.label(root, "Crear cuenta", font=FONT_TITLE,
                         fg=TEXT_PRI, bg=BG_DARK, anchor="center").pack(pady=(0, 16))

        form = tk.Frame(root, bg=BG_DARK)
        form.pack(fill="both", expand=True)

        # Nombre
        Componentes.label(form, "Nombre *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_nombre = Componentes.entry(form, "", width=40)
        self.entry_nombre.pack(fill="x", ipady=6)

        # Apellido Paterno
        Componentes.label(form, "Apellido Paterno *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_ap = Componentes.entry(form, "", width=40)
        self.entry_ap.pack(fill="x", ipady=6)

        # Apellido Materno
        Componentes.label(form, "Apellido Materno", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_am = Componentes.entry(form, "", width=40)
        self.entry_am.pack(fill="x", ipady=6)

        # Fecha de nacimiento
        Componentes.label(form, "Fecha de nacimiento * (YYYY-MM-DD)", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_fecha = Componentes.entry(form, "", width=40)
        self.entry_fecha.pack(fill="x", ipady=6)

        # Teléfono
        Componentes.label(form, "Teléfono", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_telefono = Componentes.entry(form, "", width=40)
        self.entry_telefono.pack(fill="x", ipady=6)

        # Contraseña
        Componentes.label(form, "Contraseña *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_password = Componentes.entry(form, "", show="•", width=40)
        self.entry_password.pack(fill="x", ipady=6)

        # Confirmar contraseña
        Componentes.label(form, "Confirmar contraseña *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_confirmar = Componentes.entry(form, "", show="•", width=40)
        self.entry_confirmar.pack(fill="x", ipady=6)

        # Botones
        Componentes.btn(form, "REGISTRARSE", self._registrar,
                        bg=ACCENT, fg="white",
                        font=("Helvetica", 11, "bold")).pack(fill="x", pady=(20, 6))
        Componentes.btn(form, "← Volver al login", self._volver_login,
                        bg=BG_CARD, fg=ACCENT2).pack(fill="x")

    def _registrar(self):
        nombre   = self.entry_nombre.get().strip()
        ap       = self.entry_ap.get().strip()
        am       = self.entry_am.get().strip()
        fecha    = self.entry_fecha.get().strip()
        telefono = self.entry_telefono.get().strip()
        password = self.entry_password.get()
        confirmar = self.entry_confirmar.get()

        if not all([nombre, ap, fecha, password, confirmar]):
            messagebox.showerror("Error", "Completa los campos obligatorios (*)",
                                 parent=self.ventana)
            return

        if password != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden",
                                 parent=self.ventana)
            return

        if not self._fecha_valida(fecha):
            messagebox.showerror("Error", "Fecha inválida. Usa YYYY-MM-DD",
                                 parent=self.ventana)
            return

        from datetime import datetime
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()

        usuario = Usuario(
            nombre           = nombre,
            apellido_paterno = ap,
            apellido_materno = am or None,
            fecha_nacimiento = fecha_obj,
            telefono         = telefono or None,
            contrasena       = password
        )

        resultado = UsuarioDAO.crear_usuario(usuario)

        if resultado:
            messagebox.showinfo("Éxito", "Cuenta creada exitosamente",
                                parent=self.ventana)
            self._volver_login()
        else:
            messagebox.showerror("Error",
                                 "No se pudo crear la cuenta. Intenta de nuevo.",
                                 parent=self.ventana)

    def _fecha_valida(self, fecha):
        from datetime import datetime
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _volver_login(self):
        self.ventana.destroy()
        from views.ventana_login import VentanaLogin
        VentanaLogin().ejecutar()

    def ejecutar(self):
        self.ventana.mainloop()