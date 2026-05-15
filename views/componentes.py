import tkinter as tk
from views.colores import *

class Componentes:
    """Widgets reutilizables con estilo consistente"""
    
    @staticmethod
    def btn(parent, text, cmd, fg=TEXT_PRI, bg=BG_CARD,
            font=FONT_BODY, pad=(12, 6), width=None):
        """Botón con hover effect"""
        frame = tk.Frame(parent, bg=bg, cursor="hand2")
        label = tk.Label(frame, text=text, fg=fg, bg=bg, font=font,
                         padx=pad[0], pady=pad[1])
        label.pack()
        
        frame.bind("<Button-1>", lambda e: cmd())
        label.bind("<Button-1>", lambda e: cmd())
        frame.bind("<Enter>", lambda e: frame.configure(bg=BG_HOVER) or label.configure(bg=BG_HOVER))
        frame.bind("<Leave>", lambda e: frame.configure(bg=bg) or label.configure(bg=bg))
        
        if width:
            label.configure(width=width)
        return frame
    
    @staticmethod
    def label(parent, text, font=FONT_BODY, fg=TEXT_PRI, bg=BG_DARK, anchor="w"):
        """Label con estilo"""
        return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, anchor=anchor)
    
    @staticmethod
    def entry(parent, placeholder="", show="", bg=BG_HOVER, width=30):
        """Entry con placeholder"""
        var = tk.StringVar(value=placeholder)
        entry = tk.Entry(parent, textvariable=var, font=FONT_BODY,
                         bg=bg, fg=TEXT_SEC, insertbackground=ACCENT2,
                         relief="flat", bd=0, show=show, width=width)
        
        def on_focus_in(e):
            if var.get() == placeholder:
                var.set("")
                entry.configure(fg=TEXT_PRI)
        
        def on_focus_out(e):
            if var.get() == "":
                var.set(placeholder)
                entry.configure(fg=TEXT_SEC)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return entry
    
    @staticmethod
    def divider(parent):
        """Línea divisoria"""
        tk.Frame(parent, height=1, bg=BORDER).pack(fill="x", pady=4)
    
    @staticmethod
    def cancion_row(parent, cancion_data, on_click=None, on_double_click=None, mostrar_icono=True):
        """Fila de canción reutilizable"""
        row = tk.Frame(parent, bg=BG_DARK, cursor="hand2")
        row.pack(fill="x", pady=2)
        
        if mostrar_icono:
            # Portada pequeña
            canvas = tk.Canvas(row, width=36, height=36, bg=ACCENT, highlightthickness=0)
            canvas.pack(side="left", padx=(2, 10))
            canvas.create_text(18, 18, text="♫", font=("Helvetica", 12), fill=ACCENT2)
        
        # Info
        info_frame = tk.Frame(row, bg=BG_DARK)
        info_frame.pack(side="left", fill="x", expand=True)
        
        nombre = cancion_data.get('nombre', '')
        artista = cancion_data.get('artista', '')
        
        tk.Label(info_frame, text=nombre, 
                font=("Helvetica", 10, "bold"), fg=TEXT_PRI, bg=BG_DARK).pack(anchor="w")
        tk.Label(info_frame, text=artista, 
                font=FONT_SMALL, fg=TEXT_SEC, bg=BG_DARK).pack(anchor="w")
        
        # Duración
        duracion = cancion_data.get('duracion', 0)
        if isinstance(duracion, (int, float)) and duracion > 0:
            minutos = int(duracion // 60)
            segundos = int(duracion % 60)
            texto_duracion = f"{minutos}:{segundos:02d}"
        else:
            texto_duracion = str(duracion) if duracion else "0:00"
        
        tk.Label(row, text=texto_duracion, font=FONT_TINY, fg=TEXT_MUT, 
                bg=BG_DARK).pack(side="right", padx=10)
        
        # Eventos hover
        def on_enter(e):
            row.configure(bg=BG_HOVER)
            info_frame.configure(bg=BG_HOVER)
            for child in info_frame.winfo_children():
                child.configure(bg=BG_HOVER)
        
        def on_leave(e):
            row.configure(bg=BG_DARK)
            info_frame.configure(bg=BG_DARK)
            for child in info_frame.winfo_children():
                child.configure(bg=BG_DARK)
        
        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)
        
        if on_click:
            row.bind("<Button-1>", lambda e: on_click(cancion_data))
        
        if on_double_click:
            row.bind("<Double-Button-1>", lambda e: on_double_click(cancion_data))
        
        return row
    
    @staticmethod
    def playlist_row(parent, playlist_data, on_click=None):
        """Fila de playlist reutilizable"""
        row = tk.Frame(parent, bg=BG_DARK, cursor="hand2")
        row.pack(fill="x", pady=3)
        
        # Ícono
        canvas = tk.Canvas(row, width=44, height=44, bg=ACCENT, highlightthickness=0)
        canvas.pack(side="left", padx=(0, 10))
        canvas.create_text(22, 22, text="♪", font=("Helvetica", 16), fill=ACCENT2)
        
        # Info
        info = tk.Frame(row, bg=BG_DARK)
        info.pack(side="left")
        tk.Label(info, text=playlist_data.get('nombre', ''), 
                font=FONT_H3, fg=TEXT_PRI, bg=BG_DARK).pack(anchor="w")
        
        total = playlist_data.get('total_canciones', 0)
        duracion = playlist_data.get('duracion_total', 0)
        minutos = duracion // 60 if isinstance(duracion, (int, float)) else 0
        texto_meta = f"{total} canciones • {minutos} min" if total else "Vacía"
        tk.Label(info, text=texto_meta, font=FONT_SMALL, fg=TEXT_SEC, 
                bg=BG_DARK).pack(anchor="w")
        
        # Eventos hover
        def on_enter(e):
            row.configure(bg=BG_HOVER)
            info.configure(bg=BG_HOVER)
            for child in info.winfo_children():
                child.configure(bg=BG_HOVER)
        
        def on_leave(e):
            row.configure(bg=BG_DARK)
            info.configure(bg=BG_DARK)
            for child in info.winfo_children():
                child.configure(bg=BG_DARK)
        
        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)
        
        if on_click:
            row.bind("<Button-1>", lambda e: on_click(playlist_data))
        
        return row
    
    @staticmethod
    def card(parent, titulo, subtitulo, color=ACCENT, on_click=None):
        """Tarjeta reutilizable"""
        card = tk.Frame(parent, bg=color, cursor="hand2")
        card.pack(side="left", padx=(0, 10), ipadx=10, ipady=10)
        
        tk.Label(card, text=titulo, font=("Helvetica", 10, "bold"),
                fg=TEXT_PRI, bg=color, padx=16, pady=20, justify="left").pack()
        
        if subtitulo:
            tk.Label(card, text=subtitulo, font=FONT_TINY,
                    fg=TEXT_SEC, bg=color).pack()
        
        if on_click:
            card.bind("<Button-1>", lambda e: on_click())
            card.bind("<Enter>", lambda e: card.configure(bg=lighten(color)))
            card.bind("<Leave>", lambda e: card.configure(bg=color))
        
        return card