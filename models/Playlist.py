from database.Conexion import ConexionDB
from datetime import date

class Playlist:
    def __init__(self, id_playlist=None, nombre=None, id_persona=None, fecha_creacion=None):
        self._id_playlist = id_playlist
        self._nombre = nombre
        self._id_persona = id_persona
        self._fecha_creacion = fecha_creacion or date.today()
        self.db = ConexionDB()
    
    @property
    def id_playlist(self):
        return self._id_playlist
    
    @id_playlist.setter
    def id_playlist(self, valor):
        self._id_playlist = valor
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor
    
    @property
    def id_persona(self):
        return self._id_persona
    
    @id_persona.setter
    def id_persona(self, valor):
        self._id_persona = valor
    
    @property
    def fecha_creacion(self):
        return self._fecha_creacion
    
    @fecha_creacion.setter
    def fecha_creacion(self, valor):
        self._fecha_creacion = valor