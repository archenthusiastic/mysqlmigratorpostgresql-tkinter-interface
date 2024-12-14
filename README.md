# Gestión y Migración de Bases de Datos con Python

## Descripción del Proyecto

Este proyecto consiste en la creación de una aplicación en Python que permite gestionar y migrar datos entre bases de datos **MySQL** y **PostgreSQL**. La solución está diseñada para modernizar sistemas heredados, facilitando la interacción con datos mediante una interfaz gráfica intuitiva. Adicionalmente, incluye funcionalidades CRUD (Crear, Leer, Actualizar y Eliminar) para gestionar los registros en ambas bases de datos.

---

## Características

1. **Migración de Datos:**
   - Migración de datos completa desde MySQL a PostgreSQL mediante una librería personalizada `mysqlmigratorpostgresql`.
   - Migración inversa desde PostgreSQL a MySQL de manera manual.

2. **Gestión de Registros:**
   - Visualización de registros de tablas en tiempo real.
   - Funciones CRUD (Agregar, Modificar, Eliminar) disponibles para ambas bases de datos.

3. **Cambio de Base de Datos:**
   - Posibilidad de alternar entre MySQL y PostgreSQL en la interfaz gráfica.

4. **Validación y Manejo de Errores:**
   - Manejo de errores en conexiones y operaciones de base de datos.
   - Validación de datos ingresados por el usuario.

5. **Estructura Modular:**
   - Código modular para facilitar la lectura, mantenimiento y escalabilidad.

---

## Casos de Uso

1. **Administrador de Sistemas:**
   - Realizar migraciones de datos desde un sistema antiguo (MySQL) a un sistema moderno (PostgreSQL).
   - Gestionar los datos en ambas bases de datos sin complicaciones.

2. **Desarrollador:**
   - Construir y probar aplicaciones que interactúen con bases de datos relacionales.
   - Realizar modificaciones a los esquemas de datos existentes.

---

## Requisitos Técnicos

- **Lenguaje:** Python 3.8+
- **Bibliotecas:** 
  - `PySide6` (para la interfaz gráfica)
  - `mysql-connector-python` (para conexión MySQL)
  - `psycopg2` (para conexión PostgreSQL)
- **Gestores de Bases de Datos:**
  - MySQL
  - PostgreSQL

---

## Instalación

1. **Clona el Repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/gestion_bd.git
   cd gestion_bd
   ```

2. **Instala las Dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura las Bases de Datos:**
   - Asegúrate de tener configuradas las bases de datos MySQL y PostgreSQL.
   - Actualiza las credenciales en el formulario de login de la aplicación.

---

## Ejecución

1. **Inicia la Aplicación:**
   ```bash
   python app.py
   ```

2. **Flujo de Trabajo:**
   - Ingresa las credenciales de MySQL y PostgreSQL en el formulario de login.
   - Presiona el botón "Conectar y Migrar" para realizar la migración de MySQL a PostgreSQL.
   - Visualiza, agrega, modifica o elimina registros en cualquiera de las bases de datos.
   - Cambia entre MySQL y PostgreSQL utilizando el botón "Cambiar de Base de Datos".

---

## Diseño Relacional

### Esquema Normalizado

![Diseño Relacional](https://media.discordapp.net/attachments/1313628387146731540/1317322820178673725/ConcesionariaFord_DB.png?ex=675e43fb&is=675cf27b&hm=0e061501db6f57a0ca17407d717a5f7a83bb410466aacf4a80b40b043a32791c&=&format=webp&quality=lossless)

- El diseño cumple con la 3ra Forma Normal.
- Las relaciones entre tablas son claras y bien definidas.

- Un cliente puede tener múltiples ventas, pero una venta pertenece a un solo cliente.
Autos y Ventas:

- Un auto puede aparecer en múltiples ventas, pero cada venta registra un auto específico.
Empleados y Servicios:

- Un empleado puede encargarse de múltiples servicios, pero cada servicio está asignado a un único empleado.
Proveedores:

- Relación independiente para administrar información de proveedores. Puede ser extendida para conectar a Autos si los proveedores están relacionados con inventarios.
---

## Pruebas

### Migración de Datos
- Verificación de integridad de datos entre MySQL y PostgreSQL.
- Validación de no duplicación de registros tras migraciones repetidas.

### Funcionalidades CRUD
- Confirmación de que los cambios realizados en la interfaz se reflejan en la base de datos.
- Validación de errores en operaciones como inserción de datos no válidos.

### Cierre de Conexión
- Validación de cierre correcto de conexiones al salir de la aplicación.

---

## Estructura del Proyecto

```plaintext
gestion_bd/
├── app.py                   # Archivo principal
├── components/              # Componentes de la interfaz gráfica
│   ├── login_form.py        # Formulario de conexión
│   ├── main_window.py       # Ventana principal con funcionalidades CRUD
│   └── dialogs/             # Diálogos para agregar y modificar registros
│       ├── add_dialog.py
│       ├── edit_dialog.py
├── db/                      # Módulo para conexión y migración
│   ├── db_conn.py           # Conexión a MySQL y PostgreSQL
│   └── migration.py         # Funciones de migración
├── README.md                # Documentación del proyecto
├── requirements.txt         # Dependencias del proyecto
```


<h4 align="center">App</h2>

  ```python
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
  ```

<h4 align="center">Estructura Funciones</h2>
<details>
<summary>edit</summary>
  
  ```python
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

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        try:
            self.postgres_cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' AND table_schema = 'public';
            """)
            columns = self.postgres_cursor.fetchall()

            self.postgres_cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
            record = self.postgres_cursor.fetchone()

            if record is None:
                raise ValueError(f"No se encontró ningún registro con ID {record_id} en la tabla {table_name}.")

            for index, (column_name, data_type) in enumerate(columns):
                if column_name == "id":
                    continue
                field = QLineEdit(str(record[index]))
                field.setPlaceholderText(f"Tipo: {data_type}")
                form_layout.addRow(column_name, field)
                self.fields[column_name] = field

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar el registro: {e}")
            self.reject()

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
            set_clause = ", ".join([f"{col} = %s" for col in columns])

            sql = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"
            self.postgres_cursor.execute(sql, values + [self.record_id])
            self.postgres_conn.commit()

            QMessageBox.information(self, "Éxito", "Registro modificado con éxito.")
            self.accept()
        except Exception as e:
            self.postgres_conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo modificar el registro: {e}")

```
</details>

<details>
<summary>add</summary>

  ```python
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

        self.postgres_cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}' AND table_schema = 'public';
        """)
        columns = self.postgres_cursor.fetchall()

        for column_name, data_type in columns:
            field = QLineEdit()
            field.setPlaceholderText(f"Tipo: {data_type}")
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
            columns = list(self.fields.keys())
            values = [field.text() for field in self.fields.values()]

            placeholders = ", ".join(["%s"] * len(values))
            columns_str = ", ".join(columns)
            sql = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders})"

            self.postgres_cursor.execute(sql, values)
            self.postgres_conn.commit()

            QMessageBox.information(self, "Exito", "Registro agregado con exito.")
            self.accept()
        except Exception as e:
            self.postgres_conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo guardar el registro: {e}")

