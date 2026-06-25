import sqlite3
from pathlib import Path

# Definir la ruta del archivo de base de datos
ruta_db = Path(__file__).parent / 'tickets.db'

# Función para crear la conexión a la base de datos
def obtener_conexion():
    """Establece y retorna una conexión a la base de datos SQLite."""
    conexion = sqlite3.connect(str(ruta_db))
    # Retornar la conexión establecida
    return conexion

# Función para inicializar la base de datos con las tablas
def inicializar_db():
    """Crea las tablas necesarias si no existen en la base de datos."""

    # Obtener conexión a la base de datos
    conexion = obtener_conexion()

    # Crear objeto cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # Crear tabla de eventos si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha TEXT NOT NULL,
            precio REAL NOT NULL,
            capacidad INTEGER NOT NULL,
            imagen_url TEXT DEFAULT NULL
        )
    ''')

    # Verificar si la columna 'imagen_url' existe en la tabla eventos
    # Esto es necesario para migrar bases de datos existentes
    cursor.execute("PRAGMA table_info(eventos)")
    columnas_eventos = cursor.fetchall()

    # Extraer nombres de columnas de la tabla eventos
    nombres_columnas_eventos = [columna[1] for columna in columnas_eventos]

    # Si la columna 'imagen_url' no existe, agregarla
    if 'imagen_url' not in nombres_columnas_eventos:
        print("⚠️  Agregando columna 'imagen_url' a tabla eventos...")
        try:
            # Usar ALTER TABLE para agregar la columna sin perder datos
            cursor.execute('''
                ALTER TABLE eventos
                ADD COLUMN imagen_url TEXT DEFAULT NULL
            ''')
            # Confirmar la alteración
            conexion.commit()
            print("✓ Columna 'imagen_url' agregada exitosamente")
        except Exception as e:
            # Mostrar error si algo falla
            print(f"Error al agregar columna 'imagen_url': {e}")

    # Crear tabla de usuarios si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            nombre TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'asistente',
            fecha_registro TEXT NOT NULL
        )
    ''')

    # Verificar si la columna 'rol' existe en la tabla usuarios
    # Esto es necesario para migrar bases de datos existentes que no tienen esta columna
    cursor.execute("PRAGMA table_info(usuarios)")
    columnas = cursor.fetchall()

    # Extraer los nombres de las columnas existentes
    nombres_columnas = [columna[1] for columna in columnas]

    # Si la columna 'rol' no existe, agregarla a la tabla
    if 'rol' not in nombres_columnas:
        print("⚠️  Agregando columna 'rol' a tabla usuarios...")
        try:
            # Ejecutar ALTER TABLE para agregar la columna 'rol'
            # El valor por defecto será 'asistente' para todos los registros existentes
            cursor.execute('''
                ALTER TABLE usuarios
                ADD COLUMN rol TEXT NOT NULL DEFAULT 'asistente'
            ''')
            # Confirmar la alteración de la tabla
            conexion.commit()
            print("✓ Columna 'rol' agregada exitosamente")
        except Exception as e:
            # Mostrar error si algo falla durante la migración
            print(f"Error al agregar columna 'rol': {e}")

    # Crear tabla de tickets si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            evento_id INTEGER NOT NULL,
            nombre_comprador TEXT NOT NULL,
            email TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (evento_id) REFERENCES eventos(id)
        )
    ''')

    # Verificar si la columna 'usuario_id' existe en la tabla tickets
    # Esto es necesario para migrar bases de datos existentes que no tienen esta columna
    cursor.execute("PRAGMA table_info(tickets)")
    columnas_tickets = cursor.fetchall()

    # Extraer nombres de columnas de la tabla tickets
    nombres_columnas_tickets = [columna[1] for columna in columnas_tickets]

    # Si la columna 'usuario_id' no existe en tickets, agregarla
    if 'usuario_id' not in nombres_columnas_tickets:
        print("⚠️  Agregando columna 'usuario_id' a tabla tickets...")
        try:
            # Usar ALTER TABLE para agregar la columna sin perder datos existentes
            # El valor por defecto será 1 para registros existentes (puede ajustarse)
            cursor.execute('''
                ALTER TABLE tickets
                ADD COLUMN usuario_id INTEGER DEFAULT 1
            ''')
            # Confirmar la alteración
            conexion.commit()
            print("✓ Columna 'usuario_id' agregada exitosamente")
        except Exception as e:
            # Mostrar error si algo falla
            print(f"Error al agregar columna 'usuario_id': {e}")

    # Si la columna 'usado' no existe en tickets, agregarla
    if 'usado' not in nombres_columnas_tickets:
        print("⚠️  Agregando columna 'usado' a tabla tickets...")
        try:
            # Usar ALTER TABLE para agregar la columna de estado
            # El valor por defecto será 0 (no usado) para registros existentes
            cursor.execute('''
                ALTER TABLE tickets
                ADD COLUMN usado INTEGER DEFAULT 0
            ''')
            # Confirmar la alteración
            conexion.commit()
            print("✓ Columna 'usado' agregada exitosamente")
        except Exception as e:
            # Mostrar error si algo falla
            print(f"Error al agregar columna 'usado': {e}")

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión
    conexion.close()

    # Mostrar mensaje de confirmación
    print("Base de datos inicializada correctamente.")

# Ejecutar la inicialización si este archivo se corre directamente
if __name__ == '__main__':
    inicializar_db()
