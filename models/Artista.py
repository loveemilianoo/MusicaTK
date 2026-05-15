from database.Conexion import ConexionDB
from .Persona import Persona

class Artista (Persona):
    def __init__(self, id_persona=None, nombre=None, apellido=None, correo=None, sexo=None, edad=None, banda=0, disquera=None):
        super().__init__(id_persona, nombre, apellido, correo, sexo, edad)
        self._banda = banda  
        self._disquera = disquera
        self.db = ConexionDB()
    
    @property
    def banda(self):
        return self._banda
    
    @banda.setter
    def banda(self, valor):
        self._banda = valor
    
    @property
    def disquera(self):
        return self._disquera
    
    @disquera.setter
    def disquera(self, valor):
        self._disquera = valor