from datetime import datetime, timezone
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role:
    ADMIN = 'admin'
    PIERCER = 'piercer'
    RECEPTION = 'reception'
    FINANCIAL = 'financial'

    CHOICES = [ADMIN, PIERCER, RECEPTION, FINANCIAL]

    PERMISSIONS = {
        ADMIN: {'atendimento', 'estoque', 'insumos', 'financeiro', 'dashboard', 'usuarios', 'config'},
        PIERCER: {'atendimento', 'estoque', 'insumos', 'dashboard'},
        RECEPTION: {'atendimento', 'dashboard'},
        FINANCIAL: {'financeiro', 'dashboard'},
    }

    @staticmethod
    def has_permission(role, permission):
        return permission in Role.PERMISSIONS.get(role, set())


class Studio(db.Model):
    __tablename__ = 'studios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    subdomain = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default=Role.ADMIN)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    studio = db.relationship('Studio', backref='users')
    created_by = db.relationship('User', remote_side=[id], backref='created_users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission):
        return Role.has_permission(self.role, permission)

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.is_active = True
        self.deleted_at = None


class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    tipo_joia = db.Column(db.String(100), default='')
    material = db.Column(db.String(100), default='')
    local_aplicacao = db.Column(db.String(100), default='')
    quantidade = db.Column(db.Integer, default=0)
    custo = db.Column(db.Float, default=0.0)
    valor_venda = db.Column(db.Float, default=0.0)
    local_fisico = db.Column(db.String(200), default='')
    foto = db.Column(db.String(500), default='')
    favorito = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    studio = db.relationship('Studio', backref='produtos')
    created_by = db.relationship('User', foreign_keys=[created_by_id])

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.is_active = True
        self.deleted_at = None


class Atendimento(db.Model):
    __tablename__ = 'atendimentos'
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    cliente = db.Column(db.String(200), nullable=False)
    procedimento = db.Column(db.String(200), default='')
    joia_utilizada = db.Column(db.String(200), default='')
    valor = db.Column(db.Float, default=0.0)
    forma_pagamento = db.Column(db.String(50), default='')
    piercer = db.Column(db.String(200), default='')
    status = db.Column(db.String(50), default='Pago')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    google_event_id = db.Column(db.String(500), nullable=True)
    scheduled_at = db.Column(db.DateTime, nullable=True)

    studio = db.relationship('Studio', backref='atendimentos')
    created_by = db.relationship('User', foreign_keys=[created_by_id])

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.is_active = True
        self.deleted_at = None


class Insumo(db.Model):
    __tablename__ = 'insumos'
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), default='')
    quantidade = db.Column(db.Float, default=0)
    unidade = db.Column(db.String(50), default='unidade')
    custo_unitario = db.Column(db.Float, default=0.0)
    fornecedor = db.Column(db.String(200), default='')
    local_fisico = db.Column(db.String(200), default='')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    studio = db.relationship('Studio', backref='insumos')
    created_by = db.relationship('User', foreign_keys=[created_by_id])

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.is_active = True
        self.deleted_at = None


class StockMovement(db.Model):
    __tablename__ = 'stock_movements'
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    saldo_anterior = db.Column(db.Integer, nullable=False)
    saldo_posterior = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(500), default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    studio = db.relationship('Studio', backref='stock_movements')
    produto = db.relationship('Produto', backref='stock_movements')
    created_by = db.relationship('User', foreign_keys=[created_by_id])


class CalendarIntegration(db.Model):
    __tablename__ = 'calendar_integrations'
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False, unique=True)
    access_token = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.Text, nullable=False)
    token_expiry = db.Column(db.DateTime, nullable=True)
    calendar_id = db.Column(db.String(500), nullable=True)
    tasks_list_id = db.Column(db.String(500), nullable=True)
    google_email = db.Column(db.String(200), nullable=True)
    last_sync_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    acao = db.Column(db.String(100), nullable=False)
    entidade = db.Column(db.String(100), nullable=False)
    entidade_id = db.Column(db.Integer, nullable=True)
    descricao = db.Column(db.String(500), default='')
    detalhes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    studio = db.relationship('Studio', backref='activity_logs')
    user = db.relationship('User', foreign_keys=[user_id])


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False, default='novo_agendamento')
    titulo = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.String(500), default='')
    lida = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(500), default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    studio = db.relationship('Studio', backref='notifications')


class PushSubscription(db.Model):
    __tablename__ = 'push_subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    endpoint = db.Column(db.Text, nullable=False)
    p256dh = db.Column(db.String(500), nullable=False)
    auth = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    studio = db.relationship('Studio', backref='push_subscriptions')
    user = db.relationship('User', backref='push_subscriptions')


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
