from backend.database import db

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=False, unique=True)
    can_create = db.Column(db.Boolean, default=True)
    can_edit = db.Column(db.Boolean, default=True)
    can_delete = db.Column(db.Boolean, default=False)

    specialty = db.relationship('Specialty', back_populates='permission')

    def __repr__(self):
        return f'<Permission for Specialty ID {self.specialty_id}>'
