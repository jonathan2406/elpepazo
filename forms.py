# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TimeField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email

class DoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dni = StringField('Dni', validators=[DataRequired()])
    specialty = StringField('Specialty', validators=[DataRequired()])

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dni = StringField('dni', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class AppointmentForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    reason = TextAreaField('Reason', validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int)
    patient_id = SelectField('Patient', coerce=int)

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dni = StringField('dni', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    dni = StringField('DNI', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class TwoFactorForm(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired()])