"""sync all tables with missing columns

Revision ID: 054f3d2b6a1c
Revises: d13eba4077c9
Create Date: 2026-07-22 07:55:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '054f3d2b6a1c'
down_revision = 'd13eba4077c9'
branch_labels = None
depends_on = None


EXPECTED_COLUMNS = {
    'studios': [
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=200), nullable=False),
        sa.Column('subdomain', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    ],
    'users': [
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('studio_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=False),
        sa.Column('password_hash', sa.String(length=200), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
    ],
    'activity_logs': [
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('studio_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('acao', sa.String(length=100), nullable=False),
        sa.Column('entidade', sa.String(length=100), nullable=False),
        sa.Column('entidade_id', sa.Integer(), nullable=True),
        sa.Column('descricao', sa.String(length=500), nullable=True),
        sa.Column('detalhes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    ],
    'atendimentos': [
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('studio_id', sa.Integer(), nullable=False),
        sa.Column('cliente', sa.String(length=200), nullable=False),
        sa.Column('procedimento', sa.String(length=200), nullable=True),
        sa.Column('joia_utilizada', sa.String(length=200), nullable=True),
        sa.Column('valor', sa.Float(), nullable=True),
        sa.Column('forma_pagamento', sa.String(length=50), nullable=True),
        sa.Column('piercer', sa.String(length=200), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
    ],
    'insumos': [
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('studio_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=200), nullable=False),
        sa.Column('categoria', sa.String(length=100), nullable=True),
        sa.Column('quantidade', sa.Float(), nullable=True),
        sa.Column('unidade', sa.String(length=50), nullable=True),
        sa.Column('custo_unitario', sa.Float(), nullable=True),
        sa.Column('fornecedor', sa.String(length=200), nullable=True),
        sa.Column('local_fisico', sa.String(length=200), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
    ],
    'produtos': [
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('studio_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=200), nullable=False),
        sa.Column('tipo_joia', sa.String(length=100), nullable=True),
        sa.Column('material', sa.String(length=100), nullable=True),
        sa.Column('local_aplicacao', sa.String(length=100), nullable=True),
        sa.Column('quantidade', sa.Integer(), nullable=True),
        sa.Column('custo', sa.Float(), nullable=True),
        sa.Column('valor_venda', sa.Float(), nullable=True),
        sa.Column('local_fisico', sa.String(length=200), nullable=True),
        sa.Column('foto', sa.String(length=500), nullable=True),
        sa.Column('favorito', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
    ],
    'stock_movements': [
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('studio_id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column('saldo_anterior', sa.Integer(), nullable=False),
        sa.Column('saldo_posterior', sa.Integer(), nullable=False),
        sa.Column('motivo', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
    ],
}


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    for table_name, expected_cols in EXPECTED_COLUMNS.items():
        if table_name not in existing_tables:
            print(f"[migration] Skipping {table_name} — table does not exist yet")
            continue

        existing = {c['name']: c for c in inspector.get_columns(table_name)}
        for col in expected_cols:
            if col.name not in existing:
                print(f"[migration] Adding column {table_name}.{col.name}")
                op.add_column(table_name, col)

    op.execute("UPDATE users SET is_active = TRUE WHERE is_active IS NULL")
    op.execute("UPDATE users SET role = 'admin' WHERE role IS NULL")


def downgrade():
    pass
