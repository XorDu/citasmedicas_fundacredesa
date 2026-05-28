from backend.database import db
from datetime import datetime

class MedicalHistory(db.Model):
    __tablename__ = 'medical_histories'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Encabezado (Relación Laboral y datos básicos no cubiertos en patient)
    relacion_laboral = db.Column(db.String(50)) # Titular, Familiar, Otros
    estado_civil = db.Column(db.String(50))
    ocupacion = db.Column(db.String(100))
    nacionalidad = db.Column(db.String(50))
    tipo_sangre = db.Column(db.String(10))
    observaciones = db.Column(db.Text)
    
    # Motivo y Enfermedad
    motivo_consulta = db.Column(db.Text)
    enfermedad_actual = db.Column(db.Text)
    
    # Antecedentes y Hábitos (Se almacenarán como JSON)
    antecedentes_personales = db.Column(db.Text)
    habitos_toxicos = db.Column(db.JSON) # ej: {"alcohol": "positivo", "tabaco": "negativo"...}
    habitos_fisiologicos = db.Column(db.JSON)
    enfermedades_infancia = db.Column(db.Text)
    antecedentes_familiares = db.Column(db.Text)
    cirugias_hospitalizaciones = db.Column(db.Text)
    
    # Examen Físico (JSON para fácil estructura)
    examen_fisico = db.Column(db.JSON) 
    # ej: {"ta": "", "fc": "", "fr": "", "temp": "", "peso": "", "altura": "", "imc": ""}
    impresion_general = db.Column(db.JSON) 
    # ej: {"constitucion": "", "facies": "", "actitud": "", "decubito": "", "marcha": ""}
    piel_tejido = db.Column(db.JSON)
    respiratorio = db.Column(db.JSON)
    cardiovascular = db.Column(db.JSON)
    abdomen = db.Column(db.JSON)
    neurologico = db.Column(db.JSON)
    
    # Diagnóstico y Tratamiento
    diagnostico = db.Column(db.Text)
    examenes_complementarios = db.Column(db.Text)
    tratamiento = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', backref=db.backref('medical_histories', lazy=True))
    doctor = db.relationship('User', backref=db.backref('medical_histories', lazy=True))

    def __repr__(self):
        return f'<MedicalHistory {self.id} for Patient {self.patient_id}>'
