from app.models.schemas import Insumo
from .base import BaseRepository


class InsumoRepository(BaseRepository):
    model = Insumo
