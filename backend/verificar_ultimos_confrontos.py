#!/usr/bin/env python3
import sqlite3

def verificar_ultimos_confrontos():
    conn = sqlite3.connect('models/tabelas_classificacao.db')
    cursor = conn.cursor()
    
    # Verificar São Paulo
    cursor.execute("SELECT time, ultimos_confrontos, ultimos_jogos FROM classificacao_serie_a WHERE time LIKE '%Sao Paulo%'")
    sao_paulo = cursor.fetchall()
    print('São Paulo:', sao_paulo)
    
    # Verificar Grêmio
    cursor.execute("SELECT time, ultimos_confrontos, ultimos_jogos FROM classificacao_serie_a WHERE time LIKE '%Gremio%'")
    gremio = cursor.fetchall()
    print('Grêmio:', gremio)
    
    # Verificar todos os times com hífens
    cursor.execute("SELECT time, ultimos_confrontos, ultimos_jogos FROM classificacao_serie_a WHERE ultimos_confrontos LIKE '%-%' OR ultimos_jogos LIKE '%-%'")
    com_hifens = cursor.fetchall()
    print('Times com hífens:', com_hifens)
    
    conn.close()

if __name__ == "__main__":
    verificar_ultimos_confrontos()
