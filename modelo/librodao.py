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
        sp = "exec [dbo].[sp_CrearLibro] @Titulo=%s, @Autor=%s, @ISBN=%s, @CantidadTotal=%s, @CantidadDisponible=%s, @FechaPublicacion=%s"
        param = (self.libro.titulo, self.libro.autor, self.libro.isbn, self.libro.cantidad_total, self.libro.cantidad_disponible, self.libro.fecha_publicacion)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, param)
        self.bd.conexion.commit()
        self.bd.cerrarConexion()
        
    def actualizarLibro(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_ActualizarLibro] @LibroID=%s, @Titulo=%s, @Autor=%s, @ISBN=%s, @CantidadTotal=%s, @CantidadDisponible=%s, @FechaPublicacion=%s"
        params = (self.libro.libro_id, self.libro.titulo, self.libro.autor, self.libro.isbn, self.libro.cantidad_total, self.libro.cantidad_disponible, self.libro.fecha_publicacion)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        self.bd.conexion.commit()
        self.bd.cerrarConexion()

    def eliminarLibro(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_BorrarLibro] @LibroID=%s"
        params = (self.libro.libro_id,)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        self.bd.conexion.commit()
        self.bd.cerrarConexion()

    def buscarLibro(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_ConsultarLibro] @LibroID=%s"
        param = [self.libro.libro_id]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexion()
        return filas
