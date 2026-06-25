# Ticket 313

A modern and elegant web platform for buying and managing event tickets. Built with Python, Flask, and SQLite.

**[Live Demo](https://ticket313.pythonanywhere.com)** | **[Spanish Version](#versión-en-español)**

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [System Requirements](#system-requirements)
- [License](#license)

---

## Overview

Ticket 313 is a comprehensive event ticket management system designed for modern event organizers and attendees. The platform allows producers to create and manage events, generate unique QR codes for validation, and provides attendees with an easy way to purchase tickets and maintain their purchase history.

With built-in email notifications, PDF ticket generation, and a professional producer dashboard with analytics, Ticket 313 offers everything needed to run successful events.

---

## Features

### Role-Based Access Control

- **Producer Role**
  - Create, edit, and manage events
  - Upload event posters (JPG, PNG, GIF, WebP)
  - Access to advanced analytics dashboard
  - Real-time sales tracking and revenue reports
  - Ticket validation through QR code scanning
  - Monthly and annual sales analysis

- **Attendee Role**
  - Browse available events
  - Purchase event tickets
  - Automatic ticket delivery via email
  - View complete purchase history
  - Download tickets with unique QR codes

### Ticket Management

- **Purchase Flow**
  - Simple and intuitive ticket purchase process
  - Automatic email confirmation after purchase
  - Professional PDF ticket generation
  - Unique QR code per ticket for validation

- **QR Code System**
  - Automatic QR generation for every ticket
  - Embedded in PDF tickets sent via email
  - Real-time validation by producers
  - QR scanning capability at events

### Producer Dashboard

- **Sales Analytics**
  - Total revenue overview
  - Per-event sales statistics
  - Monthly sales breakdown
  - Annual historical trends
  - Capacity utilization metrics

- **Ticket Management**
  - Complete list of sold tickets
  - Filtering and search capabilities
  - Real-time validation records
  - Export functionality (CSV, PDF)

### Attendee Features

- **My Tickets Page**
  - Complete purchase history
  - Event details and dates
  - Quantity and pricing information
  - Total spending summary
  - Easy access to ticket information

- **Email Integration**
  - Automatic confirmation emails
  - PDF tickets with embedded QR codes
  - Professional email templates
  - Immediate delivery upon purchase

### Image Management

- **Event Posters**
  - Mandatory poster upload for each event
  - Supported formats: JPG, PNG, GIF, WebP
  - Maximum file size: 50MB
  - Automatic filename sanitization
  - Secure file storage in `static/uploads/`

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.x** | Backend language |
| **Flask** | Web framework |
| **SQLite** | Database |
| **qrcode** | QR code generation |
| **reportlab** | PDF creation |
| **Pillow (PIL)** | Image processing |
| **smtplib** | Email delivery |
| **HTML5/CSS3/JavaScript** | Frontend |

---

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Gmail account with 2-factor authentication enabled (for email functionality)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ticket-313
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Email (Optional)

To enable automatic email notifications with PDF tickets:

1. Copy the configuration template:
   ```bash
   cp email_config_example.py email_config.py
   ```

2. Set up Google App Password:
   - Go to [myaccount.google.com](https://myaccount.google.com/)
   - Navigate to Security > App passwords
   - Select "Mail" and "Windows/Linux"
   - Generate and copy the app password

3. Update `email_config.py`:
   ```python
   GMAIL_EMAIL = "your-email@gmail.com"
   GMAIL_PASSWORD = "your-app-password"
   ```

### Step 5: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

---

## Usage

### For Producers

1. **Register** with the "Producer" role
2. **Create Events** by uploading:
   - Event name and description
   - Date and location
   - Ticket price
   - Event poster image
3. **Monitor Sales** through the Producer Dashboard
4. **Validate Tickets** by scanning QR codes at events

### For Attendees

1. **Register** with the "Attendee" role
2. **Browse Events** on the home page
3. **Purchase Tickets** by selecting quantity and confirming
4. **Receive Confirmation** via email with PDF ticket
5. **View History** in "My Tickets" section

---

## Project Structure

```
ticket-313/
├── app.py                      # Main Flask application
├── database.py                 # Database initialization and management
├── email_service.py            # Email, QR, and PDF generation
├── email_config_example.py     # Email configuration template
├── requirements.txt            # Python dependencies
├── static/
│   ├── css/
│   │   └── styles.css         # Main stylesheet
│   ├── js/
│   │   └── script.js          # Frontend logic
│   ├── images/                # Application images
│   └── uploads/               # Event poster storage
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── eventos.html           # Events listing
│   ├── detalle_evento.html    # Event details
│   ├── crear_evento.html      # Create event (producers)
│   ├── mis_tickets.html       # Purchase history (attendees)
│   └── panel_productor.html   # Analytics dashboard (producers)
└── README.md                   # This file
```

---

## System Requirements

- **Storage**: Minimum 100MB for application and uploads
- **Memory**: 512MB RAM recommended
- **Database**: SQLite (included with Python)
- **Email**: Gmail account with app password (for email features)
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

---

## Security Features

- Secure file upload validation
- Filename sanitization using `secure_filename()`
- Session-based authentication
- Password hashing for user accounts
- Protected routes based on user roles
- File size limits (5MB max for uploads)
- MIME type validation for images

---

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Events
- `GET /` - Home page with event listing
- `GET /evento/<id>` - Event details
- `POST /comprar-ticket` - Purchase ticket

### Producer Features
- `GET /crear-evento` - Create event form
- `POST /crear-evento` - Submit new event
- `GET /panel-productor` - Analytics dashboard

### Attendee Features
- `GET /mis-tickets` - Purchase history
- `POST /validar-qr` - QR code validation

---

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

## License

This project is open source and available under the MIT License.

---

## Support

For issues, questions, or suggestions, please open an issue in the repository or contact the development team.

---

---

# Ticket 313

Una plataforma moderna y elegante para comprar y gestionar entradas a eventos. Construida con Python, Flask y SQLite.

**[Demo en Vivo](https://ticket313.pythonanywhere.com)** | **[English Version](#table-of-contents)**

---

## Tabla de Contenidos

- [Descripción](#descripción)
- [Funcionalidades](#funcionalidades)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Licencia](#licencia)

---

## Descripción

Ticket 313 es un sistema integral de gestión de entradas para eventos diseñado para organizadores de eventos y asistentes modernos. La plataforma permite a los productores crear y gestionar eventos, generar códigos QR únicos para validación, y proporciona a los asistentes una forma fácil de comprar entradas y mantener un historial de sus compras.

Con notificaciones por correo electrónico integradas, generación de PDF de entradas y un panel de productor profesional con análisis, Ticket 313 ofrece todo lo necesario para ejecutar eventos exitosos.

---

## Funcionalidades

### Control de Acceso por Roles

- **Rol Productor**
  - Crear, editar y gestionar eventos
  - Subir afiches de eventos (JPG, PNG, GIF, WebP)
  - Acceso a panel de análisis avanzado
  - Seguimiento de ventas en tiempo real e informes de ingresos
  - Validación de entradas mediante escaneo de códigos QR
  - Análisis de ventas mensuales y anuales

- **Rol Asistente**
  - Explorar eventos disponibles
  - Comprar entradas para eventos
  - Entrega automática de entradas por correo electrónico
  - Ver historial completo de compras
  - Descargar entradas con códigos QR únicos

### Gestión de Entradas

- **Flujo de Compra**
  - Proceso de compra simple e intuitivo
  - Confirmación automática por correo electrónico después de la compra
  - Generación de PDF profesional de entradas
  - Código QR único por entrada para validación

- **Sistema de Códigos QR**
  - Generación automática de QR para cada entrada
  - Incrustado en PDF enviados por correo electrónico
  - Validación en tiempo real por productores
  - Capacidad de escaneo de QR en eventos

### Panel del Productor

- **Análisis de Ventas**
  - Vista general de ingresos totales
  - Estadísticas de ventas por evento
  - Desglose de ventas mensuales
  - Tendencias históricas anuales
  - Métricas de utilización de capacidad

- **Gestión de Entradas**
  - Lista completa de entradas vendidas
  - Capacidad de filtrado y búsqueda
  - Registros de validación en tiempo real
  - Funcionalidad de exportación (CSV, PDF)

### Funcionalidades del Asistente

- **Página Mis Entradas**
  - Historial completo de compras
  - Detalles y fechas de eventos
  - Información de cantidad y precios
  - Resumen de gastos totales
  - Acceso fácil a información de entradas

- **Integración de Correo Electrónico**
  - Correos de confirmación automáticos
  - Entradas en PDF con códigos QR incrustados
  - Plantillas profesionales de correo electrónico
  - Entrega inmediata después de la compra

### Gestión de Imágenes

- **Afiches de Eventos**
  - Subida obligatoria de afiche para cada evento
  - Formatos soportados: JPG, PNG, GIF, WebP
  - Tamaño máximo de archivo: 50MB
  - Sanitización automática de nombres de archivo
  - Almacenamiento seguro en `static/uploads/`

---

## Tecnologías

| Tecnología | Propósito |
|-----------|-----------|
| **Python 3.x** | Lenguaje de programación backend |
| **Flask** | Framework web |
| **SQLite** | Base de datos relacional |
| **qrcode** | Generación de códigos QR |
| **reportlab** | Creación de PDF |
| **Pillow (PIL)** | Procesamiento de imágenes |
| **smtplib** | Envío de correos electrónicos |
| **HTML5/CSS3/JavaScript** | Frontend |

---

## Instalación

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Gmail con autenticación de dos factores habilitada (para funcionalidad de correo)

### Paso 1: Clonar el Repositorio

```bash
git clone <url-repositorio>
cd ticket-313
```

### Paso 2: Crear Entorno Virtual (Opcional pero Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Correo Electrónico (Opcional)

Para habilitar notificaciones automáticas por correo con entradas en PDF:

1. Copiar la plantilla de configuración:
   ```bash
   cp email_config_example.py email_config.py
   ```

2. Configurar contraseña de aplicación de Google:
   - Ir a [myaccount.google.com](https://myaccount.google.com/)
   - Navegar a Seguridad > Contraseñas de aplicaciones
   - Seleccionar "Correo" y "Windows/Linux"
   - Generar y copiar la contraseña de aplicación

3. Actualizar `email_config.py`:
   ```python
   GMAIL_EMAIL = "tu-email@gmail.com"
   GMAIL_PASSWORD = "tu-contraseña-de-aplicacion"
   ```

### Paso 5: Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

---

## Uso

### Para Productores

1. **Registrarse** con el rol de "Productor"
2. **Crear Eventos** cargando:
   - Nombre y descripción del evento
   - Fecha y ubicación
   - Precio de la entrada
   - Imagen del afiche del evento
3. **Monitorear Ventas** a través del Panel del Productor
4. **Validar Entradas** escaneando códigos QR en eventos

### Para Asistentes

1. **Registrarse** con el rol de "Asistente"
2. **Explorar Eventos** en la página de inicio
3. **Comprar Entradas** seleccionando cantidad y confirmando
4. **Recibir Confirmación** por correo electrónico con entrada en PDF
5. **Ver Historial** en la sección "Mis Entradas"

---

## Estructura del Proyecto

```
ticket-313/
├── app.py                      # Aplicación principal de Flask
├── database.py                 # Inicialización y gestión de base de datos
├── email_service.py            # Generación de correo, QR y PDF
├── email_config_example.py     # Plantilla de configuración de correo
├── requirements.txt            # Dependencias de Python
├── static/
│   ├── css/
│   │   └── styles.css         # Hoja de estilos principal
│   ├── js/
│   │   └── script.js          # Lógica del frontend
│   ├── images/                # Imágenes de la aplicación
│   └── uploads/               # Almacenamiento de afiches de eventos
├── templates/
│   ├── base.html              # Plantilla base
│   ├── index.html             # Página de inicio
│   ├── login.html             # Página de inicio de sesión
│   ├── register.html          # Página de registro
│   ├── eventos.html           # Listado de eventos
│   ├── detalle_evento.html    # Detalles del evento
│   ├── crear_evento.html      # Crear evento (productores)
│   ├── mis_tickets.html       # Historial de compras (asistentes)
│   └── panel_productor.html   # Panel de análisis (productores)
└── README.md                   # Este archivo
```

---

## Requisitos del Sistema

- **Almacenamiento**: Mínimo 100MB para aplicación y descargas
- **Memoria**: 512MB RAM recomendado
- **Base de Datos**: SQLite (incluida con Python)
- **Correo Electrónico**: Cuenta de Gmail con contraseña de aplicación (para funciones de correo)
- **Navegador**: Navegador moderno (Chrome, Firefox, Safari, Edge)

---

## Características de Seguridad

- Validación segura de carga de archivos
- Sanitización de nombres de archivo usando `secure_filename()`
- Autenticación basada en sesiones
- Cifrado de contraseñas de usuario
- Rutas protegidas según roles de usuario
- Límites de tamaño de archivo (5MB máximo para descargas)
- Validación de tipo MIME para imágenes

---

## Puntos Finales de API

### Autenticación
- `POST /register` - Registro de usuario
- `POST /login` - Inicio de sesión
- `GET /logout` - Cierre de sesión

### Eventos
- `GET /` - Página de inicio con listado de eventos
- `GET /evento/<id>` - Detalles del evento
- `POST /comprar-ticket` - Comprar entrada

### Funcionalidades del Productor
- `GET /crear-evento` - Formulario crear evento
- `POST /crear-evento` - Enviar nuevo evento
- `GET /panel-productor` - Panel de análisis

### Funcionalidades del Asistente
- `GET /mis-tickets` - Historial de compras
- `POST /validar-qr` - Validación de código QR

---

## Contribuciones

Las contribuciones son bienvenidas. Por favor, siéntete libre de enviar problemas y solicitudes de extracción.

---

## Licencia

Este proyecto es código abierto y está disponible bajo la Licencia MIT.

---

## Soporte

Para problemas, preguntas o sugerencias, por favor abre un problema en el repositorio o contacta al equipo de desarrollo.

---
