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
    try:
        op.add_column('users', sa.Column('role', sa.String(length=50), nullable=True))
    except Exception:
        pass


def downgrade():
    try:
        op.drop_column('users', 'role')
    except Exception:
        pass
