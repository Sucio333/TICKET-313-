from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
import os
from pathlib import Path
from PIL import Image

# Importar módulo de base de datos
from database import inicializar_db, obtener_conexion

# Importar módulo de email con QR y PDF
from email_service import procesar_compra_y_enviar_ticket

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Configurar clave secreta para las sesiones
app.secret_key = 'tu_clave_secreta_super_segura_aqui_123'

# Configurar directorio de subida de archivos (imágenes de eventos)
# Las imágenes se guardan en static/uploads/
CARPETA_UPLOADS = Path(__file__).parent / 'static' / 'uploads'
# Crear carpeta si no existe
CARPETA_UPLOADS.mkdir(parents=True, exist_ok=True)

# Configurar tamaño máximo de archivo: 50MB (para mayor flexibilidad)
# Esto permite subir imágenes más grandes sin problemas
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Extensiones permitidas para las imágenes
EXTENSIONES_PERMITIDAS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

# Función para verificar que la extensión sea válida
def archivo_permitido(nombre_archivo):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in nombre_archivo and nombre_archivo.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS

# Inicializar la base de datos al arrancar la aplicación
inicializar_db()

# Función decoradora para proteger rutas que requieren autenticación
def login_requerido(f):
    """Verifica si el usuario está autenticado antes de acceder a la ruta."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si hay un usuario en la sesión
        if 'usuario_id' not in session:
            # Redirigir al login si no hay sesión activa
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Ruta principal de la aplicación
@app.route('/')
def inicio():
    """Renderiza la página principal con información del usuario si está autenticado."""
    # Simplemente mostrar la página de inicio (sin requerir login)
    return render_template('index.html')

# Ruta para el registro de nuevos usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Maneja el registro de nuevos usuarios."""

    # Verificar si el formulario fue enviado (POST)
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        # Obtener el rol seleccionado en el registro (productor o asistente)
        rol = request.form.get('rol', 'asistente')

        # Obtener conexión a la base de datos
        conexion = obtener_conexion()

        # Crear cursor para ejecutar comandos SQL
        cursor = conexion.cursor()

        # Verificar si el email ya está registrado
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario_existente = cursor.fetchone()

        # Si el email ya existe, mostrar error
        if usuario_existente:
            conexion.close()
            return render_template('registro.html', error='El email ya está registrado')

        # Hashear la contraseña antes de guardarla
        contraseña_hasheada = generate_password_hash(contraseña)

        # Obtener la fecha y hora actual
        fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insertar el nuevo usuario en la tabla usuarios con su rol
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, contraseña, rol, fecha_registro)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, email, contraseña_hasheada, rol, fecha_registro))

        # Confirmar los cambios en la base de datos
        conexion.commit()

        # Cerrar la conexión
        conexion.close()

        # Redirigir al login después de registrarse
        return redirect(url_for('login'))

    # Si es GET, mostrar el formulario de registro
    return render_template('registro.html')

