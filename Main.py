import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.Conexion import ConexionDB
from views.ventana_login import VentanaLogin

def main():
    db = ConexionDB()
    if not db.conectar():
        print("No se pudo conectar a la base de datos")
        return
    
    app = VentanaLogin()
    app.ejecutar()
    
    db.desconectar()

if __name__ == "__main__":
    main()