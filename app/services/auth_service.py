from app import db
from app.repositories.user_repo import UserRepository
from app.repositories.activity_log_repo import ActivityLogRepository
from app.seed import seed_studio


class AuthService:

    @staticmethod
    def login(email, password):
        user = UserRepository.find_by_email(email.lower())
        if user and user.is_active and user.check_password(password):
            return user
        return None

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
