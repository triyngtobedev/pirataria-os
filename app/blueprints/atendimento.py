from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.schemas import Produto, Atendimento
from app.middleware.tenant import inject_studio

atendimento_bp = Blueprint('atendimento', __name__, template_folder='../templates')

@atendimento_bp.before_request
def before_request():
    inject_studio()

@atendimento_bp.route('/')
@login_required
def listar():
    sid = current_user.studio_id
    atendimentos = Atendimento.query.filter_by(studio_id=sid)\
        .order_by(Atendimento.created_at.desc()).all()
    produtos = Produto.query.filter_by(studio_id=sid).order_by(Produto.nome).all()
    return render_template('atendimento.html', atendimentos=atendimentos, produtos=produtos)

@atendimento_bp.route('/novo', methods=['POST'])
@login_required
def novo():
    cliente = request.form.get('cliente', '').strip()
    if not cliente:
        flash('Nome do cliente é obrigatório.', 'danger')
        return redirect(url_for('atendimento.listar'))

    sid = current_user.studio_id
    joia = request.form.get('joia_utilizada', '').strip()

    a = Atendimento(
        studio_id=sid,
        cliente=cliente,
        procedimento=request.form.get('procedimento', '').strip(),
        joia_utilizada=joia,
        valor=float(request.form.get('valor', 0)),
        forma_pagamento=request.form.get('forma_pagamento', '').strip(),
        piercer=request.form.get('piercer', '').strip(),
        status='Pago'
    )
    db.session.add(a)

    if joia:
        produto = Produto.query.filter(
            Produto.studio_id == sid,
            Produto.nome.ilike(f'%{joia}%')
        ).first()
        if produto and produto.quantidade > 0:
            produto.quantidade -= 1

    db.session.commit()
    flash('Atendimento registrado!', 'success')
    return redirect(url_for('atendimento.listar'))

@atendimento_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    a = Atendimento.query.filter_by(id=id, studio_id=current_user.studio_id).first_or_404()
    db.session.delete(a)
    db.session.commit()
    flash('Atendimento removido.', 'warning')
    return redirect(url_for('atendimento.listar'))
