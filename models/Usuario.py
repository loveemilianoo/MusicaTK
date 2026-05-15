from database.Conexion import ConexionDB
from .Persona import Persona

class Usuario (Persona):
    def __init__(self, id_persona=None, nombre=None, apellido=None, correo=None, sexo=None, edad=None, telefono=None, membresia=None, contrasena=None):
        super().__init__(id_persona, nombre, apellido, correo, sexo, edad)
        self._telefono = telefono
        self._membresia = membresia
        self._contrasena = contrasena
        self.db = ConexionDB()
    
    @property
    def telefono(self):
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor):
        self._telefono = valor
    
    @property
    def membresia(self):
        return self._membresia
    
    @membresia.setter
    def membresia(self, valor):
        self._membresia = valor
    
    @property
    def contrasena(self):
        return self._contrasena
    
    @contrasena.setter
    def contrasena(self, valor):
        self._contrasena = valor