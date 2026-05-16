import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.UsuarioDAO import UsuarioDAO

class VentanaLogin:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("WavePlay - Login")
        self.ventana.geometry("420x580")
        self.ventana.configure(bg=BG_DARK)
        self.setup_ui()
    
    def setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK)
        root.pack(fill="both", expand=True)

        # Fondo decorativo con canvas
        c = tk.Canvas(root, width=420, height=580, bg=BG_DARK, highlightthickness=0)
        c.place(x=0, y=0)
        c.create_oval(-60, -60, 200, 200, fill="#1A0A2E", outline="")
        c.create_oval(250, 380, 500, 620, fill="#0A1A2E", outline="")
        c.create_oval(300, -40, 480, 140, fill="#1A102E", outline="")

        # Contenido centrado
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
                         fg=TEXT_SEC, bg=BG_DARK, anchor="center").pack(pady=(2, 24))

        # Campos
        wrap = tk.Frame(frame, bg=BG_CARD, padx=0, pady=0)
        wrap.pack(fill="x", pady=5, ipadx=2, ipady=2)
        inner = tk.Frame(wrap, bg=BG_CARD, padx=14, pady=10)
        inner.pack(fill="x")
        self.entry_correo = Componentes.entry(inner, "Correo electrónico", width=28)
        self.entry_correo.pack(fill="x")
        self.entry_correo.configure(bg=BG_CARD)

        wrap2 = tk.Frame(frame, bg=BG_CARD, padx=0, pady=0)
        wrap2.pack(fill="x", pady=5, ipadx=2, ipady=2)
        inner2 = tk.Frame(wrap2, bg=BG_CARD, padx=14, pady=10)
        inner2.pack(fill="x")
        self.entry_password = Componentes.entry(inner2, "Contraseña", show="•", width=28)
        self.entry_password.pack(fill="x")
        self.entry_password.configure(bg=BG_CARD)

        # Botón login
        btn_login = Componentes.btn(frame, "INICIAR SESIÓN", self.iniciar_sesion,
                                    bg=ACCENT, fg="white", font=("Helvetica", 11, "bold"))
        btn_login.pack(fill="x", pady=(18, 6))

        # Botón registro
        btn_registro = Componentes.btn(frame, "CREAR CUENTA", self._abrir_registro,
                                      bg=BG_CARD, fg=TEXT_SEC, font=FONT_SMALL)
        btn_registro.pack(fill="x", pady=6)
    
    def _abrir_registro(self):
        from views.ventana_registro import VentanaRegistro
        self.ventana.destroy()
        app = VentanaRegistro()
        app.ejecutar()
        
    
    def iniciar_sesion(self):
        correo = self.entry_correo.get()
        password = self.entry_password.get()
        
        if not correo or correo == "Correo electrónico":
            messagebox.showerror("Error", "Ingresa tu correo electrónico")
            return
        
        if not password or password == "Contraseña":
            messagebox.showerror("Error", "Ingresa tu contraseña")
            return
        
        usuario = UsuarioDAO.verificar_credenciales(correo, password)
        
        if usuario:
            messagebox.showinfo("Éxito", f"¡Bienvenido {usuario.nombre}!")
            self.ventana.destroy()
            from views.ventana_principal import VentanaPrincipal
            app = VentanaPrincipal(usuario)
            app.ejecutar()
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos")
    
    def ejecutar(self):
        self.ventana.mainloop()