from alembic import op
import sqlalchemy as sa


revision = '6f7a8b9c0d1e'
down_revision = '5e6f7a8b9c0d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('studio_id', sa.Integer(), sa.ForeignKey('studios.id'), nullable=False),
        sa.Column('tipo', sa.String(50), nullable=False, server_default='novo_agendamento'),
        sa.Column('titulo', sa.String(200), nullable=False),
        sa.Column('mensagem', sa.String(500), server_default=''),
        sa.Column('lida', sa.Boolean(), server_default=sa.text('0')),
        sa.Column('link', sa.String(500), server_default=''),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("(datetime('now'))")),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('notifications')
