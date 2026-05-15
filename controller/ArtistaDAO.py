import oracledb
from controller.BaseController import BaseController
from models.Artista import Artista

class ArtistaDAO(BaseController):
    
    @staticmethod
    def crear_artista(artista):
        """Insertar un nuevo artista"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            # Primero insertar en Persona
            query_persona = """INSERT INTO Persona (Nombre, Apellido, Correo, Sexo, Edad) 
                               VALUES (:1, :2, :3, :4, :5) RETURNING id_persona INTO :6"""
            
            id_persona = cursor.var(oracledb.NUMBER)
            cursor.execute(query_persona, (artista.nombre, artista.apellido, 
                                          artista.correo, artista.sexo, 
                                          artista.edad, id_persona))
            
            id_persona_value = id_persona.getvalue()
            
            # Luego insertar en Artista
            query_artista = """INSERT INTO Artista (id_persona, Banda, Disquera) 
                              VALUES (:1, :2, :3)"""
            cursor.execute(query_artista, (id_persona_value, artista.banda, artista.disquera))
            
            conexion.commit()
            return id_persona_value
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al crear artista: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_artista_por_id(id_persona):
        """Obtener artista por ID"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              a.Banda, a.Disquera
                       FROM Persona p
                       JOIN Artista a ON p.id_persona = a.id_persona
                       WHERE p.id_persona = :1"""
            cursor.execute(query, (id_persona,))
            result = cursor.fetchone()
            
            if result:
                return Artista(
                    id_persona=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    correo=result[3],
                    sexo=result[4],
                    edad=result[5],
                    banda=result[6],
                    disquera=result[7]
                )
            return None
        except Exception as e:
            print(f"Error al obtener artista: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_artista_por_nombre(nombre):
        """Obtener artista por nombre"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              a.Banda, a.Disquera
                       FROM Persona p
                       JOIN Artista a ON p.id_persona = a.id_persona
                       WHERE LOWER(p.Nombre) = :1"""
            cursor.execute(query, (nombre.lower(),))
            result = cursor.fetchone()
            
            if result:
                return Artista(
                    id_persona=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    correo=result[3],
                    sexo=result[4],
                    edad=result[5],
                    banda=result[6],
                    disquera=result[7]
                )
            return None
        except Exception as e:
            print(f"Error al obtener artista por nombre: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def listar_todos_artistas():
        """Listar todos los artistas"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              a.Banda, a.Disquera
                       FROM Persona p
                       JOIN Artista a ON p.id_persona = a.id_persona
                       ORDER BY p.Nombre"""
            cursor.execute(query)
            results = cursor.fetchall()
            
            artistas = []
            for row in results:
                artista = Artista(
                    id_persona=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    correo=row[3],
                    sexo=row[4],
                    edad=row[5],
                    banda=row[6],
                    disquera=row[7]
                )
                artistas.append(artista)
            return artistas
        except Exception as e:
            print(f"Error al listar artistas: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def listar_bandas():
        """Listar todas las bandas"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              a.Banda, a.Disquera
                       FROM Persona p
                       JOIN Artista a ON p.id_persona = a.id_persona
                       WHERE a.Banda = 1
                       ORDER BY p.Nombre"""
            cursor.execute(query)
            results = cursor.fetchall()
            
            bandas = []
            for row in results:
                banda = Artista(
                    id_persona=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    correo=row[3],
                    sexo=row[4],
                    edad=row[5],
                    banda=row[6],
                    disquera=row[7]
                )
                bandas.append(banda)
            return bandas
        except Exception as e:
            print(f"Error al listar bandas: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def listar_solistas():
        """Listar todos los solistas"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              a.Banda, a.Disquera
                       FROM Persona p
                       JOIN Artista a ON p.id_persona = a.id_persona
                       WHERE a.Banda = 0
                       ORDER BY p.Nombre"""
            cursor.execute(query)
            results = cursor.fetchall()
            
            solistas = []
            for row in results:
                solista = Artista(
                    id_persona=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    correo=row[3],
                    sexo=row[4],
                    edad=row[5],
                    banda=row[6],
                    disquera=row[7]
                )
                solistas.append(solista)
            return solistas
        except Exception as e:
            print(f"Error al listar solistas: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def actualizar_artista(artista):
        """Actualizar artista existente"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            # Actualizar Persona
            query_persona = """UPDATE Persona SET Nombre=:1, Apellido=:2, Correo=:3, 
                              Sexo=:4, Edad=:5 WHERE id_persona=:6"""
            cursor.execute(query_persona, (artista.nombre, artista.apellido,
                                          artista.correo, artista.sexo,
                                          artista.edad, artista.id_persona))
            
            # Actualizar Artista
            query_artista = """UPDATE Artista SET Banda=:1, Disquera=:2 
                              WHERE id_persona=:3"""
            cursor.execute(query_artista, (artista.banda, artista.disquera, artista.id_persona))
            
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al actualizar artista: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def eliminar_artista(id_persona):
        """Eliminar artista (cascade elimina de Artista primero, luego Persona)"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            # Primero eliminar en Artista
            query_artista = "DELETE FROM Artista WHERE id_persona = :1"
            cursor.execute(query_artista, (id_persona,))
            
            # Luego eliminar en Persona
            query_persona = "DELETE FROM Persona WHERE id_persona = :1"
            cursor.execute(query_persona, (id_persona,))
            
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al eliminar artista: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def listar_por_disquera(disquera):
        """Listar artistas de una disquera específica"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              a.Banda, a.Disquera
                       FROM Persona p
                       JOIN Artista a ON p.id_persona = a.id_persona
                       WHERE LOWER(a.Disquera) = :1
                       ORDER BY p.Nombre"""
            cursor.execute(query, (disquera.lower(),))
            results = cursor.fetchall()
            
            artistas = []
            for row in results:
                artista = Artista(
                    id_persona=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    correo=row[3],
                    sexo=row[4],
                    edad=row[5],
                    banda=row[6],
                    disquera=row[7]
                )
                artistas.append(artista)
            return artistas
        except Exception as e:
            print(f"Error al listar artistas por disquera: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
