import sqlite3
import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'pirataria-body-art-os-secret'

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'pirataria.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT DEFAULT '',
            quantidade INTEGER DEFAULT 0,
            custo REAL DEFAULT 0.0,
            valor_venda REAL DEFAULT 0.0,
            local_fisico TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            procedimento TEXT DEFAULT '',
            joia_utilizada TEXT DEFAULT '',
            valor REAL DEFAULT 0.0,
            forma_pagamento TEXT DEFAULT '',
            piercer TEXT DEFAULT '',
            status TEXT DEFAULT 'Pago',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

init_db()

def hoje_resumo():
    conn = get_db()
    hoje = date.today().isoformat()
    row = conn.execute('''
        SELECT
            COALESCE(SUM(valor), 0) as faturamento,
            COUNT(*) as procedimentos,
            COALESCE(SUM(CASE WHEN forma_pagamento = 'Pix' THEN valor ELSE 0 END), 0) as total_pix,
            COALESCE(SUM(CASE WHEN forma_pagamento = 'Dinheiro' THEN valor ELSE 0 END), 0) as total_dinheiro,
            COALESCE(SUM(CASE WHEN forma_pagamento = 'Cartão' THEN valor ELSE 0 END), 0) as total_cartao
        FROM atendimentos
        WHERE DATE(created_at) = ?
    ''', (hoje,)).fetchone()
    conn.close()
    return dict(row)

def hoje_str():
    return date.today().strftime('%d/%m/%Y')

def contar_clientes_novos():
    conn = get_db()
    hoje = date.today().isoformat()
    row = conn.execute('''
        SELECT COUNT(DISTINCT cliente) as total FROM atendimentos WHERE DATE(created_at) = ?
    ''', (hoje,)).fetchone()
    conn.close()
    return row['total']

def estoque_baixo():
    conn = get_db()
    rows = conn.execute('SELECT * FROM produtos WHERE quantidade <= 3 ORDER BY quantidade ASC LIMIT 10').fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- ROTAS ---

@app.route('/')
def dashboard():
    resumo = hoje_resumo()
    clientes_novos = contar_clientes_novos()
    baixo = estoque_baixo()

    conn = get_db()
    hoje = date.today().isoformat()
    atendimentos_hoje = [dict(r) for r in conn.execute(
        'SELECT * FROM atendimentos WHERE DATE(created_at) = ? ORDER BY created_at DESC', (hoje,)
    ).fetchall()]
    conn.close()

    return render_template('dashboard.html',
                         faturamento=resumo['faturamento'],
                         procedimentos=resumo['procedimentos'],
                         total_pix=resumo['total_pix'],
                         total_dinheiro=resumo['total_dinheiro'],
                         total_cartao=resumo['total_cartao'],
                         clientes_novos=clientes_novos,
                         estoque_baixo=baixo,
                         atendimentos_hoje=atendimentos_hoje,
                         hoje_data=hoje_str())

# --- ESTOQUE ---

@app.route('/estoque')
def listar_estoque():
    conn = get_db()
    produtos = [dict(r) for r in conn.execute('SELECT * FROM produtos ORDER BY created_at DESC').fetchall()]
    conn.close()
    return render_template('estoque.html', produtos=produtos)

@app.route('/estoque/adicionar', methods=['POST'])
def adicionar_produto():
    nome = request.form.get('nome', '').strip()
    if not nome:
        flash('Nome do produto é obrigatório.', 'danger')
        return redirect(url_for('listar_estoque'))

    conn = get_db()
    conn.execute('''
        INSERT INTO produtos (nome, categoria, quantidade, custo, valor_venda, local_fisico)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        nome,
        request.form.get('categoria', '').strip(),
        int(request.form.get('quantidade', 0)),
        float(request.form.get('custo', 0)),
        float(request.form.get('valor_venda', 0)),
        request.form.get('local_fisico', '').strip()
    ))
    conn.commit()
    conn.close()
    flash('Produto adicionado com sucesso!', 'success')
    return redirect(url_for('listar_estoque'))

@app.route('/estoque/editar/<int:id>', methods=['POST'])
def editar_produto(id):
    conn = get_db()
    conn.execute('''
        UPDATE produtos SET nome=?, categoria=?, quantidade=?, custo=?, valor_venda=?, local_fisico=?
        WHERE id=?
    ''', (
        request.form.get('nome', '').strip(),
        request.form.get('categoria', '').strip(),
        int(request.form.get('quantidade', 0)),
        float(request.form.get('custo', 0)),
        float(request.form.get('valor_venda', 0)),
        request.form.get('local_fisico', '').strip(),
        id
    ))
    conn.commit()
    conn.close()
    flash('Produto atualizado!', 'success')
    return redirect(url_for('listar_estoque'))

@app.route('/estoque/excluir/<int:id>')
def excluir_produto(id):
    conn = get_db()
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Produto removido.', 'warning')
    return redirect(url_for('listar_estoque'))

# --- ATENDIMENTO ---

@app.route('/atendimento')
def listar_atendimentos():
    conn = get_db()
    atendimentos = [dict(r) for r in conn.execute('SELECT * FROM atendimentos ORDER BY created_at DESC').fetchall()]
    produtos = [dict(r) for r in conn.execute('SELECT nome FROM produtos ORDER BY nome').fetchall()]
    conn.close()
    return render_template('atendimento.html', atendimentos=atendimentos, produtos=produtos)

@app.route('/atendimento/novo', methods=['POST'])
def novo_atendimento():
    cliente = request.form.get('cliente', '').strip()
    if not cliente:
        flash('Nome do cliente é obrigatório.', 'danger')
        return redirect(url_for('listar_atendimentos'))

    joia = request.form.get('joia_utilizada', '').strip()
    valor = float(request.form.get('valor', 0))
    forma = request.form.get('forma_pagamento', '').strip()

    conn = get_db()
    conn.execute('''
        INSERT INTO atendimentos (cliente, procedimento, joia_utilizada, valor, forma_pagamento, piercer, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Pago')
    ''', (
        cliente,
        request.form.get('procedimento', '').strip(),
        joia,
        valor,
        forma,
        request.form.get('piercer', '').strip()
    ))

    if joia:
        produto = conn.execute(
            'SELECT id, quantidade FROM produtos WHERE LOWER(nome) LIKE LOWER(?) LIMIT 1',
            (f'%{joia}%',)
        ).fetchone()
        if produto and produto['quantidade'] > 0:
            conn.execute('UPDATE produtos SET quantidade = quantidade - 1 WHERE id = ?', (produto['id'],))

    conn.commit()
    conn.close()
    flash('Atendimento registrado com sucesso!', 'success')
    return redirect(url_for('listar_atendimentos'))

@app.route('/atendimento/excluir/<int:id>')
def excluir_atendimento(id):
    conn = get_db()
    conn.execute('DELETE FROM atendimentos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Atendimento removido.', 'warning')
    return redirect(url_for('listar_atendimentos'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
