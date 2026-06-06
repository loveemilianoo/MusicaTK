from database.Conexion import ConexionDB
from .Persona import Persona

class Artista(Persona):
    def __init__(self, id_persona=None, nombre=None, apellido_paterno=None,
                 apellido_materno=None, fecha_nacimiento=None, fecha_fin=None,
                 banda=0, disquera=None):
        super().__init__(id_persona, nombre, apellido_paterno,
                         apellido_materno, fecha_nacimiento, fecha_fin)
        self._banda    = banda
        self._disquera = disquera
        self.db = ConexionDB()

    @property
    def banda(self):
        return self._banda
    @banda.setter
    def banda(self, v): self._banda = v

    @property
    def disquera(self):
        return self._disquera
    @disquera.setter
    def disquera(self, v): self._disquera = v