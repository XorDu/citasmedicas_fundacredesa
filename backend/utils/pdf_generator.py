import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

def generate_medical_history_pdf(history, filepath):
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='SectionHeader', parent=styles['Heading2'], fontSize=12, spaceAfter=6, textColor=colors.HexColor('#d35400')))
    styles.add(ParagraphStyle(name='NormalText', parent=styles['Normal'], fontSize=10, spaceAfter=4))
    
    elements = []

    # Try to load the logo if exists
    logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        img = Image(logo_path, width=2*inch, height=1.5*inch)
        img.hAlign = 'CENTER'
        elements.append(img)
        elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>HISTORIA MÉDICA</b>", styles['Heading1']))
    elements.append(Spacer(1, 12))

    # Basic Info Table
    data = [
        ["Relación laboral:", history.relacion_laboral or "", "N° cédula:", history.patient.cedula or ""],
        ["Nombre del paciente:", history.patient.first_name, "Apellidos:", history.patient.last_name],
        ["Edad:", str((datetime.today().date() - history.patient.birth_date).days // 365), "Sexo:", history.patient.gender or ""],
        ["Fecha de nacimiento:", history.patient.birth_date.strftime('%d/%m/%Y'), "Estado civil:", history.estado_civil or ""],
        ["Ocupación:", history.ocupacion or "", "Nacionalidad:", history.nacionalidad or ""],
        ["Tipo de sangre:", history.tipo_sangre or "", "Teléfono:", history.patient.phone or ""],
        ["Correo electrónico:", history.observaciones or ""] # Using observaciones slot roughly
    ]
    
    t = Table(data, colWidths=[1.5*inch, 2*inch, 1*inch, 2*inch])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ('BACKGROUND', (2,0), (2,-1), colors.lightgrey),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTSIZE', (0,0), (-1,-1), 9)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    # Text fields
    sections = [
        ("Motivo de consulta:", history.motivo_consulta),
        ("Enfermedad actual:", history.enfermedad_actual),
        ("Antecedentes personales:", history.antecedentes_personales),
        ("Enfermedades de la infancia:", history.enfermedades_infancia),
        ("Antecedentes familiares:", history.antecedentes_familiares),
        ("Cirugías y hospitalizaciones:", history.cirugias_hospitalizaciones),
        ("Diagnóstico:", history.diagnostico),
        ("Exámenes complementarios:", history.examenes_complementarios),
        ("Tratamiento:", history.tratamiento)
    ]

    for title, text in sections:
        elements.append(Paragraph(f"<b>{title}</b>", styles['SectionHeader']))
        elements.append(Paragraph(text or "____________________________________________________________________", styles['NormalText']))
        elements.append(Spacer(1, 8))

    doc.build(elements)
    return filepath
