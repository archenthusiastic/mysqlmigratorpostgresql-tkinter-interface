from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from components.dialogs.add import AddRecordDialog
from components.dialogs.edit import EditRecordDialog
from defensa.function import agregar_parentesis

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
        """Cargar los datos de la tabla seleccionada."""
        try:
            if not table_name:
                return
            clients_names = self.get_client_names(self.postgres_cursor)
            clients_ids = self.get_client_ids(self.postgres_cursor)
            print(clients_ids)
            print(clients_names)
            parentesis = self.agregar_parentesis(clients_names)
            print(parentesis)
            self.actualizar_registros(self.postgres_conn,
                    self.postgres_cursor,
                    tabla="clientes",
                    columna_a_actualizar="parentesis",
                    ids=clients_ids,
                    valores=parentesis
                )
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
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos: {e}")

    def add_record(self):
        table_name = self.table_selector.currentText()
        dialog = AddRecordDialog(self, table_name, self.postgres_conn, self.postgres_cursor)
        if dialog.exec():
            self.load_table_data(table_name)

    def edit_record(self):
        table_name = self.table_selector.currentText()
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un registro para modificar.")
            return

        record_id = self.table.item(selected_row, 0).text()  # Usa id_auto como columna clave
        dialog = EditRecordDialog(self, table_name, self.postgres_conn, self.postgres_cursor, record_id)
        if dialog.exec():
            self.load_table_data(table_name)

    def delete_record(self):
        table_name = self.table_selector.currentText()
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un registro para eliminar.")
            return

        try:
            self.postgres_cursor.execute(f"SELECT * FROM {table_name} LIMIT 1;")
            first_column = self.postgres_cursor.description[0][0]

            record_id = self.table.item(selected_row, 0).text()

            confirmation = QMessageBox.question(
                self,
                "Confirmación",
                f"¿Eliminar registro con {first_column} = {record_id}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirmation == QMessageBox.Yes:
                query = f"DELETE FROM {table_name} WHERE {first_column} = %s;"
                self.postgres_cursor.execute(query, (record_id,))
                self.postgres_conn.commit()

                self.load_table_data(table_name)
        except Exception as e:
            self.postgres_conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el registro: {e}")

    def get_client_names(self, cursor):
        """
        Recolecta los nombres de la tabla 'clientes'.
        :param cursor: Cursor activo de la conexión a PostgreSQL.
        :return: Lista de nombres.
        """
        try:
            cursor.execute("SELECT nombre FROM clientes;")
            nombres = [row[0] for row in cursor.fetchall()]
            return nombres
        except Exception as e:
            print(f"Error al obtener los nombres: {e}")
            return []

    def get_client_ids(self, cursor):
        """
        Recolecta los IDs de la tabla 'clientes'.
        :param cursor: Cursor activo de la conexión a PostgreSQL.
        :return: Lista de IDs.
        """
        try:
            cursor.execute("SELECT id_cliente FROM clientes;")
            ids = [row[0] for row in cursor.fetchall()]
            return ids
        except Exception as e:
            print(f"Error al obtener los IDs: {e}")
            return []

    def agregar_parentesis(self, lista_nombres):
            resultado_final = []
        
            for cadena in lista_nombres:
                longitud = len(cadena)
                resultado = []

                mitad = longitud // 2

                for i, char in enumerate(cadena):
                    if i < mitad:
                        if i > 0:
                            resultado.append('(')
                        resultado.append(char)
                    elif longitud % 2 == 0 and i == mitad:
                        resultado.append(char)
                        resultado.append(')')
                    elif longitud % 2 == 0 and i == mitad + 1:
                        resultado.append(char)
                    else:
                        resultado.append(char)
                        if i < longitud - 1:
                            resultado.append(')')

                resultado_final.append(''.join(resultado))

            return resultado_final


    def actualizar_registros(self, postgres_conn, postgres_cursor, tabla, columna_a_actualizar, ids, valores):
        """
        Actualiza registros en la base de datos PostgreSQL de forma dinámica.
        
        :param postgres_conn: Objeto de conexión a PostgreSQL.
        :param postgres_cursor: Cursor activo de la conexión.
        :param tabla: Nombre de la tabla.
        :param columna_a_actualizar: Nombre de la columna a actualizar.
        :param ids: Lista de IDs que sirven como condición.
        :param valores: Lista de nuevos valores a insertar.
        """
        if len(ids) != len(valores):
            print("Error: Las listas de IDs y valores deben tener la misma longitud.")
            return

        try:
            query = f"UPDATE {tabla} SET {columna_a_actualizar} = %s WHERE id_cliente = %s;"
            
            for id_cliente, valor in zip(ids, valores):
                postgres_cursor.execute(query, (valor, id_cliente))
            
            postgres_conn.commit()
            print("Registros actualizados exitosamente.")
        except Exception as e:
            postgres_conn.rollback()
            print(f"Error al actualizar registros: {e}")

    
