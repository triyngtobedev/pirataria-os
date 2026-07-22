from app import db
from app.models.schemas import User, Studio
from .base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def find_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def create_studio_and_user(cls, studio_nome, nome, email, password):
        studio = Studio(nome=studio_nome)
        db.session.add(studio)
        db.session.flush()

        user = User(
            studio_id=studio.id,
            nome=nome,
            email=email.lower(),
            role='admin',
            is_active=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        user.created_by_id = user.id
        return studio, user

    @classmethod
    def find_by_reset_token(cls, token):
        return User.query.filter_by(reset_token=token).first()

    @classmethod
    def list_by_studio(cls, studio_id, active_only=True):
        q = User.query.filter_by(studio_id=studio_id)
        if active_only:
            q = q.filter(User.is_active == True)
        return q.order_by(User.created_at.desc()).all()
