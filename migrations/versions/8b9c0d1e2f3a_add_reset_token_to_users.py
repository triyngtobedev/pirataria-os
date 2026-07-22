from alembic import op
import sqlalchemy as sa


revision = '8b9c0d1e2f3a'
down_revision = '7a8b9c0d1e2f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('reset_token', sa.String(200), nullable=True, unique=True))
    op.add_column('users', sa.Column('reset_token_expiry', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('users', 'reset_token_expiry')
    op.drop_column('users', 'reset_token')
