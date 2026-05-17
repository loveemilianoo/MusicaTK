from datetime import date

class Album:
    def __init__(self, id_album=None, nombre=None, id_persona=None, 
                 fecha_lanzamiento=None):
        self.id_album = id_album
        self.nombre = nombre
        self.id_persona = id_persona
        self.fecha_lanzamiento = fecha_lanzamiento or date.today()
        self.nombre_artista = None  # Para JOIN con Persona
    
    def __str__(self):
        return f"{self.nombre} (ID: {self.id_album})"
    
    def to_dict(self):
        return {
            'id_album': self.id_album,
            'nombre': self.nombre,
            'id_persona': self.id_persona,
            'fecha_lanzamiento': self.fecha_lanzamiento,
            'nombre_artista': self.nombre_artista
        }