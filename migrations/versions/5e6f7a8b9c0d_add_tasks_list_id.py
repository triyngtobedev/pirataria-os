"""add tasks_list_id to calendar_integrations

Revision ID: 5e6f7a8b9c0d
Revises: 4d5e6f7a8b9c
Create Date: 2026-07-22 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '5e6f7a8b9c0d'
down_revision = '4d5e6f7a8b9c'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'calendar_integrations' in set(inspector.get_table_names()):
        cols = {c['name'] for c in inspector.get_columns('calendar_integrations')}
        if 'tasks_list_id' not in cols:
            op.add_column('calendar_integrations', sa.Column('tasks_list_id', sa.String(500), nullable=True))


def downgrade():
    pass
