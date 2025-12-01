from modelo.conexionbd import ConexionBD
from modelo.prestamo import Prestamo

class PrestamoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.prestamo = Prestamo()
        
    def listarPrestamos(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_ListarPrestamos]"
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexion()
        return filas
            
    def insertarPrestamo(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_CrearPrestamo] @UsuarioID=%s, @LibroID=%s, @FechaPrestamo=%s, @FechaDevolucion=%s, @FechaDevolucionReal=%s, @Estado=%s"
        param = (self.prestamo.usuario_id, self.prestamo.libro_id, self.prestamo.fecha_prestamo, self.prestamo.fecha_devolucion, self.prestamo.fecha_devolucion_real, self.prestamo.estado)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, param)
        self.bd.conexion.commit()
        self.bd.cerrarConexion()
        
    def actualizarPrestamo(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_ActualizarPrestamo] @PrestamoID=%s, @UsuarioID=%s, @LibroID=%s, @FechaPrestamo=%s, @FechaDevolucion=%s, @FechaDevolucionReal=%s, @Estado=%s"
        params = (self.prestamo.prestamo_id, self.prestamo.usuario_id, self.prestamo.libro_id, self.prestamo.fecha_prestamo, self.prestamo.fecha_devolucion, self.prestamo.fecha_devolucion_real, self.prestamo.estado)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        self.bd.conexion.commit()
        self.bd.cerrarConexion()

    def eliminarPrestamo(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_BorrarPrestamo] @PrestamoID=%s"
        params = (self.prestamo.prestamo_id,)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        self.bd.conexion.commit()
        self.bd.cerrarConexion()

    def buscarPrestamo(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_ConsultarPrestamo] @PrestamoID=%s"
        param = [self.prestamo.prestamo_id]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexion()
        return filas