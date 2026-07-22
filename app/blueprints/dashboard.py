from datetime import datetime, date
from flask import Blueprint, render_template, g, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.schemas import Produto, Atendimento
from app.middleware.tenant import inject_studio
from app.quotes import quote_of_the_day

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates')

@dashboard_bp.before_request
def before_request():
    inject_studio()

@dashboard_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('landing/home.html')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    hoje = date.today()
    sid = current_user.studio_id
    primeiro_dia_mes = hoje.replace(day=1)
    quote = quote_of_the_day()

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

    resumo_mes = db.session.query(
        db.func.coalesce(db.func.sum(Atendimento.valor), 0).label('faturamento'),
        db.func.count(Atendimento.id).label('procedimentos'),
        db.func.count(db.func.distinct(Atendimento.cliente)).label('clientes'),
    ).filter(
        Atendimento.studio_id == sid,
        Atendimento.created_at >= primeiro_dia_mes
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

    total_produtos = Produto.query.filter_by(studio_id=sid).count()

    return render_template('dashboard.html',
        quote=quote,
        faturamento=resumo.faturamento,
        procedimentos=resumo.procedimentos,
        total_pix=resumo.total_pix,
        total_dinheiro=resumo.total_dinheiro,
        total_cartao=resumo.total_cartao,
        clientes_novos=clientes_novos,
        estoque_baixo=baixo,
        atendimentos_hoje=atendimentos_hoje,
        hoje_data=hoje.strftime('%d/%m/%Y'),
        mes_faturamento=resumo_mes.faturamento,
        mes_procedimentos=resumo_mes.procedimentos,
        mes_clientes=resumo_mes.clientes,
        total_produtos=total_produtos)
