import logging
from datetime import datetime, timezone
from flask import current_app

from app import db
from app.models.schemas import CalendarIntegration
from app.repositories.atendimento_repo import AtendimentoRepository
from app.repositories.produto_repo import ProdutoRepository
from app.repositories.stock_movement_repo import StockMovementRepository
from app.services.activity_service import ActivityService
from app.services.notification_service import NotificationService
from app.services import google_service

logger = logging.getLogger(__name__)


class AtendimentoService:

    @staticmethod
    def listar(studio_id):
        return AtendimentoRepository.list_by_studio(studio_id)

    @staticmethod
    def listar_produtos(studio_id):
        return ProdutoRepository.list_by_studio(studio_id)

    @staticmethod
    def registrar(studio_id, dados, user_id=None):
        a = AtendimentoRepository.create(studio_id=studio_id, **dados)
        db.session.flush()

        joia = dados.get('joia_utilizada', '')
        if joia:
            produto = ProdutoRepository.find_by_name(studio_id, joia)
            if produto and produto.quantidade > 0:
                saldo_anterior = produto.quantidade
                produto.quantidade -= 1

                StockMovementRepository.registrar(
                    studio_id=studio_id,
                    produto_id=produto.id,
                    tipo='saida',
                    quantidade=1,
                    saldo_anterior=saldo_anterior,
                    saldo_posterior=produto.quantidade,
                    motivo=f'Atendimento: {dados.get("cliente", "")}',
                    created_by_id=user_id,
                )

        db.session.commit()

        ActivityService.log(
            studio_id=studio_id, user_id=user_id,
            acao='criar', entidade='atendimento', entidade_id=a.id,
            descricao=f'Atendimento de {dados.get("cliente", "")} - R$ {dados.get("valor", 0)}'
        )

        _sync_create_event(a)

        if a.scheduled_at and a.scheduled_at > datetime.now(timezone.utc).replace(tzinfo=None):
            NotificationService.criar(
                studio_id=studio_id,
                tipo='novo_agendamento',
                titulo=f'Novo agendamento: {a.cliente}',
                mensagem=f'{a.procedimento or "Procedimento"} agendado para {a.scheduled_at.strftime("%d/%m %H:%M")}',
                link='/agenda',
            )

        return a

    @staticmethod
    def excluir(atendimento_id, user_id=None):
        a = AtendimentoRepository.get_by_id(atendimento_id)
        if a:
            sid = a.studio_id
            cliente = a.cliente
            _sync_delete_event(a)
            AtendimentoRepository.soft_delete(a)
            ActivityService.log(
                studio_id=sid, user_id=user_id,
                acao='excluir', entidade='atendimento', entidade_id=atendimento_id,
                descricao=f'Atendimento de {cliente} removido'
            )


def _sync_create_event(atendimento):
    integration = CalendarIntegration.query.filter_by(studio_id=atendimento.studio_id).first()
    if not integration:
        return
    try:
        event_id = google_service.criar_evento(
            integration,
            current_app.config['GOOGLE_CLIENT_ID'],
            current_app.config['GOOGLE_CLIENT_SECRET'],
            cliente=atendimento.cliente,
            procedimento=atendimento.procedimento or '',
            joia=atendimento.joia_utilizada or '',
            valor=atendimento.valor or 0,
            pagamento=atendimento.forma_pagamento or '',
            piercer=atendimento.piercer or '',
            data_hora=atendimento.scheduled_at,
        )
        atendimento.google_event_id = event_id
        db.session.commit()
    except Exception as e:
        logger.warning('Erro ao criar evento no Google Agenda: %s', e)


def _sync_delete_event(atendimento):
    if not atendimento.google_event_id:
        return
    integration = CalendarIntegration.query.filter_by(studio_id=atendimento.studio_id).first()
    if not integration:
        return
    try:
        google_service.excluir_evento(
            integration,
            current_app.config['GOOGLE_CLIENT_ID'],
            current_app.config['GOOGLE_CLIENT_SECRET'],
            atendimento.google_event_id,
        )
    except Exception as e:
        logger.warning('Erro ao excluir evento do Google Agenda: %s', e)
