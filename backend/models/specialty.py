from backend.database import db
from datetime import datetime

class Specialty(db.Model):
    __tablename__ = 'specialties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(7), default='#3788d8')
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)

    users = db.relationship('User', back_populates='specialty')
    permission = db.relationship('Permission', back_populates='specialty', uselist=False)
    appointments = db.relationship('Appointment', back_populates='specialty')

    def __repr__(self):
        return f'<Specialty {self.name}>'
