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
            
            query = """INSERT INTO Album (Nombre, id_persona, FechaLanzamiento) 
                       VALUES (:1, :2, :3) RETURNING Id INTO :4"""
            
            id_album = cursor.var(oracledb.NUMBER)
            cursor.execute(query, (album.nombre, album.id_persona, 
                                   album.fecha_lanzamiento, id_album))
            conexion.commit()
            return id_album.getvalue()
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
            
            query = "SELECT * FROM Album WHERE Id = :1"
            cursor.execute(query, (id_album,))
            result = cursor.fetchone()
            
            if result:
                return Album(
                    id_album=result[0],
                    nombre=result[1],
                    id_persona=result[2],
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
            
            query = "SELECT * FROM Album WHERE id_persona = :1 ORDER BY FechaLanzamiento DESC"
            cursor.execute(query, (id_persona,))
            results = cursor.fetchall()
            
            albumes = []
            for row in results:
                album = Album(
                    id_album=row[0],
                    nombre=row[1],
                    id_persona=row[2],
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
            
            query = "DELETE FROM Album WHERE Id = :1"
            cursor.execute(query, (id_album,))
            conexion.commit()
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
            
            query = "SELECT * FROM Album ORDER BY FechaLanzamiento DESC"
            cursor.execute(query)
            results = cursor.fetchall()
            
            albumes = []
            for row in results:
                album = Album(
                    id_album=row[0],
                    nombre=row[1],
                    id_persona=row[2],
                    fecha_lanzamiento=row[3]
                )
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
            
            query = "SELECT * FROM Album WHERE LOWER(Nombre) LIKE :1"
            cursor.execute(query, (f"%{nombre.lower()}%",))
            results = cursor.fetchall()
            
            albumes = []
            for row in results:
                album = Album(
                    id_album=row[0],
                    nombre=row[1],
                    id_persona=row[2],
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
            
            query = "SELECT * FROM Album ORDER BY FechaLanzamiento DESC FETCH FIRST :1 ROWS ONLY"
            cursor.execute(query, (limite,))
            results = cursor.fetchall()
            
            albumes = []
            for row in results:
                album = Album(
                    id_album=row[0],
                    nombre=row[1],
                    id_persona=row[2],
                    fecha_lanzamiento=row[3]
                )
                albumes.append(album)
            return albumes
        except Exception as e:
            print(f"Error al obtener álbumes recientes: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
