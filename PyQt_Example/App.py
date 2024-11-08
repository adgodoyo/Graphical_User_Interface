import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_PATH, 'Iconos')

import sys
import requests
from PyQt5.QtWidgets import QAction, QGridLayout, QStackedWidget, QComboBox, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QScrollArea
from PyQt5.QtGui import QPixmap, QColor, QIcon, QFont, QFontDatabase, QCursor, QDesktopServices, QPainter
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QUrl, QTimer
import firebase_admin
from firebase_admin import credentials, auth, db

# Inicializa la aplicación de Firebase con tus credenciales
cred = credentials.Certificate(os.path.join(BASE_PATH,"CREDENCIALES.json"))
firebase_admin.initialize_app(cred, {
    'databaseURL': "REPLACE URL FIREBASE"
})

API_KEY = "API KEY"

#00C08C para el verde
#E6E1E1 Gris de la interfaz
#737070 Gris Textos

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(450, 800)
        self.setWindowTitle("Entrepeers")
        self.setWindowIcon(QIcon(os.path.join(IMAGE_PATH,"Entrepeers_ico.png")))
        regular_font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_PATH,"aptos.ttf"))
        regular_font_family = QFontDatabase.applicationFontFamilies(regular_font_id)[0]
        regular_font = QFont(regular_font_family)
        QApplication.setFont(regular_font)
        #self.setStyleSheet("""
                           #font-family: 'Aptos', serif; 
                           #font-size: 15pt;
                          # """)
        self.setStyleSheet(""" 
                           font-size: 15pt;
                           """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.stack = QStackedWidget()
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.stack)

        self.login_widget = Login(self)
        self.restablecercontrasena_widget = RestablecerContrasena(self)
        self.registro_widget = Registro(self)
        self.registro_interesado_widget = RegistroInteresado(self)
        self.registro_emprendedor_widget = RegistroEmprendedor(self)
        
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.restablecercontrasena_widget)
        self.stack.addWidget(self.registro_widget)
        self.stack.addWidget(self.registro_interesado_widget)
        self.stack.addWidget(self.registro_emprendedor_widget)
        
        self.show_login()

        self.stack.currentChanged.connect(self.update_stylesheet)

    def show_login(self):
        self.stack.setCurrentWidget(self.login_widget)

    def show_restablecercontrasena(self):
        self.stack.setCurrentWidget(self.restablecercontrasena_widget)

    def show_registro(self):
        self.stack.setCurrentWidget(self.registro_widget)

    def show_registrointeresado(self):
        self.stack.setCurrentWidget(self.registro_interesado_widget)
    
    def show_registroemprendedor(self):
        self.stack.setCurrentWidget(self.registro_emprendedor_widget)

    def show_menu_user(self, user, emprendimientos):
        self.menu_user_widget = Menu_user(self, user, emprendimientos)
        self.stack.addWidget(self.menu_user_widget)
        self.stack.setCurrentWidget(self.menu_user_widget)

    def show_menu_emp(self, emp, emprendimientos):
        self.menu_emp_widget = Menu_emp(self, emp, emprendimientos)
        self.stack.addWidget(self.menu_emp_widget)
        self.stack.setCurrentWidget(self.menu_emp_widget)

    def update_stylesheet(self, index):
        if index == 0:  # Login
            self.setStyleSheet("background-color: #E6E1E1;")
        elif index == 1:  # RestablecerContrasena
            self.setStyleSheet("background-color: #E6E1E1;")
        elif index == 2:  # Registro
            self.setStyleSheet("background-color: #00C08C;")
        elif index == 3:  # RegistroInteresado
            self.setStyleSheet("background-color: #E6E1E1;")
        elif index == 4:  # RegistroEmprendedor
            self.setStyleSheet("background-color: #E6E1E1;")
        elif index == 5:  # Menu
            self.setStyleSheet("background-color: white;")
        elif index == 6:  # Menu
            self.setStyleSheet("background-color: white;")
        #00C08C para el verde
        #E6E1E1 Gris de la interfaz
        #737070 Gris Textos

class Login(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        
        self.main_layout = QVBoxLayout(self)
        
        self.main_layout.addSpacing(20)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"logo_verde_gris.svg")).scaled(QSize(250, 250), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(logo)

        self.main_layout.addSpacing(20)

        # Crea un QHBoxLayout y añade espacios elásticos
        hbox = QHBoxLayout()

        # Añade un espacio elástico al principio del QHBoxLayout
        hbox.addStretch()

        # Crea el contenedor con estilo y el QVBoxLayout
        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)
        contenedor.setFixedWidth(400)

        vbox = QVBoxLayout(contenedor)

        button_google = QPushButton('Inicia sesión con Google', self)
        button_google.setIcon(QIcon(os.path.join(IMAGE_PATH,"Google.png")))
        button_google.setIconSize(QSize(32,32))
        button_google.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: #737070;
                border-radius: 25px;
                padding: 10 10px;
                font-size: 15pt;
                text-align: left;
                margin-top: 15px;
                margin-bottom: 15px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        vbox.addWidget(button_google)

        # Añade los QLineEdit al QVBoxLayout
        user_32 = os.path.join(IMAGE_PATH, "user_32.png").replace('\\', '/')
        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("Correo")
        self.correo_input.setStyleSheet(f"""
            QLineEdit {{
                background-image: url({user_32});
                background-repeat: no-repeat;
                background-position: left center;
                background-color: #E6E1E1;
                color: black;
                border-radius: 25px;
                font-size: 15pt; 
                height: 40px;
                padding: 10 45px;
                margin-top: 15px;
                margin-bottom: 15px;
                margin-left: 10px;
                margin-right: 10px;
            }}
        """)
        vbox.addWidget(self.correo_input)

        lock_32 = os.path.join(IMAGE_PATH, "lock_32.png").replace('\\', '/')
        self.contraseña_input = QLineEdit()
        self.contraseña_input.setPlaceholderText("Contraseña")
        self.contraseña_input.setEchoMode(QLineEdit.Password) 
        self.contraseña_input.setStyleSheet(f"""
            QLineEdit {{
                background-image: url({lock_32});
                background-repeat: no-repeat;
                background-position: left center;
                background-color: #E6E1E1;
                color: black;
                font-size: 15pt; 
                border-radius: 25px;
                height: 40px;
                padding: 10 45px;
                margin-top: 15px;
                margin-bottom: 5px;
                margin-left: 10px;
                margin-right: 10px;
            }}
        """)
        vbox.addWidget(self.contraseña_input)

        olvidado = ClickableLabel("¿Olvidaste tu contraseña?")
        olvidado.setStyleSheet("font-size: 12px; color: blue;")
        olvidado.clicked.connect(self.mostrar_restablecer_contrasena)
        vbox.addWidget(olvidado)

        button_login = QPushButton('Login', self)
        button_login.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 25px;
                padding: 12 30px;
                font-weight: bold;
                font-size: 20pt;
                text-align: center;
                margin-top: 15px;
                margin-bottom: 5px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        button_login.clicked.connect(self.firebase_login)
        vbox.addWidget(button_login)

        creacion_cuenta = QHBoxLayout()
        creacion_cuenta.setContentsMargins(0, 0, 0, 15)

        creacion_cuenta.addStretch()

        pregunta = QLabel("¿No estás registrado?")
        pregunta.setStyleSheet("font-size: 12px;")
        pregunta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        creacion_cuenta.addWidget(pregunta)

        crear = ClickableLabel("Crear una Cuenta")
        crear.setStyleSheet("font-size: 12px; color: blue;")
        crear.clicked.connect(self.mostrar_registro)
        creacion_cuenta.addWidget(crear)

        creacion_cuenta.addStretch()

        vbox.addLayout(creacion_cuenta)

        # Añade el contenedor al QHBoxLayout
        hbox.addWidget(contenedor)

        # Añade un espacio elástico al final del QHBoxLayout
        hbox.addStretch()

        # Añade el QHBoxLayout al layout principal
        self.main_layout.addLayout(hbox)

        self.error_message_label = QLabel("")
        self.error_message_label.setStyleSheet("font-size: 12pt;")
        self.error_message_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.error_message_label)

        self.main_layout.addStretch()
    
    def firebase_login(self):
        self.error_message_label.clear()
        correo = self.correo_input.text()
        contraseña = self.contraseña_input.text()

        # URL de la REST API para iniciar sesión
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

        # Datos de la solicitud
        data = {
            "email": correo,
            "password": contraseña,
            "returnSecureToken": True
        }

        # Realiza la solicitud POST para iniciar sesión
        response = requests.post(url, json=data)
        ## print(response.json())

        # Verifica la respuesta
        if response.ok:
            user_id = response.json()["localId"]
            ref_usuarios = db.reference(f"usuarios/{user_id}")
            ref_emprendedores = db.reference(f"emprendedores/{user_id}")
            emprendimientos = db.reference("emprendedores").get()
            self.user_data_usuarios = ref_usuarios.get()
            self.user_data_emprendedores = ref_emprendedores.get()

            if self.user_data_usuarios:
                self.main_window.show_menu_user(self.user_data_usuarios, emprendimientos)
            elif self.user_data_emprendedores:
                self.main_window.show_menu_emp(self.user_data_emprendedores, emprendimientos)
        else:
            self.error_message_label.setText("Credenciales incorrectas.")
    
    def mostrar_registro(self):
        self.main_window.show_registro() 

    def mostrar_restablecer_contrasena(self):
        self.main_window.show_restablecercontrasena()   

class RestablecerContrasena(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        contenedor_layout.addSpacing(20)

        tittle = QLabel("OLVIDASTE LA\nCONTRASEÑA")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""color: white;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(tittle)

        contenedor_layout.addSpacing(20)

        layout.addWidget(contenedor)

        layout.addSpacing(20)

        candado = QLabel()
        candado.setPixmap(QPixmap(os.path.join(IMAGE_PATH, "password.png")).scaled(QSize(100, 100), Qt.KeepAspectRatio))
        candado.setAlignment(Qt.AlignCenter)
        layout.addWidget(candado)

        layout.addSpacing(20)

        subtittle = QLabel("¿Problemas para entrar?")
        subtittle.setAlignment(Qt.AlignCenter)
        subtittle.setStyleSheet("""
                                color: black; 
                                font-weight: bold; 
                                font-size: 15pt; 
                                text-align: center
                                """)
        layout.addWidget(subtittle)

        layout.addSpacing(15)

        text = QLabel("Escribe tu email para\nreestablecer tu contraseña")
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("color: black; font-size: 12pt; text-align: center")
        layout.addWidget(text)

        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("Correo electrónico")
        self.correo_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                font-size: 15pt; 
                border-radius: 25px;
                height: 40px;
                padding: 10 30px;
                margin-top: 30px;
                margin-bottom: 15px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        layout.addWidget(self.correo_input)

        enviar_button = QPushButton("Recuperar contraseña")
        enviar_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 25px;
                padding: 12 30px;
                font-weight: bold;
                font-size: 18pt;
                text-align: center;
                margin-top: 15px;
                margin-bottom: 5px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        enviar_button.clicked.connect(self.enviar_solicitud)
        layout.addWidget(enviar_button)

        self.mensaje_estado = QLabel("")
        self.mensaje_estado.setAlignment(Qt.AlignCenter)
        self.mensaje_estado.setStyleSheet("color: #737070; font-size: 9pt;")
        layout.addWidget(self.mensaje_estado)

        layout.addStretch()

        volver_button = QPushButton("Volver a inicio de sesión")
        volver_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 10px;
                padding: 12 30px;
                font-size: 15pt;
                text-align: center;
                margin-top: 15px;
            }
        """)
        volver_button.clicked.connect(self.volver_a_login)
        layout.addWidget(volver_button)

    def enviar_solicitud(self):
        correo = self.correo_input.text()

        if not correo:
            self.mensaje_estado.setText("Por favor, ingresa tu correo electrónico.")
            return

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={API_KEY}"
        data = {
            "requestType": "PASSWORD_RESET",
            "email": correo
        }
        response = requests.post(url, json=data)

        if response.ok:
            self.mensaje_estado.setText("Se ha enviado un correo para restablecer tu contraseña.")
        else:
            self.mensaje_estado.setText("No se pudo enviar el correo. Verifica que el correo electrónico sea correcto.")

    
    def volver_a_login(self):
        self.main_window.show_login()   

class Registro(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        
        layout = QVBoxLayout(self)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_PATH, "cohete_verde_gris.svg")).scaled(QSize(150, 150), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        contenedor_layout.addWidget(logo)

        layout.addWidget(contenedor)

        layout.addSpacing(15)

        tittle = QLabel("¿QUÉ TIPO DE\nUSUARIO ERES?")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""color: white; font-weight: bold; font-size: 30pt; text-align: center;""")
        layout.addWidget(tittle)

        layout.addSpacing(15)

        hbox = QHBoxLayout()

        # Añade un espacio elástico al principio del QHBoxLayout
        hbox.addSpacing(15)

        # Crea el contenedor con estilo y el QVBoxLayout
        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 20px;
            }
        """)
        contenedor.setFixedWidth(400)

        vbox = QVBoxLayout(contenedor)

        self.interesado_button = QPushButton("Interesado por el mundo\ndel emprendimiento")
        self.interesado_button.setIcon(QIcon(os.path.join(IMAGE_PATH,"account.png")))
        self.interesado_button.setIconSize(QSize(32,32))
        self.interesado_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: black;
                border-radius: 25px;
                text-align: left;
                font-size: 15pt;
                padding: 10 10px;
                margin-top: 60px;
                margin-bottom: 15px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        self.interesado_button.clicked.connect(self.mostrar_registro_interesado)
        vbox.addWidget(self.interesado_button)

        self.emprendedor_button = QPushButton("Tengo un\nemprendimiento")
        self.emprendedor_button.clicked.connect(self.mostrar_registro_emprendedor)
        self.emprendedor_button.setIcon(QIcon(os.path.join(IMAGE_PATH, "rocket_registration.png")))
        self.emprendedor_button.setIconSize(QSize(32,32))
        self.emprendedor_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: black;
                border-radius: 25px;
                text-align: left;
                font-size: 15pt;
                padding: 10 10px;
                margin-top: 15px;
                margin-bottom: 60px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        vbox.addWidget(self.emprendedor_button)

        # Añade el contenedor al QHBoxLayout
        hbox.addWidget(contenedor)

        # Añade un espacio elástico al final del QHBoxLayout
        hbox.addSpacing(15)

        # Añade el QHBoxLayout al layout principal
        layout.addLayout(hbox)

        layout.addStretch()

        volver_button = QPushButton("Volver a inicio de sesión")
        volver_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #00C08C;
                border-radius: 10px;
                padding: 12 30px;
                font-size: 15pt;
                text-align: center;
                margin-top: 15px;
            }
        """)
        volver_button.clicked.connect(self.volver_a_login)
        layout.addWidget(volver_button)

    def volver_a_login(self):
        self.main_window.show_login()     

    def mostrar_registro_interesado(self):
        self.main_window.show_registrointeresado()

    def mostrar_registro_emprendedor(self):
        self.main_window.show_registroemprendedor()