# Ruta para el login de usuarios
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el login de usuarios."""

    # Verificar si el formulario fue enviado (POST)
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')

        # Obtener conexión a la base de datos
        conexion = obtener_conexion()

        # Crear cursor para ejecutar comandos SQL
        cursor = conexion.cursor()

        # Buscar el usuario por email (incluyendo rol)
        cursor.execute('SELECT id, nombre, contraseña, rol FROM usuarios WHERE email = ?', (email,))

        # Obtener los datos del usuario
        usuario = cursor.fetchone()

        # Cerrar la conexión
        conexion.close()

        # Verificar si el usuario existe y la contraseña es correcta
        if usuario and check_password_hash(usuario[2], contraseña):
            # Guardar los datos del usuario en la sesión
            session['usuario_id'] = usuario[0]
            session['usuario_nombre'] = usuario[1]
            # Guardar el rol del usuario en la sesión
            session['usuario_rol'] = usuario[3]

            # Redirigir a la página principal
            return redirect(url_for('inicio'))
        else:
            # Mostrar error si las credenciales son incorrectas
            return render_template('login.html', error='Email o contraseña incorrectos')

    # Si es GET, mostrar el formulario de login
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    """Cierra la sesión del usuario actual."""

    # Limpiar los datos de la sesión
    session.clear()

    # Redirigir al login
    return redirect(url_for('login'))

# Ruta para mostrar todos los eventos (pública)
@app.route('/eventos')
def eventos():
    """Consulta todos los eventos de la base de datos y los muestra en un template."""

    # Obtener conexión a la base de datos
    conexion = obtener_conexion()

    # Crear cursor para ejecutar consultas SQL
    cursor = conexion.cursor()

    # Ejecutar consulta para obtener todos los eventos incluyendo la imagen
    # Se obtiene: id, nombre, fecha, precio, capacidad, imagen_url
    cursor.execute('SELECT id, nombre, fecha, precio, capacidad, imagen_url FROM eventos')

    # Obtener todos los resultados de la consulta
    lista_eventos = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Renderizar el template pasando la lista de eventos
    return render_template('eventos.html', eventos=lista_eventos)

# Ruta para mostrar el detalle de un evento específico (pública para ver, requiere login para comprar)
@app.route('/evento/<int:evento_id>', methods=['GET', 'POST'])
def evento_detalle(evento_id):
    """Muestra el detalle de un evento y permite comprar tickets si está autenticado."""

    # Obtener conexión a la base de datos
    conexion = obtener_conexion()

    # Crear cursor para ejecutar consultas SQL
    cursor = conexion.cursor()

    # Consultar el evento específico por su ID (incluyendo imagen del afiche)
    # Se obtiene: id, nombre, fecha, precio, capacidad, imagen_url
    cursor.execute('SELECT id, nombre, fecha, precio, capacidad, imagen_url FROM eventos WHERE id = ?', (evento_id,))

    # Obtener los datos del evento
    evento = cursor.fetchone()

    # Si el evento no existe, cerrar conexión y redirigir a eventos
    if not evento:
        conexion.close()
        return redirect(url_for('eventos'))

    # Verificar si el formulario fue enviado (POST)
    if request.method == 'POST':
        # Verificar si el usuario está autenticado para comprar
        if 'usuario_id' not in session:
            # Redirigir al login si intenta comprar sin estar autenticado
            conexion.close()
            return redirect(url_for('login'))
        # Obtener los datos del formulario de compra
        nombre_comprador = request.form.get('nombre_comprador')
        email = request.form.get('email')
        cantidad = request.form.get('cantidad')

        # Insertar el nuevo ticket en la tabla tickets (incluyendo el usuario_id)
        cursor.execute('''
            INSERT INTO tickets (usuario_id, evento_id, nombre_comprador, email, cantidad)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['usuario_id'], evento_id, nombre_comprador, email, int(cantidad)))

        # Confirmar los cambios en la base de datos
        conexion.commit()

        # Obtener el ID del ticket recién creado
        ticket_id = cursor.lastrowid

        # Cerrar la conexión
        conexion.close()

        # Preparar ruta del afiche para enviar por email
        # La imagen_url está en evento[5] (por ejemplo: /static/uploads/evento_20260624_123456.jpg)
        # Convertir a ruta local: static/uploads/evento_20260624_123456.jpg
        ruta_afiche_local = None
        if evento[5]:
            # Remover la barra inicial si existe
            ruta_relativa = evento[5].lstrip('/')
            # Construir ruta local completa
            ruta_afiche_local = Path(__file__).parent / ruta_relativa

        # Enviar email con QR, PDF y afiche al comprador
        # Llamar a la función que genera el QR, crea el PDF y envía el email con adjuntos
        procesar_compra_y_enviar_ticket(
            ticket_id=ticket_id,
            evento_nombre=evento[1],
            evento_fecha=evento[2],
            evento_precio=evento[3],
            comprador_nombre=nombre_comprador,
            comprador_email=email,
            cantidad=cantidad,
            ruta_afiche=str(ruta_afiche_local) if ruta_afiche_local else None
        )

        # Redirigir a una página de confirmación
        return redirect(url_for('evento_detalle', evento_id=evento_id, compra_exitosa=True))

    # Verificar si hay parámetro de compra exitosa en la URL
    compra_exitosa = request.args.get('compra_exitosa', False)

    # Cerrar la conexión
    conexion.close()

    # Renderizar el template pasando los datos del evento y el estado de la compra
    return render_template('evento_detalle.html', evento=evento, compra_exitosa=compra_exitosa)

# Ruta para mostrar el formulario de crear evento (solo para productores)
@app.route('/crear-evento', methods=['GET', 'POST'])
def crear_evento():
    """Maneja la creación de eventos (solo para productores)."""

    # Verificar si el usuario está autenticado
    if 'usuario_id' not in session:
        # Redirigir al login si no está autenticado
        return redirect(url_for('login'))

    # Verificar si el usuario tiene rol de productor
    if session.get('usuario_rol') != 'productor':
        # Mostrar página de acceso denegado si no es productor
        # Comentario: Los asistentes no pueden crear eventos
        return render_template('acceso_denegado.html')

    # Verificar si el formulario fue enviado (POST)
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        fecha = request.form.get('fecha')
        precio = request.form.get('precio')
        capacidad = request.form.get('capacidad')

        # Procesar la imagen del afiche (OBLIGATORIO)
        # Verificar si el archivo fue enviado
        if 'imagen' not in request.files:
            # Redirigir con error si no hay imagen
            return render_template('crear_evento.html', error='La imagen es obligatoria')

        archivo_imagen = request.files['imagen']

        # Verificar si se seleccionó un archivo
        if archivo_imagen.filename == '':
            # Redirigir con error si el archivo está vacío
            return render_template('crear_evento.html', error='Debes seleccionar una imagen')

        # Verificar que la extensión sea válida
        if not archivo_permitido(archivo_imagen.filename):
            # Redirigir con error si la extensión no es permitida
            # Los formatos permitidos están definidos en EXTENSIONES_PERMITIDAS
            return render_template('crear_evento.html', error='Formato de imagen no permitido. Usa JPG, PNG, GIF o WebP')

        try:
            # Generar un nombre seguro para el archivo
            # Usar nombre único con timestamp para evitar conflictos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Obtener extensión del archivo
            extension = archivo_imagen.filename.rsplit('.', 1)[1].lower()
            # Crear nombre único del archivo
            nombre_archivo = secure_filename(f"evento_{timestamp}_{nombre[:20].replace(' ', '_')}.{extension}")

            # Guardar la imagen en la carpeta uploads
            ruta_imagen = CARPETA_UPLOADS / nombre_archivo

            # Comprimir y redimensionar la imagen para reducir tamaño
            print(f"   Comprimiendo imagen...")
            try:
                # Abrir la imagen con PIL
                img = Image.open(archivo_imagen.stream)

                # Redimensionar si es muy grande (máximo 1200x800)
                # Esto reduce significativamente el tamaño del archivo
                img.thumbnail((1200, 800), Image.Resampling.LANCZOS)

                # Guardar con compresión (calidad 85 para JPG)
                # Esto reduce el peso sin perder mucha calidad
                if extension.lower() in ['jpg', 'jpeg']:
                    img.save(str(ruta_imagen), 'JPEG', quality=85, optimize=True)
                elif extension.lower() == 'png':
                    img.save(str(ruta_imagen), 'PNG', optimize=True)
                elif extension.lower() == 'webp':
                    img.save(str(ruta_imagen), 'WEBP', quality=85)
                else:
                    img.save(str(ruta_imagen), optimize=True)

                print(f"   ✓ Imagen comprimida y guardada")
            except Exception as e:
                print(f"   ⚠️  Error al comprimir: {e}, guardando original...")
                # Si falla la compresión, guardar original
                archivo_imagen.seek(0)
                archivo_imagen.save(str(ruta_imagen))

            # Crear ruta relativa para guardar en la BD (para servir desde static)
            ruta_imagen_bd = f"/static/uploads/{nombre_archivo}"

            # Obtener conexión a la base de datos
            conexion = obtener_conexion()

            # Crear cursor para ejecutar comandos SQL
            cursor = conexion.cursor()

            # Insertar el nuevo evento en la tabla eventos con la imagen
            cursor.execute('''
                INSERT INTO eventos (nombre, fecha, precio, capacidad, imagen_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, fecha, float(precio), int(capacidad), ruta_imagen_bd))

            # Confirmar los cambios en la base de datos
            conexion.commit()

            # Cerrar la conexión
            conexion.close()

            # Redirigir a la página de eventos después de guardar
            return redirect(url_for('eventos'))

        except Exception as e:
            # Mostrar error si algo falla al guardar la imagen
            print(f"Error al guardar imagen: {e}")
            return render_template('crear_evento.html', error=f'Error al guardar la imagen: {str(e)}')

    # Si es GET, mostrar el formulario de crear evento
    return render_template('crear_evento.html')

# Ruta para ver historial de tickets comprados (solo para asistentes)
@app.route('/mis-tickets')
def mis_tickets():
    """Muestra el historial de tickets comprados por el usuario asistente autenticado."""

    # Verificar si el usuario está autenticado
    if 'usuario_id' not in session:
        # Redirigir al login si no está autenticado
        return redirect(url_for('login'))

    # Verificar si el usuario tiene rol de asistente
    if session.get('usuario_rol') != 'asistente':
        # Mostrar página de acceso denegado si no es asistente
        # Solo asistentes pueden ver su historial de compras
        return render_template('acceso_denegado.html')

    # Obtener conexión a la base de datos
    conexion = obtener_conexion()

    # Crear cursor para ejecutar consultas SQL
    cursor = conexion.cursor()

    # Obtener todos los tickets comprados por el usuario actual
    # Se unen las tablas tickets y eventos para obtener información completa
    cursor.execute('''
        SELECT
            e.id,
            e.nombre,
            e.fecha,
            e.precio,
            t.cantidad,
            t.id as ticket_id
        FROM tickets t
        JOIN eventos e ON t.evento_id = e.id
        WHERE t.usuario_id = ?
        ORDER BY t.id DESC
    ''', (session['usuario_id'],))

    # Obtener todos los tickets del usuario
    mis_compras = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Calcular el gasto total en Python (más confiable que en Jinja2)
    # Iterar sobre cada compra y sumar el total (precio * cantidad)
    gasto_total = 0.0
    for compra in mis_compras:
        # compra[3] es el precio, compra[4] es la cantidad
        gasto_total += compra[3] * compra[4]

    # Renderizar la página con el historial de compras y el gasto total calculado
    return render_template('mis_tickets.html', compras=mis_compras, gasto_total=gasto_total)

# Ruta del panel del productor con análisis de ventas (solo para productores)
@app.route('/panel-productor')
def panel_productor():
    """Panel exclusivo para productores con análisis de ventas y datos."""

    # Verificar si el usuario está autenticado
    if 'usuario_id' not in session:
        # Redirigir al login si no está autenticado
        return redirect(url_for('login'))

    # Verificar si el usuario tiene rol de productor
    if session.get('usuario_rol') != 'productor':
        # Mostrar página de acceso denegado si no es productor
        return render_template('acceso_denegado.html')

    # Obtener conexión a la base de datos
    conexion = obtener_conexion()

    # Crear cursor para ejecutar consultas SQL
    cursor = conexion.cursor()

    # ===== ANÁLISIS POR EVENTO =====
    # Obtener ventas por evento (nombre, cantidad vendida, ingresos)
    cursor.execute('''
        SELECT
            e.id,
            e.nombre,
            e.fecha,
            e.precio,
            e.capacidad,
            COUNT(t.id) as tickets_vendidos,
            SUM(t.cantidad) as cantidad_total,
            SUM(t.cantidad * e.precio) as ingresos_totales
        FROM eventos e
        LEFT JOIN tickets t ON e.id = t.evento_id
        GROUP BY e.id
        ORDER BY ingresos_totales DESC
    ''')

    # Obtener datos de ventas por evento
    ventas_por_evento = cursor.fetchall()

    # ===== INGRESOS TOTALES =====
    # Calcular ingresos totales de todos los eventos
    cursor.execute('''
        SELECT
            SUM(t.cantidad * e.precio) as ingresos_totales
        FROM tickets t
        JOIN eventos e ON t.evento_id = e.id
    ''')

    # Obtener resultado
    resultado_ingresos = cursor.fetchone()
    ingresos_totales = resultado_ingresos[0] if resultado_ingresos[0] else 0.0

    # ===== ESTADÍSTICAS GENERALES =====
    # Obtener cantidad total de tickets vendidos
    cursor.execute('''
        SELECT
            COUNT(t.id) as cantidad_tickets,
            SUM(t.cantidad * e.precio) as ingresos_totales
        FROM tickets t
        JOIN eventos e ON t.evento_id = e.id
    ''')

    # Obtener estadísticas generales
    stats_generales = cursor.fetchone()
    cantidad_tickets_total = stats_generales[0] if stats_generales[0] else 0

    # Obtener lista de todos los tickets para historial
    cursor.execute('''
        SELECT
            t.id,
            e.nombre as evento,
            t.nombre_comprador,
            t.email,
            t.cantidad,
            e.precio,
            (t.cantidad * e.precio) as total_pagado
        FROM tickets t
        JOIN eventos e ON t.evento_id = e.id
        ORDER BY t.id DESC
    ''')

    # Obtener historial de tickets
    historial_tickets = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Renderizar el panel del productor con análisis de datos
    return render_template('panel_productor.html',
                         ventas_por_evento=ventas_por_evento,
                         ingresos_totales=ingresos_totales,
                         cantidad_tickets_total=cantidad_tickets_total,
                         historial_tickets=historial_tickets)

# Ejecutar la aplicación si se corre este archivo directamente
if __name__ == '__main__':
    app.run(debug=True)
