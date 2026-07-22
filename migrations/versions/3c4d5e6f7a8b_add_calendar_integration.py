"""add calendar_integrations table + google_event_id to atendimentos

Revision ID: 3c4d5e6f7a8b
Revises: 2b3c4d5e6f7a
Create Date: 2026-07-22 08:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '3c4d5e6f7a8b'
down_revision = '2b3c4d5e6f7a'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = set(inspector.get_table_names())

    if 'calendar_integrations' not in tables:
        op.create_table('calendar_integrations',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('studio_id', sa.Integer(), nullable=False),
            sa.Column('access_token', sa.Text(), nullable=False),
            sa.Column('refresh_token', sa.Text(), nullable=False),
            sa.Column('token_expiry', sa.DateTime(), nullable=True),
            sa.Column('calendar_id', sa.String(length=500), nullable=True),
            sa.Column('google_email', sa.String(length=200), nullable=True),
            sa.Column('last_sync_at', sa.DateTime(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['studio_id'], ['studios.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('studio_id')
        )

    if 'atendimentos' in tables:
        cols = {c['name'] for c in inspector.get_columns('atendimentos')}
        if 'google_event_id' not in cols:
            op.add_column('atendimentos', sa.Column('google_event_id', sa.String(length=500), nullable=True))


def downgrade():
    pass
