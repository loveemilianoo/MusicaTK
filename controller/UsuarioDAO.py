import oracledb
from controller.BaseController import BaseController
from models.Usuario import Usuario

class UsuarioDAO(BaseController):

    @staticmethod
    def crear_usuario(usuario):
        """Insertar nuevo usuario — inserta en Persona y luego en Usuario"""
        conexion = None
        cursor   = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor   = conexion.cursor()

            query_persona = """INSERT INTO Persona
                                   (Nombre, ApellidoPaterno, ApellidoMaterno, FechaDeNacimiento)
                               VALUES (:1, :2, :3, :4)
                               RETURNING id_persona INTO :5"""
            id_var = cursor.var(oracledb.NUMBER)
            cursor.execute(query_persona, (
                usuario.nombre,
                usuario.apellido_paterno,
                usuario.apellido_materno,
                usuario.fecha_nacimiento,
                id_var
            ))
            id_val = id_var.getvalue()
            if isinstance(id_val, (list, tuple)):
                id_val = id_val[0]

            query_usuario = """INSERT INTO Usuario (id_persona, Telefono, Contrasena)
                               VALUES (:1, :2, :3)"""
            cursor.execute(query_usuario, (id_val, usuario.telefono, usuario.contrasena))

            conexion.commit()
            print(f"✓ Usuario creado con ID: {id_val}")
            return id_val
        except Exception as e:
            if conexion: conexion.rollback()
            print(f"✗ Error al crear usuario: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def verificar_usuario(nombre, apellido_paterno, apellido_materno, fecha_nacimiento):
        """
        Login de usuario — verifica por nombre + apellidos + fecha de nacimiento.
        Devuelve objeto Usuario si existe en tabla Usuario, None si no.
        """
        conexion = None
        cursor   = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor   = conexion.cursor()

            query = """SELECT p.id_persona, p.Nombre, p.ApellidoPaterno,
                              p.ApellidoMaterno, p.FechaDeNacimiento,
                              u.Telefono, u.Contrasena
                       FROM Persona p
                       JOIN Usuario u ON p.id_persona = u.id_persona
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
                return Usuario(
                    id_persona       = row[0],
                    nombre           = row[1],
                    apellido_paterno = row[2],
                    apellido_materno = row[3],
                    fecha_nacimiento = row[4],
                    telefono         = row[5],
                    contrasena       = row[6]
                )
            return None
        except Exception as e:
            print(f"Error al verificar usuario: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def buscar_persona(nombre, apellido_paterno, apellido_materno, fecha_nacimiento):
        """
        Busca solo en Persona sin importar si es Usuario o Artista.
        Útil para la pantalla de selección de rol.
        """
        conexion = None
        cursor   = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor   = conexion.cursor()

            query = """SELECT id_persona, Nombre, ApellidoPaterno,
                              ApellidoMaterno, FechaDeNacimiento
                       FROM Persona
                       WHERE LOWER(Nombre)          = LOWER(:1)
                         AND LOWER(ApellidoPaterno) = LOWER(:2)
                         AND LOWER(NVL(ApellidoMaterno, '')) = LOWER(NVL(:3, ''))
                         AND TRUNC(FechaDeNacimiento) = TRUNC(TO_DATE(:4, 'YYYY-MM-DD'))"""
            cursor.execute(query, (
                nombre, apellido_paterno,
                apellido_materno or '', fecha_nacimiento
            ))
            row = cursor.fetchone()

            if row:
                from models.Persona import Persona
                return Persona(
                    id_persona       = row[0],
                    nombre           = row[1],
                    apellido_paterno = row[2],
                    apellido_materno = row[3],
                    fecha_nacimiento = row[4]
                )
            return None
        except Exception as e:
            print(f"Error al buscar persona: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)

    @staticmethod
    def obtener_usuario_por_id(id_persona):
        conexion = None
        cursor   = None
        try:
            conexion = BaseController.obtener_conexion()
            cursor   = conexion.cursor()
            query = """SELECT p.id_persona, p.Nombre, p.ApellidoPaterno,
                              p.ApellidoMaterno, p.FechaDeNacimiento,
                              u.Telefono, u.Contrasena
                       FROM Persona p
                       JOIN Usuario u ON p.id_persona = u.id_persona
                       WHERE p.id_persona = :1"""
            cursor.execute(query, (id_persona,))
            row = cursor.fetchone()
            if row:
                return Usuario(
                    id_persona       = row[0],
                    nombre           = row[1],
                    apellido_paterno = row[2],
                    apellido_materno = row[3],
                    fecha_nacimiento = row[4],
                    telefono         = row[5],
                    contrasena       = row[6]
                )
            return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            BaseController.cerrar_recursos(cursor, conexion)