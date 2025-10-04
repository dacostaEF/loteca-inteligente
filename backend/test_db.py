import sqlite3

# Conectar ao banco
conn = sqlite3.connect('models/tabelas_classificacao.db')
cursor = conn.cursor()

# Verificar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tabelas:', [t[0] for t in tables])

# Verificar dados
try:
    cursor.execute('SELECT COUNT(*) FROM classificacao_serie_a')
    count_a = cursor.fetchone()[0]
    print(f'Série A: {count_a} registros')
except Exception as e:
    print(f'Erro Série A: {e}')

try:
    cursor.execute('SELECT COUNT(*) FROM classificacao_serie_b')
    count_b = cursor.fetchone()[0]
    print(f'Série B: {count_b} registros')
except Exception as e:
    print(f'Erro Série B: {e}')

# Verificar alguns dados
try:
    cursor.execute('SELECT * FROM classificacao_serie_a LIMIT 3')
    dados_a = cursor.fetchall()
    print(f'Primeiros dados Série A: {dados_a}')
except Exception as e:
    print(f'Erro dados Série A: {e}')

conn.close()
