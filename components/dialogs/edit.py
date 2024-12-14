from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt

class EditRecordDialog(QDialog):
    def __init__(self, parent, table_name, postgres_conn, postgres_cursor, record_id):
        super().__init__(parent)
        self.setWindowTitle(f"Editar Registro en {table_name}")
        self.setGeometry(300, 300, 400, 300)

        self.table_name = table_name
        self.postgres_conn = postgres_conn
        self.postgres_cursor = postgres_cursor
        self.record_id = record_id
        self.fields = {}

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        self.postgres_cursor.execute(f"SELECT * FROM {table_name} WHERE id_auto = %s", (record_id,))
        record = self.postgres_cursor.fetchone()
        columns = [desc[0] for desc in self.postgres_cursor.description]

        for index, column_name in enumerate(columns):
            field = QLineEdit(str(record[index]))
            form_layout.addRow(column_name, field)
            self.fields[column_name] = field

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
            updates = [f"{column} = %s" for column in self.fields.keys()]
            values = [field.text() for field in self.fields.values()]
            values.append(self.record_id)

            sql = f"UPDATE {self.table_name} SET {', '.join(updates)} WHERE id_auto = %s"
            self.postgres_cursor.execute(sql, values)
            self.postgres_conn.commit()

            QMessageBox.information(self, "Éxito", "Registro actualizado con éxito.")
            self.accept()
        except Exception as e:
            self.postgres_conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el registro: {e}")
