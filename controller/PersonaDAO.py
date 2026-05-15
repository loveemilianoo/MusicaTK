import oracledb
from controller.PersonaDAO import BaseController
from models.Persona import Persona

class PersonaController(BaseController):
    
    @staticmethod
    def crear_persona(persona):
        """Insertar una nueva persona"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """INSERT INTO Persona (Nombre, Apellido, Correo, Sexo, Edad) 
                       VALUES (:1, :2, :3, :4, :5) RETURNING id_persona INTO :6"""
            
            # Parámetro para el RETURNING
            id_persona = cursor.var(oracledb.NUMBER)
            cursor.execute(query, (persona.nombre, persona.apellido, 
                                   persona.correo, persona.sexo, 
                                   persona.edad, id_persona))
            conexion.commit()
            return id_persona.getvalue()
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
            
            query = "SELECT * FROM Persona WHERE id_persona = :1"
            cursor.execute(query, (id_persona,))
            result = cursor.fetchone()
            
            if result:
                return Persona(
                    id_persona=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    correo=result[3],
                    sexo=result[4],
                    edad=result[5]
                )
            return None
        except Exception as e:
            print(f"Error al obtener persona: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_persona_por_correo(correo):
        """Obtener persona por correo"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "SELECT * FROM Persona WHERE Correo = :1"
            cursor.execute(query, (correo,))
            result = cursor.fetchone()
            
            if result:
                return Persona(
                    id_persona=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    correo=result[3],
                    sexo=result[4],
                    edad=result[5]
                )
            return None
        except Exception as e:
            print(f"Error al obtener persona por correo: {e}")
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
            
            query = """UPDATE Persona SET Nombre=:1, Apellido=:2, Correo=:3, 
                       Sexo=:4, Edad=:5 WHERE id_persona=:6"""
            cursor.execute(query, (persona.nombre, persona.apellido,
                                   persona.correo, persona.sexo,
                                   persona.edad, persona.id_persona))
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
            
            query = "SELECT * FROM Persona ORDER BY Nombre"
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            personas = []
            for row in resultados:
                persona = Persona(
                    id_persona=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    correo=row[3],
                    sexo=row[4],
                    edad=row[5]
                )
                personas.append(persona)
            return personas
        except Exception as e:
            print(f"Error al listar personas: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)