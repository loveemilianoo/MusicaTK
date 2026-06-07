import oracledb
from controller.BaseController import BaseController
from models.Persona import Persona

class PersonaDAO(BaseController):

    @staticmethod
    def crear_persona(persona):
        """Insertar una nueva persona"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """INSERT INTO Persona
                           (Nombre, ApellidoPaterno, ApellidoMaterno, FechaDeNacimiento)
                       VALUES (:1, :2, :3, :4) RETURNING id_persona INTO :5"""

            id_persona = cursor.var(oracledb.NUMBER)
            cursor.execute(query, (persona.nombre, persona.apellido_paterno,
                                   persona.apellido_materno, persona.fecha_nacimiento,
                                   id_persona))

            id_value = id_persona.getvalue()
            if isinstance(id_value, (list, tuple)):
                id_value = id_value[0]

            print(f"✓ Persona '{persona.nombre}' creada con ID: {id_value}")
            conexion.commit()
            return id_value
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al crear persona: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def obtener_persona_por_id(id_persona):
        """Obtener persona por ID"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """SELECT id_persona, Nombre, ApellidoPaterno, ApellidoMaterno,
                              FechaDeNacimiento, FechaDeFin
                       FROM Persona WHERE id_persona = :1"""
            cursor.execute(query, (id_persona,))
            result = cursor.fetchone()

            if result:
                return Persona(
                    id_persona=result[0],
                    nombre=result[1],
                    apellido_paterno=result[2],
                    apellido_materno=result[3],
                    fecha_nacimiento=result[4],
                    fecha_fin=result[5]
                )
            return None
        except Exception as e:
            print(f"Error al obtener persona: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def actualizar_persona(persona):
        """Actualizar persona existente"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """UPDATE Persona
                       SET Nombre=:1, ApellidoPaterno=:2, ApellidoMaterno=:3,
                           FechaDeNacimiento=:4
                       WHERE id_persona=:5"""
            cursor.execute(query, (persona.nombre, persona.apellido_paterno,
                                   persona.apellido_materno, persona.fecha_nacimiento,
                                   persona.id_persona))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al actualizar persona: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def eliminar_persona(id_persona):
        """Eliminar persona (y sus extensiones por CASCADE)"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = "DELETE FROM Persona WHERE id_persona = :1"
            cursor.execute(query, (id_persona,))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al eliminar persona: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def listar_todas_personas():
        """Listar todas las personas"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """SELECT id_persona, Nombre, ApellidoPaterno, ApellidoMaterno,
                              FechaDeNacimiento, FechaDeFin
                       FROM Persona ORDER BY Nombre"""
            cursor.execute(query)
            resultados = cursor.fetchall()

            personas = []
            for row in resultados:
                persona = Persona(
                    id_persona=row[0],
                    nombre=row[1],
                    apellido_paterno=row[2],
                    apellido_materno=row[3],
                    fecha_nacimiento=row[4],
                    fecha_fin=row[5]
                )
                personas.append(persona)
            return personas
        except Exception as e:
            print(f"Error al listar personas: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
