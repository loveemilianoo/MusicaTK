from controller.BaseController import BaseController
from models.IdentidadGenero import IdentidadGenero

class IdentidadGeneroDAO(BaseController):

    @staticmethod
    def listar_todas():
        """Listar el catálogo de identidades de género"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """SELECT Id, IdentidadDeGenero
                       FROM IdentidadDeGenero
                       ORDER BY IdentidadDeGenero"""
            cursor.execute(query)
            results = cursor.fetchall()

            identidades = []
            for row in results:
                identidades.append(IdentidadGenero(
                    id_identidad=row[0],
                    identidad=row[1]
                ))
            return identidades
        except Exception as e:
            print(f"Error al listar identidades de género: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def asignar_a_persona(id_persona, id_identidad):
        """Asignar (o reemplazar) la identidad de género de una persona"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            # Una identidad por persona: limpiar la anterior y registrar la nueva
            cursor.execute(
                "DELETE FROM Genero_Persona WHERE id_persona = :1",
                (id_persona,)
            )
            cursor.execute(
                """INSERT INTO Genero_Persona (id_persona, id_identidad)
                   VALUES (:1, :2)""",
                (id_persona, id_identidad)
            )
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al asignar identidad de género: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def obtener_de_persona(id_persona):
        """Obtener la identidad de género de una persona (o None)"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """SELECT i.Id, i.IdentidadDeGenero
                       FROM Genero_Persona gp
                       JOIN IdentidadDeGenero i ON gp.id_identidad = i.Id
                       WHERE gp.id_persona = :1"""
            cursor.execute(query, (id_persona,))
            row = cursor.fetchone()

            if row:
                return IdentidadGenero(id_identidad=row[0], identidad=row[1])
            return None
        except Exception as e:
            print(f"Error al obtener identidad de género: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
