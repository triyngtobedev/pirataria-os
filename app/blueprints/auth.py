import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.middleware.tenant import inject_studio
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.before_request
def before_request():
    inject_studio()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = AuthService.login(email, password)
        if user:
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        current_app.logger.warning(
            'Login failed for %s: user=%s',
            email,
            user  # None if not found or inactive
        )
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

@auth_bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        AuthService.gerar_token_reset(email)
        flash('Se o email existir, enviaremos um link de recuperacao.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot.html')

@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    if request.method == 'POST':
        senha = request.form.get('password', '')
        if len(senha) < 6:
            flash('Senha deve ter no minimo 6 caracteres.', 'danger')
            return render_template('auth/reset.html', token=token)
        sucesso, msg = AuthService.resetar_senha(token, senha)
        flash(msg, 'success' if sucesso else 'danger')
        if sucesso:
            return redirect(url_for('auth.login'))
    return render_template('auth/reset.html', token=token)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard.index'))
