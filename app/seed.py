from datetime import datetime, timedelta, date
import random
from app import db
from app.models.schemas import Produto, Atendimento

_produtos_seed = [
    {"nome": "Argola Clicker Dourada 8mm", "categoria": "Argola", "quantidade": 12, "custo": 35, "valor_venda": 120, "local_fisico": "Gaveta 1"},
    {"nome": "Argola Clicker Prata 8mm", "categoria": "Argola", "quantidade": 8, "custo": 30, "valor_venda": 100, "local_fisico": "Gaveta 1"},
    {"nome": "Argola Clicker Dourada 10mm", "categoria": "Argola", "quantidade": 6, "custo": 38, "valor_venda": 130, "local_fisico": "Gaveta 1"},
    {"nome": "Argola Titanio Preto 8mm", "categoria": "Argola", "quantidade": 5, "custo": 40, "valor_venda": 140, "local_fisico": "Gaveta 1"},
    {"nome": "Argola Titanio Dourado 8mm", "categoria": "Argola", "quantidade": 10, "custo": 42, "valor_venda": 150, "local_fisico": "Gaveta 2"},
    {"nome": "Barbell Reto Titanio 12mm", "categoria": "Barbell", "quantidade": 15, "custo": 25, "valor_venda": 90, "local_fisico": "Gaveta 2"},
    {"nome": "Barbell Curvo Titanio 10mm", "categoria": "Barbell", "quantidade": 10, "custo": 28, "valor_venda": 95, "local_fisico": "Gaveta 2"},
    {"nome": "Barbell Reto Acrilico 14mm", "categoria": "Barbell", "quantidade": 20, "custo": 8, "valor_venda": 40, "local_fisico": "Gaveta 3"},
    {"nome": "Lobulo Argola Dourada 6mm", "categoria": "Lóbulo", "quantidade": 7, "custo": 32, "valor_venda": 110, "local_fisico": "Gaveta 3"},
    {"nome": "Lobulo Argola Prata 6mm", "categoria": "Lóbulo", "quantidade": 10, "custo": 28, "valor_venda": 95, "local_fisico": "Gaveta 3"},
    {"nome": "Lobulo Argola Titanio 6mm", "categoria": "Lóbulo", "quantidade": 2, "custo": 38, "valor_venda": 130, "local_fisico": "Gaveta 3"},
    {"nome": "Umbilical Barbell Curvo Titanio", "categoria": "Umbilical", "quantidade": 4, "custo": 35, "valor_venda": 120, "local_fisico": "Gaveta 4"},
    {"nome": "Umbilical Barbell Curvo Acrilico", "categoria": "Umbilical", "quantidade": 3, "custo": 10, "valor_venda": 50, "local_fisico": "Gaveta 4"},
    {"nome": "Microdermal Base Titanio", "categoria": "Microdermal", "quantidade": 6, "custo": 20, "valor_venda": 80, "local_fisico": "Gaveta 4"},
    {"nome": "Microdermal Top Cristal", "categoria": "Microdermal", "quantidade": 0, "custo": 15, "valor_venda": 60, "local_fisico": "Gaveta 4"},
    {"nome": "Argola Nariz Titanio Dourada 1.2mm", "categoria": "Nariz", "quantidade": 8, "custo": 22, "valor_venda": 80, "local_fisico": "Gaveta 5"},
    {"nome": "Argola Nariz Titanio Prata 1.2mm", "categoria": "Nariz", "quantidade": 3, "custo": 20, "valor_venda": 75, "local_fisico": "Gaveta 5"},
    {"nome": "Argola Nariz Acrilico 1.2mm", "categoria": "Nariz", "quantidade": 15, "custo": 5, "valor_venda": 30, "local_fisico": "Gaveta 5"},
    {"nome": "Pino Nariz Titanio com Cristal", "categoria": "Nariz", "quantidade": 1, "custo": 18, "valor_venda": 70, "local_fisico": "Gaveta 5"},
    {"nome": "BANANA Barbell Titanio 8mm", "categoria": "Banana", "quantidade": 9, "custo": 30, "valor_venda": 105, "local_fisico": "Gaveta 2"},
]

