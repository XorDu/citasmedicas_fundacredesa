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
    styles.add(ParagraphStyle(name='BoldText', parent=styles['Normal'], fontSize=10, spaceAfter=4, fontName='Helvetica-Bold'))
    
    elements = []

    logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        img = Image(logo_path, width=2*inch, height=1.5*inch)
        img.hAlign = 'CENTER'
        elements.append(img)
        elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>HISTORIA MÉDICA</b>", styles['Heading1']))
    elements.append(Spacer(1, 12))

    age = str((datetime.today().date() - history.patient.birth_date).days // 365) if history.patient.birth_date else ""

    data = [
        ["Relación laboral:", history.relacion_laboral or "", "N° cédula:", history.patient.cedula or ""],
        ["Nombre del paciente:", history.patient.first_name, "Apellidos:", history.patient.last_name],
        ["Edad:", age, "Sexo:", history.patient.gender or ""],
        ["Fecha de nacimiento:", history.patient.birth_date.strftime('%d/%m/%Y') if history.patient.birth_date else "", "Estado civil:", history.estado_civil or ""],
        ["Ocupación:", history.ocupacion or "", "Nacionalidad:", history.nacionalidad or ""],
        ["Tipo de sangre:", history.tipo_sangre or "", "Teléfono:", history.patient.phone or ""],
        ["Correo electrónico:", history.patient.email or "", "", ""]
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
    
    if history.observaciones:
        elements.append(Paragraph(f"<b>Observaciones:</b> {history.observaciones}", styles['NormalText']))
        elements.append(Spacer(1, 10))

    # Text fields basic
    elements.append(Paragraph("<b>Motivo de consulta:</b>", styles['SectionHeader']))
    elements.append(Paragraph(history.motivo_consulta or "____________________", styles['NormalText']))
    elements.append(Spacer(1, 8))
    
    elements.append(Paragraph("<b>Enfermedad actual:</b>", styles['SectionHeader']))
    elements.append(Paragraph(history.enfermedad_actual or "____________________", styles['NormalText']))
    elements.append(Spacer(1, 8))
    
    elements.append(Paragraph("<b>Antecedentes personales:</b>", styles['SectionHeader']))
    elements.append(Paragraph(history.antecedentes_personales or "____________________", styles['NormalText']))
    elements.append(Spacer(1, 8))

    # Habits Tables
    habitos_toxicos = history.habitos_toxicos or {}
    habitos_fisiologicos = history.habitos_fisiologicos or {}

    tox_data = [["Hábitos tóxicos", "Positivo", "Negativo"]]
    for h in ['Alcohol', 'Tabaco', 'Drogas', 'Infusiones', 'Actividad física']:
        val = habitos_toxicos.get(h, '')
        tox_data.append([h, "X" if val == "Positivo" else "", "X" if val == "Negativo" else ""])

    fis_data = [["Hábitos fisiológicos", "Positivo", "Negativo"]]
    for h in ['Alimentación', 'Diuresis', 'Sueño', 'Alergias', 'Otros']:
        val = habitos_fisiologicos.get(h, '')
        fis_data.append([h, "X" if val == "Positivo" else "", "X" if val == "Negativo" else ""])

    t_tox = Table(tox_data, colWidths=[2*inch, 1*inch, 1*inch])
    t_tox.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 9)
    ]))
    
    t_fis = Table(fis_data, colWidths=[2*inch, 1*inch, 1*inch])
    t_fis.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 9)
    ]))

    # We can place them side by side using a container table
    elements.append(Table([[t_tox, t_fis]], colWidths=[4*inch, 4*inch]))
    elements.append(Spacer(1, 12))

    sections = [
        ("Enfermedades de la infancia:", history.enfermedades_infancia),
        ("Antecedentes familiares:", history.antecedentes_familiares),
        ("Cirugías y hospitalizaciones:", history.cirugias_hospitalizaciones),
    ]
    for title, text in sections:
        elements.append(Paragraph(f"<b>{title}</b>", styles['SectionHeader']))
        elements.append(Paragraph(text or "__________________________________________________", styles['NormalText']))
        elements.append(Spacer(1, 8))

    # Examen Físico
    elements.append(Paragraph("<b>Examen físico:</b>", styles['SectionHeader']))
    ef = history.examen_fisico or {}
    ef_text = " | ".join([f"<b>{k}:</b> {v}" for k, v in ef.items() if v])
    if ef_text: elements.append(Paragraph(ef_text, styles['NormalText']))
    
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Impresión general:</b>", styles['BoldText']))
    ig = history.impresion_general or {}
    ig_text = " | ".join([f"<b>{k}:</b> {v}" for k, v in ig.items() if v])
    if ig_text: elements.append(Paragraph(ig_text, styles['NormalText']))
    
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Piel, faneras y tejido celular subcutáneo:</b>", styles['BoldText']))
    pf = history.piel_tejido or {}
    pf_text = " | ".join([f"<b>{k}:</b> {v}" for k, v in pf.items() if v])
    if pf_text: elements.append(Paragraph(pf_text, styles['NormalText']))

    elements.append(Spacer(1, 8))
    
    sys_sections = [
        ("Respiratorio", history.respiratorio or {}),
        ("Cardiovascular", history.cardiovascular or {}),
        ("Abdomen", history.abdomen or {}),
        ("Neurológico", history.neurologico or {})
    ]
    
    for title, dic in sys_sections:
        elements.append(Paragraph(f"<b>{title}:</b>", styles['BoldText']))
        s_text = " | ".join([f"<b>{k}:</b> {v}" for k, v in dic.items() if v])
        if s_text: elements.append(Paragraph(s_text, styles['NormalText']))
        elements.append(Spacer(1, 4))
        
    elements.append(Spacer(1, 8))
    final_sections = [
        ("Diagnóstico:", history.diagnostico),
        ("Exámenes complementarios:", history.examenes_complementarios),
        ("Tratamiento:", history.tratamiento)
    ]
    for title, text in final_sections:
        elements.append(Paragraph(f"<b>{title}</b>", styles['SectionHeader']))
        elements.append(Paragraph(text or "__________________________________________________", styles['NormalText']))
        elements.append(Spacer(1, 8))
        
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("___________________________", styles['NormalText']))
    elements.append(Paragraph(f"Firma médico: {history.doctor.full_name}", styles['NormalText']))

    doc.build(elements)
    return filepath
