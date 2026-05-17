import oracledb
from controller.BaseController import BaseController
from models.Genero import Genero

class GeneroDAO(BaseController):
    
    @staticmethod
    def crear_genero(genero):
        """Insertar un nuevo género"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "INSERT INTO Genero (Nombre) VALUES (:1) RETURNING Id INTO :2"
            
            id_genero = cursor.var(oracledb.NUMBER)
            cursor.execute(query, (genero.nombre, id_genero))
            
            # Extraer correctamente el valor del array
            id_value = id_genero.getvalue()
            if isinstance(id_value, (list, tuple)):
                id_value = id_value[0]
            
            print(f"✓ Género '{genero.nombre}' creado con ID: {id_value}")
            conexion.commit()
            return id_value
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al crear género: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_genero_por_id(id_genero):
        """Obtener género por ID"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Genero WHERE Id = :1"
            cursor.execute(query, (id_genero,))
            result = cursor.fetchone()
            
            if result:
                return Genero(
                    id_genero=result[0],
                    nombre=result[1]
                )
            return None
        except Exception as e:
            print(f"Error al obtener género: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_genero_por_nombre(nombre):
        """Obtener género por nombre"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Genero WHERE LOWER(Nombre) = :1"
            cursor.execute(query, (nombre.lower(),))
            result = cursor.fetchone()
            
            if result:
                return Genero(
                    id_genero=result[0],
                    nombre=result[1]
                )
            return None
        except Exception as e:
            print(f"Error al obtener género por nombre: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def listar_todos_generos():
        """Listar todos los géneros"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Genero ORDER BY Nombre"
            cursor.execute(query)
            results = cursor.fetchall()
            
            generos = []
            for row in results:
                genero = Genero(
                    id_genero=row[0],
                    nombre=row[1]
                )
                generos.append(genero)
            return generos
        except Exception as e:
            print(f"Error al listar géneros: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def actualizar_genero(genero):
        """Actualizar género existente"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "UPDATE Genero SET Nombre=:1 WHERE Id=:2"
            cursor.execute(query, (genero.nombre, genero.id_genero))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al actualizar género: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def eliminar_genero(id_genero):
        """Eliminar género"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "DELETE FROM Genero WHERE Id = :1"
            cursor.execute(query, (id_genero,))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al eliminar género: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def buscar_genero_por_nombre(nombre):
        """Buscar géneros por nombre (parcial)"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Genero WHERE LOWER(Nombre) LIKE :1 ORDER BY Nombre"
            cursor.execute(query, (f"%{nombre.lower()}%",))
            results = cursor.fetchall()
            
            generos = []
            for row in results:
                genero = Genero(
                    id_genero=row[0],
                    nombre=row[1]
                )
                generos.append(genero)
            return generos
        except Exception as e:
            print(f"Error al buscar géneros: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def agregar_genero_a_cancion(id_cancion, id_genero):
        """Asociar un género a una canción"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "INSERT INTO Cancion_Genero (id_cancion, id_genero) VALUES (:1, :2)"
            cursor.execute(query, (id_cancion, id_genero))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al agregar género a canción: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def quitar_genero_de_cancion(id_cancion, id_genero):
        """Desasociar un género de una canción"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "DELETE FROM Cancion_Genero WHERE id_cancion = :1 AND id_genero = :2"
            cursor.execute(query, (id_cancion, id_genero))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al quitar género de canción: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_canciones_por_genero(id_genero):
        """Obtener todas las canciones de un género"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT c.Id, c.Nombre, c.Duracion, p.Nombre as Artista
                       FROM Cancion_Genero cg
                       JOIN Cancion c ON cg.id_cancion = c.Id
                       JOIN Persona p ON c.id_artista = p.id_persona
                       WHERE cg.id_genero = :1
                       ORDER BY c.Nombre"""
            cursor.execute(query, (id_genero,))
            results = cursor.fetchall()
            
            return results
        except Exception as e:
            print(f"Error al obtener canciones por género: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_generos_por_cancion(id_cancion):
        """Obtener todos los géneros de una canción"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT g.Id, g.Nombre
                       FROM Cancion_Genero cg
                       JOIN Genero g ON cg.id_genero = g.Id
                       WHERE cg.id_cancion = :1
                       ORDER BY g.Nombre"""
            cursor.execute(query, (id_cancion,))
            results = cursor.fetchall()
            
            generos = []
            for row in results:
                genero = Genero(
                    id_genero=row[0],
                    nombre=row[1]
                )
                generos.append(genero)
            return generos
        except Exception as e:
            print(f"Error al obtener géneros de canción: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def contar_canciones_por_genero(id_genero):
        """Obtener cantidad de canciones de un género"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT COUNT(*) FROM Cancion_Genero WHERE id_genero = :1"
            cursor.execute(query, (id_genero,))
            result = cursor.fetchone()
            
            return result[0] if result[0] else 0
        except Exception as e:
            print(f"Error al contar canciones: {e}")
            return 0
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_generos_populares(limite=10):
        """Obtener géneros más populares (con más canciones)"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT g.Id, g.Nombre, COUNT(cg.id_cancion) as TotalCanciones
                       FROM Genero g
                       LEFT JOIN Cancion_Genero cg ON g.Id = cg.id_genero
                       GROUP BY g.Id, g.Nombre
                       ORDER BY TotalCanciones DESC
                       FETCH FIRST :1 ROWS ONLY"""
            cursor.execute(query, (limite,))
            results = cursor.fetchall()
            
            return results
        except Exception as e:
            print(f"Error al obtener géneros populares: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
