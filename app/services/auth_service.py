import logging

from app import db
from app.repositories.user_repo import UserRepository
from app.repositories.activity_log_repo import ActivityLogRepository
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
