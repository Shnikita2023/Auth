"""Initial tables v1

Revision ID: 868ffc58bd3b
Revises: 
Create Date: 2024-05-23 10:18:44.377727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '868ffc58bd3b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('сredential',
    sa.Column('oid', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('middle_name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('number_phone', sa.String(length=11), nullable=False),
    sa.Column('time_call', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_index(op.f('ix_сredential_email'), 'сredential', ['email'], unique=True)
    op.create_index(op.f('ix_сredential_number_phone'), 'сredential', ['number_phone'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_сredential_number_phone'), table_name='сredential')
    op.drop_index(op.f('ix_сredential_email'), table_name='сredential')
    op.drop_table('сredential')
    # ### end Alembic commands ###
