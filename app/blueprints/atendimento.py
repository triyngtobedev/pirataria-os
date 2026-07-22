from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.middleware.tenant import inject_studio
from app.services.atendimento_service import AtendimentoService

atendimento_bp = Blueprint('atendimento', __name__, template_folder='../templates')

@atendimento_bp.before_request
def before_request():
    inject_studio()

@atendimento_bp.route('/')
@login_required
def listar():
    atendimentos = AtendimentoService.listar(current_user.studio_id)
    produtos = AtendimentoService.listar_produtos(current_user.studio_id)
    return render_template('atendimento.html', atendimentos=atendimentos, produtos=produtos)

@atendimento_bp.route('/novo', methods=['POST'])
@login_required
def novo():
    cliente = request.form.get('cliente', '').strip()
    if not cliente:
        flash('Nome do cliente é obrigatório.', 'danger')
        return redirect(url_for('atendimento.listar'))

    scheduled_raw = request.form.get('scheduled_at', '').strip()
    scheduled_at = None
    if scheduled_raw:
        try:
            scheduled_at = datetime.fromisoformat(scheduled_raw)
        except (ValueError, TypeError):
            pass

    dados = {
        'cliente': cliente,
        'procedimento': request.form.get('procedimento', '').strip(),
        'joia_utilizada': request.form.get('joia_utilizada', '').strip(),
        'valor': float(request.form.get('valor', 0)),
        'forma_pagamento': request.form.get('forma_pagamento', '').strip(),
        'piercer': request.form.get('piercer', '').strip(),
        'status': 'Pago',
        'scheduled_at': scheduled_at,
    }

    AtendimentoService.registrar(
        current_user.studio_id, dados,
        user_id=current_user.id
    )

    flash('Atendimento registrado!', 'success')
    return redirect(url_for('atendimento.listar'))

@atendimento_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    AtendimentoService.excluir(id, user_id=current_user.id)
    flash('Atendimento removido.', 'warning')
    return redirect(url_for('atendimento.listar'))
