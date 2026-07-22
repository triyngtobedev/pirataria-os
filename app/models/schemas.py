from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Studio(db.Model):
    __tablename__ = 'studios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    subdomain = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    studio = db.relationship('Studio', backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    studio = db.relationship('Studio', backref='produtos')

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    studio = db.relationship('Studio', backref='atendimentos')

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    studio = db.relationship('Studio', backref='insumos')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
