from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from components.dialogs.add import AddRecordDialog
from components.dialogs.edit import EditRecordDialog

class MainWindow(QWidget):
    def __init__(self, postgres_conn, postgres_cursor):
        super().__init__()
        self.setWindowTitle("Gestión de Base de Datos PostgreSQL")
        self.setGeometry(100, 100, 900, 600)

        self.postgres_conn = postgres_conn
        self.postgres_cursor = postgres_cursor

        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Selector de tablas
        self.table_selector = QComboBox()
        self.table_selector.currentTextChanged.connect(self.load_table_data)
        main_layout.addWidget(self.table_selector)

        # Tabla para mostrar los datos
        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        # Botones CRUD
        crud_layout = QHBoxLayout()

        add_button = QPushButton("Agregar")
        add_button.clicked.connect(self.add_record)
        crud_layout.addWidget(add_button)

        edit_button = QPushButton("Modificar")
        edit_button.clicked.connect(self.edit_record)
        crud_layout.addWidget(edit_button)

        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(self.delete_record)
        crud_layout.addWidget(delete_button)

        main_layout.addLayout(crud_layout)

        # Cargar tablas
        self.load_tables()

    def load_tables(self):
        """Cargar la lista de tablas de la base de datos."""
        try:
            self.postgres_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = [row[0] for row in self.postgres_cursor.fetchall()]
            self.table_selector.addItems(tables)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las tablas: {e}")

    def load_table_data(self, table_name):
        """Cargar los datos de la tabla seleccionada en el widget de la tabla."""
        try:
            if not table_name:
                return

            self.postgres_cursor.execute(f"SELECT * FROM {table_name};")
            rows = self.postgres_cursor.fetchall()
            columns = [desc[0] for desc in self.postgres_cursor.description]

            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(columns))
            self.table.setHorizontalHeaderLabels(columns)

            for row_index, row in enumerate(rows):
                for col_index, value in enumerate(row):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos de la tabla: {e}")

    def add_record(self):
        """Abrir diálogo para agregar un registro."""
        table_name = self.table_selector.currentText()
        if not table_name:
            QMessageBox.warning(self, "Error", "No hay ninguna tabla seleccionada.")
            return

        dialog = AddRecordDialog(self, table_name, self.postgres_conn, self.postgres_cursor)
        if dialog.exec():
            self.load_table_data(table_name)  # Recargar datos después de agregar

    def edit_record(self):
        """Abrir diálogo para modificar un registro."""
        table_name = self.table_selector.currentText()
        if not table_name:
            QMessageBox.warning(self, "Error", "No hay ninguna tabla seleccionada.")
            return

        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un registro para modificar.")
            return

        try:
            record_id = self.table.item(selected_row, 0).text()  # Asume que la columna `id` está en la posición 0
            if not record_id:
                raise ValueError("El registro seleccionado no tiene un ID válido.")

            dialog = EditRecordDialog(self, table_name, self.postgres_conn, self.postgres_cursor, record_id)
            if dialog.exec():
                self.load_table_data(table_name)  # Recargar datos después de modificar
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el diálogo de edición: {e}")

    def delete_record(self):
        """Eliminar el registro seleccionado."""
        table_name = self.table_selector.currentText()
        if not table_name:
            QMessageBox.warning(self, "Error", "No hay ninguna tabla seleccionada.")
            return

        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un registro para eliminar.")
            return

        try:
            record_id = self.table.item(selected_row, 0).text()  # Asume que la columna `id` está en la posición 0
            if not record_id:
                raise ValueError("El registro seleccionado no tiene un ID válido.")

            confirmation = QMessageBox.question(
                self,
                "Confirmación",
                f"¿Seguro que deseas eliminar el registro con ID {record_id}?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirmation == QMessageBox.Yes:
                self.postgres_cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (record_id,))
                self.postgres_conn.commit()
                QMessageBox.information(self, "Éxito", "Registro eliminado con éxito.")
                self.load_table_data(table_name)  # Recargar datos después de eliminar
        except Exception as e:
            self.postgres_conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el registro: {e}")
