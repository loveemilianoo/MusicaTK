import oracledb
from controller.BaseController import BaseController
from models.Artista import Artista

class ArtistaDAO(BaseController):

    @staticmethod
    def crear_artista(artista):
        """Inserta en Persona y luego en Artista"""
        conexion = None
        cursor   = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor   = conexion.cursor()

            query_persona = """INSERT INTO Persona
                                   (Nombre, ApellidoPaterno, ApellidoMaterno,
                                    FechaDeNacimiento, FechaDeFin)
                               VALUES (:1, :2, :3, :4, :5)
                               RETURNING id_persona INTO :6"""
            id_var = cursor.var(oracledb.NUMBER)
            cursor.execute(query_persona, (
                artista.nombre,
                artista.apellido_paterno,
                artista.apellido_materno,
                artista.fecha_nacimiento,
                artista.fecha_fin,
                id_var
            ))
            id_val = id_var.getvalue()
            if isinstance(id_val, (list, tuple)):
                id_val = id_val[0]

            query_artista = """INSERT INTO Artista (id_persona, Banda, Disquera)
                               VALUES (:1, :2, :3)"""
            cursor.execute(query_artista, (id_val, artista.banda, artista.disquera))

            conexion.commit()
            print(f"✓ Artista '{artista.nombre}' creado con ID: {id_val}")
            return id_val
        except Exception as e:
            if conexion: conexion.rollback()
            print(f"Error al crear artista: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def obtener_artista_por_id(id_persona):
        """Devuelve objeto Artista si el id_persona existe en tabla Artista"""
        conexion = None
        cursor   = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor   = conexion.cursor()
            query = """SELECT p.id_persona, p.Nombre, p.ApellidoPaterno,
                              p.ApellidoMaterno, p.FechaDeNacimiento,
                              a.Banda, a.Disquera
                       FROM Persona p
                       JOIN Artista a ON p.id_persona = a.id_persona
                       WHERE p.id_persona = :1"""
            cursor.execute(query, (id_persona,))
            row = cursor.fetchone()
            if row:
                return Artista(
                    id_persona       = row[0],
                    nombre           = row[1],
                    apellido_paterno = row[2],
                    apellido_materno = row[3],
                    fecha_nacimiento = row[4],
                    banda            = row[5],
                    disquera         = row[6]
                )
            return None
        except Exception as e:
            print(f"Error al obtener artista: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def verificar_artista(nombre, apellido_paterno, apellido_materno, fecha_nacimiento):
        """
        Login de artista — misma lógica que verificar_usuario
        pero hace JOIN con Artista en lugar de Usuario.
        """
        conexion = None
        cursor   = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor   = conexion.cursor()
            query = """SELECT p.id_persona, p.Nombre, p.ApellidoPaterno,
                              p.ApellidoMaterno, p.FechaDeNacimiento,
                              a.Banda, a.Disquera
                       FROM Persona p
                       JOIN Artista a ON p.id_persona = a.id_persona
                       WHERE LOWER(p.Nombre)          = LOWER(:1)
                         AND LOWER(p.ApellidoPaterno) = LOWER(:2)
                         AND LOWER(NVL(p.ApellidoMaterno, '')) = LOWER(NVL(:3, ''))
                         AND TRUNC(p.FechaDeNacimiento) = TRUNC(TO_DATE(:4, 'YYYY-MM-DD'))"""
            cursor.execute(query, (
                nombre, apellido_paterno,
                apellido_materno or '', fecha_nacimiento
            ))
            row = cursor.fetchone()
            if row:
                return Artista(
                    id_persona       = row[0],
                    nombre           = row[1],
                    apellido_paterno = row[2],
                    apellido_materno = row[3],
                    fecha_nacimiento = row[4],
                    banda            = row[5],
                    disquera         = row[6]
                )
            return None
        except Exception as e:
            print(f"Error al verificar artista: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def convertir_usuario_a_artista(id_persona, banda=0, disquera=None):
        """
        Convierte un Usuario existente en Artista
        insertando su id_persona en la tabla Artista.
        """
        conexion = None
        cursor   = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor   = conexion.cursor()
            query = """INSERT INTO Artista (id_persona, Banda, Disquera)
                       VALUES (:1, :2, :3)"""
            cursor.execute(query, (id_persona, banda, disquera))
            conexion.commit()
            print(f"✓ Usuario {id_persona} convertido a Artista")
            return True
        except Exception as e:
            if conexion: conexion.rollback()
            print(f"Error al convertir a artista: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def listar_todos_artistas():
        conexion = None
        cursor   = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor   = conexion.cursor()
            query = """SELECT p.id_persona, p.Nombre, p.ApellidoPaterno,
                              p.ApellidoMaterno, p.FechaDeNacimiento,
                              a.Banda, a.Disquera
                       FROM Persona p
                       JOIN Artista a ON p.id_persona = a.id_persona
                       ORDER BY p.Nombre"""
            cursor.execute(query)
            results = cursor.fetchall()
            artistas = []
            for row in results:
                artistas.append(Artista(
                    id_persona       = row[0],
                    nombre           = row[1],
                    apellido_paterno = row[2],
                    apellido_materno = row[3],
                    fecha_nacimiento = row[4],
                    banda            = row[5],
                    disquera         = row[6]
                ))
            return artistas
        except Exception as e:
            print(f"Error al listar artistas: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def actualizar_artista(id_persona, datos):
        conexion = None
        cursor   = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor   = conexion.cursor()
            query_persona = """UPDATE Persona SET Nombre=:1, ApellidoPaterno=:2
                               WHERE id_persona=:3"""
            cursor.execute(query_persona, (
                datos.get("nombre"), datos.get("apellido_paterno"), id_persona
            ))
            query_artista = """UPDATE Artista SET Banda=:1, Disquera=:2
                               WHERE id_persona=:3"""
            cursor.execute(query_artista, (
                datos.get("es_banda"), datos.get("disquera"), id_persona
            ))
            conexion.commit()
            return True
        except Exception as e:
            if conexion: conexion.rollback()
            print(f"Error al actualizar artista: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)