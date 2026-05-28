from backend.database import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='specialty') # 'superadmin' or 'specialty'
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    specialty = db.relationship('Specialty', back_populates='users')
    appointments_created = db.relationship('Appointment', back_populates='creator')

    def __repr__(self):
        return f'<User {self.username} - {self.role}>'
