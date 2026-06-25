import qrcode
import smtplib
import os
import tempfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

# Configuración de Gmail - Credenciales para envío de emails
# El email se envía desde esta dirección al comprador del ticket
GMAIL_USER = "jovannycoronado985@gmail.com"
# Contraseña de aplicación de Google (NO la contraseña de Gmail normal)
# Esta contraseña se generó desde https://myaccount.google.com/apppasswords
GMAIL_PASSWORD = "jlwh ogzh dray iyww"

# Función para generar código QR único
def generar_qr_ticket(ticket_id, evento_nombre, comprador_email):
    """
    Genera un código QR único para un ticket.
    El QR contiene información del ticket para validación en el evento.
    """

    # Crear datos para el QR con información del ticket
    datos_qr = f"TICKET_ID:{ticket_id}|EVENTO:{evento_nombre}|EMAIL:{comprador_email}|FECHA:{datetime.now().strftime('%Y-%m-%d')}"

    # Crear instancia de QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Agregar datos al QR
    qr.add_data(datos_qr)
    qr.make(fit=True)

    # Crear imagen del QR
    img_qr = qr.make_image(fill_color="black", back_color="white")

    # Retornar la imagen como bytes
    return img_qr

# Función para crear PDF solo del QR ampliado
def crear_pdf_qr(ticket_id, evento_nombre, qr_image):
    """
    Crea un PDF con el código QR ampliado y legible.
    Este PDF es para imprimir o escanear fácilmente en la puerta.
    """

    # Crear buffer en memoria para el PDF
    pdf_buffer = BytesIO()

    # Crear documento PDF
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

    # Lista de elementos del PDF
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#0a0a0a'),
        spaceAfter=30,
        alignment=1  # Centro
    )

    # Título
    titulo = Paragraph("CÓDIGO QR DEL TICKET", title_style)
    elements.append(titulo)
    elements.append(Spacer(1, 0.3*inch))

    # Información del evento
    evento_info = Paragraph(
        f"<b>Evento:</b> {evento_nombre}<br/><b>Ticket ID:</b> #{ticket_id}",
        styles['Normal']
    )
    elements.append(evento_info)
    elements.append(Spacer(1, 0.4*inch))

    # Guardar QR en carpeta temporal
    carpeta_temp = tempfile.gettempdir()
    qr_path = os.path.join(carpeta_temp, f"qr_ampliado_{ticket_id}.png")
    qr_image.save(qr_path)

    # Agregar QR ampliado (más grande en esta página)
    from reportlab.platypus import Image as RLImage
    qr_img = RLImage(qr_path, width=4*inch, height=4*inch)
    elements.append(qr_img)

    elements.append(Spacer(1, 0.3*inch))

    # Instrucciones
    instrucciones = Paragraph(
        "<b>ESCANEA ESTE CÓDIGO QR EN LA ENTRADA DEL EVENTO</b><br/>"
        "Presenta este documento en la puerta.",
        styles['Normal']
    )
    elements.append(instrucciones)

    # Construir PDF
    doc.build(elements)

    # Preparar buffer para lectura
    pdf_buffer.seek(0)
    return pdf_buffer

