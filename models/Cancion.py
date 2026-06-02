from datetime import date

class Cancion:
    def __init__(self, id_cancion=None, nombre=None, duracion=None,
                 id_artista=None, id_album=None, no_track=None,
                 fecha_lanzamiento=None, ruta_archivo=None):  
        self.id_cancion = id_cancion
        self.nombre = nombre
        self.duracion = duracion
        self.id_artista = id_artista
        self.id_album = id_album
        self.no_track = no_track
        self.fecha_lanzamiento = fecha_lanzamiento or date.today()
        self.ruta_archivo = ruta_archivo  
        self.nombre_artista = None

    def formatear_duracion(self):
        minutos = self.duracion // 60
        segundos = self.duracion % 60
        return f"{minutos}:{segundos:02d}"

    def __str__(self):
        return f"{self.nombre} - {self.formatear_duracion()}"