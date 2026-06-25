# CLAUDE.md

Este archivo proporciona guía a Claude Code (claude.ai/code) al trabajar con este repositorio.

## Proyecto: Ticket 313

Aplicación web para la venta y gestión de entradas a eventos construida con Flask y SQLite. Plataforma moderna y elegante para comprar y crear eventos.

### Tecnologías Utilizadas
- **Python** — Lenguaje de programación backend
- **Flask** — Framework web ligero
- **SQLite** — Base de datos relacional

## Estructura de Carpetas

- **app.py** — Punto de entrada de la aplicación Flask
- **templates/** — Plantillas HTML para renderizar páginas (Jinja2)
- **static/** — Archivos estáticos (CSS, JavaScript, imágenes)
- **requirements.txt** — Dependencias de Python

## Primeros Pasos

### Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicación
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000` (puerto por defecto de Flask).

## Desarrollo

### Agregar Páginas
1. Crear una ruta en `app.py`
2. Crear la plantilla HTML correspondiente en `templates/`
3. Hacer referencia a la plantilla en la ruta con `render_template()`

### Agregar Archivos Estáticos
Colocar archivos CSS en `static/css/`, JavaScript en `static/js/`, imágenes en `static/images/`.

## Notas de Arquitectura

Esta es una estructura monolítica de Flask. Cuando el código crezca:
- Considerar separar rutas en blueprints (app/routes/)
- Mover modelos de base de datos a un archivo separado (app/models.py)
- Extraer lógica de negocio en módulos de utilidad según sea necesario

Por ahora, mantener la lógica en `app.py` para simplificar.

## Subida Obligatoria de Imágenes ✅

- **Requisito**: Cada nuevo evento REQUIERE una imagen de afiche
- **Validación de archivo**:
  - Formatos permitidos: JPG, PNG, GIF, WebP
  - Tamaño máximo: 50MB
  - Validación en frontend y backend
- **Almacenamiento**:
  - Ruta base: `static/uploads/`
  - Nombres de archivo: `evento_TIMESTAMP_nombre.ext`
  - Sanitizados con `secure_filename()` para seguridad
- **Base de datos**: Columna `imagen_url` en tabla `eventos` guarda la ruta relativa
- **Configuración en app.py**:
  - `CARPETA_UPLOADS`: Ruta donde se guardan las imágenes
  - `app.config['MAX_CONTENT_LENGTH']`: Límite de tamaño (5MB)
  - `EXTENSIONES_PERMITIDAS`: Conjunto de extensiones válidas
  - `archivo_permitido()`: Función que valida la extensión

### Flujo de Crear Evento
1. Usuario selecciona imagen en formulario
2. Backend valida:
   - Archivo existe y no está vacío
   - Extensión es permitida
   - Tamaño no excede 5MB
3. Si es válido:
   - Guarda imagen en `static/uploads/` con nombre único
   - Guarda ruta en BD
   - Redirige a /eventos
4. Si hay error:
   - Muestra mensaje en formulario
   - Usuario puede corregir y reintentar

## Sistema de Email con QR y PDF ✅

- **Generación de QR**: Se crea un código QR único para cada ticket con información de validación
- **Creación de PDF**: Se genera un PDF profesional con datos del ticket y el QR incrustado
- **Envío de Email**: Se envía automáticamente al comprador después de la compra
- **Seguridad**: Utiliza contraseñas de aplicación de Google, no contraseñas reales
- **Librerías**: qrcode, reportlab, Pillow para QR y PDF; smtplib para email

### Configuración de Gmail

Para que funcione el envío de emails:

1. **Archivo de configuración**: Copiar `email_config_example.py` a `email_config.py`
2. **Habilitar 2FA**: En tu cuenta Google habilita autenticación de dos factores
3. **Generar contraseña de app**:
   - Ir a https://myaccount.google.com/
   - Seguridad > Contraseñas de aplicaciones
   - Seleccionar "Mail" y "Windows/Linux"
   - Copiar contraseña generada
4. **Configurar credenciales**: Actualizar `email_config_example.py` con:
   - Tu email de Gmail
   - Contraseña de aplicación (no contraseña normal)

### Archivos de Email

- `email_service.py`: Módulo que maneja QR, PDF y envío de emails
- `email_config_example.py`: Template de configuración (NO commits con credenciales)
- Función `procesar_compra_y_enviar_ticket()`: Se llama al registrar ticket

## Migraciones de Base de Datos

### ⚠️ IMPORTANTE: Usar ALTER TABLE en lugar de recrear tablas

**Principio:** Cuando necesites agregar una columna nueva a una tabla existente, SIEMPRE usa `ALTER TABLE`. NUNCA recrees la tabla ni elimines la base de datos.

**Por qué:** 
- `ALTER TABLE` preserva todos los datos existentes
- Si borras la BD, pierdes todos los registros (usuarios, eventos, tickets)
- Las migraciones deben ser no-destructivas

**Ejemplo correcto:**
```python
# ✅ CORRECTO: Agregar columna sin perder datos
cursor.execute('''
    ALTER TABLE usuarios
    ADD COLUMN nuevo_campo TEXT DEFAULT 'valor_por_defecto'
''')

# ❌ INCORRECTO: Recrear tabla (pierde todo)
cursor.execute('DROP TABLE usuarios')
cursor.execute('CREATE TABLE usuarios (...)')
```

**En database.py:**
Siempre verificar si la columna existe antes de agregarla:
```python
# Verificar si existe
cursor.execute("PRAGMA table_info(tabla_nombre)")
columnas = [col[1] for col in cursor.fetchall()]

# Agregar solo si no existe
if 'nueva_columna' not in columnas:
    cursor.execute('ALTER TABLE tabla_nombre ADD COLUMN nueva_columna TIPO')
```

**Flujo de desarrollo:**
1. Agregar columna con `ALTER TABLE` en `database.py`
2. Crear función que use la columna
3. No eliminar ni recrear base de datos
4. Los datos existentes se preservan con valores por defecto

## Convenciones de Código

### Comentarios
**Todos los comentarios del código deben ser escritos en español.** Esto aplica a:
- Comentarios inline
- Docstrings de funciones y clases
- Comentarios de bloques de código
- Notas y explicaciones

Ejemplo:
```python
# Valida que el email sea único en la base de datos
def validar_email_unico(email):
    """Verifica si el email ya está registrado."""
    pass
```

## Sistema de Autenticación ✅

- **Login** — Los usuarios pueden iniciar sesión con email y contraseña.
- **Registro** — Nuevos usuarios pueden crear una cuenta eligiendo su rol (Productor o Asistente).
- **Sesiones** — Las sesiones se mantienen activas mientras el usuario está logueado.
- **Logout** — Los usuarios pueden cerrar sesión en cualquier momento.
- **Rutas Protegidas** — Las rutas requieren autenticación según el rol del usuario.

## Restricciones de Roles ✅

- **Productores**:
  - ✓ Pueden crear eventos nuevos
  - ✓ Acceso a `/crear-evento`
  - ✓ Acceso al panel de productor (`/panel-productor`)
  - ✓ Pueden validar entradas de eventos

- **Asistentes**:
  - ✓ Pueden ver eventos
  - ✓ Pueden comprar tickets
  - ✓ Acceso a `/mis-tickets` (historial de compras)
  - ✗ NO pueden crear eventos
  - ✗ NO pueden acceder a `/crear-evento`
  - ✗ NO pueden acceder al panel del productor

- **Mensajes de Error**:
  - Si un asistente intenta acceder a rutas de productor, ve página "Acceso Denegado"
  - El botón "+ Crear Evento" solo se muestra a productores
  - El panel del productor solo accesible para productores

## Página Mis Tickets para Asistentes ✅

- **Ruta**: `/mis-tickets` (solo accesible para asistentes autenticados)
- **Información mostrada**:
  - Nombre del evento (clickeable para ver detalle)
  - Fecha del evento
  - Cantidad de tickets comprados
  - Precio unitario
  - Total pagado por esa compra
- **Resumen**: Total gastado en todas las entradas
- **Diseño**: Tabla responsiva con diseño Ticket 313
- **Protección**: Redirige a login si no está autenticado, muestra error si es productor

### Consulta SQL
```sql
SELECT e.id, e.nombre, e.fecha, e.precio, t.cantidad, t.id
FROM tickets t
JOIN eventos e ON t.evento_id = e.id
WHERE t.usuario_id = ?
ORDER BY t.id DESC
```

## Funcionalidades Futuras

- **Notificaciones por Email** — Confirmación automática de compras:
  - Al comprar un ticket, se envía email automático al comprador
  - El email incluye un código QR único en PDF adjunto
  - El QR permite validar la entrada en el evento
  - El productor puede escanear el QR desde su panel
  - Se guardan registros de emails enviados

- **Página Mis Tickets para Asistentes** — Historial de compras:
  - Nueva ruta `/mis-tickets` solo accesible para asistentes
  - Muestra todos los tickets comprados por el usuario
  - Información: evento, fecha, precio, estado (usado/no usado)
  - Opción de descargar QR de cada ticket
  - Historial completo de transacciones

- **Dashboard Mejorado del Productor** — Análisis de ventas:
  - Ruta `/panel-productor` con estadísticas avanzadas
  - **Por evento**: ventas, ingresos, tickets vendidos, capacidad utilizada
  - **Ingresos totales**: suma de todas las ventas del productor
  - **Conteo mensual**: gráfico de ventas por mes del año actual
  - **Conteo anual**: histórico de años anteriores
  - **Conteo histórico**: gráfico de tendencias a largo plazo
  - Tabla detallada de todos los tickets vendidos con filtros
  - Exportar reportes en CSV o PDF

- **Imágenes de Eventos** — Gestión de afiches para eventos:
  - Al crear un evento, es obligatorio subir una imagen de afiche.
  - Las imágenes se guardan en `static/uploads/` del servidor.
  - El afiche se muestra en la card del evento en la lista.
  - También aparece en la página de detalle del evento para mayor impacto visual.
  - Esto mejora la presentación y atracción de los eventos.

- **Sistema de Roles** — Crear dos tipos de usuarios:
  - **Productor**: Puede crear, editar y eliminar eventos propios.
  - **Asistente**: Puede ver eventos y comprar tickets.

- **Sistema de QR** — Generación y validación de códigos QR para tickets:
  - Al comprar un ticket, se genera automáticamente un código QR único.
  - El QR se envía por email al comprador junto con los detalles del evento.
  - Los Productores tendrán acceso a una página exclusiva de validación.
  - Desde esta página pueden escanear o ingresar el QR para marcar el ticket como usado.
  - Esto permite verificar la asistencia al evento en tiempo real.

- **Integración de Pagos** — Implementar integración con MercadoPago o Flow para procesar pagos de tickets. El dinero debe llegar directo a la cuenta del organizador del evento.


que todo el codigo se comente en español 