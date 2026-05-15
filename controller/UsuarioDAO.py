import oracledb
from controller.BaseController import BaseController
from models.Usuario import Usuario

class UsuarioDAO(BaseController):
    
    @staticmethod
    def crear_usuario(usuario):
        """Insertar un nuevo usuario"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            # Primero insertar en Persona
            query_persona = """INSERT INTO Persona (Nombre, Apellido, Correo, Sexo, Edad) 
                               VALUES (:1, :2, :3, :4, :5) RETURNING id_persona INTO :6"""
            
            id_persona = cursor.var(oracledb.NUMBER)
            cursor.execute(query_persona, (usuario.nombre, usuario.apellido, 
                                          usuario.correo, usuario.sexo, 
                                          usuario.edad, id_persona))
            
            id_persona_value = id_persona.getvalue()
            
            # Luego insertar en Usuario
            query_usuario = """INSERT INTO Usuario (id_persona, Telefono, Membresia, Contrasena) 
                              VALUES (:1, :2, :3, :4)"""
            cursor.execute(query_usuario, (id_persona_value, usuario.telefono, 
                                          usuario.membresia, usuario.contrasena))
            
            conexion.commit()
            return id_persona_value
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al crear usuario: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_usuario_por_id(id_persona):
        """Obtener usuario por ID"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              u.Telefono, u.Membresia, u.Contrasena
                       FROM Persona p
                       JOIN Usuario u ON p.id_persona = u.id_persona
                       WHERE p.id_persona = :1"""
            cursor.execute(query, (id_persona,))
            result = cursor.fetchone()
            
            if result:
                return Usuario(
                    id_persona=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    correo=result[3],
                    sexo=result[4],
                    edad=result[5],
                    telefono=result[6],
                    membresia=result[7],
                    contrasena=result[8]
                )
            return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_usuario_por_correo(correo):
        """Obtener usuario por correo"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              u.Telefono, u.Membresia, u.Contrasena
                       FROM Persona p
                       JOIN Usuario u ON p.id_persona = u.id_persona
                       WHERE LOWER(p.Correo) = :1"""
            cursor.execute(query, (correo.lower(),))
            result = cursor.fetchone()
            
            if result:
                return Usuario(
                    id_persona=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    correo=result[3],
                    sexo=result[4],
                    edad=result[5],
                    telefono=result[6],
                    membresia=result[7],
                    contrasena=result[8]
                )
            return None
        except Exception as e:
            print(f"Error al obtener usuario por correo: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def verificar_credenciales(correo, contrasena):
        """Verificar credenciales de usuario (login)"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              u.Telefono, u.Membresia, u.Contrasena
                       FROM Persona p
                       JOIN Usuario u ON p.id_persona = u.id_persona
                       WHERE LOWER(p.Correo) = :1 AND u.Contrasena = :2"""
            cursor.execute(query, (correo.lower(), contrasena))
            result = cursor.fetchone()
            
            if result:
                return Usuario(
                    id_persona=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    correo=result[3],
                    sexo=result[4],
                    edad=result[5],
                    telefono=result[6],
                    membresia=result[7],
                    contrasena=result[8]
                )
            return None
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def listar_todos_usuarios():
        """Listar todos los usuarios"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              u.Telefono, u.Membresia, u.Contrasena
                       FROM Persona p
                       JOIN Usuario u ON p.id_persona = u.id_persona
                       ORDER BY p.Nombre"""
            cursor.execute(query)
            results = cursor.fetchall()
            
            usuarios = []
            for row in results:
                usuario = Usuario(
                    id_persona=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    correo=row[3],
                    sexo=row[4],
                    edad=row[5],
                    telefono=row[6],
                    membresia=row[7],
                    contrasena=row[8]
                )
                usuarios.append(usuario)
            return usuarios
        except Exception as e:
            print(f"Error al listar usuarios: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def actualizar_usuario(usuario):
        """Actualizar usuario existente"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            # Actualizar Persona
            query_persona = """UPDATE Persona SET Nombre=:1, Apellido=:2, Correo=:3, 
                              Sexo=:4, Edad=:5 WHERE id_persona=:6"""
            cursor.execute(query_persona, (usuario.nombre, usuario.apellido,
                                          usuario.correo, usuario.sexo,
                                          usuario.edad, usuario.id_persona))
            
            # Actualizar Usuario
            query_usuario = """UPDATE Usuario SET Telefono=:1, Membresia=:2, Contrasena=:3 
                              WHERE id_persona=:4"""
            cursor.execute(query_usuario, (usuario.telefono, usuario.membresia, 
                                          usuario.contrasena, usuario.id_persona))
            
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def eliminar_usuario(id_persona):
        """Eliminar usuario (cascade elimina de Usuario primero, luego Persona)"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            # Primero eliminar en Usuario
            query_usuario = "DELETE FROM Usuario WHERE id_persona = :1"
            cursor.execute(query_usuario, (id_persona,))
            
            # Luego eliminar en Persona
            query_persona = "DELETE FROM Persona WHERE id_persona = :1"
            cursor.execute(query_persona, (id_persona,))
            
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al eliminar usuario: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def buscar_usuario_por_nombre(nombre):
        """Buscar usuarios por nombre"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              u.Telefono, u.Membresia, u.Contrasena
                       FROM Persona p
                       JOIN Usuario u ON p.id_persona = u.id_persona
                       WHERE LOWER(p.Nombre) LIKE :1 OR LOWER(p.Apellido) LIKE :1
                       ORDER BY p.Nombre"""
            cursor.execute(query, (f"%{nombre.lower()}%",))
            results = cursor.fetchall()
            
            usuarios = []
            for row in results:
                usuario = Usuario(
                    id_persona=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    correo=row[3],
                    sexo=row[4],
                    edad=row[5],
                    telefono=row[6],
                    membresia=row[7],
                    contrasena=row[8]
                )
                usuarios.append(usuario)
            return usuarios
        except Exception as e:
            print(f"Error al buscar usuarios: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def listar_usuarios_por_membresia(membresia):
        """Listar usuarios de una membresía específica"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.id_persona, p.Nombre, p.Apellido, p.Correo, p.Sexo, p.Edad,
                              u.Telefono, u.Membresia, u.Contrasena
                       FROM Persona p
                       JOIN Usuario u ON p.id_persona = u.id_persona
                       WHERE LOWER(u.Membresia) = :1
                       ORDER BY p.Nombre"""
            cursor.execute(query, (membresia.lower(),))
            results = cursor.fetchall()
            
            usuarios = []
            for row in results:
                usuario = Usuario(
                    id_persona=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    correo=row[3],
                    sexo=row[4],
                    edad=row[5],
                    telefono=row[6],
                    membresia=row[7],
                    contrasena=row[8]
                )
                usuarios.append(usuario)
            return usuarios
        except Exception as e:
            print(f"Error al listar usuarios por membresía: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def contar_usuarios_por_membresia():
        """Obtener cantidad de usuarios por cada tipo de membresía"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT u.Membresia, COUNT(*) as Total
                       FROM Usuario u
                       GROUP BY u.Membresia"""
            cursor.execute(query)
            results = cursor.fetchall()
            
            return results
        except Exception as e:
            print(f"Error al contar usuarios por membresía: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def cambiar_contrasena(id_persona, contrasena_nueva):
        """Cambiar contraseña de un usuario"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "UPDATE Usuario SET Contrasena=:1 WHERE id_persona=:2"
            cursor.execute(query, (contrasena_nueva, id_persona))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al cambiar contraseña: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def cambiar_membresia(id_persona, nueva_membresia):
        """Cambiar membresía de un usuario"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = "UPDATE Usuario SET Membresia=:1 WHERE id_persona=:2"
            cursor.execute(query, (nueva_membresia, id_persona))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al cambiar membresía: {e}")
            return False
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
    
    @staticmethod
    def obtener_playlists_usuario(id_persona):
        """Obtener playlists de un usuario"""
        conexion = None
        cursor = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor = conexion.cursor()
            
            query = """SELECT p.Id, p.Nombre, p.FechaCreacion, COUNT(cp.id_cancion) as TotalCanciones
                       FROM Playlist p
                       LEFT JOIN Cancion_Playlist cp ON p.Id = cp.id_playlist
                       WHERE p.id_persona = :1
                       GROUP BY p.Id, p.Nombre, p.FechaCreacion
                       ORDER BY p.FechaCreacion DESC"""
            cursor.execute(query, (id_persona,))
            results = cursor.fetchall()
            
            return results
        except Exception as e:
            print(f"Error al obtener playlists del usuario: {e}")
            return []
        finally:
            BaseController.cerrar_recursos(cursor, conexion)
