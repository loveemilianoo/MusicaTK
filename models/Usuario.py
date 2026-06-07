from database.Conexion import ConexionDB
from .Persona import Persona

class Usuario(Persona):
    def __init__(self, id_persona=None, nombre=None, apellido_paterno=None,
                 apellido_materno=None, fecha_nacimiento=None, fecha_fin=None,
                 telefono=None, contrasena=None):
        super().__init__(id_persona, nombre, apellido_paterno,
                         apellido_materno, fecha_nacimiento, fecha_fin)
        self._telefono  = telefono
        self._contrasena = contrasena
        self.db = ConexionDB()

    @property
    def telefono(self):
        return self._telefono
    @telefono.setter
    def telefono(self, v): self._telefono = v

    @property
    def contrasena(self):
        return self._contrasena
    @contrasena.setter
    def contrasena(self, v): self._contrasena = v