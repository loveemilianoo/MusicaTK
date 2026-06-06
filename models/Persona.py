from database.Conexion import ConexionDB

class Persona:
    def __init__(self, id_persona=None, nombre=None, apellido_paterno=None,
                 apellido_materno=None, fecha_nacimiento=None, fecha_fin=None):
        self._id_persona       = id_persona
        self._nombre           = nombre
        self._apellido_paterno = apellido_paterno
        self._apellido_materno = apellido_materno
        self._fecha_nacimiento = fecha_nacimiento
        self._fecha_fin        = fecha_fin
        self.db = ConexionDB()

    @property
    def id_persona(self):
        return self._id_persona
    @id_persona.setter
    def id_persona(self, v): self._id_persona = v

    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, v): self._nombre = v

    @property
    def apellido_paterno(self):
        return self._apellido_paterno
    @apellido_paterno.setter
    def apellido_paterno(self, v): self._apellido_paterno = v

    @property
    def apellido_materno(self):
        return self._apellido_materno
    @apellido_materno.setter
    def apellido_materno(self, v): self._apellido_materno = v

    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento
    @fecha_nacimiento.setter
    def fecha_nacimiento(self, v): self._fecha_nacimiento = v

    @property
    def fecha_fin(self):
        return self._fecha_fin
    @fecha_fin.setter
    def fecha_fin(self, v): self._fecha_fin = v

    @property
    def nombre_completo(self):
        partes = [self._nombre, self._apellido_paterno]
        if self._apellido_materno:
            partes.append(self._apellido_materno)
        return " ".join(partes)