class RegistroInteresado(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        contenedor_layout.addSpacing(20)
        
        tittle = QLabel("CREA TU CUENTA")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""color: white;
                            font-weight: bold;
                            font-size: 30pt;
                            text-align: center
                            """)
        
        contenedor_layout.addWidget(tittle)

        contenedor_layout.addSpacing(20)

        layout.addWidget(contenedor)
        

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre")
        self.nombre_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #737070;
                font-size: 12pt;
                border-radius: 25px;
                height: 40px;
                padding: 10 30px;
                margin-top: 30px;
                margin-bottom: 15px;
                margin-left: 40px;
                margin-right: 40px;
            }
        """)
        layout.addWidget(self.nombre_input)

        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Usuario")
        self.usuario_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #737070;
                font-size: 12pt;
                border-radius: 25px;
                height: 40px;
                padding: 10 30px;
                margin-top: 15px;
                margin-bottom: 15px;
                margin-left: 40px;
                margin-right: 40px;
            }
        """)
        layout.addWidget(self.usuario_input)

        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("Correo electrónico")
        self.correo_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #737070;
                font-size: 12pt;
                border-radius: 25px;
                height: 40px;
                padding: 10 30px;
                margin-top: 15px;
                margin-bottom: 15px;
                margin-left: 40px;
                margin-right: 40px;
            }
        """)
        layout.addWidget(self.correo_input)

        self.contraseña_input = QLineEdit()
        self.contraseña_input.setPlaceholderText("Contraseña")
        self.contraseña_input.setEchoMode(QLineEdit.Password)
        self.contraseña_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #737070;
                font-size: 12pt;
                border-radius: 25px;
                height: 40px;
                padding: 10 30px;
                margin-top: 15px;
                margin-bottom: 15px;
                margin-left: 40px;
                margin-right: 40px;
            }
        """)
        layout.addWidget(self.contraseña_input)

        self.categoria_input = QComboBox()
        self.categoria_input.addItem("Categoría de interés")  # Opción por defecto
        self.categoria_input.addItems(["Tecnología", "Salud", "Educación", "Finanzas", "Moda", "Logística", "Finanzas" "Arte", "Otra"])
        self.categoria_input.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #737070;
                font-size: 12pt;
                border-radius: 25px;
                padding: 12px 30px;
                margin-top: 15px;
                margin-bottom: 15px;
                margin-left: 40px;
                margin-right: 40px;
                min-height: 30px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(iconos/arrow_down_16.png);
                padding-right: 35px;
            }
            QComboBox QAbstractItemView {
                border: 1px #E6E1E1;
                selection-background-color: #E6E1E1;
                color: #737070;
                background-color: #E6E1E1;
                border-radius: 15px;
            }
        """)
        layout.addWidget(self.categoria_input)

        registrar_button = QPushButton("Crear Cuenta")
        registrar_button.clicked.connect(self.registrar_usuario)
        registrar_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 25px;
                padding: 12 30px;
                font-weight: bold;
                font-size: 20pt;
                text-align: center;
                margin-top: 15px;
                margin-bottom:5px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        layout.addWidget(registrar_button)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("font-size: 10pt; color: #737070;")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        layout.addStretch()

        volver_button = QPushButton("Volver")
        volver_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #00C08C;
                border-radius: 10px;
                padding: 12 30px;
                font-size: 15pt;
                text-align: center;
                margin-top: 15px;
            }
        """)
        volver_button.clicked.connect(self.volver_a_registro)
        layout.addWidget(volver_button)

        layout.addStretch()
        

    def volver_a_registro(self):
        self.main_window.show_registro()  
    
    def volver_a_login(self):
    # QTimer.singleShot espera 3000 milisegundos (3 segundos) antes de ejecutar self.main_window.show_login
        QTimer.singleShot(3000, self.main_window.show_login)

    def registrar_usuario(self):
        self.message_label.setText("")
        nombre = self.nombre_input.text()
        usuario = self.usuario_input.text()
        correo = self.correo_input.text()
        contraseña = self.contraseña_input.text()
        categoria = self.categoria_input.currentText()
        if not (nombre and usuario and correo and contraseña and categoria != "Categoría de interés"):
            self.message_label.setText("Error, Por favor, completa todos los campos.")
            return
        
        url_check = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={API_KEY}"
        data_check = {"email": [correo]}
        response_check = requests.post(url_check, json=data_check)
        if response_check.ok and "users" in response_check.json() and response_check.json()["users"]:
            self.message_label.setText("Error. El correo electrónico ya está registrado.")
            return 

        # Registra el usuario en Firebase Authentication
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
        data = {
            "email": correo,
            "password": contraseña,
            "returnSecureToken": True
        }
        response = requests.post(url, json=data)
        if response.ok:
            user_id = response.json()["localId"]

            # Guarda los datos adicionales del usuario en Firebase Realtime Database
            ref = db.reference(f"usuarios/{user_id}")
            ref.set({
                "nombre": nombre,
                "usuario": usuario,
                "categoria": categoria,
                "tipo": "interesado"
            })

            self.message_label.setText("Registro exitoso, Usuario registrado con éxito.")
            self.volver_a_login()
        else:
            self.message_label.setText("Error, No se pudo registrar al usuario.")

class RegistroEmprendedor(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        contenedor_layout.addSpacing(20)
        
        tittle = QLabel("CREA TU CUENTA")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 30pt;
            text-align: center
        """)
        
        contenedor_layout.addWidget(tittle)

        contenedor_layout.addSpacing(20)

        layout.addWidget(contenedor)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del emprendimiento")
        self.nombre_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #737070;
                font-size: 12pt;
                border-radius: 25px;
                height: 40px;
                padding: 10 30px;
                margin-top: 30px;
                margin-bottom: 15px;
                margin-left: 40px;
                margin-right: 40px;
            }
        """)
        layout.addWidget(self.nombre_input)

        self.descripcion_input = QLineEdit()
        self.descripcion_input.setPlaceholderText("Descripción")
        self.descripcion_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #737070;
                font-size: 12pt;
                border-radius: 25px;
                height: 40px;
                padding: 10 30px;
                margin-top: 15px;
                margin-bottom: 15px;
                margin-left: 40px;
                margin-right: 40px;
            }
        """)
        layout.addWidget(self.descripcion_input)

        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("Correo electrónico")
        self.correo_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #737070;
                font-size: 12pt;
                border-radius: 25px;
                height: 40px;
                padding: 10 30px;
                margin-top: 15px;
                margin-bottom: 15px;
                margin-left: 40px;
                margin-right: 40px;
            }
        """)
        layout.addWidget(self.correo_input)

        self.contraseña_input = QLineEdit()
        self.contraseña_input.setPlaceholderText("Contraseña")
        self.contraseña_input.setEchoMode(QLineEdit.Password)
        self.contraseña_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #737070;
                font-size: 12pt;
                border-radius: 25px;
                height: 40px;
                padding: 10 30px;
                margin-top: 15px;
                margin-bottom: 15px;
                margin-left: 40px;
                margin-right: 40px;
            }
        """)
        layout.addWidget(self.contraseña_input)

        self.categoria_input = QComboBox()
        self.categoria_input.addItem("Categoría")  # Opción por defecto
        self.categoria_input.addItems(["Tecnología", "Salud", "Educación", "Finanzas", "Moda", "Logística", "Finanzas", "Arte", "Otra"])
        self.categoria_input.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #737070;
                font-size: 12pt;
                border-radius: 25px;
                padding: 12px 30px;
                margin-top: 15px;
                margin-bottom: 15px;
                margin-left: 40px;
                margin-right: 40px;
                min-height: 30px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(iconos/arrow_down_16.png);
                padding-right: 35px;
            }
            QComboBox QAbstractItemView {
                border: 1px #E6E1E1;
                selection-background-color: #E6E1E1;
                color: #737070;
                background-color: #E6E1E1;
                border-radius: 15px;
            }
        """)
        layout.addWidget(self.categoria_input)

        registrar_button = QPushButton("Crear Cuenta")
        registrar_button.clicked.connect(self.registrar_emprendedor)
        registrar_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 25px;
                padding: 12 30px;
                font-weight: bold;
                font-size: 20pt;
                text-align: center;
                margin-top: 15px;
                margin-bottom:5px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        layout.addWidget(registrar_button)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("font-size: 10pt; color: #737070;")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        layout.addStretch()

        volver_button = QPushButton("Volver")
        volver_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #00C08C;
                border-radius: 10px;
                padding: 12 30px;
                font-size: 15pt;
                text-align: center;
                margin-top: 15px;
            }
        """)
        volver_button.clicked.connect(self.volver_a_registro)
        layout.addWidget(volver_button)
        
        layout.addStretch()

    def volver_a_login(self):
    # QTimer.singleShot espera 3000 milisegundos (3 segundos) antes de ejecutar self.main_window.show_login
        QTimer.singleShot(3000, self.main_window.show_login)

    def volver_a_registro(self):
        self.main_window.show_registro() 

    def registrar_emprendedor(self):
        self.message_label.setText("")
        nombre = self.nombre_input.text()
        descripcion = self.descripcion_input.text()
        correo = self.correo_input.text()
        contraseña = self.contraseña_input.text()
        categoria = self.categoria_input.currentText()
        if not (nombre and descripcion and correo and contraseña and categoria != "Categoría"):
            self.message_label.setText("Error, Por favor, completa todos los campos.")
            return
        
        url_check = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={API_KEY}"
        data_check = {"email": [correo]}
        response_check = requests.post(url_check, json=data_check)
        if response_check.ok and "users" in response_check.json() and response_check.json()["users"]:
            self.message_label.setText("Error, El correo electrónico ya está registrado.")
            return 

        # Registra el emprendedor en Firebase Authentication
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
        data = {
            "email": correo,
            "password": contraseña,
            "returnSecureToken": True
        }
        response = requests.post(url, json=data)
        if response.ok:
            user_id = response.json()["localId"]

            # Guarda los datos adicionales del emprendedor en Firebase Realtime Database
            ref = db.reference(f"emprendedores/{user_id}")
            ref.set({
                "nombre": nombre,
                "descripcion": descripcion,
                "categoria": categoria,
                "tipo": "emprendedor"
            })

            self.message_label.setText("Registro exitoso, Emprendedor registrado con éxito.")
            self.volver_a_login()
        else:
            self.message_label.setText("Error, No se pudo registrar al emprendedor.")

class Menu_user(QWidget):
    def __init__(self, main_window, user, emprendimientos):
        super().__init__()
        self.main_window = main_window
        self.user = user
        self.emprendimientos = emprendimientos
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.stack2 = QStackedWidget()
        self.stack2.addWidget(Feed(self)) 
        self.stack2.addWidget(Directorio(self, self.emprendimientos))
        self.stack2.addWidget(Perfil_user(self, self.user))
        self.stack2.addWidget(Config_user(self))
        self.stack2.addWidget(Membresias(self))
        self.stack2.addWidget(Conocenos(self))
        self.stack2.addWidget(Silver(self))
        self.stack2.addWidget(Gold(self))
        self.stack2.addWidget(Emerald(self))
        self.stack2.addWidget(Emprendimiento1(self))
        self.stack2.addWidget(Emprendimiento2(self))
        self.stack2.addWidget(Emprendimiento3(self))
        self.stack2.addWidget(Emprendimiento4(self))
        self.stack2.addWidget(Emprendimiento5(self))
        self.stack2.addWidget(Emprendimiento6(self))
        self.stack2.addWidget(Emprendimiento7(self))
        layout.addWidget(self.stack2)

        self.icono_activo_feed = QIcon(os.path.join(IMAGE_PATH, "home_selected.png"))
        self.icono_inactivo_feed = QIcon(os.path.join(IMAGE_PATH, "home.png"))

        self.icono_activo_dir = QIcon(os.path.join(IMAGE_PATH, "rocket_selected.png"))
        self.icono_inactivo_dir = QIcon(os.path.join(IMAGE_PATH, "rocket.png"))

        self.icono_activo_perfil = QIcon(os.path.join(IMAGE_PATH, "profile_selected.png"))
        self.icono_inactivo_perfil = QIcon(os.path.join(IMAGE_PATH, "profile.png"))

        self.icono_activo_config = QIcon(os.path.join(IMAGE_PATH, "menu_green.png"))
        self.icono_inactivo_config = QIcon(os.path.join(IMAGE_PATH, "menu_green.png"))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(0)
        self.button_feed = QPushButton()
        self.button_feed.setIcon(self.icono_activo_feed)
        self.button_feed.setIconSize(QSize(40,40))
        self.button_feed.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: white;
                font-weight: bold;
                font-size: 20pt;
                text-align: center;
                padding: 10 5px;
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                border: none;
            }
        """)
        self.button_dir = QPushButton()
        self.button_dir.setIcon(self.icono_inactivo_dir)
        self.button_dir.setIconSize(QSize(40,40))
        self.button_dir.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: white;
                font-weight: bold;
                font-size: 20pt;
                text-align: center;
                padding: 10 5px;
                border: none;
            }
        """)
        self.button_perfil = QPushButton()
        self.button_perfil.setIcon(self.icono_inactivo_perfil)
        self.button_perfil.setIconSize(QSize(40,40))
        self.button_perfil.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: white;
                font-weight: bold;
                padding: 10 5px;
                font-size: 20pt;
                text-align: center;
                border: none;
            }
        """)
        self.button_config = QPushButton()
        self.button_config.setIcon(self.icono_inactivo_config)
        self.button_config.setIconSize(QSize(40,40))
        self.button_config.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: white;
                font-weight: bold;
                padding: 10 5px;
                font-size: 20pt;
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
                text-align: center;
                border: none;
            }
        """)
        self.button_feed.clicked.connect(self.on_feed_clicked)
        self.button_dir.clicked.connect(self.on_dir_clicked)
        self.button_perfil.clicked.connect(self.on_perfil_clicked)
        self.button_config.clicked.connect(self.on_config_clicked)
        button_layout.addWidget(self.button_feed)
        button_layout.addWidget(self.button_dir)
        button_layout.addWidget(self.button_perfil)
        button_layout.addWidget(self.button_config)
        layout.addLayout(button_layout)

    def changeStackIndex(self, index):
        self.stack2.setCurrentIndex(index)
    
    def on_feed_clicked(self):
        self.stack2.setCurrentIndex(0)
        self.button_feed.setIcon(self.icono_activo_feed)
        self.button_dir.setIcon(self.icono_inactivo_dir)
        self.button_perfil.setIcon(self.icono_inactivo_perfil)
        self.button_config.setIcon(self.icono_inactivo_config)

    def on_dir_clicked(self):
        self.stack2.setCurrentIndex(1)
        self.button_feed.setIcon(self.icono_inactivo_feed)
        self.button_dir.setIcon(self.icono_activo_dir)
        self.button_perfil.setIcon(self.icono_inactivo_perfil)
        self.button_config.setIcon(self.icono_inactivo_config)

    def on_perfil_clicked(self):
        self.stack2.setCurrentIndex(2)
        self.button_feed.setIcon(self.icono_inactivo_feed)
        self.button_dir.setIcon(self.icono_inactivo_dir)
        self.button_perfil.setIcon(self.icono_activo_perfil)
        self.button_config.setIcon(self.icono_inactivo_config)

    def on_config_clicked(self):
        self.stack2.setCurrentIndex(3)
        self.button_feed.setIcon(self.icono_inactivo_feed)
        self.button_dir.setIcon(self.icono_inactivo_dir)
        self.button_perfil.setIcon(self.icono_inactivo_perfil)
        self.button_config.setIcon(self.icono_activo_config)

    def on_emprendimiento_user_clicked(self, nombre, descripcion, categoria):
        # Asegúrate de que el widget de emprendimiento usuario se crea correctamente
        emprendimiento_user = EmprendimientoUser(self, nombre, descripcion, categoria)
        self.stack2.addWidget(emprendimiento_user)
        index = self.stack2.indexOf(emprendimiento_user)  # Obtén el índice del nuevo widget
        self.stack2.setCurrentIndex(index) 

