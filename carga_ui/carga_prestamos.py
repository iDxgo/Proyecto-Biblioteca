#1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from modelo.prestamodao import PrestamoDAO
from datetime import datetime

#2.- Cargar archivo .ui
class Load_ui_prestamos(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar archivo .ui
        uic.loadUi("ui/prestamos.ui", self)
        self.show()
        self.prestamodao = PrestamoDAO()
        
#3.- Configurar contenedores
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Abrir menu
        self.boton_menu.clicked.connect(self.abrir_menu)
        # mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        #salir
        self.boton_salir.clicked.connect(lambda: self.close())
        #Fijar ancho columnas
        self.tabla_prestamos.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

#4.- Conectar botones a funciones
#Botones para cambiar de página
        self.boton_crear.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_crear))
        self.boton_buscar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_buscar))
        self.boton_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        self.boton_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.boton_consultar_todos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_consultar_todos))

        #Botones para guardar, buscar, eliminar, actualizar y limpiar
        self.buscar_eliminar.clicked.connect(self.buscar_prestamo_eliminar)
        self.buscar_actualizar.clicked.connect(self.buscar_prestamo_actualizar)
        self.buscar_buscar.clicked.connect(self.buscar_prestamo_buscar)
        self.accion_guardar.clicked.connect(self.guardar_prestamo)
        self.accion_eliminar.clicked.connect(self.eliminar_prestamo)
        self.accion_actualizar.clicked.connect(self.actualizar_prestamo)
        self.accion_limpiar.clicked.connect(self.limpiar_prestamo)
        self.boton_refrescar.clicked.connect(self.actualizar_tabla)
        
