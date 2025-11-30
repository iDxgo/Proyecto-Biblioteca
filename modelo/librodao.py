from modelo.conexionbd import ConexionBD
from modelo.libro import Libro

class LibroDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.libro = Libro()
        
    def listarLibros(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_ListarLibros]"
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexion()
        return filas
            
    def insertarLibro(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_CrearLibro] @Titulo=?, @Autor=?, @ISBN=?, @CantidadTotal=?, @CantidadDisponible=?, @FechaPublicacion=?"
        param = (self.libro.titulo, self.libro.autor, self.libro.isbn, self.libro.cantidad_total, self.libro.cantidad_disponible, self.libro.fecha_publicacion)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.bd.cerrarConexion()
        
    def actualizarLibro(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_ActualizarLibro] @LibroID=?, @Titulo=?, @Autor=?, @ISBN=?, @CantidadTotal=?, @CantidadDisponible=?, @FechaPublicacion=?"
        params = (self.libro.libro_id, self.libro.titulo, self.libro.autor, self.libro.isbn, self.libro.cantidad_total, self.libro.cantidad_disponible, self.libro.fecha_publicacion)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        self.bd.conexion.commit()
        self.bd.cerrarConexion()

    def eliminarLibro(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_BorrarLibro] @LibroID=?"
        params = (self.libro.libro_id,)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        cursor.commit()
        self.bd.cerrarConexion()

    def buscarLibro(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_ConsultarLibro] @LibroID=?"
        param = [self.libro.libro_id]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexion()
        return filas
