from flask import Flask, render_template, request, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Rutas para las páginas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/facultades')
def facultades():
    return render_template('facultades.html')

@app.route('/recomend')
def recomend():
    return render_template('recomend.html')

@app.route('/pedidos')
def pedidos():
    return render_template('pedidos.html')

# Configuración de la base de datos
DATABASE = 'biblioteca.db'

def conectar_bd():
    return sqlite3.connect(DATABASE)

@app.route('/', methods=['GET', 'POST'])
def formulario():
    mensaje = None  # Mensaje que se mostrará debajo del formulario
    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        libro_deseado = request.form['libro']
        fecha_retiro = request.form['fecha_retiro']
        fecha_devolucion = request.form['fecha_devolucion']

        # Conectar a la base de datos y realizar la consulta
        conn = conectar_bd()
        cursor = conn.cursor()

 # Consulta para verificar la disponibilidad del libro y obtener la universidad
        cursor.execute("""
            SELECT libros.id, libros.disponibilidad, universidades.nombre
            FROM libros
            JOIN universidades ON libros.universidad_id = universidades.id
            WHERE libros.titulo = ?
        """, (libro_deseado,))
        
        resultado = cursor.fetchone()

        if resultado:
            libro_id, disponibilidad, nombre_universidad = resultado
            if disponibilidad > 0:
                # Actualizar la cantidad disponible del libro
                cursor.execute("UPDATE libros SET disponibilidad = ? WHERE id = ?", (disponibilidad - 1, libro_id))

                # Insertar el pedido en la tabla de pedidos
                cursor.execute("""
                    INSERT INTO pedidos (nombre_cliente, cedula, libro_id, fecha_retiro, fecha_devolucion)
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, cedula, libro_id, fecha_retiro, fecha_devolucion))

                conn.commit()

                flash(f"Reserva realizada con éxito. El libro '{libro_deseado}' está disponible en la '{nombre_universidad}'", 'success')
                mensaje = f"Reserva realizada con éxito. El libro '{libro_deseado}' está disponible en la '{nombre_universidad}'"
            else:
                flash(f"El libro '{libro_deseado}' no está disponible en la '{nombre_universidad}'", 'danger')
                mensaje = f"El libro '{libro_deseado}' no está disponible en la '{nombre_universidad}'"
        else:
            flash(f"Libro '{libro_deseado}' no encontrado en la base de datos", 'danger')
            mensaje = f"Libro '{libro_deseado}' no encontrado en la base de datos"

        conn.close()

    return render_template('pedidos.html', mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)