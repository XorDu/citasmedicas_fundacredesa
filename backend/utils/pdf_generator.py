import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime


def safe(value, default=""):
    """Safely return a string value, avoiding None."""
    if value is None:
        return default
    return str(value)


def safe_date(date_obj, fmt='%d/%m/%Y'):
    """Safely format a date object."""
    if date_obj is None:
        return ""
    try:
        return date_obj.strftime(fmt)
    except Exception:
        return ""


def safe_dict(value):
    """Safely return a dict, defaulting to empty dict."""
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    return {}


def generate_medical_history_pdf(history, filepath):
    """Generate a PDF for a medical history record.
    
    All attribute accesses are wrapped in safe accessors to prevent
    AttributeError or TypeError from None values.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)

    doc = SimpleDocTemplate(
        filepath, pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    orange = colors.HexColor('#d35400')
    styles.add(ParagraphStyle(
        name='SectionHeader', parent=styles['Heading2'],
        fontSize=12, spaceAfter=6, textColor=orange
    ))
    styles.add(ParagraphStyle(
        name='NormalText', parent=styles['Normal'],
        fontSize=10, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name='BoldText', parent=styles['Normal'],
        fontSize=10, spaceAfter=4, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        name='CenterTitle', parent=styles['Heading1'],
        alignment=1, textColor=orange
    ))

    elements = []

    # ---------- Logo ----------
    logo_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'frontend', 'static', 'img', 'logo.png'
    )
    logo_path = os.path.abspath(logo_path)
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=2 * inch, height=1.2 * inch)
            img.hAlign = 'CENTER'
            elements.append(img)
            elements.append(Spacer(1, 10))
        except Exception:
            pass  # Skip logo if it can't be loaded

    elements.append(Paragraph("<b>HISTORIA MÉDICA</b>", styles['CenterTitle']))
    elements.append(Spacer(1, 12))

    # ---------- Patient info ----------
    patient = history.patient
    birth_date = getattr(patient, 'birth_date', None) if patient else None
    age = ""
    if birth_date:
        try:
            age = str((datetime.today().date() - birth_date).days // 365)
        except Exception:
            age = ""

    data = [
        ["Relación laboral:", safe(getattr(history, 'relacion_laboral', None)),
         "N° cédula:", safe(getattr(patient, 'cedula', None)) if patient else ""],
        ["Nombre:", safe(getattr(patient, 'first_name', None)) if patient else "",
         "Apellidos:", safe(getattr(patient, 'last_name', None)) if patient else ""],
        ["Edad:", age,
         "Sexo:", safe(getattr(patient, 'gender', None)) if patient else ""],
        ["Fecha de nac.:", safe_date(birth_date),
         "Estado civil:", safe(getattr(history, 'estado_civil', None))],
        ["Ocupación:", safe(getattr(history, 'ocupacion', None)),
         "Nacionalidad:", safe(getattr(history, 'nacionalidad', None))],
        ["Tipo de sangre:", safe(getattr(history, 'tipo_sangre', None)),
         "Teléfono:", safe(getattr(patient, 'phone', None)) if patient else ""],
        ["Correo:", safe(getattr(patient, 'email', None)) if patient else "",
         "", ""],
    ]

    t = Table(data, colWidths=[1.5 * inch, 2 * inch, 1 * inch, 2 * inch])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fde8d0')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#fde8d0')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    # ---------- Observaciones ----------
    obs = safe(getattr(history, 'observaciones', None))
    if obs:
        elements.append(Paragraph(f"<b>Observaciones:</b> {obs}", styles['NormalText']))
        elements.append(Spacer(1, 10))

    # ---------- Text sections ----------
    text_fields = [
        ("Motivo de consulta:", getattr(history, 'motivo_consulta', None)),
        ("Enfermedad actual:", getattr(history, 'enfermedad_actual', None)),
        ("Antecedentes personales:", getattr(history, 'antecedentes_personales', None)),
    ]
    for title, val in text_fields:
        elements.append(Paragraph(f"<b>{title}</b>", styles['SectionHeader']))
        elements.append(Paragraph(safe(val, "____________________"), styles['NormalText']))
        elements.append(Spacer(1, 8))

    # ---------- Habits tables ----------
    habitos_toxicos = safe_dict(getattr(history, 'habitos_toxicos', None))
    habitos_fisiologicos = safe_dict(getattr(history, 'habitos_fisiologicos', None))

    tox_data = [["Hábitos tóxicos", "Positivo", "Negativo"]]
    for h in ['Alcohol', 'Tabaco', 'Drogas', 'Infusiones', 'Actividad física']:
        val = habitos_toxicos.get(h, '')
        tox_data.append([h, "X" if val == "Positivo" else "", "X" if val == "Negativo" else ""])

    fis_data = [["Hábitos fisiológicos", "Positivo", "Negativo"]]
    for h in ['Alimentación', 'Diuresis', 'Sueño', 'Alergias', 'Otros']:
        val = habitos_fisiologicos.get(h, '')
        fis_data.append([h, "X" if val == "Positivo" else "", "X" if val == "Negativo" else ""])

    table_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ])

    t_tox = Table(tox_data, colWidths=[2 * inch, 1 * inch, 1 * inch])
    t_tox.setStyle(table_style)

    t_fis = Table(fis_data, colWidths=[2 * inch, 1 * inch, 1 * inch])
    t_fis.setStyle(table_style)

    elements.append(Table([[t_tox, t_fis]], colWidths=[4 * inch, 4 * inch]))
    elements.append(Spacer(1, 12))

    # ---------- More text sections ----------
    more_sections = [
        ("Enfermedades de la infancia:", getattr(history, 'enfermedades_infancia', None)),
        ("Antecedentes familiares:", getattr(history, 'antecedentes_familiares', None)),
        ("Cirugías y hospitalizaciones:", getattr(history, 'cirugias_hospitalizaciones', None)),
    ]
    for title, text in more_sections:
        elements.append(Paragraph(f"<b>{title}</b>", styles['SectionHeader']))
        elements.append(Paragraph(safe(text, "__________________________________________________"), styles['NormalText']))
        elements.append(Spacer(1, 8))

    # ---------- Examen Físico ----------
    elements.append(Paragraph("<b>Examen físico:</b>", styles['SectionHeader']))
    ef = safe_dict(getattr(history, 'examen_fisico', None))
    ef_text = " | ".join([f"<b>{k}:</b> {v}" for k, v in ef.items() if v])
    if ef_text:
        elements.append(Paragraph(ef_text, styles['NormalText']))

    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Impresión general:</b>", styles['BoldText']))
    ig = safe_dict(getattr(history, 'impresion_general', None))
    ig_text = " | ".join([f"<b>{k}:</b> {v}" for k, v in ig.items() if v])
    if ig_text:
        elements.append(Paragraph(ig_text, styles['NormalText']))

    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Piel, faneras y tejido celular subcutáneo:</b>", styles['BoldText']))
    pf = safe_dict(getattr(history, 'piel_tejido', None))
    pf_text = " | ".join([f"<b>{k}:</b> {v}" for k, v in pf.items() if v])
    if pf_text:
        elements.append(Paragraph(pf_text, styles['NormalText']))

    elements.append(Spacer(1, 8))

    # ---------- System sections ----------
    sys_sections = [
        ("Respiratorio", safe_dict(getattr(history, 'respiratorio', None))),
        ("Cardiovascular", safe_dict(getattr(history, 'cardiovascular', None))),
        ("Abdomen", safe_dict(getattr(history, 'abdomen', None))),
        ("Neurológico", safe_dict(getattr(history, 'neurologico', None))),
    ]
    for title, dic in sys_sections:
        elements.append(Paragraph(f"<b>{title}:</b>", styles['BoldText']))
        s_text = " | ".join([f"<b>{k}:</b> {v}" for k, v in dic.items() if v])
        if s_text:
            elements.append(Paragraph(s_text, styles['NormalText']))
        elements.append(Spacer(1, 4))

    elements.append(Spacer(1, 8))

    # ---------- Diagnosis and treatment ----------
    final_sections = [
        ("Diagnóstico:", getattr(history, 'diagnostico', None)),
        ("Exámenes complementarios:", getattr(history, 'examenes_complementarios', None)),
        ("Tratamiento:", getattr(history, 'tratamiento', None)),
    ]
    for title, text in final_sections:
        elements.append(Paragraph(f"<b>{title}</b>", styles['SectionHeader']))
        elements.append(Paragraph(safe(text, "__________________________________________________"), styles['NormalText']))
        elements.append(Spacer(1, 8))

    # ---------- Doctor signature ----------
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("___________________________", styles['NormalText']))
    doctor = history.doctor
    doctor_name = safe(getattr(doctor, 'full_name', None), "N/A") if doctor else "N/A"
    elements.append(Paragraph(f"Firma médico: {doctor_name}", styles['NormalText']))

    # ---------- Build PDF ----------
    doc.build(elements)
    return filepath
