from database.Conexion import ConexionDB
from datetime import date

class Album:
    def __init__(self, id_album=None, nombre=None, id_persona=None, fecha_lanzamiento=None):
        self._id_album = id_album
        self._nombre = nombre
        self._id_persona = id_persona
        self._fecha_lanzamiento = fecha_lanzamiento or date.today()
        self.db = ConexionDB()
    
    @property
    def id_album(self):
        return self._id_album
    
    @id_album.setter
    def id_album(self, valor):
        self._id_album = valor
    
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
    def fecha_lanzamiento(self):
        return self._fecha_lanzamiento
    
    @fecha_lanzamiento.setter
    def fecha_lanzamiento(self, valor):
        self._fecha_lanzamiento = valor