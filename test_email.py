#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de prueba para verificar que Gmail funciona correctamente.
Intenta enviar un email de prueba para diagnosticar problemas.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración de Gmail (cambiar con tus credenciales)
GMAIL_USER = "jovannycoronado985@gmail.com"
GMAIL_PASSWORD = "jlwh ogzh dray iyww"
CORREO_DESTINO = "sucio3tres3@gmail.com"  # Tu email para recibir el test

print("=" * 70)
print("🧪 PRUEBA DE CONEXIÓN CON GMAIL")
print("=" * 70)
print()

print(f"📧 Datos de conexión:")
print(f"   Remitente: {GMAIL_USER}")
print(f"   Destinatario: {CORREO_DESTINO}")
print(f"   Servidor: smtp.gmail.com:465 (SSL)")
print()

try:
    # Paso 1: Crear mensaje
    print("1️⃣ Creando mensaje de email...")
    mensaje = MIMEMultipart('alternative')
    mensaje['From'] = GMAIL_USER
    mensaje['To'] = CORREO_DESTINO
    mensaje['Subject'] = 'Prueba de Ticket 313 - Email Test'

    cuerpo = """
    <html>
        <body style="font-family: Arial; background-color: #fafafa;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px;">
                <h2>✅ Prueba de Email Exitosa</h2>
                <p>Si recibes este email, significa que la configuración de Gmail es correcta.</p>
                <p><strong>¡Tu sistema está listo para enviar tickets!</strong></p>
                <hr>
                <p style="color: #999; font-size: 12px;">
                    Ticket 313 - Test Email<br>
                    Si no recibiste este email, algo falló en la autenticación.
                </p>
            </div>
        </body>
    </html>
    """

    parte_html = MIMEText(cuerpo, 'html', 'utf-8')
    mensaje.attach(parte_html)
    print("   ✓ Mensaje creado\n")

    # Paso 2: Conectar a Gmail
    print("2️⃣ Conectando a servidor SMTP...")
    servidor = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    print("   ✓ Conectado a smtp.gmail.com:465\n")

    # Paso 3: Autenticarse
    print("3️⃣ Autenticando con Gmail...")
    servidor.login(GMAIL_USER, GMAIL_PASSWORD)
    print(f"   ✓ Autenticación exitosa para {GMAIL_USER}\n")

    # Paso 4: Enviar email
    print("4️⃣ Enviando email...")
    servidor.send_message(mensaje)
    print(f"   ✓ Email enviado a {CORREO_DESTINO}\n")

    # Paso 5: Cerrar conexión
    print("5️⃣ Cerrando conexión...")
    servidor.quit()
    print("   ✓ Conexión cerrada\n")

    print("=" * 70)
    print("✅ PRUEBA EXITOSA")
    print("=" * 70)
    print()
    print("📧 El email debería llegar en los próximos minutos a:")
    print(f"   {CORREO_DESTINO}")
    print()
    print("Si NO recibes el email:")
    print("  1. Revisa carpeta de SPAM")
    print("  2. Verifica que la contraseña de aplicación sea correcta")
    print("  3. Asegúrate de haber habilitado 2FA en Google")
    print("  4. Intenta generar una nueva contraseña de aplicación")
    print()

except smtplib.SMTPAuthenticationError as e:
    print("\n" + "=" * 70)
    print("❌ ERROR DE AUTENTICACIÓN")
    print("=" * 70)
    print(f"\nProblema: {e}\n")
    print("⚠️  SOLUCIONES:")
    print("  1. Verifica que el email sea correcto: jovannycoronado985@gmail.com")
    print("  2. Verifica la contraseña de aplicación (sin espacios extras)")
    print("  3. Ve a https://myaccount.google.com/apppasswords")
    print("  4. Genera una NUEVA contraseña de aplicación")
    print("  5. Copia exactamente la contraseña (sin espacios)")
    print("  6. Actualiza GMAIL_PASSWORD en email_service.py")
    print()

except smtplib.SMTPException as e:
    print("\n" + "=" * 70)
    print("❌ ERROR SMTP")
    print("=" * 70)
    print(f"\nProblema: {e}\n")
    print("⚠️  SOLUCIONES:")
    print("  1. Verifica tu conexión a internet")
    print("  2. Intenta acceder a Gmail en el navegador")
    print("  3. Verifica que el firewall no bloquee puerto 465")
    print()

except Exception as e:
    print("\n" + "=" * 70)
    print("❌ ERROR DESCONOCIDO")
    print("=" * 70)
    print(f"\nTipo: {type(e).__name__}")
    print(f"Mensaje: {e}\n")
    import traceback
    print("Traceback completo:")
    print(traceback.format_exc())
    print()
