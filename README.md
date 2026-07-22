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

---

## ✦ Recursos

### Agenda e Agendamentos
- **Agenda inteligente** com visão de próximos e passados
- **Sincronização bidirecional** com Google Calendar e Google Tasks
- **Campo de data/hora** no registro de atendimento para agendar serviços futuros
- **Badge com contagem** de próximos agendamentos na Agenda
- **Horários no fuso BRT** (America/Sao Paulo) — sem confusão de UTC

### Notificações
- **Notificações no Dashboard** ao criar agendamentos futuros
- **Notificação push PWA** via Web Push API — o piercer recebe alerta no celular mesmo com o navegador fechado
- **Inscrição por clique** no sininho 🔔 do navbar

### Catálogo de Joias
Cadastro completo com nome, tipo (argola, barbell, banana etc.), material (titânio, aço, ouro 18k etc.), local de aplicação, quantidade em estoque, custo, valor de venda e foto opcional com visualização em modal expandido. Busca por texto em tempo real, filtro por status de estoque, favoritos e ordenação por nome, quantidade, custo ou valor de venda.

### Atendimentos
Registro de atendimentos com busca inteligente de joias no estoque. Ao selecionar uma joia, a quantidade é baixada automaticamente. Suporte a múltiplas formas de pagamento (Pix, Dinheiro, Cartão, Débito, Crédito).

### Insumos
Controle de estoque para materiais de consumo: luvas, agulhas, antissépticos, embalagens etc. Com categorias, unidades de medida (unidade, par, ml, g), custo unitário e fornecedor.

### Financeiro
Planilha anual com receita, custo estimado das joias utilizadas, lucro e quebra por forma de pagamento (Pix, Dinheiro, Cartão) mês a mês, com totais acumulados.

### Dashboard
Visão geral do dia: faturamento, procedimentos, clientes, estoque baixo, próximos agendamentos, notificações + frase motivacional diária com rodízio de 30 frases.

### Autenticação e Segurança
- Login, cadastro e logout
- **Recuperação de senha** via email (SMTP) com fallback mostrando o link na tela
- **Alteração de senha** pelo usuário logado (🔑 no navbar)
- Multi-estúdio com dados 100% isolados por tenant

### Google Calendar + Tasks
- Conexão OAuth2 com escopos de calendário e tarefas
- Sincronização automática a cada 5 minutos (APScheduler)
- Criação/atualização/exclusão de eventos ao registrar/remover atendimentos
- Importação de eventos do calendário e tarefas do Google Tasks como atendimentos
- Extração automática de horário do título da tarefa (ex: "14:30 - Cliente")
- Conversão de fuso horário para BRT

### Experiência do Usuário
- **Tema dark/light** — alternador com 3 modos: claro, escuro e automático (sistema)
- **PWA** — instala como aplicativo no celular via navegador com service worker para cache offline
- **Responsivo** — funciona em desktop e mobile
- **Interface old school** com fontes Pirata One + Playfair Display

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
| Task scheduling | APScheduler 3.11 |
| Google APIs | google-api-python-client, google-auth-oauthlib |
| Push notification | pywebpush + Web Push API |
| Container | Docker + Gunicorn |
| Deploy | Railway |

---

## ✦ Novidades da v0.2

- **Sistema de notificações** com modelo próprio e exibição no Dashboard
- **Notificação push PWA** no celular para novos agendamentos
- **Campo de data/hora** no formulário de atendimento (agendamento futuro)
- **Correção de fuso horário** — tudo em BRT, sem confusão com UTC
- **Recuperação de senha** por email com fallback na tela
- **Alteração de senha** pelo próprio usuário
- **Badge de contagem** de próximos agendamentos na Agenda
- **Re-sync forçado** ao reiniciar para corrigir horários antigos
- **Correção na exibição** de valores zero (R$ 0) na Agenda
- **Compatibilidade PostgreSQL** nas migrations (boolean, timestamp)

---

## ✦ Arquitetura

