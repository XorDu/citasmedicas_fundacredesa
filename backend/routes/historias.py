import os
import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from backend.models.patient import Patient
from backend.models.user import User
from backend.models.medical_history import MedicalHistory
from backend.database import db
from backend.utils.pdf_generator import generate_medical_history_pdf

historias_bp = Blueprint('historias', __name__, url_prefix='/historias')

@historias_bp.route('/')
@login_required
def index():
    historias = MedicalHistory.query.all()
    medicos = User.query.filter_by(role='specialty').all()
    
    return render_template('historias/list.html', historias=historias, medicos=medicos)

@historias_bp.route('/create/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def create(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Calculate age
    from datetime import date
    today = date.today()
    age = today.year - patient.birth_date.year - ((today.month, today.day) < (patient.birth_date.month, patient.birth_date.day)) if patient.birth_date else ''
    
    if request.method == 'POST':
        # Recolectar diccionarios para los campos JSON
        habitos_toxicos = { h: request.form.get(f'tox_{h}', '') for h in ['Alcohol', 'Tabaco', 'Drogas', 'Infusiones', 'Actividad física'] }
        habitos_fisiologicos = { h: request.form.get(f'fis_{h}', '') for h in ['Alimentación', 'Diuresis', 'Sueño', 'Alergias', 'Otros'] }
        examen_fisico = { h: request.form.get(f'ef_{h}', '') for h in ['TA', 'FC', 'FR', 'Temperatura', 'Peso', 'Altura', 'IMC'] }
        impresion_general = { h: request.form.get(f'ig_{h}', '') for h in ['Constitución', 'Facies', 'Actitud', 'Decúbito', 'Marcha'] }
        piel_tejido = { h: request.form.get(f'pf_{h}', '') for h in ['Aspecto', 'Distribución pilosa', 'Lesiones', 'Faneras', 'Tejido celular subcutáneo'] }
        respiratorio = { h: request.form.get(f'resp_{h}', '') for h in ['Inspección', 'Palpación', 'Percusión', 'Auscultación'] }
        cardiovascular = { h: request.form.get(f'cardio_{h}', '') for h in ['Inspección', 'Palpación', 'Auscultación', 'Pulsos'] }
        abdomen = { h: request.form.get(f'abdom_{h}', '') for h in ['Inspección', 'Palpación', 'Percusión', 'Auscultación'] }
        neurologico = { h: request.form.get(f'neuro_{h}', '') for h in ['Glasgow', 'Motilidad Activa', 'Motilidad Pasiva', 'Motilidad Refleja', 'Pares Craneales', 'Sensibilidad'] }

        history = MedicalHistory(
            patient_id=patient.id,
            doctor_id=current_user.id if current_user.role == 'specialty' else request.form.get('doctor_id'),
            relacion_laboral=request.form.get('relacion_laboral'),
            estado_civil=request.form.get('estado_civil'),
            ocupacion=request.form.get('ocupacion'),
            nacionalidad=request.form.get('nacionalidad'),
            tipo_sangre=request.form.get('tipo_sangre'),
            observaciones=request.form.get('observaciones'),
            motivo_consulta=request.form.get('motivo_consulta'),
            enfermedad_actual=request.form.get('enfermedad_actual'),
            antecedentes_personales=request.form.get('antecedentes_personales'),
            enfermedades_infancia=request.form.get('enfermedades_infancia'),
            antecedentes_familiares=request.form.get('antecedentes_familiares'),
            cirugias_hospitalizaciones=request.form.get('cirugias_hospitalizaciones'),
            diagnostico=request.form.get('diagnostico'),
            examenes_complementarios=request.form.get('examenes_complementarios'),
            tratamiento=request.form.get('tratamiento'),
            
            # Asignando los JSONs
            habitos_toxicos=habitos_toxicos,
            habitos_fisiologicos=habitos_fisiologicos,
            examen_fisico=examen_fisico,
            impresion_general=impresion_general,
            piel_tejido=piel_tejido,
            respiratorio=respiratorio,
            cardiovascular=cardiovascular,
            abdomen=abdomen,
            neurologico=neurologico
        )
        
        db.session.add(history)
        db.session.commit()
        flash('Historia médica guardada exitosamente.', 'success')
        return redirect(url_for('historias.index'))
        
    medicos = User.query.filter_by(role='specialty').all()
    return render_template('historias/create.html', patient=patient, medicos=medicos, today_date=today.strftime('%Y-%m-%d'), age=age)

@historias_bp.route('/view/<int:id>')
@login_required
def view(id):
    history = MedicalHistory.query.get_or_404(id)
    return render_template('historias/view.html', history=history)

@historias_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    history = MedicalHistory.query.get_or_404(id)
    
    if request.method == 'POST':
        # Collect dicts for JSON fields
        habitos_toxicos = { h: request.form.get(f'tox_{h}', '') for h in ['Alcohol', 'Tabaco', 'Drogas', 'Infusiones', 'Actividad física'] }
        habitos_fisiologicos = { h: request.form.get(f'fis_{h}', '') for h in ['Alimentación', 'Diuresis', 'Sueño', 'Alergias', 'Otros'] }
        examen_fisico = { h: request.form.get(f'ef_{h}', '') for h in ['TA', 'FC', 'FR', 'Temperatura', 'Peso', 'Altura', 'IMC'] }
        impresion_general = { h: request.form.get(f'ig_{h}', '') for h in ['Constitución', 'Facies', 'Actitud', 'Decúbito', 'Marcha'] }
        piel_tejido = { h: request.form.get(f'pf_{h}', '') for h in ['Aspecto', 'Distribución pilosa', 'Lesiones', 'Faneras', 'Tejido celular subcutáneo'] }
        respiratorio = { h: request.form.get(f'resp_{h}', '') for h in ['Inspección', 'Palpación', 'Percusión', 'Auscultación'] }
        cardiovascular = { h: request.form.get(f'cardio_{h}', '') for h in ['Inspección', 'Palpación', 'Auscultación', 'Pulsos'] }
        abdomen = { h: request.form.get(f'abdom_{h}', '') for h in ['Inspección', 'Palpación', 'Percusión', 'Auscultación'] }
        neurologico = { h: request.form.get(f'neuro_{h}', '') for h in ['Glasgow', 'Motilidad Activa', 'Motilidad Pasiva', 'Motilidad Refleja', 'Pares Craneales', 'Sensibilidad'] }

        history.relacion_laboral = request.form.get('relacion_laboral')
        history.estado_civil = request.form.get('estado_civil')
        history.ocupacion = request.form.get('ocupacion')
        history.nacionalidad = request.form.get('nacionalidad')
        history.tipo_sangre = request.form.get('tipo_sangre')
        history.observaciones = request.form.get('observaciones')
        history.motivo_consulta = request.form.get('motivo_consulta')
        history.enfermedad_actual = request.form.get('enfermedad_actual')
        history.antecedentes_personales = request.form.get('antecedentes_personales')
        history.enfermedades_infancia = request.form.get('enfermedades_infancia')
        history.antecedentes_familiares = request.form.get('antecedentes_familiares')
        history.cirugias_hospitalizaciones = request.form.get('cirugias_hospitalizaciones')
        history.diagnostico = request.form.get('diagnostico')
        history.examenes_complementarios = request.form.get('examenes_complementarios')
        history.tratamiento = request.form.get('tratamiento')
        
        # Assign JSON fields
        history.habitos_toxicos = habitos_toxicos
        history.habitos_fisiologicos = habitos_fisiologicos
        history.examen_fisico = examen_fisico
        history.impresion_general = impresion_general
        history.piel_tejido = piel_tejido
        history.respiratorio = respiratorio
        history.cardiovascular = cardiovascular
        history.abdomen = abdomen
        history.neurologico = neurologico
        
        db.session.commit()
        flash('Historia médica actualizada exitosamente.', 'success')
        return redirect(url_for('historias.view', id=history.id))
        
    return render_template('historias/edit.html', history=history)

@historias_bp.route('/pdf/<int:id>')
@login_required
def generate_pdf(id):
    history = MedicalHistory.query.get_or_404(id)
    
    # Build a safe filename (cedula can be None for minors)
    patient_identifier = history.patient.cedula if history.patient and history.patient.cedula else f"paciente_{history.patient_id}"
    filename = f"historia_{patient_identifier}_{history.id}.pdf"
    
    pdf_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'static', 'pdfs')
    pdf_dir = os.path.abspath(pdf_dir)
    os.makedirs(pdf_dir, exist_ok=True)
    filepath = os.path.join(pdf_dir, filename)
    
    try:
        generate_medical_history_pdf(history, filepath)
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f'Error al generar el PDF: {str(e)}', 'danger')
        return redirect(url_for('historias.view', id=history.id))
    
    return send_file(filepath, as_attachment=True, download_name=filename)