#5.- Operaciones con el modelo de datos            
    def guardar_prestamo(self):
        try:
            self.prestamodao.prestamo.usuario_id = int(self.usuario_id_crear.text())
            self.prestamodao.prestamo.libro_id = int(self.libro_id_crear.text())
            
            # Formatear fechas correctamente
            fecha_prestamo = self.fecha_prestamo_crear.text()
            fecha_devolucion = self.fecha_devolucion_crear.text()
            fecha_devolucion_real = self.fecha_devolucion_real_crear.text()
            
            # Validar y formatear fechas
            self.prestamodao.prestamo.fecha_prestamo = self.formatear_fecha(fecha_prestamo)
            self.prestamodao.prestamo.fecha_devolucion = self.formatear_fecha(fecha_devolucion)
            
            # Fecha devolución real puede estar vacía
            if fecha_devolucion_real.strip():
                self.prestamodao.prestamo.fecha_devolucion_real = self.formatear_fecha(fecha_devolucion_real)
            else:
                self.prestamodao.prestamo.fecha_devolucion_real = None
                
            self.prestamodao.prestamo.estado = self.estado_crear.text()
            
            self.prestamodao.insertarPrestamo()
            self.label_titulo.setText("Préstamo agregado exitosamente")
            self.limpiar_formulario_crear()
            
        except Exception as e:
            self.label_titulo.setText(f"Error al guardar: {str(e)}")

    def actualizar_prestamo(self):
        try:
            self.prestamodao.prestamo.prestamo_id = int(self.prestamo_id_actualizar.text())
            self.prestamodao.prestamo.usuario_id = int(self.usuario_id_actualizar.text())
            self.prestamodao.prestamo.libro_id = int(self.libro_id_actualizar.text())
            
            # Formatear fechas correctamente para actualización
            self.prestamodao.prestamo.fecha_prestamo = self.formatear_fecha(self.fecha_prestamo_actualizar.text())
            self.prestamodao.prestamo.fecha_devolucion = self.formatear_fecha(self.fecha_devolucion_actualizar.text())
            
            fecha_devolucion_real = self.fecha_devolucion_real_actualizar.text()
            if fecha_devolucion_real.strip():
                self.prestamodao.prestamo.fecha_devolucion_real = self.formatear_fecha(fecha_devolucion_real)
            else:
                self.prestamodao.prestamo.fecha_devolucion_real = None
                
            self.prestamodao.prestamo.estado = self.estado_actualizar.text()
            
            self.prestamodao.actualizarPrestamo()
            self.label_titulo.setText(f"Préstamo {self.prestamodao.prestamo.prestamo_id} actualizado")
            
        except Exception as e:
            self.label_titulo.setText(f"Error al actualizar: {str(e)}")

    def formatear_fecha(self, fecha_texto):
        """Convierte diferentes formatos de fecha a formato SQL Server"""
        if not fecha_texto.strip():
            return None
            
        try:
            # Intentar diferentes formatos de fecha
            formatos = [
                '%Y-%m-%d %H:%M:%S',    # 2024-01-15 14:30:00
                '%Y-%m-%d %H:%M',       # 2024-01-15 14:30
                '%Y-%m-%d',             # 2024-01-15
                '%d/%m/%Y %H:%M:%S',    # 15/01/2024 14:30:00
                '%d/%m/%Y %H:%M',       # 15/01/2024 14:30
                '%d/%m/%Y',             # 15/01/2024
                '%m/%d/%Y %H:%M:%S',    # 01/15/2024 14:30:00
                '%m/%d/%Y %H:%M',       # 01/15/2024 14:30
                '%m/%d/%Y'              # 01/15/2024
            ]
            
            for formato in formatos:
                try:
                    fecha_obj = datetime.strptime(fecha_texto.strip(), formato)
                    # Convertir a formato SQL Server estándar
                    return fecha_obj.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    continue
                    
            # Si ningún formato funciona, lanzar error
            raise ValueError(f"Formato de fecha no reconocido: {fecha_texto}")
            
        except Exception as e:
            raise ValueError(f"Error al formatear fecha '{fecha_texto}': {str(e)}")
            
    def limpiar_prestamo(self):
        self.prestamo_id_buscar.clear()
        self.usuario_id_buscar.clear()
        self.libro_id_buscar.clear()
        self.fecha_prestamo_buscar.clear()
        self.fecha_devolucion_buscar.clear()
        self.fecha_devolucion_real_buscar.clear()
        self.estado_buscar.clear()

    def limpiar_formulario_crear(self):
        self.usuario_id_crear.clear()
        self.libro_id_crear.clear()
        self.fecha_prestamo_crear.clear()
        self.fecha_devolucion_crear.clear()
        self.fecha_devolucion_real_crear.clear()
        self.estado_crear.clear()


    def eliminar_prestamo(self):
        try:
            self.prestamodao.prestamo.prestamo_id = int(self.prestamo_id_eliminar.text())
            self.prestamodao.eliminarPrestamo()
            self.label_titulo.setText(f"Préstamo {self.prestamodao.prestamo.prestamo_id} eliminado")
            self.limpiar_formulario_eliminar()
            
        except Exception as e:
            self.label_titulo.setText(f"Error al eliminar: {str(e)}")

    def limpiar_formulario_eliminar(self):
        self.prestamo_id_eliminar.clear()
        self.usuario_id_eliminar.clear()
        self.libro_id_eliminar.clear()
        self.fecha_prestamo_eliminar.clear()
        self.fecha_devolucion_eliminar.clear()
        self.fecha_devolucion_real_eliminar.clear()
        self.estado_eliminar.clear()

    def buscar_prestamo_eliminar(self):
        try:
            prestamo_id = self.prestamo_id_eliminar.text().strip()
            
            if not prestamo_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.prestamodao.prestamo.prestamo_id = int(prestamo_id)
            datos = self.prestamodao.buscarPrestamo()
            
            if datos and len(datos) > 0:
                prestamo = datos[0]
                self.usuario_id_eliminar.setText(str(prestamo[1]))
                self.libro_id_eliminar.setText(str(prestamo[2]))
                self.fecha_prestamo_eliminar.setText(str(prestamo[3]))
                self.fecha_devolucion_eliminar.setText(str(prestamo[4]))
                self.fecha_devolucion_real_eliminar.setText(str(prestamo[5]))
                self.estado_eliminar.setText(str(prestamo[6]))
            else:
                self.label_titulo.setText("Préstamo no encontrado")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")

    def buscar_prestamo_actualizar(self):
        try:
            prestamo_id = self.prestamo_id_actualizar.text().strip()
            
            if not prestamo_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.prestamodao.prestamo.prestamo_id = int(prestamo_id)
            datos = self.prestamodao.buscarPrestamo()
            
            if datos and len(datos) > 0:
                prestamo = datos[0]
                self.usuario_id_actualizar.setText(str(prestamo[1]))
                self.libro_id_actualizar.setText(str(prestamo[2]))
                self.fecha_prestamo_actualizar.setText(str(prestamo[3]))
                self.fecha_devolucion_actualizar.setText(str(prestamo[4]))
                self.fecha_devolucion_real_actualizar.setText(str(prestamo[5]))
                self.estado_actualizar.setText(str(prestamo[6]))
            else:
                self.label_titulo.setText("Préstamo no encontrado")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")

    def buscar_prestamo_buscar(self):
        try:
            prestamo_id = self.prestamo_id_buscar.text().strip()
            
            if not prestamo_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.prestamodao.prestamo.prestamo_id = int(prestamo_id)
            datos = self.prestamodao.buscarPrestamo()
            
            if datos and len(datos) > 0:
                prestamo = datos[0]
                self.usuario_id_buscar.setText(str(prestamo[1]))
                self.libro_id_buscar.setText(str(prestamo[2]))
                self.fecha_prestamo_buscar.setText(str(prestamo[3]))
                self.fecha_devolucion_buscar.setText(str(prestamo[4]))
                self.fecha_devolucion_real_buscar.setText(str(prestamo[5]))
                self.estado_buscar.setText(str(prestamo[6]))
            else:
                self.label_titulo.setText("Préstamo no encontrado")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")
    
    def actualizar_tabla(self):
        try:
            datos = self.prestamodao.listarPrestamos()
            self.tabla_prestamos.setRowCount(len(datos))
            fila = 0
            for item in datos:
                self.tabla_prestamos.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[0])))  # ID
                self.tabla_prestamos.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[1])))  # Usuario ID
                self.tabla_prestamos.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[2])))  # Libro ID
                self.tabla_prestamos.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item[3])))  # Fecha Préstamo
                self.tabla_prestamos.setItem(fila, 4, QtWidgets.QTableWidgetItem(str(item[4])))  # Fecha Devolución
                self.tabla_prestamos.setItem(fila, 5, QtWidgets.QTableWidgetItem(str(item[5])))  # Fecha Devolución Real
                self.tabla_prestamos.setItem(fila, 6, QtWidgets.QTableWidgetItem(str(item[6])))  # Estado
                fila += 1
                
            self.label_titulo.setText(f"Tabla actualizada - {len(datos)} préstamos encontrados")
            
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