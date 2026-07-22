from alembic import op
import sqlalchemy as sa


revision = '7a8b9c0d1e2f'
down_revision = '6f7a8b9c0d1e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('push_subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('studio_id', sa.Integer(), sa.ForeignKey('studios.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('endpoint', sa.Text(), nullable=False),
        sa.Column('p256dh', sa.String(500), nullable=False),
        sa.Column('auth', sa.String(500), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('push_subscriptions')
