from backend.database import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30)
    
    type = db.Column(db.String(50)) # General, Seguimiento, etc.
    status = db.Column(db.String(20), default='pendiente') # pendiente, confirmada, cancelada, completada
    room = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', back_populates='appointments')
    specialty = db.relationship('Specialty', back_populates='appointments')
    creator = db.relationship('User', back_populates='appointments_created')

    def __repr__(self):
        return f'<Appointment {self.id} on {self.appointment_date} at {self.appointment_time}>'