_atendimentos_seed = [
    {"cliente": "Ana Beatriz", "procedimento": "Piercing Nariz", "joia": "Argola Nariz Titanio Dourada 1.2mm", "valor": 180, "pagamento": "Pix", "dias_atras": 0},
    {"cliente": "Carlos Eduardo", "procedimento": "Piercing Lóbulo", "joia": "Lobulo Argola Dourada 6mm", "valor": 150, "pagamento": "Pix", "dias_atras": 0},
    {"cliente": "Marina Silva", "procedimento": "Piercing Umbilical", "joia": "Umbilical Barbell Curvo Titanio", "valor": 220, "pagamento": "Cartão", "dias_atras": 0},
    {"cliente": "Rafael Oliveira", "procedimento": "Microdermal", "joia": "Microdermal Base Titanio", "valor": 250, "pagamento": "Dinheiro", "dias_atras": 0},
    {"cliente": "Juliana Costa", "procedimento": "Piercing Nariz", "joia": "Argola Nariz Titanio Prata 1.2mm", "valor": 175, "pagamento": "Pix", "dias_atras": 1},
    {"cliente": "Pedro Santos", "procedimento": "Troca de Joia", "joia": "Argola Clicker Dourada 8mm", "valor": 80, "pagamento": "Pix", "dias_atras": 1},
    {"cliente": "Larissa Mendes", "procedimento": "Piercing Lóbulo", "joia": "Lobulo Argola Prata 6mm", "valor": 140, "pagamento": "Dinheiro", "dias_atras": 2},
    {"cliente": "Thiago Almeida", "procedimento": "Barbell Reto", "joia": "Barbell Reto Titanio 12mm", "valor": 160, "pagamento": "Cartão", "dias_atras": 3},
    {"cliente": "Fernanda Lima", "procedimento": "Piercing Nariz", "joia": "Argola Clicker Prata 8mm", "valor": 170, "pagamento": "Pix", "dias_atras": 5},
    {"cliente": "Gabriel Rocha", "procedimento": "Microdermal Top", "joia": "Microdermal Top Cristal", "valor": 100, "pagamento": "Pix", "dias_atras": 5},
    {"cliente": "Amanda Torres", "procedimento": "Piercing Umbilical", "joia": "Umbilical Barbell Curvo Acrilico", "valor": 150, "pagamento": "Dinheiro", "dias_atras": 7},
    {"cliente": "Bruno Carvalho", "procedimento": "Troca de Joia", "joia": "Argola Titanio Dourado 8mm", "valor": 80, "pagamento": "Pix", "dias_atras": 7},
    {"cliente": "Camila Ribeiro", "procedimento": "Piercing Banana", "joia": "BANANA Barbell Titanio 8mm", "valor": 200, "pagamento": "Cartão", "dias_atras": 10},
    {"cliente": "Diego Martins", "procedimento": "Piercing Nariz", "joia": "Argola Nariz Acrilico 1.2mm", "valor": 120, "pagamento": "Pix", "dias_atras": 12},
    {"cliente": "Elisa Campos", "procedimento": "Piercing Lóbulo", "joia": "Lobulo Argola Titanio 6mm", "valor": 190, "pagamento": "Dinheiro", "dias_atras": 15},
]

def seed_studio(studio_id):
    if Produto.query.filter_by(studio_id=studio_id).first():
        return

    for p in _produtos_seed:
        db.session.add(Produto(studio_id=studio_id, **p))

    agora = datetime.utcnow()
    for a in _atendimentos_seed:
        created = agora - timedelta(days=a["dias_atras"], hours=random.randint(9, 18))
        db.session.add(Atendimento(
            studio_id=studio_id,
            cliente=a["cliente"],
            procedimento=a["procedimento"],
            joia_utilizada=a["joia"],
            valor=a["valor"],
            forma_pagamento=a["pagamento"],
            piercer="Padrinho",
            status="Pago",
            created_at=created
        ))

    db.session.commit()
