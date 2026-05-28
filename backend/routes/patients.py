from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from backend.models.patient import Patient, Representative
from backend.database import db
from datetime import datetime

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

@patients_bp.route('/')
@login_required
def index():
    query = request.args.get('q', '')
    if query:
        patients = Patient.query.filter(
            db.or_(
                Patient.cedula.contains(query),
                Patient.first_name.ilike(f'%{query}%'),
                Patient.last_name.ilike(f'%{query}%')
            )
        ).all()
    else:
        patients = Patient.query.all()
    return render_template('patients/list.html', patients=patients, query=query)

@patients_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        is_minor = request.form.get('is_minor') == 'true'
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birth_date_str = request.form.get('birth_date')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        
        birth_date = None
        if birth_date_str:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

        representative_id = None
        cedula = request.form.get('cedula')
        
        if is_minor:
            # Handle Representative
            rep_cedula = request.form.get('rep_cedula')
            rep_first_name = request.form.get('rep_first_name')
            rep_last_name = request.form.get('rep_last_name')
            rep_phone = request.form.get('rep_phone')
            rep_email = request.form.get('rep_email')
            
            # Find or create Representative
            rep = Representative.query.filter_by(cedula=rep_cedula).first()
            if not rep:
                rep = Representative(
                    cedula=rep_cedula,
                    first_name=rep_first_name,
                    last_name=rep_last_name,
                    phone=rep_phone,
                    email=rep_email
                )
                db.session.add(rep)
                db.session.flush()
            representative_id = rep.id
            cedula = None # Minors typically do not have a cedula in this system
        else:
            # Direct patient - check if cedula already exists
            if cedula:
                existing = Patient.query.filter_by(cedula=cedula).first()
                if existing:
                    flash(f'El paciente con cédula {cedula} ya se encuentra registrado.', 'danger')
                    return redirect(url_for('patients.index'))

        patient = Patient(
            cedula=cedula,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            gender=gender,
            phone=phone,
            email=email,
            address=address,
            is_minor=is_minor,
            representative_id=representative_id
        )
        db.session.add(patient)
        db.session.commit()
        
        flash('Paciente registrado exitosamente.', 'success')
        return redirect(url_for('patients.index'))

    return render_template('patients/create.html')

@patients_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient.first_name = request.form.get('first_name')
        patient.last_name = request.form.get('last_name')
        
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            patient.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            
        patient.gender = request.form.get('gender')
        patient.phone = request.form.get('phone')
        patient.email = request.form.get('email')
        patient.address = request.form.get('address')
        
        is_minor = request.form.get('is_minor') == 'true'
        patient.is_minor = is_minor
        
        if is_minor:
            rep_cedula = request.form.get('rep_cedula')
            rep_first_name = request.form.get('rep_first_name')
            rep_last_name = request.form.get('rep_last_name')
            rep_phone = request.form.get('rep_phone')
            rep_email = request.form.get('rep_email')
            
            rep = Representative.query.filter_by(cedula=rep_cedula).first()
            if not rep:
                rep = Representative(
                    cedula=rep_cedula,
                    first_name=rep_first_name,
                    last_name=rep_last_name,
                    phone=rep_phone,
                    email=rep_email
                )
                db.session.add(rep)
                db.session.flush()
            else:
                # Update existing rep
                rep.first_name = rep_first_name
                rep.last_name = rep_last_name
                rep.phone = rep_phone
                rep.email = rep_email
            patient.representative_id = rep.id
            patient.cedula = None
        else:
            patient.cedula = request.form.get('cedula')
            patient.representative_id = None
            
        db.session.commit()
        flash('Datos del paciente actualizados.', 'success')
        return redirect(url_for('patients.index'))
        
    return render_template('patients/edit.html', patient=patient)

@patients_bp.route('/api/search_representative')
@login_required
def search_representative():
    cedula = request.args.get('cedula')
    if not cedula:
        return jsonify({"error": "Cédula is required"}), 400
        
    rep = Representative.query.filter_by(cedula=cedula).first()
    if rep:
        minors = Patient.query.filter_by(representative_id=rep.id, is_minor=True).all()
        return jsonify({
            "found": True,
            "representative": {
                "id": rep.id,
                "name": f"{rep.first_name} {rep.last_name}"
            },
            "minors": [{"id": p.id, "name": f"{p.first_name} {p.last_name}"} for p in minors]
        })
    else:
        # If not representative, it might be a direct patient
        patient = Patient.query.filter_by(cedula=cedula).first()
        if patient:
            return jsonify({
                "found": True,
                "is_direct_patient": True,
                "patient": {"id": patient.id, "name": f"{patient.first_name} {patient.last_name}"}
            })
            
    return jsonify({"found": False})
