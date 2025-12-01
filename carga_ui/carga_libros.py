#1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from modelo.librodao import LibroDAO

#2.- Cargar archivo .ui
class Load_ui_libros(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar archivo .ui
        uic.loadUi("ui/libros.ui", self)
        self.show()
        self.librodao = LibroDAO()
        
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
        self.tabla_libros.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

#4.- Conectar botones a funciones
#Botones para cambiar de página
        self.boton_crear.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_crear))
        self.boton_buscar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_buscar))
        self.boton_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        self.boton_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.boton_consultar_todos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_consultar_todos))

        #Botones para guardar, buscar, eliminar, actualizar y limpiar
        self.buscar_eliminar.clicked.connect(self.buscar_libro_eliminar)
        self.buscar_actualizar.clicked.connect(self.buscar_libro_actualizar)
        self.buscar_buscar.clicked.connect(self.buscar_libro_buscar)
        self.accion_guardar.clicked.connect(self.guardar_libro)
        self.accion_eliminar.clicked.connect(self.eliminar_libro)
        self.accion_actualizar.clicked.connect(self.actualizar_libro)
        self.accion_limpiar.clicked.connect(self.limpiar_libro)
        self.boton_refrescar.clicked.connect(self.actualizar_tabla)
        
#5.- Operaciones con el modelo de datos            
    def guardar_libro(self):
        try:
            self.librodao.libro.titulo = self.titulo_crear.text()
            self.librodao.libro.autor = self.autor_crear.text()
            self.librodao.libro.isbn = self.isbn_crear.text()
            self.librodao.libro.cantidad_total = int(self.cantidad_total_crear.text())
            self.librodao.libro.cantidad_disponible = int(self.cantidad_disponible_crear.text())
            self.librodao.libro.fecha_publicacion = self.fecha_publicacion_crear.text()
            
            self.librodao.insertarLibro()
            self.label_titulo.setText("Libro agregado exitosamente")
            self.limpiar_formulario_crear()
            
        except Exception as e:
            self.label_titulo.setText(f"Error al guardar: {str(e)}")

    def limpiar_libro(self):
        self.libro_id_buscar.clear()
        self.titulo_buscar.clear()
        self.autor_buscar.clear()
        self.isbn_buscar.clear()
        self.cantidad_total_buscar.clear()
        self.cantidad_disponible_buscar.clear()
        self.fecha_publicacion_buscar.clear()

    def limpiar_formulario_crear(self):
        self.titulo_crear.clear()
        self.autor_crear.clear()
        self.isbn_crear.clear()
        self.cantidad_total_crear.clear()
        self.cantidad_disponible_crear.clear()
        self.fecha_publicacion_crear.clear()

    def actualizar_libro(self):
        try:
            self.librodao.libro.libro_id = int(self.libro_id_actualizar.text())
            self.librodao.libro.titulo = self.titulo_actualizar.text()
            self.librodao.libro.autor = self.autor_actualizar.text()
            self.librodao.libro.isbn = self.isbn_actualizar.text()
            self.librodao.libro.cantidad_total = int(self.cantidad_total_actualizar.text())
            self.librodao.libro.cantidad_disponible = int(self.cantidad_disponible_actualizar.text())
            self.librodao.libro.fecha_publicacion = self.fecha_publicacion_actualizar.text()
            
            self.librodao.actualizarLibro()
            self.label_titulo.setText(f"Libro {self.librodao.libro.libro_id} actualizado")
            
        except Exception as e:
            self.label_titulo.setText(f"Error al actualizar: {str(e)}")

    def eliminar_libro(self):
        try:
            self.librodao.libro.libro_id = int(self.libro_id_eliminar.text())
            self.librodao.eliminarLibro()
            self.label_titulo.setText(f"Libro {self.librodao.libro.libro_id} eliminado")
            self.limpiar_libro()
            
        except Exception as e:
            self.label_titulo.setText(f"Error al eliminar: {str(e)}")

    def buscar_libro_eliminar(self):
        try:
            libro_id = self.libro_id_eliminar.text().strip()
            
            if not libro_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.librodao.libro.libro_id = int(libro_id)
            datos = self.librodao.buscarLibro()
            
            if datos and len(datos) > 0:
                libro = datos[0]
                self.titulo_eliminar.setText(str(libro[1]))
                self.autor_eliminar.setText(str(libro[2]))
                self.isbn_eliminar.setText(str(libro[3]))
                self.cantidad_total_eliminar.setText(str(libro[4]))
                self.cantidad_disponible_eliminar.setText(str(libro[5]))
                self.fecha_publicacion_eliminar.setText(str(libro[6]))
            else:
                self.label_titulo.setText("Libro no encontrado")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")

    def buscar_libro_actualizar(self):
        try:
            libro_id = self.libro_id_actualizar.text().strip()
            
            if not libro_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.librodao.libro.libro_id = int(libro_id)
            datos = self.librodao.buscarLibro()
            
            if datos and len(datos) > 0:
                libro = datos[0]
                self.titulo_actualizar.setText(str(libro[1]))
                self.autor_actualizar.setText(str(libro[2]))
                self.isbn_actualizar.setText(str(libro[3]))
                self.cantidad_total_actualizar.setText(str(libro[4]))
                self.cantidad_disponible_actualizar.setText(str(libro[5]))
                self.fecha_publicacion_actualizar.setText(str(libro[6]))
            else:
                self.label_titulo.setText("Libro no encontrado")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")

    def buscar_libro_buscar(self):
        try:
            libro_id = self.libro_id_buscar.text().strip()
            
            if not libro_id:
                self.label_titulo.setText("Error: Ingrese un ID para buscar")
                return
            
            self.librodao.libro.libro_id = int(libro_id)
            datos = self.librodao.buscarLibro()
            
            if datos and len(datos) > 0:
                libro = datos[0]
                self.titulo_buscar.setText(str(libro[1]))
                self.autor_buscar.setText(str(libro[2]))
                self.isbn_buscar.setText(str(libro[3]))
                self.cantidad_total_buscar.setText(str(libro[4]))
                self.cantidad_disponible_buscar.setText(str(libro[5]))
                self.fecha_publicacion_buscar.setText(str(libro[6]))
            else:
                self.label_titulo.setText("Libro no encontrado")
                
        except Exception as e:
            self.label_titulo.setText(f"Error en búsqueda: {str(e)}")
    
    def actualizar_tabla(self):
        try:
            datos = self.librodao.listarLibros()
            self.tabla_libros.setRowCount(len(datos))
            fila = 0
            for item in datos:
                self.tabla_libros.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[0])))  # ID
                self.tabla_libros.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[1])))  # Título
                self.tabla_libros.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[2])))  # Autor
                self.tabla_libros.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item[3])))  # ISBN
                self.tabla_libros.setItem(fila, 4, QtWidgets.QTableWidgetItem(str(item[4])))  # Cantidad Total
                self.tabla_libros.setItem(fila, 5, QtWidgets.QTableWidgetItem(str(item[5])))  # Cantidad Disponible
                self.tabla_libros.setItem(fila, 6, QtWidgets.QTableWidgetItem(str(item[6])))  # Fecha Publicación
                fila += 1
                
            self.label_titulo.setText(f"Tabla actualizada - {len(datos)} libros encontrados")
            
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