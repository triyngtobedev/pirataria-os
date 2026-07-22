from app.repositories.atendimento_repo import AtendimentoRepository
from app.repositories.produto_repo import ProdutoRepository


class FinanceiroService:

    NOMES_MESES = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro',
    ]

    @classmethod
    def relatorio_mensal(cls, studio_id, ano):
        meses = []
        for mes in range(1, 13):
            row, atendimentos = AtendimentoRepository.total_por_mes(studio_id, ano, mes)

            custo_total = 0
            for at in atendimentos:
                if at.joia_utilizada:
                    prod = ProdutoRepository.find_by_name(studio_id, at.joia_utilizada)
                    if prod:
                        custo_total += prod.custo

            meses.append({
                'mes': mes,
                'nome_mes': cls.NOMES_MESES[mes - 1],
                'atendimentos': row.total,
                'receita': row.receita,
                'custo': custo_total,
                'lucro': row.receita - custo_total,
                'pix': row.pix,
                'dinheiro': row.dinheiro,
                'cartao': row.cartao,
            })

        return meses
