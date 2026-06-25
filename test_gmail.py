#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuracion de Gmail
GMAIL_USER = "jovannycoronado985@gmail.com"
GMAIL_PASSWORD = "jlwh ogzh dray iyww"
CORREO_DESTINO = "sucio3tres3@gmail.com"

print("=" * 70)
print("[TEST] PRUEBA DE CONEXION CON GMAIL")
print("=" * 70)
print()
print("[INFO] Remitente: " + GMAIL_USER)
print("[INFO] Destinatario: " + CORREO_DESTINO)
print()

try:
    print("[PASO 1] Creando mensaje...")
    mensaje = MIMEMultipart('alternative')
    mensaje['From'] = GMAIL_USER
    mensaje['To'] = CORREO_DESTINO
    mensaje['Subject'] = 'Prueba Ticket 313'

    cuerpo = "<html><body><h2>Prueba exitosa</h2><p>Gmail funciona correctamente.</p></body></html>"
    parte_html = MIMEText(cuerpo, 'html', 'utf-8')
    mensaje.attach(parte_html)
    print("            OK\n")

    print("[PASO 2] Conectando a smtp.gmail.com:465...")
    servidor = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    print("            OK\n")

    print("[PASO 3] Autenticando...")
    servidor.login(GMAIL_USER, GMAIL_PASSWORD)
    print("            OK\n")

    print("[PASO 4] Enviando email...")
    servidor.send_message(mensaje)
    print("            OK\n")

    print("[PASO 5] Cerrando conexion...")
    servidor.quit()
    print("            OK\n")

    print("=" * 70)
    print("[EXITO] EMAIL ENVIADO CORRECTAMENTE")
    print("=" * 70)
    print()
    print("Revisa tu bandeja en: " + CORREO_DESTINO)
    print()

except smtplib.SMTPAuthenticationError as e:
    print("\n" + "=" * 70)
    print("[ERROR] FALLO LA AUTENTICACION")
    print("=" * 70)
    print("\nProblema: " + str(e))
    print("\nSOLUCION:")
    print("1. Genera una NUEVA contraseña de aplicacion en:")
    print("   https://myaccount.google.com/apppasswords")
    print("2. Copia exactamente la contraseña (sin espacios)")
    print("3. Reemplaza en email_service.py:")
    print("   GMAIL_PASSWORD = 'la_nueva_contraseña'")
    print()

except Exception as e:
    print("\n" + "=" * 70)
    print("[ERROR] " + type(e).__name__)
    print("=" * 70)
    print("\nMensaje: " + str(e))
    print()
    import traceback
    print(traceback.format_exc())
