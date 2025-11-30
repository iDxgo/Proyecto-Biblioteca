#1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from modelo.usuariodao import UsuarioDAO

#2.- Cargar archivo .ui
class Load_ui_usuarios(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar archivo .ui
        uic.loadUi("ui/usuarios.ui", self)
        self.show()
        self.usuariodao = UsuarioDAO()
        
#3.- Configurar contenedores
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Abrir menu
        self.boton_menu.clicked.connect(self.abrir_menu)
        # mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        self.boton_salir.clicked.connect(lambda: self.close())
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

#4.- Conectar botones a funciones
#Botones para cambiar de página
        self.boton_crear.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_crear))
        self.boton_buscar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_buscar))
        self.boton_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        self.boton_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.boton_consultar_todos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_consultar_todos))

        #Botones para guardar, buscar, eliminar, actualizar y limpiar
        self.buscar_eliminar.clicked.connect(self.buscar_usuario_eliminar)
        self.buscar_actualizar.clicked.connect(self.buscar_usuario_actualizar)
        self.buscar_buscar.clicked.connect(self.buscar_usuario_buscar)
        self.accion_guardar.clicked.connect(self.guardar_usuario)
        self.accion_eliminar.clicked.connect(self.eliminar_usuario)
        self.accion_actualizar.clicked.connect(self.actualizar_usuario)
        self.accion_limpiar.clicked.connect(self.limpiar_usuario)
        self.boton_refrescar.clicked.connect(self.actualizar_tabla)
        
