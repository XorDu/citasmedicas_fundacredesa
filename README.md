# Sistema de Gestión Médica - Fundacredesa

Sistema integral desarrollado con Python (Flask), SQLite y Vanilla HTML/CSS/JS con diseño Glassmorphism.

## Características
- Gestión de roles (Superadmin y Especialidades)
- Agenda global con códigos de colores por especialidad
- Historias clínicas completas (Anamnesis, Examen Físico, Hábitos, Diagnóstico)
- Generación de reportes PDF de historias médicas (vía ReportLab)
- Control de contraseñas por Superadmin

## Instalación
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Inicializar DB: `python seed.py`
4. Correr servidor: `python run.py`
