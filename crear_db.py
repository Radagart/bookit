import sqlite3

# Conectarse a la base de datos (creará un archivo biblioteca.db si no existe)
conn = sqlite3.connect('biblioteca.db')

# Crear un cursor
cursor = conn.cursor()

# Crear la tabla universidades
cursor.execute('''
    CREATE TABLE IF NOT EXISTS universidades (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL
    )
''')

# Crear la tabla libros
cursor.execute('''
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        universidad_id INTEGER,
        FOREIGN KEY (universidad_id) REFERENCES universidades(id)
    )
''')

# Crear la tabla pedidos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY,
        nombre_cliente TEXT NOT NULL,
        cedula TEXT NOT NULL,
        libro_id INTEGER,
        fecha_retiro DATE NOT NULL,
        fecha_devolucion DATE NOT NULL,
        FOREIGN KEY (libro_id) REFERENCES libros(id)
    )
''')

# Agregar tres universidades de ejemplo
cursor.execute("INSERT INTO universidades (nombre) VALUES ('Universidad Comunera')")
cursor.execute("INSERT INTO universidades (nombre) VALUES ('Universidad Americana')")
cursor.execute("INSERT INTO universidades (nombre) VALUES ('Universidad Autónoma')")

# Hacer commit para guardar los cambios
conn.commit()

# Cerrar la conexión
conn.close()
