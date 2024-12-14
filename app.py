from PySide6.QtWidgets import QApplication
from components.login_form import LoginForm
from db.db_conn import connect_mysql, connect_postgresql
from db.migration import migrate_all_tables
from components.main_window import MainWindow

class App:
    def __init__(self):
        self.mysql_connected = False
        self.postgresql_connected = False

    def start(self):
        app = QApplication([])
        window = LoginForm()
        window.show()
        app.exec()


if __name__ == "__main__":
    
    App().start()
