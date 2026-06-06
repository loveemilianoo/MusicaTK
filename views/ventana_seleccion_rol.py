import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes

class VentanaSeleccionRol:
    """
    Ventana intermedia entre el login y el home.
    El usuario ya fue identificado en Persona; aquí elige
    si entra como Usuario o como Artista.
    """

    def __init__(self, persona):
        self.persona = persona   # objeto Persona con id, nombre, apellidos, fecha
        self.ventana = tk.Tk()
        self.ventana.title("WavePlay — ¿Cómo deseas entrar?")
        self.ventana.geometry("420x500")
        self.ventana.configure(bg=BG_DARK)
        self.ventana.resizable(False, False)
        self._setup_ui()

    def _setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK)
        root.pack(fill="both", expand=True, padx=40, pady=30)

        # Logo pequeño
        logo = tk.Canvas(root, width=48, height=48, bg=BG_DARK, highlightthickness=0)
        logo.pack()
        logo.create_oval(2, 2, 46, 46, fill=ACCENT, outline="")
        logo.create_oval(12, 12, 36, 36, fill=BG_DARK, outline="")
        logo.create_oval(18, 18, 30, 30, fill=ACCENT2, outline="")

        # Saludo
        tk.Label(root, text=f"¡Hola, {self.persona.nombre}!",
                 font=("Helvetica", 20, "bold"), fg=TEXT_PRI,
                 bg=BG_DARK, anchor="center").pack(pady=(12, 4))
        tk.Label(root, text="¿Cómo deseas iniciar sesión?",
                 font=FONT_BODY, fg=TEXT_SEC,
                 bg=BG_DARK, anchor="center").pack(pady=(0, 30))

        # ── Botón Usuario ──────────────────────────────────
        usr_f = tk.Frame(root, bg=BG_CARD, cursor="hand2")
        usr_f.pack(fill="x", pady=(0, 12), ipady=4)

        tk.Label(usr_f, text="🎧", font=("Helvetica", 24),
                 fg=ACCENT2, bg=BG_CARD).pack(pady=(14, 4))
        tk.Label(usr_f, text="Entrar como Usuario",
                 font=("Helvetica", 12, "bold"), fg=TEXT_PRI,
                 bg=BG_CARD).pack()
        tk.Label(usr_f, text="Escucha y gestiona tus playlists",
                 font=FONT_TINY, fg=TEXT_MUT, bg=BG_CARD).pack(pady=(2, 14))

        for w in usr_f.winfo_children() + [usr_f]:
            w.bind("<Button-1>", lambda e: self._entrar_como_usuario())
        usr_f.bind("<Enter>", lambda e: usr_f.configure(bg=BG_HOVER))
        usr_f.bind("<Leave>", lambda e: usr_f.configure(bg=BG_CARD))

        # ── Botón Artista ──────────────────────────────────
        art_f = tk.Frame(root, bg=BG_CARD, cursor="hand2")
        art_f.pack(fill="x", ipady=4)

        tk.Label(art_f, text="🎤", font=("Helvetica", 24),
                 fg=ACCENT, bg=BG_CARD).pack(pady=(14, 4))
        tk.Label(art_f, text="Entrar como Artista",
                 font=("Helvetica", 12, "bold"), fg=TEXT_PRI,
                 bg=BG_CARD).pack()
        tk.Label(art_f, text="Sube música y gestiona tu portal",
                 font=FONT_TINY, fg=TEXT_MUT, bg=BG_CARD).pack(pady=(2, 14))

        for w in art_f.winfo_children() + [art_f]:
            w.bind("<Button-1>", lambda e: self._entrar_como_artista())
        art_f.bind("<Enter>", lambda e: art_f.configure(bg=BG_HOVER))
        art_f.bind("<Leave>", lambda e: art_f.configure(bg=BG_CARD))

        # ── Volver ─────────────────────────────────────────
        btn_volver = Componentes.btn(root, "← Volver", self._volver,
                                     bg=BG_DARK, fg=TEXT_MUT, font=FONT_SMALL)
        btn_volver.pack(pady=(20, 0))

    # ──────────────────────────────────────────────────────
    def _entrar_como_usuario(self):
        from controller.UsuarioDAO import UsuarioDAO
        usuario = UsuarioDAO.obtener_usuario_por_id(self.persona.id_persona)

        if usuario:
            self._abrir_principal(usuario)
        else:
            messagebox.showerror(
                "Sin cuenta de usuario",
                "Esta persona no tiene cuenta de usuario registrada.\n"
                "Crea una cuenta primero.",
                parent=self.ventana
            )

    def _entrar_como_artista(self):
        from controller.ArtistaDAO import ArtistaDAO
        artista = ArtistaDAO.obtener_artista_por_id(self.persona.id_persona)

        if artista:
            self._abrir_principal(artista)
        else:
            # No es artista — preguntar si quiere convertirse
            respuesta = messagebox.askyesno(
                "No eres artista",
                f"{self.persona.nombre}, no tienes perfil de artista.\n\n"
                "¿Deseas convertirte en artista ahora?\n"
                "Podrás subir música y gestionar tu portal.",
                parent=self.ventana
            )
            if respuesta:
                self._convertir_a_artista()

    def _convertir_a_artista(self):
        """Abre el formulario de conversión con los datos de Persona ya cargados."""
        self.ventana.destroy()
        from views.ventana_convertir_artista import VentanaConvertirArtista
        VentanaConvertirArtista(self.persona).ejecutar()

    def _abrir_principal(self, sesion):
        self.ventana.destroy()
        from views.ventana_principal import VentanaPrincipal
        VentanaPrincipal(sesion).ejecutar()

    def _volver(self):
        self.ventana.destroy()
        from views.ventana_login import VentanaLogin
        VentanaLogin().ejecutar()

    def ejecutar(self):
        self.ventana.mainloop()