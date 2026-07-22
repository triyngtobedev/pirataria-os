from datetime import datetime, timezone, date
from app.repositories.atendimento_repo import AtendimentoRepository
from app.repositories.produto_repo import ProdutoRepository
from app.models.schemas import Atendimento, CalendarIntegration
from app.quotes import quote_of_the_day


class DashboardService:

    @staticmethod
    def dados(studio_id):
        hoje = date.today()

        resumo_dia = AtendimentoRepository.resumo_dia(studio_id)
        resumo_mes = AtendimentoRepository.resumo_mes(studio_id)
        estoque_baixo = ProdutoRepository.estoque_baixo(studio_id)
        atendimentos_hoje = AtendimentoRepository.listar_hoje(studio_id)
        total_produtos = ProdutoRepository.total_ativo(studio_id)

        agora = datetime.now(timezone.utc).replace(tzinfo=None)
        proximos = Atendimento.query.filter(
            Atendimento.studio_id == studio_id,
            Atendimento.is_active == True,
        ).order_by(Atendimento.scheduled_at.asc().nullsfirst()).limit(50).all()
        proximos = [a for a in proximos if not a.scheduled_at or a.scheduled_at >= agora][:3]

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
            'tem_calendario': tem_calendario,
        }