#5.- Operaciones con el modelo de datos            
    def guardar_usuario(self):
        try:
            self.usuariodao.usuario.username = self.username_crear.text()
            self.usuariodao.usuario.password = self.password_crear.text()
            self.usuariodao.usuario.nombre = self.nombre_crear.text()
            self.usuariodao.usuario.email = self.email_crear.text()
            #self.usuariodao.usuario.fecha_registro = self.fecha_registro_crear.text()
            
            self.usuariodao.insertarUsuario()
            self.label_titulo.setText("Usuario agregado exitosamente")
            self.limpiar_formulario_crear()
            
        except Exception as e:
            self.label_titulo.setText(f"Error al guardar: {str(e)}")

    def limpiar_usuario(self):
        self.id_buscar.clear()
        self.username_buscar.clear()
        self.password_buscar.clear()
        self.nombre_buscar.clear()
        self.email_buscar.clear()
        self.fecha_registro_buscar.clear()

    def limpiar_formulario_crear(self):
        self.username_crear.clear()
        self.password_crear.clear()
        self.nombre_crear.clear()
        self.email_crear.clear()
        self.fecha_registro_crear.clear()

    def actualizar_usuario(self):
        try:
            self.usuariodao.usuario.usuario_id = int(self.id_actualizar.text())
            self.usuariodao.usuario.username = self.username_actualizar.text()
            self.usuariodao.usuario.password = self.password_actualizar.text()
            self.usuariodao.usuario.nombre = self.nombre_actualizar.text()
            self.usuariodao.usuario.email = self.email_actualizar.text()
            self.usuariodao.usuario.fecha_registro = self.fecha_registro_actualizar.text()
            
            self.usuariodao.actualizarUsuario()
            self.label_titulo.setText(f"Usuario {self.usuariodao.usuario.usuario_id} actualizado")
            
        except Exception as e:
            self.label_titulo.setText(f"Error al actualizar: {str(e)}")

    def eliminar_usuario(self):
        try:
            self.usuariodao.usuario.usuario_id = int(self.id_eliminar.text())
            self.usuariodao.eliminarUsuario()
            self.label_titulo.setText(f"Usuario {self.usuariodao.usuario.usuario_id} eliminado")
            self.limpiar_formulario_eliminar()
            
        except Exception as e:
            self.label_titulo.setText(f"Error al eliminar: {str(e)}")

    def limpiar_formulario_eliminar(self):
        self.id_eliminar.clear()
        self.username_eliminar.clear()
        self.password_eliminar.clear()
        self.nombre_eliminar.clear()
        self.email_eliminar.clear()
        self.fecha_registro_eliminar.clear()

    def buscar_usuario_eliminar(self):
        try:
            usuario_id = self.id_eliminar.text().strip()
            
            if not usuario_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.usuariodao.usuario.usuario_id = int(usuario_id)
            datos = self.usuariodao.buscarUsuario()
            
            if datos and len(datos) > 0:
                usuario = datos[0]
                self.username_eliminar.setText(str(usuario[1]))
                self.password_eliminar.setText(str(usuario[2]))
                self.nombre_eliminar.setText(str(usuario[3]))
                self.email_eliminar.setText(str(usuario[4]))
                self.fecha_registro_eliminar.setText(str(usuario[5]))
            else:
                self.label_titulo.setText("Usuario no encontrado")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")

    def buscar_usuario_actualizar(self):
        try:
            usuario_id = self.id_actualizar.text().strip()
            
            if not usuario_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.usuariodao.usuario.usuario_id = int(usuario_id)
            datos = self.usuariodao.buscarUsuario()
            
            if datos and len(datos) > 0:
                usuario = datos[0]
                self.username_actualizar.setText(str(usuario[1]))
                self.password_actualizar.setText(str(usuario[2]))
                self.nombre_actualizar.setText(str(usuario[3]))
                self.email_actualizar.setText(str(usuario[4]))
                self.fecha_registro_actualizar.setText(str(usuario[5]))
            else:
                self.label_titulo.setText("Usuario no encontrado")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")

    def buscar_usuario_buscar(self):
        try:
            usuario_id = self.id_buscar.text().strip()
            
            if not usuario_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.usuariodao.usuario.usuario_id = int(usuario_id)
            datos = self.usuariodao.buscarUsuario()
            
            if datos and len(datos) > 0:
                usuario = datos[0]
                self.username_buscar.setText(str(usuario[1]))
                self.password_buscar.setText(str(usuario[2]))
                self.nombre_buscar.setText(str(usuario[3]))
                self.email_buscar.setText(str(usuario[4]))
                self.fecha_registro_buscar.setText(str(usuario[5]))
            else:
                self.label_titulo.setText("Usuario no encontrado")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")
    
    def actualizar_tabla(self):
        try:
            datos = self.usuariodao.listarUsuarios()
            self.tabla_usuarios.setRowCount(len(datos))
            fila = 0
            for item in datos:
                self.tabla_usuarios.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[0])))  # ID
                self.tabla_usuarios.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[1])))  # Username
                self.tabla_usuarios.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[2])))  # Password
                self.tabla_usuarios.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item[3])))  # Nombre
                self.tabla_usuarios.setItem(fila, 4, QtWidgets.QTableWidgetItem(str(item[4])))  # Email
                self.tabla_usuarios.setItem(fila, 5, QtWidgets.QTableWidgetItem(str(item[5])))  # Fecha Registro
                fila += 1
                
            self.label_titulo.setText(f"Tabla actualizada - {len(datos)} usuarios encontrados")
            
        except Exception as e:
            self.label_titulo.setText(f"Error al cargar tabla: {str(e)}")

    def abrir_menu(self):
        from carga_ui.carga_menu import Load_ui_menu
        menu = Load_ui_menu()
        menu.show()
        self.hide()

    # 6.- mover ventana
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

#7.- Mover menú
    def mover_menu(self):
        if True:			
            width = self.frame_lateral.width()
            widthb = self.boton_menu.width()
            normal = 0
            if width==0:
                extender = 200
                self.boton_menu.setText("Menú")
            else:
                extender = normal
                self.boton_menu.setText("")
                
            self.animacion = QPropertyAnimation(self.frame_lateral, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            
            self.animacionb = QPropertyAnimation(self.boton_menu, b'minimumWidth')
        
            self.animacionb.setStartValue(width)
            self.animacionb.setEndValue(extender)
            self.animacionb.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacionb.start()