import oracledb
from controller.BaseController import BaseController
from models.Playlist import Playlist
from datetime import date

class PlaylistDAO(BaseController):
    
    @staticmethod
    def crear_playlist(playlist):
        """Insertar una nueva playlist"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """INSERT INTO Playlist (Nombre, id_persona, FechaCreacion) 
                       VALUES (:1, :2, :3) RETURNING Id INTO :4"""
            
            id_playlist = cursor.var(oracledb.NUMBER)
            cursor.execute(query, (playlist.nombre, playlist.id_persona, 
                                   playlist.fecha_creacion, id_playlist))
            
            # Extraer correctamente el valor del array
            id_value = id_playlist.getvalue()
            if isinstance(id_value, (list, tuple)):
                id_value = id_value[0]
            
            print(f"✓ Playlist '{playlist.nombre}' creada con ID: {id_value}")
            conexion.commit()
            return id_value
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"✗ Error al crear playlist: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_playlist_por_id(id_playlist):
        """Obtener playlist por ID"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Playlist WHERE Id = :1"
            cursor.execute(query, (id_playlist,))
            result = cursor.fetchone()
            
            if result:
                return Playlist(
                    id_playlist=result[0],
                    nombre=result[1],
                    id_persona=result[2],
                    fecha_creacion=result[3]
                )
            return None
        except Exception as e:
            print(f"Error al obtener playlist: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_playlists_por_usuario(id_persona):
        """Obtener todas las playlists de un usuario"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Playlist WHERE id_persona = :1 ORDER BY FechaCreacion DESC"
            cursor.execute(query, (id_persona,))
            results = cursor.fetchall()
            
            playlists = []
            for row in results:
                playlist = Playlist(
                    id_playlist=row[0],
                    nombre=row[1],
                    id_persona=row[2],
                    fecha_creacion=row[3]
                )
                playlists.append(playlist)
            return playlists
        except Exception as e:
            print(f"Error al obtener playlists del usuario: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def actualizar_playlist(playlist):
        """Actualizar playlist existente"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "UPDATE Playlist SET Nombre=:1, id_persona=:2, FechaCreacion=:3 WHERE Id=:4"
            cursor.execute(query, (playlist.nombre, playlist.id_persona,
                                   playlist.fecha_creacion, playlist.id_playlist))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al actualizar playlist: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def eliminar_playlist(id_playlist):
        """Eliminar playlist"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "DELETE FROM Playlist WHERE Id = :1"
            cursor.execute(query, (id_playlist,))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al eliminar playlist: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def listar_todas_playlists():
        """Listar todas las playlists"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Playlist ORDER BY FechaCreacion DESC"
            cursor.execute(query)
            results = cursor.fetchall()
            
            playlists = []
            for row in results:
                playlist = Playlist(
                    id_playlist=row[0],
                    nombre=row[1],
                    id_persona=row[2],
                    fecha_creacion=row[3]
                )
                playlists.append(playlist)
            return playlists
        except Exception as e:
            print(f"Error al listar playlists: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def buscar_playlist_por_nombre(nombre):
        """Buscar playlists por nombre"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Playlist WHERE LOWER(Nombre) LIKE :1 ORDER BY Nombre"
            cursor.execute(query, (f"%{nombre.lower()}%",))
            results = cursor.fetchall()
            
            playlists = []
            for row in results:
                playlist = Playlist(
                    id_playlist=row[0],
                    nombre=row[1],
                    id_persona=row[2],
                    fecha_creacion=row[3]
                )
                playlists.append(playlist)
            return playlists
        except Exception as e:
            print(f"Error al buscar playlists: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def agregar_cancion_a_playlist(id_cancion, id_playlist):
        """Agregar una canción a la playlist"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "INSERT INTO Cancion_Playlist (id_cancion, id_playlist) VALUES (:1, :2)"
            cursor.execute(query, (id_cancion, id_playlist))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al agregar canción a playlist: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def quitar_cancion_de_playlist(id_cancion, id_playlist):
        """Quitar una canción de la playlist"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "DELETE FROM Cancion_Playlist WHERE id_cancion = :1 AND id_playlist = :2"
            cursor.execute(query, (id_cancion, id_playlist))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al quitar canción de playlist: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_canciones_playlist(id_playlist):
        """Obtener todas las canciones de una playlist"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT c.Id, c.Nombre, c.Duracion, pe.Nombre as Artista
                       FROM Cancion_Playlist cp
                       JOIN Cancion c ON cp.id_cancion = c.Id
                       LEFT JOIN Persona pe ON c.id_artista = pe.id_persona
                       WHERE cp.id_playlist = :1"""
            cursor.execute(query, (id_playlist,))
            results = cursor.fetchall()
            
            return results
        except Exception as e:
            print(f"Error al obtener canciones de playlist: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def contar_canciones_playlist(id_playlist):
        """Obtener cantidad de canciones en una playlist"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT COUNT(*) FROM Cancion_Playlist WHERE id_playlist = :1"
            cursor.execute(query, (id_playlist,))
            result = cursor.fetchone()
            
            return result[0] if result[0] else 0
        except Exception as e:
            print(f"Error al contar canciones: {e}")
            return 0
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_duracion_total_playlist(id_playlist):
        """Obtener duración total de una playlist"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT SUM(c.Duracion) 
                       FROM Cancion_Playlist cp
                       JOIN Cancion c ON cp.id_cancion = c.Id
                       WHERE cp.id_playlist = :1"""
            cursor.execute(query, (id_playlist,))
            result = cursor.fetchone()
            
            return result[0] if result[0] else 0
        except Exception as e:
            print(f"Error al obtener duración total: {e}")
            return 0
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_playlists_con_detalle():
        """Obtener playlists con información del usuario"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.Id, p.Nombre, p.FechaCreacion, pe.Nombre as Usuario,
                              COUNT(cp.id_cancion) as TotalCanciones
                       FROM Playlist p
                       JOIN Persona pe ON p.id_persona = pe.id_persona
                       LEFT JOIN Cancion_Playlist cp ON p.Id = cp.id_playlist
                       GROUP BY p.Id, p.Nombre, p.FechaCreacion, pe.Nombre
                       ORDER BY p.FechaCreacion DESC"""
            cursor.execute(query)
            results = cursor.fetchall()
            
            return results
        except Exception as e:
            print(f"Error al obtener playlists con detalle: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_playlists_populares(limite=10):
        """Obtener playlists más populares (con más canciones)"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.Id, p.Nombre, p.FechaCreacion, pe.Nombre as Usuario,
                              COUNT(cp.id_cancion) as TotalCanciones
                       FROM Playlist p
                       JOIN Persona pe ON p.id_persona = pe.id_persona
                       LEFT JOIN Cancion_Playlist cp ON p.Id = cp.id_playlist
                       GROUP BY p.Id, p.Nombre, p.FechaCreacion, pe.Nombre
                       ORDER BY TotalCanciones DESC
                       FETCH FIRST :1 ROWS ONLY"""
            cursor.execute(query, (limite,))
            results = cursor.fetchall()
            
            return results
        except Exception as e:
            print(f"Error al obtener playlists populares: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)