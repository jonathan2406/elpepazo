# init_db.py

from app import app, db
from models import Doctor, Patient
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create tables
    db.create_all()

    # Admin user data
    admin_dni = 999999
    admin_password = 'adminpassword'  # Cambia esto por una contraseña segura

    # Create admin user
    hashed_password = generate_password_hash(admin_password, method='sha256')
    admin_user = Patient(
        name='Admin', 
        dni=admin_dni, 
        email='admin@example.com',  # Cambia esto por un email válido
        password_hash=hashed_password,
        otp_secret='JBSWY3DPEHPK3PXP'  # Genera un OTP secreto válido aquí o usa una cadena aleatoria
    )

    # Check if the admin user already exists
    existing_admin = Patient.query.filter_by(dni=admin_dni).first()
    if existing_admin:
        print("Admin user already exists.")
    else:
        # Add admin user to database
        db.session.add(admin_user)
        db.session.commit()
        print("Database initialized and admin user created.")

