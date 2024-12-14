def migrate_all_tables(migrator):
    try:
        migrator.migrate_all()
        print("Migración completada con éxito.")
    except Exception as e:
        raise Exception(f"Error durante la migración: {e}")
