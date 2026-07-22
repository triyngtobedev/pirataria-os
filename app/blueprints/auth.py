from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = AuthService.login(email, password)
        if user:
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        flash('Email ou senha inválidos.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if len(password) < 6:
            flash('Senha deve ter no mínimo 6 caracteres.', 'danger')
            return render_template('auth/register.html')

        user, error = AuthService.register(
            studio_nome=request.form.get('studio_nome', '').strip(),
            nome=request.form.get('nome', '').strip(),
            email=email,
            password=password,
        )
        if user:
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        flash(error or 'Erro ao cadastrar.', 'danger')
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard.index'))
