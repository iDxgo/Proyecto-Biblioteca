# biblioteca.py
import reflex as rx
import pyodbc
from datetime import datetime
from pydantic import BaseModel

COLOR = "#7d1fa2"   #  <<--- EL COLOR PRINCIPAL

# ---------------------------
#   CONEXIÓN A SQL SERVER
# ---------------------------
def db():
    return pyodbc.connect(
        r'DRIVER={SQL Server};'
        r'SERVER=DESKTOP-SSUO5NK\SQLEXPRESS04;'
        r'DATABASE=Biblioteca;'
        r'Trusted_Connection=yes;'
    )

# ------------------------------------
#   MODELOS Pydantic
# ------------------------------------
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    isbn: str
    cantidad_total: int
    disponibles: int
    fecha_publicacion: str

class Prestamo(BaseModel):
    prestamo_id: int
    titulo: str
    autor: str
    fecha_prestamo: str
    fecha_devolucion: str
    fecha_devolucion_real: str | None
    estado: str
    dias_restantes: int

class Multa(BaseModel):
    multa_id: int
    titulo: str
    monto: float
    fecha_multa: str
    estado: str
    fecha_vencimiento: str
    dias_atraso: int

# ---------------------------
#      STATE PRINCIPAL
# ---------------------------
class BibliotecaState(rx.State):
    usuario_id: int | None = None
    nombre: str = ""
    autenticado: bool = False

    usuario_input: str = ""
    pass_input: str = ""
    login_error: str = ""

    libros: list[Libro] = []
    prestamos: list[Prestamo] = []
    multas: list[Multa] = []

    def intentar_login(self):
        try:
            conn = db()
            cursor = conn.cursor()
            cursor.execute("EXEC sp_AutenticarUsuario ?, ?", (self.usuario_input, self.pass_input))
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row:
                self.usuario_id = int(row[0])
                self.nombre = str(row[1])
                self.autenticado = True
                self.login_error = ""
                return rx.redirect("/biblioteca")
            else:
                self.login_error = "Credenciales incorrectas."
        except Exception as e:
            self.login_error = f"Error: {e}"

    def _format_date(self, val):
        if val is None:
            return ""
        if isinstance(val, datetime):
            return val.strftime("%Y-%m-%d %H:%M:%S")
        return str(val)

    def load_user(self):
        if not self.usuario_id:
            return
        self.cargar_libros()
        self.cargar_prestamos()
        self.cargar_multas()

    def cargar_libros(self):
        try:
            conn = db()
            cursor = conn.cursor()
            cursor.execute("EXEC sp_ObtenerLibros")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            self.libros = [
                Libro(
                    id=int(r[0]),
                    titulo=str(r[1]),
                    autor=str(r[2]),
                    isbn=str(r[3] or ""),
                    cantidad_total=int(r[4] or 0),
                    disponibles=int(r[5] or 0),
                    fecha_publicacion=self._format_date(r[6])
                ) for r in rows
            ]
        except Exception as e:
            print("Error cargando libros:", e)
            self.libros = []

    def cargar_prestamos(self):
        try:
            conn = db()
            cursor = conn.cursor()
            cursor.execute("EXEC sp_ObtenerPrestamosUsuario ?", (self.usuario_id,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            self.prestamos = [
                Prestamo(
                    prestamo_id=int(r[0]),
                    titulo=str(r[1]),
                    autor=str(r[2]),
                    fecha_prestamo=self._format_date(r[3]),
                    fecha_devolucion=self._format_date(r[4]),
                    fecha_devolucion_real=self._format_date(r[5]) if r[5] else None,
                    estado=str(r[6]),
                    dias_restantes=int(r[7] or 0),
                ) for r in rows
            ]
        except Exception as e:
            print("Error cargando préstamos:", e)
            self.prestamos = []

    def cargar_multas(self):
        try:
            conn = db()
            cursor = conn.cursor()
            cursor.execute("EXEC sp_ObtenerMultasUsuario ?", (self.usuario_id,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            self.multas = [
                Multa(
                    multa_id=int(r[0]),
                    titulo=str(r[1]),
                    monto=float(r[2]),
                    fecha_multa=self._format_date(r[3]),
                    estado=str(r[4]),
                    fecha_vencimiento=self._format_date(r[5]),
                    dias_atraso=int(r[6] or 0),
                ) for r in rows
            ]
        except Exception as e:
            print("Error cargando multas:", e)
            self.multas = []

    def pedir_prestamo(self, libro_id: int):
        try:
            if not self.usuario_id:
                print("Usuario no autenticado")
                return
            conn = db()
            cursor = conn.cursor()
            cursor.execute("EXEC sp_SolicitarPrestamo ?, ?", (self.usuario_id, int(libro_id)))
            conn.commit()
            cursor.close()
            conn.close()

            self.cargar_libros()
            self.cargar_prestamos()
        except Exception as e:
            print("Error solicitando préstamo:", e)

    def logout(self):
        self.usuario_id = None
        self.nombre = ""
        self.autenticado = False
        self.libros = []
        self.prestamos = []
        self.multas = []
        return rx.redirect("/")

# Componente de fondo Aurora
def aurora_background():
    return rx.box(
        style={
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "background": "linear-gradient(-45deg, #191654, #7d1fa2, #c95191, #7d1fa2, #191654)",
            "background_size": "400% 400%",
            "animation": "aurora_gradient 15s ease infinite",
            "z_index": "-1",
        }
    )

# ---------------------------
#       PÁGINA LOGIN
# ---------------------------
def login_page():
    return rx.fragment(
        rx.html("""
            <style>
                @keyframes aurora_gradient {
                    0% {
                        background-position: 0% 50%;
                    }
                    50% {
                        background-position: 100% 50%;
                    }
                    100% {
                        background-position: 0% 50%;
                    }
                }
            </style>
        """),
        rx.box(
            aurora_background(),
            rx.center(
                rx.box(
                    rx.card(
                        rx.vstack(
                            rx.heading("Iniciar sesión", size="6", color="white"),
                            rx.input(
                                placeholder="Usuario",
                                on_change=BibliotecaState.set_usuario_input,
                                value=BibliotecaState.usuario_input,
                            ),
                            rx.input(
                                placeholder="Contraseña",
                                type="password",
                                on_change=BibliotecaState.set_pass_input,
                                value=BibliotecaState.pass_input,
                            ),
                            rx.button(
                                "Entrar",
                                on_click=BibliotecaState.intentar_login,
                                width="100%",
                                bg="white",
                                color="#7d1fa2",
                            ),
                            rx.text(BibliotecaState.login_error, color="red"),
                            spacing="4",
                            width="22em",
                        ),
                        padding="6",
                        bg="#9a4cc0",
                        border_radius="12px",
                        box_shadow="0px 4px 12px rgba(0,0,0,0.3)",
                    ),
                    display="flex",
                    justify_content="center",
                    align_items="center",
                    height="100vh",
                    width="100%",
                ),
            ),
        )
    )

# ---------------------------
#     PÁGINA PRINCIPAL
# ---------------------------
def biblioteca_page():
    return rx.fragment(
        rx.html("""
            <style>
                @keyframes aurora_gradient {
                    0% {
                        background-position: 0% 50%;
                    }
                    50% {
                        background-position: 100% 50%;
                    }
                    100% {
                        background-position: 0% 50%;
                    }
                }
            </style>
        """),
        rx.box(
            aurora_background(),
            rx.cond(
                BibliotecaState.autenticado,

                rx.center(rx.vstack(
                    rx.hstack(
                        rx.heading(
                            f"Biblioteca — {BibliotecaState.nombre}",
                            size="4",
                            color=COLOR,
                            padding="4",
                            margin_y="2",
                            background_color="#1e1e1e",
                            border=f"2px solid {COLOR}",
                        ),
                        rx.spacer(),
                        rx.button("Cerrar sesión", on_click=BibliotecaState.logout, bg=COLOR, color="white"),
                    ),

                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger("Buscar libros", value="libros", color="white"),
                            rx.tabs.trigger("Mis préstamos", value="prestamos", color="white"),
                            rx.tabs.trigger("Multas", value="multas", color="white"),
                            background_color="#1e1e1e",
                        ),

                        # LIBROS
                        rx.tabs.content(
                            rx.vstack(
                                rx.text("Resultados:", size="2", color='white'),
                                rx.foreach(
                                    BibliotecaState.libros,
                                    lambda libro: rx.card(
                                        rx.hstack(
                                            rx.vstack(
                                                rx.text(libro.titulo, weight="bold", color=COLOR),
                                                rx.text(libro.autor),
                                                rx.text(f"ISBN: {libro.isbn}"),
                                                rx.text(f"Disponibles: {libro.disponibles}/{libro.cantidad_total}"),
                                                rx.text(f"Publicado: {libro.fecha_publicacion}"),
                                            ),
                                            rx.button(
                                                "Pedir",
                                                on_click=lambda _=None, id=libro.id: BibliotecaState.pedir_prestamo(id),
                                                disabled=(libro.disponibles <= 0),
                                                bg=COLOR,
                                                color="white",
                                            ),
                                        ),
                                        padding="4",
                                        margin_y="2",
                                        background_color="#1e1e1e",
                                        border=f"2px solid {COLOR}",
                                    )
                                )
                            ),
                            value="libros",
                        ),

                        # PRÉSTAMOS
                        rx.tabs.content(
                            rx.vstack(
                                rx.text("Mis préstamos:", size="2", color='white'),
                                rx.foreach(
                                    BibliotecaState.prestamos,
                                    lambda p: rx.card(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.vstack(
                                                    rx.text(p.titulo, weight="bold", color=COLOR),
                                                    rx.text(p.autor),
                                                ),
                                                rx.vstack(
                                                    rx.text(f"Salida: {p.fecha_prestamo}"),
                                                    rx.text(f"Límite: {p.fecha_devolucion}"),
                                                    rx.text(f"Días restantes: {p.dias_restantes}"),
                                                ),
                                            ),
                                            rx.text(f"Estado: {p.estado}", color=COLOR),
                                        ),
                                        padding="4",
                                        margin_y="2",
                                        background_color="#1e1e1e",
                                        border=f"2px solid {COLOR}",
                                    )
                                )
                            ),
                            value="prestamos",
                        ),

                        # MULTAS
                        rx.tabs.content(
                            rx.vstack(
                                rx.text("Multas:", size="2", color='white'),
                                rx.foreach(
                                    BibliotecaState.multas,
                                    lambda m: rx.card(
                                        rx.hstack(
                                            rx.vstack(
                                                rx.text(m.titulo, weight="bold", color=COLOR),
                                                rx.text(f"Monto: ${m.monto:.2f}"),
                                                rx.text(f"Fecha multa: {m.fecha_multa}"),
                                                rx.text(f"Atraso: {m.dias_atraso} días"),
                                            ),
                                            rx.vstack(
                                                rx.text(f"Estado: {m.estado}", color=COLOR),
                                                rx.text(f"Vence: {m.fecha_vencimiento}"),
                                            ),
                                        ),
                                        padding="4",
                                        margin_y="2",
                                        background_color="#1e1e1e",
                                        border=f"2px solid {COLOR}",
                                    )
                                )
                            ),
                            value="multas",
                        ),
                    ),),
                    on_mount=BibliotecaState.load_user,
                    padding="6",
                ),

                rx.center(
                    rx.vstack(
                        rx.heading("No autenticado", color=COLOR),
                        rx.link("Ir a login", href="/", color=COLOR),
                        spacing="4",
                    )
                )
            )
        )
    )

# ---------------------------
#        CONFIG APP
# ---------------------------
app = rx.App()
app.add_page(login_page, route="/")
app.add_page(biblioteca_page, route="/biblioteca", on_load=BibliotecaState.load_user)