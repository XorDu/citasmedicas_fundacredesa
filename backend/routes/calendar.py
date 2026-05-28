from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from backend.models.appointment import Appointment
from backend.models.specialty import Specialty
from backend.models.patient import Patient

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/')
@login_required
def index():
    specialties = Specialty.query.filter_by(active=True).all()
    return render_template('agenda.html', specialties=specialties)

@calendar_bp.route('/api/events')
@login_required
def get_events():
    start = request.args.get('start')
    end = request.args.get('end')
    
    # In a real app, parse start/end and filter appointments. 
    # For now, return all appointments to show in the calendar.
    appointments = Appointment.query.all()
    
    events = []
    for appt in appointments:
        # Check permissions for editing
        editable = False
        if current_user.role == 'superadmin' or appt.specialty_id == current_user.specialty_id:
            editable = True
            
        events.append({
            'id': appt.id,
            'title': f'{appt.patient.first_name} {appt.patient.last_name} - {appt.type}',
            'start': f"{appt.appointment_date}T{appt.appointment_time}",
            'end': f"{appt.appointment_date}T{appt.appointment_time}", # Simplified, should use duration
            'color': appt.specialty.color,
            'editable': editable,
            'extendedProps': {
                'specialty': appt.specialty.name,
                'status': appt.status,
                'room': appt.room
            }
        })
        
    return jsonify(events)
