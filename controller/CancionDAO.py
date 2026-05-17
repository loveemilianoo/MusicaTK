import oracledb
from controller.BaseController import BaseController
from models.Cancion import Cancion

class CancionDAO(BaseController):
    
    @staticmethod
    def crear_cancion(cancion):
        """Insertar una nueva canción"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """INSERT INTO Cancion (Nombre, Duracion, id_artista, id_album, Notrack) 
                       VALUES (:1, :2, :3, :4, :5) RETURNING Id INTO :6"""
            
            id_cancion = cursor.var(oracledb.NUMBER)
            cursor.execute(query, (cancion.nombre, cancion.duracion, 
                                   cancion.id_artista, cancion.id_album,
                                   cancion.notrack, id_cancion))
            
            # Extraer correctamente el valor del array
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
    def obtener_cancion_por_id(id_cancion):
        """Obtener canción por ID"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Cancion WHERE Id = :1"
            cursor.execute(query, (id_cancion,))
            result = cursor.fetchone()
            
            if result:
                return Cancion(
                    id_cancion=result[0],
                    nombre=result[1],
                    duracion=result[2],
                    id_artista=result[3],
                    id_album=result[4],
                    notrack=result[5]
                )
            return None
        except Exception as e:
            print(f"Error al obtener canción: {e}")
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
            
            query = "SELECT * FROM Cancion WHERE id_artista = :1 ORDER BY Nombre"
            cursor.execute(query, (id_artista,))
            results = cursor.fetchall()
            
            canciones = []
            for row in results:
                cancion = Cancion(
                    id_cancion=row[0],
                    nombre=row[1],
                    duracion=row[2],
                    id_artista=row[3],
                    id_album=row[4],
                    notrack=row[5]
                )
                canciones.append(cancion)
            return canciones
        except Exception as e:
            print(f"Error al obtener canciones del artista: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_canciones_por_album(id_album):
        """Obtener todas las canciones de un álbum"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Cancion WHERE id_album = :1 ORDER BY Notrack"
            cursor.execute(query, (id_album,))
            results = cursor.fetchall()
            
            canciones = []
            for row in results:
                cancion = Cancion(
                    id_cancion=row[0],
                    nombre=row[1],
                    duracion=row[2],
                    id_artista=row[3],
                    id_album=row[4],
                    notrack=row[5]
                )
                canciones.append(cancion)
            return canciones
        except Exception as e:
            print(f"Error al obtener canciones del álbum: {e}")
            return []
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
            
            query = """UPDATE Cancion SET Nombre=:1, Duracion=:2, id_artista=:3,
                       id_album=:4, Notrack=:5 WHERE Id=:6"""
            cursor.execute(query, (cancion.nombre, cancion.duracion,
                                   cancion.id_artista, cancion.id_album,
                                   cancion.notrack, cancion.id_cancion))
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
    
    @staticmethod
    def listar_todas_canciones():
        """Listar todas las canciones"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Cancion ORDER BY Nombre"
            cursor.execute(query)
            results = cursor.fetchall()
            
            canciones = []
            for row in results:
                cancion = Cancion(
                    id_cancion=row[0],
                    nombre=row[1],
                    duracion=row[2],
                    id_artista=row[3],
                    id_album=row[4],
                    notrack=row[5]
                )
                canciones.append(cancion)
            return canciones
        except Exception as e:
            print(f"Error al listar canciones: {e}")
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
            
            query = "SELECT * FROM Cancion WHERE LOWER(Nombre) LIKE :1"
            cursor.execute(query, (f"%{nombre.lower()}%",))
            results = cursor.fetchall()
            
            canciones = []
            for row in results:
                cancion = Cancion(
                    id_cancion=row[0],
                    nombre=row[1],
                    duracion=row[2],
                    id_artista=row[3],
                    id_album=row[4],
                    notrack=row[5]
                )
                canciones.append(cancion)
            return canciones
        except Exception as e:
            print(f"Error al buscar canciones: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_canciones_con_detalle():
        """Obtener canciones con información del artista y álbum"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT c.Id, c.Nombre, c.Duracion, p.Nombre as Artista,
                              a.Nombre as Album
                       FROM Cancion c
                       JOIN Persona p ON c.id_artista = p.id_persona
                       LEFT JOIN Album a ON c.id_album = a.Id
                       ORDER BY c.Nombre"""
            cursor.execute(query)
            results = cursor.fetchall()
            
            return results
        except Exception as e:
            print(f"Error al obtener canciones con detalle: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_canciones_sin_album():
        """Obtener canciones que no tienen álbum asignado"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Cancion WHERE id_album IS NULL ORDER BY Nombre"
            cursor.execute(query)
            results = cursor.fetchall()
            
            canciones = []
            for row in results:
                cancion = Cancion(
                    id_cancion=row[0],
                    nombre=row[1],
                    duracion=row[2],
                    id_artista=row[3],
                    id_album=row[4],
                    notrack=row[5]
                )
                canciones.append(cancion)
            return canciones
        except Exception as e:
            print(f"Error al obtener canciones sin álbum: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_duracion_total_artista(id_artista):
        """Obtener duración total de canciones de un artista"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT SUM(Duracion) FROM Cancion WHERE id_artista = :1"
            cursor.execute(query, (id_artista,))
            result = cursor.fetchone()
            
            return result[0] if result[0] else 0
        except Exception as e:
            print(f"Error al obtener duración total: {e}")
            return 0
        finally:
            BaseController.cerrar_recursos(cursor, conexion)