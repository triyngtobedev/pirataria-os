def test_financeiro_page(client, auth_client, atendimento):
    resp = client.get('/financeiro/')
    assert resp.status_code == 200
    assert b'Receita' in resp.data


def test_financeiro_service(app, db, studio_user, atendimento):
    from app.services.financeiro_service import FinanceiroService
    from datetime import datetime, timezone
    s, u = studio_user
    with app.app_context():
        ano = datetime.now(timezone.utc).year
        meses = FinanceiroService.relatorio_mensal(s.id, ano)
        assert len(meses) == 12
        mes_atual = [m for m in meses if m['atendimentos'] > 0]
        assert len(mes_atual) >= 1
        assert mes_atual[0]['receita'] > 0
