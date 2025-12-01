import pymssql
import os

class ConexionBD:
    def __init__(self):
        self.conexion = None
        self.server = os.getenv('DB_SERVER', 'localhost')
        self.port = int(os.getenv('DB_PORT', '1433'))
        self.database = os.getenv('DB_NAME', 'Biblioteca')
        self.username = os.getenv('DB_USER', 'sa')
        self.password = os.getenv('DB_PASSWORD', 'BibliotecaPass123!')
    
    def establecerConexionBD(self):
        """Establece la conexión con la base de datos"""
        try:
            self.conexion = pymssql.connect(
                server=self.server,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print("✓ Conexión a BD establecida")
            return True
        except Exception as e:
            print(f"✗ Error al conectar a BD: {e}")
            self.conexion = None
            return False
    
    def cerrarConexion(self):
        """Cierra la conexión con la base de datos"""
        try:
            if self.conexion:
                self.conexion.close()
                print("✓ Conexión a BD cerrada")
        except Exception as e:
            print(f"✗ Error al cerrar conexión: {e}")
    
    def ejecutarConsulta(self, query, params=None):
        """Ejecuta una consulta SELECT y retorna los resultados"""
        try:
            self.establecerConexionBD()
            cursor = self.conexion.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            resultados = cursor.fetchall()
            cursor.close()
            self.cerrarConexion()
            return resultados
        except Exception as e:
            print(f"✗ Error ejecutando consulta: {e}")
            self.cerrarConexion()
            return []
    
    def ejecutarComando(self, query, params=None):
        """Ejecuta un comando INSERT, UPDATE o DELETE"""
        try:
            self.establecerConexionBD()
            cursor = self.conexion.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.conexion.commit()
            cursor.close()
            self.cerrarConexion()
            return True
        except Exception as e:
            print(f"✗ Error ejecutando comando: {e}")
            if self.conexion:
                self.conexion.rollback()
            self.cerrarConexion()
            return False