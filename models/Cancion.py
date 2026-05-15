from database.Conexion import ConexionDB

class Cancion:
    def __init__(self, id_cancion=None, nombre=None, duracion=None, id_artista=None, id_album=None, notrack=None):
        self._id_cancion = id_cancion
        self._nombre = nombre
        self._duracion = duracion  
        self._id_artista = id_artista
        self._id_album = id_album
        self._notrack = notrack
        self.db = ConexionDB()
    
    @property
    def id_cancion(self):
        return self._id_cancion
    
    @id_cancion.setter
    def id_cancion(self, valor):
        self._id_cancion = valor
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor
    
    @property
    def duracion(self):
        return self._duracion
    
    @duracion.setter
    def duracion(self, valor):
        self._duracion = valor
    
    @property
    def id_artista(self):
        return self._id_artista
    
    @id_artista.setter
    def id_artista(self, valor):
        self._id_artista = valor
    
    @property
    def id_album(self):
        return self._id_album
    
    @id_album.setter
    def id_album(self, valor):
        self._id_album = valor
    
    @property
    def notrack(self):
        return self._notrack
    
    @notrack.setter
    def notrack(self, valor):
        self._notrack = valor