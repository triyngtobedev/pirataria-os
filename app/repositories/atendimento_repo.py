from datetime import datetime, date
from app import db
from app.models.schemas import Atendimento
from .base import BaseRepository


class AtendimentoRepository(BaseRepository):
    model = Atendimento

    @classmethod
    def listar_hoje(cls, studio_id):
        hoje = date.today()
        return Atendimento.query.filter(
            Atendimento.studio_id == studio_id,
            Atendimento.is_active == True,
            db.func.date(Atendimento.created_at) == hoje
        ).order_by(Atendimento.created_at.desc()).all()

    @classmethod
    def resumo_dia(cls, studio_id):
        hoje = date.today()
        return db.session.query(
            db.func.coalesce(db.func.sum(Atendimento.valor), 0).label('faturamento'),
            db.func.count(Atendimento.id).label('procedimentos'),
            db.func.coalesce(db.func.sum(db.case(
                (Atendimento.forma_pagamento == 'Pix', Atendimento.valor), else_=0
            )), 0).label('total_pix'),
            db.func.coalesce(db.func.sum(db.case(
                (Atendimento.forma_pagamento == 'Dinheiro', Atendimento.valor), else_=0
            )), 0).label('total_dinheiro'),
            db.func.coalesce(db.func.sum(db.case(
                (Atendimento.forma_pagamento.in_(['Cartão', 'Crédito', 'Débito']), Atendimento.valor), else_=0
            )), 0).label('total_cartao'),
            db.func.count(db.func.distinct(Atendimento.cliente)).label('clientes_novos'),
        ).filter(
            Atendimento.studio_id == studio_id,
            Atendimento.is_active == True,
            db.func.date(Atendimento.created_at) == hoje
        ).first()

    @classmethod
    def resumo_mes(cls, studio_id):
        hoje = date.today()
        primeiro_dia = hoje.replace(day=1)
        return db.session.query(
            db.func.coalesce(db.func.sum(Atendimento.valor), 0).label('faturamento'),
            db.func.count(Atendimento.id).label('procedimentos'),
            db.func.count(db.func.distinct(Atendimento.cliente)).label('clientes'),
        ).filter(
            Atendimento.studio_id == studio_id,
            Atendimento.is_active == True,
            Atendimento.created_at >= primeiro_dia
        ).first()

    @classmethod
    def total_por_mes(cls, studio_id, ano, mes):
        row = db.session.query(
            db.func.coalesce(db.func.sum(Atendimento.valor), 0).label('receita'),
            db.func.count(Atendimento.id).label('total'),
            db.func.coalesce(db.func.sum(db.case(
                (Atendimento.forma_pagamento == 'Pix', Atendimento.valor), else_=0
            )), 0).label('pix'),
            db.func.coalesce(db.func.sum(db.case(
                (Atendimento.forma_pagamento == 'Dinheiro', Atendimento.valor), else_=0
            )), 0).label('dinheiro'),
            db.func.coalesce(db.func.sum(db.case(
                (Atendimento.forma_pagamento.in_(['Cartão', 'Crédito', 'Débito']), Atendimento.valor), else_=0
            )), 0).label('cartao'),
        ).filter(
            Atendimento.studio_id == studio_id,
            Atendimento.is_active == True,
            db.func.extract('year', Atendimento.created_at) == ano,
            db.func.extract('month', Atendimento.created_at) == mes
        ).first()

        atendimentos = Atendimento.query.filter(
            Atendimento.studio_id == studio_id,
            Atendimento.is_active == True,
            db.func.extract('year', Atendimento.created_at) == ano,
            db.func.extract('month', Atendimento.created_at) == mes
        ).all()

        return row, atendimentos