class Menu_emp(QWidget):
    def __init__(self, main_window, emp, emprendimientos):
        super().__init__()
        self.main_window = main_window
        self.emp = emp
        self.emprendimientos = emprendimientos
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.stack2 = QStackedWidget()
        self.stack2.addWidget(Feed(self)) 
        self.stack2.addWidget(Directorio(self, self.emprendimientos))
        self.stack2.addWidget(Perfil_emp(self, self.emp))
        self.stack2.addWidget(Config_emp(self))
        self.stack2.addWidget(Membresias(self))
        self.stack2.addWidget(Conocenos(self))
        self.stack2.addWidget(Silver(self))
        self.stack2.addWidget(Gold(self))
        self.stack2.addWidget(Emerald(self))
        self.stack2.addWidget(Emprendimiento1(self))
        self.stack2.addWidget(Emprendimiento2(self))
        self.stack2.addWidget(Emprendimiento3(self))
        self.stack2.addWidget(Emprendimiento4(self))
        self.stack2.addWidget(Emprendimiento5(self))
        self.stack2.addWidget(Emprendimiento6(self))
        self.stack2.addWidget(Emprendimiento7(self))
        layout.addWidget(self.stack2)

        self.icono_activo_feed = QIcon(os.path.join(IMAGE_PATH, "home_selected.png"))
        self.icono_inactivo_feed = QIcon(os.path.join(IMAGE_PATH, "home.png"))

        self.icono_activo_dir = QIcon(os.path.join(IMAGE_PATH, "rocket_selected.png"))
        self.icono_inactivo_dir = QIcon(os.path.join(IMAGE_PATH, "rocket.png"))

        self.icono_activo_perfil = QIcon(os.path.join(IMAGE_PATH, "profile_selected.png"))
        self.icono_inactivo_perfil = QIcon(os.path.join(IMAGE_PATH, "profile.png"))

        self.icono_activo_config = QIcon(os.path.join(IMAGE_PATH, "menu_green.png"))
        self.icono_inactivo_config = QIcon(os.path.join(IMAGE_PATH, "menu_green.png"))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(0)
        self.button_feed = QPushButton()
        self.button_feed.setIcon(self.icono_activo_feed)
        self.button_feed.setIconSize(QSize(40,40))
        self.button_feed.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: white;
                font-weight: bold;
                font-size: 20pt;
                text-align: center;
                padding: 10 5px;
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                border: none;
            }
        """)
        self.button_dir = QPushButton()
        self.button_dir.setIcon(self.icono_inactivo_dir)
        self.button_dir.setIconSize(QSize(40,40))
        self.button_dir.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: white;
                font-weight: bold;
                font-size: 20pt;
                text-align: center;
                padding: 10 5px;
                border: none;
            }
        """)
        self.button_perfil = QPushButton()
        self.button_perfil.setIcon(self.icono_inactivo_perfil)
        self.button_perfil.setIconSize(QSize(40,40))
        self.button_perfil.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: white;
                font-weight: bold;
                padding: 10 5px;
                font-size: 20pt;
                text-align: center;
                border: none;
            }
        """)
        self.button_config = QPushButton()
        self.button_config.setIcon(self.icono_inactivo_config)
        self.button_config.setIconSize(QSize(40,40))
        self.button_config.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: white;
                font-weight: bold;
                padding: 10 5px;
                font-size: 20pt;
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
                text-align: center;
                border: none;
            }
        """)
        self.button_feed.clicked.connect(self.on_feed_clicked)
        self.button_dir.clicked.connect(self.on_dir_clicked)
        self.button_perfil.clicked.connect(self.on_perfil_clicked)
        self.button_config.clicked.connect(self.on_config_clicked)
        button_layout.addWidget(self.button_feed)
        button_layout.addWidget(self.button_dir)
        button_layout.addWidget(self.button_perfil)
        button_layout.addWidget(self.button_config)
        layout.addLayout(button_layout)

    def changeStackIndex(self, index):
        self.stack2.setCurrentIndex(index)
    
    def on_feed_clicked(self):
        self.stack2.setCurrentIndex(0)
        self.button_feed.setIcon(self.icono_activo_feed)
        self.button_dir.setIcon(self.icono_inactivo_dir)
        self.button_perfil.setIcon(self.icono_inactivo_perfil)
        self.button_config.setIcon(self.icono_inactivo_config)

    def on_dir_clicked(self):
        self.stack2.setCurrentIndex(1)
        self.button_feed.setIcon(self.icono_inactivo_feed)
        self.button_dir.setIcon(self.icono_activo_dir)
        self.button_perfil.setIcon(self.icono_inactivo_perfil)
        self.button_config.setIcon(self.icono_inactivo_config)

    def on_perfil_clicked(self):
        self.stack2.setCurrentIndex(2)
        self.button_feed.setIcon(self.icono_inactivo_feed)
        self.button_dir.setIcon(self.icono_inactivo_dir)
        self.button_perfil.setIcon(self.icono_activo_perfil)
        self.button_config.setIcon(self.icono_inactivo_config)

    def on_config_clicked(self):
        self.stack2.setCurrentIndex(3)
        self.button_feed.setIcon(self.icono_inactivo_feed)
        self.button_dir.setIcon(self.icono_inactivo_dir)
        self.button_perfil.setIcon(self.icono_inactivo_perfil)
        self.button_config.setIcon(self.icono_activo_config)

    def on_emprendimiento_user_clicked(self, nombre, descripcion, categoria):
        # Asegúrate de que el widget de emprendimiento usuario se crea correctamente
        emprendimiento_user = EmprendimientoUser(self, nombre, descripcion, categoria)
        self.stack2.addWidget(emprendimiento_user)
        index = self.stack2.indexOf(emprendimiento_user)  # Obtén el índice del nuevo widget
        self.stack2.setCurrentIndex(index) 

class Feed(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"logotipo_negro.svg")).scaled(QSize(200,600), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        contenedor_layout.addWidget(logo)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        evento_color = QWidget()
        evento_color_layout = QVBoxLayout(evento_color)
        evento_color.setStyleSheet("""
                    QWidget {
                       background-color: #E6E1E1;
                        border-radius: 10px;
                    }
                """)
        evento_contenedor = ClickableWidget()
        evento_contenedor.setFixedHeight(150)
        
        evento_contenedor.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://gamechangers.com.co/")))
        hbox_evento = QHBoxLayout(evento_contenedor)
        imagen_evento = QPixmap(os.path.join(IMAGE_PATH,"evento1.png"))
        imagen_evento = imagen_evento.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_evento_label = QLabel()
        imagen_evento_label.setPixmap(imagen_evento)

        vbox_evento = QVBoxLayout()
        tittle_evento = QLabel("Game Changers Fest 2024")
        tittle_evento.setStyleSheet("""
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: black;
                                    """)
        #tittle_evento.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox_evento.addWidget(tittle_evento)

        desc_evento = QLabel("""Abril 26, 27 y 28
Conocimiento, hábitos y estrategias de expertos y líderes.
El lugar correcto para crear conexiones de valor ideales.
""")
        desc_evento.setStyleSheet("""
                                    font-size: 12px;
                                    color: black;
                                    """)
        desc_evento.setFixedWidth(250)  # Establece el tamaño fijo (ancho, alto)
        desc_evento.setWordWrap(True)
        #desc_evento.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox_evento.addWidget(desc_evento)
        vbox_evento.addStretch()

        hbox_evento.addWidget(imagen_evento_label)
        hbox_evento.addLayout(vbox_evento)

        evento_color_layout.addWidget(evento_contenedor)

        content_layout.addWidget(evento_color)
        
# Contenido Destacado
        tittle_contenido = QLabel("Contenido Destacado")
        tittle_contenido.setStyleSheet("""
                                    font-size: 32px;
                                    font-weight: bold;
                                    color: black;
                                    margin-top: 20px;
                                    margin-bottom: 5px;
                                    """)
        tittle_contenido.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(tittle_contenido)

        division1 = QWidget()
        division1.setFixedHeight(10)
        division1.setStyleSheet("""
            QWidget {
                background-color: #00C08C;  /* Color de fondo */
                border-radius: 5px;  /* Radio del borde para esquinas redondeadas */
            }
        """)
        content_layout.addWidget(division1)

        destacado_contenedor = QWidget()
        destacado_layout = QVBoxLayout(destacado_contenedor)
        hbox_destacado1 = QHBoxLayout()

# Destacado 1
        vbox1_click = ClickableWidget()
        vbox1_click_layout = QVBoxLayout(vbox1_click)
        vbox1_click.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.infobae.com/colombia/2024/04/09/en-colombia-75-de-100-empresas-fracasan-en-tres-anos-segun-director-de-reconocido-festival-de-emprendimientos/")))
        vbox1 = QWidget()
        vbox1.setFixedWidth(150)
        vbox1.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;  /* Color de fondo */
                border-radius: 15px;  /* Radio del borde para esquinas redondeadas */
            }
        """)
        vbox1_layout = QVBoxLayout(vbox1)

        imagen1 = QPixmap(os.path.join(IMAGE_PATH,"noticia1.jpg"))
        imagen1 = imagen1.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen1_label = QLabel()
        imagen1_label.setPixmap(imagen1)
        imagen1_label.setAlignment(Qt.AlignCenter)

        vbox1_layout.addWidget(imagen1_label)

        tittle_hbox1 = QLabel("En Colombia, 75 de cada 100 empresas que se crean fracasan en tres años: cuál es la razón")
        tittle_hbox1.setStyleSheet("""
                                    font-size: 12px;
                                    font-weight: bold;
                                    color: black;
                                    """)
        tittle_hbox1.setWordWrap(True)
        tittle_hbox1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox1_layout.addWidget(tittle_hbox1)

        vbox1_click_layout.addWidget(vbox1)
        hbox_destacado1.addWidget(vbox1_click)

    # Destacado 2

        vbox2_click = ClickableWidget()
        vbox2_click_layout = QVBoxLayout(vbox2_click)
        vbox2_click.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://emprendedores.es/gestion/crear-una-empresa/tipo-sociedad-emprender/")))
        vbox2 = QWidget()
        vbox2.setFixedWidth(150)
        vbox2.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;  /* Color de fondo */
                border-radius: 15px;  /* Radio del borde para esquinas redondeadas */
            }
        """)
        vbox2_layout = QVBoxLayout(vbox2)

        imagen2 = QPixmap(os.path.join(IMAGE_PATH,"articulo1.jpg"))
        imagen2 = imagen2.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen2_label = QLabel()
        imagen2_label.setPixmap(imagen2)
        imagen2_label.setAlignment(Qt.AlignCenter)

        vbox2_layout.addWidget(imagen2_label)

        tittle_hbox2 = QLabel("¿Qué tipo de sociedad mercantil te interesa montar?")
        tittle_hbox2.setStyleSheet("""
                                    font-size: 12px;
                                    font-weight: bold;
                                    color: black;
                                    """)
        tittle_hbox2.setWordWrap(True)
        tittle_hbox2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox2_layout.addWidget(tittle_hbox2)

        vbox2_click_layout.addWidget(vbox2)
        hbox_destacado1.addWidget(vbox2_click)

        hbox_destacado2 = QHBoxLayout()
        
# Destacado 3
        vbox3_click = ClickableWidget()
        vbox3_click_layout = QVBoxLayout(vbox3_click)
        vbox3_click.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.youtube.com/watch?v=eHJnEHyyN1Y")))
        vbox3 = QWidget()
        vbox3.setFixedWidth(150)
        vbox3.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;  /* Color de fondo */
                border-radius: 15px;  /* Radio del borde para esquinas redondeadas */
            }
        """)
        vbox3_layout = QVBoxLayout(vbox3)

        imagen3 = QPixmap(os.path.join(IMAGE_PATH,"video1.png"))
        imagen3 = imagen3.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen3_label = QLabel()
        imagen3_label.setPixmap(imagen3)
        imagen3_label.setAlignment(Qt.AlignCenter)

        vbox3_layout.addWidget(imagen3_label)

        tittle_hbox3 = QLabel("""6 Tips on Being a Successful Entrepreneur | John Mullins | TED
""")
        tittle_hbox3.setWordWrap(True)
        tittle_hbox3.setStyleSheet("""
                                    font-size: 12px;
                                    font-weight: bold;
                                    color: black;
                                    """)
        tittle_hbox3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox3_layout.addWidget(tittle_hbox3)
        
        vbox3_click_layout.addWidget(vbox3)
        hbox_destacado2.addWidget(vbox3_click)

    # Destacado 4

        vbox4_click = ClickableWidget()
        vbox4_click_layout = QVBoxLayout(vbox4_click)
        vbox2_click.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.innpulsacolombia.com/cemprende/eventos/mompreneurfest2024")))
        vbox4 = QWidget()
        vbox4.setFixedWidth(150)
        vbox4.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;  /* Color de fondo */
                border-radius: 15px;  /* Radio del borde para esquinas redondeadas */
            }
        """)
        vbox4_layout = QVBoxLayout(vbox4)

        imagen4 = QPixmap(os.path.join(IMAGE_PATH,"evento2.png"))
        imagen4 = imagen4.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen4_label = QLabel()
        imagen4_label.setPixmap(imagen4)
        imagen4_label.setAlignment(Qt.AlignCenter)

        vbox4_layout.addWidget(imagen4_label)

        tittle_hbox4 = QLabel(" Mompreneurs fest")
        tittle_hbox4.setStyleSheet("""
                                    font-size: 12px;
                                    font-weight: bold;
                                    color: black;
                                    """)
        tittle_hbox4.setWordWrap(True)
        tittle_hbox4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox4_layout.addWidget(tittle_hbox4)

        vbox4_click_layout.addWidget(vbox4)
        hbox_destacado2.addWidget(vbox4_click)

        destacado_layout.addLayout(hbox_destacado1)
        destacado_layout.addLayout(hbox_destacado2)

        content_layout.addWidget(destacado_contenedor)

        tittle_explorar = QLabel("Sigue Explorando")
        tittle_explorar.setStyleSheet("""
                                    font-size: 32px;
                                    font-weight: bold;
                                    color: black;
                                    margin-top: 20px;
                                    margin-bottom: 5px;
                                    """)
        tittle_explorar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(tittle_explorar)

        division2 = QWidget()
        division2.setFixedHeight(10)
        division2.setStyleSheet("""
            QWidget {
                background-color: #00C08C;  /* Color de fondo */
                border-radius: 5px;  /* Radio del borde para esquinas redondeadas */
            }
        """)
        content_layout.addWidget(division2)
        
