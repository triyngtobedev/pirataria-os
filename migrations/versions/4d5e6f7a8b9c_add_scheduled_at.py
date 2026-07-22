"""add scheduled_at to atendimentos for calendar event time

Revision ID: 4d5e6f7a8b9c
Revises: 3c4d5e6f7a8b
Create Date: 2026-07-22 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '4d5e6f7a8b9c'
down_revision = '3c4d5e6f7a8b'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'atendimentos' in set(inspector.get_table_names()):
        cols = {c['name'] for c in inspector.get_columns('atendimentos')}
        if 'scheduled_at' not in cols:
            op.add_column('atendimentos', sa.Column('scheduled_at', sa.DateTime(), nullable=True))


def downgrade():
    pass
