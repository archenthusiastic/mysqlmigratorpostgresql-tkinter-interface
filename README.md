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


<h4 align="center">Estructura</h2>

  ```cpp
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
  ```

<h4 align="center">Funciones</h2>
<details>
<summary>Validar Fecha</summary>
  
  ```cpp
bool validarFecha(int anio, int mes, int dia) {
    if(anio == 0) {
        cout << "Year value is invalid: " << anio << endl;
        return false;
    }
    if(mes < 1 || mes > 12 )
    {
        cout << "Month value is invalid: "<< mes << endl;
        return false;
    }
    if (dia < 1 || dia > 31) 
    {
        cout << "Day value is invalid: "<<dia<<endl;
        return false;
    }
    if(mes == 2) 
    {
        if(dia > 29)
        {
            cout << "Day value is invalid: "<< dia << endl;
            return false;
        }
    }
    else if(mes == 4 || mes == 6 || mes == 9 || mes == 11) 
    {
        if(dia > 30) {
            cout << "Day value is invalid: "<< dia << endl;
            return false;
        }
    }
    return true;
}
```

Basicamente mediante una funcion booleana dentro de funcionan agrego filtros en forma de sentencias que permiten detectar si una fecha no es valida es decir su formato es erroneo
</details>

<details>
<summary>Contar Guiones</summary>

  ```cpp
int contarGuiones(const string& str) {
    int count = 0;
    for (char c : str) {
        if (c == '-') {
            count++;
        }
    }
    return count;
}
```

Esta funcion me permite asegurarme que la fecha siga el formato year-moth-day
</details>

<details>
<summary>formatearFecha</summary>

  ```cpp
string formatearFecha(int anio, int mes, int dia) {
    return to_string(anio) + "-" + (mes < 10 ? "0" : "") + to_string(mes) + "-" + (dia < 10 ? "0" : "") + to_string(dia);
}
```

Esta funcion me permite agregar los 0 que faltan a la fecha
</details>

<details>
  <summary>insertarEventoEnOrden</summary>

  ```cpp
void insertarEventoEnOrden(vector<string>& eventos, const string& evento) {
    auto it = eventos.begin();
    while (it != eventos.end() && *it < evento) {
        ++it;
    }
    if(it == eventos.end() || *it != evento) {
        eventos.insert(it,evento);
    }
}
```

Con esto ordeno los eventos en orden acendente como es requerido
</details>

<details>
  <summary>imprimirFechas</summary>

  ```cpp
void imprimirFechas(const map<string, vector<string>>& fechas) {
    for (const auto& par : fechas) {
        cout << "Fecha: " << par.first << endl;
        for (const auto& evento : par.second) {
            cout << "  - " << evento << endl;
        }
        cout << "-----------------------------------" << endl;
    }
}
```

Con esta funcion muestro las fechas en consola
</details>

<details>
<summary>eliminarEvento</summary>

  ```cpp
bool eliminarEvento(vector<string>& eventos, const string& evento) {
    for (auto it = eventos.begin(); it != eventos.end(); ++it) {
        if (*it == evento) {
            eventos.erase(it);
            return true;
        }
    }
    return false;
}
```

esta funcion de tipo booleana me permite eliminar los eventos la uso para los comandos de eliminacion
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

## Contacto

Autor: [Tu Nombre]  
Correo: [tu_email@example.com]  
GitHub: [https://github.com/tu_usuario](https://github.com/tu_usuario)
