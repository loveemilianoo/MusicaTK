import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.PlaylistDAO import PlaylistDAO
from models.Playlist import Playlist
from datetime import date

class VentanaCrearPlaylist:
    def __init__(self, usuario_actual, on_creada_callback, parent_ventana):
        self.usuario_actual = usuario_actual
        self.on_creada = on_creada_callback
        self.ventana = tk.Toplevel(parent_ventana)
        self.ventana.title("Crear Playlist")
        self.ventana.geometry("500x550")
        self.ventana.configure(bg=BG_DARK)
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self.ventana, text="Crear nueva playlist", font=FONT_TITLE,
                fg=TEXT_PRI, bg=BG_DARK).pack(pady=20)
        
        form = tk.Frame(self.ventana, bg=BG_DARK)
        form.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Portada
        cover_frame = tk.Frame(form, bg=BG_DARK)
        cover_frame.pack(pady=10)
        
        cover = tk.Canvas(cover_frame, width=150, height=150, bg=BG_CARD, 
                         highlightthickness=2, highlightbackground=ACCENT)
        cover.pack()
        cover.create_text(75, 65, text="♫", font=("Helvetica", 50), fill=ACCENT)
        cover.create_text(75, 115, text="Subir imagen", font=FONT_SMALL, fill=TEXT_MUT)
        
        # Nombre
        Componentes.label(form, "Nombre de la playlist", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(15, 5))
        self.entry_nombre = Componentes.entry(form, "Mi playlist increíble", width=45)
        self.entry_nombre.pack(fill="x", ipady=8)
        
        # Descripción
        Componentes.label(form, "Descripción", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(15, 5))
        self.text_descripcion = tk.Text(form, font=FONT_BODY, bg=BG_CARD, fg=TEXT_PRI,
                                        insertbackground=ACCENT2, relief="flat", bd=0,
                                        height=4, padx=10, pady=8)
        self.text_descripcion.pack(fill="x")
        self.text_descripcion.insert("1.0", "¿De qué trata esta playlist?")
        
        # Visibilidad
        Componentes.label(form, "Visibilidad", font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(15, 5))
        self.visibilidad_var = tk.StringVar(value="Privada")
        vis_frame = tk.Frame(form, bg=BG_DARK)
        vis_frame.pack(fill="x")
        
        for opt in ["Privada", "Pública"]:
            rb = tk.Radiobutton(vis_frame, text=opt, variable=self.visibilidad_var, value=opt,
                               bg=BG_DARK, fg=TEXT_PRI, selectcolor=BG_DARK,
                               activebackground=BG_DARK, font=FONT_BODY)
            rb.pack(side="left", padx=10)
        
        # Botones
        btn_frame = tk.Frame(form, bg=BG_DARK)
        btn_frame.pack(fill="x", pady=20)
        
        btn_guardar = Componentes.btn(btn_frame, "GUARDAR PLAYLIST", self._guardar,
                                      bg=ACCENT, fg="white", font=("Helvetica", 11, "bold"))
        btn_guardar.pack(side="left", fill="x", expand=True, padx=5)
        
        btn_cancelar = Componentes.btn(btn_frame, "Cancelar", self.ventana.destroy,
                                       bg=BG_CARD, fg=TEXT_SEC)
        btn_cancelar.pack(side="left", fill="x", expand=True, padx=5)
    
    def _guardar(self):
        nombre = self.entry_nombre.get()
        
        if not nombre or nombre == "Mi playlist increíble":
            messagebox.showerror("Error", "Ingresa un nombre para la playlist")
            return
        
        playlist = Playlist(
            nombre=nombre,
            id_persona=self.usuario_actual.id_persona,
            fecha_creacion=date.today()
        )
        
        resultado = PlaylistDAO.crear_playlist(playlist)
        
        if resultado:
            messagebox.showinfo("Éxito", "Playlist creada exitosamente")
            self.on_creada()
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear la playlist")