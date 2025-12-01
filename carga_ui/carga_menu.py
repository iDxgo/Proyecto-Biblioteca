import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from carga_ui.carga_libros import Load_ui_libros
from carga_ui.carga_usuarios import Load_ui_usuarios
from carga_ui.carga_prestamos import Load_ui_prestamos
from carga_ui.carga_multas import Load_ui_multas


class Load_ui_menu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/menu.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.show()
        
        # Conectar botones
        self.boton_libros.clicked.connect(self.abrir_libros)
        self.boton_usuarios.clicked.connect(self.abrir_usuarios)
        self.boton_prestamos.clicked.connect(self.abrir_prestamos)
        self.boton_multas.clicked.connect(self.abrir_multas)
        self.boton_salir.clicked.connect(lambda: self.close())
    
    def abrir_libros(self):
        libros = Load_ui_libros()
        libros.show()
        self.close()
        
    def abrir_usuarios(self):
        usuarios = Load_ui_usuarios()
        usuarios.show()
        self.close()
        
    def abrir_prestamos(self):
        prestamos = Load_ui_prestamos()
        prestamos.show()
        self.close()
        
    def abrir_multas(self):
        multas = Load_ui_multas()
        multas.show()
        self.close()
    