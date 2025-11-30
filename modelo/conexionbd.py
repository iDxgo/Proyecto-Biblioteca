import pyodbc 

class ConexionBD:
    def __init__(self):
        self.conexion = ''
        
    def establecerConexionBD(self):
        try: 
            self.conexion = pyodbc.connect("DRIVER={SQL Server};"
            "SERVER=DAGO_VICTUS;"
            "DATABASE=Biblioteca;"  # Reemplaza con tu base de datos
            "Trusted_Connection=yes;")
            print("Conexion Establecida")
            
        except Exception as ex:
            print("No se pudo establecer la conexion")
            print("Error",ex)
            
    def cerrarConexion(self):
        self.conexion.close()