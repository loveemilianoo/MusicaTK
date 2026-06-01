import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.ArtistaDAO import ArtistaDAO
from models.Artista import Artista

class VentanaRegistroArtista:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("WavePlay - Registro de Artista")
        self.ventana.geometry("450x680")
        self.ventana.configure(bg=BG_DARK)
        self.setup_ui()

    def setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK)
        root.pack(fill="both", expand=True, padx=30, pady=20)

        # Encabezado
        Componentes.label(root, "Registro de artista", font=FONT_TITLE,
                         fg=TEXT_PRI, bg=BG_DARK, anchor="center").pack(pady=(0, 4))
        Componentes.label(root, "Crea tu perfil para subir música", font=FONT_SMALL,
                         fg=TEXT_SEC, bg=BG_DARK, anchor="center").pack(pady=(0, 16))

        form = tk.Frame(root, bg=BG_DARK)
        form.pack(fill="both", expand=True)

        # ── Campos personales ──────────────────────────────
        Componentes.label(form, "Nombre artístico / Nombre *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_nombre = Componentes.entry(form, "", width=40)
        self.entry_nombre.pack(fill="x", ipady=6)

        Componentes.label(form, "Apellido", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_apellido = Componentes.entry(form, "", width=40)
        self.entry_apellido.pack(fill="x", ipady=6)

        Componentes.label(form, "Correo electrónico *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_correo = Componentes.entry(form, "", width=40)
        self.entry_correo.pack(fill="x", ipady=6)

        Componentes.label(form, "Contraseña *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_password = Componentes.entry(form, "", show="•", width=40)
        self.entry_password.pack(fill="x", ipady=6)

        Componentes.label(form, "Confirmar contraseña *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_confirmar = Componentes.entry(form, "", show="•", width=40)
        self.entry_confirmar.pack(fill="x", ipady=6)

        # Sexo
        Componentes.label(form, "Sexo", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        sexo_frame = tk.Frame(form, bg=BG_DARK)
        sexo_frame.pack(fill="x")
        self.sexo_var = tk.StringVar(value="M")
        for texto, valor in [("Masculino", "M"), ("Femenino", "F"), ("Otro", "O")]:
            tk.Radiobutton(sexo_frame, text=texto, variable=self.sexo_var, value=valor,
                          bg=BG_DARK, fg=TEXT_PRI, selectcolor=BG_DARK,
                          activebackground=BG_DARK, font=FONT_BODY).pack(side="left", padx=8)

        Componentes.label(form, "Edad *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_edad = Componentes.entry(form, "", width=20)
        self.entry_edad.pack(anchor="w", ipady=6)

        # ── Campos exclusivos de artista ───────────────────
        Componentes.divider(form)

        Componentes.label(form, "Tipo de artista", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 4))
        tipo_frame = tk.Frame(form, bg=BG_DARK)
        tipo_frame.pack(fill="x")
        self.banda_var = tk.StringVar(value="0")
        tk.Radiobutton(tipo_frame, text="Solista", variable=self.banda_var, value="0",
                      bg=BG_DARK, fg=TEXT_PRI, selectcolor=BG_DARK,
                      activebackground=BG_DARK, font=FONT_BODY).pack(side="left", padx=8)
        tk.Radiobutton(tipo_frame, text="Banda", variable=self.banda_var, value="1",
                      bg=BG_DARK, fg=TEXT_PRI, selectcolor=BG_DARK,
                      activebackground=BG_DARK, font=FONT_BODY).pack(side="left", padx=8)

        Componentes.label(form, "Disquera / Sello (opcional)", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_disquera = Componentes.entry(form, "", width=40)
        self.entry_disquera.pack(fill="x", ipady=6)

        # ── Botones ────────────────────────────────────────
        btn_registrar = Componentes.btn(form, "CREAR CUENTA DE ARTISTA", self._registrar,
                                        bg=ACCENT, fg="white",
                                        font=("Helvetica", 11, "bold"))
        btn_registrar.pack(fill="x", pady=(20, 6))

        btn_volver = Componentes.btn(form, "← Volver al login", self._volver_login,
                                     bg=BG_CARD, fg=ACCENT2)
        btn_volver.pack(fill="x")

    # ──────────────────────────────────────────────────────
    def _registrar(self):
        nombre   = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        correo   = self.entry_correo.get().strip()
        password = self.entry_password.get()
        confirmar = self.entry_confirmar.get()
        edad_str  = self.entry_edad.get().strip()
        disquera  = self.entry_disquera.get().strip()
        es_banda  = int(self.banda_var.get())

        # Validaciones
        if not all([nombre, correo, password, confirmar, edad_str]):
            messagebox.showerror("Error", "Completa los campos obligatorios (*)",
                                 parent=self.ventana)
            return

        if password != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden",
                                 parent=self.ventana)
            return

        try:
            edad_int = int(edad_str)
            if edad_int <= 0 or edad_int > 120:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Edad inválida", parent=self.ventana)
            return

        # Crear objeto Artista y guardar
        artista = Artista(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            sexo=self.sexo_var.get(),
            edad=edad_int,
            banda=es_banda,
            disquera=disquera if disquera else None,
            contrasena=password
        )

        resultado = ArtistaDAO.crear_artista(artista)

        if resultado:
            messagebox.showinfo("Éxito",
                                f"Cuenta de artista creada.\n¡Bienvenido {nombre}!",
                                parent=self.ventana)
            self._volver_login()
        else:
            messagebox.showerror("Error",
                                 "No se pudo crear la cuenta.\nEl correo puede estar en uso.",
                                 parent=self.ventana)

    def _volver_login(self):
        self.ventana.destroy()
        from views.ventana_login import VentanaLogin
        login = VentanaLogin()
        login.ejecutar()

    def ejecutar(self):
        self.ventana.mainloop()