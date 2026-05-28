from flask import Blueprint, render_template
from flask_login import login_required
from backend.models.appointment import Appointment
from backend.models.patient import Patient
from datetime import date

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/inicio')
@login_required
def index():
    # Obtener citas de hoy
    today = date.today()
    citas_hoy = Appointment.query.filter_by(appointment_date=today).all()
    
    # Actividad reciente (ejemplo básico: últimas 5 citas creadas)
    actividad_reciente = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', citas_hoy=citas_hoy, actividad_reciente=actividad_reciente)
