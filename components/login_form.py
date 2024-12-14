from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from components.main_window import MainWindow
from mysqlmigratorpostgresql import MysqlMigratorPostgresql

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulario de Conexión")
        self.setGeometry(100, 100, 400, 500)

        self.migrator = MysqlMigratorPostgresql()

        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("Conexión a MySQL y PostgreSQL")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        mysql_form = QFormLayout()
        mysql_title = QLabel("MySQL")
        mysql_title.setAlignment(Qt.AlignCenter)
        mysql_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(mysql_title)

        self.mysql_host_input = QLineEdit()
        self.mysql_host_input.setPlaceholderText("Host")
        mysql_form.addRow("Host:", self.mysql_host_input)

        self.mysql_port_input = QLineEdit()
        self.mysql_port_input.setPlaceholderText("Port")
        mysql_form.addRow("Port:", self.mysql_port_input)

        self.mysql_user_input = QLineEdit()
        self.mysql_user_input.setPlaceholderText("User")
        mysql_form.addRow("User:", self.mysql_user_input)

        self.mysql_password_input = QLineEdit()
        self.mysql_password_input.setEchoMode(QLineEdit.Password)
        self.mysql_password_input.setPlaceholderText("Password")
        mysql_form.addRow("Password:", self.mysql_password_input)

        self.mysql_database_input = QLineEdit()
        self.mysql_database_input.setPlaceholderText("Database")
        mysql_form.addRow("Database:", self.mysql_database_input)

        layout.addLayout(mysql_form)

        postgres_form = QFormLayout()
        postgres_title = QLabel("PostgreSQL")
        postgres_title.setAlignment(Qt.AlignCenter)
        postgres_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(postgres_title)

        self.postgres_host_input = QLineEdit()
        self.postgres_host_input.setPlaceholderText("Host")
        postgres_form.addRow("Host:", self.postgres_host_input)

        self.postgres_port_input = QLineEdit()
        self.postgres_port_input.setPlaceholderText("Port")
        postgres_form.addRow("Port:", self.postgres_port_input)

        self.postgres_user_input = QLineEdit()
        self.postgres_user_input.setPlaceholderText("User")
        postgres_form.addRow("User:", self.postgres_user_input)

        self.postgres_password_input = QLineEdit()
        self.postgres_password_input.setEchoMode(QLineEdit.Password)
        self.postgres_password_input.setPlaceholderText("Password")
        postgres_form.addRow("Password:", self.postgres_password_input)

        self.postgres_database_input = QLineEdit()
        self.postgres_database_input.setPlaceholderText("Database")
        postgres_form.addRow("Database:", self.postgres_database_input)

        layout.addLayout(postgres_form)

        self.connect_button = QPushButton("Conectar y Migrar")
        self.connect_button.setStyleSheet("padding: 10px; font-size: 14px;")
        self.connect_button.clicked.connect(self.migrate_and_connect)
        layout.addWidget(self.connect_button, alignment=Qt.AlignCenter)

    def migrate_and_connect(self):
        try:
            self.migrator.connect_mysql(
                host=self.mysql_host_input.text(),
                port=int(self.mysql_port_input.text()),
                user=self.mysql_user_input.text(),
                password=self.mysql_password_input.text(),
                database=self.mysql_database_input.text()
            )
            QMessageBox.information(self, "Conexión MySQL", "Conexión a MySQL exitosa.")

            self.migrator.connect_postgresql(
                host=self.postgres_host_input.text(),
                port=int(self.postgres_port_input.text()),
                user=self.postgres_user_input.text(),
                password=self.postgres_password_input.text(),
                database=self.postgres_database_input.text()
            )
            QMessageBox.information(self, "Conexión PostgreSQL", "Conexión a PostgreSQL exitosa.")

            self.migrator.migrate_all()
            QMessageBox.information(self, "Migración", "Migración completada con éxito.")

            postgres_conn = self.migrator.postgres_conn
            postgres_cursor = self.migrator.postgres_cursor

            self.main_window = MainWindow(postgres_conn, postgres_cursor)
            self.main_window.show()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error durante la conexión o migración: {e}")
