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
    
    if request.method == 'POST':
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
            tratamiento=request.form.get('tratamiento')
        )
        
        # Parse JSON fields from form (simplified for demo)
        # habitos_toxicos = {"alcohol": request.form.get('alcohol'), ...}
        
        db.session.add(history)
        db.session.commit()
        flash('Historia médica guardada exitosamente.', 'success')
        return redirect(url_for('historias.index'))
        
    medicos = User.query.filter_by(role='specialty').all()
    return render_template('historias/create.html', patient=patient, medicos=medicos)

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
        history.motivo_consulta = request.form.get('motivo_consulta')
        history.enfermedad_actual = request.form.get('enfermedad_actual')
        history.diagnostico = request.form.get('diagnostico')
        history.tratamiento = request.form.get('tratamiento')
        db.session.commit()
        flash('Historia médica actualizada.', 'success')
        return redirect(url_for('historias.view', id=history.id))
        
    return render_template('historias/edit.html', history=history)

@historias_bp.route('/pdf/<int:id>')
@login_required
def generate_pdf(id):
    history = MedicalHistory.query.get_or_404(id)
    filename = f"historia_{history.patient.cedula}_{history.id}.pdf"
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'static', 'pdfs', filename)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    generate_medical_history_pdf(history, filepath)
    
    return send_file(filepath, as_attachment=True)
