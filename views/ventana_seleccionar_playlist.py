import tkinter as tk
from tkinter import ttk, messagebox
from models.Playlist import Playlist

class VentanaSeleccionarPlaylist:
    def __init__(self, usuario_actual, id_cancion):
        self.usuario_actual = usuario_actual
        self.id_cancion = id_cancion
        self.ventana = tk.Toplevel()
        self.ventana.title("Agregar a Playlist")
        self.ventana.geometry("400x400")
        self.ventana.configure(bg='#1a1a2e')
        self.setup_ui()
    
    def setup_ui(self):
        lbl_titulo = tk.Label(self.ventana, text="📋 Seleccionar Playlist",
                              font=('Arial', 16, 'bold'),
                              fg='#e94560', bg='#1a1a2e')
        lbl_titulo.pack(pady=20)
        
        # Lista de playlists
        self.lista_playlists = tk.Listbox(self.ventana, font=('Arial', 12),
                                          bg='#16213e', fg='white',
                                          selectbackground='#e94560',
                                          height=10)
        self.lista_playlists.pack(fill='both', expand=True, padx=40, pady=10)
        
        self.cargar_playlists()
        
        # Botones
        frame_botones = tk.Frame(self.ventana, bg='#1a1a2e')
        frame_botones.pack(pady=20)
        
        btn_agregar = tk.Button(frame_botones, text="➕ Agregar",
                               command=self.agregar_a_playlist,
                               bg='#28a745', fg='white',
                               font=('Arial', 11, 'bold'), width=12)
        btn_agregar.pack(side='left', padx=10)
        
        btn_crear = tk.Button(frame_botones, text="✨ Crear nueva",
                              command=self.crear_nueva_playlist,
                              bg='#007bff', fg='white',
                              font=('Arial', 11, 'bold'), width=12)
        btn_crear.pack(side='left', padx=10)
        
        btn_cancelar = tk.Button(frame_botones, text="Cancelar",
                                command=self.ventana.destroy,
                                bg='#dc3545', fg='white',
                                font=('Arial', 11, 'bold'), width=12)
        btn_cancelar.pack(side='left', padx=10)
    
    def cargar_playlists(self):
        playlists = Playlist.obtener_por_usuario(self.usuario_actual.id_persona)
        for p in playlists:
            self.lista_playlists.insert('end', f"{p[1]} (ID: {p[0]})")
    
    def agregar_a_playlist(self):
        seleccion = self.lista_playlists.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una playlist")
            return
        
        texto = self.lista_playlists.get(seleccion[0])
        id_playlist = int(texto.split("ID: ")[1].strip(")"))
        
        playlist = Playlist.buscar_por_id(id_playlist)
        if playlist.agregar_cancion(self.id_cancion):
            messagebox.showinfo("Éxito", "Canción agregada a la playlist")
            self.ventana.destroy()
        else:
            messagebox.showwarning("Advertencia", "La canción ya está en esta playlist")
    
    def crear_nueva_playlist(self):
        self.ventana.destroy()
        from views.ventana_crear_playlist import VentanaCrearPlaylist
        ventana = VentanaCrearPlaylist(self.usuario_actual, self.id_cancion)
        ventana.ejecutar()