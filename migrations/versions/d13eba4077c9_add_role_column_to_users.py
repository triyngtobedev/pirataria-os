"""add role column to users

Revision ID: d13eba4077c9
Revises: 0f225bf89d71
Create Date: 2026-07-22 07:05:46.298746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd13eba4077c9'
down_revision = '0f225bf89d71'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('users')]
    if 'role' not in columns:
        op.add_column('users', sa.Column('role', sa.String(length=50), nullable=True))


def downgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('users')]
    if 'role' in columns:
        op.drop_column('users', 'role')
