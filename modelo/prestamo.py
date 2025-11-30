class Prestamo():
    def __init__(self):
        self.prestamo_id: int = 0
        self.usuario_id: int = 0
        self.libro_id: int = 0
        self.fecha_prestamo: str = ""
        self.fecha_devolucion: str = ""
        self.fecha_devolucion_real: str = ""
        self.estado: str = ""