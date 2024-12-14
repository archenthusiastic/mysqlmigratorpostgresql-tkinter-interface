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
