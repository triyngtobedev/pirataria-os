from app import db


class BaseRepository:
    model = None

    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls.model, id)

    @classmethod
    def get_active_by_id(cls, id, studio_id=None):
        q = cls.model.query.filter(cls.model.id == id, cls.model.is_active == True)
        if studio_id is not None and hasattr(cls.model, 'studio_id'):
            q = q.filter(cls.model.studio_id == studio_id)
        return q.first()

    @classmethod
    def get_by_id_and_studio(cls, id, studio_id):
        return cls.model.query.filter_by(id=id, studio_id=studio_id).first()

    @classmethod
    def list_by_studio(cls, studio_id, active_only=True, order_by=None):
        q = cls.model.query.filter_by(studio_id=studio_id)
        if active_only and hasattr(cls.model, 'is_active'):
            q = q.filter(cls.model.is_active == True)
        if order_by is not None:
            q = q.order_by(order_by)
        else:
            q = q.order_by(cls.model.created_at.desc())
        return q.all()

    @classmethod
    def create(cls, **kwargs):
        obj = cls.model(**kwargs)
        db.session.add(obj)
        return obj

    @classmethod
    def save(cls):
        db.session.commit()

    @classmethod
    def soft_delete(cls, obj):
        if hasattr(obj, 'soft_delete'):
            obj.soft_delete()
            db.session.commit()
            return True
        return False

    @classmethod
    def hard_delete(cls, obj):
        db.session.delete(obj)
        db.session.commit()
