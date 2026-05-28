from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from backend.models.appointment import Appointment
from backend.models.patient import Patient, Representative
from backend.models.specialty import Specialty
from backend.database import db
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@appointments_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # If not superadmin, specialty users need permission to create
    if current_user.role == 'specialty':
        from backend.models.permission import Permission
        perm = Permission.query.filter_by(specialty_id=current_user.specialty_id).first()
        if not perm or not perm.can_create:
            flash('No tienes permiso para crear citas.', 'danger')
            return redirect(url_for('calendar.index'))

    if request.method == 'POST':
        # Logic to handle minor/representative or direct patient
        is_minor = request.form.get('is_minor') == 'true'
        patient_id = None
        
        if is_minor:
            selected_minor_id = request.form.get('selected_minor_id')
            if selected_minor_id:
                patient_id = selected_minor_id
            else:
                # Create minor and representative if they don't exist
                pass # Simplified for this demo
        else:
            cedula = request.form.get('cedula')
            patient = Patient.query.filter_by(cedula=cedula).first()
            if patient:
                patient_id = patient.id
            else:
                # Create patient
                patient = Patient(
                    cedula=cedula,
                    first_name=request.form.get('first_name'),
                    last_name=request.form.get('last_name'),
                    birth_date=datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date()
                )
                db.session.add(patient)
                db.session.flush()
                patient_id = patient.id
                
        specialty_id = current_user.specialty_id if current_user.role == 'specialty' else request.form.get('specialty_id')
        
        appointment = Appointment(
            patient_id=patient_id,
            specialty_id=specialty_id,
            created_by_id=current_user.id,
            appointment_date=datetime.strptime(request.form.get('appointment_date'), '%Y-%m-%d').date(),
            appointment_time=datetime.strptime(request.form.get('appointment_time'), '%H:%M').time(),
            type=request.form.get('type', 'General'),
            room=request.form.get('room')
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Cita agendada exitosamente.', 'success')
        return redirect(url_for('calendar.index'))
        
    specialties = Specialty.query.all() if current_user.role == 'superadmin' else []
    return render_template('appointments/create.html', specialties=specialties)

@appointments_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    appointment = Appointment.query.get_or_404(id)
    
    if current_user.role == 'specialty':
        if appointment.specialty_id != current_user.specialty_id:
            flash('No puedes eliminar citas de otra especialidad.', 'danger')
            return redirect(url_for('calendar.index'))
            
        from backend.models.permission import Permission
        perm = Permission.query.filter_by(specialty_id=current_user.specialty_id).first()
        if not perm or not perm.can_delete:
            flash('Tu especialidad no tiene permisos para borrar citas.', 'danger')
            return redirect(url_for('calendar.index'))
            
    db.session.delete(appointment)
    db.session.commit()
    flash('Cita eliminada.', 'success')
    return redirect(url_for('calendar.index'))
