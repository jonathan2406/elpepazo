from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, Doctor, Patient, Appointment
from forms import DoctorForm, PatientForm, AppointmentForm
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Patient.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/doctors', methods=['GET', 'POST'])
def manage_doctors():
    form = DoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(name=form.name.data, specialty=form.specialty.data)
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added successfully')
        return redirect(url_for('manage_doctors'))
    doctors = Doctor.query.all()
    return render_template('admin/doctors.html', form=form, doctors=doctors)

@app.route('/admin/patients', methods=['GET', 'POST'])
def manage_patients():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(name=form.name.data, cedula=form.cedula.data)
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully')
        return redirect(url_for('manage_patients'))
    patients = Patient.query.all()
    return render_template('admin/patients.html', form=form, patients=patients)

@app.route('/admin/appointments', methods=['GET', 'POST'])
def manage_appointments():
    form = AppointmentForm()
    form.doctor_id.choices = [(doctor.id, doctor.name) for doctor in Doctor.query.all()]
    form.patient_id.choices = [(patient.id, patient.name) for patient in Patient.query.all()]
    if form.validate_on_submit():
        appointment = Appointment(
            date=form.date.data, 
            time=form.time.data, 
            reason=form.reason.data, 
            doctor_id=form.doctor_id.data, 
            patient_id=form.patient_id.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment created successfully')
        return redirect(url_for('manage_appointments'))
    appointments = Appointment.query.all()
    return render_template('admin/appointments.html', form=form, appointments=appointments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cedula = request.form['cedula']
        patient = Patient.query.filter_by(cedula=cedula).first()
        if patient:
            login_user(patient)
            return redirect(url_for('user_panel'))
        else:
            flash('Invalid Cedula')
    return render_template('user/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/panel')
@login_required
def user_panel():
    return render_template('user/panel.html')

@app.route('/user/request_appointment', methods=['GET', 'POST'])
@login_required
def request_appointment():
    form = AppointmentForm()
    form.doctor_id.choices = [(doctor.id, doctor.name) for doctor in Doctor.query.all()]
    if form.validate_on_submit():
        appointment = Appointment(
            date=form.date.data, 
            time=form.time.data, 
            reason=form.reason.data, 
            doctor_id=form.doctor_id.data, 
            patient_id=current_user.id
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment requested successfully')
        return redirect(url_for('user_panel'))
    return render_template('user/request_appointment.html', form=form)

@app.route('/user/view_appointments')
@login_required
def view_appointments():
    appointments = Appointment.query.filter_by(patient_id=current_user.id).all()
    return render_template('user/view_appointments.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)
