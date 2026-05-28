from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from backend.models.patient import Patient, Representative
from backend.database import db

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