#EXPLORAR
        explorar_contenedor = QWidget()
        explorar_layout = QVBoxLayout(explorar_contenedor)
        explorar_contenedor.setFixedWidth(390)
        
        noticia1_click = ClickableWidget()
        noticia1_click_layout = QVBoxLayout(noticia1_click)
        noticia1_click.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.larepublica.co/finanzas/primera-charla-con-shark-tanks-en-14-version-del-camp-de-asobancaria-3821245")))

        noticia1_contenedor = QWidget()
        #noticia1_contenedor.setFixedHeight(150)
        noticia1_contenedor.setStyleSheet("""
                    QWidget {
                        background-color: #E6E1E1;
                        border-radius: 10px;
                    }
                """)
        hbox_noticia1 = QHBoxLayout(noticia1_contenedor)
        imagen_noticia1 = QPixmap(os.path.join(IMAGE_PATH,"noticia2.webp"))
        imagen_noticia1 = imagen_noticia1.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_noticia1_label = QLabel()
        imagen_noticia1_label.setPixmap(imagen_noticia1)
        imagen_noticia1_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)

        vbox_noticia1 = QVBoxLayout()
        tittle_noticia1 = QLabel("Hay oportunidad, pero hay que cambiar las reglas del juego para emprendedores")
        tittle_noticia1.setStyleSheet("""
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: black;
                                    """)
        tittle_noticia1.setWordWrap(True)
        vbox_noticia1.addWidget(tittle_noticia1)

        desc_noticia1 = QLabel("Los principales problemas para los emprendedores son los papeleos que se deben hacer y la cantidad de impuestos cobrados")
        desc_noticia1.setStyleSheet("""
                                    font-size: 12px;
                                    color: black;
                                    """)
        desc_noticia1.setFixedWidth(250)  # Establece el tamaño fijo (ancho, alto)
        desc_noticia1.setWordWrap(True)
        vbox_noticia1.addWidget(desc_noticia1)
        vbox_noticia1.addStretch()

        hbox_noticia1.addWidget(imagen_noticia1_label)
        hbox_noticia1.addLayout(vbox_noticia1)

        noticia1_click_layout.addWidget(noticia1_contenedor)
        explorar_layout.addWidget(noticia1_click)

        content_layout.addWidget(explorar_contenedor)

        content_layout.addStretch()

        layout.addWidget(scroll)

