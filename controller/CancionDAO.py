import oracledb
from controller.BaseController import BaseController
from models.Cancion import Cancion
from datetime import date

class CancionDAO(BaseController):

    @staticmethod
    def crear_cancion(cancion):
        """Insertar una nueva canción"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """INSERT INTO Cancion
                           (Nombre, Duracion, id_artista, FechaDeLanzamiento, RutaDeArchivo)
                       VALUES (:1, :2, :3, :4, :5) RETURNING Id INTO :6"""

            id_cancion = cursor.var(oracledb.NUMBER)
            cursor.execute(query, (cancion.nombre, cancion.duracion,
                                   cancion.id_artista, cancion.fecha_lanzamiento,
                                   cancion.ruta_de_archivo, id_cancion))

            id_value = id_cancion.getvalue()
            if isinstance(id_value, (list, tuple)):
                id_value = id_value[0]

            print(f"✓ Canción '{cancion.nombre}' creada con ID: {id_value}")
            conexion.commit()
            return id_value
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al crear canción: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def obtener_canciones_por_artista(id_artista):
        """Obtener todas las canciones de un artista"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """SELECT Id, Nombre, Duracion, id_album, NumeroDeTrack,
                              FechaDeLanzamiento, RutaDeArchivo
                       FROM Cancion
                       WHERE id_artista = :1
                       ORDER BY FechaDeLanzamiento DESC"""
            cursor.execute(query, (id_artista,))
            results = cursor.fetchall()

            canciones = []
            for row in results:
                cancion = Cancion(
                    id_cancion=row[0],
                    nombre=row[1],
                    duracion=row[2],
                    id_artista=id_artista,
                    id_album=row[3],
                    numero_track=row[4],
                    fecha_lanzamiento=row[5],
                    ruta_de_archivo=row[6]  # ── NUEVO
                )
                canciones.append(cancion)
            return canciones
        except Exception as e:
            print(f"Error al obtener canciones: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def obtener_todas_canciones():
        """Obtener todas las canciones"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """SELECT c.Id, c.Nombre, c.Duracion, c.id_artista,
                              p.Nombre as Artista, c.id_album,
                              c.FechaDeLanzamiento, c.RutaDeArchivo
                       FROM Cancion c
                       JOIN Persona p ON c.id_artista = p.id_persona
                       ORDER BY c.FechaDeLanzamiento DESC"""
            cursor.execute(query)
            results = cursor.fetchall()

            canciones = []
            for row in results:
                cancion = Cancion(
                    id_cancion=row[0],
                    nombre=row[1],
                    duracion=row[2],
                    id_artista=row[3],
                    id_album=row[5],
                    fecha_lanzamiento=row[6],
                    ruta_de_archivo=row[7]  # ── NUEVO
                )
                cancion.nombre_artista = row[4]
                canciones.append(cancion)
            return canciones
        except Exception as e:
            print(f"Error al obtener canciones: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def buscar_cancion_por_nombre(nombre):
        """Buscar canciones por nombre"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """SELECT Id, Nombre, Duracion, id_artista, id_album,
                              NumeroDeTrack, RutaDeArchivo
                       FROM Cancion
                       WHERE LOWER(Nombre) LIKE LOWER(:1)
                       ORDER BY Nombre"""
            cursor.execute(query, (f"%{nombre}%",))
            results = cursor.fetchall()

            canciones = []
            for row in results:
                cancion = Cancion(
                    id_cancion=row[0],
                    nombre=row[1],
                    duracion=row[2],
                    id_artista=row[3],
                    id_album=row[4],
                    numero_track=row[5],
                    ruta_de_archivo=row[6]  # ── NUEVO
                )
                canciones.append(cancion)
            return canciones
        except Exception as e:
            print(f"Error al buscar canciones: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def obtener_cancion_por_id(id_cancion):
        """Obtener canción por ID"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """SELECT Id, Nombre, Duracion, id_artista, id_album,
                              NumeroDeTrack, FechaDeLanzamiento, RutaDeArchivo
                       FROM Cancion WHERE Id = :1"""
            cursor.execute(query, (id_cancion,))
            result = cursor.fetchone()

            if result:
                return Cancion(
                    id_cancion=result[0],
                    nombre=result[1],
                    duracion=result[2],
                    id_artista=result[3],
                    id_album=result[4],
                    numero_track=result[5],
                    fecha_lanzamiento=result[6],
                    ruta_de_archivo=result[7]  # ── NUEVO
                )
            return None
        except Exception as e:
            print(f"Error al obtener canción: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def actualizar_cancion(cancion):
        """Actualizar canción existente"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            query = """UPDATE Cancion
                       SET Nombre = :1, Duracion = :2, id_artista = :3,
                           id_album = :4, NumeroDeTrack = :5,
                           FechaDeLanzamiento = :6, RutaDeArchivo = :7
                       WHERE Id = :8"""
            cursor.execute(query, (cancion.nombre, cancion.duracion,
                                   cancion.id_artista, cancion.id_album,
                                   cancion.numero_track, cancion.fecha_lanzamiento,
                                   cancion.ruta_de_archivo, cancion.id_cancion))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al actualizar canción: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def eliminar_cancion(id_cancion):
        """Eliminar canción"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()

            try:
                cursor.execute(
                    "DELETE FROM Cancion_Playlist WHERE id_cancion = :1",
                    (id_cancion,)
                )
            except:
                pass

            query = "DELETE FROM Cancion WHERE Id = :1"
            cursor.execute(query, (id_cancion,))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al eliminar canción: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod  # ── NUEVO MÉTODO
    def actualizar_ruta(id_cancion, ruta_archivo):
        """Actualizar solo la ruta del archivo de audio"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            query = "UPDATE Cancion SET RutaDeArchivo = :1 WHERE Id = :2"
            cursor.execute(query, (ruta_archivo, id_cancion))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al actualizar ruta: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)