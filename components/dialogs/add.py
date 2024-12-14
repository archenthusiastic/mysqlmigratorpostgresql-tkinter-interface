from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt

class AddRecordDialog(QDialog):
    def __init__(self, parent, table_name, postgres_conn, postgres_cursor):
        super().__init__(parent)
        self.setWindowTitle(f"Añadir Registro a {table_name}")
        self.setGeometry(300, 300, 400, 300)

        self.table_name = table_name
        self.postgres_conn = postgres_conn
        self.postgres_cursor = postgres_cursor
        self.fields = {}

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        # Obtener columnas excepto las seriales (id_auto)
        self.postgres_cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}' AND column_default IS NULL;
        """)
        columns = self.postgres_cursor.fetchall()

        for column_name, data_type in columns:
            field = QLineEdit()
            field.setPlaceholderText(f"Tipo: {data_type}")
            form_layout.addRow(column_name, field)
            self.fields[column_name] = field

        # Botones
        button_layout = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_record)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def save_record(self):
        try:
            columns = list(self.fields.keys())
            values = [field.text() for field in self.fields.values()]

            placeholders = ", ".join(["%s"] * len(values))
            columns_str = ", ".join(columns)
            sql = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders})"

            self.postgres_cursor.execute(sql, values)
            self.postgres_conn.commit()

            QMessageBox.information(self, "Éxito", "Registro agregado con éxito.")
            self.accept()
        except Exception as e:
            self.postgres_conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo guardar el registro: {e}")
