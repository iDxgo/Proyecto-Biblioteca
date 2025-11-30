from modelo.conexionbd import ConexionBD
from modelo.usuario import Usuario

class UsuarioDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.usuario = Usuario()
        
    def listarUsuarios(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_ListarUsuarios]"
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexion()
        return filas
            
    def insertarUsuario(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_CrearUsuario] @Username=?, @Password=?, @Nombre=?, @Email=?"
        param = (self.usuario.username, self.usuario.password, self.usuario.nombre, self.usuario.email)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.bd.cerrarConexion()
        
    def actualizarUsuario(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_ActualizarUsuario] @UsuarioID=?, @Username=?, @Password=?, @Nombre=?, @Email=?"
        params = (self.usuario.usuario_id, self.usuario.username, self.usuario.password, self.usuario.nombre, self.usuario.email)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        self.bd.conexion.commit()
        self.bd.cerrarConexion()

    def eliminarUsuario(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_BorrarUsuario] @UsuarioID=?"
        params = (self.usuario.usuario_id,)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        cursor.commit()
        self.bd.cerrarConexion()

    def buscarUsuario(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_ConsultarUsuario] @UsuarioID=?"
        param = [self.usuario.usuario_id]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexion()
        return filas
    
    def autenticarUsuarioDirecto(self, username, password):
        """
        Autenticación directa con consulta SQL
        """
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            
            query = """
            SELECT UsuarioID, Username, Nombre 
            FROM Usuarios 
            WHERE Username = ? AND Password = ?
            """
            param = (username, password)
            cursor.execute(query, param)
            filas = cursor.fetchall()
            self.bd.cerrarConexion()
            
            if filas and len(filas) > 0:
                usuario_data = filas[0]
                usuario = Usuario()
                usuario.usuario_id = usuario_data[0]
                usuario.username = usuario_data[1]
                usuario.nombre = usuario_data[2]
                return usuario
            else:
                return None
                
        except Exception as e:
            print(f"Error en autenticación directa: {str(e)}")
            self.bd.cerrarConexion()
            return None