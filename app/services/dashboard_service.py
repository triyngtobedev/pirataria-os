from datetime import datetime, timedelta, timezone, date
from app import db
from app.repositories.atendimento_repo import AtendimentoRepository
from app.repositories.produto_repo import ProdutoRepository
from app.models.schemas import Atendimento, CalendarIntegration
from app.services.notification_service import NotificationService
from app.quotes import quote_of_the_day

BRT = timezone(timedelta(hours=-3))


class DashboardService:

    @staticmethod
    def dados(studio_id):
        agora = datetime.now(BRT)
        hoje = agora.date()

        resumo_dia = AtendimentoRepository.resumo_dia(studio_id)
        resumo_mes = AtendimentoRepository.resumo_mes(studio_id)
        estoque_baixo = ProdutoRepository.estoque_baixo(studio_id)
        atendimentos_hoje = AtendimentoRepository.listar_hoje(studio_id)
        total_produtos = ProdutoRepository.total_ativo(studio_id)
        proximos = Atendimento.query.filter(
            Atendimento.studio_id == studio_id,
            Atendimento.is_active == True,
            Atendimento.scheduled_at.isnot(None),
            db.func.date(Atendimento.scheduled_at) >= hoje,
        ).order_by(Atendimento.scheduled_at.asc()).limit(3).all()

        notificacoes = NotificationService.listar_nao_lidas(studio_id, limite=5)

        tem_calendario = CalendarIntegration.query.filter_by(studio_id=studio_id).first() is not None

        return {
            'quote': quote_of_the_day(),
            'hoje_data': hoje.strftime('%d/%m/%Y'),
            'faturamento': resumo_dia.faturamento,
            'procedimentos': resumo_dia.procedimentos,
            'total_pix': resumo_dia.total_pix,
            'total_dinheiro': resumo_dia.total_dinheiro,
            'total_cartao': resumo_dia.total_cartao,
            'clientes_novos': resumo_dia.clientes_novos,
            'mes_faturamento': resumo_mes.faturamento,
            'mes_procedimentos': resumo_mes.procedimentos,
            'mes_clientes': resumo_mes.clientes,
            'estoque_baixo': estoque_baixo,
            'atendimentos_hoje': atendimentos_hoje,
            'total_produtos': total_produtos,
            'proximos_agendamentos': proximos,
            'notificacoes': notificacoes,
            'tem_calendario': tem_calendario,
        }
