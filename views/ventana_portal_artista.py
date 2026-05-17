import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.CancionDAO import CancionDAO
from controller.ArtistaDAO import ArtistaDAO
from controller.AlbumDAO import AlbumDAO

class VentanaPortalArtista:
    """Portal/Dashboard para artistas con estadísticas y gestión de canciones"""
    
    def __init__(self, usuario_actual, app_principal):
        self.usuario_actual = usuario_actual
        self.app = app_principal
        self.ventana = None
    
    def mostrar(self, parent):
        """Mostrar el portal en el frame parent"""
        # Limpiar contenido anterior
        for w in parent.winfo_children():
            w.destroy()
        
        # Header con nombre artista
        header = tk.Frame(parent, bg=BG_DARK)
        header.pack(fill="x", pady=(0, 20))
        
        # Obtener datos del artista
        artista = ArtistaDAO.obtener_artista_por_id(self.usuario_actual.id_persona)
        nombre_artista = f"{self.usuario_actual.nombre}" if artista else self.usuario_actual.nombre
        
        # Banner decorativo
        banner = tk.Canvas(header, width=700, height=100, bg="#1A0A2E", highlightthickness=0)
        banner.pack(fill="x")
        banner.create_text(20, 35, text=f"🎤 {nombre_artista}", anchor="w",
                          font=("Helvetica", 20, "bold"), fill=TEXT_PRI)
        banner.create_text(20, 65, text="Portal de Artista • Gestiona tus canciones y álbumes",
                          anchor="w", font=FONT_SMALL, fill=TEXT_SEC)
        
        # Botones de acción rápida
        actions = tk.Frame(parent, bg=BG_DARK)
        actions.pack(fill="x", pady=(0, 20))
        
        btn_subir = Componentes.btn(actions, "＋ Subir canción", 
                                     lambda: self._abrir_subir_cancion(),
                                     bg=ACCENT, fg="white")
        btn_subir.pack(side="left", padx=(0, 10))
        
        btn_album = Componentes.btn(actions, "💿 Crear álbum", 
                                    lambda: self._abrir_crear_album(),
                                    bg="#1A3A5C", fg=TEXT_PRI)
        btn_album.pack(side="left", padx=(0, 10))
        
        btn_perfil = Componentes.btn(actions, "✎ Editar perfil", 
                                     lambda: self._abrir_editar_perfil(),
                                     bg=BG_CARD, fg=TEXT_SEC)
        btn_perfil.pack(side="left")
        
        # Estadísticas
        self._mostrar_estadisticas(parent)
        
        # Tabla de canciones
        self._mostrar_mis_canciones(parent)
    
    def _mostrar_estadisticas(self, parent):
        """Mostrar estadísticas del artista"""
        stats_titulo = tk.Label(parent, text="Estadísticas", font=FONT_H2,
                               fg=TEXT_PRI, bg=BG_DARK, anchor="w")
        stats_titulo.pack(fill="x", pady=(0, 8))
        
        stats_row = tk.Frame(parent, bg=BG_DARK)
        stats_row.pack(fill="x", pady=(0, 20))
        
        stats_data = [
            ("0", "Oyentes mensuales", ACCENT2),
            ("0", "Reproducciones", GREEN),
            ("0", "Seguidores", "#60A5FA"),
            ("0", "Álbumes", "#F59E0B"),
        ]
        
        for valor, etiqueta, color in stats_data:
            stat_card = tk.Frame(stats_row, bg=BG_CARD, padx=20, pady=14)
            stat_card.pack(side="left", padx=(0, 10))
            
            tk.Label(stat_card, text=valor, font=("Helvetica", 18, "bold"),
                    fg=color, bg=BG_CARD).pack(anchor="w")
            tk.Label(stat_card, text=etiqueta, font=FONT_TINY, 
                    fg=TEXT_MUT, bg=BG_CARD).pack(anchor="w")
    
    def _mostrar_mis_canciones(self, parent):
        """Mostrar tabla de canciones del usuario"""
        titulo = tk.Label(parent, text="Mis canciones", font=FONT_H2,
                         fg=TEXT_PRI, bg=BG_DARK, anchor="w")
        titulo.pack(fill="x", pady=(0, 8))
        
        # Headers
        header = tk.Frame(parent, bg=BG_DARK)
        header.pack(fill="x")
        
        cols = [("#", 3), ("Título", 25), ("Álbum", 18), ("Dur.", 7), ("Estado", 12), ("", 8)]
        for col_name, width in cols:
            tk.Label(header, text=col_name, font=FONT_TINY, fg=TEXT_MUT,
                    bg=BG_DARK, width=width, anchor="w").pack(side="left")
        
        Componentes.divider(parent)
        
        # Obtener canciones del usuario
        canciones = CancionDAO.obtener_canciones_por_artista(self.usuario_actual.id_persona)
        
        if not canciones:
            tk.Label(parent, text="No tienes canciones. ¡Sube tu primera canción!",
                    font=FONT_BODY, fg=TEXT_MUT, bg=BG_DARK).pack(pady=20)
            return
        
        # Estados simulados
        estados = {0: "✔ Publicada", 1: "⏳ Revisión"}
        
        for i, cancion in enumerate(canciones, 1):
            row = tk.Frame(parent, bg=BG_DARK, cursor="hand2")
            row.pack(fill="x", pady=2)
            row.bind("<Enter>", lambda e, r=row: r.configure(bg=BG_HOVER))
            row.bind("<Leave>", lambda e, r=row: r.configure(bg=BG_DARK))
            
            # # (número)
            tk.Label(row, text=str(i), font=FONT_SMALL, fg=TEXT_MUT,
                    bg=BG_DARK, width=3).pack(side="left")
            
            # Canvas icono
            canvas = tk.Canvas(row, width=34, height=34, bg=ACCENT, highlightthickness=0)
            canvas.pack(side="left", padx=(2, 8))
            canvas.create_text(17, 17, text="♫", font=("Helvetica", 11), fill=ACCENT2)
            
            # Título
            tk.Label(row, text=cancion.nombre, font=("Helvetica", 10, "bold"),
                    fg=TEXT_PRI, bg=BG_DARK, width=25, anchor="w").pack(side="left")
            
            # Álbum
            album_nombre = "Sin álbum"
            if cancion.id_album:
                album = AlbumDAO.obtener_album_por_id(cancion.id_album)
                if album:
                    album_nombre = album.nombre
            tk.Label(row, text=album_nombre, font=FONT_BODY, fg=TEXT_SEC,
                    bg=BG_DARK, width=18, anchor="w").pack(side="left")
            
            # Duración
            duracion = f"{int(cancion.duracion//60)}:{int(cancion.duracion%60):02d}" if cancion.duracion else "0:00"
            tk.Label(row, text=duracion, font=FONT_SMALL, fg=TEXT_MUT,
                    bg=BG_DARK, width=7).pack(side="left")
            
            # Estado (simulado)
            estado_texto = estados.get(i % 2, "✔ Publicada")
            color_estado = "#4ADE80" if "✔" in estado_texto else "#F59E0B"
            tk.Label(row, text=estado_texto, font=FONT_TINY, fg=color_estado,
                    bg=BG_DARK, width=12).pack(side="left")
            
            # Acciones
            acciones = tk.Frame(row, bg=BG_DARK)
            acciones.pack(side="left", padx=6)
            
            # Editar
            edit_btn = tk.Label(acciones, text="✎", fg=ACCENT2, bg=BG_DARK,
                               font=FONT_BODY, cursor="hand2")
            edit_btn.pack(side="left", padx=3)
            edit_btn.bind("<Button-1>", lambda e, cid=cancion.id_cancion: 
                         messagebox.showinfo("Editar", f"Editar canción ID {cid}"))
            
            # Eliminar
            delete_btn = tk.Label(acciones, text="🗑", fg="#EF4444", bg=BG_DARK,
                                 font=FONT_BODY, cursor="hand2")
            delete_btn.pack(side="left", padx=3)
            delete_btn.bind("<Button-1>", lambda e, cid=cancion.id_cancion: 
                           self._confirmar_eliminar_cancion(cid))
    
    def _confirmar_eliminar_cancion(self, id_cancion):
        """Confirmar eliminación de canción"""
        if messagebox.askyesno("Confirmar", "¿Eliminar esta canción?"):
            if CancionDAO.eliminar_cancion(id_cancion):
                messagebox.showinfo("Éxito", "Canción eliminada correctamente")
                # Recargar
                self.mostrar(self.app.content)
            else:
                messagebox.showerror("Error", "No se pudo eliminar la canción")
    
    def _abrir_subir_cancion(self):
        """Abrir ventana de subir canción"""
        from views.ventana_subir_cancion import VentanaSubirCancion
        VentanaSubirCancion(self.usuario_actual, self.app)
    
    def _abrir_crear_album(self):
        """Abrir ventana de crear álbum"""
        from views.ventana_crear_album import VentanaCrearAlbum

        def on_creado():
            self.mostrar(self.app.content)

        VentanaCrearAlbum(self.usuario_actual, self.app, on_creado)

    def _abrir_editar_perfil(self):
        """Abrir ventana de editar perfil del artista"""
        from views.ventana_editar_perfil_artista import VentanaEditarPerfilArtista

        def on_guardado():
            self.mostrar(self.app.content)

        VentanaEditarPerfilArtista(self.usuario_actual, self.app, on_guardado)