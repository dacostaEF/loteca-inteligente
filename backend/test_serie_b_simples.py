#!/usr/bin/env python3
"""
Teste simples da Série B
"""
import sqlite3
import os

def test_serie_b_simples():
    print("🔍 [TEST] Teste simples da Série B...")
    
    db_path = "models/tabelas_classificacao.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Banco não existe: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Verificar se tabela existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='classificacao_serie_b'
        """)
        
        table_exists = cursor.fetchone()
        print(f"📋 [TEST] Tabela existe: {bool(table_exists)}")
        
        if not table_exists:
            print("❌ Tabela não existe!")
            return
        
        # Testar query básica
        cursor.execute("SELECT COUNT(*) as total FROM classificacao_serie_b")
        count = cursor.fetchone()['total']
        print(f"📊 [TEST] Total de registros: {count}")
        
        # Testar query completa (similar ao método)
        cursor.execute("""
            SELECT 
                id, posicao, time, pontos, jogos, vitorias, empates, derrotas,
                gols_pro, gols_contra, saldo_gols, aproveitamento,
                ultimos_jogos, zona, created_at, updated_at
            FROM classificacao_serie_b 
            ORDER BY posicao ASC
            LIMIT 3
        """)
        
        rows = cursor.fetchall()
        dados = [dict(row) for row in rows]
        
        print(f"🏆 [TEST] Query retornou: {len(dados)} registros")
        
        if dados:
            print("🎯 [TEST] Primeiro registro:")
            print(f"    {dados[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ [TEST] Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_serie_b_simples()
