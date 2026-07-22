def test_dashboard_page(client, auth_client):
    resp = client.get('/dashboard')
    assert resp.status_code == 200


def test_landing_page(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Pirataria' in resp.data


def test_dashboard_service(app, db, studio_user, atendimento):
    from app.services.dashboard_service import DashboardService
    s, u = studio_user
    with app.app_context():
        dados = DashboardService.dados(s.id)
        assert 'quote' in dados
        assert dados['procedimentos'] >= 1
        assert dados['total_produtos'] >= 0
