from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app import db
from app.models.schemas import Produto, Atendimento
from app.middleware.tenant import inject_studio

financeiro_bp = Blueprint('financeiro', __name__, template_folder='../templates')

@financeiro_bp.before_request
def before_request():
    inject_studio()

@financeiro_bp.route('/')
@login_required
def mensal():
    sid = current_user.studio_id
    ano = request.args.get('ano', datetime.utcnow().year, type=int)

    meses = []
    for mes in range(1, 13):
        receita = db.session.query(
            db.func.coalesce(db.func.sum(Atendimento.valor), 0)
        ).filter(
            Atendimento.studio_id == sid,
            db.func.extract('year', Atendimento.created_at) == ano,
            db.func.extract('month', Atendimento.created_at) == mes
        ).scalar() or 0

        total_atendimentos = db.session.query(
            db.func.count(Atendimento.id)
        ).filter(
            Atendimento.studio_id == sid,
            db.func.extract('year', Atendimento.created_at) == ano,
            db.func.extract('month', Atendimento.created_at) == mes
        ).scalar() or 0

        pix = db.session.query(
            db.func.coalesce(db.func.sum(Atendimento.valor), 0)
        ).filter(
            Atendimento.studio_id == sid,
            Atendimento.forma_pagamento == 'Pix',
            db.func.extract('year', Atendimento.created_at) == ano,
            db.func.extract('month', Atendimento.created_at) == mes
        ).scalar() or 0

        dinheiro = db.session.query(
            db.func.coalesce(db.func.sum(Atendimento.valor), 0)
        ).filter(
            Atendimento.studio_id == sid,
            Atendimento.forma_pagamento == 'Dinheiro',
            db.func.extract('year', Atendimento.created_at) == ano,
            db.func.extract('month', Atendimento.created_at) == mes
        ).scalar() or 0

        cartao = db.session.query(
            db.func.coalesce(db.func.sum(Atendimento.valor), 0)
        ).filter(
            Atendimento.studio_id == sid,
            Atendimento.forma_pagamento.in_(['Cartão', 'Crédito', 'Débito']),
            db.func.extract('year', Atendimento.created_at) == ano,
            db.func.extract('month', Atendimento.created_at) == mes
        ).scalar() or 0

        atendimentos_mes = Atendimento.query.filter(
            Atendimento.studio_id == sid,
            db.func.extract('year', Atendimento.created_at) == ano,
            db.func.extract('month', Atendimento.created_at) == mes
        ).all()

        custo_total = 0
        for at in atendimentos_mes:
            if at.joia_utilizada:
                prod = Produto.query.filter(
                    Produto.studio_id == sid,
                    Produto.nome.ilike(f'%{at.joia_utilizada}%')
                ).first()
                if prod:
                    custo_total += prod.custo

        meses.append({
            'mes': mes,
            'nome_mes': ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
                         'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'][mes-1],
            'atendimentos': total_atendimentos,
            'receita': receita,
            'custo': custo_total,
            'lucro': receita - custo_total,
            'pix': pix,
            'dinheiro': dinheiro,
            'cartao': cartao,
        })

    return render_template('financeiro.html', meses=meses, ano=ano)
