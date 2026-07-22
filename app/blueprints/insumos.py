from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.middleware.tenant import inject_studio
from app.services.insumo_service import InsumoService

insumos_bp = Blueprint('insumos', __name__, template_folder='../templates')

@insumos_bp.before_request
def before_request():
    inject_studio()

@insumos_bp.route('/')
@login_required
def listar():
    insumos = InsumoService.listar(current_user.studio_id)
    return render_template('insumos.html', insumos=insumos)

@insumos_bp.route('/adicionar', methods=['POST'])
@login_required
def adicionar():
    nome = request.form.get('nome', '').strip()
    if not nome:
        flash('Nome do insumo é obrigatório.', 'danger')
        return redirect(url_for('insumos.listar'))

    dados = {
        'nome': nome,
        'categoria': request.form.get('categoria', '').strip(),
        'quantidade': float(request.form.get('quantidade', 0)),
        'unidade': request.form.get('unidade', 'unidade').strip(),
        'custo_unitario': float(request.form.get('custo_unitario', 0)),
        'fornecedor': request.form.get('fornecedor', '').strip(),
        'local_fisico': request.form.get('local_fisico', '').strip(),
    }

    InsumoService.criar(current_user.studio_id, dados, user_id=current_user.id)
    flash('Insumo adicionado!', 'success')
    return redirect(url_for('insumos.listar'))

@insumos_bp.route('/editar/<int:id>', methods=['POST'])
@login_required
def editar(id):
    dados = {
        'nome': request.form.get('nome', '').strip(),
        'categoria': request.form.get('categoria', '').strip(),
        'quantidade': float(request.form.get('quantidade', 0)),
        'unidade': request.form.get('unidade', 'unidade').strip(),
        'custo_unitario': float(request.form.get('custo_unitario', 0)),
        'fornecedor': request.form.get('fornecedor', '').strip(),
        'local_fisico': request.form.get('local_fisico', '').strip(),
    }

    result = InsumoService.atualizar(id, dados, user_id=current_user.id)
    if result:
        flash('Insumo atualizado!', 'success')
    else:
        flash('Insumo não encontrado.', 'danger')
    return redirect(url_for('insumos.listar'))

@insumos_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    InsumoService.excluir(id, user_id=current_user.id)
    flash('Insumo removido.', 'warning')
    return redirect(url_for('insumos.listar'))
