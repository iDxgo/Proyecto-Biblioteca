from modelo.conexionbd import ConexionBD
from modelo.usuario import Usuario

class UsuarioDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.usuario = Usuario()
        
    def listarUsuarios(self):
        """Lista todos los usuarios"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            cursor.execute("EXEC sp_ListarUsuarios")
            filas = cursor.fetchall()
            cursor.close()
            self.bd.cerrarConexion()
            return filas
        except Exception as e:
            print(f"Error listando usuarios: {e}")
            self.bd.cerrarConexion()
            return []
            
    def insertarUsuario(self):
        """Inserta un nuevo usuario"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            cursor.execute(
                "EXEC sp_CrearUsuario %s, %s, %s, %s",
                (self.usuario.username, self.usuario.password, 
                 self.usuario.nombre, self.usuario.email)
            )
            self.bd.conexion.commit()
            cursor.close()
            self.bd.cerrarConexion()
            print("✓ Usuario insertado")
            return True
        except Exception as e:
            print(f"✗ Error insertando usuario: {e}")
            if self.bd.conexion:
                self.bd.conexion.rollback()
            self.bd.cerrarConexion()
            return False
        
    def actualizarUsuario(self):
        """Actualiza un usuario existente"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            cursor.execute(
                "EXEC sp_ActualizarUsuario %s, %s, %s, %s, %s",
                (self.usuario.usuario_id, self.usuario.username, 
                 self.usuario.password, self.usuario.nombre, self.usuario.email)
            )
            self.bd.conexion.commit()
            cursor.close()
            self.bd.cerrarConexion()
            print("✓ Usuario actualizado")
            return True
        except Exception as e:
            print(f"✗ Error actualizando usuario: {e}")
            if self.bd.conexion:
                self.bd.conexion.rollback()
            self.bd.cerrarConexion()
            return False

    def eliminarUsuario(self):
        """Elimina un usuario"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            cursor.execute("EXEC sp_BorrarUsuario %s", (self.usuario.usuario_id,))
            self.bd.conexion.commit()
            cursor.close()
            self.bd.cerrarConexion()
            print("✓ Usuario eliminado")
            return True
        except Exception as e:
            print(f"✗ Error eliminando usuario: {e}")
            if self.bd.conexion:
                self.bd.conexion.rollback()
            self.bd.cerrarConexion()
            return False

    def buscarUsuario(self):
        """Busca un usuario por ID"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            cursor.execute("EXEC sp_ConsultarUsuario %s", (self.usuario.usuario_id,))
            filas = cursor.fetchall()
            cursor.close()
            self.bd.cerrarConexion()
            return filas
        except Exception as e:
            print(f"✗ Error buscando usuario: {e}")
            self.bd.cerrarConexion()
            return []
    
    def autenticarUsuarioDirecto(self, username, password):
        """Autentica un usuario con username y password"""
        try:
            self.bd.establecerConexionBD()
            
            # Verificar que la conexión se estableció correctamente
            if not self.bd.conexion:
                print("✗ No se pudo establecer la conexión")
                return None
            
            cursor = self.bd.conexion.cursor()
            cursor.execute("EXEC sp_AutenticarUsuario %s, %s", (username, password))
            row = cursor.fetchone()
            cursor.close()
            self.bd.cerrarConexion()
            
            if row:
                # Poblar el objeto usuario
                self.usuario.usuario_id = int(row[0])
                self.usuario.nombre = str(row[1])
                self.usuario.username = username
                self.usuario.autenticado = True
                self.usuario.login_error = ""
                print(f"✓ Usuario autenticado: {username}")
                return username
            else:
                self.usuario.login_error = "Credenciales incorrectas."
                print("✗ Credenciales incorrectas")
                return None
                
        except Exception as e:
            print(f"✗ Error en autenticación: {e}")
            self.usuario.login_error = f"Error: {str(e)}"
            self.bd.cerrarConexion()
            return None