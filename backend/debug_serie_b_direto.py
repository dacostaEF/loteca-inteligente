#!/usr/bin/env python3
"""
Debug direto da Série B
"""
from models.classificacao_db import classificacao_db

def debug_serie_b():
    print("🔍 [DEBUG] Testando classificacao_db.get_classificacao_serie_b()...")
    
    try:
        dados = classificacao_db.get_classificacao_serie_b()
        print(f"📊 [DEBUG] Retornou {len(dados)} registros")
        
        if dados:
            print("🏆 [DEBUG] Primeiros 3:")
            for i, time in enumerate(dados[:3]):
                print(f"   {i+1}. {time}")
        else:
            print("❌ [DEBUG] Nenhum dado retornado!")
            
            # Verificar diretamente no banco
            import sqlite3
            conn = sqlite3.connect("models/tabelas_classificacao.db")
            cursor = conn.cursor()
            
            # Verificar se tabela existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='classificacao_serie_b'")
            exists = cursor.fetchone()
            print(f"🗄️ [DEBUG] Tabela existe: {bool(exists)}")
            
            if exists:
                cursor.execute("SELECT COUNT(*) FROM classificacao_serie_b")
                count = cursor.fetchone()[0]
                print(f"📊 [DEBUG] Total de registros: {count}")
                
                if count > 0:
                    cursor.execute("SELECT time, posicao, pontos FROM classificacao_serie_b ORDER BY posicao LIMIT 3")
                    times = cursor.fetchall()
                    print("🏆 [DEBUG] Dados diretos:")
                    for time in times:
                        print(f"   {time[1]}º {time[0]} - {time[2]} pts")
            
            conn.close()
            
    except Exception as e:
        print(f"❌ [DEBUG] Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_serie_b()
