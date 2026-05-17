import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.CancionDAO import CancionDAO
from controller.AlbumDAO import AlbumDAO
from models.Cancion import Cancion

class VentanaSubirCancion:
    """Ventana para subir una nueva canción"""
    
    def __init__(self, usuario_actual, app_principal):
        self.usuario_actual = usuario_actual
        self.app = app_principal
        self.ventana = tk.Toplevel(app_principal.ventana)
        self.ventana.title("Subir nueva canción")
        self.ventana.geometry("800x700")
        self.ventana.configure(bg=BG_DARK)
        self.ventana.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Crear la interfaz de usuario"""
        root = tk.Frame(self.ventana, bg=BG_DARK, padx=28, pady=20)
        root.pack(fill="both", expand=True)
        
        # Botón volver
        back = tk.Frame(root, bg=BG_DARK, cursor="hand2")
        back.pack(anchor="w", pady=(0, 20))
        back_lbl = tk.Label(back, text="← Volver", font=FONT_BODY, fg=ACCENT2, bg=BG_DARK)
        back_lbl.pack()
        for w in (back, back_lbl):
            w.bind("<Button-1>", lambda e: self.ventana.destroy())
        
        # Título
        tk.Label(root, text="Subir nueva canción", font=FONT_TITLE,
                fg=TEXT_PRI, bg=BG_DARK, anchor="w").pack(fill="x", pady=(0, 20))
        
        # Body
        body = tk.Frame(root, bg=BG_DARK)
        body.pack(fill="both", expand=True)
        
        # Izquierda - zona de subida
        left = tk.Frame(body, bg=BG_DARK)
        left.pack(side="left", padx=(0, 30))
        
        # Canvas drop zone
        drop_zone = tk.Canvas(left, width=180, height=180, bg=BG_CARD,
                            highlightthickness=2, highlightbackground=ACCENT, cursor="hand2")
        drop_zone.pack()
        drop_zone.create_text(90, 60, text="🎵", font=("Helvetica", 48), fill=ACCENT)
        drop_zone.create_text(90, 110, text="Arrastra archivo", font=FONT_H3, fill=TEXT_SEC)
        drop_zone.create_text(90, 135, text="MP3, WAV, FLAC", font=FONT_TINY, fill=TEXT_MUT)
        
        # Botón examinar
        btn_f = tk.Frame(left, bg=ACCENT, cursor="hand2")
        btn_f.pack(fill="x", pady=12)
        btn_lbl = tk.Label(btn_f, text="Examinar archivo", fg="white", bg=ACCENT, 
                          font=FONT_BODY, pady=8)
        btn_lbl.pack(fill="x")
        
        # Progreso
        tk.Label(left, text="Progreso", font=FONT_TINY, fg=TEXT_MUT, bg=BG_DARK).pack(anchor="w", pady=(8, 2))
        prog_bg = tk.Frame(left, bg=BG_HOVER, height=6, width=180)
        prog_bg.pack(anchor="w")
        prog_fill = tk.Frame(prog_bg, bg=ACCENT2, height=6, width=90)
        prog_fill.place(x=0, y=0)
        
        # Derecha - metadatos
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)
        
        # Campos del formulario
        self.entries = {}
        campos = [
            ("titulo", "Título de la canción *", "Mi Canción"),
            ("artista", "Artista *", "Mi Nombre"),
            ("fechaLanzamiento", "Fecha de lanzamiento *", "2026-12-01"),
            ("genero", "Género", "Electrónica"),
        ]
        
        for key, label, placeholder in campos:
            tk.Label(right, text=label, font=FONT_H3, fg=TEXT_SEC,
                    bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 3))
            
            entry = tk.Entry(right, font=FONT_BODY, bg=BG_CARD, fg=TEXT_SEC,
                           insertbackground=ACCENT2, relief="flat", bd=0)
            entry.insert(0, placeholder)
            entry.pack(fill="x", ipady=8, ipadx=10)
            self.entries[key] = entry
        
        # Duracion
        tk.Label(right, text="Duración (segundos) *", font=FONT_H3, fg=TEXT_SEC,
                bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 3))
        self.entries["duracion"] = tk.Entry(right, font=FONT_BODY, bg=BG_CARD, fg=TEXT_SEC,
                                           insertbackground=ACCENT2, relief="flat", bd=0)
        self.entries["duracion"].insert(0, "180")
        self.entries["duracion"].pack(fill="x", ipady=8, ipadx=10)
        
        # Visibilidad
        tk.Label(right, text="Visibilidad", font=FONT_H3, fg=TEXT_SEC,
                bg=BG_DARK, anchor="w").pack(fill="x", pady=(10, 4))
        
        self.visibilidad = tk.StringVar(value="Pública")
        vis_row = tk.Frame(right, bg=BG_DARK)
        vis_row.pack(fill="x")
        for opt in ["Pública", "Privada"]:
            tk.Radiobutton(vis_row, text=opt, variable=self.visibilidad, value=opt,
                          bg=BG_DARK, fg=TEXT_PRI, selectcolor=BG_CARD,
                          activebackground=BG_DARK, font=FONT_SMALL,
                          borderwidth=0, highlightthickness=0).pack(side="left", padx=(0, 14))
        
        # Botón publicar
        pub_f = tk.Frame(right, bg=GREEN, cursor="hand2")
        pub_f.pack(fill="x", pady=(20, 0), ipadx=14, ipady=10)
        pub_lbl = tk.Label(pub_f, text="PUBLICAR CANCIÓN", fg=BG_DARK, bg=GREEN,
                         font=("Helvetica", 11, "bold"))
        pub_lbl.pack(fill="x")
        
        for w in (pub_f, pub_lbl):
            w.bind("<Button-1>", lambda e: self._publicar_cancion())
            w.bind("<Enter>", lambda e: pub_f.configure(bg="#22C55E") or pub_lbl.configure(bg="#22C55E"))
            w.bind("<Leave>", lambda e: pub_f.configure(bg=GREEN) or pub_lbl.configure(bg=GREEN))
    
    def _publicar_cancion(self):
        """Publicar la canción en la BD"""
        # Validar campos obligatorios
        titulo = self.entries["titulo"].get()
        duracion_str = self.entries["duracion"].get()
        fechaLanzamiento = self.entries["fechaLanzamiento"].get().strip()
        
        if not titulo or titulo == "Mi Canción":
            messagebox.showerror("Error", "Debes ingresar un título")
            return
        
        try:
            duracion = int(duracion_str)
        except ValueError:
            messagebox.showerror("Error", "La duración debe ser un número")
            return
        
        if not fechaLanzamiento or not self._es_fecha_valida(fechaLanzamiento):
            messagebox.showerror("Error", "La fecha de lanzamiento debe ser válida (YYYY-MM-DD)")
            return
        
        try:
            from datetime import datetime
            fecha_obj = datetime.strptime(fechaLanzamiento, "%Y-%m-%d").date()
            
            # Crear objeto Cancion
            cancion = Cancion(
                nombre=titulo,
                duracion=duracion,
                id_artista=self.usuario_actual.id_persona,
                fecha_lanzamiento=fecha_obj
            )
            
            # Intentar guardar
            resultado = CancionDAO.crear_cancion(cancion)
            
            if resultado:
                messagebox.showinfo("Éxito", f"¡Canción publicada correctamente!\nID: {resultado}", parent=self.ventana)
                self.ventana.destroy()
                # Recargar el portal
                if hasattr(self.app, 'mostrar_portal_artista'):
                    self.app.mostrar_portal_artista()
            else:
                messagebox.showerror("Error", "No se pudo guardar la canción", parent=self.ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Error al publicar: {e}", parent=self.ventana)
    
    def _es_fecha_valida(self, fecha_str):
        """Valida si la fecha está en formato YYYY-MM-DD."""
        from datetime import datetime
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
