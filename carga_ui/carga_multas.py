#1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from modelo.multadao import MultaDAO

#2.- Cargar archivo .ui
class Load_ui_multas(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar archivo .ui
        uic.loadUi("ui/multas.ui", self)
        self.show()
        self.multadao = MultaDAO()
        
#3.- Configurar contenedores
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Abrir menu
        self.boton_menu.clicked.connect(self.abrir_menu)
        # mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        #menu lateral
        self.boton_salir.clicked.connect(lambda: self.close())
        #Fijar ancho columnas
        self.tabla_multas.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

#4.- Conectar botones a funciones
#Botones para cambiar de página
        self.boton_crear.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_crear))
        self.boton_buscar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_buscar))
        self.boton_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        self.boton_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.boton_consultar_todos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_consultar_todos))

        #Botones para guardar, buscar, eliminar, actualizar y limpiar
        self.buscar_eliminar.clicked.connect(self.buscar_multa_eliminar)
        self.buscar_actualizar.clicked.connect(self.buscar_multa_actualizar)
        self.buscar_buscar.clicked.connect(self.buscar_multa_buscar)
        self.accion_guardar.clicked.connect(self.guardar_multa)
        self.accion_eliminar.clicked.connect(self.eliminar_multa)
        self.accion_actualizar.clicked.connect(self.actualizar_multa)
        self.accion_limpiar.clicked.connect(self.limpiar_multa)
        self.boton_refrescar.clicked.connect(self.actualizar_tabla)
        
#5.- Operaciones con el modelo de datos            
    def guardar_multa(self):
        try:
            self.multadao.multa.prestamo_id = int(self.prestamo_id_crear.text())
            self.multadao.multa.usuario_id = int(self.usuario_id_crear.text())
            self.multadao.multa.monto = float(self.monto_crear.text())
            self.multadao.multa.fecha_multa = self.fecha_multa_crear.text()
            self.multadao.multa.estado = self.estado_crear.text()
            
            self.multadao.insertarMulta()
            self.label_titulo.setText("Multa agregada exitosamente")
            self.limpiar_formulario_crear()
            
        except Exception as e:
            self.label_titulo.setText(f"Error al guardar: {str(e)}")

    def limpiar_multa(self):
        self.multa_id_buscar.clear()
        self.prestamo_id_buscar.clear()
        self.usuario_id_buscar.clear()
        self.monto_buscar.clear()
        self.fecha_multa_buscar.clear()
        self.estado_buscar.clear()

    def limpiar_formulario_crear(self):
        self.prestamo_id_crear.clear()
        self.usuario_id_crear.clear()
        self.monto_crear.clear()
        self.fecha_multa_crear.clear()
        self.estado_crear.clear()

    def actualizar_multa(self):
        try:
            self.multadao.multa.multa_id = int(self.multa_id_actualizar.text())
            self.multadao.multa.prestamo_id = int(self.prestamo_id_actualizar.text())
            self.multadao.multa.usuario_id = int(self.usuario_id_actualizar.text())
            self.multadao.multa.monto = float(self.monto_actualizar.text())
            self.multadao.multa.fecha_multa = self.fecha_multa_actualizar.text()
            self.multadao.multa.estado = self.estado_actualizar.text()
            
            self.multadao.actualizarMulta()
            self.label_titulo.setText(f"Multa {self.multadao.multa.multa_id} actualizada")
            
        except Exception as e:
            self.label_titulo.setText(f"Error al actualizar: {str(e)}")

    def eliminar_multa(self):
        try:
            self.multadao.multa.multa_id = int(self.multa_id_eliminar.text())
            self.multadao.eliminarMulta()
            self.label_titulo.setText(f"Multa {self.multadao.multa.multa_id} eliminada")
            self.limpiar_formulario_eliminar()
            
        except Exception as e:
            self.label_titulo.setText(f"Error al eliminar: {str(e)}")

    def limpiar_formulario_eliminar(self):
        self.multa_id_eliminar.clear()
        self.prestamo_id_eliminar.clear()
        self.usuario_id_eliminar.clear()
        self.monto_eliminar.clear()
        self.fecha_multa_eliminar.clear()
        self.estado_eliminar.clear()

    def buscar_multa_eliminar(self):
        try:
            multa_id = self.multa_id_eliminar.text().strip()
            
            if not multa_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.multadao.multa.multa_id = int(multa_id)
            datos = self.multadao.buscarMulta()
            
            if datos and len(datos) > 0:
                multa = datos[0]
                self.prestamo_id_eliminar.setText(str(multa[1]))
                self.usuario_id_eliminar.setText(str(multa[2]))
                self.monto_eliminar.setText(str(multa[3]))
                self.fecha_multa_eliminar.setText(str(multa[4]))
                self.estado_eliminar.setText(str(multa[5]))
            else:
                self.label_titulo.setText("Multa no encontrada")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")

    def buscar_multa_actualizar(self):
        try:
            multa_id = self.multa_id_actualizar.text().strip()
            
            if not multa_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.multadao.multa.multa_id = int(multa_id)
            datos = self.multadao.buscarMulta()
            
            if datos and len(datos) > 0:
                multa = datos[0]
                self.prestamo_id_actualizar.setText(str(multa[1]))
                self.usuario_id_actualizar.setText(str(multa[2]))
                self.monto_actualizar.setText(str(multa[3]))
                self.fecha_multa_actualizar.setText(str(multa[4]))
                self.estado_actualizar.setText(str(multa[5]))
            else:
                self.label_titulo.setText("Multa no encontrada")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")

    def buscar_multa_buscar(self):
        try:
            multa_id = self.multa_id_buscar.text().strip()
            
            if not multa_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.multadao.multa.multa_id = int(multa_id)
            datos = self.multadao.buscarMulta()
            
            if datos and len(datos) > 0:
                multa = datos[0]
                self.prestamo_id_buscar.setText(str(multa[1]))
                self.usuario_id_buscar.setText(str(multa[2]))
                self.monto_buscar.setText(str(multa[3]))
                self.fecha_multa_buscar.setText(str(multa[4]))
                self.estado_buscar.setText(str(multa[5]))
            else:
                self.label_titulo.setText("Multa no encontrada")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")
    
    def actualizar_tabla(self):
        try:
            datos = self.multadao.listarMultas()
            self.tabla_multas.setRowCount(len(datos))
            fila = 0
            for item in datos:
                self.tabla_multas.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[0])))  # ID
                self.tabla_multas.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[1])))  # Préstamo ID
                self.tabla_multas.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[2])))  # Usuario ID
                self.tabla_multas.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item[3])))  # Monto
                self.tabla_multas.setItem(fila, 4, QtWidgets.QTableWidgetItem(str(item[4])))  # Fecha Multa
                self.tabla_multas.setItem(fila, 5, QtWidgets.QTableWidgetItem(str(item[5])))  # Estado
                fila += 1
                
            self.label_titulo.setText(f"Tabla actualizada - {len(datos)} multas encontradas")
            
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