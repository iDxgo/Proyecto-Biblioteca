#1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation, QTimer
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from modelo.usuariodao import UsuarioDAO

#2.- Cargar archivo .ui
class Load_ui_login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar archivo .ui
        uic.loadUi("ui/login.ui", self)
        self.show()
        self.usuariodao = UsuarioDAO()
        
#3.- Configurar contenedores
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        
        #Cerrar ventana
        self.boton_salir.clicked.connect(self.salir_aplicacion)
        
        # mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        
        # Botón login
        self.boton_login.clicked.connect(self.iniciar_sesion)
        
        # Enter en campos de texto también ejecuta login
        self.usuario_login.returnPressed.connect(self.iniciar_sesion)
        self.password_login.returnPressed.connect(self.iniciar_sesion)
        
        # Inicializar mensaje
        self.label_mensaje.setText("Ingrese sus credenciales")
        
#4.- Funciones de login
    def iniciar_sesion(self):
        username = self.usuario_login.text().strip()
        password = self.password_login.text().strip()

        if not username or not password:
            self.mostrar_mensaje_error("Por favor, complete todos los campos")
            return

        try:
            usuario_dao = UsuarioDAO()
            resultado = usuario_dao.autenticarUsuarioDirecto(username, password)

            if resultado:
                nombre_usuario = usuario_dao.usuario.nombre
                self.mostrar_mensaje_exito(f"¡Bienvenido, {nombre_usuario}!")

                self.usuario_autenticado = usuario_dao.usuario

                QTimer.singleShot(1000, self.abrir_menu_principal)
            else:
                self.mostrar_mensaje_error("Usuario o contraseña incorrectos")
                self.limpiar_campos()

        except Exception as e:
            print(f"Error completo: {e}")
            self.mostrar_mensaje_error(f"Error de conexión: {str(e)}")
    
    def mostrar_mensaje_exito(self, mensaje):
        """Muestra mensaje de éxito"""
        self.label_mensaje.setStyleSheet("color: #4CAF50; font-weight: bold;")
        self.label_mensaje.setText(mensaje)
        self.boton_login.setEnabled(False)  # Deshabilitar botón temporalmente

    def mostrar_mensaje_error(self, mensaje):
        """Muestra mensaje de error"""
        self.label_mensaje.setStyleSheet("color: #f44336; font-weight: bold;")
        self.label_mensaje.setText(mensaje)
        
        # Efecto de shake en el frame de login
        self.animar_error()

    def animar_error(self):
        """Animación de shake para indicar error"""
        self.animacion = QPropertyAnimation(self.frame_login, b"pos")
        self.animacion.setDuration(100)
        self.animacion.setLoopCount(3)
        
        pos_original = self.frame_login.pos()
        self.animacion.setKeyValueAt(0, pos_original)
        self.animacion.setKeyValueAt(0.25, pos_original + QtCore.QPoint(5, 0))
        self.animacion.setKeyValueAt(0.75, pos_original + QtCore.QPoint(-5, 0))
        self.animacion.setKeyValueAt(1, pos_original)
        
        self.animacion.start()

    def limpiar_campos(self):
        """Limpia los campos de usuario y contraseña"""
        self.password_login.clear()
        self.usuario_login.selectAll()
        self.usuario_login.setFocus()

    def abrir_menu_principal(self):
        """Abre la ventana del menú principal"""
        try:
            from carga_ui.carga_menu import Load_ui_menu
            self.menu_principal = Load_ui_menu()
            self.menu_principal.show()
            self.hide()
        except ImportError as e:
            self.mostrar_mensaje_error("Error: No se pudo cargar el menú principal")
            self.boton_login.setEnabled(True)

    def salir_aplicacion(self):
        """Cierra la aplicación"""
        self.close()

    # 5.- mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        
    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()