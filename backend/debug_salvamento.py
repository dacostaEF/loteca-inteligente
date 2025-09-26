#!/usr/bin/env python3
"""
Debug do salvamento - verificar se chegou no banco
"""
import sqlite3
import os
from datetime import datetime

def verificar_salvamento():
    print("🔍 [DEBUG] Verificando último salvamento no banco...")
    
    db_path = "models/tabelas_classificacao.db"
    
    if not os.path.exists(db_path):
        print(f"❌ [DEBUG] Banco não existe: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Verificar últimas atualizações na Série A
        print("\n📊 [DEBUG] === SÉRIE A ===")
        cursor.execute("""
            SELECT time, pontos, jogos, vitorias, data_atualizacao 
            FROM classificacao_serie_a 
            ORDER BY data_atualizacao DESC 
            LIMIT 5
        """)
        
        serie_a = cursor.fetchall()
        for row in serie_a:
            print(f"   {row['time']}: {row['pontos']} pts - Atualizado: {row['data_atualizacao']}")
        
        # Verificar últimas atualizações na Série B
        print("\n📊 [DEBUG] === SÉRIE B ===")
        cursor.execute("""
            SELECT time, pontos, jogos, vitorias, updated_at 
            FROM classificacao_serie_b 
            ORDER BY updated_at DESC 
            LIMIT 5
        """)
        
        serie_b = cursor.fetchall()
        for row in serie_b:
            print(f"   {row['time']}: {row['pontos']} pts - Atualizado: {row['updated_at']}")
        
        # Verificar mudanças recentes (última hora)
        print("\n⏰ [DEBUG] === MUDANÇAS RECENTES ===")
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
            SELECT 'Serie A' as serie, time, pontos, data_atualizacao as timestamp
            FROM classificacao_serie_a 
            WHERE data_atualizacao >= datetime('now', '-1 hour')
            UNION
            SELECT 'Serie B' as serie, time, pontos, updated_at as timestamp
            FROM classificacao_serie_b 
            WHERE updated_at >= datetime('now', '-1 hour')
            ORDER BY timestamp DESC
        """)
        
        recentes = cursor.fetchall()
        if recentes:
            for row in recentes:
                print(f"   {row['serie']}: {row['time']} - {row['timestamp']}")
        else:
            print("   ❌ Nenhuma alteração na última hora")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ [DEBUG] Erro: {e}")

if __name__ == "__main__":
    verificar_salvamento()
