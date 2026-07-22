"""fix existing users: set is_active and role defaults

Revision ID: 1a2b3c4d5e6f
Revises: 054f3d2b6a1c
Create Date: 2026-07-22 08:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '1a2b3c4d5e6f'
down_revision = '054f3d2b6a1c'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    users_cols = {c['name'] for c in inspector.get_columns('users')}

    if 'is_active' in users_cols:
        op.execute("UPDATE users SET is_active = TRUE WHERE is_active IS NULL")
    if 'role' in users_cols:
        op.execute("UPDATE users SET role = 'admin' WHERE role IS NULL")


def downgrade():
    pass