# Función para crear PDF del ticket con QR
def crear_pdf_ticket(ticket_id, evento_nombre, evento_fecha, evento_precio, comprador_nombre, comprador_email, cantidad, qr_image):
    """
    Crea un PDF profesional con los datos del ticket y el código QR único.
    El PDF incluye:
    - Nombre del evento
    - Fecha del evento
    - Precio del ticket
    - Nombre del comprador
    - Email del comprador
    - Número único del ticket
    - Código QR para validación en la puerta

    El PDF se envía por email al comprador como adjunto.
    """

    # Crear un buffer en memoria para construir el PDF sin guardar archivo físico
    pdf_buffer = BytesIO()

    # Crear documento PDF con márgenes personalizados
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

    # Lista que contendrá todos los elementos del PDF (texto, tablas, espacios)
    elements = []

    # Obtener estilos predefinidos de reportlab
    styles = getSampleStyleSheet()
    # Crear estilo personalizado para el título del PDF
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0a0a0a'),
        spaceAfter=30,
        alignment=1  # Alinear al centro
    )

    # Agregar título principal del documento
    titulo = Paragraph("ENTRADA DE EVENTO", title_style)
    elements.append(titulo)
    # Agregar espaciador (separación visual)
    elements.append(Spacer(1, 0.2*inch))

    # Crear tabla con información del evento y ticket para mostrar en el PDF
    # Columna 1: etiqueta, Columna 2: valor
    data = [
        # Nombre del evento
        ['EVENTO:', evento_nombre],
        # Fecha en que se realizará el evento
        ['FECHA:', evento_fecha],
        # Precio individual de la entrada
        ['PRECIO POR ENTRADA:', f"${evento_precio}"],
        # Cantidad de entradas compradas en esta transacción
        ['CANTIDAD DE ENTRADAS:', str(cantidad)],
        # Cálculo del total: precio × cantidad
        ['TOTAL:', f"${float(evento_precio) * int(cantidad)}"],
        # Fila vacía para separación
        ['', ''],
        # Nombre completo de la persona que compró el ticket
        ['COMPRADOR:', comprador_nombre],
        # Email del comprador para contacto
        ['EMAIL:', comprador_email],
        # Número único del ticket para identificación
        ['NÚMERO DE TICKET:', f"#{ticket_id}"],
    ]

    # Crear tabla con los datos definidos arriba
    tabla = Table(data, colWidths=[2*inch, 4*inch])
    # Aplicar estilos a la tabla (colores, bordes, fuentes)
    tabla.setStyle(TableStyle([
        # Fondo gris para la primera columna (etiquetas)
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        # Texto en color negro
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        # Alineación a la izquierda
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # Fuente en negrita para etiquetas
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        # Tamaño de fuente
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        # Relleno debajo de celdas
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        # Bordes negros alrededor de la tabla
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Colores alternados en filas para mejor legibilidad
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))

    # Agregar la tabla al documento
    elements.append(tabla)
    # Agregar espaciador antes del QR
    elements.append(Spacer(1, 0.3*inch))

    # Crear título para la sección del código QR
    qr_title = Paragraph("CÓDIGO QR - Escanear en la entrada", styles['Heading2'])
    elements.append(qr_title)
    # Espaciador pequeño
    elements.append(Spacer(1, 0.1*inch))

    # Guardar la imagen del QR en la carpeta temporal del sistema
    # Usar tempfile.gettempdir() para obtener la carpeta temporal de Windows/Linux/Mac
    carpeta_temp = tempfile.gettempdir()
    qr_path = os.path.join(carpeta_temp, f"qr_{ticket_id}.png")
    qr_image.save(qr_path)

    # Agregar la imagen del QR al PDF
    from reportlab.platypus import Image as RLImage
    qr_img = RLImage(qr_path, width=2*inch, height=2*inch)
    elements.append(qr_img)

    # Agregar nota importante con instrucciones para el asistente
    nota = Paragraph(
        "<b>IMPORTANTE:</b> Presenta esta entrada en la entrada del evento. "
        "Se escaneará el código QR para validar tu acceso.",
        styles['Normal']
    )
    elements.append(nota)
    # Espaciador antes del pie de página
    elements.append(Spacer(1, 0.2*inch))

    # Crear pie de página con fecha de generación y marca de la plataforma
    footer = Paragraph(
        f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')} | Ticket 313",
        styles['Normal']
    )
    elements.append(footer)

    # Construir el PDF con todos los elementos agregados
    doc.build(elements)

    # Preparar el buffer para lectura (posicionar al inicio)
    pdf_buffer.seek(0)
    # Retornar el PDF como bytes para envío por email
    return pdf_buffer

# Función para enviar email con PDFs al comprador
def enviar_email_ticket(comprador_email, comprador_nombre, evento_nombre, ticket_id, pdf_ticket, pdf_qr):
    """
    Envía un email al comprador del ticket con 2 PDFs adjuntos:
    1. PDF del ticket: con datos del evento, comprador y QR pequeño
    2. PDF del QR: con código QR ampliado para imprimir y escanear fácilmente

    Se utiliza Gmail (SMTP en puerto 587 con TLS) para enviar de forma segura.
    El email se envía SOLO al comprador especificado.

    Parámetros:
    - comprador_email: Email del comprador
    - comprador_nombre: Nombre del comprador
    - evento_nombre: Nombre del evento
    - ticket_id: ID único del ticket
    - pdf_ticket: Buffer con el PDF del ticket
    - pdf_qr: Buffer con el PDF del QR ampliado
    """

    try:
        print(f"\n📧 [INICIO] Enviando email a: {comprador_email}")
        print(f"   Evento: {evento_nombre}")
        print(f"   Ticket ID: {ticket_id}")

        # Crear mensaje multipart para HTML + adjuntos
        mensaje = MIMEMultipart()
        # Remitente
        mensaje['From'] = GMAIL_USER
        # Destinatario
        mensaje['To'] = comprador_email
        # Asunto del email
        mensaje['Subject'] = f'Tu entrada para {evento_nombre} - Ticket 313'

        # Crear cuerpo del email en HTML (formato profesional)
        cuerpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #fafafa; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <!-- Encabezado con confirmación -->
                    <h2 style="color: #0a0a0a;">¡Entrada Confirmada!</h2>
                    <!-- Saludo personalizado al comprador -->
                    <p>Hola <strong>{comprador_nombre}</strong>,</p>
                    <!-- Información principal del evento -->
                    <p>Tu entrada para <strong>{evento_nombre}</strong> ha sido confirmada. Adjuntamos tu PDF con el código QR único y el afiche del evento.</p>

                    <!-- Sección con detalles del ticket -->
                    <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #333;">Detalles del Ticket</h3>
                        <!-- Número único del ticket para identificación -->
                        <p><strong>Número de Ticket:</strong> #{ticket_id}</p>
                        <!-- Email del comprador registrado -->
                        <p><strong>Email de compra:</strong> {comprador_email}</p>
                    </div>

                    <!-- Instrucciones importantes para el comprador -->
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        <strong>Instrucciones importantes:</strong><br>
                        1. Descarga el PDF adjunto a este email<br>
                        2. Presenta la entrada en la puerta del evento<br>
                        3. El código QR será escaneado para validar tu acceso<br>
                        4. Conserva esta entrada hasta después de asistir al evento
                    </p>

                    <!-- Pie de página con información de la plataforma -->
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    <p style="color: #999; font-size: 12px;">
                        Ticket 313 - Venta de Entradas<br>
                        {datetime.now().strftime('%d de %B de %Y')}
                    </p>
                </div>
            </body>
        </html>
        """

        # Adjuntar la parte HTML al mensaje
        print(f"   Agregando contenido HTML...")
        parte_html = MIMEText(cuerpo_html, 'html', 'utf-8')
        mensaje.attach(parte_html)
        print(f"   ✓ HTML agregado")

        # Adjuntar el PDF del ticket con datos y QR pequeño
        print(f"   Adjuntando PDF del ticket...")
        try:
            pdf_ticket.seek(0)
            adjunto_ticket = MIMEApplication(pdf_ticket.read(), _subtype='octet-stream')
            adjunto_ticket.add_header('Content-Disposition', 'attachment', filename=f'Entrada_Ticket_{ticket_id}.pdf')
            mensaje.attach(adjunto_ticket)
            print(f"   ✓ PDF del ticket adjuntado")
        except Exception as e:
            print(f"   ⚠️  Error al adjuntar PDF del ticket: {e}")

        # Adjuntar el PDF con QR ampliado
        print(f"   Adjuntando PDF con QR ampliado...")
        try:
            pdf_qr.seek(0)
            adjunto_qr = MIMEApplication(pdf_qr.read(), _subtype='octet-stream')
            adjunto_qr.add_header('Content-Disposition', 'attachment', filename=f'QR_Ticket_{ticket_id}.pdf')
            mensaje.attach(adjunto_qr)
            print(f"   ✓ PDF del QR adjuntado")
        except Exception as e:
            print(f"   ⚠️  Error al adjuntar PDF del QR: {e}")

        # Conectar al servidor SMTP seguro de Gmail (puerto 587 = TLS)
        # Usar puerto 587 en lugar de 465 para mejor compatibilidad
        print(f"   Conectando a servidor SMTP...")
        servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        servidor_smtp.starttls()  # Iniciar conexión TLS
        print(f"   ✓ Conectado a smtp.gmail.com:587 (TLS)")

        # Iniciar sesión con las credenciales configuradas
        print(f"   Autenticando con: {GMAIL_USER}")
        servidor_smtp.login(GMAIL_USER, GMAIL_PASSWORD)
        print(f"   ✓ Autenticación exitosa")

        # Enviar el mensaje solo al comprador especificado
        print(f"   Enviando mensaje...")
        try:
            # Usar send_message() que es el método recomendado para Python 3
            servidor_smtp.send_message(mensaje)
            print(f"   ✓ Mensaje enviado")
        except Exception as e:
            print(f"   ❌ Error al enviar: {e}")
            raise

        # Cerrar la conexión con el servidor SMTP
        try:
            servidor_smtp.quit()
        except:
            # Intentar cerrar incluso si hay error
            servidor_smtp.close()
        print(f"   ✓ Conexión cerrada")

        # Confirmación de éxito
        print(f"✅ Email enviado exitosamente a {comprador_email}\n")
        return True

    except smtplib.SMTPAuthenticationError as e:
        # Error de autenticación con Gmail
        print(f"\n❌ ERROR DE AUTENTICACIÓN: {e}")
        print(f"   Verifica que:")
        print(f"   - El email {GMAIL_USER} es correcto")
        print(f"   - La contraseña de aplicación es válida")
        print(f"   - Tienes 2FA habilitado en tu cuenta Google")
        print(f"   - La contraseña no tiene espacios extras\n")
        return False

    except smtplib.SMTPException as e:
        # Error general de SMTP
        print(f"\n❌ ERROR SMTP: {e}")
        print(f"   Verifica la conexión a internet y la configuración del servidor\n")
        return False

    except Exception as e:
        # Mostrar error completo si algo falla durante el envío
        print(f"\n❌ ERROR AL ENVIAR EMAIL: {type(e).__name__}")
        print(f"   Mensaje: {e}")
        import traceback
        print(f"   Traceback completo:")
        print(traceback.format_exc())
        print()
        return False

# Función principal que integra todo
def procesar_compra_y_enviar_ticket(ticket_id, evento_nombre, evento_fecha, evento_precio, comprador_nombre, comprador_email, cantidad, ruta_afiche=None):
    """
    Función principal que coordina la generación del QR, creación del PDF y envío del email.
    Se llama después de que se registra un nuevo ticket en la base de datos.

    Parámetros:
    - ticket_id: ID único del ticket
    - evento_nombre: Nombre del evento
    - evento_fecha: Fecha del evento
    - evento_precio: Precio del ticket
    - comprador_nombre: Nombre del comprador
    - comprador_email: Email del comprador
    - cantidad: Cantidad de tickets comprados
    - ruta_afiche: Ruta local del archivo de imagen del afiche (opcional)
    """

    try:
        print(f"\n{'='*60}")
        print(f"📝 PROCESANDO COMPRA DE TICKET")
        print(f"{'='*60}")
        print(f"  Ticket ID: {ticket_id}")
        print(f"  Comprador: {comprador_nombre}")
        print(f"  Email: {comprador_email}")
        print(f"  Evento: {evento_nombre}")
        print(f"  Cantidad: {cantidad}")
        print(f"{'='*60}\n")

        # Generar código QR único para el ticket
        print("🔲 Generando código QR...")
        qr_image = generar_qr_ticket(ticket_id, evento_nombre, comprador_email)
        print("   ✓ QR generado exitosamente\n")

        # Crear PDF con ticket, datos del evento y QR pequeño
        print("📄 Creando PDF del ticket...")
        pdf_ticket = crear_pdf_ticket(
            ticket_id,
            evento_nombre,
            evento_fecha,
            evento_precio,
            comprador_nombre,
            comprador_email,
            cantidad,
            qr_image
        )
        print("   ✓ PDF del ticket creado\n")

        # Crear PDF separado con QR ampliado
        print("📄 Creando PDF con QR ampliado...")
        pdf_qr = crear_pdf_qr(ticket_id, evento_nombre, qr_image)
        print("   ✓ PDF del QR creado\n")

        # Enviar email con 2 PDFs (sin afiche para evitar problemas)
        print("📧 Iniciando envío de email...")
        resultado = enviar_email_ticket(
            comprador_email,
            comprador_nombre,
            evento_nombre,
            ticket_id,
            pdf_ticket,
            pdf_qr
        )

        if resultado:
            print(f"\n{'='*60}")
            print(f"✅ TICKET PROCESADO Y ENVIADO EXITOSAMENTE")
            print(f"{'='*60}\n")
            return True
        else:
            print(f"\n{'='*60}")
            print(f"❌ ERROR AL ENVIAR EL TICKET")
            print(f"{'='*60}\n")
            return False

    except Exception as e:
        # Mostrar error completo con traceback
        print(f"\n{'='*60}")
        print(f"❌ ERROR EN PROCESAR_COMPRA_Y_ENVIAR_TICKET")
        print(f"{'='*60}")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {e}")
        import traceback
        print(f"\nTraceback completo:")
        print(traceback.format_exc())
        print(f"{'='*60}\n")
        return False
