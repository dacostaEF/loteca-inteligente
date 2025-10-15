#!/usr/bin/env python3
"""
Script para inserir dados reais da Série A Italiana 2025-26
Baseado na imagem fornecida pelo usuário
"""

import sqlite3
import os

def insert_serie_a_italiana_data():
    """Inserir dados reais da Série A Italiana"""
    
    db_path = "tabelas_classificacao.db"
    
    if not os.path.exists(db_path):
        print(f"ERRO: Banco {db_path} nao encontrado!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Inserindo dados da Serie A Italiana 2025-26...")
        
        # Primeiro, criar a tabela se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classificacao_serie_a_italiana (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                posicao INTEGER NOT NULL,
                time TEXT NOT NULL,
                pontos INTEGER DEFAULT 0,
                jogos INTEGER DEFAULT 0,
                vitorias INTEGER DEFAULT 0,
                empates INTEGER DEFAULT 0,
                derrotas INTEGER DEFAULT 0,
                gols_pro INTEGER DEFAULT 0,
                gols_contra INTEGER DEFAULT 0,
                saldo_gols INTEGER DEFAULT 0,
                aproveitamento REAL DEFAULT 0.0,
                ultimos_confrontos TEXT DEFAULT '',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Limpar dados existentes
        cursor.execute("DELETE FROM classificacao_serie_a_italiana")
        
        # Dados reais da Série A Italiana 2025-26 (baseado na imagem)
        dados_serie_a = [
            (1, 'Napoli', 15, 6, 5, 0, 1, 12, 6, 6, 83.3, 'VVVLV'),
            (2, 'Roma', 15, 6, 5, 0, 1, 7, 2, 5, 83.3, 'LVVVV'),
            (3, 'Milan', 13, 6, 4, 1, 1, 9, 3, 6, 72.2, 'VVVVE'),
            (4, 'Inter', 12, 6, 4, 0, 2, 17, 8, 9, 66.7, 'VLVVV'),
            (5, 'Juventus', 12, 6, 3, 3, 0, 9, 5, 4, 66.7, 'VVEEE'),
            (6, 'Atalanta', 10, 6, 2, 4, 0, 11, 5, 6, 55.6, 'VVEED'),
            (7, 'Bologna', 10, 6, 3, 1, 2, 9, 5, 4, 55.6, 'VLVVE'),
            (8, 'Como', 9, 6, 2, 3, 1, 7, 5, 2, 50.0, 'LVVEE'),
            (9, 'Sassuolo', 9, 6, 3, 0, 3, 8, 8, 0, 50.0, 'VLLVV'),
            (10, 'Cremonese', 9, 6, 2, 3, 1, 7, 8, -1, 50.0, 'EEEVL'),
            (11, 'Cagliari', 8, 6, 2, 2, 2, 6, 6, 0, 44.4, 'VVEDE'),
            (12, 'Udinese', 8, 6, 2, 2, 2, 6, 9, -3, 44.4, 'VVLLE'),
            (13, 'Lazio', 7, 6, 2, 1, 3, 10, 7, 3, 38.9, 'VLLLV'),
            (14, 'Parma', 5, 6, 1, 2, 3, 3, 7, -4, 27.8, 'LEEDL'),
            (15, 'Lecce', 5, 6, 1, 2, 3, 5, 10, -5, 27.8, 'LLEDV'),
            (16, 'Torino', 5, 6, 1, 2, 3, 5, 13, -8, 27.8, 'VLLLE'),
            (17, 'Fiorentina', 3, 6, 0, 3, 3, 4, 8, -4, 16.7, 'LEEDL'),
            (18, 'Verona', 3, 6, 0, 3, 3, 2, 9, -7, 16.7, 'LEEDL'),
            (19, 'Genoa', 2, 6, 0, 2, 4, 3, 9, -6, 11.1, 'LEEDL'),
            (20, 'Pisa', 2, 6, 0, 2, 4, 3, 10, -7, 11.1, 'LLEDL')
        ]
        
        # Inserir dados
        cursor.executemany("""
            INSERT INTO classificacao_serie_a_italiana 
            (posicao, time, pontos, jogos, vitorias, empates, derrotas, 
             gols_pro, gols_contra, saldo_gols, aproveitamento, ultimos_confrontos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados_serie_a)
        
        # Verificar inserção
        cursor.execute("SELECT COUNT(*) FROM classificacao_serie_a_italiana")
        count = cursor.fetchone()[0]
        
        print(f"OK: {count} times inseridos na Serie A Italiana!")
        
        # Mostrar top 5
        cursor.execute("""
            SELECT posicao, time, pontos, jogos, vitorias, empates, derrotas, 
                   gols_pro, gols_contra, saldo_gols, aproveitamento
            FROM classificacao_serie_a_italiana 
            ORDER BY posicao LIMIT 5
        """)
        
        times = cursor.fetchall()
        print("\nTop 5 da Serie A Italiana:")
        for time in times:
            pos, nome, pts, jogos, vit, emp, der, gp, gc, sg, ap = time
            print(f"   {pos}o {nome}: {pts}pts ({vit}V-{emp}E-{der}D) | GP:{gp} GC:{gc} SG:{sg:+d} | {ap:.1f}%")
        
        conn.commit()
        conn.close()
        
        print("\nDados da Serie A Italiana inseridos com sucesso!")
        print("Agora voce pode selecionar 'Serie A Italiana' na Central Admin!")
        
        return True
        
    except Exception as e:
        print(f"ERRO ao inserir dados: {e}")
        return False

if __name__ == "__main__":
    insert_serie_a_italiana_data()