class Directorio(QWidget):
    def __init__(self, menu, emprendimientos):
        super().__init__()
        self.menu = menu
        self.emprendimientos = emprendimientos
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"logotipo_negro.svg")).scaled(QSize(200,600), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        contenedor_layout.addWidget(logo)

        layout.addWidget(contenedor)

        buscar_layout = QHBoxLayout()
        
        buscar_input = QLineEdit()
        buscar_input.setPlaceholderText("Buscar")
        buscar_input.setStyleSheet("""
            QLineEdit {
                background-color: #E6E1E1;
                color: #737070;
                font-size: 12pt;
                border-radius: 15px;
                padding: 10 30px;
                margin-top: 10px;
                margin-right: 5px;
            }
        """)

        categoria_input = QComboBox()
        categoria_input.addItem("Categorías")  # Opción por defecto
        categoria_input.addItems(["Tecnología", "Salud", "Educación", "Finanzas", "Otra"])
        categoria_input.setStyleSheet("""
            QComboBox {
                background-color: #E6E1E1;
                color: #737070;
                font-size: 12pt;
                border-radius: 15px;
                padding: 12px 30px;
                margin-top: 10px;
                margin-left: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(path/to/your/dropdown-arrow-icon.png);
            }
            QComboBox QAbstractItemView {
                border: 1px #E6E1E1;
                selection-background-color: #E6E1E1;
                color: #737070;
                background-color: #E6E1E1;
                border-radius: 15px;
            }
        """)

        buscar_layout.addWidget(buscar_input)
        buscar_layout.addWidget(categoria_input)

        layout.addLayout(buscar_layout)



        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes
        content_widget.setFixedWidth(400)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""QScrollArea { border: none;
                             margin-left: 10px;
                              }""")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        emprendimientos_contenedor = QWidget()
        emprendimientos_layout = QVBoxLayout(emprendimientos_contenedor)
        emprendimientos_layout.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes
        emprendimientos_contenedor.setFixedWidth(390)

        # EMPRENDIMIENTO 01
        emp1_icon = os.path.join(IMAGE_PATH,"YOOB1.jpg")
        emp1_desc = "App para los nómadas digitales con trabajos freelance, solucionamos la complejidad de conseguir trabajo para este tipo de mercado."
        emp1 = EmprendimientoWidget("YOOB", emp1_desc, "Servicios", emp1_icon)
        emp1.clicked.connect(lambda: self.menu.changeStackIndex(9))

        emprendimientos_layout.addWidget(emp1)


        emprendimientos_layout.addSpacing(10)

# EMPRENDIMIENTO 02
        emp2_icon = os.path.join(IMAGE_PATH,"servicetrade1.png")
        emp2_desc = "App para los nómadas digitales con trabajos freelance, solucionamos la complejidad de conseguir trabajo para este tipo de mercado."
        emp2 = EmprendimientoWidget("Service Trade", emp2_desc, "Servicios", emp2_icon )
        emp2.clicked.connect(lambda: self.menu.changeStackIndex(10))

        emprendimientos_layout.addWidget(emp2)
        
        emprendimientos_layout.addSpacing(10)
       
# EMPRENDIMIENTO 03
        emp3_icon = os.path.join(IMAGE_PATH,"Ecotech1.png")
        emp3_desc = "EcoTech Solutions es una empresa que desarrolla soluciones tecnológicas innovadoras para promover la sostenibilidad ambiental."
        emp3 = EmprendimientoWidget("EcoTech Solutions", emp3_desc, "Tecnología", emp3_icon)
        emp3.clicked.connect(lambda: self.menu.changeStackIndex(11))

        emprendimientos_layout.addWidget(emp3)
        
        emprendimientos_layout.addSpacing(10)
        
# EMPRENDIMIENTO 04
        emp4_icon = os.path.join(IMAGE_PATH,"fit1.png")
        emp4_desc = "EcoTech Solutions es una empresa que desarrolla soluciones tecnológicas innovadoras para promover la sostenibilidad ambiental."    
        emp4 = EmprendimientoWidget("FitByte", emp4_desc, "Salud", emp4_icon)
        emp4.clicked.connect(lambda: self.menu.changeStackIndex(12))

        emprendimientos_layout.addWidget(emp4)
        
        emprendimientos_layout.addSpacing(10)

# EMPRENDIMIENTO 05
        emp5_icon = os.path.join(IMAGE_PATH,"crypto1.png")
        emp5_desc = "CryptoSecure es una plataforma de custodia segura para criptomonedas y activos digitales. "    
        emp5 = EmprendimientoWidget("CryptoSecure", emp5_desc, "Finanzas", emp5_icon)
        emp5.clicked.connect(lambda: self.menu.changeStackIndex(13))

        emprendimientos_layout.addWidget(emp5)
        
        emprendimientos_layout.addSpacing(10)

# EMPRENDIMIENTO 06
        emp6_icon = os.path.join(IMAGE_PATH,"drone1.png")
        emp6_desc = "DroneDelivery es una empresa innovadora que ofrece servicios de entrega rápida utilizando drones."            
        emp6 = EmprendimientoWidget("DroneDelivery", emp6_desc, "Logística", emp6_icon)
        emp6.clicked.connect(lambda: self.menu.changeStackIndex(14))

        emprendimientos_layout.addWidget(emp6)
        
        emprendimientos_layout.addSpacing(10)

# EMPRENDIMIENTO 07
        emp7_icon = os.path.join(IMAGE_PATH,"art1.png")
        emp7_desc = "ArtVerse es una plataforma en línea que conecta a artistas emergentes con coleccionistas y amantes del arte de todo el mundo."            
        emp7 = EmprendimientoWidget("ArtVerse", emp7_desc, "Arte", emp7_icon)
        emp7.clicked.connect(lambda: self.menu.changeStackIndex(15))

        emprendimientos_layout.addWidget(emp7)
        
        emprendimientos_layout.addSpacing(10)

# Emprendimientos de la DB

        for id, emprendimiento in self.emprendimientos.items():
            nombre = emprendimiento.get('nombre', '')
            descripcion = emprendimiento.get("descripcion", "")
            categoria = emprendimiento.get('categoria', '')
            icon_path = "ruta/a/la/imagen"  # Asegúrate de que esta ruta sea correcta
            emprendimientos_db = EmprendimientoWidget(nombre, descripcion, categoria)
            emprendimientos_db.clicked.connect(lambda nombre=nombre, descripcion=descripcion, categoria=categoria: self.menu.on_emprendimiento_user_clicked(nombre, descripcion, categoria))
            emprendimientos_layout.addWidget(emprendimientos_db)

        content_layout.addWidget(emprendimientos_contenedor)

        content_layout.addStretch()
        layout.addWidget(scroll)

class Emprendimiento1(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0 , 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        nombre = QLabel("YOOB")
        nombre.setAlignment(Qt.AlignCenter)
        nombre.setWordWrap(True)
        nombre.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(nombre)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        imagen_perfil = QPixmap(os.path.join(IMAGE_PATH,"YOOB1.jpg"))
        imagen_perfil = imagen_perfil.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_perfil_label = QLabel()
        imagen_perfil_label.setPixmap(imagen_perfil)
        imagen_perfil_label.setAlignment(Qt.AlignCenter)
        imagen_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        content_layout.addWidget(imagen_perfil_label)

        categoria = QLabel("Servicios")
        categoria.setStyleSheet("""
                            font-size: 12pt;
                            """)
        categoria.setAlignment(Qt.AlignCenter)
        
        content_layout.addWidget(categoria)

        content_layout.addSpacing(5)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        compartir_button = QPushButton("Compartir")
        compartir_button.setFixedSize(110, 30)
        compartir_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(compartir_button)

        catalogo_button = QPushButton("Catálogo")
        catalogo_button.setFixedSize(110, 30)
        catalogo_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(catalogo_button)

        link_button = QPushButton("link")
        link_button.setFixedSize(110, 30)
        link_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(link_button)

        content_layout.addWidget(buttons_widget)

        content_layout.addSpacing(5)

        descripcion = QLabel("App para los nómadas digitales con trabajos freelance, solucionamos la complejidad de conseguir trabajo para este tipo de mercado con un app innovadora y dinámica")
        descripcion.setStyleSheet("""
                                    font-size: 25px;
                                    color: black;
                                    """)
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setWordWrap(True)
        content_layout.addWidget(descripcion)

        content_layout.addSpacing(15)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)

        info_layout.addSpacing(10)

        info_hbox1_widget = QWidget()
        info_hbox1 = QHBoxLayout(info_hbox1_widget)
        info_hbox1_widget.setStyleSheet("padding: 5 5px;")

        imagen1_label = QLabel()
        imagen1_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"YOOB2.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox1.addWidget(imagen1_label)

        desc1 = QLabel("""Nuestro equipo""")
        desc1.setAlignment(Qt.AlignLeft)
        desc1.setStyleSheet("font-size: 12pt;")
        desc1.setWordWrap(True)
        desc1.setFixedWidth(220)
        
        info_hbox1.addWidget(desc1)

        info_layout.addWidget(info_hbox1_widget)

# Segunda Info

        info_hbox2_widget = QWidget()
        info_hbox2 = QHBoxLayout(info_hbox2_widget)
        info_hbox2_widget.setStyleSheet("padding: 5 5px;")

        imagen2_label = QLabel()
        imagen2_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"YOOB3.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imagen2_label.setAlignment(Qt.AlignCenter)

        info_hbox2.addWidget(imagen2_label)

        desc2 = QLabel("""Da un recorrido por nuestra app""")
        desc2.setAlignment(Qt.AlignLeft)
        desc2.setStyleSheet("font-size: 12pt;")
        desc2.setWordWrap(True)
        desc2.setFixedWidth(220)
        
        info_hbox2.addWidget(desc2)

        info_layout.addWidget(info_hbox2_widget)

# Tercera Información

        info_hbox3_widget = QWidget()
        info_hbox3 = QHBoxLayout(info_hbox3_widget)
        info_hbox3_widget.setStyleSheet("padding: 5 5px;")

        imagen3_label = QLabel()
        imagen3_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"sabana.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox3.addWidget(imagen3_label)

        desc3 = QLabel("""Somos un emprendimiento nacido en la Universidad de la Sabana""")
        desc3.setAlignment(Qt.AlignLeft)
        desc3.setStyleSheet("font-size: 12pt;")
        desc3.setWordWrap(True)
        desc3.setFixedWidth(220)
        
        info_hbox3.addWidget(desc3)

        info_layout.addWidget(info_hbox3_widget)

        content_layout.addWidget(info_widget)

        content_layout.addSpacing(15)

        contacto = QLabel("Contacto")
        contacto.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        numero = QLabel("Número")
        numero.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        Correo = QLabel("Correo")
        Correo.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        redes = QLabel("Perfil de redes Sociales")
        redes.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        
        reportar_contenido = QPushButton("Reportar Contenido")
        reportar_contenido.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        reportar_cuenta = QPushButton("Reportar Cuenta")
        reportar_cuenta.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        
        #content_layout.addWidget(contacto)
        #content_layout.addWidget(numero)
        #content_layout.addWidget(Correo)
        #content_layout.addWidget(redes)
        content_layout.addSpacing(15)
        content_layout.addWidget(reportar_contenido)
        content_layout.addWidget(reportar_cuenta)

        content_layout.addStretch()

        layout.addWidget(scroll)

class Emprendimiento2(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0 , 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        nombre = QLabel("Service Trade")
        nombre.setAlignment(Qt.AlignCenter)
        nombre.setWordWrap(True)
        nombre.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(nombre)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        imagen_perfil = QPixmap(os.path.join(IMAGE_PATH,"servicetrade1.png"))
        imagen_perfil = imagen_perfil.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_perfil_label = QLabel()
        imagen_perfil_label.setPixmap(imagen_perfil)
        imagen_perfil_label.setAlignment(Qt.AlignCenter)
        imagen_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        content_layout.addWidget(imagen_perfil_label)

        categoria = QLabel("Servicios")
        categoria.setStyleSheet("""
                            font-size: 12pt;
                            """)
        categoria.setAlignment(Qt.AlignCenter)
        
        content_layout.addWidget(categoria)

        content_layout.addSpacing(5)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        compartir_button = QPushButton("Compartir")
        compartir_button.setFixedSize(110, 30)
        compartir_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(compartir_button)

        catalogo_button = QPushButton("Catálogo")
        catalogo_button.setFixedSize(110, 30)
        catalogo_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(catalogo_button)

        link_button = QPushButton("link")
        link_button.setFixedSize(110, 30)
        link_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(link_button)

        content_layout.addWidget(buttons_widget)

        content_layout.addSpacing(5)

        descripcion = QLabel("Es una plataforma que centraliza la información asociada a la internacionalización de servicios. Lo hace por medio de Webscraping y solo utiliza fuentes veraces.")
        descripcion.setStyleSheet("""
                                    font-size: 25px;
                                    color: black;
                                    """)
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setWordWrap(True)
        content_layout.addWidget(descripcion)

        content_layout.addSpacing(15)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)

        info_layout.addSpacing(10)

        info_hbox1_widget = QWidget()
        info_hbox1 = QHBoxLayout(info_hbox1_widget)
        info_hbox1_widget.setStyleSheet("padding: 5 5px;")

        imagen1_label = QLabel()
        imagen1_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"servicetrade2.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox1.addWidget(imagen1_label)

        desc1 = QLabel("""Conoce nuestra página""")
        desc1.setAlignment(Qt.AlignLeft)
        desc1.setStyleSheet("font-size: 12pt;")
        desc1.setWordWrap(True)
        desc1.setFixedWidth(220)
        
        info_hbox1.addWidget(desc1)

        info_layout.addWidget(info_hbox1_widget)

# Segunda Info

        info_hbox2_widget = QWidget()
        info_hbox2 = QHBoxLayout(info_hbox2_widget)
        info_hbox2_widget.setStyleSheet("padding: 5 5px;")

        imagen2_label = QLabel()
        imagen2_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"YOOB3.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imagen2_label.setAlignment(Qt.AlignCenter)

        info_hbox2.addWidget(imagen2_label)

        desc2 = QLabel("""Da un recorrido por nuestra app""")
        desc2.setAlignment(Qt.AlignLeft)
        desc2.setStyleSheet("font-size: 12pt;")
        desc2.setWordWrap(True)
        desc2.setFixedWidth(220)
        
        info_hbox2.addWidget(desc2)

        #info_layout.addWidget(info_hbox2_widget)

# Tercera Información

        info_hbox3_widget = QWidget()
        info_hbox3 = QHBoxLayout(info_hbox3_widget)
        info_hbox3_widget.setStyleSheet("padding: 5 5px;")

        imagen3_label = QLabel()
        imagen3_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"sabana.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox3.addWidget(imagen3_label)

        desc3 = QLabel("""Somos un emprendimiento nacido en la Universidad de la Sabana""")
        desc3.setAlignment(Qt.AlignLeft)
        desc3.setStyleSheet("font-size: 12pt;")
        desc3.setWordWrap(True)
        desc3.setFixedWidth(220)
        
        info_hbox3.addWidget(desc3)

        info_layout.addWidget(info_hbox3_widget)

        content_layout.addWidget(info_widget)

        content_layout.addSpacing(15)

        contacto = QLabel("Contacto")
        contacto.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        numero = QLabel("Número")
        numero.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        Correo = QLabel("Correo")
        Correo.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        redes = QLabel("Perfil de redes Sociales")
        redes.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        
        reportar_contenido = QPushButton("Reportar Contenido")
        reportar_contenido.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        reportar_cuenta = QPushButton("Reportar Cuenta")
        reportar_cuenta.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        
        #content_layout.addWidget(contacto)
        #content_layout.addWidget(numero)
        #content_layout.addWidget(Correo)
        #content_layout.addWidget(redes)
        content_layout.addSpacing(15)
        content_layout.addWidget(reportar_contenido)
        content_layout.addWidget(reportar_cuenta)

        content_layout.addStretch()

        layout.addWidget(scroll)

class Emprendimiento3(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0 , 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        nombre = QLabel("EcoTech Solutions")
        nombre.setAlignment(Qt.AlignCenter)
        nombre.setWordWrap(True)
        nombre.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(nombre)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        imagen_perfil = QPixmap(os.path.join(IMAGE_PATH,"Ecotech1.png"))
        imagen_perfil = imagen_perfil.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_perfil_label = QLabel()
        imagen_perfil_label.setPixmap(imagen_perfil)
        imagen_perfil_label.setAlignment(Qt.AlignCenter)
        imagen_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        content_layout.addWidget(imagen_perfil_label)

        categoria = QLabel("Tecnología")
        categoria.setStyleSheet("""
                            font-size: 12pt;
                            """)
        categoria.setAlignment(Qt.AlignCenter)
        
        content_layout.addWidget(categoria)

        content_layout.addSpacing(5)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        compartir_button = QPushButton("Compartir")
        compartir_button.setFixedSize(110, 30)
        compartir_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(compartir_button)

        catalogo_button = QPushButton("Catálogo")
        catalogo_button.setFixedSize(110, 30)
        catalogo_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(catalogo_button)

        link_button = QPushButton("link")
        link_button.setFixedSize(110, 30)
        link_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(link_button)

        content_layout.addWidget(buttons_widget)

        content_layout.addSpacing(5)

        descripcion = QLabel("EcoTech Solutions es una empresa que desarrolla soluciones tecnológicas innovadoras para promover la sostenibilidad ambiental. Ofrecen una amplia gama de productos y servicios, desde paneles solares de última generación hasta sistemas de riego inteligentes, con el objetivo de reducir la huella de carbono y fomentar prácticas eco-amigables.")
        descripcion.setStyleSheet("""
                                    font-size: 25px;
                                    color: black;
                                    """)
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setWordWrap(True)
        content_layout.addWidget(descripcion)

        content_layout.addSpacing(15)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)

        info_layout.addSpacing(10)

        info_hbox1_widget = QWidget()
        info_hbox1 = QHBoxLayout(info_hbox1_widget)
        info_hbox1_widget.setStyleSheet("padding: 5 5px;")

        imagen1_label = QLabel()
        imagen1_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"Ecotech2.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox1.addWidget(imagen1_label)

        desc1 = QLabel("""Energía renovable, futuro sostenible""")
        desc1.setAlignment(Qt.AlignLeft)
        desc1.setStyleSheet("font-size: 12pt;")
        desc1.setWordWrap(True)
        desc1.setFixedWidth(220)
        
        info_hbox1.addWidget(desc1)

        info_layout.addWidget(info_hbox1_widget)

# Segunda Info

        info_hbox2_widget = QWidget()
        info_hbox2 = QHBoxLayout(info_hbox2_widget)
        info_hbox2_widget.setStyleSheet("padding: 5 5px;")

        imagen2_label = QLabel()
        imagen2_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"Ecotech3.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imagen2_label.setAlignment(Qt.AlignCenter)

        info_hbox2.addWidget(imagen2_label)

        desc2 = QLabel("""Innovación verde para un planeta más limpio""")
        desc2.setAlignment(Qt.AlignLeft)
        desc2.setStyleSheet("font-size: 12pt;")
        desc2.setWordWrap(True)
        desc2.setFixedWidth(220)
        
        info_hbox2.addWidget(desc2)

        info_layout.addWidget(info_hbox2_widget)

# Tercera Información

        info_hbox3_widget = QWidget()
        info_hbox3 = QHBoxLayout(info_hbox3_widget)
        info_hbox3_widget.setStyleSheet("padding: 5 5px;")

        imagen3_label = QLabel()
        imagen3_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"sabana.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox3.addWidget(imagen3_label)

        desc3 = QLabel("""Somos un emprendimiento nacido en la Universidad de la Sabana""")
        desc3.setAlignment(Qt.AlignLeft)
        desc3.setStyleSheet("font-size: 12pt;")
        desc3.setWordWrap(True)
        desc3.setFixedWidth(220)
        
        info_hbox3.addWidget(desc3)

        #info_layout.addWidget(info_hbox3_widget)

        content_layout.addWidget(info_widget)

        content_layout.addSpacing(15)

        contacto = QLabel("Contacto")
        contacto.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        numero = QLabel("Número: +57 314 567 8901")
        numero.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        Correo = QLabel("Correo: info@ecotechsolutions.co")
        Correo.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        redes = QLabel("Perfil de redes Sociales")
        redes.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        
        reportar_contenido = QPushButton("Reportar Contenido")
        reportar_contenido.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        reportar_cuenta = QPushButton("Reportar Cuenta")
        reportar_cuenta.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        
        content_layout.addWidget(contacto)
        content_layout.addWidget(numero)
        content_layout.addWidget(Correo)
        #content_layout.addWidget(redes)
        content_layout.addSpacing(15)
        content_layout.addWidget(reportar_contenido)
        content_layout.addWidget(reportar_cuenta)

        content_layout.addStretch()

        layout.addWidget(scroll)

class Emprendimiento4(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0 , 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        nombre = QLabel("FitByte")
        nombre.setAlignment(Qt.AlignCenter)
        nombre.setWordWrap(True)
        nombre.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(nombre)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        imagen_perfil = QPixmap(os.path.join(IMAGE_PATH,"fit1.png"))
        imagen_perfil = imagen_perfil.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_perfil_label = QLabel()
        imagen_perfil_label.setPixmap(imagen_perfil)
        imagen_perfil_label.setAlignment(Qt.AlignCenter)
        imagen_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        content_layout.addWidget(imagen_perfil_label)

        categoria = QLabel("Salud")
        categoria.setStyleSheet("""
                            font-size: 12pt;
                            """)
        categoria.setAlignment(Qt.AlignCenter)
        
        content_layout.addWidget(categoria)

        content_layout.addSpacing(5)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        compartir_button = QPushButton("Compartir")
        compartir_button.setFixedSize(110, 30)
        compartir_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(compartir_button)

        catalogo_button = QPushButton("Catálogo")
        catalogo_button.setFixedSize(110, 30)
        catalogo_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(catalogo_button)

        link_button = QPushButton("link")
        link_button.setFixedSize(110, 30)
        link_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(link_button)

        content_layout.addWidget(buttons_widget)

        content_layout.addSpacing(5)

        descripcion = QLabel("FitByte es una plataforma digital que combina inteligencia artificial y tecnología portátil para brindar un enfoque personalizado en el cuidado de la salud. Mediante el uso de dispositivos wearables y una aplicación móvil, FitByte recopila datos sobre el estilo de vida del usuario y ofrece recomendaciones nutricionales, rutinas de ejercicios y seguimiento de métricas clave para mantener un estilo de vida saludable.")
        descripcion.setStyleSheet("""
                                    font-size: 25px;
                                    color: black;
                                    """)
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setWordWrap(True)
        content_layout.addWidget(descripcion)

        content_layout.addSpacing(15)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)

        info_layout.addSpacing(10)

        info_hbox1_widget = QWidget()
        info_hbox1 = QHBoxLayout(info_hbox1_widget)
        info_hbox1_widget.setStyleSheet("padding: 5 5px;")

        imagen1_label = QLabel()
        imagen1_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"fit2.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox1.addWidget(imagen1_label)

        desc1 = QLabel("""Tu compañero digital hacia una vida saludable""")
        desc1.setAlignment(Qt.AlignLeft)
        desc1.setStyleSheet("font-size: 12pt;")
        desc1.setWordWrap(True)
        desc1.setFixedWidth(220)
        
        info_hbox1.addWidget(desc1)

        info_layout.addWidget(info_hbox1_widget)

# Segunda Info

        info_hbox2_widget = QWidget()
        info_hbox2 = QHBoxLayout(info_hbox2_widget)
        info_hbox2_widget.setStyleSheet("padding: 5 5px;")

        imagen2_label = QLabel()
        imagen2_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"fit3.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imagen2_label.setAlignment(Qt.AlignCenter)

        info_hbox2.addWidget(imagen2_label)

        desc2 = QLabel("""Datos inteligentes, hábitos más sanos""")
        desc2.setAlignment(Qt.AlignLeft)
        desc2.setStyleSheet("font-size: 12pt;")
        desc2.setWordWrap(True)
        desc2.setFixedWidth(220)
        
        info_hbox2.addWidget(desc2)

        info_layout.addWidget(info_hbox2_widget)

# Tercera Información

        info_hbox3_widget = QWidget()
        info_hbox3 = QHBoxLayout(info_hbox3_widget)
        info_hbox3_widget.setStyleSheet("padding: 5 5px;")

        imagen3_label = QLabel()
        imagen3_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"sabana.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox3.addWidget(imagen3_label)

        desc3 = QLabel("""Somos un emprendimiento nacido en la Universidad de la Sabana""")
        desc3.setAlignment(Qt.AlignLeft)
        desc3.setStyleSheet("font-size: 12pt;")
        desc3.setWordWrap(True)
        desc3.setFixedWidth(220)
        
        info_hbox3.addWidget(desc3)

        #info_layout.addWidget(info_hbox3_widget)

        content_layout.addWidget(info_widget)

        content_layout.addSpacing(15)

        contacto = QLabel("Contacto")
        contacto.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        numero = QLabel("Número: +57 320 987 6543")
        numero.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        Correo = QLabel("Correo: contacto@fitbyte.com.co")
        Correo.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        redes = QLabel("Perfil de redes Sociales")
        redes.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        
        reportar_contenido = QPushButton("Reportar Contenido")
        reportar_contenido.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        reportar_cuenta = QPushButton("Reportar Cuenta")
        reportar_cuenta.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        
        content_layout.addWidget(contacto)
        content_layout.addWidget(numero)
        content_layout.addWidget(Correo)
        #content_layout.addWidget(redes)
        content_layout.addSpacing(15)
        content_layout.addWidget(reportar_contenido)
        content_layout.addWidget(reportar_cuenta)

        content_layout.addStretch()

        layout.addWidget(scroll)

class Emprendimiento5(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0 , 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        nombre = QLabel("CryptoSecure")
        nombre.setAlignment(Qt.AlignCenter)
        nombre.setWordWrap(True)
        nombre.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(nombre)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        imagen_perfil = QPixmap(os.path.join(IMAGE_PATH,"crypto1.png"))
        imagen_perfil = imagen_perfil.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_perfil_label = QLabel()
        imagen_perfil_label.setPixmap(imagen_perfil)
        imagen_perfil_label.setAlignment(Qt.AlignCenter)
        imagen_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        content_layout.addWidget(imagen_perfil_label)

        categoria = QLabel("Finanzas")
        categoria.setStyleSheet("""
                            font-size: 12pt;
                            """)
        categoria.setAlignment(Qt.AlignCenter)
        
        content_layout.addWidget(categoria)

        content_layout.addSpacing(5)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        compartir_button = QPushButton("Compartir")
        compartir_button.setFixedSize(110, 30)
        compartir_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(compartir_button)

        catalogo_button = QPushButton("Catálogo")
        catalogo_button.setFixedSize(110, 30)
        catalogo_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(catalogo_button)

        link_button = QPushButton("link")
        link_button.setFixedSize(110, 30)
        link_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(link_button)

        content_layout.addWidget(buttons_widget)

        content_layout.addSpacing(5)

        descripcion = QLabel("CryptoSecure es una plataforma de custodia segura para criptomonedas y activos digitales. Utilizando tecnología de cifrado avanzada y protocolos de seguridad de última generación, CryptoSecure ofrece a sus clientes una solución confiable para almacenar y gestionar sus inversiones en criptomonedas, brindando tranquilidad y protección contra amenazas cibernéticas.")
        descripcion.setStyleSheet("""
                                    font-size: 25px;
                                    color: black;
                                    """)
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setWordWrap(True)
        content_layout.addWidget(descripcion)

        content_layout.addSpacing(15)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)

        info_layout.addSpacing(10)

        info_hbox1_widget = QWidget()
        info_hbox1 = QHBoxLayout(info_hbox1_widget)
        info_hbox1_widget.setStyleSheet("padding: 5 5px;")

        imagen1_label = QLabel()
        imagen1_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"crypto2.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox1.addWidget(imagen1_label)

        desc1 = QLabel("""La bóveda digital para tus criptoactivos""")
        desc1.setAlignment(Qt.AlignLeft)
        desc1.setStyleSheet("font-size: 12pt;")
        desc1.setWordWrap(True)
        desc1.setFixedWidth(220)
        
        info_hbox1.addWidget(desc1)

        info_layout.addWidget(info_hbox1_widget)

# Segunda Info

        info_hbox2_widget = QWidget()
        info_hbox2 = QHBoxLayout(info_hbox2_widget)
        info_hbox2_widget.setStyleSheet("padding: 5 5px;")

        imagen2_label = QLabel()
        imagen2_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"crypto3.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imagen2_label.setAlignment(Qt.AlignCenter)

        info_hbox2.addWidget(imagen2_label)

        desc2 = QLabel("""Seguridad descentralizada, confianza garantizada""")
        desc2.setAlignment(Qt.AlignLeft)
        desc2.setStyleSheet("font-size: 12pt;")
        desc2.setWordWrap(True)
        desc2.setFixedWidth(220)
        
        info_hbox2.addWidget(desc2)

        info_layout.addWidget(info_hbox2_widget)

# Tercera Información

        info_hbox3_widget = QWidget()
        info_hbox3 = QHBoxLayout(info_hbox3_widget)
        info_hbox3_widget.setStyleSheet("padding: 5 5px;")

        imagen3_label = QLabel()
        imagen3_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"sabana.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox3.addWidget(imagen3_label)

        desc3 = QLabel("""Somos un emprendimiento nacido en la Universidad de la Sabana""")
        desc3.setAlignment(Qt.AlignLeft)
        desc3.setStyleSheet("font-size: 12pt;")
        desc3.setWordWrap(True)
        desc3.setFixedWidth(220)
        
        info_hbox3.addWidget(desc3)

        #info_layout.addWidget(info_hbox3_widget)

        content_layout.addWidget(info_widget)

        content_layout.addSpacing(15)

        contacto = QLabel("Contacto")
        contacto.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        numero = QLabel("Número: +57 315 432 1098")
        numero.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        Correo = QLabel("Correo: seguridad@cryptosecure.co")
        Correo.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        redes = QLabel("Perfil de redes Sociales")
        redes.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        
        reportar_contenido = QPushButton("Reportar Contenido")
        reportar_contenido.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        reportar_cuenta = QPushButton("Reportar Cuenta")
        reportar_cuenta.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        
        content_layout.addWidget(contacto)
        content_layout.addWidget(numero)
        content_layout.addWidget(Correo)
        #content_layout.addWidget(redes)
        content_layout.addSpacing(15)
        content_layout.addWidget(reportar_contenido)
        content_layout.addWidget(reportar_cuenta)

        content_layout.addStretch()

        layout.addWidget(scroll)

class Emprendimiento6(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0 , 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        nombre = QLabel("DroneDelivery")
        nombre.setAlignment(Qt.AlignCenter)
        nombre.setWordWrap(True)
        nombre.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(nombre)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        imagen_perfil = QPixmap(os.path.join(IMAGE_PATH,"drone1.png"))
        imagen_perfil = imagen_perfil.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_perfil_label = QLabel()
        imagen_perfil_label.setPixmap(imagen_perfil)
        imagen_perfil_label.setAlignment(Qt.AlignCenter)
        imagen_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        content_layout.addWidget(imagen_perfil_label)

        categoria = QLabel("Logística")
        categoria.setStyleSheet("""
                            font-size: 12pt;
                            """)
        categoria.setAlignment(Qt.AlignCenter)
        
        content_layout.addWidget(categoria)

        content_layout.addSpacing(5)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        compartir_button = QPushButton("Compartir")
        compartir_button.setFixedSize(110, 30)
        compartir_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(compartir_button)

        catalogo_button = QPushButton("Catálogo")
        catalogo_button.setFixedSize(110, 30)
        catalogo_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(catalogo_button)

        link_button = QPushButton("link")
        link_button.setFixedSize(110, 30)
        link_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(link_button)

        content_layout.addWidget(buttons_widget)

        content_layout.addSpacing(5)

        descripcion = QLabel("DroneDelivery es una empresa innovadora que ofrece servicios de entrega rápida utilizando drones. Su objetivo es optimizar la última milla de la cadena de suministro, entregando paquetes de manera eficiente y eco-amigable. Cuentan con una flota de drones de última generación y una red de estaciones de carga estratégicamente ubicadas para garantizar entregas rápidas y confiables.")
        descripcion.setStyleSheet("""
                                    font-size: 25px;
                                    color: black;
                                    """)
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setWordWrap(True)
        content_layout.addWidget(descripcion)

        content_layout.addSpacing(15)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)

        info_layout.addSpacing(10)

        info_hbox1_widget = QWidget()
        info_hbox1 = QHBoxLayout(info_hbox1_widget)
        info_hbox1_widget.setStyleSheet("padding: 5 5px;")

        imagen1_label = QLabel()
        imagen1_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"drone2.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox1.addWidget(imagen1_label)

        desc1 = QLabel("""El futuro de la entrega, justo a tiempo""")
        desc1.setAlignment(Qt.AlignLeft)
        desc1.setStyleSheet("font-size: 12pt;")
        desc1.setWordWrap(True)
        desc1.setFixedWidth(220)
        
        info_hbox1.addWidget(desc1)

        info_layout.addWidget(info_hbox1_widget)

# Segunda Info

        info_hbox2_widget = QWidget()
        info_hbox2 = QHBoxLayout(info_hbox2_widget)
        info_hbox2_widget.setStyleSheet("padding: 5 5px;")

        imagen2_label = QLabel()
        imagen2_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"drone3.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imagen2_label.setAlignment(Qt.AlignCenter)

        info_hbox2.addWidget(imagen2_label)

        desc2 = QLabel("""Envíos rápidos y eco-amigables desde el cielo""")
        desc2.setAlignment(Qt.AlignLeft)
        desc2.setStyleSheet("font-size: 12pt;")
        desc2.setWordWrap(True)
        desc2.setFixedWidth(220)
        
        info_hbox2.addWidget(desc2)

        info_layout.addWidget(info_hbox2_widget)

# Tercera Información

        info_hbox3_widget = QWidget()
        info_hbox3 = QHBoxLayout(info_hbox3_widget)
        info_hbox3_widget.setStyleSheet("padding: 5 5px;")

        imagen3_label = QLabel()
        imagen3_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"sabana.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox3.addWidget(imagen3_label)

        desc3 = QLabel("""Somos un emprendimiento nacido en la Universidad de la Sabana""")
        desc3.setAlignment(Qt.AlignLeft)
        desc3.setStyleSheet("font-size: 12pt;")
        desc3.setWordWrap(True)
        desc3.setFixedWidth(220)
        
        info_hbox3.addWidget(desc3)

        #info_layout.addWidget(info_hbox3_widget)

        content_layout.addWidget(info_widget)

        content_layout.addSpacing(15)

        contacto = QLabel("Contacto")
        contacto.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        numero = QLabel("Número: +57 318 765 4321")
        numero.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        Correo = QLabel("Correo: servicio@dronedelivery.com.co")
        Correo.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        redes = QLabel("Perfil de redes Sociales")
        redes.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        
        reportar_contenido = QPushButton("Reportar Contenido")
        reportar_contenido.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        reportar_cuenta = QPushButton("Reportar Cuenta")
        reportar_cuenta.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        
        content_layout.addWidget(contacto)
        content_layout.addWidget(numero)
        content_layout.addWidget(Correo)
        #content_layout.addWidget(redes)
        content_layout.addSpacing(15)
        content_layout.addWidget(reportar_contenido)
        content_layout.addWidget(reportar_cuenta)

        content_layout.addStretch()

        layout.addWidget(scroll)

class Emprendimiento7(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0 , 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        nombre = QLabel("ArtVerse")
        nombre.setAlignment(Qt.AlignCenter)
        nombre.setWordWrap(True)
        nombre.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(nombre)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        imagen_perfil = QPixmap(os.path.join(IMAGE_PATH,"art1.png"))
        imagen_perfil = imagen_perfil.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_perfil_label = QLabel()
        imagen_perfil_label.setPixmap(imagen_perfil)
        imagen_perfil_label.setAlignment(Qt.AlignCenter)
        imagen_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        content_layout.addWidget(imagen_perfil_label)

        categoria = QLabel("Arte")
        categoria.setStyleSheet("""
                            font-size: 12pt;
                            """)
        categoria.setAlignment(Qt.AlignCenter)
        
        content_layout.addWidget(categoria)

        content_layout.addSpacing(5)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        compartir_button = QPushButton("Compartir")
        compartir_button.setFixedSize(110, 30)
        compartir_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(compartir_button)

        catalogo_button = QPushButton("Catálogo")
        catalogo_button.setFixedSize(110, 30)
        catalogo_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(catalogo_button)

        link_button = QPushButton("link")
        link_button.setFixedSize(110, 30)
        link_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(link_button)

        content_layout.addWidget(buttons_widget)

        content_layout.addSpacing(5)

        descripcion = QLabel("ArtVerse es una plataforma en línea que conecta a artistas emergentes con coleccionistas y amantes del arte de todo el mundo. Utilizando tecnología de realidad virtual, los usuarios pueden explorar galerías virtuales, asistir a exposiciones y subastas, además de comprar obras de arte directamente desde su hogar.")
        descripcion.setStyleSheet("""
                                    font-size: 25px;
                                    color: black;
                                    """)
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setWordWrap(True)
        content_layout.addWidget(descripcion)

        content_layout.addSpacing(15)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)

        info_layout.addSpacing(10)

        info_hbox1_widget = QWidget()
        info_hbox1 = QHBoxLayout(info_hbox1_widget)
        info_hbox1_widget.setStyleSheet("padding: 5 5px;")

        imagen1_label = QLabel()
        imagen1_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"art2.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox1.addWidget(imagen1_label)

        desc1 = QLabel("""Sumergido en un mundo de arte sin fronteras""")
        desc1.setAlignment(Qt.AlignLeft)
        desc1.setStyleSheet("font-size: 12pt;")
        desc1.setWordWrap(True)
        desc1.setFixedWidth(220)
        
        info_hbox1.addWidget(desc1)

        info_layout.addWidget(info_hbox1_widget)

# Segunda Info

        info_hbox2_widget = QWidget()
        info_hbox2 = QHBoxLayout(info_hbox2_widget)
        info_hbox2_widget.setStyleSheet("padding: 5 5px;")

        imagen2_label = QLabel()
        imagen2_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"art3.jpg")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imagen2_label.setAlignment(Qt.AlignCenter)

        info_hbox2.addWidget(imagen2_label)

        desc2 = QLabel("""Colecciona arte, explora culturas""")
        desc2.setAlignment(Qt.AlignLeft)
        desc2.setStyleSheet("font-size: 12pt;")
        desc2.setWordWrap(True)
        desc2.setFixedWidth(220)
        
        info_hbox2.addWidget(desc2)

        info_layout.addWidget(info_hbox2_widget)

# Tercera Información

        info_hbox3_widget = QWidget()
        info_hbox3 = QHBoxLayout(info_hbox3_widget)
        info_hbox3_widget.setStyleSheet("padding: 5 5px;")

        imagen3_label = QLabel()
        imagen3_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"sabana.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox3.addWidget(imagen3_label)

        desc3 = QLabel("""Somos un emprendimiento nacido en la Universidad de la Sabana""")
        desc3.setAlignment(Qt.AlignLeft)
        desc3.setStyleSheet("font-size: 12pt;")
        desc3.setWordWrap(True)
        desc3.setFixedWidth(220)
        
        info_hbox3.addWidget(desc3)

        #info_layout.addWidget(info_hbox3_widget)

        content_layout.addWidget(info_widget)

        content_layout.addSpacing(15)

        contacto = QLabel("Contacto")
        contacto.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        numero = QLabel("Número: +57 312 345 6789")
        numero.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        Correo = QLabel("Correo: soporte@artverse.co")
        Correo.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        redes = QLabel("Perfil de redes Sociales")
        redes.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        
        reportar_contenido = QPushButton("Reportar Contenido")
        reportar_contenido.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        reportar_cuenta = QPushButton("Reportar Cuenta")
        reportar_cuenta.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        
        content_layout.addWidget(contacto)
        content_layout.addWidget(numero)
        content_layout.addWidget(Correo)
        #content_layout.addWidget(redes)
        content_layout.addSpacing(15)
        content_layout.addWidget(reportar_contenido)
        content_layout.addWidget(reportar_cuenta)

        content_layout.addStretch()

        layout.addWidget(scroll)                                                

class EmprendimientoUser(QWidget):
    def __init__(self, menu, nombre, descripcion, categoria):
        super().__init__()
        self.menu = menu
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0 , 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        nombre = QLabel(self.nombre)
        nombre.setAlignment(Qt.AlignCenter)
        nombre.setWordWrap(True)
        nombre.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(nombre)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        imagen_perfil = QPixmap(os.path.join(IMAGE_PATH,"default.png"))
        imagen_perfil = imagen_perfil.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_perfil_label = QLabel()
        imagen_perfil_label.setPixmap(imagen_perfil)
        imagen_perfil_label.setAlignment(Qt.AlignCenter)
        imagen_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        content_layout.addWidget(imagen_perfil_label)

        categoria = QLabel(self.categoria)
        categoria.setStyleSheet("""
                            font-size: 12pt;
                            """)
        categoria.setAlignment(Qt.AlignCenter)
        
        content_layout.addWidget(categoria)

        content_layout.addSpacing(5)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        compartir_button = QPushButton("Compartir")
        compartir_button.setFixedSize(110, 30)
        compartir_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(compartir_button)

        catalogo_button = QPushButton("Catálogo")
        catalogo_button.setFixedSize(110, 30)
        catalogo_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(catalogo_button)

        link_button = QPushButton("link")
        link_button.setFixedSize(110, 30)
        link_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        buttons_layout.addWidget(link_button)

        content_layout.addWidget(buttons_widget)

        content_layout.addSpacing(5)

        descripcion = QLabel(self.descripcion)
        descripcion.setStyleSheet("""
                                    font-size: 35px;
                                    color: black;
                                    """)
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setWordWrap(True)
        content_layout.addWidget(descripcion)

        content_layout.addSpacing(15)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)

        info_layout.addSpacing(10)

        info_hbox1_widget = QWidget()
        info_hbox1 = QHBoxLayout(info_hbox1_widget)
        info_hbox1_widget.setStyleSheet("padding: 5 5px;")

        imagen1_label = QLabel()
        imagen1_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"default.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox1.addWidget(imagen1_label)

        desc1 = QLabel("""Cuenta más a tus clientes a que te dedicas acompañado de una imagen""")
        desc1.setAlignment(Qt.AlignLeft)
        desc1.setStyleSheet("font-size: 12pt;")
        desc1.setWordWrap(True)
        desc1.setFixedWidth(220)
        
        info_hbox1.addWidget(desc1)

        info_layout.addWidget(info_hbox1_widget)

# Segunda Info

        info_hbox2_widget = QWidget()
        info_hbox2 = QHBoxLayout(info_hbox2_widget)
        info_hbox2_widget.setStyleSheet("padding: 5 5px;")

        imagen2_label = QLabel()
        imagen2_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"default.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox2.addWidget(imagen2_label)

        desc2 = QLabel("""Comunica los productos o servicios que ofreces""")
        desc2.setAlignment(Qt.AlignLeft)
        desc2.setStyleSheet("font-size: 12pt;")
        desc2.setWordWrap(True)
        desc2.setFixedWidth(220)
        
        info_hbox2.addWidget(desc2)

        info_layout.addWidget(info_hbox2_widget)

# Tercera Información

        info_hbox3_widget = QWidget()
        info_hbox3 = QHBoxLayout(info_hbox3_widget)
        info_hbox3_widget.setStyleSheet("padding: 5 5px;")

        imagen3_label = QLabel()
        imagen3_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"default.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox3.addWidget(imagen3_label)

        desc3 = QLabel("""Comparte una foto que sientas importante""")
        desc3.setAlignment(Qt.AlignLeft)
        desc3.setStyleSheet("font-size: 12pt;")
        desc3.setWordWrap(True)
        desc3.setFixedWidth(220)
        
        info_hbox3.addWidget(desc3)

        info_layout.addWidget(info_hbox3_widget)

        content_layout.addWidget(info_widget)

        content_layout.addSpacing(15)

        contacto = QLabel("Contacto")
        contacto.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        numero = QLabel("Número")
        numero.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        Correo = QLabel("Correo")
        Correo.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        redes = QLabel("Perfil de redes Sociales")
        redes.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        
        reportar_contenido = QPushButton("Reportar Contenido")
        reportar_contenido.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        reportar_cuenta = QPushButton("Reportar Cuenta")
        reportar_cuenta.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                border-radius: 20px;
                font-size: 12pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        
        content_layout.addWidget(contacto)
        content_layout.addWidget(numero)
        content_layout.addWidget(Correo)
        content_layout.addWidget(redes)
        content_layout.addSpacing(15)
        content_layout.addWidget(reportar_contenido)
        content_layout.addWidget(reportar_cuenta)

        content_layout.addStretch()

        layout.addWidget(scroll)

class Perfil_user(QWidget):
    def __init__(self, menu, user):
        super().__init__()
        self.menu = menu
        self.user = user
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        tittle = QLabel(self.user["nombre"])
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setWordWrap(True)
        tittle.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(tittle)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        imagen_perfil = QPixmap(os.path.join(IMAGE_PATH,"default.png"))
        imagen_perfil = imagen_perfil.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_perfil_label = QLabel()
        imagen_perfil_label.setPixmap(imagen_perfil)
        imagen_perfil_label.setAlignment(Qt.AlignCenter)
        imagen_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        content_layout.addWidget(imagen_perfil_label)

        content_layout.addSpacing(5)

        bio_widget = QWidget()
        bio_layout = QHBoxLayout(bio_widget)

        bio_vbox1 = QVBoxLayout()

        categoria = QLabel(f"Categoría: {self.user["categoria"]}")
        categoria.setStyleSheet("""
                            font-size: 12pt;
                            """)

        descripcion = QLabel("Descripción de la persona")
        descripcion.setStyleSheet("""
                            font-size: 12pt;
                            """)

        bio_vbox1.addWidget(categoria)
        bio_vbox1.addWidget(descripcion)

        bio_layout.addLayout(bio_vbox1)

        bio_vbox2 = QVBoxLayout()

        editar_button = QPushButton("Editar Perfil")
        editar_button.setFixedSize(120, 30)
        editar_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        bio_vbox2.addWidget(editar_button)

        bio_layout.addLayout(bio_vbox2)

        content_layout.addWidget(bio_widget)

        content_layout.addSpacing(5)

        socios_widget = QWidget()
        socios_layout = QVBoxLayout(socios_widget)

        posibles = QLabel("Posibles socios:")
        posibles.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        socios_layout.addWidget(posibles)

        socios_h = QHBoxLayout()

        socio1 = SocioWidget("Nombre")

        socios_h.addWidget(socio1)

        socio2 = SocioWidget("Nombre")
        socios_h.addWidget(socio2)

        socio3 = SocioWidget("Nombre")
        socios_h.addWidget(socio3)

        socios_layout.addLayout(socios_h)

        content_layout.addWidget(socios_widget)

        tittle_sigo = QLabel("Emprendimientos que sigo")
        tittle_sigo.setStyleSheet("""
                                    font-size: 25px;
                                    font-weight: bold;
                                    color: black;
                                    """)
        tittle_sigo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(tittle_sigo)

        # EMPRENDIMIENTO 01
        
        emp1 = EmprendimientoWidget("Nombre 1", "Descripción del Emprendimiento 1", "Tecnología")

        content_layout.addWidget(emp1)

        content_layout.addSpacing(5)

# EMPRENDIMIENTO 02
        
        emp2 = EmprendimientoWidget("Nombre 2", "Descripción del Emprendimiento 2", "Tecnología")

        content_layout.addWidget(emp2)
        
        content_layout.addSpacing(5)

        info_layout = QVBoxLayout

        contacto = QLabel("Contacto")
        contacto.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        numero = QLabel("Número")
        numero.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        Correo = QLabel("Correo")
        Correo.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        redes = QLabel("Perfil de redes Sociales")
        redes.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        content_layout.addWidget(contacto)
        content_layout.addWidget(numero)
        content_layout.addWidget(Correo)
        content_layout.addWidget(redes)

        content_layout.addStretch()

        layout.addWidget(scroll) 

class Perfil_emp(QWidget):
    def __init__(self, menu, emp):
        super().__init__()
        self.menu = menu
        self.emp = emp
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0 , 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        nombre = QLabel(self.emp["nombre"])
        nombre.setAlignment(Qt.AlignCenter)
        nombre.setWordWrap(True)
        nombre.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(nombre)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        imagen_perfil = QPixmap(os.path.join(IMAGE_PATH,"default.png"))
        imagen_perfil = imagen_perfil.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_perfil_label = QLabel()
        imagen_perfil_label.setPixmap(imagen_perfil)
        imagen_perfil_label.setAlignment(Qt.AlignCenter)
        imagen_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        content_layout.addWidget(imagen_perfil_label)

        content_layout.addSpacing(5)

        bio_widget = QWidget()
        bio_layout = QHBoxLayout(bio_widget)

        bio_vbox1 = QVBoxLayout()

        categoria = QLabel(f"Categoría: {self.emp["categoria"]}")
        categoria.setStyleSheet("""
                            font-size: 12pt;
                            """)

        bio_vbox1.addWidget(categoria)

        bio_layout.addLayout(bio_vbox1)

        bio_vbox2 = QVBoxLayout()

        editar_button = QPushButton("Editar Perfil")
        editar_button.setFixedSize(120, 30)
        editar_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """)

        bio_vbox2.addWidget(editar_button)

        bio_layout.addLayout(bio_vbox2)

        content_layout.addWidget(bio_widget)

        content_layout.addSpacing(5)

        descripcion = QLabel(self.emp["descripcion"])
        descripcion.setStyleSheet("""
                                    font-size: 35px;
                                    color: black;
                                    """)
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setWordWrap(True)
        content_layout.addWidget(descripcion)

        content_layout.addSpacing(15)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)

        info_layout.addSpacing(10)

        info_hbox1_widget = QWidget()
        info_hbox1 = QHBoxLayout(info_hbox1_widget)
        info_hbox1_widget.setStyleSheet("padding: 5 5px;")

        imagen1_label = QLabel()
        imagen1_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"default.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox1.addWidget(imagen1_label)

        desc1 = QLabel("""Cuenta más a tus clientes a que te dedicas acompañado de una imagen""")
        desc1.setAlignment(Qt.AlignLeft)
        desc1.setStyleSheet("font-size: 12pt;")
        desc1.setWordWrap(True)
        desc1.setFixedWidth(220)
        
        info_hbox1.addWidget(desc1)

        info_layout.addWidget(info_hbox1_widget)

