import tkinter as tk
from tkinter import ttk, messagebox
from models.Playlist import Playlist

class VentanaPlaylists:
    def __init__(self, usuario_actual):
        self.usuario_actual = usuario_actual
        self.ventana = tk.Toplevel()
        self.ventana.title("Mis Playlists")
        self.ventana.geometry("800x600")
        self.ventana.configure(bg='#1a1a2e')
        self.playlist_actual = None
        self.setup_ui()
    
    def setup_ui(self):
        # Frame izquierdo - lista de playlists
        frame_izquierdo = tk.Frame(self.ventana, bg='#16213e', width=250)
        frame_izquierdo.pack(side='left', fill='y', padx=5, pady=5)
        
        lbl_playlists = tk.Label(frame_izquierdo, text="📋 Mis Playlists",
                                font=('Arial', 14, 'bold'),
                                fg='#e94560', bg='#16213e')
        lbl_playlists.pack(pady=10)
        
        self.lista_playlists = tk.Listbox(frame_izquierdo, font=('Arial', 11),
                                          bg='#1a1a2e', fg='white',
                                          selectbackground='#e94560',
                                          height=20)
        self.lista_playlists.pack(fill='both', expand=True, padx=10, pady=5)
        self.lista_playlists.bind('<<ListboxSelect>>', self.mostrar_canciones)
        
        btn_nueva = tk.Button(frame_izquierdo, text="+ Nueva Playlist",
                             command=self.crear_playlist,
                             bg='#28a745', fg='white',
                             font=('Arial', 11, 'bold'))
        btn_nueva.pack(pady=10, padx=10, fill='x')
        
        # Frame derecho - canciones de la playlist
        frame_derecho = tk.Frame(self.ventana, bg='#0f3460')
        frame_derecho.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        lbl_canciones = tk.Label(frame_derecho, text="🎵 Canciones",
                                font=('Arial', 14, 'bold'),
                                fg='white', bg='#0f3460')
        lbl_canciones.pack(pady=10)
        
        # Tabla de canciones
        columnas = ('ID', 'Nombre', 'Artista', 'Duración')
        self.tabla_canciones = ttk.Treeview(frame_derecho, columns=columnas, show='headings')
        
        for col in columnas:
            self.tabla_canciones.heading(col, text=col)
            self.tabla_canciones.column(col, width=120)
        
        self.tabla_canciones.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Info de la playlist
        self.lbl_info = tk.Label(frame_derecho, text="",
                                font=('Arial', 10), fg='#ccc', bg='#0f3460')
        self.lbl_info.pack(pady=5)
        
        # Botones de acción
        frame_botones = tk.Frame(frame_derecho, bg='#0f3460')
        frame_botones.pack(pady=10)
        
        btn_eliminar_cancion = tk.Button(frame_botones, text="❌ Quitar canción",
                                        command=self.quitar_cancion,
                                        bg='#dc3545', fg='white',
                                        font=('Arial', 10, 'bold'))
        btn_eliminar_cancion.pack(side='left', padx=5)
        
        btn_eliminar_playlist = tk.Button(frame_botones, text="🗑 Eliminar playlist",
                                         command=self.eliminar_playlist,
                                         bg='#ff6b6b', fg='white',
                                         font=('Arial', 10, 'bold'))
        btn_eliminar_playlist.pack(side='left', padx=5)
        
        self.cargar_playlists()
    
    def cargar_playlists(self):
        self.lista_playlists.delete(0, 'end')
        playlists = Playlist.obtener_por_usuario(self.usuario_actual.id_persona)
        for p in playlists:
            self.lista_playlists.insert('end', f"{p[1]} ({p[0]})")
    
    def mostrar_canciones(self, event):
        seleccion = self.lista_playlists.curselection()
        if not seleccion:
            return
        
        texto = self.lista_playlists.get(seleccion[0])
        id_playlist = int(texto.split("(")[1].strip(")"))
        self.playlist_actual = Playlist.buscar_por_id(id_playlist)
        
        # Limpiar tabla
        for item in self.tabla_canciones.get_children():
            self.tabla_canciones.delete(item)
        
        # Cargar canciones
        canciones = self.playlist_actual.obtener_canciones()
        for c in canciones:
            duracion = f"{c[2] // 60}:{c[2] % 60:02d}"
            self.tabla_canciones.insert('', 'end', values=(c[0], c[1], c[3], duracion))
        
        total_canciones = self.playlist_actual.contar_canciones()
        duracion_total = self.playlist_actual.duracion_total()
        minutos = duracion_total // 60
        segundos = duracion_total % 60
        self.lbl_info.config(text=f"📊 {total_canciones} canciones • ⏱ {minutos}:{segundos:02d}")
    
    def quitar_cancion(self):
        if not self.playlist_actual:
            messagebox.showwarning("Advertencia", "Selecciona una playlist")
            return
        
        seleccion = self.tabla_canciones.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una canción")
            return
        
        id_cancion = self.tabla_canciones.item(seleccion[0])['values'][0]
        self.playlist_actual.quitar_cancion(id_cancion)
        
        messagebox.showinfo("Éxito", "Canción eliminada de la playlist")
        self.mostrar_canciones(None)
    
    def eliminar_playlist(self):
        if not self.playlist_actual:
            messagebox.showwarning("Advertencia", "Selecciona una playlist")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar esta playlist y todas sus canciones?"):
            self.playlist_actual.eliminar()
            messagebox.showinfo("Éxito", "Playlist eliminada")
            self.playlist_actual = None
            self.cargar_playlists()
            for item in self.tabla_canciones.get_children():
                self.tabla_canciones.delete(item)
            self.lbl_info.config(text="")
    
    def crear_playlist(self):
        from views.Ventana_crear_playlist import VentanaCrearPlaylist
        VentanaCrearPlaylist(self.usuario_actual)
        self.cargar_playlists()
    
    def ejecutar(self):
        self.ventana.grab_set()
        self.ventana.wait_window()