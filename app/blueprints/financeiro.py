from datetime import datetime, timezone
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.middleware.tenant import inject_studio
from app.services.financeiro_service import FinanceiroService

financeiro_bp = Blueprint('financeiro', __name__, template_folder='../templates')

@financeiro_bp.before_request
def before_request():
    inject_studio()

@financeiro_bp.route('/')
@login_required
def mensal():
    ano = request.args.get('ano', datetime.now(timezone.utc).year, type=int)
    meses = FinanceiroService.relatorio_mensal(current_user.studio_id, ano)
    return render_template('financeiro.html', meses=meses, ano=ano)
