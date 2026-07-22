from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.middleware.tenant import inject_studio
from app.services.dashboard_service import DashboardService

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
    dados = DashboardService.dados(current_user.studio_id)
    return render_template('dashboard.html', **dados)
