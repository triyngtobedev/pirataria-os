import os
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.middleware.tenant import inject_studio
from app.services.produto_service import ProdutoService
from app.services.stock_service import StockService
from app.services.activity_service import ActivityService

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_MIMES = {'image/png', 'image/jpeg', 'image/gif', 'image/webp'}

def _validar_foto(file):
    if not file or not file.filename:
        return ''
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in ALLOWED_EXT:
        return ''

    file.seek(0)
    import magic
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    if mime not in ALLOWED_MIMES:
        return ''

    nome = secure_filename(f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{file.filename}")
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, nome))
    return nome

estoque_bp = Blueprint('estoque', __name__, template_folder='../templates')

@estoque_bp.before_request
def before_request():
    inject_studio()

@estoque_bp.route('/')
@login_required
def listar():
    fav = request.args.get('fav')
    produtos = ProdutoService.listar(current_user.studio_id, favoritos_only=bool(fav))
    historico = StockService.historico(current_user.studio_id)
    return render_template('estoque.html', produtos=produtos, historico=historico)

@estoque_bp.route('/adicionar', methods=['POST'])
@login_required
def adicionar():
    nome = request.form.get('nome', '').strip()
    if not nome:
        flash('Nome do produto é obrigatório.', 'danger')
        return redirect(url_for('estoque.listar'))

    dados = {
        'nome': nome,
        'tipo_joia': request.form.get('tipo_joia', '').strip(),
        'material': request.form.get('material', '').strip(),
        'local_aplicacao': request.form.get('local_aplicacao', '').strip(),
        'quantidade': int(request.form.get('quantidade', 0)),
        'custo': float(request.form.get('custo', 0)),
        'valor_venda': float(request.form.get('valor_venda', 0)),
        'local_fisico': request.form.get('local_fisico', '').strip(),
    }

    foto = _validar_foto(request.files.get('foto'))
    ProdutoService.criar(
        current_user.studio_id, dados,
        foto=foto, user_id=current_user.id
    )
    flash('Produto adicionado!', 'success')
    return redirect(url_for('estoque.listar'))

@estoque_bp.route('/editar/<int:id>', methods=['POST'])
@login_required
def editar(id):
    p = ProdutoService.get_by_id(id)
    if not p or p.studio_id != current_user.studio_id:
        flash('Produto não encontrado.', 'danger')
        return redirect(url_for('estoque.listar'))

    dados = {
        'nome': request.form.get('nome', '').strip(),
        'tipo_joia': request.form.get('tipo_joia', '').strip(),
        'material': request.form.get('material', '').strip(),
        'local_aplicacao': request.form.get('local_aplicacao', '').strip(),
        'local_fisico': request.form.get('local_fisico', '').strip(),
    }

    qtde = int(request.form.get('quantidade', 0))
    if qtde != p.quantidade:
        StockService.ajuste(
            current_user.studio_id, p.id, qtde,
            motivo='Edição manual',
            created_by_id=current_user.id
        )
    else:
        p.custo = float(request.form.get('custo', 0))
        p.valor_venda = float(request.form.get('valor_venda', 0))

    foto = _validar_foto(request.files.get('foto'))
    ProdutoService.atualizar(id, dados, foto=foto, user_id=current_user.id)
    flash('Produto atualizado!', 'success')
    return redirect(url_for('estoque.listar'))

@estoque_bp.route('/favoritar/<int:id>')
@login_required
def favoritar(id):
    p = ProdutoService.get_by_id(id)
    if p and p.studio_id == current_user.studio_id:
        ProdutoService.favoritar(id)
    return redirect(url_for('estoque.listar'))

@estoque_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    p = ProdutoService.get_by_id(id)
    if p and p.studio_id == current_user.studio_id:
        ProdutoService.excluir(id, user_id=current_user.id)
        flash('Produto removido.', 'warning')
    return redirect(url_for('estoque.listar'))
