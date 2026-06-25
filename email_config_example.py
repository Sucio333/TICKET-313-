# ⚠️  CONFIGURACIÓN DE EMAIL - ARCHIVO DE EJEMPLO
# Este archivo muestra cómo configurar las credenciales de Gmail
# NUNCA commits este archivo con contraseñas reales al repositorio
# Copia este archivo a email_config.py y agrega tus credenciales

# Configuración de Gmail para enviar emails con tickets
GMAIL_CONFIG = {
    # Tu email de Gmail
    'email': 'tu_email@gmail.com',

    # Contraseña de aplicación de Google (NO la contraseña de Gmail)
    # Para obtenerla:
    # 1. Abre https://myaccount.google.com/
    # 2. Ve a "Seguridad" en el menú lateral
    # 3. Busca "Contraseñas de aplicaciones"
    # 4. Selecciona "Mail" y "Windows/Linux"
    # 5. Copia la contraseña generada (sin espacios)
    'password': 'tu_contraseña_app_generada',

    # Servidor SMTP de Gmail (no cambiar)
    'smtp_server': 'smtp.gmail.com',

    # Puerto SMTP seguro (no cambiar)
    'smtp_port': 465,
}

# Instrucciones para habilitar "Contraseñas de aplicaciones" en Google:
# 1. Asegúrate de tener 2FA habilitado en tu cuenta Google
# 2. Abre Google Account: https://myaccount.google.com/
# 3. En el menú izquierdo: Seguridad > Contraseñas de aplicaciones
# 4. Selecciona "Mail" como aplicación y "Windows/Linux" como dispositivo
# 5. Google generará una contraseña de 16 caracteres
# 6. Cópiala aquí en el campo 'password'

# IMPORTANTE:
# - No uses tu contraseña de Gmail normal, usa contraseña de aplicación
# - No commits este archivo a Git si contiene credenciales reales
# - Considera usar variables de entorno para mayor seguridad:
#   export GMAIL_USER="tu_email@gmail.com"
#   export GMAIL_PASSWORD="tu_contraseña_app"
