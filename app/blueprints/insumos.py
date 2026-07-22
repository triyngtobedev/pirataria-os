from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.schemas import Insumo
from app.middleware.tenant import inject_studio

insumos_bp = Blueprint('insumos', __name__, template_folder='../templates')

@insumos_bp.before_request
def before_request():
    inject_studio()

@insumos_bp.route('/')
@login_required
def listar():
    insumos = Insumo.query.filter_by(studio_id=current_user.studio_id)\
        .order_by(Insumo.created_at.desc()).all()
    return render_template('insumos.html', insumos=insumos)

@insumos_bp.route('/adicionar', methods=['POST'])
@login_required
def adicionar():
    nome = request.form.get('nome', '').strip()
    if not nome:
        flash('Nome do insumo é obrigatório.', 'danger')
        return redirect(url_for('insumos.listar'))

    i = Insumo(
        studio_id=current_user.studio_id,
        nome=nome,
        categoria=request.form.get('categoria', '').strip(),
        quantidade=float(request.form.get('quantidade', 0)),
        unidade=request.form.get('unidade', 'unidade').strip(),
        custo_unitario=float(request.form.get('custo_unitario', 0)),
        fornecedor=request.form.get('fornecedor', '').strip(),
        local_fisico=request.form.get('local_fisico', '').strip()
    )
    db.session.add(i)
    db.session.commit()
    flash('Insumo adicionado!', 'success')
    return redirect(url_for('insumos.listar'))

@insumos_bp.route('/editar/<int:id>', methods=['POST'])
@login_required
def editar(id):
    i = Insumo.query.filter_by(id=id, studio_id=current_user.studio_id).first_or_404()
    i.nome = request.form.get('nome', '').strip()
    i.categoria = request.form.get('categoria', '').strip()
    i.quantidade = float(request.form.get('quantidade', 0))
    i.unidade = request.form.get('unidade', 'unidade').strip()
    i.custo_unitario = float(request.form.get('custo_unitario', 0))
    i.fornecedor = request.form.get('fornecedor', '').strip()
    i.local_fisico = request.form.get('local_fisico', '').strip()
    db.session.commit()
    flash('Insumo atualizado!', 'success')
    return redirect(url_for('insumos.listar'))

@insumos_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    i = Insumo.query.filter_by(id=id, studio_id=current_user.studio_id).first_or_404()
    db.session.delete(i)
    db.session.commit()
    flash('Insumo removido.', 'warning')
    return redirect(url_for('insumos.listar'))
