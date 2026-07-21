from datetime import datetime, date
from flask import Blueprint, render_template, g
from flask_login import login_required, current_user
from app import db
from app.models.schemas import Produto, Atendimento
from app.middleware.tenant import inject_studio

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates')

@dashboard_bp.before_request
def before_request():
    inject_studio()

@dashboard_bp.route('/')
@login_required
def index():
    hoje = date.today()
    sid = current_user.studio_id

    resumo = db.session.query(
        db.func.coalesce(db.func.sum(Atendimento.valor), 0).label('faturamento'),
        db.func.count(Atendimento.id).label('procedimentos'),
        db.func.coalesce(db.func.sum(db.case((Atendimento.forma_pagamento == 'Pix', Atendimento.valor), else_=0)), 0).label('total_pix'),
        db.func.coalesce(db.func.sum(db.case((Atendimento.forma_pagamento == 'Dinheiro', Atendimento.valor), else_=0)), 0).label('total_dinheiro'),
        db.func.coalesce(db.func.sum(db.case((Atendimento.forma_pagamento == 'Cartão', Atendimento.valor), else_=0)), 0).label('total_cartao'),
    ).filter(
        Atendimento.studio_id == sid,
        db.func.date(Atendimento.created_at) == hoje
    ).first()

    clientes_novos = db.session.query(
        db.func.count(db.func.distinct(Atendimento.cliente))
    ).filter(
        Atendimento.studio_id == sid,
        db.func.date(Atendimento.created_at) == hoje
    ).scalar() or 0

    baixo = Produto.query.filter(
        Produto.studio_id == sid,
        Produto.quantidade <= 3
    ).order_by(Produto.quantidade).all()

    atendimentos_hoje = Atendimento.query.filter(
        Atendimento.studio_id == sid,
        db.func.date(Atendimento.created_at) == hoje
    ).order_by(Atendimento.created_at.desc()).all()

    return render_template('dashboard.html',
        faturamento=resumo.faturamento,
        procedimentos=resumo.procedimentos,
        total_pix=resumo.total_pix,
        total_dinheiro=resumo.total_dinheiro,
        total_cartao=resumo.total_cartao,
        clientes_novos=clientes_novos,
        estoque_baixo=baixo,
        atendimentos_hoje=atendimentos_hoje,
        hoje_data=hoje.strftime('%d/%m/%Y'))
