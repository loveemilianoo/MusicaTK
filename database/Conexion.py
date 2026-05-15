import oracledb
import os

class ConexionDB:
    _instancia = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.conexion = None
        return cls._instancia
    
    def conectar(self):
        """Conectar a Oracle"""
        try:
            # Configura según tu Oracle
            dsn = oracledb.makedsn("144.24.50.227", 1521, service_name="BASEORACPDB1")
            self.conexion = oracledb.connect(
                user="SYSTEM",
                password="oracle1",
                dsn=dsn
            )
            print("Conectado a Oracle")
            return self.conexion
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None
    
    def desconectar(self):
        if self.conexion:
            self.conexion.close()
            print("Desconectado")
    
    def ejecutar_consulta(self, query, params=None):
        """Ejecutar SELECT"""
        cursor = self.conexion.cursor()
        cursor.execute(query, params or {})
        return cursor.fetchall()
    
    def ejecutar_insert(self, query, params=None):
        """Ejecutar INSERT, UPDATE, DELETE"""
        cursor = self.conexion.cursor()
        cursor.execute(query, params or {})
        self.conexion.commit()
        return cursor.lastrowid if hasattr(cursor, 'lastrowid') else None
    
