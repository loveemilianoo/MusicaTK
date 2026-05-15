import tkinter as tk
from tkinter import ttk, messagebox
from views.colores import *
from views.componentes import Componentes
from controller.UsuarioDAO import UsuarioDAO
from models.Usuario import Usuario

class VentanaRegistro:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("WavePlay - Registro")
        self.ventana.geometry("450x650")
        self.ventana.configure(bg=BG_DARK)
        self.setup_ui()
    
    def setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK)
        root.pack(fill="both", expand=True, padx=30, pady=20)
        
        Componentes.label(root, "Crear cuenta", font=FONT_TITLE,
                         fg=TEXT_PRI, bg=BG_DARK, anchor="center").pack(pady=(0, 20))
        
        # Formulario
        form = tk.Frame(root, bg=BG_DARK)
        form.pack(fill="both", expand=True)
        
        # Nombre
        Componentes.label(form, "Nombre", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(10, 2))
        self.entry_nombre = Componentes.entry(form, "", width=40)
        self.entry_nombre.pack(fill="x", ipady=6)
        
        # Apellido
        Componentes.label(form, "Apellido", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(10, 2))
        self.entry_apellido = Componentes.entry(form, "", width=40)
        self.entry_apellido.pack(fill="x", ipady=6)
        
        # Correo
        Componentes.label(form, "Correo electrónico", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(10, 2))
        self.entry_correo = Componentes.entry(form, "", width=40)
        self.entry_correo.pack(fill="x", ipady=6)
        
        # Teléfono
        Componentes.label(form, "Teléfono", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(10, 2))
        self.entry_telefono = Componentes.entry(form, "", width=40)
        self.entry_telefono.pack(fill="x", ipady=6)
        
        # Contraseña
        Componentes.label(form, "Contraseña", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(10, 2))
        self.entry_password = Componentes.entry(form, "", show="•", width=40)
        self.entry_password.pack(fill="x", ipady=6)
        
        # Confirmar contraseña
        Componentes.label(form, "Confirmar contraseña", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(10, 2))
        self.entry_confirmar = Componentes.entry(form, "", show="•", width=40)
        self.entry_confirmar.pack(fill="x", ipady=6)
        
        # Sexo
        Componentes.label(form, "Sexo", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(10, 2))
        sexo_frame = tk.Frame(form, bg=BG_DARK)
        sexo_frame.pack(fill="x")
        self.sexo_var = tk.StringVar(value="M")
        for texto, valor in [("Masculino", "M"), ("Femenino", "F"), ("Otro", "O")]:
            rb = tk.Radiobutton(sexo_frame, text=texto, variable=self.sexo_var, value=valor,
                               bg=BG_DARK, fg=TEXT_PRI, selectcolor=BG_DARK,
                               activebackground=BG_DARK, font=FONT_BODY)
            rb.pack(side="left", padx=10)
        
        # Edad
        Componentes.label(form, "Edad", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(10, 2))
        self.entry_edad = Componentes.entry(form, "", width=20)
        self.entry_edad.pack(anchor="w", ipady=6)
        
        # Membresía
        Componentes.label(form, "Membresía", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(10, 2))
        self.membresia_var = tk.StringVar(value="Free")
        combo = ttk.Combobox(form, textvariable=self.membresia_var,
                            values=["Free", "Premium", "Family"],
                            state="readonly", font=FONT_BODY)
        combo.pack(anchor="w", ipady=4)
        
        # Botones
        btn_registrar = Componentes.btn(form, "REGISTRARSE", self.registrar,
                                        bg=ACCENT, fg="white", font=("Helvetica", 11, "bold"))
        btn_registrar.pack(fill="x", pady=20)
        
        btn_volver = Componentes.btn(form, "← Volver al login", self.volver_login,
                                     bg=BG_CARD, fg=ACCENT2)
        btn_volver.pack(fill="x")
    
    def registrar(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        correo = self.entry_correo.get()
        telefono = self.entry_telefono.get()
        password = self.entry_password.get()
        confirmar = self.entry_confirmar.get()
        edad = self.entry_edad.get()
        
        if not all([nombre, apellido, correo, telefono, password, edad]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if password != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        try:
            edad_int = int(edad)
            if edad_int <= 0 or edad_int > 120:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Edad inválida")
            return
        
        # Crear usuario usando el controlador
        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            sexo=self.sexo_var.get(),
            edad=edad_int,
            telefono=telefono,
            membresia=self.membresia_var.get(),
            contrasena=password
        )
        
        resultado = UsuarioDAO.crear_usuario(usuario)
        
        if resultado:
            messagebox.showinfo("Éxito", "Cuenta creada exitosamente")
            self.volver_login()
        else:
            messagebox.showerror("Error", "El correo ya está registrado")
    
    def volver_login(self):
        self.ventana.destroy()
        from views.ventana_login import VentanaLogin
        login = VentanaLogin()
        login.ejecutar()
    
    def ejecutar(self):
        self.ventana.mainloop()