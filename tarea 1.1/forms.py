from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class DoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    specialty = StringField('Specialty', validators=[DataRequired()])

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    cedula = StringField('Cedula', validators=[DataRequired()])

class AppointmentForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    reason = TextAreaField('Reason', validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int)
    patient_id = SelectField('Patient', coerce=int)
