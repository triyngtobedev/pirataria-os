import logging
import secrets
from datetime import datetime, timedelta, timezone

from flask import current_app, url_for

from app import db
from app.repositories.user_repo import UserRepository
from app.repositories.activity_log_repo import ActivityLogRepository
from app.services.email_service import enviar_email
from app.seed import seed_studio

logger = logging.getLogger(__name__)


class AuthService:

    @staticmethod
    def login(email, password):
        user = UserRepository.find_by_email(email.lower())
        if not user:
            logger.warning('Login failed: user not found for %s', email)
            return None
        if not user.is_active:
            logger.warning('Login failed: user %s is inactive (is_active=%s)', email, user.is_active)
            return None
        if not user.check_password(password):
            logger.warning('Login failed: wrong password for %s', email)
            return None
        return user

    @staticmethod
    def register(studio_nome, nome, email, password):
        existing = UserRepository.find_by_email(email.lower())
        if existing:
            return None, 'Email já cadastrado.'

        studio, user = UserRepository.create_studio_and_user(
            studio_nome=studio_nome,
            nome=nome,
            email=email,
            password=password,
        )
        db.session.commit()

        seed_studio(studio.id)

        return user, None

    @staticmethod
    def gerar_token_reset(email):
        user = UserRepository.find_by_email(email.lower())
        if not user:
            return False
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
        db.session.commit()

        link = url_for('auth.reset', token=token, _external=True)
        assunto = 'Recuperacao de senha - Pirataria OS'
        corpo = f"""
        <h2>Recuperacao de senha</h2>
        <p>Clique no link abaixo para redefinir sua senha:</p>
        <p><a href="{link}">{link}</a></p>
        <p>Este link expira em 1 hora.</p>
        <p>Se voce nao solicitou esta recuperacao, ignore este email.</p>
        """
        enviar_email(email, assunto, corpo)
        return True

    @staticmethod
    def resetar_senha(token, nova_senha):
        user = UserRepository.find_by_reset_token(token)
        if not user:
            return False, 'Token invalido.'
        if user.reset_token_expiry is None or user.reset_token_expiry.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return False, 'Token expirado.'
        user.set_password(nova_senha)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
        return True, 'Senha redefinida com sucesso!'