# Segunda Info

        info_hbox2_widget = QWidget()
        info_hbox2 = QHBoxLayout(info_hbox2_widget)
        info_hbox2_widget.setStyleSheet("padding: 5 5px;")

        imagen2_label = QLabel()
        imagen2_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"default.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox2.addWidget(imagen2_label)

        desc2 = QLabel("""Comunica los productos o servicios que ofreces""")
        desc2.setAlignment(Qt.AlignLeft)
        desc2.setStyleSheet("font-size: 12pt;")
        desc2.setWordWrap(True)
        desc2.setFixedWidth(220)
        
        info_hbox2.addWidget(desc2)

        info_layout.addWidget(info_hbox2_widget)

# Tercera Información

        info_hbox3_widget = QWidget()
        info_hbox3 = QHBoxLayout(info_hbox3_widget)
        info_hbox3_widget.setStyleSheet("padding: 5 5px;")

        imagen3_label = QLabel()
        imagen3_label.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"default.png")).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        info_hbox3.addWidget(imagen3_label)

        desc3 = QLabel("""Comparte una foto que sientas importante""")
        desc3.setAlignment(Qt.AlignLeft)
        desc3.setStyleSheet("font-size: 12pt;")
        desc3.setWordWrap(True)
        desc3.setFixedWidth(220)
        
        info_hbox3.addWidget(desc3)

        info_layout.addWidget(info_hbox3_widget)

        content_layout.addWidget(info_widget)

        content_layout.addSpacing(15)

        contacto = QLabel("Contacto")
        contacto.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        numero = QLabel("Número")
        numero.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        Correo = QLabel("Correo")
        Correo.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        redes = QLabel("Perfil de redes Sociales")
        redes.setStyleSheet("""
                            font-size: 12pt;
                            """)
        
        content_layout.addWidget(contacto)
        content_layout.addWidget(numero)
        content_layout.addWidget(Correo)
        content_layout.addWidget(redes)

        content_layout.addStretch()

        layout.addWidget(scroll) 

