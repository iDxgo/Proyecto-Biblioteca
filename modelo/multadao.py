from modelo.conexionbd import ConexionBD
from modelo.multa import Multa

class MultaDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.multa = Multa()
        
    def listarMultas(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_ListarMultas]"
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexion()
        return filas
            
    def insertarMulta(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_CrearMulta] @PrestamoID=?, @UsuarioID=?, @Monto=?, @FechaMulta=?, @Estado=?"
        param = (self.multa.prestamo_id, self.multa.usuario_id, self.multa.monto, self.multa.fecha_multa, self.multa.estado)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.bd.cerrarConexion()
        
    def actualizarMulta(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_ActualizarMulta] @MultaID=?, @PrestamoID=?, @UsuarioID=?, @Monto=?, @FechaMulta=?, @Estado=?"
        params = (self.multa.multa_id, self.multa.prestamo_id, self.multa.usuario_id, self.multa.monto, self.multa.fecha_multa, self.multa.estado)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        self.bd.conexion.commit()
        self.bd.cerrarConexion()

    def eliminarMulta(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_BorrarMulta] @MultaID=?"
        params = (self.multa.multa_id,)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        cursor.commit()
        self.bd.cerrarConexion()

    def buscarMulta(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_ConsultarMulta] @MultaID=?"
        param = [self.multa.multa_id]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexion()
        return filas