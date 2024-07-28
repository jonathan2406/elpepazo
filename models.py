
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db:SQLAlchemy = SQLAlchemy()

class Doctor(db.Model):
    # Overwrite
    def get_id(self):
        return self.dni
    
    name = db.Column(db.String(150), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.Integer, nullable=False, primary_key=True)

class Patient(db.Model, UserMixin):
    # Overwrite
    def get_id(self):
        return self.dni
    name = db.Column(db.String(150), nullable=False)
    dni = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.dni'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.dni'), nullable=False)

class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.dni'))