class Config_user(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.main_window = menu
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        tittle = QLabel("OPCIONES")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(tittle)

        layout.addWidget(contenedor)

        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)

        buttons_layout.addStretch()

        buttons_layout.addSpacing(15)

        conocenos_button = QPushButton("Conócenos", self)
        conocenos_button.clicked.connect(lambda: self.main_window.changeStackIndex(5))
        conocenos_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        buttons_layout.addWidget(conocenos_button)

        buttons_layout.addSpacing(15)

        config_button = QPushButton("Configuración", self)
        config_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        buttons_layout.addWidget(config_button)

        buttons_layout.addSpacing(15)

        cerrar_button = QPushButton("Cerrar Sesión", self)
        cerrar_button.clicked.connect(lambda: self.main_window.main_window.show_login())
        cerrar_button.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                font-weight: bold;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        buttons_layout.addWidget(cerrar_button)
        
        buttons_layout.addStretch()
        layout.addWidget(buttons_widget)

class Config_emp(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.main_window = menu
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #00C08C;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        tittle = QLabel("OPCIONES")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(tittle)

        layout.addWidget(contenedor)

        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)

        buttons_layout.addStretch()

        # Botón para cambiar a la página de membresías
        membresias_button = QPushButton("Membresías", self)
        membresias_button.clicked.connect(lambda: self.main_window.changeStackIndex(4))
        membresias_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        buttons_layout.addWidget(membresias_button)

        buttons_layout.addSpacing(15)

        conocenos_button = QPushButton("Conócenos", self)
        conocenos_button.clicked.connect(lambda: self.main_window.changeStackIndex(5))
        conocenos_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        buttons_layout.addWidget(conocenos_button)

        buttons_layout.addSpacing(15)

        config_button = QPushButton("Configuración", self)
        config_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        buttons_layout.addWidget(config_button)

        buttons_layout.addSpacing(15)

        cerrar_button = QPushButton("Cerrar Sesión", self)
        cerrar_button.clicked.connect(lambda: self.main_window.main_window.show_login())
        cerrar_button.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: red;
                font-weight: bold;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        buttons_layout.addWidget(cerrar_button)
        
        buttons_layout.addStretch()
        layout.addWidget(buttons_widget)

