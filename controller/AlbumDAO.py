import oracledb
from controller.BaseController import BaseController
from models.Album import Album
from datetime import date

class AlbumDAO(BaseController):
    
    @staticmethod
    def crear_album(album):
        """Insertar un nuevo álbum"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """INSERT INTO Album (id_persona, Nombre, FechaLanzamiento) 
                       VALUES (:1, :2, :3) RETURNING Id INTO :4"""
            
            id_album = cursor.var(oracledb.NUMBER)
            cursor.execute(query, (album.id_persona, album.nombre, 
                                   album.fecha_lanzamiento, id_album))
            
            # Extraer correctamente el valor
            id_value = id_album.getvalue()
            if isinstance(id_value, (list, tuple)):
                id_value = id_value[0]
            
            print(f"✓ Album '{album.nombre}' creado con ID: {id_value}")
            conexion.commit()
            return id_value
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al crear álbum: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_album_por_id(id_album):
        """Obtener álbum por ID"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT Id, id_persona, Nombre, FechaLanzamiento FROM Album WHERE Id = :1"
            cursor.execute(query, (id_album,))
            result = cursor.fetchone()
            
            if result:
                return Album(
                    id_album=result[0],
                    id_persona=result[1],
                    nombre=result[2],
                    fecha_lanzamiento=result[3]
                )
            return None
        except Exception as e:
            print(f"Error al obtener álbum: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_albumes_por_artista(id_persona):
        """Obtener todos los álbumes de un artista"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT Id, id_persona, Nombre, FechaLanzamiento 
                       FROM Album WHERE id_persona = :1 
                       ORDER BY FechaLanzamiento DESC"""
            cursor.execute(query, (id_persona,))
            results = cursor.fetchall()
            
            albumes = []
            for row in results:
                album = Album(
                    id_album=row[0],
                    id_persona=row[1],
                    nombre=row[2],
                    fecha_lanzamiento=row[3]
                )
                albumes.append(album)
            return albumes
        except Exception as e:
            print(f"Error al obtener álbumes: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def actualizar_album(album):
        """Actualizar álbum existente"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """UPDATE Album SET Nombre=:1, id_persona=:2, 
                       FechaLanzamiento=:3 WHERE Id=:4"""
            cursor.execute(query, (album.nombre, album.id_persona,
                                   album.fecha_lanzamiento, album.id_album))
            conexion.commit()
            print(f"✓ Album '{album.nombre}' actualizado")
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al actualizar álbum: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def eliminar_album(id_album):
        """Eliminar álbum"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            # Primero verificar si tiene canciones
            query_check = "SELECT COUNT(*) FROM Cancion WHERE id_album = :1"
            cursor.execute(query_check, (id_album,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"⚠ El álbum tiene {count} canciones. Elimínelas primero.")
                return False
            
            query = "DELETE FROM Album WHERE Id = :1"
            cursor.execute(query, (id_album,))
            conexion.commit()
            print(f"✓ Album ID {id_album} eliminado")
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al eliminar álbum: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def listar_todos_albumes():
        """Listar todos los álbumes"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT a.Id, a.id_persona, a.Nombre, a.FechaLanzamiento, 
                              p.Nombre as Artista
                       FROM Album a
                       JOIN Persona p ON a.id_persona = p.id_persona
                       ORDER BY a.FechaLanzamiento DESC"""
            cursor.execute(query)
            results = cursor.fetchall()
            
            albumes = []
            for row in results:
                album = Album(
                    id_album=row[0],
                    id_persona=row[1],
                    nombre=row[2],
                    fecha_lanzamiento=row[3]
                )
                album.nombre_artista = row[4]  # Campo adicional
                albumes.append(album)
            return albumes
        except Exception as e:
            print(f"Error al listar álbumes: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def buscar_album_por_nombre(nombre):
        """Buscar álbumes por nombre"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT Id, id_persona, Nombre, FechaLanzamiento 
                       FROM Album 
                       WHERE LOWER(Nombre) LIKE :1
                       ORDER BY Nombre"""
            cursor.execute(query, (f"%{nombre.lower()}%",))
            results = cursor.fetchall()
            
            albumes = []
            for row in results:
                album = Album(
                    id_album=row[0],
                    id_persona=row[1],
                    nombre=row[2],
                    fecha_lanzamiento=row[3]
                )
                albumes.append(album)
            return albumes
        except Exception as e:
            print(f"Error al buscar álbumes: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_albumes_recientes(limite=10):
        """Obtener los últimos álbumes lanzados"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            # Sintaxis compatible con Oracle
            query = """SELECT * FROM (
                          SELECT a.Id, a.id_persona, a.Nombre, a.FechaLanzamiento,
                                 p.Nombre as Artista
                          FROM Album a
                          JOIN Persona p ON a.id_persona = p.id_persona
                          ORDER BY a.FechaLanzamiento DESC
                      ) WHERE ROWNUM <= :1"""
            cursor.execute(query, (limite,))
            results = cursor.fetchall()
            
            albumes = []
            for row in results:
                album = Album(
                    id_album=row[0],
                    id_persona=row[1],
                    nombre=row[2],
                    fecha_lanzamiento=row[3]
                )
                album.nombre_artista = row[4]
                albumes.append(album)
            return albumes
        except Exception as e:
            print(f"Error al obtener álbumes recientes: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_canciones_del_album(id_album):
        """Obtener todas las canciones de un álbum"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT Id, Nombre, Duracion, No_track
                       FROM Cancion
                       WHERE id_album = :1
                       ORDER BY No_track"""
            cursor.execute(query, (id_album,))
            results = cursor.fetchall()
            
            canciones = []
            for row in results:
                canciones.append({
                    'id': row[0],
                    'nombre': row[1],
                    'duracion': row[2],
                    'track': row[3]
                })
            return canciones
        except Exception as e:
            print(f"Error al obtener canciones del álbum: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def contar_canciones_album(id_album):
        """Contar cuántas canciones tiene un álbum"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT COUNT(*) FROM Cancion WHERE id_album = :1"
            cursor.execute(query, (id_album,))
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error al contar canciones: {e}")
            return 0
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def duracion_total_album(id_album):
        """Calcular duración total del álbum en segundos"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT SUM(Duracion) FROM Cancion WHERE id_album = :1"
            cursor.execute(query, (id_album,))
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0
        except Exception as e:
            print(f"Error al calcular duración: {e}")
            return 0
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def agregar_cancion_a_album(id_album, id_cancion, numero_track=None):
        """
        Actualiza la FK id_album en la tabla Cancion para asociarla al álbum
        """
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            # Actualizar la canción con el ID del álbum
            if numero_track is not None:
                query = "UPDATE Cancion SET id_album = :1, No_track = :2 WHERE Id = :3"
                cursor.execute(query, (id_album, numero_track, id_cancion))
            else:
                query = "UPDATE Cancion SET id_album = :1 WHERE Id = :2"
                cursor.execute(query, (id_album, id_cancion))
            
            conexion.commit()
            print(f"✓ Canción {id_cancion} asociada al álbum {id_album}")
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al asociar canción: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)