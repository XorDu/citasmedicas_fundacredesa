from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.specialty import Specialty
from backend.models.permission import Permission
from werkzeug.security import generate_password_hash
import random

app = create_app('development')

def seed_database():
    with app.app_context():
        db.create_all()

        # Create Superadmin if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            superadmin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                role='superadmin',
                full_name='Super Administrador'
            )
            db.session.add(superadmin)

        # Especialidades basadas en la foto proporcionada
        specialties_data = [
            {'name': 'Pediatría', 'color': '#f39c12', 'desc': 'Atención médica para niños y adolescentes', 'doctor': 'Dra. Gaudis Guevara'},
            {'name': 'Medicina General', 'color': '#2ecc71', 'desc': 'Atención primaria e integral', 'doctor': 'Dra. Yajaira Pérez'},
            {'name': 'Nutrición', 'color': '#8e44ad', 'desc': 'Control y evaluación nutricional', 'doctor': 'Lic. Jenny Labrador'},
            {'name': 'Nefrología', 'color': '#3498db', 'desc': 'Estudio y tratamiento del riñón', 'doctor': 'Dra. Yaneth León'},
            {'name': 'Ginecología', 'color': '#e74c3c', 'desc': 'Atención médica de la mujer', 'doctor': 'Dra. Mileydy D\'Arthenay'},
            {'name': 'Gastroenterología', 'color': '#16a085', 'desc': 'Sistema digestivo', 'doctor': 'Dra. Dayana Ascanio'},
            {'name': 'Geriatría', 'color': '#95a5a6', 'desc': 'Atención del adulto mayor', 'doctor': 'Dra. Nilda Hernández'},
            {'name': 'Fisioterapia', 'color': '#d35400', 'desc': 'Rehabilitación física', 'doctor': 'Ft. Jorge Saavedra'},
            {'name': 'Cardiología', 'color': '#c0392b', 'desc': 'Estudio y tratamiento del corazón', 'doctor': 'Dr. Emiro Flores Díaz'},
            {'name': 'Traumatología', 'color': '#2c3e50', 'desc': 'Tratamiento de lesiones óseas y musculares', 'doctor': 'Dr. Aly Cerbando Pérez'},
        ]

        for s_data in specialties_data:
            specialty = Specialty.query.filter_by(name=s_data['name']).first()
            if not specialty:
                specialty = Specialty(
                    name=s_data['name'],
                    color=s_data['color'],
                    description=s_data['desc']
                )
                db.session.add(specialty)
                db.session.flush() # To get specialty.id

                # Default permissions
                permission = Permission(
                    specialty_id=specialty.id,
                    can_create=True,
                    can_edit=True,
                    can_delete=False
                )
                db.session.add(permission)

                # Create user for this specialty
                user_username = s_data['name'].lower().replace('í', 'i').replace('ó', 'o').replace(' ', '')[:6] + 'user'
                if not User.query.filter_by(username=user_username).first():
                    user = User(
                        username=user_username,
                        password_hash=generate_password_hash('user123'),
                        role='specialty',
                        specialty_id=specialty.id,
                        full_name=s_data['doctor']
                    )
                    db.session.add(user)

        db.session.commit()
        print("Database seeded successfully with new specialties and doctors!")

if __name__ == '__main__':
    seed_database()