class Membresias(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"cohete_verde_gris.svg")).scaled(QSize(150, 150), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        contenedor_layout.addWidget(logo)

        layout.addWidget(contenedor)

        layout.addSpacing(20)

        tittle = QLabel("MEMBRESÍAS")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""color: #00C08C;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        layout.addWidget(tittle)

        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)

        buttons_layout.addStretch()

        # Botón para cambiar a la página de membresías
        silver_button = QPushButton("SILVER", self)
        silver_button.clicked.connect(lambda: self.menu.changeStackIndex(6))
        silver_button.setStyleSheet("""
            QPushButton {
                background-color: #E6E1E1;
                color: white;
                border-radius: 20px;
                font-size: 15pt;
                font-weight: bold;
                padding: 30 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        buttons_layout.addWidget(silver_button)

        buttons_layout.addSpacing(15)

        gold_button = QPushButton("SAPPHIRE", self)
        gold_button.clicked.connect(lambda: self.menu.changeStackIndex(7))
        gold_button.setStyleSheet("""
            QPushButton {
                background-color: #080c42;
                color: white;
                border-radius: 20px;
                font-size: 15pt;
                font-weight: bold;
                padding: 30 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        buttons_layout.addWidget(gold_button)

        buttons_layout.addSpacing(15)

        emerald_button = QPushButton("EMERALD", self)
        emerald_button.clicked.connect(lambda: self.menu.changeStackIndex(8))
        emerald_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: white;
                border-radius: 20px;
                font-size: 15pt;
                font-weight: bold;
                padding: 30 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        buttons_layout.addWidget(emerald_button)
        
        buttons_layout.addStretch()
        layout.addWidget(buttons_widget)

class Conocenos(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.main_window = menu
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        contenedor1 = QWidget()
        contenedor1.setStyleSheet("""
            QWidget {
                background-color: #E6E1E1;
                border-radius: 20px;
            }
        """)
        contenedor1_layout = QVBoxLayout(contenedor1)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"cohete_verde_gris.svg")).scaled(QSize(150, 150), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        contenedor1_layout.addWidget(logo)

        layout.addWidget(contenedor1)

        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 20px;
            }
        """)
        contenedor_layout = QVBoxLayout(contenedor)

        tittle = QLabel("CONÓCENOS")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""color: #00C08C;
                            font-weight: bold;
                            font-size: 35pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(tittle)

        layout.addWidget(contenedor)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setFixedWidth(390)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)  # Usa content_widget aquí
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        subtittle = QLabel("¿QUÉ ES ENTREPEERS?")
        subtittle.setAlignment(Qt.AlignCenter)
        subtittle.setStyleSheet("""color: #00C08C;
                            font-weight: bold;
                            font-size: 20pt;
                            text-align: center
                            """)
        content_layout.addWidget(subtittle)

        desc = QLabel("""Una plataforma innovadora que te permite compartir tus proyectos, aumentar tu visibilidad y conectar con posibles inversionistas, socios y clientes.
Además, te ofrecemos recomendaciones de información relevante y actualizada, y te facilitamos establecer conexiones confiables.""")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("""color: black;
                            font-size: 12pt;
                            text-align: center
                            """)
        content_layout.addWidget(desc)

        content_layout.addSpacing(20)

        grid_layout = QGridLayout()
        
        foto1 = QPixmap(os.path.join(IMAGE_PATH,"jarden.PNG"))
        foto1 = foto1.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        foto1_label = QLabel()
        foto1_label.setPixmap(foto1)
        foto1_label.setAlignment(Qt.AlignCenter)
        foto1_texto = QLabel("Jarden Ariza\nDirector Operaciones")
        foto1_texto.setAlignment(Qt.AlignCenter)

        v_layout1 = QVBoxLayout()
        v_layout1.addWidget(foto1_label)
        v_layout1.addWidget(foto1_texto)

        foto2 = QPixmap(os.path.join(IMAGE_PATH,"nicolas.jpg"))
        foto2 = foto2.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        foto2_label = QLabel()
        foto2_label.setPixmap(foto2)
        foto2_label.setAlignment(Qt.AlignCenter)
        foto2_texto = QLabel("Nicolas Leyton\nDirector General")
        foto2_texto.setAlignment(Qt.AlignCenter)

        v_layout2 = QVBoxLayout()
        v_layout2.addWidget(foto2_label)
        v_layout2.addWidget(foto2_texto)

        foto3 = QPixmap(os.path.join(IMAGE_PATH,"santiago.jpg"))
        foto3 = foto3.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        foto3_label = QLabel()
        foto3_label.setPixmap(foto3)
        foto3_label.setAlignment(Qt.AlignCenter)
        foto3_texto = QLabel("Santiago Rueda\nDirector Marketing")
        foto3_texto.setAlignment(Qt.AlignCenter)

        v_layout3 = QVBoxLayout()
        v_layout3.addWidget(foto3_label)
        v_layout3.addWidget(foto3_texto)

        foto4 = QPixmap(os.path.join(IMAGE_PATH,"humberto.jpg"))
        foto4 = foto4.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        foto4_label = QLabel()
        foto4_label.setPixmap(foto4)
        foto4_label.setAlignment(Qt.AlignCenter)
        foto4_texto = QLabel("Humberto Sinning\nDirector Financiero")
        foto4_texto.setAlignment(Qt.AlignCenter)

        v_layout4 = QVBoxLayout()
        v_layout4.addWidget(foto4_label)
        v_layout4.addWidget(foto4_texto)

        grid_layout.addLayout(v_layout1, 0, 0)
        grid_layout.addLayout(v_layout2, 0, 1)
        grid_layout.addLayout(v_layout3, 1, 0)
        grid_layout.addLayout(v_layout4, 1, 1)

        content_layout.addLayout(grid_layout)

        content_layout.addSpacing(20)

        mision = QLabel("MISIÓN")
        mision.setStyleSheet("""color: #00C08C;
                            font-weight: bold;
                            font-size: 20pt;
                            text-align: center
                            """)
        content_layout.addWidget(mision)

        desc_mision = QLabel("Facilitar el camino hacia el éxito para los emprendedores en Colombia, proporcionando un ecosistema integral de herramientas, conocimientos y redes de contacto que permitan evolucionar y dar visibilidad a proyectos transformándolos en empresas prósperas y sostenibles.  ")
        desc_mision.setStyleSheet("""color: black;
                            font-size: 12pt;
                            text-align: center
                            """)
        desc_mision.setWordWrap(True)
        content_layout.addWidget(desc_mision)

        content_layout.addSpacing(10)

        vision = QLabel("VISIÓN")
        vision.setStyleSheet("""color: #00C08C;
                            font-weight: bold;
                            font-size: 20pt;
                            text-align: center
                            """)
        content_layout.addWidget(vision)

        desc_vision = QLabel("Ser el referente líder en el impulso del emprendimiento en Colombia y Chile, reconocidos por el compromiso con la excelencia, la innovación continua y el apoyo constante a los sueños empresariales de nuestros clientes. Para el 2029 buscamos alcanzar un impacto positivo en el apalancamiento de 8.000 empresas cada año. ")
        desc_vision.setStyleSheet("""color: black;
                            font-size: 12pt;
                            text-align: center
                            """)
        desc_vision.setWordWrap(True)
        content_layout.addWidget(desc_vision)

        content_layout.addSpacing(20)

        contactanos = QLabel("CONTÁCTANOS")
        contactanos.setStyleSheet("""color: #00C08C;
                            font-weight: bold;
                            font-size: 20pt;
                            text-align: center
                            """)
        content_layout.addWidget(contactanos)

        desc_contactanos = QLabel("entrepeers3@gmail.com")
        desc_contactanos.setStyleSheet("""color: black;
                            font-size: 12pt;
                            text-align: center
                            """)
        content_layout.addWidget(desc_contactanos)

        content_layout.addSpacing(20)

        pqrs = QLabel("PQRS")
        pqrs.setStyleSheet("""color: #00C08C;
                            font-weight: bold;
                            font-size: 20pt;
                            text-align: center
                            """)
        content_layout.addWidget(pqrs)

        pqrs_edit = QLineEdit()
        pqrs_edit.setPlaceholderText("Cuadro de texto")
        pqrs_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                border-radius: 15px;
                padding: 5px;
                font-size: 16px;
            }
        """)
        content_layout.addWidget(pqrs_edit)

        content_layout.addSpacing(20)

        gusta = QLabel("¿TE GUSTA ENTREPEERS")
        gusta.setStyleSheet("""color: #00C08C;
                            font-weight: bold;
                            font-size: 20pt;
                            text-align: center
                            """)
        gusta.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(gusta)

        calif_button = QPushButton("Califícanos", self)
        calif_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: black;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        content_layout.addWidget(calif_button)

        content_layout.addSpacing(20)

        mejorar_edit = QLineEdit()
        mejorar_edit.setPlaceholderText("¿En qué podemos mejorar?")
        mejorar_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                border-radius: 15px;
                padding: 5px;
                font-size: 16px;
            }
        """)
        content_layout.addWidget(mejorar_edit)


        content_layout.addStretch()

        layout.addWidget(scroll)

class Silver(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.main_window = menu
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        contenedor1 = QWidget()
        contenedor1.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 20px;
            }
        """)
        contenedor1_layout = QVBoxLayout(contenedor1)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"cohete_negro.svg")).scaled(QSize(100, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        contenedor1_layout.addWidget(logo)

        layout.addWidget(contenedor1)

        contenedor_widget = QWidget()
        contenedor_widget.setStyleSheet("background-color: #E6E1E1; border-radius: 20px;")
        contenedor_layout = QVBoxLayout(contenedor_widget)

        contenedor_layout.addStretch()

        tittle = QLabel("SILVER")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 30pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(tittle)

        contenedor_layout.addSpacing(15)

        text = QLabel("""1. Acceso a la plataforma: Crea tu cuenta y establece un perfil
básico para comenzar tu viaje.\n2. Conexiones limitadas: Conecta con otros emprendedores dentro
de un límite establecido.\n3. Mensajería limitada: Comunícate con otros miembros de la
plataforma dentro de un límite de mensajes por día o por
semana.\n4. Acceso a eventos públicos: Mantente al tanto de los eventos
públicos y regístrate para asistir.\n5. Acceso limitado a recursos de aprendizaje: Accede a una
selección de nuestros recursos de aprendizaje para ayudarte a
crecer y desarrollar tu empresa.\n6. Soporte al cliente básico: Recibe asistencia de nuestro equipo de
soporte al cliente.\n\nPrecio: $60.000/Mensual
                        """)
        text.setStyleSheet("""
                            font-size: 10pt;""")
        text.setWordWrap(True)
        text.setAlignment(Qt.AlignCenter)

        contenedor_layout.addWidget(text)
        
        contenedor_layout.addSpacing(15)

        unirse_button = QPushButton("¡Únete Ahora!", self)
        unirse_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        contenedor_layout.addWidget(unirse_button)

        volver_button = QPushButton("Volver")
        volver_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #00C08C;
                border-radius: 10px;
                padding: 12 30px;
                font-size: 15pt;
                text-align: center;
                margin-top: 15px;
            }
        """)
        volver_button.clicked.connect(lambda: self.main_window.changeStackIndex(4))
        contenedor_layout.addWidget(volver_button)

        contenedor_layout.addStretch()

        layout.addWidget(contenedor_widget)

class Gold(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.main_window = menu
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        contenedor1 = QWidget()
        contenedor1.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 20px;
            }
        """)
        contenedor1_layout = QVBoxLayout(contenedor1)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"cohete_azul.svg")).scaled(QSize(100, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        contenedor1_layout.addWidget(logo)

        layout.addWidget(contenedor1)

        contenedor_widget = QWidget()
        contenedor_widget.setStyleSheet("background-color: #080c42;border-radius: 20px;")
        contenedor_layout = QVBoxLayout(contenedor_widget)

        contenedor_layout.addStretch()

        tittle = QLabel("SHAPPHIRE")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""color: white;
                            font-weight: bold;
                            font-size: 30pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(tittle)

        contenedor_layout.addSpacing(15)

        text = QLabel("""1. Conexiones ilimitadas: Conecta con tantos
emprendedores como desees, sin restricciones.\n2. Mensajería ilimitada: Comunícate sin límites con
otros miembros de la plataforma.\n3. Acceso a eventos exclusivos: Obtén acceso a
eventos exclusivos para miembros intermedios y
superiores.\n4. Acceso a todos los recursos de aprendizaje:
Accede a todos nuestros recursos de aprendizaje
para ayudarte a crecer y desarrollar tu empresa.\n5. Soporte al cliente prioritario: Recibe asistencia
prioritaria de nuestro equipo de soporte al cliente.\n6. Promoción de perfil: Aumenta tu visibilidad con la
promoción de tu perfil dentro de la plataforma.\n\nPrecio: $90,000/Mensual
                        """)
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("""color: white; font-size: 10pt;""")
        text.setWordWrap(True)
        contenedor_layout.addWidget(text)

        contenedor_layout.addSpacing(15)

        unirse_button = QPushButton("¡Únete Ahora!", self)
        unirse_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        contenedor_layout.addWidget(unirse_button)

        volver_button = QPushButton("Volver")
        volver_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #00C08C;
                border-radius: 10px;
                padding: 12 30px;
                font-size: 15pt;
                text-align: center;
                margin-top: 15px;
            }
        """)
        volver_button.clicked.connect(lambda: self.main_window.changeStackIndex(4))
        contenedor_layout.addWidget(volver_button)

        contenedor_layout.addStretch()

        layout.addWidget(contenedor_widget)

class Emerald(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.main_window = menu
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        contenedor1 = QWidget()
        contenedor1.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 20px;
            }
        """)
        contenedor1_layout = QVBoxLayout(contenedor1)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_PATH,"cohete_verde.svg")).scaled(QSize(100, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        contenedor1_layout.addWidget(logo)

        layout.addWidget(contenedor1)

        contenedor_widget = QWidget()
        contenedor_widget.setStyleSheet("background-color: #00C08C;border-radius: 20px;")
        contenedor_layout = QVBoxLayout(contenedor_widget)

        contenedor_layout.addStretch()

        tittle = QLabel("EMERALD")
        tittle.setAlignment(Qt.AlignCenter)
        tittle.setStyleSheet("""color: black;
                            font-weight: bold;
                            font-size: 30pt;
                            text-align: center
                            """)
        contenedor_layout.addWidget(tittle)

        contenedor_layout.addSpacing(2)

        text = QLabel("""1. Conexiones ilimitadas: Conecta con tantos emprendedores como
desees, sin restricciones.\n2. Mensajería ilimitada: Comunícate sin límites con otros miembros
de la plataforma.\n3. Acceso a todos los eventos: Obtén acceso a todos los eventos,
incluyendo aquellos exclusivos para miembros premium.\n4. Acceso total a recursos de aprendizaje: Accede a todos nuestros
recursos de aprendizaje para ayudarte a crecer y desarrollar tu
empresa.\n5. Soporte al cliente prioritario: Recibe asistencia prioritaria de
nuestro equipo de soporte al cliente.\n6. Promoción de perfil: Aumenta tu visibilidad con la promoción de tu
perfil dentro de la plataforma.\n7. Oportunidades de networking exclusivas: Participa en eventos de
networking exclusivos para miembros premium.\n8. Publicidad gratuita: Promociona tus productos o servicios en la
plataforma de forma gratuita.\n\nPrecio: $120,000/Mensual
                        """)
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("""
                            font-size: 9pt;""")
        text.setWordWrap(True)

        contenedor_layout.addWidget(text)

        contenedor_layout.addSpacing(5)

        unirse_button = QPushButton("¡Únete Ahora!", self)
        unirse_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 20px;
                font-size: 15pt;
                padding: 12 30px;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)
        contenedor_layout.addWidget(unirse_button)

        volver_button = QPushButton("Volver")
        volver_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #00C08C;
                border-radius: 10px;
                padding: 12 30px;
                font-size: 15pt;
                text-align: center;
                margin-top: 15px;
            }
        """)
        volver_button.clicked.connect(lambda: self.main_window.changeStackIndex(4))
        contenedor_layout.addWidget(volver_button)

        contenedor_layout.addStretch()

        layout.addWidget(contenedor_widget)              

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        self.clicked.emit()

class EmprendimientoWidget(QWidget):
    clicked = pyqtSignal(str, str, str, str)

    def __init__(self, nombre, descripcion, categoria, icon_path = os.path.join(IMAGE_PATH,"default.png"), url = "ola!"):
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.icon_path = icon_path
        self.url = url
        self.setupUI(nombre, descripcion, categoria, icon_path = os.path.join(IMAGE_PATH,"default.png"), url = "ola!")
    
    def setupUI(self, nombre, descripcion, categoria, icon_path, url):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes
        layout.setSpacing(0)  # Elimina el espacio entre widgets

        emp_click = ClickableWidget()
        emp_click_layout = QVBoxLayout(emp_click)
        emp_click.clicked.connect(self.emit_info)        
        emp_contenedor = QWidget()
        emp_contenedor.setFixedHeight(120)
        emp_contenedor.setStyleSheet("""
                    QWidget {
                        background-color: #E6E1E1;
                        border-radius: 10px;
                        padding: 2 5px
                    }
                """)
        hbox_emp2 = QHBoxLayout(emp_contenedor)

        imagen_label = QLabel()
        pixmap = QPixmap(self.icon_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        imagen_label.setPixmap(pixmap)
        
        vbox_layout = QVBoxLayout()
        nombre_label = QLabel(self.nombre)
        nombre_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        
        descripcion_label = QLabel(self.descripcion)
        descripcion_label.setStyleSheet("font-size: 12px; color: black;")
        descripcion_label.setFixedWidth(230)
        descripcion_label.setWordWrap(True)
        
        categoria_label = QLabel(self.categoria)
        categoria_label.setStyleSheet("font-size: 12px; color: black;")
        
        vbox_layout.addWidget(nombre_label)
        vbox_layout.addWidget(descripcion_label)
        vbox_layout.addWidget(categoria_label)
        
        hbox_emp2.addWidget(imagen_label)
        hbox_emp2.addLayout(vbox_layout)

        emp_click_layout.addWidget(emp_contenedor)
        layout.addWidget(emp_click)
    
    def emit_info(self):
        self.clicked.emit(self.nombre, self.descripcion, self.categoria, self.icon_path)

class SocioWidget(QWidget):

    def __init__(self, nombre, icon_path=os.path.join(IMAGE_PATH,"default.png")):
        super().__init__()
        self.setupUI(nombre, icon_path)
    
    def setupUI(self, nombre, icon_path):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes

        socio1 = QWidget()
        socio1_layout = QVBoxLayout(socio1)
        socio1.setStyleSheet("""
                            background-color: #E6E1E1;
                            border-radius: 10px;
                            """)
        socio1.setFixedWidth(100)
        socio1_perfil = QPixmap(icon_path)
        
        socio1_perfil = socio1_perfil.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        socio1_perfil_label = QLabel()
        socio1_perfil_label.setPixmap(socio1_perfil)
        socio1_perfil_label.setAlignment(Qt.AlignCenter)
        socio1_perfil_label.setStyleSheet("""
                                            QLabel {
                                                border-radius: 10px;
                                            }
                                        """)
        socio1_layout.addWidget(socio1_perfil_label)

        socio1_nombre = QLabel(nombre)
        socio1_nombre.setAlignment(Qt.AlignCenter)
        socio1_nombre.setStyleSheet("""
                            font-size: 12pt;
                            """)
        socio1_layout.addWidget(socio1_nombre)

        socio1_button = QPushButton("Ver")
        socio1_button.setStyleSheet("""
            QPushButton {
                background-color: #00C08C;
                color: black;
                border-radius: 5px;
                padding: 5 5px;
                font-size: 12pt;
                text-align: center;
                margin-bottom: 5px;
            }
        """)
        socio1_layout.addWidget(socio1_button)

        layout.addWidget(socio1)

class ClickableWidget(QWidget):
    clicked = pyqtSignal()  # Señal personalizada para manejar los clics

    def __init__(self, parent=None):
        super(ClickableWidget, self).__init__(parent)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emitir la señal cuando se hace clic en el widget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
