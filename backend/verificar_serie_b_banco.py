#!/usr/bin/env python3
"""
Verificar e criar estrutura para Série B
"""
import sqlite3
import os

def verificar_e_criar_serie_b():
    print("🔍 [SÉRIE B] Verificando estrutura do banco...")
    
    db_path = "models/tabelas_classificacao.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se tabela Serie B existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='classificacao_serie_b'")
        serie_b_exists = cursor.fetchone()
        
        if not serie_b_exists:
            print("❌ [SÉRIE B] Tabela classificacao_serie_b não existe. Criando...")
            
            # Criar tabela Serie B baseada na Serie A
            cursor.execute("""
                CREATE TABLE classificacao_serie_b (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time VARCHAR(100) NOT NULL,
                    posicao INTEGER NOT NULL,
                    pontos INTEGER DEFAULT 0,
                    jogos INTEGER DEFAULT 0,
                    vitorias INTEGER DEFAULT 0,
                    empates INTEGER DEFAULT 0,
                    derrotas INTEGER DEFAULT 0,
                    gols_pro INTEGER DEFAULT 0,
                    gols_contra INTEGER DEFAULT 0,
                    saldo_gols INTEGER DEFAULT 0,
                    aproveitamento DECIMAL(5,2) DEFAULT 0.0,
                    ultimos_jogos VARCHAR(10) DEFAULT 'NNNNN',
                    zona VARCHAR(20),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Inserir times da Série B (20 times)
            times_serie_b = [
                "Santos", "Novorizontino", "Sport", "Mirassol", "Ceará",
                "Vila Nova", "América-MG", "Operário", "Goiás", "Avaí",
                "Paysandu", "Coritiba", "Amazonas", "Chapecoense", "CRB",
                "Ponte Preta", "Ituano", "Botafogo-SP", "Brusque", "Guarani"
            ]
            
            for i, time in enumerate(times_serie_b, 1):
                cursor.execute("""
                    INSERT INTO classificacao_serie_b 
                    (time, posicao, pontos, jogos, vitorias, empates, derrotas, gols_pro, gols_contra, saldo_gols, aproveitamento)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (time, i, 0, 0, 0, 0, 0, 0, 0, 0, 0.0))
            
            conn.commit()
            print("✅ [SÉRIE B] Tabela criada com 20 times!")
            
        else:
            print("✅ [SÉRIE B] Tabela já existe!")
            
        # Verificar registros
        cursor.execute("SELECT COUNT(*) FROM classificacao_serie_b")
        count = cursor.fetchone()[0]
        print(f"📊 [SÉRIE B] Total de times: {count}")
        
        if count > 0:
            cursor.execute("SELECT time, posicao, pontos FROM classificacao_serie_b ORDER BY posicao LIMIT 5")
            times = cursor.fetchall()
            print("🏆 [SÉRIE B] Top 5:")
            for time in times:
                print(f"   {time[1]}º {time[0]} - {time[2]} pts")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ [SÉRIE B] Erro: {e}")
        return False

if __name__ == "__main__":
    verificar_e_criar_serie_b()
