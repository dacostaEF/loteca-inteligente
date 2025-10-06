import sqlite3

conn = sqlite3.connect('backend/models/tabelas_classificacao.db')
cursor = conn.cursor()

# Verificar todos os times
cursor.execute('SELECT time, ultimos_confrontos, ultimos_jogos FROM classificacao_serie_a ORDER BY posicao')
todos = cursor.fetchall()

print('=== TODOS OS TIMES ===')
for time in todos:
    print(f'{time[0]}: ultimos_confrontos="{time[1]}", ultimos_jogos="{time[2]}"')

conn.close()
