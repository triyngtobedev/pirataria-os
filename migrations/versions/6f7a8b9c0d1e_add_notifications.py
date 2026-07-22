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
        sa.Column('tipo', sa.String(50), nullable=False, server_default=sa.text("'novo_agendamento'")),
        sa.Column('titulo', sa.String(200), nullable=False),
        sa.Column('mensagem', sa.String(500), server_default=sa.text("''")),
        sa.Column('lida', sa.Boolean(), server_default=sa.text('false')),
        sa.Column('link', sa.String(500), server_default=sa.text("''")),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('notifications')
