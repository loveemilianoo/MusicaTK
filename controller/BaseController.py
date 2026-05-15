from database.Conexion import ConexionDB

class BaseController:
    @staticmethod
    def obtener_conexion():
        db = ConexionDB()
        db.conectar()
        return db.conexion
    
    @staticmethod
    def cerrar_recursos(cursor=None, conexion=None):
        try:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        except Exception as e:
            print(f"Error al cerrar recursos: {e}")