from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt

class EditRecordDialog(QDialog):
    def __init__(self, parent, table_name, postgres_conn, postgres_cursor, record_id):
        super().__init__(parent)
        self.setWindowTitle(f"Modificar Registro en {table_name}")
        self.setGeometry(300, 300, 400, 300)

        self.table_name = table_name
        self.postgres_conn = postgres_conn
        self.postgres_cursor = postgres_cursor
        self.record_id = record_id
        self.fields = {}

        # Layout principal
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        # Obtener columnas y datos del registro
        try:
            # Consultar columnas de la tabla
            self.postgres_cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' AND table_schema = 'public';
            """)
            columns = self.postgres_cursor.fetchall()

            # Consultar datos del registro
            self.postgres_cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
            record = self.postgres_cursor.fetchone()

            # Validar que el registro exista
            if record is None:
                raise ValueError(f"No se encontró ningún registro con ID {record_id} en la tabla {table_name}.")

            # Crear campos del formulario
            for index, (column_name, data_type) in enumerate(columns):
                if column_name == "id":  # No modificar la columna `id`
                    continue
                field = QLineEdit(str(record[index]))
                field.setPlaceholderText(f"Tipo: {data_type}")
                form_layout.addRow(column_name, field)
                self.fields[column_name] = field

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar el registro: {e}")
            self.reject()

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
        """Guardar los cambios realizados."""
        try:
            columns = list(self.fields.keys())
            values = [field.text() for field in self.fields.values()]
            set_clause = ", ".join([f"{col} = %s" for col in columns])

            sql = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"
            self.postgres_cursor.execute(sql, values + [self.record_id])
            self.postgres_conn.commit()

            QMessageBox.information(self, "Éxito", "Registro modificado con éxito.")
            self.accept()
        except Exception as e:
            self.postgres_conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo modificar el registro: {e}")
