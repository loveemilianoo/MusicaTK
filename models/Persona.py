from database.Conexion import ConexionDB

class Persona:
    def __init__(self, id_persona=None, nombre=None, apellido=None, correo=None, sexo=None, edad=None):
        self._id_persona = id_persona
        self._nombre = nombre
        self._apellido = apellido
        self._correo = correo
        self._sexo = sexo
        self._edad = edad
        self.db = ConexionDB()

    @property
    def id_persona(self):
        return self._id_persona
    @id_persona.setter
    def id_persona(self, valor):
        self._id_persona = valor

    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def apellido(self):
        return self._apellido
    @apellido.setter
    def apellido(self, valor):
        self._apellido = valor

    @property
    def correo(self):
        return self._correo
    @correo.setter
    def correo(self, valor):
        self._correo = valor

    @property
    def sexo(self):
        return self._sexo
    @sexo.setter
    def sexo(self, valor):
        self._sexo = valor

    @property
    def edad(self):
        return self._edad
    @edad.setter
    def edad(self, valor):
        self._edad = valor

    @property
    def nombreCompleto(self):
        return f"{self.nombre} {self.apellido}"
    @nombreCompleto.setter
    def nombreCompleto(self, valor):
        partes = valor.split()
        if len(partes) >= 2:
            self.nombre = partes[0]
            self.apellido = ' '.join(partes[1:])
        else:
            self.nombre = valor
            self.apellido = ''