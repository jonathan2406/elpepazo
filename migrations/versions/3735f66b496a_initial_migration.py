"""Initial migration

Revision ID: 3735f66b496a
Revises: 
Create Date: 2024-07-30 23:26:58.256973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3735f66b496a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('password_hash', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('doctor',
    sa.Column('dni', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('specialty', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('dni')
    )
    op.create_table('patient',
    sa.Column('dni', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password_hash', sa.String(length=150), nullable=False),
    sa.Column('otp_secret', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('dni'),
    sa.UniqueConstraint('email')
    )
    op.create_table('appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.dni'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.dni'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointment')
    op.drop_table('patient')
    op.drop_table('doctor')
    op.drop_table('admin')
    # ### end Alembic commands ###
