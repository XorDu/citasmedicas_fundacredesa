# Sistema de Gestión de Citas e Historias Médicas - Fundacredesa

Este es un sistema web completo desarrollado en **Python (Flask)**, diseñado específicamente para la fundación Fundacredesa. Permite gestionar pacientes, agendar citas globales por especialidad, crear historias clínicas detalladas y exportarlas a PDF.

## 🚀 Características Principales

1. **Gestión de Pacientes:** 
   - Creación de fichas de pacientes.
   - Soporte para pacientes menores de edad asociados a un representante legal.
   - Buscador en tiempo real por número de cédula, nombres o apellidos.

2. **Historias Médicas Electrónicas:**
   - Formularios clínicos exhaustivos (Anamnesis, Hábitos, Examen Físico por sistemas).
   - **Exportación a PDF** lista para imprimir y firmar.

3. **Agenda Global:**
   - Calendario interactivo.
   - Separación visual por colores según la especialidad médica.

4. **Sistema de Roles y Seguridad:**
   - **Superadmin:** Acceso total, gestión de usuarios, edición de permisos y reseteo de contraseñas de médicos en tiempo real.
   - **Médico / Especialidad:** Acceso restringido a sus propias citas e historias.

---

## 🛠️ Tecnologías Utilizadas
- **Backend:** Python 3, Flask, SQLAlchemy (SQLite).
- **Frontend:** HTML5, CSS3 (Glassmorphism), Vanilla JavaScript, Bootstrap 5.
- **Reportes:** ReportLab (Generación de PDFs).

---

## ⚙️ Cómo ejecutar el proyecto en cualquier PC (Windows)

Dado que este proyecto está construido en Python, **no es necesario usar XAMPP** (que está orientado a PHP/MySQL). Ejecutar esto es mucho más fácil gracias al archivo `start.bat` incluido.

### Requisito previo:
Asegúrate de tener instalado **Python** en la computadora. (Puedes descargarlo de [python.org](https://www.python.org/downloads/)). Al instalarlo, asegúrate de marcar la casilla **"Add Python to PATH"**.

### Pasos para iniciar:

1. **Inicializar la Base de Datos:**
   Haz doble clic en el archivo `init_db.py` (o córrelo en consola con `python init_db.py`). 
   *Esto creará la base de datos `fundacredesa.db` y generará las especialidades, el usuario administrador y los médicos por defecto.*

2. **Arrancar el Servidor:**
   Simplemente haz doble clic en el archivo **`start.bat`**.
   *Este archivo instalará automáticamente las librerías necesarias (si no están instaladas) y arrancará el servidor web.*

3. **Acceder al Sistema:**
   Abre tu navegador web (Chrome, Edge, Firefox) y entra a la siguiente dirección:
   👉 **http://localhost:5000**

### 🔑 Credenciales por defecto:
- **SuperAdministrador:** 
  - Usuario: `admin`
  - Contraseña: `admin123`

---

## 🎨 Personalización del Logo
Para cambiar el logo que aparece en el menú lateral izquierdo:
1. Toma tu imagen del logo.
2. Nómbrala exactamente **`logo.png`**.
3. Reemplaza el archivo existente en la carpeta `frontend/static/img/logo.png`.
4. Refresca la página en tu navegador (`Ctrl + F5`).
