from database.Conexion import ConexionDB

class Genero:
    def __init__(self, id_genero=None, nombre=None):
        self._id_genero = id_genero
        self._nombre = nombre
        self.db = ConexionDB()
    
    @property
    def id_genero(self):
        return self._id_genero
    
    @id_genero.setter
    def id_genero(self, valor):
        self._id_genero = valor
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor