from modelo.conexionbd import ConexionBD
from modelo.multa import Multa

class MultaDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.multa = Multa()
        
    def listarMultas(self):
        """Lista todas las multas"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            cursor.execute("EXEC sp_ListarMultas")
            filas = cursor.fetchall()
            cursor.close()
            self.bd.cerrarConexion()
            return filas
        except Exception as e:
            print(f"✗ Error listando multas: {e}")
            self.bd.cerrarConexion()
            return []
            
    def insertarMulta(self):
        """Inserta una nueva multa"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            cursor.execute(
                "EXEC sp_CrearMulta %s, %s, %s, %s, %s",
                (self.multa.prestamo_id, self.multa.usuario_id, 
                 self.multa.monto, self.multa.fecha_multa, self.multa.estado)
            )
            self.bd.conexion.commit()
            cursor.close()
            self.bd.cerrarConexion()
            print("✓ Multa insertada")
            return True
        except Exception as e:
            print(f"✗ Error insertando multa: {e}")
            if self.bd.conexion:
                self.bd.conexion.rollback()
            self.bd.cerrarConexion()
            return False
        
    def actualizarMulta(self):
        """Actualiza una multa existente"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            cursor.execute(
                "EXEC sp_ActualizarMulta %s, %s, %s, %s, %s, %s",
                (self.multa.multa_id, self.multa.prestamo_id, 
                 self.multa.usuario_id, self.multa.monto, 
                 self.multa.fecha_multa, self.multa.estado)
            )
            self.bd.conexion.commit()
            cursor.close()
            self.bd.cerrarConexion()
            print("✓ Multa actualizada")
            return True
        except Exception as e:
            print(f"✗ Error actualizando multa: {e}")
            if self.bd.conexion:
                self.bd.conexion.rollback()
            self.bd.cerrarConexion()
            return False

    def eliminarMulta(self):
        """Elimina una multa"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            cursor.execute("EXEC sp_BorrarMulta %s", (self.multa.multa_id,))
            self.bd.conexion.commit()
            cursor.close()
            self.bd.cerrarConexion()
            print("✓ Multa eliminada")
            return True
        except Exception as e:
            print(f"✗ Error eliminando multa: {e}")
            if self.bd.conexion:
                self.bd.conexion.rollback()
            self.bd.cerrarConexion()
            return False

    def buscarMulta(self):
        """Busca una multa por ID"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            cursor.execute("EXEC sp_ConsultarMulta %s", (self.multa.multa_id,))
            filas = cursor.fetchall()
            cursor.close()
            self.bd.cerrarConexion()
            return filas
        except Exception as e:
            print(f"✗ Error buscando multa: {e}")
            self.bd.cerrarConexion()
            return []
