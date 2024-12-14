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
