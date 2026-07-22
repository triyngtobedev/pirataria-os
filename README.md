<p align="center">
  <img src="app/static/logos/logo-principal.png" alt="Pirataria Body Art" width="320">
</p>

<p align="center">
  <strong>Sistema de gestão profissional para estúdios de body piercing</strong>
  <br>
  <sub>Feito por piercers, para piercers — com a cara da cultura old school</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-em%20produ%C3%A7%C3%A3o-d4a843?style=flat-square">
  <img src="https://img.shields.io/badge/python-3.12-3776AB?style=flat-square&logo=python">
  <img src="https://img.shields.io/badge/flask-3.1-000?style=flat-square&logo=flask">
  <img src="https://img.shields.io/badge/postgresql-16-336791?style=flat-square&logo=postgresql">
  <img src="https://img.shields.io/badge/licen%C3%A7a-MIT-2ecc71?style=flat-square">
</p>

---

## ✦ Sobre

O **Pirataria Body Art OS** é um sistema web completo para gerenciamento de estúdios de body piercing. Nasceu da necessidade real de um estúdio brasileiro que precisava de um software à altura da sua arte — nada de planilhas ou sistemas genéricos.

Controle seu catálogo de joias, registre atendimentos com baixa automática de estoque, gerencie insumos, acompanhe seu faturamento mensal — tudo com a identidade visual old school que representa a cultura do body piercing.

### Recursos

- **Catálogo de Joias** — Cadastro completo com tipo, material, local de aplicação, custo, valor de venda, foto opcional e filtros de ordenação (nome, quantidade, custo, venda)
- **Atendimentos** — Registro com baixa automática de estoque, formas de pagamento (Pix, Dinheiro, Cartão), busca e ordenação por cliente, valor e data
- **Insumos** — Controle de estoque de materiais de consumo (luvas, agulhas, antissépticos etc.) com ordenação por nome, quantidade e custo
- **Financeiro** — Planilha anual com receita, custo, lucro e divisão por forma de pagamento, ordenável por mês, atendimentos, receita e lucro
- **Multi-estúdio** — Cadastro separado por estúdio, dados 100% isolados
- **Dashboard** — Visão geral do dia: faturamento, procedimentos, clientes, estoque baixo + frase motivacional diária
- **Tema dark/light** — Alternador com 3 modos: claro, escuro e automático (sistema)
- **PWA** — Instala como aplicativo no celular via navegador
- **Docker** — Pronto para deploy em produção
- **Landing page** — Apresentação do sistema para visitantes

---

## ✦ Stack

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.12 + Flask 3.1 |
| ORM | SQLAlchemy 3.1 |
| Frontend | Bootstrap 5.3 + Bootstrap Icons |
| Fonte | Pirata One + Playfair Display |
| Banco | SQLite (dev) / PostgreSQL 16 (prod) |
| Auth | Flask-Login + Werkzeug |
| Container | Docker + Gunicorn |
| Deploy | Railway |

---

## ✦ Arquitetura

```
pirataria-os/
├── run.py                 # Entry point da aplicação
├── config.py              # Configurações (dev/prod)
├── Dockerfile             # Container para produção
├── docker-compose.yml     # PostgreSQL + app (dev local)
├── railway.json           # Configuração Railway
│
├── app/                   # Pacote principal
│   ├── __init__.py        # App factory (create_app)
│   ├── models/
│   │   └── schemas.py     # Studio, User, Produto, Atendimento, Insumo
│   ├── blueprints/
│   │   ├── auth.py        # Login, registro, logout
│   │   ├── dashboard.py   # Dashboard principal
│   │   ├── estoque.py     # Catálogo de joias
│   │   ├── atendimento.py # Registro de atendimentos
│   │   ├── insumos.py     # Controle de insumos
│   │   └── financeiro.py  # Planilha financeira mensal
│   ├── middleware/
│   │   └── tenant.py      # Isolamento multi-estúdio
│   ├── templates/         # Jinja2 templates
│   ├── static/            # CSS, JS, imagens, uploads
│   ├── quotes.py          # 30 frases motivacionais
│   └── seed.py            # Dados de demonstração
│
└── requirements.txt
```

---

## ✦ Funcionalidades em detalhe

### Dashboard
Visão consolidada do dia: faturamento, número de procedimentos, clientes atendidos, formas de pagamento, itens com estoque baixo, frase motivacional diária e tema adaptável (claro/escuro/sistema).

### Catálogo de Joias
Cadastro completo com nome, tipo (argola, barbell, banana etc.), material (titânio, aço, ouro 18k etc.), local de aplicação, quantidade em estoque, custo, valor de venda e **foto opcional** com visualização em modal expandido. Busca por texto em tempo real, filtro por status de estoque, favoritos e ordenação por nome, quantidade, custo ou valor de venda.

### Atendimentos
Registro de atendimentos com busca inteligente de joias no estoque. Ao selecionar uma joia, a quantidade é baixada automaticamente. Suporte a múltiplas formas de pagamento.

### Insumos
Controle de estoque para materiais de consumo: luvas, agulhas, antissépticos, embalagens etc. Com categorias, unidades de medida (unidade, par, ml, g), custo unitário e fornecedor.

### Financeiro
Planilha anual com receita, custo estimado das joias utilizadas, lucro e quebra por forma de pagamento (Pix, Dinheiro, Cartão) mês a mês, com totais acumulados.

### Multi-estúdio
Cada estúdio tem seu próprio cadastro, login e dados completamente isolados — ideal para redes de estúdios ou franquias.

---

## ✦ Como rodar localmente

### Com Python

```bash
# Clone
git clone https://github.com/triyngtobedev/pirataria-os.git
cd pirataria-os

# Ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependências
pip install -r requirements.txt

# Rodar
python run.py
```

Acesse `http://localhost:5000` e cadastre seu estúdio.

### Com Docker

```bash
docker-compose up --build
```

Acesse `http://localhost:5000`.

---

## ✦ Deploy

### Railway (recomendado)

1. Faça fork do repositório
2. Crie um projeto no [Railway](https://railway.app) a partir do GitHub
3. Adicione um banco PostgreSQL
4. Configure as variáveis:
   - `FLASK_ENV=production`
   - `SECRET_KEY=uma-chave-segura`
5. Pronto! O Railway detecta o Dockerfile e faz o build automaticamente

---

## ✦ Licença

MIT — Use, modifique e distribua à vontade.

---

<p align="center">
  <sub>✦ Pirataria Body Art OS v0.2 ✦</sub>
  <br>
  <sub>Feito com dedicação para a cultura do body piercing brasileiro</sub>
</p>
