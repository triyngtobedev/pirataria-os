import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.schemas import Produto
from app.middleware.tenant import inject_studio

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def _salvar_foto(file):
    if file and file.filename:
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext in ALLOWED_EXT:
            nome = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, nome))
            return nome
    return ''

estoque_bp = Blueprint('estoque', __name__, template_folder='../templates')

@estoque_bp.before_request
def before_request():
    inject_studio()

@estoque_bp.route('/')
@login_required
def listar():
    produtos = Produto.query.filter_by(studio_id=current_user.studio_id)\
        .order_by(Produto.created_at.desc()).all()
    return render_template('estoque.html', produtos=produtos)

@estoque_bp.route('/adicionar', methods=['POST'])
@login_required
def adicionar():
    nome = request.form.get('nome', '').strip()
    if not nome:
        flash('Nome do produto é obrigatório.', 'danger')
        return redirect(url_for('estoque.listar'))

    p = Produto(
        studio_id=current_user.studio_id,
        nome=nome,
        tipo_joia=request.form.get('tipo_joia', '').strip(),
        material=request.form.get('material', '').strip(),
        local_aplicacao=request.form.get('local_aplicacao', '').strip(),
        quantidade=int(request.form.get('quantidade', 0)),
        custo=float(request.form.get('custo', 0)),
        valor_venda=float(request.form.get('valor_venda', 0)),
        local_fisico=request.form.get('local_fisico', '').strip(),
        foto=_salvar_foto(request.files.get('foto'))
    )
    db.session.add(p)
    db.session.commit()
    flash('Produto adicionado!', 'success')
    return redirect(url_for('estoque.listar'))

@estoque_bp.route('/editar/<int:id>', methods=['POST'])
@login_required
def editar(id):
    p = Produto.query.filter_by(id=id, studio_id=current_user.studio_id).first_or_404()
    p.nome = request.form.get('nome', '').strip()
    p.tipo_joia = request.form.get('tipo_joia', '').strip()
    p.material = request.form.get('material', '').strip()
    p.local_aplicacao = request.form.get('local_aplicacao', '').strip()
    p.quantidade = int(request.form.get('quantidade', 0))
    p.custo = float(request.form.get('custo', 0))
    p.valor_venda = float(request.form.get('valor_venda', 0))
    p.local_fisico = request.form.get('local_fisico', '').strip()
    foto = _salvar_foto(request.files.get('foto'))
    if foto:
        p.foto = foto
    db.session.commit()
    flash('Produto atualizado!', 'success')
    return redirect(url_for('estoque.listar'))

@estoque_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    p = Produto.query.filter_by(id=id, studio_id=current_user.studio_id).first_or_404()
    db.session.delete(p)
    db.session.commit()
    flash('Produto removido.', 'warning')
    return redirect(url_for('estoque.listar'))
