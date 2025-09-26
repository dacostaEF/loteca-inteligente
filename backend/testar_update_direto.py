#!/usr/bin/env python3
"""
Testar update diretamente na classe
"""
from models.classificacao_db import classificacao_db

def testar_update_direto():
    print("🧪 [TESTE] Testando update direto na classe...")
    
    # Teste 1: Série A
    print("\n1️⃣ [TESTE] Série A...")
    resultado_a = classificacao_db.update_time_stats(
        time_id=1,
        campo='pontos', 
        valor='99',
        serie='a'
    )
    print(f"   Resultado Série A: {resultado_a}")
    
    # Teste 2: Série B  
    print("\n2️⃣ [TESTE] Série B...")
    resultado_b = classificacao_db.update_time_stats(
        time_id=1,
        campo='pontos',
        valor='88', 
        serie='b'
    )
    print(f"   Resultado Série B: {resultado_b}")
    
    # Verificar se funcionou
    print("\n🔍 [VERIFICAÇÃO] Checando se salvou...")
    
    import sqlite3
    conn = sqlite3.connect("models/tabelas_classificacao.db")
    cursor = conn.cursor()
    
    # Série A
    cursor.execute("SELECT time, pontos FROM classificacao_serie_a WHERE id = 1")
    serie_a = cursor.fetchone()
    print(f"   Série A ID 1: {serie_a}")
    
    # Série B  
    cursor.execute("SELECT time, pontos FROM classificacao_serie_b WHERE id = 1")
    serie_b = cursor.fetchone()
    print(f"   Série B ID 1: {serie_b}")
    
    conn.close()

if __name__ == "__main__":
    testar_update_direto()