```
pirataria-os/
├── run.py                 # Entry point da aplicação
├── config.py              # Configurações (dev/prod)
├── Dockerfile             # Container para produção
├── docker-compose.yml     # PostgreSQL + app (dev local)
├── railway.json           # Configuração Railway
├── startup.sh             # Script de inicialização (migrations + gunicorn)
│
├── app/                   # Pacote principal
│   ├── __init__.py        # App factory (create_app)
│   ├── models/
│   │   └── schemas.py     # Studio, User, Produto, Atendimento, Insumo,
│   │                      # CalendarIntegration, Notification, PushSubscription
│   ├── blueprints/
│   │   ├── auth.py        # Login, registro, logout, recuperação de senha
│   │   ├── dashboard.py   # Dashboard principal
│   │   ├── estoque.py     # Catálogo de joias
│   │   ├── atendimento.py # Registro de atendimentos
│   │   ├── insumos.py     # Controle de insumos
│   │   ├── financeiro.py  # Planilha financeira mensal
│   │   ├── calendar.py    # Google Calendar + Tasks + Agenda
│   │   └── notifications.py # Inscrição push PWA
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── atendimento_service.py
│   │   ├── dashboard_service.py
│   │   ├── google_service.py    # Google Calendar/Tasks API
│   │   ├── sync_service.py      # Sincronização bidirecional
│   │   ├── notification_service.py
│   │   ├── push_service.py      # Envio de push notification
│   │   └── email_service.py     # Envio de email (SMTP)
│   ├── repositories/       # Padrão Repository (CRUD)
│   ├── middleware/
│   │   └── tenant.py      # Isolamento multi-estúdio
│   ├── templates/          # Jinja2 templates
│   ├── static/             # CSS, JS, imagens, uploads
│   ├── quotes.py           # 30 frases motivacionais
│   └── seed.py             # Dados de demonstração
│
├── migrations/             # Alembic (9 migrações)
└── requirements.txt
```

---

## ✦ Funcionalidades em detalhe

### Dashboard
Visão consolidada do dia: faturamento, número de procedimentos, clientes atendidos, formas de pagamento, itens com estoque baixo, próximos agendamentos, notificações de novos agendamentos e frase motivacional diária. Tema adaptável (claro/escuro/sistema).

### Agenda
Lista de próximos agendamentos (com data futura) e atendimentos passados. Sincronização manual ou automática com Google Calendar. Badge com contagem de próximos.

### Google Calendar / Tasks
Conecte sua conta Google e sincronize eventos e tarefas automaticamente. Eventos do calendário viram atendimentos no sistema. Tarefas com horário no título (ex: "14:30 - Maria") têm o horário extraído automaticamente.

### Notificações Push
Ative as notificações pelo sininho 🔔 no navbar (requer PWA instalado). Ao criar um agendamento futuro, todos os dispositivos inscritos no estúdio recebem um push com os detalhes.

### Recuperação de Senha
Na tela de login, clique em "Esqueci minha senha". Digite o email cadastrado. Se o SMTP estiver configurado, um link de recuperação é enviado por email. Caso contrário, o link é exibido diretamente na tela.

---

## ✦ Variáveis de Ambiente

| Variável | Obrigatório | Descrição |
|----------|-------------|-----------|
| `FLASK_ENV` | Não | `development` ou `production` |
| `SECRET_KEY` | Sim (prod) | Chave secreta do Flask |
| `DATABASE_URL` | Não | URL do banco (default: SQLite) |
| `GOOGLE_CLIENT_ID` | Não | ID do app Google OAuth |
| `GOOGLE_CLIENT_SECRET` | Não | Secret do app Google OAuth |
| `GOOGLE_REDIRECT_URI` | Não | URL de callback OAuth |
| `VAPID_PUBLIC_KEY` | Não | Chave pública para push notification |
| `VAPID_PRIVATE_KEY` | Não | Chave privada para push notification |
| `SMTP_HOST` | Não | Servidor SMTP (ex: smtp.gmail.com) |
| `SMTP_PORT` | Não | Porta SMTP (default: 587) |
| `SMTP_USER` | Não | Usuário SMTP |
| `SMTP_PASS` | Não | Senha SMTP |
| `SMTP_FROM` | Não | Remetente dos emails |

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
4. Configure as variáveis de ambiente (veja tabela acima)
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
