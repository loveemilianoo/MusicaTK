class IdentidadGenero:
    def __init__(self, id_identidad=None, identidad=None):
        self._id_identidad = id_identidad
        self._identidad = identidad

    @property
    def id_identidad(self):
        return self._id_identidad

    @id_identidad.setter
    def id_identidad(self, valor):
        self._id_identidad = valor

    @property
    def identidad(self):
        return self._identidad

    @identidad.setter
    def identidad(self, valor):
        self._identidad = valor
