from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, Doctor, Patient, Appointment
from forms import DoctorForm, PatientForm, AppointmentForm, RegistrationForm, LoginForm, TwoFactorForm
from config import Config
from notifications import Notifications
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp

import os
import pyotp
import qrcode
from io import BytesIO
from flask import send_file, render_template, redirect, url_for, request, flash
from forms import RegistrationForm
from models import Patient
from werkzeug.security import generate_password_hash
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Patient.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/error')
def error_page():
    return render_template('error.html')

@app.route('/admin/doctors', methods=['GET', 'POST'])
@login_required
def manage_doctors():
    if not current_user.dni in [100,200,300]:
        return redirect(url_for('index'))
    form = DoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(name=form.name.data, specialty=form.specialty.data, dni=form.dni.data)
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added successfully')
        return redirect(url_for('manage_doctors'))
    doctors = Doctor.query.all()
    return render_template('admin/doctors.html', form=form, doctors=doctors)

@app.route('/admin/patients', methods=['GET', 'POST'])
@login_required
def manage_patients():
    form = PatientForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        patient = Patient(name=form.name.data, dni=form.dni.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully')
        return redirect(url_for('manage_patients'))
    patients = Patient.query.all()
    return render_template('admin/patients.html', form=form, patients=patients)

@app.route('/admin/appointments', methods=['GET', 'POST'])
@login_required
def manage_appointments():
    form = AppointmentForm()
    form.doctor_id.choices = [(doctor.dni, doctor.name) for doctor in Doctor.query.all()]
    form.patient_id.choices = [(patient.dni, patient.name) for patient in Patient.query.all()]
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

        # Notification block
        patient = Patient.query.get(form.patient_id.data)
        if patient:
            notify = Notifications()
            notify.format_email(
                date=form.date.data, 
                time=form.time.data, 
                reason=form.reason.data, 
                doctor_id=form.doctor_id.data, 
                patient_id=form.patient_id.data)
            notify.send_email(patient.email, "New appointment scheduled successfully!", form.reason.data)

        return redirect(url_for('manage_appointments'))
    appointments = Appointment.query.all()
    return render_template('admin/appointments.html', form=form, appointments=appointments)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        patientDni = Patient.query.filter_by(dni=form.dni.data).first()
        patientEmail = Patient.query.filter_by(dni=form.email.data).first()
        
        if patientDni:
            flash('DNI already registered')
        if patientEmail:
            flash('Email already')
        else:
            otp_secret = pyotp.random_base32()
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            new_patient = Patient(
                name=form.name.data, 
                dni=form.dni.data, 
                email=form.email.data, 
                password_hash=hashed_password,
                otp_secret=otp_secret
            )
            db.session.add(new_patient)
            db.session.commit()

            # Generar el código QR
            totp = pyotp.TOTP(otp_secret)
            qr_uri = totp.provisioning_uri(name=form.email.data, issuer_name="Reyah")
            qr = qrcode.make(qr_uri)
            qr_path = os.path.join('static', 'otp_qr.png')
            qr.save(qr_path)

            # Redirigir a la página para mostrar el QR

            flash('register done!!!')
            return render_template('user/qr_display.html', qr_path='otp_qr.png')

    return render_template('user/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(dni=form.dni.data).first()
        if patient and check_password_hash(patient.password_hash, form.password.data):
            login_user(patient)
            return redirect(url_for('two_factor'))
        else:
            flash('Invalid DNI or password')
    return render_template('user/login.html', form=form)

@app.route('/two_factor', methods=['GET', 'POST'])
@login_required
def two_factor():
    form = TwoFactorForm()
    if form.validate_on_submit():
        if pyotp.TOTP(current_user.otp_secret).verify(form.otp.data):
            return redirect(url_for('user_panel'))
        else:
            flash('Invalid OTP')
    return render_template('user/two_factor.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/panel')
@login_required
def user_panel():
    appointments = Appointment.query.filter_by(patient_id=current_user.dni).all()
    return render_template('user/panel.html', appointments=appointments)

# endpoint
@app.route('/user/request_appointments', methods=['GET', 'POST'])
@login_required
def request_appointments():
    form = AppointmentForm()
    form.doctor_id.choices = [(doctor.dni, doctor.name) for doctor in Doctor.query.all()]
    form.patient_id.choices = [(current_user.dni, current_user.name)]
    if form.validate_on_submit():
        appointment = Appointment(
            date=form.date.data, 
            time=form.time.data, 
            reason=form.reason.data, 
            doctor_id=form.doctor_id.data, 
            patient_id=current_user.dni
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment requested successfully')

        # Notification block
        patient = Patient.query.get(form.patient_id.data)
        if patient:
            notify = Notifications()
            notify.format_email(
                date=form.date.data, 
                time=form.time.data, 
                reason=form.reason.data, 
                doctor=form.doctor_id.data, 
                patient=form.patient_id.data)
            notify.send_email(to_address=patient.email)

        return redirect(url_for('user_panel'))


    # template
    return render_template('user/request_appointments.html', form=form)

# endpoint
@app.route('/user/view_appointments')
@login_required
def view_appointments():
    appointments = Appointment.query.filter_by(patient_id=current_user.dni).all()
    # template
    return render_template('user/view_appointments.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)