```
</details>

<details>
<summary>login_form</summary>

  ```python
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

```
</details>

<details>
  <summary>main window</summary>

  ```cpp
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

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.table_selector = QComboBox()
        self.table_selector.currentTextChanged.connect(self.load_table_data)
        main_layout.addWidget(self.table_selector)

        self.table = QTableWidget()
        main_layout.addWidget(self.table)

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

        self.load_tables()

    def load_tables(self):
        try:
            self.postgres_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = [row[0] for row in self.postgres_cursor.fetchall()]
            self.table_selector.addItems(tables)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las tablas: {e}")

    def load_table_data(self, table_name):
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
        table_name = self.table_selector.currentText()
        if not table_name:
            QMessageBox.warning(self, "Error", "No hay ninguna tabla seleccionada.")
            return

        dialog = AddRecordDialog(self, table_name, self.postgres_conn, self.postgres_cursor)
        if dialog.exec():
            self.load_table_data(table_name)

    def edit_record(self):
        table_name = self.table_selector.currentText()
        if not table_name:
            QMessageBox.warning(self, "Error", "No hay ninguna tabla seleccionada.")
            return

        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un registro para modificar.")
            return

        try:
            record_id = self.table.item(selected_row, 0).text()
            if not record_id:
                raise ValueError("El registro seleccionado no tiene un ID válido.")

            dialog = EditRecordDialog(self, table_name, self.postgres_conn, self.postgres_cursor, record_id)
            if dialog.exec():
                self.load_table_data(table_name)
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
            record_id = self.table.item(selected_row, 0).text()
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
                self.load_table_data(table_name)
        except Exception as e:
            self.postgres_conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el registro: {e}")

```

</details>

<details>
  <summary>db connect</summary>

  ```python
from mysqlmigratorpostgresql import MysqlMigratorPostgresql

def connect_mysql(migrator, host, port, user, password, database):
    try:
        migrator.connect_mysql(host, port, user, password, database)
        print("Conexión a MySQL exitosa.")
    except Exception as e:
        raise Exception(f"Error al conectar a MySQL: {e}")

def connect_postgresql(migrator, host, port, user, password, database):
    try:
        migrator.connect_postgresql(host, port, user, password, database)
        print("Conexión a PostgreSQL exitosa.")
    except Exception as e:
        raise Exception(f"Error al conectar a PostgreSQL: {e}")

```
</details>

<details>
<summary>migracion</summary>

  ```python
def migrate_all_tables(migrator):
    try:
        migrator.migrate_all()
        print("Migración completada con éxito.")
    except Exception as e:
        raise Exception(f"Error durante la migración: {e}")

```
</details>


---

## Contribución

Si deseas contribuir:
1. Haz un fork del proyecto.
2. Crea una nueva rama para tu funcionalidad: `git checkout -b feature/nueva_funcionalidad`.
3. Haz un pull request detallando los cambios realizados.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---
