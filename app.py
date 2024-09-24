from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar_bd():
    conn = sqlite3.connect('voluntarios.db')
    return conn

def criar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS voluntarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            telefone TEXT,
            atividade TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM voluntarios')
    voluntarios = cursor.fetchall()
    conn.close()
    return render_template('index.html', voluntarios=voluntarios)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        atividade = request.form['atividade']

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO voluntarios (nome, email, telefone, atividade) VALUES (?, ?, ?, ?)', 
                       (nome, email, telefone, atividade))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('adicionar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM voluntarios WHERE id = ?', (id,))
    voluntario = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        atividade = request.form['atividade']

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE voluntarios 
            SET nome = ?, email = ?, telefone = ?, atividade = ? 
            WHERE id = ?
        ''', (nome, email, telefone, atividade, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('editar.html', voluntario=voluntario)

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM voluntarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)
