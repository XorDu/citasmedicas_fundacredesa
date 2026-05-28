from backend.database import db
from datetime import datetime

class Representative(db.Model):
    __tablename__ = 'representatives'

    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

    patients = db.relationship('Patient', back_populates='representative')

    def __repr__(self):
        return f'<Representative {self.cedula} - {self.first_name} {self.last_name}>'

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(20), unique=True, nullable=True) # Nullable for minors without ID
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    is_minor = db.Column(db.Boolean, default=False)
    representative_id = db.Column(db.Integer, db.ForeignKey('representatives.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    representative = db.relationship('Representative', back_populates='patients')
    appointments = db.relationship('Appointment', back_populates='patient')

    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'
